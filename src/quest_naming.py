"""Naming rules shared by quest filling and final table exports."""
from __future__ import annotations

import re


def normalize_character_references(value, campaign_id: str):
    if isinstance(value,dict):
        return {key:normalize_character_references(item,campaign_id) for key,item in value.items()}
    if isinstance(value,list):
        return [normalize_character_references(item,campaign_id) for item in value]
    if not isinstance(value,str):
        return value
    pattern = rf"({re.escape(campaign_id)}_Character_\d+)(?!\d|_\d)"
    return re.sub(pattern,r"\1_1",value)


def normalize_generated_reference(value, campaign_id: str):
    value = normalize_character_references(value,campaign_id)
    if isinstance(value,str):
        for family in ("furniture","quest_action"):
            value = value.replace(f"/{family}/Fun/{campaign_id}/",f"/{family}/{campaign_id}/")
    return value
