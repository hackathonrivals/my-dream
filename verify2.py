import re
with open(r'C:\Users\abhiy\OneDrive\Desktop\hackathon rivals\index.html', 'r', encoding='utf-8') as f:
    html = f.read()

checks = [
    ('loginBtn onclick', 'loginBtn.*onclick'),
    ('lockLoginBtn onclick', 'lockLoginBtn.*onclick'),
    ('lockSignupBtn onclick', 'lockSignupBtn.*onclick'),
    ('arenaLoginBtn onclick', 'arenaLoginBtn.*onclick'),
    ('arenaSignupBtn onclick', 'arenaSignupBtn.*onclick'),
    ('themeToggle onclick', 'themeToggle.*onclick'),
    ('loginClose onclick', 'loginClose.*onclick'),
    ('loginSubmit onclick', 'loginSubmit.*onclick'),
    ('nextBtn onclick', 'nextBtn.*onclick'),
    ('prevBtn onclick', 'prevBtn.*onclick'),
    ('addMember onclick', 'addMember.*onclick'),
    ('pgRun onclick', 'pgRun.*onclick'),
    ('pgReset onclick', 'pgReset.*onclick'),
    ('pgCopy onclick', 'pgCopy.*onclick'),
    ('addTc onclick', 'addTc.*onclick'),
    ('arenaClear onclick', 'arenaClear.*onclick'),
    ('arenaRun onclick', 'arenaRun.*onclick'),
    ('qSubmit onclick', 'qSubmit.*onclick'),
    ('fbSubmit onclick', 'fbSubmit.*onclick'),
]

print('=== Inline onclick Handlers ===')
for name, pattern in checks:
    found = re.search(pattern, html) is not None
    status = "FOUND" if found else "MISSING"
    print(f'{name}: {status}')