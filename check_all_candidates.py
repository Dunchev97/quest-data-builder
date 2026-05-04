import json

ctx = json.load(open('campaigns/StoneGnome_2026/pack_001/context_pack.json', 'r', encoding='utf-8'))

# Check all gr_garbage candidates across all quests
print("=== gr_garbage candidates ===")
for qi, q in enumerate(ctx['quests']):
    for t in q['tasks']:
        if t.get('candidate_domain') == 'gr_garbage':
            print(f"Q{q['quest_number']} Task {t['task_number']}: {t['task_template_name']}")
            for c in t['candidates'][:3]:
                title = c.get('garbage_title', c.get('flower_title', c.get('collection_title', '?')))
                print(f"  {c['candidate_id']}: {title}")

print("\n=== collection_drop candidates ===")
for qi, q in enumerate(ctx['quests']):
    for t in q['tasks']:
        if t.get('candidate_domain') == 'collection_drop':
            print(f"Q{q['quest_number']} Task {t['task_number']}: {t['task_template_name']}")
            for c in t['candidates'][:3]:
                title = c.get('collection_title', '?')
                print(f"  {c['candidate_id']}: {title}")
