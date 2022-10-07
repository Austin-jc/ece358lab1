import numpy as np
import matplotlib.pyplot as plt
from scipy.optimize import curve_fit
from queue import Queue

class Simulator:

  def __init__(self,
               lam,
               transmission_rate,
               avg_packet_length,
               observer_rate_multiplier=5):
    self.lam = lam  # average number of packets arriving per sec
    self.avg_packet_length = avg_packet_length  # L
    self.transmission_rate = transmission_rate  # aka service rate, C
    self.observer_rate = lam * observer_rate_multiplier  # alpha

  def random_exp(self, avg, size=1):
    uniform_dist = np.random.uniform(0,1, size)
    if size == 1:
      return (-1/avg)*np.log(1-uniform_dist[0])
    return [(-1/avg)*np.log(1-u) for u in uniform_dist]

  def simulate(self, time, buffersize=0):
    trafficQueue = Queue(
      maxsize=buffersize) 
    departureQueue = Queue(maxsize=0)
    lost_packet_count = 0
    arrival_event_count = 0
    departure_event_count = 0
    observation_event_count = 0
    packet_counts = []
    idle_observations = 0
    q = self.generate_packet_arrivals(1000) + self.generate_observer_events(
      1000)
    q.sort(key=lambda x: x['timestamp'])
    for event in q:
      # return if simulation time reached
      if (event['timestamp'] > time):
        return {
          'lost_packet_count': lost_packet_count,
          'arrival_event_count': arrival_event_count,
          'departure_event_count': departure_event_count,
          'observation_event_count': observation_event_count,
          'packet_counts': packet_counts,
          'idle_observations': idle_observations
        }

      # update the trafficQueue if a departure occured, arrival cannot happen at same time as departure so non inclusive
      while (not departureQueue.empty()
             and departureQueue.queue[0] < event['timestamp']):
        #since every departure is guaranteed to have an arrival, we can just blindy remove from traffic
        trafficQueue.get()
        departureQueue.get()

      if (event['type'] == 'arrival'):
        arrival_event_count += 1
        if (trafficQueue.full()):
          #if full just add to counter and move on
          lost_packet_count += 1
          continue
        #generate departure
        departureQueue.put_nowait(
          self.generate_departure_time(event, departureQueue))
        trafficQueue.put_nowait(event)

      elif (event['type'] == 'observation'):
        observation_event_count += 1
        # how to calc avg number https://piazza.com/class/l7kkceewigl6py/post/87
        packet_counts.append(trafficQueue.qsize())
        if (trafficQueue.empty()):
          idle_observations += 1

    return {
      'lost_packet_count': lost_packet_count,
      'arrival_event_count': arrival_event_count,
      'departure_event_count': departure_event_count,
      'observation_event_count': observation_event_count,
      'packet_counts': packet_counts,
      'idle_observations': idle_observations
    }

  def generate_departure_time(self, arrival_event, departureQueue):
    last_departure_time = -1
    if (not departureQueue.empty()):
      last_departure_time = departureQueue.queue[-1]
    departure_time = max(arrival_event['timestamp'], last_departure_time) + (
      arrival_event['packet_length'] / self.transmission_rate)
    return departure_time

  def generate_packet_arrivals(self, time):
    event_count = time * self.lam
    arrivals = []
    arrival_time = 0
    for i in range(event_count):
      arrival_time += self.random_exp(self.lam)  # add inter arrival time
      packet_length = self.random_exp(1/self.avg_packet_length)# 1/L because we want the average to be L, but the exponential distribution mean is the inverse
      arrivals.append({
        'timestamp': arrival_time,
        'packet_length': packet_length,
        'type': 'arrival'
      })
    return arrivals

  def generate_observer_events(self, time):
    event_count = time * self.observer_rate
    observations = []
    observation_timestamp = 0
    for i in range(event_count):
      # cant just do this sadge return [observation_timestamp += self.random_exp(scale = 1 / self.observer_rate) for i in range(event_count)]
      observation_timestamp += self.random_exp(self.observer_rate)
      observations.append({
        'timestamp': observation_timestamp,
        'type': 'observation'
      })
    return observations


def q5(title):
  k = [10, 25, 50]
  for i in k:
    rho_output = []
    print(f'k={i}')
    for j in range(5,16):
      print(f'rho={j/10}')
      rho = j/10
      lam = rho/0.002
      s = Simulator(int(lam), 1000000, 2000)
      res = s.simulate(1000, i)
      en = sum(res['packet_counts'])/res['observation_event_count']
      idle_counts = res['idle_observations']
      packets_lost = res['lost_packet_count']
      rho_output.append([rho, en, idle_counts, res['observation_event_count'], packets_lost, res['arrival_event_count'] ])
    np.savetxt(f'{title}.csv', rho_output, delimiter=',')

def stability_test():
  s = Simulator(125, 1000000, 2000)
  res1 = s.simulate(1000, 25)
  res2 = s.simulate(2000, 25)
  en1 = sum(res1['packet_counts'])/res1['observation_event_count']
  en2 = sum(res2['packet_counts'])/res2['observation_event_count']
  return en1/en2
