import datetime
import json

import matplotlib.dates
import matplotlib.pyplot as plt

DATE_FORMAT = "%Y-%m-%dT%H:%M:%S.%fZ"
DATE_BOUNDS_FORMAT = "%m/%d"


plt.style.use("ggplot")
bounds = [None, None]


def load_from_file(year, filename=None):
    if filename is None:
        filename = f"{year}.json"

    with open(filename) as f:
        return json.load(f)


def parse_date(date_string):
    return datetime.datetime.strptime(date_string, DATE_FORMAT)


def update_axis_bounds(data):
    min_date = parse_date(data[0]).strftime(DATE_BOUNDS_FORMAT)
    max_date = parse_date(data[-1]).strftime(DATE_BOUNDS_FORMAT)

    bounds[0] = min_date if bounds[0] is None else min(bounds[0], min_date)
    bounds[1] = max_date if bounds[1] is None else max(bounds[1], max_date)


def set_axis_bounds(ax, year):
    min_date = datetime.datetime.strptime(bounds[0], DATE_BOUNDS_FORMAT).replace(year=year) - datetime.timedelta(days=2)
    max_date = datetime.datetime.strptime(bounds[1], DATE_BOUNDS_FORMAT).replace(year=year) + datetime.timedelta(days=2)
    ax.set_xlim([min_date, max_date])


def plot_rsvps(ax, year):
    raw = load_from_file(year)

    data = raw["result"]["data"]

    going = [x for x in data if x["status"] == "GOING"]
    maybe = [x for x in data if x["status"] == "MAYBE"]

    # hist = [x for x in data if not (len(x['rsvpHistory']) == 1 and x['rsvpHistory'][0]['status'] == "GOING")]

    x = sorted([x["rsvpDate"] for x in data])
    y = range(1, len(x) + 1)

    dates = matplotlib.dates.date2num(x)
    ax.plot_date(dates, y, "m.")

    update_axis_bounds(x)


def plot_blasts(ax, year):
    blasts = load_from_file(year, f"{year}-blast.json") or []
    for blast in blasts:
        timestamp = parse_date(blast["sentAt"]["timestampValue"])
        ax.axvline(x=timestamp, color="b", label="BLAST", linestyle="dashed")


def plot_comments(ax, year):
    comments = load_from_file(year, f"{year}-comment.json") or []
    for comment in comments:
        timestamp = parse_date(comment["publishedAt"]["timestampValue"])
        ax.axvline(x=timestamp, color="g", label="COMMENT", linestyle="dashed")


def plot(ax, year):
    ax.set_title(year)

    plot_rsvps(ax, year)
    plot_blasts(ax, year)
    plot_comments(ax, year)


def main():
    years = (2022, 2023)

    fig, axs = plt.subplots(len(years))
    fig.suptitle("Good Company Party Attendance")

    for year, ax in zip(years, axs):
        plot(ax, year)

    for year, ax in zip(years, axs):
        set_axis_bounds(ax, year)

    plt.show()


if __name__ == "__main__":
    main()
