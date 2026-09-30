import re
from collections import Counter

with open(r'C:\Users\abhiy\OneDrive\Desktop\hackathon rivals\index.html', 'r', encoding='utf-8') as f:
    html = f.read()

# Check duplicate IDs
ids = re.findall(r'id="([^"]+)"', html)
id_map = {}
for id in ids:
    id_map[id] = id_map.get(id, 0) + 1

print('=== Duplicate IDs ===')
for k, v in id_map.items():
    if v > 1:
        print(f'{k}: x{v}')

# Check for unmatched tags
open_tags = re.findall(r'<([a-z][a-z0-9]*)[^>]*>', html)
close_tags = re.findall(r'</([a-z][a-z0-9]*)>', html)

open_count = Counter(open_tags)
close_count = Counter(close_tags)

print('\n=== Unmatched Tags ===')
all_tags = set(open_count.keys()) | set(close_count.keys())
for tag in sorted(all_tags):
    o = open_count.get(tag, 0)
    c = close_count.get(tag, 0)
    if o != c:
        print(f'{tag}: open={o} close={c} diff={o-c}')

# Check for common JS issues in script
script_match = re.search(r'<script>([\s\S]*?)</script>', html)
if script_match:
    script = script_match.group(1)
    lines = script.split('\n')
    print('\n=== Potential JS Issues ===')
    for i, line in enumerate(lines, 1):
        stripped = line.strip()
        if re.match(r'^(return|throw|break|continue)\s+\S', stripped) and not stripped.endswith(';'):
            print(f'Line {i}: Missing semicolon - {stripped[:80]}')
        if 'console.log' in stripped and not stripped.endswith(';') and not stripped.endswith('{'):
            print(f'Line {i}: console.log missing semicolon - {stripped[:80]}')
        # Check for const/let/var without semicolon
        if re.match(r'^(const|let|var)\s+\w+\s*=', stripped) and not stripped.endswith(';') and not stripped.endswith(','):
            # Check if it's the end of statement
            if not (stripped.endswith('{') or stripped.endswith('(') or stripped.endswith('[')):
                # Might be continued on next line
                pass
        # Check for potential undefined variables
        if 'document.getElementById' in stripped and '.value' in stripped:
            # Check if element exists
            pass