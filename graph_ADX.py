# Displays ADX data in graph form.

from ADX import DMI
import matplotlib.pyplot as plt

DIs = DMI('PEP', size=50)
# [0] is the past
DXs = []
for i in DIs:
    DX = (abs(i[0] - i[1]))/abs((i[0]+i[1])) * 100
    DXs.append(DX)
prior_ADX = sum(DXs[0:14])/14
ADX_list = []
for i in DXs[14:]:
    ADX = ((prior_ADX*13)+i)/14
    prior_ADX = ADX
    ADX_list.append(ADX)

DIs.reverse()
ADX_list.reverse()

x_values = [i+1 for i in range(len(DIs))]
y_pos_values = [i[0] for i in DIs]
y_neg_values = [i[1] for i in DIs]
y_ADX_values = ADX_list

# Adding a bunch of filler data to ADX list, it doesn't show later in the graph.
for i in range(14):
    y_ADX_values.append(0)

fig, ax = plt.subplots() # idk need to read documentation

ax.plot(x_values, y_pos_values, color='green', label='+DI')
ax.plot(x_values, y_neg_values, color='red', label='-DI')
ax.plot(x_values, y_ADX_values, color='blue', label='ADX')
plt.xlim([len(x_values), 0]) # makes the x axis go from [0] to [1]
ax.legend(loc="upper left", prop={'size': 20}) # legend font size -> 20

plt.show()
