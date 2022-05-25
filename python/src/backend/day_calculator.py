from datetime import datetime, timedelta


def get_weekday_in_n_days(n: int) -> str:
    today = datetime.today()

    target_day = today + timedelta(days=n)

    weekday = target_day.weekday()

    mapper = {0: "Monday", 1: "Tuesday", 2: "Wednesday",
              3: "Thursday", 4: "Friday", 5: "Saturday", 6: "Sunday"}

    return mapper.get(weekday)
