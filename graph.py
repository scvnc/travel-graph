#!/usr/bin/env python



import networkx as nx
import csv
from datetime import datetime
from sql import Route, session

from networkx.algorithms.shortest_paths.generic import shortest_path

def create_date_str(datetime):
  format = '%Y-%m-%d %I:%M %p %z'
  return datetime.strftime(format)
  
def create_date (datestr):
  format = '%Y-%m-%d %I:%M %p %z'
  return datetime.strptime(datestr, format)

def create(**kwargs):
  kwargs['depart'] = create_date(kwargs['depart'])
  kwargs['arrive'] = create_date(kwargs['arrive'])
  r = Route(**kwargs)
  session.add(r)
  

with open('routes.txt', 'r') as csvfile:
  spamreader = csv.reader(csvfile, delimiter=',', quotechar='"')
  for row in spamreader:
    create(
      source=row[0], 
      dest=row[1], 
      depart=row[2], 
      arrive=row[3], 
      fare=row[4],
      carrier=row[5])

session.commit()


class Location ():
  
  def __init__ (self, route):
    self._route = route

  @property
  def name (self):
    
    # If a route
    if(type(self._route) != str):
      return "{0}(${1})".format(self._route.dest, self._route.fare)
    
    else:
      return self._route


  @property
  def city_name (self):
    
    # If a route
    if(type(self._route) != str):
      return (self._route.dest)
    
    else:
      return self._route

  def __repr__ (self):
    return self.city_name


START=Location('LNK')
END=Location('NYP')
FINAL=Location('---')

G=nx.MultiDiGraph()

def populate_edges(location):
  
  # Query for all routes from this location
  routes = session.query(Route)\
    .filter(Route.source == location.city_name)
  
  # If we're arriving from a previous route, eliminate nonconnectables
  if type(location._route) == Route:
    routes = routes.filter(Route.depart > location._route.arrive)
  

  routes = routes.all()
  

  for route in routes:
    
    next_location = Location(route)
    
    G.add_edge(location, next_location, weight=route.fare)
    
    if(next_location.city_name == END.city_name):
      G.add_edge(next_location, FINAL)
    else:
      populate_edges(next_location)

populate_edges(START)


path = shortest_path(G, source=START,target=FINAL, weight='weight')


for node in path:
  print(node._route)
