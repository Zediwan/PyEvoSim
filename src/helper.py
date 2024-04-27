def format_number(value: float | int) -> str:
    if value is not None:
        num = round(value, 2)
        s = f"{num}"
        if num >= 1000000:
            num = round(num/1000000, 2)
            s = f"{num}m"
        elif num >= 1000:
            num = round(num/1000, 2)
            s = f"{num}k"
        return s 
    else:
        return ""