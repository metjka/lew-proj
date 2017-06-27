import sqlite3, math, plotly
from plotly.graph_objs import Scatter, Layout, Pie, Figure, Bar

dates = ["1999", "2000", "2001", "2002", "2003", "2004", "2005",
         "2006", "2007", "2008", "2009", "2010", "2011", "2012",
         "2013", "2014", "2015", "2015 Q2", "2016", "2016 Q2"]

con = sqlite3.connect("Auto.db")

cur = con.cursor()
values = list(cur.execute("SELECT * FROM Auto"))


def buildLinePlotGraf(data):
    dataForPlot = []
    for val in data:
        country = val[:1][0]
        value = val[1:]
        dataForPlot.append(Scatter(name=country, x=dates, y=value))
    plotly.offline.plot(dataForPlot, filename='line.html')
    return dataForPlot


def buildPieForCountry(year):
    data = list(cur.execute("SELECT a.Country ,a.\"" + year + "\" FROM Auto a "))
    co = []
    va = []
    for d in data:
        co.append(d[0])
        va.append(float(d[1].replace(",", "")))
    pie = Pie(labels=co, values=va)
    plotly.offline.plot([pie], filename="pie.html")
    return pie


def buildBar(data):
    grafData = []
    for val in data:
        country = val[:1][0]
        value = val[1:]
        grafData.append(Bar(x=dates, y=value, name=country))
    fig = Figure(data=grafData, layout=Layout(barmode='stack'))
    plotly.offline.plot(fig)
    return grafData


def buildAll(data):
    temp = []
    for a in data[0][1:]:
        temp.append(int(a.replace(",", "")))

    for dat in data[1:]:
        for s in range(len(dat[1:])):
            temp[s] += int(dat[1:][s].replace(",", ""))
    sca = Scatter(name="All", x=dates, y=temp)

    plotly.offline.plot([sca], filename="All.html")
    return sca


def growthRate(country):
    co = None
    for d in values:
        if (d[0] == country):
            co = d
    if (co == None): raise ValueError("Not found!")
    start = int(co[1:][0].replace(",", ""))
    end = int(co[1:][-1].replace(",", ""))
    rate = (end / start) * 100
    return str(math.trunc(rate)) + "%"


def AverageGrowthRate(country):
    co = None
    for d in values:
        if (d[0] == country):
            co = d
    if (co == None): raise ValueError("Not found!")
    start = int(co[1:][0].replace(",", ""))
    end = int(co[1:][-1].replace(",", ""))
    rate = ((end / start) - 1) * 100
    return str(math.trunc(rate)) + "%"


# buildLinePlotGraf(values)
# buildPieForCountry('2002')
# buildBar(values)
# buildAll(values)
print("Basic Growth Rates")
print("Spain", growthRate('Spain'))
print("Serbia", growthRate('Serbia'))
print("India", growthRate('India'))
print("Russia", growthRate('Russia'))
print("France", growthRate('France'))
print("Italy", growthRate('Italy'))
print("--------------------------")
print("")
print("Spain", AverageGrowthRate('Spain'))
print("Serbia", AverageGrowthRate('Serbia'))
print("India", AverageGrowthRate('India'))
print("Russia", AverageGrowthRate('Russia'))
print("France", AverageGrowthRate('France'))
print("Italy", AverageGrowthRate('Italy'))
print("--------------------------")
con.close()
