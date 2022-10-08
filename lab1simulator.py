import numpy
import csv
import sys
import finiteSimulator
import simulator



def main(argv):
  finite_data_columns = [ 
    'idle_time',
    'idle_observations',
    'simulation_time',
    'arrival_event_count',
    'departure_event_count',
    'observer_event_count',
    'lost_packet_count',
    'en'
  ] 

  infinite_data_columns = [
    'lost_packet_count',
    'arrival_event_count',
    'departure_event_count',
    'observation_event_count',
    'idle_observations',
    'en'
  ]

  if (argv[0] == 'infinite'):
    s = simulator.Simulator(int(argv[2]), int(argv[3]),int(argv[4]))
    res = s.simulate(int(argv[1]))
    en = sum(res['packet_counts'])/res['observer_event_count']
    res.pop('packet_counts')
    res['en'] = en
    with open(f'{argv[5]}.csv', 'w') as csvfile:
      writer = csv.DictWriter(csvfile, fieldnames=finite_data_columns)
      writer.writeheader()
      writer.writerow(res)
  elif ((argv[0] == 'finite')):
    s = finiteSimulator.Simulator(int(argv[2]), int(argv[3]),int(argv[4]))
    res = s.simulate(int(argv[1]), int(argv[5]))
    en = sum(res['packet_counts'])/res['observation_event_count']
    res.pop('packet_counts')
    res['en'] = en
    with open(f'{argv[6]}.csv', 'w') as csvfile:
      writer = csv.DictWriter(csvfile, fieldnames=infinite_data_columns)
      writer.writeheader()
      writer.writerow(res)

if __name__ == "__main__":
   main(sys.argv[1:])