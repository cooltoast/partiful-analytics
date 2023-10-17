import datetime
import json
import matplotlib.pyplot as plt
import matplotlib.dates


plt.style.use('ggplot')
bounds = [None, None]


def load_from_file(year):
    filename = f'{year}.json'

    with open(filename) as f:
        return json.load(f)


def get_date(date_string):
    return datetime.datetime.strptime(date_string, '%Y-%m-%dT%H:%M:%S.%fZ').strftime('%m/%d')


def update_axis_bounds(data):
    min_date = get_date(data[0])
    max_date = get_date(data[-1])

    bounds[0] = min_date if bounds[0] is None else min(bounds[0], min_date)
    bounds[1] = max_date if bounds[1] is None else max(bounds[1], max_date)


def set_axis_bounds(ax, year):
    min_date = datetime.datetime.strptime(bounds[0], '%m/%d').replace(year=year) - datetime.timedelta(days=2)
    max_date = datetime.datetime.strptime(bounds[1], '%m/%d').replace(year=year) + datetime.timedelta(days=2)
    ax.set_xlim([min_date, max_date])


def plot(ax, year, data):
    x = sorted([x['rsvpDate'] for x in data])
    y = range(1, len(x) + 1)

    dates = matplotlib.dates.date2num(x)
    ax.plot_date(dates, y, 'm.')

    update_axis_bounds(x)


def plot_rsvps(ax, year):
    ax.set_title(year)

    raw = load_from_file(year)

    data = raw['result']['data']

    going = [x for x in data if x['status'] == 'GOING']
    maybe = [x for x in data if x['status'] == 'MAYBE']

    # hist = [x for x in data if not (len(x['rsvpHistory']) == 1 and x['rsvpHistory'][0]['status'] == "GOING")]

    plot(ax, year, going)


def main():
    years = (2022, 2023)

    fig, axs = plt.subplots(len(years))
    fig.suptitle('Good Company Party Attendance')

    for year, ax in zip(years, axs):
        plot_rsvps(ax, year)

    for year, ax in zip(years, axs):
        set_axis_bounds(ax, year)

    plt.show()


if __name__ == "__main__":
    main()
