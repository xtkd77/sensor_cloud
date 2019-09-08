import pandas as pd
import matplotlib.pyplot as plt
from matplotlib.dates import DateFormatter

df = pd.read_csv('tmp.csv')
df.columns = ['date','time','key','val','a']

df['tmp'] = df.date + " " + df.time
df['datetime'] = pd.to_datetime(df.tmp)

unit_str = ['hPa', 'deg', 'percent']
fig, ax = plt.subplots(3, 1, figsize=(10,5), sharex=True)

plt.suptitle("%s" % df.date[0])
for i, key in enumerate(['pressure', 'temperature', 'humidity']):
    ax[i].plot(df[df.key == key].datetime, df[df.key == key].val)
    ax[i].grid(True)
    ax[i].set_ylabel(f'{key} [%s]' % unit_str[i])
ax[0].set_xticklabels([])
ax[1].set_xticklabels([])
ax[2].set_xlabel('date time')
ax[2].xaxis.set_major_formatter(DateFormatter('%H:%M'))
ax[2].set_xlim([df.datetime[0], df.datetime[len(df)-1]])

plt.savefig('out.png')
plt.show()
