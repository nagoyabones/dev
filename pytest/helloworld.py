import datetime
from dateutil import relativedelta
import calendar
import locale


def main():
    locale.setlocale(locale.LC_ALL, "")

    dt = datetime.date.today()
    p = dt - relativedelta.relativedelta(years=1)

    weekday_name = calendar.day_name[p.weekday()]

    dt_month = str(dt.month)
    dt_day = str(dt.day)

    print("去年の" + dt_month + "月" + dt_day + "日は" + weekday_name + "でした。")


if __name__ == "__main__":
    main()
    test
