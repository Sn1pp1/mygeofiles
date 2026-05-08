#!/usr/bin/env python3
import json
import os

def convert_to_singbox_format(input_file, output_file):
    """Convert domain list to Sing-box rule set format"""
    
    # Read domains from txt file
    domains = []
    with open(input_file, 'r', encoding='utf-8') as f:
        for line in f:
            domain = line.strip()
            if domain and not domain.startswith('#'):
                domains.append(domain)
    
    # Create Sing-box rule set structure
    rule_set = {
        "version": 1,
        "rules": [
            {
                "domain_suffix": domains
            }
        ]
    }
    
    # Write to JSON file
    with open(output_file, 'w', encoding='utf-8') as f:
        json.dump(rule_set, f, indent=2, ensure_ascii=False)
    
    print(f"Converted {len(domains)} domains to {output_file}")

if __name__ == "__main__":
    # Get the directory where the script is located
    script_dir = os.path.dirname(os.path.abspath(__file__))
    root_dir = os.path.dirname(script_dir)
    
    input_path = os.path.join(root_dir, 'files', 'domain-list.txt')
    output_path = os.path.join(root_dir, 'files', 'domain-list.json')
    
    convert_to_singbox_format(input_path, output_path)
