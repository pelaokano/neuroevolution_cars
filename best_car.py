import pygame
from utils import NeuralNetwork
import playercar as pc

# Inicializar pygame
pygame.init()
screen = pygame.display.set_mode((1600, 900))
clock = pygame.time.Clock()
font = pygame.font.SysFont("Arial", 20)

# Cargar pista
background = pygame.image.load("bg7.png")
collision_map = pygame.image.load("bg4.png")

# Crear una red neuronal nueva (pesos/sesgos aleatorios)
nn = NeuralNetwork()  # usa arquitectura por defecto [6, 6, 4]

# Crear un auto controlado por esa red
car_image = pygame.image.load("Images/Sprites/white_small.png")
car = pc.PlayerCar(car_image)
car.show_sensors = True

# Tiempo inicial
start_ticks = pygame.time.get_ticks()

def draw_hud(screen, car, start_ticks):
    elapsed_seconds = (pygame.time.get_ticks() - start_ticks) // 1000
    minutes = elapsed_seconds // 60
    seconds = elapsed_seconds % 60
    t1 = font.render(f"Tiempo: {minutes:02}:{seconds:02}", True, (255, 255, 255))
    t2 = font.render(f"Score: {int(car.score)}", True, (255, 255, 255))
    screen.blit(t1, (20, 20))
    screen.blit(t2, (20, 50))

# Bucle principal
running = True
while running:
    screen.blit(background, (0, 0))

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

    if car.alive:
        car.update()
        car.update_sensors(collision_map)
        input_vector = car.distances + [car.velocity]
        actions = nn.decide_action(input_vector)

        car.set_accel(0.2 if actions[0] else -0.2 if actions[1] else 0)
        if actions[2]: car.rotate(-5)
        if actions[3]: car.rotate(5)

        if car.check_collision(collision_map):
            print("Colisión.")
            car.velocity = 0
            car.acceleration = 0

    car.draw(screen)
    draw_hud(screen, car, start_ticks)
    pygame.display.update()
    clock.tick(30)

pygame.quit()
