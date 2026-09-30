import re

with open(r'C:\Users\abhiy\OneDrive\Desktop\hackathon rivals\index.html', 'r', encoding='utf-8') as f:
    html = f.read()

issues = []

# 1. Check for duplicate function definitions
funcs = re.findall(r'function (\w+)\s*\(', html)
from collections import Counter
dup_funcs = [f for f, c in Counter(funcs).items() if c > 1]
if dup_funcs:
    issues.append(f'Duplicate functions: {dup_funcs}')

# 2. Check for missing closing braces in functions
open_braces = html.count('{')
close_braces = html.count('}')
if open_braces != close_braces:
    issues.append(f'Brace mismatch: {open_braces} open vs {close_braces} close')

# 3. Check for template literal issues in JS
script_match = re.search(r'<script>([\s\S]*?)</script>', html)
if script_match:
    script = script_match.group(1)
    backticks = script.count('`')
    if backticks % 2 != 0:
        issues.append(f'Unclosed template literals: {backticks} backticks')

# 3. Check for undefined critical variables
critical_vars = ['supabase', 'showToast', 'submitAuth', 'updateFormFields', 'attachRunButton']
for var in critical_vars:
    if f'{var}(' in script and f'function {var}' not in script and f'const {var}' not in script and f'let {var}' not in script:
        issues.append(f'{var} used but not defined')

# 5. Check for async without try/catch in critical paths
if 'await ' in script:
    # Find all async functions
    async_funcs = re.findall(r'async function (\w+)', script)
    for func in async_funcs:
        # Check if it has try/catch
        func_body = re.search(rf'async function {func}\s*\([^)]*\)\s*\{{([\s\S]*?)\n\}}', script)
        if func_body and 'try {' not in func_body.group(1) and 'await' in func_body.group(1):
            issues.append(f'async function {func} has await but no try/catch')

print('=== Issues Found ===')
for issue in issues:
    print(f'  - {issue}')
if not issues:
    print('No major issues found')