import numpy as np
import finiteSimulator as simulator

def q5():
  k = [10, 25, 50]
  for i in k:
    rho_output = []
    print(f'k={i}')
    for j in range(5,16):
      print(f'rho={j/10}')
      rho = j/10
      lam = rho/0.002
      s = simulator.Simulator(int(lam), 1000000, 2000)
      res = s.simulate(1000, i)
      en = sum(res['packet_counts'])/res['observation_event_count']
      idle_counts = res['idle_observations']
      packets_lost = res['lost_packet_count']
      rho_output.append([rho, en, idle_counts, res['observation_event_count'], packets_lost, res['arrival_event_count'] ])
    np.savetxt(f'q6outputk{i}.csv', rho_output, delimiter=',', header="rho, E[N], idle observations, total observations made, packets lost, total arrival events")

q5()