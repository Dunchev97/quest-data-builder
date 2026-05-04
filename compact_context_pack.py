import json
import shutil
from pathlib import Path

# 1. Compact context_pack.json
with open('campaigns/StoneGnome_2026/pack_001/context_pack.json', 'r', encoding='utf-8') as f:
    ctx = json.load(f)

def compact_candidate(c):
    result = {"candidate_id": c["candidate_id"], "domain": c["domain"]}
    if c["domain"] == "garbage":
        result["garbage_classname"] = c["garbage_classname"]
        result["garbage_title"] = c["garbage_title"]
        result["locations"] = [loc["title"] for loc in c.get("locations", [])]
        result["has_world_location"] = c.get("has_world_location", False)
    elif c["domain"] == "flower":
        result["flower_classname"] = c["flower_classname"]
        result["flower_title"] = c["flower_title"]
    elif c["domain"] == "collection_drop":
        result["collection_classname"] = c["collection_classname"]
        result["collection_title"] = c["collection_title"]
        result["source_classname"] = c["source_classname"]
        result["source_title"] = c["source_title"]
        result["mode"] = c["mode"]
        result["locations"] = [loc["title"] for loc in c.get("locations", [])]
        result["has_world_location"] = c.get("has_world_location", False)
    elif c["domain"] == "gr_garbage":
        result["garbage_classname"] = c["garbage_classname"]
        result["garbage_title"] = c["garbage_title"]
        result["mode"] = c["mode"]
        result["locations"] = [loc["title"] for loc in c.get("locations", [])]
        result["has_world_location"] = c.get("has_world_location", False)
    return result

for q in ctx["quests"]:
    for t in q["tasks"]:
        if t.get("candidates"):
            t["candidates"] = [compact_candidate(c) for c in t["candidates"]]
        if "search_text" in t:
            del t["search_text"]
        if "notes" in t and t["notes"]:
            t["notes"] = []

with open('campaigns/StoneGnome_2026/pack_001/context_pack.json', 'w', encoding='utf-8') as f:
    json.dump(ctx, f, ensure_ascii=False, indent=2)

print(f"Compact context_pack written")

# 2. Move context_candidate_history to campaign level
pack_history = Path('campaigns/StoneGnome_2026/pack_001/context_candidate_history.json')
campaign_history = Path('campaigns/StoneGnome_2026/context_candidate_history.json')

if pack_history.exists():
    with open(pack_history, 'r', encoding='utf-8') as f:
        history = json.load(f)
    
    # If campaign level exists, merge
    if campaign_history.exists():
        with open(campaign_history, 'r', encoding='utf-8') as f:
            campaign_hist = json.load(f)
        # Merge logic: update with pack data
        for key, value in history.items():
            if key not in campaign_hist:
                campaign_hist[key] = value
            elif isinstance(value, list):
                campaign_hist[key] = list(set(campaign_hist[key] + value))
        history = campaign_hist
    
    with open(campaign_history, 'w', encoding='utf-8') as f:
        json.dump(history, f, ensure_ascii=False, indent=2)
    
    pack_history.unlink()
    print(f"Moved context_candidate_history to campaign level")

# 3. Remove preview files
for preview in [
    'campaigns/StoneGnome_2026/pack_001/quest_plan.preview.md',
    'campaigns/StoneGnome_2026/pack_001/quest_plan.resolved.preview.md',
    'campaigns/StoneGnome_2026/pack_001/context_pack.preview.md',
]:
    p = Path(preview)
    if p.exists():
        p.unlink()
        print(f"Removed {preview}")

print("Done!")
