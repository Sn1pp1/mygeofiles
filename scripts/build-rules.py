#!/usr/bin/env python3
import json
import logging
import requests
import subprocess
import tempfile
import time
import ipaddress
from pathlib import Path

# ============================================
# 🔧 CONFIGURATION
# ============================================
SOURCES_FILE = Path("scripts/sources.json")
OUTPUT_DIR = Path("files")
SING_BOX = "sing-box"

# ✅ Вернул константы
REQUEST_TIMEOUT = 30
REQUEST_RETRIES = 3
REQUEST_DELAY = 2

GEOSITE_BASE = "https://raw.githubusercontent.com/hydraponique/roscomvpn-geosite/master/data"
GEOIP_BASE = "https://raw.githubusercontent.com/hydraponique/roscomvpn-geoip/master/release/text"

# ============================================
# 🔧 LOGGING SETUP
# ============================================
logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s [%(levelname)s] %(message)s",
    datefmt="%H:%M:%S"
)
logger = logging.getLogger(__name__)

# ============================================
# 🔧 HELPER FUNCTIONS
# ============================================
def load_sources():
    """Загружает sources.json"""
    try:
        with open(SOURCES_FILE, "r", encoding="utf-8") as f:
            return json.load(f)
    except FileNotFoundError:
        logger.error(f"❌ Sources file not found: {SOURCES_FILE}")
        return {}
    except json.JSONDecodeError as e:
        logger.error(f"❌ Invalid JSON in {SOURCES_FILE}: {e}")
        return {}

def check_sing_box():
    """Проверяет что sing-box установлен и работает"""
    try:
        result = subprocess.run(
            [SING_BOX, "version"],
            capture_output=True, text=True, timeout=10
        )
        if result.returncode == 0:
            version = result.stdout.strip().split('\n')[0]
            logger.info(f"✅ sing-box found: {version}")
            return True
    except FileNotFoundError:
        logger.error(f"❌ {SING_BOX} not found in PATH")
    except subprocess.TimeoutExpired:
        logger.error(f"❌ {SING_BOX} check timed out")
    except Exception as e:
        logger.error(f"❌ Error checking {SING_BOX}: {e}")
    return False

def download_text_with_retry(url, retries=REQUEST_RETRIES):
    """Скачивает текст с ретраями и обработкой ошибок"""
    headers = {"User-Agent": "Mozilla/5.0 (compatible; SRS-Builder/1.0)"}
    
    for attempt in range(1, retries + 1):
        try:
            logger.debug(f"  ↓ {url} (attempt {attempt}/{retries})")
            resp = requests.get(url, timeout=REQUEST_TIMEOUT, headers=headers)
            resp.raise_for_status()
            
            items = []
            for line in resp.text.splitlines():
                line = line.strip()
                if line and not line.startswith("#") and not line.startswith("!"):
                    items.append(line)
            return items
            
        except requests.exceptions.RequestException as e:
            logger.warning(f"  ⚠ Attempt {attempt} failed: {e}")
            if attempt < retries:
                time.sleep(REQUEST_DELAY * attempt)
            else:
                logger.error(f"  ❌ Failed after {retries} attempts: {url}")
                return []

def is_valid_ip_cidr(item):
    """Проверяет что строка — валидный IP/CIDR"""
    try:
        ipaddress.ip_network(item, strict=False)
        return True
    except ValueError:
        return False

def create_rule_json(items):
    """Создаёт JSON для компиляции в SRS — БЕЗ ЛИМИТОВ"""
    domains = []
    domain_suffix = []
    ip_cidr = []
    
    for item in items:
        if is_valid_ip_cidr(item):
            ip_cidr.append(item)
        elif item.startswith("."):
            domain_suffix.append(item)
        else:
            domains.append(item)
    
    # ✅ Все правила сохраняются без обрезки
    rules = {}
    if domains:
        rules["domain"] = domains
    if domain_suffix:
        rules["domain_suffix"] = domain_suffix
    if ip_cidr:
        rules["ip_cidr"] = ip_cidr
    
    if not rules:
        return None
    
    return {"version": 1, "rules": [rules]}

def compile_srs(json_data, output_path):
    """Компилирует JSON в SRS через sing-box"""
    with tempfile.NamedTemporaryFile(mode="w", suffix=".json", delete=False) as tmp:
        json_path = Path(tmp.name)
        json.dump(json_data, tmp, indent=2, ensure_ascii=False)
    
    try:
        logger.info(f"  ⚙ Compiling → {output_path.name}")
        result = subprocess.run(
            [SING_BOX, "rule-set", "compile", str(json_path), "-o", str(output_path)],
            capture_output=True, text=True, timeout=60
        )
        
        if result.returncode != 0:
            logger.error(f"  ❌ Compile error: {result.stderr.strip()}")
            return False
        
        logger.info(f"  ✅ Created {output_path.name} ({output_path.stat().st_size:,} bytes)")
        return True
        
    except subprocess.TimeoutExpired:
        logger.error("  ❌ Compile timed out")
        return False
    except Exception as e:
        logger.error(f"  ❌ Compile failed: {e}")
        return False
    finally:
        json_path.unlink(missing_ok=True)

def build_category(name, config):
    """Собирает правила для категории"""
    logger.info(f"\n📦 Building '{name}'...")
    all_items = set()
    
    for cat in config.get("geosite", []):
        url = f"{GEOSITE_BASE}/{cat}"
        items = download_text_with_retry(url)
        if items:
            all_items.update(items)
            logger.info(f"    + {cat}: {len(items)} items")
        else:
            logger.warning(f"    ⚠ {cat}: empty or failed")
    
    for cat in config.get("geoip", []):
        url = f"{GEOIP_BASE}/{cat}.txt"
        items = download_text_with_retry(url)
        if items:
            all_items.update(items)
            logger.info(f"    + geoip/{cat}: {len(items)} items")
        else:
            logger.warning(f"    ⚠ geoip/{cat}: empty or failed")
    
    if not all_items:
        logger.warning(f"  ⚠ No items for '{name}', skipping")
        return False
    
    logger.info(f"  Total: {len(all_items):,} unique items")
    
    rule_json = create_rule_json(list(all_items))
    if not rule_json:
        logger.warning(f"  ⚠ No valid rules for '{name}'")
        return False
    
    srs_path = OUTPUT_DIR / f"{name}.srs"
    return compile_srs(rule_json, srs_path)

# ============================================
# 🔧 MAIN
# ============================================
def main():
    logger.info("🚀 Sing-box SRS Builder starting...")
    
    if not check_sing_box():
        logger.error("❌ Cannot proceed without sing-box")
        return 1
    
    OUTPUT_DIR.mkdir(exist_ok=True)
    
    if not SOURCES_FILE.exists():
        logger.error(f"❌ Sources file not found: {SOURCES_FILE}")
        return 1
    
    sources = load_sources()
    if not sources:
        logger.error("❌ Failed to load sources")
        return 1
    
    success_count = 0
    for category in ["block", "direct"]:
        if category in sources:
            if build_category(category, sources[category]):
                success_count += 1
        else:
            logger.warning(f"  ⚠ Category '{category}' not found in sources")
    
    logger.info(f"\n✅ Done! Built {success_count}/2 categories")
    
    for f in sorted(OUTPUT_DIR.glob("*.srs")):
        logger.info(f"  • {f.name} ({f.stat().st_size:,} bytes)")
    
    return 0 if success_count > 0 else 1

if __name__ == "__main__":
    exit(main())
