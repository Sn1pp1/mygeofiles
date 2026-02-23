#!/usr/bin/env python3
import json
import requests
import subprocess
import tempfile
from pathlib import Path

SOURCES_FILE = Path("scripts/sources.json")
OUTPUT_DIR = Path("files")
SING_BOX = "sing-box"

GEOSITE_BASE = "https://raw.githubusercontent.com/hydraponique/roscomvpn-geosite/master/data"
GEOIP_BASE = "https://raw.githubusercontent.com/hydraponique/roscomvpn-geoip/master/release/text"

def load_sources():
    with open(SOURCES_FILE, "r", encoding="utf-8") as f:
        return json.load(f)

def download_text(url):
    print(f"  ↓ {url}")
    resp = requests.get(url, timeout=30)
    resp.raise_for_status()
    
    items = []
    for line in resp.text.splitlines():
        line = line.strip()
        if line and not line.startswith("#") and not line.startswith("!"):
            items.append(line)
    return items

def is_ip_cidr(item):
    return "/" in item or (item.count(".") == 3 and all(c.isdigit() or c == "." for c in item))

def create_rule_json(items):
    domains = []
    domain_suffix = []
    ip_cidr = []
    
    for item in items:
        if is_ip_cidr(item):
            ip_cidr.append(item)
        elif item.startswith("."):
            domain_suffix.append(item)
        else:
            domains.append(item)
    
    rules = {}
    if domains:
        rules["domain"] = domains[:10000]
    if domain_suffix:
        rules["domain_suffix"] = domain_suffix[:10000]
    if ip_cidr:
        rules["ip_cidr"] = ip_cidr[:10000]
    
    if not rules:
        return None
    
    return {"version": 1, "rules": [rules]}

def compile_srs(json_data, output_path):
    with tempfile.NamedTemporaryFile(mode="w", suffix=".json", delete=False) as tmp:
        json_path = Path(tmp.name)
        json.dump(json_data, tmp, indent=2, ensure_ascii=False)
    
    print(f"  ⚙ Compiling → {output_path.name}")
    result = subprocess.run(
        [SING_BOX, "rule-set", "compile", str(json_path), "-o", str(output_path)],
        capture_output=True, text=True
    )
    
    json_path.unlink(missing_ok=True)
    
    if result.returncode != 0:
        print(f"  ❌ Error: {result.stderr}")
        return False
    return True

def build_category(name, config):
    print(f"\n📦 Building '{name}'...")
    all_items = set()
    
    for cat in config.get("geosite", []):
        url = f"{GEOSITE_BASE}/{cat}/{cat}.txt"
        try:
            items = download_text(url)
            all_items.update(items)
            print(f"    + {cat}: {len(items)} items")
        except Exception as e:
            print(f"    ⚠ {cat}: {e}")
    
    for cat in config.get("geoip", []):
        url = f"{GEOIP_BASE}/{cat}.txt"
        try:
            items = download_text(url)
            all_items.update(items)
            print(f"    + geoip/{cat}: {len(items)} items")
        except Exception as e:
            print(f"    ⚠ geoip/{cat}: {e}")
    
    if not all_items:
        print(f"  ⚠ No items for '{name}', skipping")
        return False
    
    print(f"  Total: {len(all_items)} unique items")
    
    rule_json = create_rule_json(list(all_items))
    if not rule_json:
        return False
    
    srs_path = OUTPUT_DIR / f"{name}.srs"
    if compile_srs(rule_json, srs_path):
        print(f"  ✅ Created {srs_path.name} ({srs_path.stat().st_size} bytes)")
        return True
    return False

def main():
    print("🚀 RoscomVPN SRS Builder")
    OUTPUT_DIR.mkdir(exist_ok=True)
    
    sources = load_sources()
    
    for category in ["block", "direct"]:
        if category in sources:
            build_category(category, sources[category])
    
    print("\n✅ Done! Files:")
    for f in sorted(OUTPUT_DIR.glob("*.srs")):
        print(f"  • {f.name}")

if __name__ == "__main__":
    main()
