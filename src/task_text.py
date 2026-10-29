"""Shared grammatical forms for fixed task and resource text."""


def simple_nominative_to_accusative(value: str) -> str:
    words = value.strip().rstrip(".").split()
    converted: list[str] = []
    has_feminine_modifier = any(word.lower().endswith(("ая", "яя")) for word in words[:-1])
    last_index = len(words) - 1
    for index, word in enumerate(words):
        lower = word.lower()
        if lower.endswith("ая"):
            converted.append(word[:-2] + "ую")
        elif lower.endswith("яя"):
            converted.append(word[:-2] + "юю")
        elif index == last_index and lower.endswith(("чка", "жка", "шка", "щка", "ка")):
            converted.append(word[:-1] + "у")
        elif index == last_index and lower.endswith(("ля", "ря")):
            converted.append(word[:-1] + "ю")
        elif index == last_index and lower.endswith("ия"):
            converted.append(word[:-2] + "ию")
        elif index == last_index and lower.endswith("а") and (len(words) == 1 or has_feminine_modifier):
            converted.append(word[:-1] + "у")
        elif index == last_index and lower.endswith("я") and (len(words) == 1 or has_feminine_modifier):
            converted.append(word[:-1] + "ю")
        else:
            converted.append(word)
    return " ".join(converted)
