class Car(object):
	"""docstring for Car
		@direction Direction that the cell is going to move 
		@required_steps Steps needed to produce a pollutant 
		@current_step Current step the cell is in 
		@label label for the object
	"""
	def __init__(self, required_steps, label, particle_life_time, route, color=1, current_step=0):
		super(Car, self).__init__()
		self.required_steps = required_steps 
		self.current_step = current_step
		self.label = label
		self.particle_life_time = particle_life_time
		self.color = color
		self.route = route
		self.route_i = 0
		self.position = self.route[self.route_i]

	def get_current_position(self):
		return self.position
	def get_next_position(self):
		return self.route[self.route_i +1]
	def move_forward(self):
		self.route_i += 1 
		self.position = self.route[self.route_i]
		return self.get_current_position()
	def move_backward(self):
		self.route_i -= 1 
		self.position = self.route[self.route_i]
		return self.get_current_position()
	def __repr__(self):
		return self.label

class Particle(object):
	"""docstring for Particle
		@life_time the number of states the Particle is going to die in
	"""
	def __init__(self, life_time):
		super(Particle, self).__init__()
		self.life_time = life_time
	def __repr__(self):
		return str(self.life_time)

class Factory(object):
	"""docstring for Factory
		@label label for the object
	"""
	def __init__(self, label):
		super(Factory, self).__init__()
		self.label = label
		self.particle_life_time = 100
	def __repr__(self):
		return self.label


class Air(object):
	"""docstring for Air
		@direction Direction that the pollutant is going to move 
	"""
	def __init__(self, direction):
		super(Air, self).__init__()
		self.direction = direction
	def __repr__(self):
		return self.direction

class Rain(object):
	"""docstring for Rain
		@direction Direction that the pollutant is going to move 
	"""
	def __init__(self, dispersion_ratio, active=False):
		super(Rain, self).__init__()
		self.dispersion_ratio = dispersion_ratio
		self.active = active
	def __repr__(self):
		return "Raining"

		

