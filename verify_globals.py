import re
with open(r'C:\Users\abhiy\OneDrive\Desktop\hackathon rivals\index.html', 'r', encoding='utf-8') as f:
    html = f.read()

checks = [
    'window.submitAuth',
    'window.updateFormFields',
    'window.openLogin',
    'window.closeLogin',
    'window.addMember',
    'window.setStep',
    'window.renderTC',
    'window.arenaRun',
    'window.sendAI',
    'window.getAIResponse',
    'window.loadLang',
    'window.runCode',
    'window.toggleTheme',
]

print('=== Global Function Exposure ===')
for check in checks:
    found = (check + ' =') in html
    status = 'OK' if found else 'MISSING'
    print(f'{check}: {status}')