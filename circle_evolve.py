
from PIL import Image, ImageDraw, ImageFilter
from random import randint
import os
from math import sqrt
import heapq

_DEFAULT_SIZE = (400,600)
def render_image(points,file):
	im = Image.new("RGB", _DEFAULT_SIZE , "#FFFFFF")
	draw = ImageDraw.Draw(im)
	C = find_centroid(points)
	for point in points:
		borders = ((point[0] - 1, point[1]-1), (point[0] + 1,  point[1]+1))
		draw.rectangle(borders, fill="#000000")
	
	borders = ((C[0] - 1, C[1]-1), (C[0] + 1,  C[1]+1))
	draw.rectangle(borders, fill="#FF0000")
	del draw
	output = os.path.join("C:\\Users\\Gleapsite\\Documents\\ColonialMakery\\Survival_of_the_Artist\\circle",file)
	print(output)
	im.save(output, "PNG")
	
def render_complex(individuals, file):
	im = Image.new("RGB", _DEFAULT_SIZE , "#FFFFFF")
	draw = ImageDraw.Draw(im)
	
	for i, individual in enumerate(individuals):
		C = find_centroid(individual)
		for j, point in enumerate(individual):
			#borders = ((point[0] - 1, point[1]-1), (point[0] + 1,  point[1]+1))
			#draw.rectangle(borders, fill="#000000")
			#print(point)
			#print(individuals[i+1][j])
			if i < len(individuals)-1:
				color = int(((len(individuals)-i)/len(individuals))*255)
				draw.line(point + individuals[i+1][j], fill=(color, color, color), width=2)
		im.filter(ImageFilter.GaussianBlur(radius=5))
	del draw
	output = os.path.join("C:\\Users\\Gleapsite\\Documents\\ColonialMakery\\Survival_of_the_Artist\\circle",file)
	print(output)
	im.save(output, "PNG")
	
	
def Generate_random_points(num, start=(0,0), size=_DEFAULT_SIZE):
	return [(randint(start[0], size[0]), randint(start[1], size[1])) for i in range(0,num)]


def check_fitness(points):
	C = find_centroid(points)
	radii = [find_distance(C, point) for point in points]
	#print(radii)
	#print("%s %s %s" % (C, min(radii), max(radii)))
	return max(radii) - min(radii)

def find_distance(point1, point2):
	return sqrt((point1[0]-point2[0])**2 + (point1[1]-point2[1])**2)

def find_centroid(points):
	x = 0
	y = 0
	for point in points: 
		x = x + point[0]
		y = y + point[1]
	x = x/len(points)
	y = y/len(points)
	return (x,y)

	
def Select_fittest(population, number):
	ranks = [check_fitness(individual) for individual in population]
	best = [] 
	for rank in heapq.nlargest(number, ranks):
		index = ranks.index(rank)
		best.append(population[index])
	return best

def generate_children(parent, popsize):
	#print(len(parent))
	return [mutate_points(parent[0]) for pop in range(0,popsize)]
	
def mutate_points(points):
	#print(len(points))
	return [mutate_point(point) for point in points]
		
def mutate_point(point):
	#print(point)
	x = point[0] + randint(-5,5)
	y = point[1] + randint(-5,5)
	if x < 0:
		x = 0
	if x > _DEFAULT_SIZE[0]:
		x = _DEFAULT_SIZE[0]
	if y < 0:
		y = 0
	if y > _DEFAULT_SIZE[1]:
		y = _DEFAULT_SIZE[1]
	return (x,y)

if __name__ == "__main__": 
	evolutionary_path = []
	pop_size = 100
	generations = 1000
	pop = [Generate_random_points(100) for i in range(0,pop_size)]
	
	for i in range(0,generations):
		print("GENERATION %i" % i)
		best = Select_fittest(pop, 1)  #bump up when crossover happens
		pop = generate_children(best, pop_size)
		evolutionary_path.append(best[0])
		
		if i > 20:
			render_complex(evolutionary_path, "path%i.png" % i)
			evolutionary_path.pop(0)
	
	


def old_test():
	individual = Generate_random_points(100)
	print(individual)
	render_image(individual, "test.png")
	check_fitness(individual)