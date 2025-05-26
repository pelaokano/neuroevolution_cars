import pygame
import playercar as pc
from utils import NeuralNetwork 
from utils import save_top_networks

pygame.init()
screen = pygame.display.set_mode((1600, 900))
clock = pygame.time.Clock()
font = pygame.font.SysFont("Arial", 20)

# Carga la pista visual y la de colisión
# background = pygame.image.load("randomGeneratedTrackFront.png")
# collision_map = pygame.image.load("randomGeneratedTrackBack.png")

def draw_nn_output(screen, output, x=20, y=20):
    pygame.draw.rect(screen, (0, 0, 0), (x - 10, y - 10, 200, 130))  # fondo negro
    labels = ["Acelerar", "Frenar", "Girar der.", "Girar izq."]
    for i, value in enumerate(output):
        text = f"{labels[i]}: {value:.2f}"
        rendered = font.render(text, True, (255, 255, 255))
        screen.blit(rendered, (x, y + i * 25))

def draw_hud(screen, cars, start_ticks):
    # Tiempo transcurrido en segundos
    elapsed_seconds = (pygame.time.get_ticks() - start_ticks) // 1000
    minutes = elapsed_seconds // 60
    seconds = elapsed_seconds % 60
    time_text = f"Tiempo: {minutes:02}:{seconds:02}"

    # Contador de autos vivos
    alive_count = sum(car.alive for car in cars)
    alive_text = f"Autos vivos: {alive_count}"

    # Renderizar y mostrar
    t1 = font.render(time_text, True, (255, 255, 255))
    t2 = font.render(alive_text, True, (255, 255, 255))
    screen.blit(t1, (20, 20))
    screen.blit(t2, (20, 50))

background = pygame.image.load("bg7.png")
collision_map = pygame.image.load("bg4.png")

# Carga imagen del auto
car_image = pygame.image.load("Images/Sprites/white_small.png")

# Parámetros
NUM_CARS = 200
cars = []
networks = []

# Inicialización de coches y redes
for _ in range(NUM_CARS):
    car = pc.PlayerCar(car_image)
    car.show_sensors = False
    nn = NeuralNetwork()
    cars.append(car)
    networks.append(nn)

# car = pc.PlayerCar(car_image)
# nn = NeuralNetwork()  # Red neuronal para controlar el coche

running = True
start_ticks = pygame.time.get_ticks()  # milisegundos desde el inicio

while running:
    screen.blit(background, (0, 0))

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

    
    # Evaluar y actualizar todos los autos
    for car, nn in zip(cars, networks):
        if not car.alive:
            continue  # salta este auto
        car.update()
        car.update_sensors(collision_map)
        input_vector = car.distances + [car.velocity]
        actions = nn.decide_action(input_vector)

        # Acciones de la red neuronal
        if actions[0]: car.set_accel(0.2)
        elif actions[1]: car.set_accel(-0.2)
        else: car.set_accel(0)

        if actions[2]: car.rotate(-5)
        if actions[3]: car.rotate(5)

        if car.check_collision(collision_map):
            # vuelve al principio
            # car.reset()
            
            # detiene el auto
            car.velocity = 0
            car.acceleration = 0

        car.draw(screen)
    
    # Verifica si todos los autos han "muerto" (colisionado)
    all_dead = all(not car.alive for car in cars)
    if all_dead:
        print("Todos los autos han colisionado.")
        save_top_networks(networks, cars, top_n=10)
        running = False
    
    # Obtener el mejor coche
    best_index = max(range(NUM_CARS), key=lambda i: cars[i].score)
    best_output = networks[best_index].feedforward(cars[best_index].distances + [cars[best_index].velocity])
    draw_hud(screen, cars, start_ticks)
    
    elapsed_seconds = (pygame.time.get_ticks() - start_ticks) // 1000
    if elapsed_seconds >= 60:
        print("Tiempo máximo alcanzado. Autos restantes serán desactivados.")
        for car in cars:
            car.alive = False
        
    pygame.display.update()
    clock.tick(30)
    
pygame.quit()
