from utilities import telegram_bot


bot = telegram_bot.Bot()


def calculate_people_inside(db, accessed, exited):
    results = {}
    for entry in accessed:
        try:
            current = results[entry.nif_nie]
        except Exception:
            current = 0
        current = current + 1
        results[entry.nif_nie] = current
    for entry in exited:
        try:
            current = results[entry.nif_nie]
        except Exception:
            current = 0
        current = current - 1
        results[entry.nif_nie] = current
    return ", ".join([key for key, value in results.items() if value == 1])


def evaluate_and_notify(current, association, max_people, type):
    if current + 1 >= max_people and type == "access":
        bot.notify(
            message="Limit has just been reached.",
            title='Warning',
            association=association
        )
        return
    if current >= max_people and type == "exit":
        bot.notify(
            message="Space available now.",
            title='Info',
            association=association
        )
        return
    if current >= max_people and type == "access":
        bot.notify(
            message="Someone could not access %s. %s people already inside." % (
                association, max_people),
            title='Access denied',
            association=association
        )
        return


def json_to_csv(data):
    """
    Read monthly events from database as csv.
    """
    csv = ""
    for entry in data:
        csv += ",".join(
            map(
                lambda x: str(x),
                [entry.id, entry.time, entry.type, entry.email,
                 entry.nif_nie, entry.association])) + "\n"
    return csv
