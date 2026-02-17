from datetime import date, timedelta

def calculate_share(total_cost, participants):
    if not participants:
        return 0
    return round(total_cost / len(participants), 2)

def week_range():
    today = date.today()
    start = today - timedelta(days=today.weekday())
    return start.isoformat(), today.isoformat()
