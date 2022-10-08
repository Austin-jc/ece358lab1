import numpy as np
import matplotlib.pyplot as plt
from scipy.optimize import curve_fit
from queue import Queue

#classes might be overkill
class Simulator:
  def __init__(self, lam, transmission_rate, avg_packet_length, observer_rate_multiplier = 5):
    self.lam = lam # average number of packets arriving per sec
    self.avg_packet_length = avg_packet_length # L
    self.transmission_rate = transmission_rate # aka service rate, C
    self.observer_rate = lam * observer_rate_multiplier # alpha

  def random_exp(self, avg, size=1):
    uniform_dist = np.random.uniform(0,1, size)
    if size == 1:
      return (-1/avg)*np.log(1-uniform_dist[0])
    return [(-1/avg)*np.log(1-u) for u in uniform_dist]

  def simulate(self, time):
    trafficQueue = Queue(maxsize=0) # use standard queue of infinite size. get() is O(1)
    observation_data = { 
      'packet_counts': [],
      'idle_time': 0,
      'idle_observations': 0,
      'simulation_time': time,
      'arrival_event_count': 0,
      'departure_event_count': 0,
      'observer_event_count': 0,
      'lost_packet_count': 0,
    }

    queue_empty_start_time = 0
    # generate the arrival events
    desQueue = self.generate_des_event_queue(time)
    # interate desQueue by going in order, pushing poping into q 
    for event in desQueue:
      if (event['timestamp'] > time): 
        # return if simulation time reached
        return observation_data
  
      if (event['type'] == 'arrival'):
        observation_data['arrival_event_count'] += 1
        if (trafficQueue.empty()):
          # log idle time
          observation_data['idle_time'] += abs(event['timestamp'] - queue_empty_start_time)
        trafficQueue.put_nowait(event) 
      elif (event['type'] == 'departure'):
        observation_data['departure_event_count'] += 1
        trafficQueue.get_nowait()
        if (trafficQueue.empty()):
          #start idle counter
          queue_empty_start_time = event['timestamp']
      elif (event['type'] == 'observation'):
        observation_data['observer_event_count'] += 1
        # how to calc avg number https://piazza.com/class/l7kkceewigl6py/post/87
        observation_data['packet_counts'].append(trafficQueue.qsize())
        if(trafficQueue.empty()):
          observation_data['idle_observations'] += 1
    return observation_data
  
  def generate_packet_arrivals(self, time):
    event_count = time * self.lam
    arrivals = []
    arrival_time = 0
    for i in range(event_count):
      arrival_time += self.random_exp(self.lam) # add inter arrival time
      packet_length = self.random_exp(1/self.avg_packet_length) # 1/L because we want the average to be L, but the exponential distribution mean is the inverse
      arrivals.append({ 'timestamp': arrival_time, 'packet_length': packet_length, 'type': 'arrival' })
    return arrivals
    
  def calc_departure_times(self, packet_events):
    #departure time is arrival + serivce time + leftover time from other packets in the queue
    departure_times = []
    next_free_time = 0
    for i in range(len(packet_events)):
      departure_time = max(packet_events[i]['timestamp'], next_free_time) + (packet_events[i]['packet_length'] / self.transmission_rate) # from the slides L/C @ 12 minutes
      next_free_time = departure_time
      departure_times.append({'timestamp': departure_time, 'type': 'departure' })
    return departure_times

  def generate_observer_events(self, time):
    event_count = time * self.observer_rate
    observations = []
    observation_timestamp = 0
    for i in range(event_count):
      observation_timestamp += self.random_exp(self.observer_rate)
      observations.append({ 'timestamp': observation_timestamp, 'type': 'observation' })
    return observations

  def generate_des_event_queue(self, time):
    arrival_events = self.generate_packet_arrivals(time)
    departure_times = self.calc_departure_times(arrival_events)
    observer_events = self.generate_observer_events(time)

    # im choosing to sort at end rather than use a PQ https://stackoverflow.com/questions/3759112/whats-faster-inserting-into-a-priority-queue-or-sorting-retrospectively#:~:text=Inserting%20n%20items%20into%20a,You%20need%20to%20test.
    desQueue = arrival_events + departure_times + observer_events
    desQueue.sort(key=lambda x: x['timestamp'])
    return desQueue


def q3(title):
  output = []
  for i in range(25,96):
    print(str(i-24) + '/70 ')
    rho = i/100
    lam = rho/0.002
    s = Simulator(int(lam), 1000000, 2000)
    res = s.simulate(1000)

    # arrivals = s.generate_packet_arrivals(1000)
    # packet_lengths = [a['packet_length'] for a in arrivals]
    # sum(packet_lengths)/len(packet_lengths)
    en = sum(res['packet_counts'])/res['observer_event_count']
    p_idle = res['idle_time']
    print("pidle: " + str(p_idle))
    output.append([rho, en, p_idle, res['idle_observations'], res['observer_event_count']])
  a = np.asarray(output)
  np.savetxt(f'{title}.csv', a, delimiter=",")
  print('done!')

def stability_test():
  s = Simulator(125, 1000000, 2000)
  res1 = s.simulate(1000)
  res2 = s.simulate(2000)
  en1 = sum(res1['packet_counts'])/res1['observer_event_count']
  en2 = sum(res2['packet_counts'])/res2['observer_event_count']
  return en1/en2

def q4():
  lam = 1.2/0.002
  s = Simulator(int(lam), 1000000, 2000)
  res = s.simulate(1000)
  # en = sum(res['packet_counts'])/res['observer_event_count']
  p_idle = res['idle_time']
  print(en)
  print(p_idle)
  # np.savetxt("ece358lab1q4.csv", np.asarray(res['packet_counts']), delimiter=",")

