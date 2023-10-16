import json
import matplotlib.pyplot as plt
import matplotlib.dates


def plot(ax, data):
    x = sorted([x['rsvpDate'] for x in data])
    y = range(1, len(x) + 1)

    dates = matplotlib.dates.date2num(x)
    ax.plot_date(dates, y)


def plot_rsvps(ax, raw):
    data = raw['result']['data']
    going = [x for x in data if x['status'] == 'GOING']
    maybe = [x for x in data if x['status'] == 'MAYBE']

    # hist = [x for x in data if not (len(x['rsvpHistory']) == 1 and x['rsvpHistory'][0]['status'] == "GOING")]

    plot(ax, going)


def main():
    filenames = ('2022.json', '2023.json')

    fig, axs = plt.subplots(len(filenames))
    fig.suptitle('Good Company Party Attendance')

    for i, filename in enumerate(filenames):
        ax = axs[i]

        ax.set_title(filename.split('.')[0])

        raw = json.load(open(filename))
        plot_rsvps(ax, raw)

    plt.show()


if __name__ == "__main__":
    main()
