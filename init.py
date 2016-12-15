import pprint
import time
from objects import *
import pygame,sys
from pygame.locals import *
from util import *

BLACK= pygame.Color(239,133,89)
WHITE = pygame.Color(250,233,226)
GRAY = pygame.Color(204,0,0)
pygame.init()
try: import psyco; psyco.full()
except: "Psyco module not found: will run a tad slower"
x = 1200
y = 700 

screen = pygame.display.set_mode((x, y))
factory_img = pygame.image.load('assets/factory_1.png').convert()
background = pygame.image.load('assets/ESCOM.png')
car_img = pygame.image.load('assets/car_1_UP.png').convert()
def update(screen, cars, factories,  particles):
	
	screen.blit(background, (0, 0))

	
	pollutant_size =2
	
	i = 0
	j = 0
	for row_factory in factories:
		j = 0
		for factory in row_factory:
			if factory is not None:
				screen.blit(factory_img, (i*pollutant_size,j*pollutant_size))
			j+=1
		i+=1


	car_size = 2
	
	x = 0
	for car in cars:
		print car.get_current_position()
		i, j = car.get_current_position()
		screen.blit(car_img, (i*car_size,j*car_size))
		particles[i][j].life_time += car.particle_life_time
		cars[x].move_forward()
		x+=1

	particle_size = 2

	i = 0
	j = 0
	for row_particle in particles:
		j = 0
		for particle in row_particle:
			s = pygame.Surface((particle_size,particle_size)) 
			if particle.life_time >= 128: 
				s.set_alpha(128)
			else:
				s.set_alpha(particle.life_time)
			s.fill(GRAY)           
			screen.blit(s, (i*particle_size,j*particle_size))
			
			j+=1
		i+=1
	
	

def update_factories(factories, particles, x, y):
	i = 0
	j = 0
	for row_factory in factories:
		j = 0
		for factory in row_factory:
			if factory is not None:
				particles[i][j].life_time+=factory.particle_life_time
			j+=1
		i+=1
	return particles	

def update_particles(particles, x, y, rain, air):
	particles2 = [[ Particle(0) for j in range(y)] for i in range(x)]
	i = 0
	j = 0
	for row_particle in particles:
		j=0
		for particle in row_particle:
			if particle is not None:
				if rain.active:
					particles[i][j].life_time -=rain.dispersion_ratio
				else:
					particles[i][j].life_time -= 1
				if particle.life_time < 0:
					particles[i][j].life_time = 0
			if air.direction is not 'STATIC':
				if air.direction == 'SOUTH':
					if j+1<y:
						particles2[i][j+1] = particles[i][j]
				if air.direction == 'NORTH':
					if j-1>=0:
						particles2[i][j-1] = particles[i][j]
				if air.direction == 'EAST':
					if i+1<x:
						particles2[i+1][j] = particles[i][j]
				if air.direction == 'WEST':
					if i-1>=0:
						particles2[i-1][j] = particles[i][j]
			j+=1
		i+=1

	if air.direction == 'STATIC':
		return particles
	else:
		return particles2


def main():
	


	
	clock = pygame.time.Clock()

	background = pygame.image.load('assets/ESCOM.png')
	screen.blit(background, (0, 0))

	streets = []
	car_size = 2
	cars = generate_random_cars(5)
	
	particle_size = 2
	particles = [[ Particle(0) for j in range(y/particle_size)] for i in range(x/particle_size)]
	factory_size = 2
	factories = [[ None for j in range(y/factory_size)] for i in range(x/factory_size)]

	factory1 = Factory('Factory1')
	factories[50][50] = factory1
	factory2 = Factory('Factory1')
	factories[60][60] = factory1
	factories[10][30] = factory1
	factories[20][80] = factory1
	factories[25][100] = factory1
	factories[190][120] = factory1
	factories[180][80] = factory1
	factories[160][70] = factory1

	air = Air('STATIC')
	rain = Rain(20, active=False)
	# pp = pprint.PrettyPrinter()
	# pp.pprint(cars)
	# print "-"*100
	# pp.pprint(particles)


	#Checar estados
	state_number = 0

	deleting = False
	paused = True
	moused = False
	while True:
		for e in pygame.event.get():
			if e.type == QUIT:
				pygame.quit()
				sys.exit()
			elif e.type == KEYDOWN:
				if e.key == K_ESCAPE: pygame.quit();  sys.exit()
				elif e.key == K_p: paused = not paused
				elif e.key == K_d: deleting = True
				elif e.key == K_r: rain.active = not rain.active
				elif e.key == K_UP: air.direction = 'NORTH'
				elif e.key == K_DOWN: air.direction = 'SOUTH'
				elif e.key == K_LEFT: air.direction = 'WEST'
				elif e.key == K_RIGHT: air.direction = 'EAST'
				elif e.key == K_s: air.direction = 'STATIC'
				elif e.key == K_a:
					print streets
					st_f = open('st_dump.out', 'w+')
					for row_street in streets:
						st_f.write('%i %i\n' % (row_street[0], row_street[1]))

			
			elif e.type == MOUSEBUTTONDOWN: moused = True
			elif e.type == MOUSEBUTTONUP: moused = False
			elif e.type == KEYUP:
				if e.key == K_d: deleting = False		

		# print "Current state %i" % state_number
		# pp = pprint.PrettyPrinter()
		# pp.pprint(cars)
		# print "-"*100
		# pp.pprint(particles)


		state_number+=1

		if moused == True:
				mx,my = [pygame.mouse.get_pos()[i]/2 for i in range(2)]
				if (mx, my) not in streets: 
					streets.append((mx, my))
				pygame.draw.rect(screen,GRAY,(mx*2,my*2,2,2))
		
		if deleting == True:	
			mx,my = [pygame.mouse.get_pos()[i]/2 for i in range(2)]
			streets.remove((mx, my))
			pygame.draw.rect(screen,BLACK,(mx*2,my*2,2,2))

		if paused == False:
			particles = update_factories(factories, particles, x/factory_size, y/factory_size)
			particles = update_particles(particles, x/particle_size, x/particle_size, rain, air)
			update(screen, cars, factories,  particles)

		clock.tick(40)	
		pygame.display.flip()
		pygame.time.delay(100)
		



if __name__ == '__main__':
	main()






