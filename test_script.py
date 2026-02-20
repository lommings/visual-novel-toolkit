import re

content = open(r'C:\Users\lommi\Projects\visual-novel-toolkit\output\1140119_Temp\monogatari-game\js\script.js', encoding='utf-8').read()

# Find all jump targets
jumps = re.findall(r"'Do': 'jump (\w+)'", content)
passages = re.findall(r"^\t'(\w+)': \[", content, re.MULTILINE)

print(f'Passages: {len(passages)}')
print(f'Jumps: {len(jumps)}')

# Check for missing targets
missing = set(jumps) - set(passages)
if missing:
    print(f'Missing targets: {missing}')
else:
    print('All jump targets exist!')

# Check all endings have 'end'
endings = ['Ending_UnembraceableLove', 'Ending_BreakChains', 'Ending_LostShadow', 'Ending_SilentEnd']
for e in endings:
    if f"'{e}'" in content and "'end'" in content[content.find(f"'{e}'"):content.find(f"'{e}'")+2000]:
        print(f'✓ {e} has end')
    else:
        print(f'✗ {e} missing end')
