import numpy
import pandas

import sys
import finiteSimulator
import simulator



def main(argv):
  finite_data_columns = [
    'packet_counts', 
    'idle_time',
    'idle_observations',
    'simulation_time',
    'arrival_event_count',
    'departure_event_count',
    'observer_event_count',
    'lost_packet_count'
  ] 

  infinite_data_columns = [
    'lost_packet_count',
    'arrival_event_count',
    'departure_event_count',
    'observation_event_count',
    'packet_counts',
    'idle_observations'
  ]

  if (argv[0] == 'infinite'):
    s = simulator.Simulator(int(argv[2]), int(argv[3]),int(argv[4]))
    res = s.simulate(int(argv[1]))
    df = pandas.DataFrame(res, columns=finite_data_columns)
    df.to_csv(argv[5])
  elif ((argv[0] == 'finite')):
    s = finiteSimulator.Simulator(int(argv[2]), int(argv[3]),int(argv[4]))
    res = s.simulate(int(argv[1]), int(argv[5]))
    df = pandas.DataFrame(res, columns=infinite_data_columns)
    df.to_csv(argv[6])

if __name__ == "__main__":
   main(sys.argv[1:])