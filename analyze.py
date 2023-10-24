import datetime
import json
from collections import OrderedDict

import matplotlib.dates
import matplotlib.pyplot as plt

DATE_FORMAT = "%Y-%m-%dT%H:%M:%S.%fZ"
DATE_BOUNDS_FORMAT = "%m/%d"


plt.style.use("Solarize_Light2")
bounds = [None, None]


def load_from_file(filename):
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
    bounds_buffer = datetime.timedelta(days=4)
    min_date = datetime.datetime.strptime(bounds[0], DATE_BOUNDS_FORMAT).replace(year=year) - bounds_buffer
    max_date = datetime.datetime.strptime(bounds[1], DATE_BOUNDS_FORMAT).replace(year=year) + bounds_buffer
    ax.set_xlim([min_date, max_date])


def display_legend(fig, axs):
    handles, labels = [], OrderedDict()

    for ax in axs:
        for h, l in zip(*ax.get_legend_handles_labels()):
            if l not in labels:
                labels[l] = None
                handles.append(h)

    fig.legend(handles, labels.keys(), loc="right")


def plot_rsvps(ax, year, status, plot_color):
    raw = load_from_file(f"{year}.json")

    data = raw["result"]["data"]

    rsvps = []
    for x in data:
        if x["status"] == status:
            for _ in range(x["plusOneCount"] + 1):
                rsvps.append(x["rsvpDate"])

    # hist = [x for x in data if not (len(x['rsvpHistory']) == 1 and x['rsvpHistory'][0]['status'] == "GOING")]

    rsvps.sort()
    count = range(1, len(rsvps) + 1)

    dates = matplotlib.dates.date2num(rsvps)
    ax.plot_date(dates, count, ".", color=plot_color, label=status.title())

    update_axis_bounds(rsvps)


def plot_blasts(ax, year):
    blasts = load_from_file(f"{year}-blast.json") or []
    for blast in blasts:
        timestamp = parse_date(blast["sentAt"]["timestampValue"])
        ax.axvline(x=timestamp, color="blue", label="Text Blast", linestyle="dashed")


def plot_comments(ax, year):
    comments = load_from_file(f"{year}-comment.json") or []
    for comment in comments:
        timestamp = parse_date(comment["publishedAt"]["timestampValue"])
        ax.axvline(x=timestamp, color="#5e0ba1", label="Comment", linestyle="dashed")


def plot_event(ax, year):
    event = load_from_file(f"{year}-event.json")
    timestamp = parse_date(event["startDate"])
    ax.axvline(x=timestamp, color="magenta", label="PARTY", linestyle="dashed")


def plot(ax, year):
    ax.set_title(year)

    plot_rsvps(ax, year, "GOING", "green")
    plot_rsvps(ax, year, "MAYBE", "orange")
    plot_blasts(ax, year)
    plot_comments(ax, year)
    plot_event(ax, year)


def main():
    years = (2022, 2023)

    fig, axs = plt.subplots(len(years))
    fig.suptitle("Good Company Party Attendance")

    for year, ax in zip(years, axs):
        plot(ax, year)

    for year, ax in zip(years, axs):
        set_axis_bounds(ax, year)

    display_legend(fig, axs)

    plt.show()


if __name__ == "__main__":
    main()
