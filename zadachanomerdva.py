import numpy as np
import requests
import csv
from scipy.special import spherical_jn, spherical_yn
import matplotlib.pyplot as plt
import os
from io import StringIO


def h_func(n, x):
 return spherical_jn(n, x) + 1j * spherical_yn(n, x)


def a_func(n, kr):
 return spherical_jn(n, kr) / h_func(n, kr)


def b_func(n, kr):
 b_numerator = kr * spherical_jn(n-1, kr) - n * spherical_jn(n, kr)
 b_denominator = kr * h_func(n-1, kr) - n * h_func(n, kr)
 return b_numerator / b_denominator


def a(r, f):
 w = 3e8 / f
 k = 2 * np.pi / w
 kr = k * r
 result = 0
 for n in range(1, 30):
  term = ((-1) ** n) * (n + 0.5) * (b_func(n, kr) - a_func(n, kr))
  result += term

 return (w ** 2 / np.pi) * (np.abs(result) ** 2)



url = "https://jenyay.net/uploads/Student/Modelling/task_rcs.csv"
response = requests.get(url)
data = response.text
csv_data = csv.reader(StringIO(data))
for row in csv_data:
 variant = row[0]
 if variant == "3":
  D = float(row[1])
  fmin = float(row[2])
  fmax = float(row[3])

f = np.linspace(fmin,fmax,500)
r = D / 2

F = []
L = []
rcs = []
data = []

for f1 in f:
 V = a(r, f1)
 F.append(f1)
 L.append(3e8 / f1)
 rcs.append(V)


if not os.path.exists('results'):
 os.makedirs('results')

with open('results/values.csv','w') as file:
 writer = csv.writer(file)
 for i, (val1, val2) in enumerate(zip(F, rcs), start=1):
   writer.writerow([i, val1, val2])




plt.figure(figsize=(16, 9))
plt.plot(F, rcs, label='f(x)', color='k')
plt.title('График')
plt.xlabel('F')
plt.ylabel('rcs')
plt.grid(True)
plt.legend()
plt.show()
