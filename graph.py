import numpy as np
import matplotlib.pyplot as plt
import datetime

x = [
    datetime.datetime(2017, 4, 20),
    datetime.datetime(2018, 2, 8),
    datetime.datetime(2018, 6, 5)]
y = [414+128, 299+128, 285+128]

ax = plt.subplot(111)
ax.bar(x, y, width=50)
ax.xaxis_date()

plt.show()