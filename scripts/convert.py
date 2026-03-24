#!/usr/bin/env python3
"""
Конвертер: простые домены → MRS формат для Mihomo
"""
import struct
import sys

def convert_to_mrs(input_file: str, output_file: str):
    # Читаем домены
    with open(input_file, 'r', encoding='utf-8') as f:
        lines = [line.strip() for line in f if line.strip() and not line.startswith('#')]
    
    # Формируем правила DOMAIN-SUFFIX
    rules = []
    for line in lines:
        if line.startswith(('DOMAIN-', 'IP-CIDR', 'PROCESS-', 'AND(', 'OR(')):
            rules.append(line)
        else:
            rules.append(f'DOMAIN-SUFFIX,{line}')
    
    # Генерируем MRS (правильный бинарный формат)
    with open(output_file, 'wb') as f:
        # Заголовок
        f.write(b'MRS\x00')                    # Magic: 4 байта
        f.write(struct.pack('<I', 1))          # Version: 4 байта (little-endian uint32)
        f.write(struct.pack('<I', len(rules))) # Count: 4 байта (little-endian uint32)
        
        # Каждое правило: 2 байта длина + данные
        for rule in rules:
            rule_bytes = rule.encode('utf-8')
            f.write(struct.pack('<H', len(rule_bytes)))  # Length: 2 байта (little-endian uint16)
            f.write(rule_bytes)                          # Data
    
    print(f"✅ Конвертировано {len(rules)} правил в MRS формат")
    print(f"📁 Выходной файл: {output_file}")

if __name__ == '__main__':
    if len(sys.argv) != 3:
        print("Использование: python convert.py input.txt output.mrs")
        sys.exit(1)
    convert_to_mrs(sys.argv[1], sys.argv[2])
