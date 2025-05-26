import pygame
import playercar as pc
from utils import NeuralNetwork, save_top_networks, mutate_weights, mutate_biases, crossover_weights, crossover_biases
import random

pygame.init()
screen = pygame.display.set_mode((1600, 900))
clock = pygame.time.Clock()
font = pygame.font.SysFont("Arial", 20)

# Constantes
NUM_CARS = 200
TOP_K = 10
MUTATION_ROUNDS = 5

generation = 1

# Carga pista y colisiones
background = pygame.image.load("bg7.png")
collision_map = pygame.image.load("bg4.png")
car_image = pygame.image.load("Images/Sprites/white_small.png")

# Inicializar coches y redes
def init_population():
    cars = []
    networks = []
    for _ in range(NUM_CARS):
        car = pc.PlayerCar(car_image)
        car.show_sensors = False
        nn = NeuralNetwork(architecture=[6, 4, 4])
        cars.append(car)
        networks.append(nn)
    return cars, networks

cars, networks = init_population()

# HUD
def draw_hud(screen, cars, start_ticks, generation):
    elapsed_seconds = (pygame.time.get_ticks() - start_ticks) // 1000
    minutes = elapsed_seconds // 60
    seconds = elapsed_seconds % 60
    time_text = f"Tiempo: {minutes:02}:{seconds:02}"
    alive_text = f"Autos vivos: {sum(car.alive for car in cars)}"
    gen_text = f"Generación: {generation}"

    screen.blit(font.render(time_text, True, (255,255,255)), (20,20))
    screen.blit(font.render(alive_text, True, (255,255,255)), (20,50))
    screen.blit(font.render(gen_text, True, (255,255,0)), (20,80))

# Evolución
def evolve_generation(cars, networks):
    scored = sorted(zip(cars, networks), key=lambda x: x[0].score, reverse=True)
    # top_networks = [net.clone()[0] for _, net in scored[:TOP_K]]
    top_networks = [net.clone() for _, net in scored[:TOP_K]]

    new_cars, new_networks = [], []
    for _ in range(NUM_CARS):
        p1, p2 = random.sample(top_networks, 2)
        child = NeuralNetwork(p1.sizes)
        crossover_weights(p1, p2, child)
        crossover_biases(p1, p2, child)
        for _ in range(MUTATION_ROUNDS):
            mutate_weights(child)
            mutate_biases(child)
        car = pc.PlayerCar(car_image)
        car.show_sensors = False
        new_cars.append(car)
        new_networks.append(child)
    return new_cars, new_networks

# Loop principal
running = True
start_ticks = pygame.time.get_ticks()

while running:
    screen.blit(background, (0, 0))

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

    # Actualizar coches
    for car, nn in zip(cars, networks):
        if not car.alive:
            continue
        car.update()
        car.update_sensors(collision_map)
        input_vector = car.distances + [car.velocity]
        actions = nn.decide_action(input_vector)

        car.set_accel(0.2 if actions[0] else -0.2 if actions[1] else 0)
        if actions[2]: car.rotate(-5)
        if actions[3]: car.rotate(5)

        if car.check_collision(collision_map):
            car.velocity = 0
            car.acceleration = 0

        car.draw(screen)

    # Dibujar HUD
    # draw_hud(screen, cars, start_ticks)
    draw_hud(screen, cars, start_ticks, generation)

    # Verificar fin de generación
    elapsed_seconds = (pygame.time.get_ticks() - start_ticks) // 1000
    all_dead = all(not car.alive for car in cars)
    if all_dead or elapsed_seconds >= 40:
        print("Generación terminada")
        save_top_networks(networks, cars, top_n=TOP_K)
        generation += 1
        cars, networks = evolve_generation(cars, networks)
        start_ticks = pygame.time.get_ticks()

    pygame.display.update()
    clock.tick(30)

pygame.quit()
