import pygame
import pickle
from utils import NeuralNetwork
import playercar as pc

# Inicializar pygame
pygame.init()
screen = pygame.display.set_mode((1600, 900))
clock = pygame.time.Clock()
font = pygame.font.SysFont("Arial", 20)

# Cargar imágenes
background = pygame.image.load("bg7.png")
collision_map = pygame.image.load("bg4.png")
car_image = pygame.image.load("Images/Sprites/green_small.png")

# Cargar top 10 redes
with open("top_networks.pkl", "rb") as f:
    top_networks = pickle.load(f)

# Inicializar autos con cada red neuronal
cars = []
for nn in top_networks:
    car = pc.PlayerCar(car_image)
    car.show_sensors = True
    cars.append((car, nn))

# HUD general
def draw_hud(screen, start_ticks, cars):
    elapsed = (pygame.time.get_ticks() - start_ticks) // 1000
    minutes = elapsed // 60
    seconds = elapsed % 60
    t1 = font.render(f"Tiempo: {minutes:02}:{seconds:02}", True, (255, 255, 255))
    t2 = font.render(f"Autos vivos: {sum(car.alive for car, _ in cars)}", True, (255, 255, 255))
    screen.blit(t1, (20, 20))
    screen.blit(t2, (20, 50))

# Bucle principal
start_ticks = pygame.time.get_ticks()
running = True

while running:
    screen.blit(background, (0, 0))

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

    # Actualizar y dibujar todos los autos
    for idx, (car, nn) in enumerate(cars):
        if car.alive:
            car.update()
            car.update_sensors(collision_map)
            input_vector = car.distances + [car.velocity]
            actions = nn.decide_action(input_vector)

            car.set_accel(0.2 if actions[0] else -0.2 if actions[1] else 0)
            if actions[2]: car.rotate(-5)
            if actions[3]: car.rotate(5)

            if car.check_collision(collision_map):
                print(f"Auto #{idx+1} colisionó. Score: {car.score:.2f}")
                car.velocity = 0
                car.acceleration = 0
                car.alive = False

        # Dibujar auto
        car.draw(screen)

    # Dibujar HUD general
    draw_hud(screen, start_ticks, cars)

    pygame.display.update()
    clock.tick(30)

    # Fin si todos han muerto o pasan 40 segundos
    elapsed = (pygame.time.get_ticks() - start_ticks) // 1000
    if all(not car.alive for car, _ in cars) or elapsed >= 40:
        print("Simulación finalizada.")
        for i, (car, _) in enumerate(cars):
            print(f"Auto #{i+1} - Score: {car.score:.2f}")
        pygame.time.delay(2000)
        break

pygame.quit()
