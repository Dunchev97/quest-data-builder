import json

ctx = json.load(open('campaigns/StoneGnome_2026/pack_001/context_pack.json', 'r', encoding='utf-8'))
print(f'Total quests: {len(ctx["quests"])}')
for q in ctx['quests']:
    print(f'\nQuest {q["quest_number"]}: {q["title_quest"]} ({q["character"]})')
    for t in q['tasks']:
        print(f'  Task {t["task_number"]}: {t["task_template_name"]} (domain: {t.get("candidate_domain", "none")})')
        if t.get('candidates'):
            print(f'    Candidates: {len(t["candidates"])} available')
            for i, c in enumerate(t['candidates'][:3]):
                if 'collection_title' in c:
                    print(f'      - {c["candidate_id"]}: {c["collection_title"]}')
                elif 'garbage_title' in c:
                    print(f'      - {c["candidate_id"]}: {c["garbage_title"]}')
                elif 'flower_title' in c:
                    print(f'      - {c["candidate_id"]}: {c["flower_title"]}')
                else:
                    print(f'      - {c["candidate_id"]}: {list(c.keys())}')
        else:
            print(f'    No candidates (generated/story template)')
