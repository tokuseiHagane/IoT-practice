import matplotlib.pyplot as plt
import json


def lineplot(x_data, y_data, x_label="", y_label="", title=""):
    _, ax = plt.subplots()

    ax.plot(x_data, y_data, lw = 2, color = '#539caf', alpha = 1)

    ax.set_title(title)
    ax.set_xlabel(x_label)
    ax.set_ylabel(y_label)
    plt.savefig('lineplot_co2.png')


def histogram(data, n_bins, x_label = "", y_label = "", title = "", cumulative=False):
    _, ax = plt.subplots()
    ax.hist(data, bins=n_bins, cumulative=cumulative, color='#e28743')
    ax.set_ylabel(y_label)
    ax.set_xlabel(x_label)
    ax.set_title(title)
    plt.savefig('histogram_illuminance.png')


def circular(values, labels, title):
    _, ax = plt.subplots()
    ax.pie(values, labels=labels, autopct='%1.1f%%', shadow=True, wedgeprops={'lw':1, 'ls':'--','edgecolor':"k"}, rotatelabels=True)
    ax.axis("equal")
    ax.set_title(title)
    plt.savefig('circular_vin.png')


if __name__ == '__main__':
    #  получение показателйей
    dictionary = json.load(open('data.json', 'r'))["data"]
    xAxis = [item['time'].split(' ')[-1] for item in dictionary]
    yIlluminance = [int(item['illuminance']) for item in dictionary]
    yVin = [float(item['Vin']) for item in dictionary]
    yCO2 = [int(item['CO2']) for item in dictionary]

    #  перевод показателей в целочисленное значение
    xAxis = [sum([int(el.split(':')[::-1][n])*60**n for n in range(3)]) for el in xAxis]
    base_t = xAxis[0]
    xAxis = xAxis[100:]
    yCO2 = yCO2[100:]
    xAxis = [el % base_t for el in xAxis]

    groups = {'23.0 В. >=': len([el for el in yVin if el >= 23.0 ]),
              '< 23.0 В.': len(([el for el in yVin if el < 23.0 ]))}
    
    lineplot(xAxis, yCO2, 'Время, c', "Показатели", "Изменения показателя датчика СО2\n(первые 100 зн. забракованы)")
    histogram(yIlluminance, 50, 'Кол-во', 'Значения', 'Распределение показаний освещения')
    circular(groups.values(), groups.keys(), 'Кгруговая диаграмма Vin (~24В)')

