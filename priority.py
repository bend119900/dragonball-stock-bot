def get_priority(product_name):
    name = product_name.lower()

    is_japanese = "japanese" in name

    if "booster box" in name and not is_japanese:
        return "HIGH"

    if "booster box" in name and is_japanese:
        return "MEDIUM"

    if "fb09" in name or "fb10" in name:
        if not is_japanese:
            return "HIGH"
        return "MEDIUM"

    if "booster pack" in name:
        return "MEDIUM"

    if "starter deck" in name:
        return "MEDIUM"

    return "LOW"


def priority_icon(priority):
    if priority == "HIGH":
        return "🚨🔥"
    if priority == "MEDIUM":
        return "📦"
    return "🔵"