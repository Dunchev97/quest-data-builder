import json

ctx = json.load(open('campaigns/StoneGnome_2026/pack_001/context_pack.json', 'r', encoding='utf-8'))

# Find Q1 task 2 candidates
print('Q1 Task 2 candidates:')
for t in ctx['quests'][0]['tasks']:
    if t['task_number'] == 2:
        for c in t['candidates'][:10]:
            title = c.get('collection_title', c.get('garbage_title', c.get('flower_title', '?')))
            print(f'  {c["candidate_id"]}: {title}')

# Find Q10 task 3 candidates (task_number 30)
print('\nQ10 Task 30 candidates:')
for t in ctx['quests'][9]['tasks']:
    if t['task_number'] == 30:
        for c in t['candidates'][:10]:
            title = c.get('flower_title', c.get('garbage_title', c.get('collection_title', '?')))
            print(f'  {c["candidate_id"]}: {title}')
