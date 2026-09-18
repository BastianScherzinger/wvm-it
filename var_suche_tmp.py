import json, re
d = json.load(open('content.json', encoding='utf-8'))
def walk(o, p=''):
    if isinstance(o, dict):
        for k, v in o.items():
            walk(v, p + '.' + k)
    elif isinstance(o, list):
        for i, v in enumerate(o):
            walk(v, p + f'[{i}]')
    elif isinstance(o, str) and re.search('Kontakt-, Anfrage|gelöscht|Speicherdauer|Frist', o):
        print(p)
        for m in re.finditer('.{0,300}(Kontakt-, Anfrage|gelöscht|Speicherdauer|Frist).{0,500}', o):
            print('  >>', m.group(0)); print()
walk(d)
