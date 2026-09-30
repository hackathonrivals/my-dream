import re
from collections import Counter

with open(r'C:\Users\abhiy\OneDrive\Desktop\hackathon rivals\index.html', 'r', encoding='utf-8') as f:
    html = f.read()

# Find actual HTML IDs (not in script)
# Split into head/body and script
parts = re.split(r'<script>', html)
head_body = parts[0]
script = ''.join(parts[1:]).split('</script>')[0] if len(parts) > 1 else ''

# Check duplicate IDs in HTML only
ids = re.findall(r'id="([^"]+)"', head_body)
id_map = {}
for id in ids:
    id_map[id] = id_map.get(id, 0) + 1

print('=== Duplicate HTML IDs ===')
for k, v in id_map.items():
    if v > 1:
        print(f'{k}: x{v}')

# Check all element IDs referenced in JS
js_ids = re.findall(r'document\.getElementById\([\'"]([^\'"]+)[\'"]\)', script)
print('\n=== JS getElementById calls ===')
for id in sorted(set(js_ids)):
    # Check if element exists in HTML
    if f'id="{id}"' not in head_body and f"id='{id}'" not in head_body:
        print(f'MISSING: {id}')

# Check querySelector calls
qs_ids = re.findall(r'querySelector\([\'"](#[^\'"]+)[\'"]\)', script)
print('\n=== JS querySelector calls ===')
for id in sorted(set(qs_ids)):
    clean = id[1:]  # remove #
    if f'id="{clean}"' not in head_body and f"id='{clean}'" not in head_body:
        print(f'MISSING: {clean}')

# Check for undefined variables in JS
print('\n=== Potential undefined variables ===')
# Look for variables used before declaration
var_declarations = set(re.findall(r'(?:const|let|var)\s+(\w+)', script))
# Look for variable usage
var_usages = set(re.findall(r'\b([a-zA-Z_$][a-zA-Z0-9_$]*)\b', script))
# Filter to likely variable names (not keywords)
keywords = {'const','let','var','function','return','if','else','for','while','do','try','catch','finally','switch','case','default','break','continue','new','this','super','class','extends','import','export','async','await','typeof','instanceof','in','of','from','as','default','yield','void','delete','debugger','with','arguments','eval','undefined','null','true','false','Infinity','NaN','Object','Array','String','Number','Boolean','Date','RegExp','Error','Promise','JSON','Math','console','window','document','navigator','localStorage','sessionStorage','fetch','setTimeout','setInterval','clearTimeout','clearInterval','parseInt','parseFloat','isNaN','isFinite','encodeURI','encodeURIComponent','decodeURI','decodeURIComponent'}
potential_vars = var_usages - var_declarations - keywords
# Filter to only camelCase or PascalCase or underscore vars
potential_vars = [v for v in potential_vars if re.match(r'^[a-z][a-zA-Z0-9]*$', v) and len(v) > 2]
# Remove common DOM methods/properties
dom_methods = {'querySelector','querySelectorAll','getElementById','getElementsByClassName','getElementsByTagName','addEventListener','removeEventListener','appendChild','removeChild','insertBefore','replaceChild','createElement','createTextNode','setAttribute','getAttribute','removeAttribute','classList','style','value','innerHTML','textContent','dataset','parentNode','parentElement','childNodes','children','firstChild','lastChild','nextSibling','previousSibling','scrollTop','scrollHeight','offsetTop','offsetHeight','clientWidth','clientHeight','focus','blur','click','submit','reset','preventDefault','stopPropagation','stopImmediatePropagation','target','currentTarget','key','code','which','button','clientX','clientY','pageX','pageY','screenX','screenY','shiftKey','ctrlKey','altKey','metaKey','bubbles','cancelable','defaultPrevented','eventPhase','isTrusted','timeStamp','type','detail','view','relatedTarget','fromElement','toElement','charCode','keyCode','wheelDelta','detail','buttons','button','movementX','movementY','offsetX','offsetY','layerX','layerY'}
potential_vars = [v for v in potential_vars if v not in dom_methods]
print('\n=== Potentially undefined variables ===')
for v in sorted(potential_vars)[:50]:
    print(v)

# Check for syntax issues in JS
print('\n=== JS Syntax Issues ===')
script_lines = script.split('\n')
for i, line in enumerate(script_lines, 1):
    stripped = line.strip()
    # Check for const/let/var without semicolon at end of statement
    if re.match(r'^(const|let|var)\s+\w+\s*=\s*[^=,;{}[\]()]+$', stripped) and not stripped.endswith(';'):
        print(f'Line {i}: Missing semicolon - {stripped[:100]}')
    # Check for function declarations without semicolon (if not ending with {)
    if re.match(r'^function\s+\w+\s*\([^)]*\)\s*[^{]*$', stripped):
        print(f'Line {i}: Function declaration issue - {stripped[:100]}')
    # Check for arrow functions assigned to variables without semicolon
    if re.match(r'^(const|let|var)\s+\w+\s*=\s*\([^)]*\)\s*=>\s*[^;{]*$', stripped):
        print(f'Line {i}: Arrow function missing semicolon - {stripped[:100]}')