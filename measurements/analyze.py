__author__ = 'mithrawnuruodo'

import matplotlib.pyplot as plt
import numpy as np



data = np.genfromtxt("slaprinter_down_one_step.dat", delimiter=",")

one_step = data[:,0]
two_steps = data[:,1]

plt.hist(one_step, normed=1, bins=5, label="steps=1")
plt.hist(two_steps, normed=1,bins=5, label="steps=2")
plt.legend(loc="upper right")
plt.savefig("measurement_hist.eps")
plt.clf()

mu1 = np.median(one_step)
mu2 = np.median(two_steps)

avg1 = np.mean(one_step)
avg2 = np.mean(two_steps)

print("mu1 =" + str(mu1))
print("mu2 =" + str(mu2))

print("avg1 =" + str(avg1))
print("avg2 =" + str(avg2))