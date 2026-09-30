import re
with open(r'C:\Users\abhiy\OneDrive\Desktop\hackathon rivals\index.html', 'r', encoding='utf-8') as f:
    html = f.read()

critical = ['loginBtn', 'lockLoginBtn', 'lockSignupBtn', 'arenaLoginBtn', 'arenaSignupBtn',
    'pgRun', 'pgReset', 'pgCopy', 'nextBtn', 'prevBtn', 'addMember',
    'qSubmit', 'fbSubmit', 'addTc', 'arenaClear', 'arenaRun',
    'themeToggle', 'loginClose', 'loginSubmit', 'loginModal']

print('=== Critical Button Verification ===')
for id in critical:
    found = f'id="{id}"' in html or f"id='{id}'" in html
    print(f'{id}: {"FOUND" if found else "MISSING"}')