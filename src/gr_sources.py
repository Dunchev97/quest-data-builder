"""Keep GR task templates, drop mechanics and player-facing text consistent."""
try:
    from .task_text import simple_nominative_to_accusative
except ImportError:
    from task_text import simple_nominative_to_accusative


GARBAGE_GR_TEMPLATES = {
    "TT-013": ("GR с мусора в локации дома", "get_asset GR garbage location_tags"),
    "TT-014": ("GR с конкретного мусора в гостях", "get_asset GR in_guest garbage classname"),
    "TT-015": ("GR с конкретного мусора дома", "get_asset GR garbage classname"),
}


def effective_template_id(template_id, candidate):
    # Existing TT-013 candidate pools contain concrete garbage, not location-wide drops.
    if template_id == "TT-013" and (candidate or {}).get("garbage_classname"):
        return "TT-014" if candidate.get("mode") == "guest" else "TT-015"
    return template_id


def garbage_hint(source_title, mode, locations):
    if mode not in {"home", "guest"} or not source_title or not locations:
        raise ValueError("Concrete GR needs a garbage title, home/guest mode and search locations")
    place = "в гостях" if mode == "guest" else "дома"
    titles = [source_title] if isinstance(source_title, str) else source_title
    title = ", ".join(simple_nominative_to_accusative(value) for value in titles)
    return f"Убирай {title} {place}, чтобы найти. Место поиска: {locations}."


def location_hint(locations):
    if not locations:
        raise ValueError("Location-wide GR needs explicit search locations")
    return f"Убирай мусор в локации {locations} дома, чтобы найти."


def candidate_mode(candidate, task_type):
    mode = (candidate or {}).get("mode")
    return mode or ("guest" if "in_guest" in task_type else "home")
