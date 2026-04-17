def get_built_atempo(speed: float) -> str:
    if 0.5 <= speed <= 2.0:
        return f"atempo={speed}"

    filters = []
    while speed < 0.5:
        filters.append("atempo=0.5")
        speed /= 0.5
    while speed > 2.0:
        filters.append("atempo=2.0")
        speed /= 2.0

    filters.append(f"atempo={speed}")
    return ",".join(filters)
