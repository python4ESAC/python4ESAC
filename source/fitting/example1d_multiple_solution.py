import numpy as np
from scipy.optimize import curve_fit
import matplotlib.pyplot as mpl

# Let's create a function to model and create data
def func(x, a, x0, sigma):
    return a*np.exp(-(x-x0)**2/(2*sigma**2))

# Generating clean data
x = np.linspace(0, 20, 200)
y1 = func(x[np.where(x <= 10)], 1, 3, 1)
y2 = func(x[np.where(x > 10)], -2, 15, 0.5)

y = np.hstack([y1, y2])

# Adding noise to the data
yn = y + 0.2 * np.random.normal(size=len(x))

# Executing curve_fit on noisy data
popt, pcov = curve_fit(func, x, yn, p0=[-1,15,1])

#popt returns the best fit values for parameters of the given model (func)
print popt

ym = func(x, popt[0], popt[1], popt[2])

fig = mpl.figure()
ax = fig.add_subplot(111)
ax.plot(x, y, c='k', label='Function')
ax.scatter(x, yn)
ax.plot(x, ym, c='r', label='Best fit')
ax.legend()
fig.savefig('model_fit_multiple_solution.png')