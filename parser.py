import sys
import time
import os


from datetime import datetime
import dateutil.relativedelta as dateu
import plotly
from plotly.graph_objs import *
import plotly.plotly as py
import plotly.graph_objs as go
from plotly.tools import FigureFactory as FF
import plotly.tools as pyt

pyt.set_credentials_file(username='paoloc', api_key='ee28u45bns')

def readFromFile():
  arduFile = "../energyBuffer.log"
  lines = []
  try:
      with open(arduFile, "r") as f:
          lines = f.readlines()
      lines = map(lambda x: x.rstrip(), lines)
      return lines
  except:
      return lines

lines = readFromFile()

xA = []
xB = []
xC = []

yA = []
yB = []
yC = []

for line in lines:
    try:
        fase_tmp = line.split(',')[1]
    except:
        fase_tmp = '4'

    if fase_tmp == '2':
        xA.append(line.split(',')[0])
        yA.append(line.split(',')[2])
    elif fase_tmp == '3':
        xB.append(line.split(',')[0])
        yB.append(line.split(',')[2])
    else:
        print "errore, id non presente tra 2 e 3"

traceY = Scatter(
    x=xA,
    y=yA,
    name='Raw'
)

# Calcolo Potenza Istantanea in Watt
yyA = []
yyB = []

for y in yA:
    yyA.append(3600000/float(y))
for y in yB:
    yyB.append(3600000/float(y))




# # Calcolo ritardo
# eA = []
# i = 1
#
# for x in xA[1:]:
#     d0 = datetime.strptime(xA[i-1], '%Y-%m-%d %H:%M:%S.%f')
#     d1 = datetime.strptime(xA[i], '%Y-%m-%d %H:%M:%S.%f')
#     eA.append((d1 - d0).total_seconds()*1000 - float(yA[i]))
#     i = i + 1
#
# traceE = Scatter(
#     x=xA,
#     y=eA,
#     name='errore'
# )

now = datetime.now()

yesterday = now - dateu.relativedelta(days=1)
print "Yesterday: " + str(yesterday)

p_this_week_s = now - dateu.relativedelta(days=now.weekday())
p_this_week_s = p_this_week_s.replace(hour=00,minute=00,second=00,microsecond=00)
print "p_this_week_s: " + str(p_this_week_s)

last_week = now - dateu.relativedelta(days=7)

p_last_week_s = last_week - dateu.relativedelta(days=last_week.weekday())
p_last_week_s = p_last_week_s.replace(p_last_week_s.year,p_last_week_s.month,p_last_week_s.day,hour=00,minute=00,second=00,microsecond=00)
print "p_last_week_s: " + str(p_last_week_s)

p_last_week_e = p_last_week_s + dateu.relativedelta(days=6)
p_last_week_e = p_last_week_e.replace(hour=23,minute=59,second=59,microsecond=9999)
print "p_last_week_e: " + str(p_last_week_e)

last_year = now - dateu.relativedelta(year=1)

this_W = [0.0,0.0,0.0,0.0,0.0,0.0,0.0]
last_W = [0.0,0.0,0.0,0.0,0.0,0.0,0.0]
this_M = 0.0
last_M = 0.0
this_Y = [0.0,0.0,0.0,0.0,0.0,0.0,0.0,0.0,0.0,0.0,0.0,0.0]
last_Y = [0.0,0.0,0.0,0.0,0.0,0.0,0.0,0.0,0.0,0.0,0.0,0.0]

this_W2 = [0.0,0.0,0.0,0.0,0.0,0.0,0.0]
last_W2 = [0.0,0.0,0.0,0.0,0.0,0.0,0.0]
this_M2 = 0.0
last_M2 = 0.0
this_Y2 = [0.0,0.0,0.0,0.0,0.0,0.0,0.0,0.0,0.0,0.0,0.0,0.0]
last_Y2 = [0.0,0.0,0.0,0.0,0.0,0.0,0.0,0.0,0.0,0.0,0.0,0.0]

yest = [0.0,0.0,0.0,0.0,0.0,0.0,0.0,0.0,0.0,0.0,0.0,0.0,0.0,0.0,0.0,0.0,0.0,0.0,0.0,0.0,0.0,0.0,0.0,0.0]
yest2 = [0.0,0.0,0.0,0.0,0.0,0.0,0.0,0.0,0.0,0.0,0.0,0.0,0.0,0.0,0.0,0.0,0.0,0.0,0.0,0.0,0.0,0.0,0.0,0.0]

total = 0.0
total2 = 0.0

# Selezione delle x solamente dell'ultima settimana
# scorsa settimana

i = 0

for x in xA:

    try:
        d0 = datetime.strptime(x, '%Y-%m-%d %H:%M:%S.%f')
    except:
        d0 = datetime.strptime(x, '%Y-%m-%d %H:%M:%S')

    if d0 >= p_this_week_s:
        # sono nei giorni di questa settimana
        this_W[d0.weekday()] = this_W[d0.weekday()] + 0.001
        if d0.day == yesterday.day:
            yest[d0.hour] = yest[d0.hour] + 0.001

    if d0 >= p_last_week_s and d0 <= p_last_week_e:
        # sono nei giorni della scorsa settimana
        last_W[d0.weekday()] = last_W[d0.weekday()] + 0.001


    if d0.year == now.year:
        this_Y[d0.month-1] = this_Y[d0.month-1] + 0.001

    if d0.year == last_year.year:
        last_Y[d0.month-1] = last_Y[d0.month-1] + 0.001

    ## total
    total = total + 0.001

    i = i + 1

i = 0
for x in xB:

    try:
        d0 = datetime.strptime(x, '%Y-%m-%d %H:%M:%S.%f')
    except:
        d0 = datetime.strptime(x, '%Y-%m-%d %H:%M:%S')

    if d0 >= p_this_week_s:
        # sono nei giorni di questa settimana
        this_W2[d0.weekday()] = this_W2[d0.weekday()] + 0.001
        if d0.day == yesterday.day:
            yest2[d0.hour] = yest2[d0.hour] + 0.001

    if d0 >= p_last_week_s and d0 <= p_last_week_e:
        # sono nei giorni della scorsa settimana
        last_W2[d0.weekday()] = last_W2[d0.weekday()] + 0.001


    if d0.year == now.year:
        this_Y2[d0.month-1] = this_Y2[d0.month-1] + 0.001

    if d0.year == last_year.year:
        last_Y2[d0.month-1] = last_Y2[d0.month-1] + 0.001

    ## total2
    total2 = total2 + 0.001

    i = i + 1

print "Total: " + str(total)
print "Total2: " + str(total2)

this_W_SUM = [this_W[i]+this_W2[i] for i in xrange(len(this_W))]
last_W_SUM = [last_W[i]+last_W2[i] for i in xrange(len(last_W))]
this_Y_SUM = [this_Y[i]+this_Y2[i] for i in xrange(len(this_Y))]
last_Y_SUM = [last_Y[i]+last_Y2[i] for i in xrange(len(last_Y))]

traceYESTERDAY = go.Bar(
    y = yest,
    name = "Illuminazione Piano Terra"
)

traceYESTERDAY2 = go.Bar(
    y = yest2,
    name = "Illuminazione Cucina"
)


traceLASTWEEK = go.Bar(
    x = ["Lunedi","Martedi","Mercoledi", "Giovedi", "Venerdi","Sabato","Domenica"],
    y = last_W,
    name = "Illuminazione Piano Terra"
)
traceLASTWEEK2 = go.Bar(
    x = ["Lunedi","Martedi","Mercoledi", "Giovedi", "Venerdi","Sabato","Domenica"],
    y = last_W2,
    name = "Illuminazione Cucina"
)

traceTHISWEEKSUM = go.Bar(
    x = ["Lunedi","Martedi","Mercoledi", "Giovedi", "Venerdi","Sabato","Domenica"],
    y = this_W_SUM,
    name = "Settimana attuale"
)
traceLASTWEEKSUM = go.Bar(
    x = ["Lunedi","Martedi","Mercoledi", "Giovedi", "Venerdi","Sabato","Domenica"],
    y = last_W_SUM,
    name = "Settimana scorsa"
)

traceTHISYEARSUM = go.Bar(
    x=['Gen', 'Feb', 'Mar', 'Apr', 'Mag', 'Giu',
       'Lug', 'Ago', 'Set', 'Ott', 'Nov', 'Dic'],
    y=this_Y_SUM,
    name='Anno attuale'
)
traceLASTYEARSUM = go.Bar(
    x=['Gen', 'Feb', 'Mar', 'Apr', 'Mag', 'Giu',
       'Lug', 'Ago', 'Set', 'Ott', 'Nov', 'Dic'],
    y=last_Y_SUM,
    name='Anno scorso'
)

## Yesterday!
data = Data([traceYESTERDAY,traceYESTERDAY2])
layout = dict(title = 'Consumo elettrico durante il ' + yesterday.strftime("%d/%m/%y"),
              xaxis = dict(title = 'ore del giorno'),
              yaxis = dict(title = 'kWh'),
              barmode='stack'
              )

fig = dict(data=data, layout=layout)
plotly.offline.plot(fig, filename = 'html/yesterday.html')

## Week vs. Last Week
data = Data([traceTHISWEEKSUM,traceLASTWEEKSUM])
layout = dict(title = 'Confronto consumi settimana attuale e settimana passata',
              xaxis = dict(title = 'giorni'),
              yaxis = dict(title = 'kWh'),
              barmode='group'
              )

fig = dict(data=data, layout=layout)
plotly.offline.plot(fig, filename = 'html/week_last_week.html')

## Year vs. Last Year
data = Data([traceTHISYEARSUM,traceLASTYEARSUM])
layout = dict(title = 'Confronto consumi anno attuale e anno passato',
              xaxis = dict(title = 'mesi'),
              yaxis = dict(title = 'kWh'),
              barmode='group'
              )

fig = dict(data=data, layout=layout)
plotly.offline.plot(fig, filename = 'html/year_last_year.html')

## Pie and generale
labels = ['Piano Terra','Cucina']
values = [total,total2]

tracePIE = go.Pie(
    labels = labels,
    values = values,
    hole = .4,
    )

data = Data([tracePIE])

layout = dict(title = "Consumi totali")

fig = dict(data=data, layout=layout)
plotly.offline.plot(fig, filename = 'html/pie.html')
