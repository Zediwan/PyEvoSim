def format_number(value) -> str:
    if isinstance(value, (int, float)):
        num = round(value, 2)
        s = f"{num}"
        if num >= 1000000:
            num = round(num / 1000000, 2)
            s = f"{num}m"
        elif num >= 1000:
            num = round(num / 1000, 2)
            s = f"{num}k"
        return s
    elif isinstance(value, str):
        return value
    else:
        return ""
