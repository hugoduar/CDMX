import random
from objects import *


def load_route(file_name):
	route = []
	file = open(file_name, 'r')
	lines = file.readlines()
	for line in lines:
		route.append([int(x) for x in line.split(' ')])
	return route

def generate_random_cars(n):
	cars = []
	for i in range(n):
		rand_route = i%6 + 1
		particle_life_time = random.randint(100, 150)
		cars.append(Car(1, 'car %i' %i, particle_life_time, load_route('routes/route_%i.out'%rand_route)))

	return cars

