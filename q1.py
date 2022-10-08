import numpy as np
import csv

def random_exp(avg, size):
  uniform_dist = np.random.uniform(0,1, size)
  if size == 1:
    return (-1/avg)*np.log(1-uniform_dist[0])
  return [(-1/avg)*np.log(1-u) for u in uniform_dist]

def q1(lam):
  means = []
  variances = []
  for i in range(10):
    res = random_exp(lam, 1000)
    means.append(np.mean(res))
    variances.append(np.var(res))
  return  { 'means': means, 'vars': variances }

res = q1(75)
with open('q1output.csv', 'w', newline='') as csvfile:
  writer = csv.writer(csvfile)
  writer.writerow(res.keys())
  writer.writerows(zip(*res.values()))
