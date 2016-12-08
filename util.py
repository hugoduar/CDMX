import random
from objects import *


def generate_random_cars(n, x, y, size):
	cars = [[ None for j in range(y)] for i in range(x)]

	for i in range(n):
		xrand = random.randint(0, x-1)
		yrand = random.randint(0, y-1)
		direction = random.choice(['UP', 'DOWN', 'LEFT', 'RIGHT'])
		particle_life_time = random.randint(100, 150)
		cars[xrand][yrand] = Car(direction, 1, 'car %i' %i, particle_life_time)

	return cars

