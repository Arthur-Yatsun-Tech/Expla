import matplotlib.pyplot as plt
import matplotlib as mpl
import numpy as np
from matplotlib.font_manager import FontProperties

data = np.random.uniform(0, 1, 12).reshape(3, 4)
final_data = [['%.3f' % j for j in i] for i in data]

mpl.style.use('Solarize_Light2')

array1 = np.array([1, 1.25, 1.3])
array2 = array1 - 0.1
array3 = array1 + 0.0323

x = np.arange(3)

y2 = np.random.randn(25)

fig = plt.figure()
ax = fig.add_subplot(111)
# zip joins x and y coordinates in pairs

xs = np.arange(0, 3, 1)
ys = array1
a = ax.plot(xs, array1, 'o-')
b = ax.plot(xs, array2, 'o-')
c = ax.plot(xs, array3, 'o-')

labels = [
    ['A\u207A\u2081\u2081', 'A\u2081\u2082', 'A\u2081\u2083', 'A\u2081\u2084', 'A\u2081\u2085'],
    ['A\u2082\u2081', 'A\u2082\u2082', 'A\u2082\u2083', 'A\u2082\u2084', 'A\u2082\u2085'],
    ['A\u2083\u2081', 'A\u2083\u2082', 'A\u2083\u2083', 'A\u2083\u2084', 'A\u2083\u2085']
]

for x, y, label in zip(xs, ys, labels[0]):
    plt.annotate(label,  # this is the text
                 (x, y),  # this is the point to label
                 textcoords="offset points",  # how to position the text
                 xytext=(5, -10),  # distance from text to points (x,y)
                 )  # horizontal alignment can be left, right or center


# plt.xticks(np.arange(0,10,1))
# plt.yticks(np.arange(0,7,0.5))
plt.legend(('Система в \"+\"', 'Система в \"0\"', 'Система в \"-\"'), loc='lower right')
plt.show()
