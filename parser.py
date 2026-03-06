import json, sys, os, re
def extract(obj, target_type):
    res = []
    if isinstance(obj, dict):
        for k, v in obj.items():
            if target_type == 'geosite':
                if k in ['domain_suffix', 'domain']: res.extend(v)
                elif k == 'domain_keyword': res.extend(['keyword:' + x for x in v])
                elif k == 'domain_regex':
                    for r in v:
                        try: re.compile(r); res.append('regexp:' + r)
                        except: continue
                else: res.extend(extract(v, target_type))
            elif target_type == 'geoip':
                if k == 'ip_cidr': res.extend(v)
                else: res.extend(extract(v, target_type))
    elif isinstance(obj, list):
        for item in obj: res.extend(extract(item, target_type))
    return res
try:
    target, filename = sys.argv[1], sys.argv[2]
    if not os.path.exists('temp.json'): sys.exit(0)
    with open('temp.json', 'r', encoding='utf-8') as f: data = json.load(f)
    results = list(set(filter(None, extract(data, target))))
    if results:
        with open(f'data/{target}/{filename}', 'w', encoding='utf-8') as f_out:
            f_out.write('\n'.join(results) + '\n')
        print(f"✅ Parsed {len(results)} rules")
except Exception as e: print(f"Parser error: {e}")
