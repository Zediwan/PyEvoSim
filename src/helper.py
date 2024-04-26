def format_number(value: float) -> str:
    num = round(value)
    s = f"{num}"
    if num >= 1000000:
        num = round(num/1000000,1)
        s = f"{num}m"
    elif num >= 1000:
        num = round(num/1000,1)
        s = f"{num}k"
    return s 