def get_priority(product_name):
    name = product_name.lower()

    if "booster box" in name:
        return "HIGH"

    if "fb09" in name or "fb10" in name:
        return "HIGH"

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