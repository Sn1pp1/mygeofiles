#!/usr/bin/env python3
import json
import os
import sys
import subprocess

def parse_json_file(filepath):
    """Parse JSON and normalize to rule groups for sing-box"""
    rules = {
        'domain_suffix': [],
        'domain_keyword': [],
        'domain_regex': [],
        'domain': [],
        'ip_cidr': []
    }
    
    with open(filepath, 'r', encoding='utf-8') as f:
        data = json.load(f)
    
    # Формат: {"version": 1, "rules": [...]}
    if 'rules' in data:
        for rule in data['rules']:
            for rule_type, values in rule.items():
                if rule_type in rules and isinstance(values, list):
                    rules[rule_type].extend(values)
    # Формат: {"domain_suffix": [...]}
    else:
        for rule_type, values in data.items():
            if rule_type in rules and isinstance(values, list):
                rules[rule_type].extend(values)
    
    # Удаляем пустые категории и дубликаты
    return {k: list(set(v)) for k, v in rules.items() if v}

def create_rule_set_json(rules, output_path):
    """Create proper JSON structure for sing-box rule-set compile"""
    rule_set = {
        "version": 1,
        "rules": []
    }
    
    # Добавляем только непустые категории в правильном порядке
    for rule_type in ['domain', 'domain_suffix', 'domain_keyword', 'domain_regex', 'ip_cidr']:
        if rules.get(rule_type):
            rule_set["rules"].append({rule_type: rules[rule_type]})
    
    with open(output_path, 'w', encoding='utf-8') as f:
        json.dump(rule_set, f, indent=2, ensure_ascii=False)
    
    total = sum(len(v) for v in rules.values())
    print(f"📄 Created rule set with {total} rules: {output_path}")
    return total

def compile_to_srs(input_json, output_srs, sing_box_path='sing-box'):
    """Compile JSON to binary .srs using sing-box"""
    try:
        result = subprocess.run(
            [sing_box_path, 'rule-set', 'compile', input_json, '-o', output_srs],
            capture_output=True,
            text=True,
            check=True
        )
        print(f"✅ Compiled: {output_srs}")
        return True
    except subprocess.CalledProcessError as e:
        print(f"❌ Compilation failed: {e.stderr}")
        return False
    except FileNotFoundError:
        print(f"❌ sing-box not found. Please install it first.")
        return False

def main():
    script_dir = os.path.dirname(os.path.abspath(__file__))
    root_dir = os.path.dirname(script_dir)
    
    # Пути к файлам
    json_input = os.path.join(root_dir, 'files', 'domain-list.json')
    temp_rules = os.path.join(root_dir, 'files', '.temp-rules.json')
    srs_output = os.path.join(root_dir, 'files', 'domain-list.srs')
    
    # Читаем только JSON (TXT больше не нужен для этого скрипта)
    if not os.path.exists(json_input):
        print(f"❌ Input file not found: {json_input}")
        print("💡 Hint: Run convert-to-json.yml first to generate domain-list.json")
        sys.exit(1)
    
    print(f"📥 Reading from JSON: {json_input}")
    rules = parse_json_file(json_input)
    
    if not rules:
        print("⚠️  No valid rules found in input file")
        sys.exit(0)
    
    # Создаём промежуточный JSON для компиляции
    print("🔧 Preparing rule set JSON...")
    create_rule_set_json(rules, temp_rules)
    
    # Компилируем в .srs
    print("🔨 Compiling to .srs format...")
    if compile_to_srs(temp_rules, srs_output):
        size = os.path.getsize(srs_output)
        print(f"🎉 Success! Output: {srs_output} ({size} bytes)")
    else:
        sys.exit(1)
    
    # Очищаем временный файл
    if os.path.exists(temp_rules):
        os.remove(temp_rules)

if __name__ == "__main__":
    main()
