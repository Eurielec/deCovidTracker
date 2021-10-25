def calculate_people_inside(accessed, exited):
    results = {}
    for entry in accessed:
        try:
            current = results[entry.email]
        except Exception:
            current = 0
        current = current + 1
        results[entry.email] = current
    for entry in exited:
        try:
            current = results[entry.email]
        except Exception:
            current = 0
        current = current - 1
        results[entry.email] = current
    return ", ".join([key for key, value in results.items() if value == 1])
