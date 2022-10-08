import numpy as np
import csv
import simulator
def q3():
  output = []
  headers = ['rho', 'E[N]', 'idle observations', 'total observations made']
  for i in range(25,96):
    print(str(i-24) + '/70 ')
    rho = i/100
    lam = rho/0.002
    s = simulator.Simulator(int(lam), 1000000, 2000)
    res = s.simulate(1000)

    # arrivals = s.generate_packet_arrivals(1000)
    # packet_lengths = [a['packet_length'] for a in arrivals]
    # sum(packet_lengths)/len(packet_lengths)
    en = sum(res['packet_counts'])/res['observer_event_count']
    output.append([rho, en, res['idle_observations'], res['observer_event_count']])
  with open('q3output.csv', 'w', newline='') as csvfile:
    writer = csv.writer(csvfile)
    writer.writerow(headers)
    writer.writerows(output)

q3()