from math import sqrt
import matplotlib.pyplot as pl
import numpy as np


#x' = alpha - x^2
alpha_min = -1
alpha_max = 1
def positive_side_sqrt(x):
    if x>=0:
        return sqrt(x)
def negative_side_sqrt(x):
    if x>=0:
        return -sqrt(x)

alphas = np.linspace(alpha_min,alpha_max,10000)

pl.xlabel('alpha')
pl.ylabel('x')
pl.title('Bifurcation diagram')
pl.plot(alphas, [positive_side_sqrt(x) for x in alphas], "g-",label='Stable', )
pl.plot(alphas, [negative_side_sqrt(x) for x in alphas], "r-",label='Unstable', )
pl.legend(loc = "lower left")
pl.axis([alpha_min, alpha_max,-2,2])
pl.show()


#x' = alpha - x^2
alpha_min = 2
alpha_max = 4
def positive_side_sqrt_2(x):
    if x>=3:
        return sqrt((x - 3) / 2)
def negative_side_sqrt_2(x):
    if x>=3:
        return -sqrt((x - 3) / 2)

alphas = np.linspace(alpha_min,alpha_max,10000)

pl.xlabel('alpha')
pl.ylabel('x')
pl.title('Bifurcation diagram')
pl.plot(alphas, [positive_side_sqrt_2(x) for x in alphas], "g-",label='Stable', )
pl.plot(alphas, [negative_side_sqrt_2(x) for x in alphas], "r-",label='Unstable', )
pl.legend(loc = "lower left")
pl.axis([alpha_min, alpha_max,-2,2])
pl.show()