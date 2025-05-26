import pygame
import math

def move(point, angle, unit):
    x, y = point
    rad = math.radians(-angle % 360)
    x += unit * math.sin(rad)
    y += unit * math.cos(rad)
    return x, y

def rotation(origin, point, angle):
    ox, oy = origin
    px, py = point
    qx = ox + math.cos(angle) * (px - ox) - math.sin(angle) * (py - oy)
    qy = oy + math.sin(angle) * (px - ox) + math.cos(angle) * (py - oy)
    return qx, qy

class PlayerCar:
    def __init__(self, image, x=120, y=480, angle=180, max_speed=10):
        self.car_image = image
        self.x = x
        self.y = y
        self.angle = angle
        self.velocity = 0
        self.acceleration = 0
        self.max_speed = max_speed
        self.width = 17
        self.height = 35
        self.update_corners()
        self.show_sensors = True
        self.sensors = []  # lista de puntos finales
        self.distances = []  # lista de distancias (números)
        self.score = 0
        self.alive = True
        
        self.initial_x = x
        self.initial_y = y
        self.no_movement_counter = 0
        self.max_stuck_frames = 300  # 4 segundos si usas 30 FPS
        self.distance_tol = 50
        
        self.prev_positions = []  # historial de posiciones
        self.prev_angles = []     # historial de ángulos
        self.stuck_rotation_counter = 0

    def update_corners(self):
        self.center = self.x, self.y
        w2, h2 = self.width / 2, self.height / 2
        self.a = self.x - w2, self.y + h2
        self.b = self.x + w2, self.y + h2
        self.c = self.x + w2, self.y - h2
        self.d = self.x - w2, self.y - h2
        self.a = rotation(self.center, self.a, math.radians(self.angle))
        self.b = rotation(self.center, self.b, math.radians(self.angle))
        self.c = rotation(self.center, self.c, math.radians(self.angle))
        self.d = rotation(self.center, self.d, math.radians(self.angle))
    
    def update_sensors(self, collision_surface):
        self.sensors = []
        self.distances = []
        angles = [0, 45, -45, 90, -90]
        max_distance = 200
        for delta_angle in angles:
            sensor_angle = self.angle + delta_angle
            point = self.center
            distance = 0
            while distance < max_distance:
                x, y = move(point, sensor_angle, distance)
                x, y = int(x), int(y)
                if (0 <= x < collision_surface.get_width() and 
                    0 <= y < collision_surface.get_height()):
                    if collision_surface.get_at((x, y)).a == 0:
                        break
                distance += 1
            end_point = move(self.center, sensor_angle, distance)
            self.sensors.append(end_point)
            self.distances.append(distance)

    def set_accel(self, accel):
        self.acceleration = accel

    def rotate(self, rot):
        self.angle = (self.angle + rot) % 360
        
    def detect_spinning(self):
        if len(self.prev_positions) < 30:
            return

        dx = self.prev_positions[-1][0] - self.prev_positions[0][0]
        dy = self.prev_positions[-1][1] - self.prev_positions[0][1]
        net_distance = math.hypot(dx, dy)

        angle_diff = abs(self.prev_angles[-1] - self.prev_angles[0])
        if angle_diff > 180:
            angle_diff = 360 - angle_diff

        if net_distance < 10 and angle_diff > 90:
            self.stuck_rotation_counter += 1
        else:
            self.stuck_rotation_counter = 0

        if self.stuck_rotation_counter > 30:
            self.alive = False
    
    def update(self):
        if not self.alive:
            return

        self.score += self.velocity

        # Actualización de velocidad
        if self.acceleration != 0:
            self.velocity += self.acceleration
            self.velocity = max(0, min(self.velocity, self.max_speed))
        else:
            self.velocity *= 0.92

        # Movimiento
        self.x, self.y = move((self.x, self.y), self.angle, self.velocity)
        self.update_corners()

        # Verificar si está estancado (poca distancia desde el inicio)
        dx = self.x - self.initial_x
        dy = self.y - self.initial_y
        distance_from_start = math.hypot(dx, dy)

        if distance_from_start < self.distance_tol:
            self.no_movement_counter += 1
        else:
            self.no_movement_counter = 0

        if self.no_movement_counter > self.max_stuck_frames:
            print("Auto eliminado por estar quieto.")
            self.alive = False

        # Historial de posición y ángulo
        self.prev_positions.append((self.x, self.y))
        self.prev_angles.append(self.angle)

        if len(self.prev_positions) > 30:
            self.prev_positions.pop(0)
            self.prev_angles.pop(0)

        # Detección de giro en el lugar
        if len(self.prev_positions) >= 30:
            dx = self.prev_positions[-1][0] - self.prev_positions[0][0]
            dy = self.prev_positions[-1][1] - self.prev_positions[0][1]
            net_distance = math.hypot(dx, dy)

            angle_diff = abs(self.prev_angles[-1] - self.prev_angles[0])
            if angle_diff > 180:
                angle_diff = 360 - angle_diff

            if net_distance < 10 and angle_diff > 90:
                self.stuck_rotation_counter += 1
            else:
                self.stuck_rotation_counter = 0

            if self.stuck_rotation_counter > 30:
                print("Auto eliminado por girar en el lugar.")
                self.score = -100  # penalización fuerte
                self.alive = False

    def draw(self, surface):
        rotated = pygame.transform.rotate(self.car_image, -self.angle - 180)
        rect = rotated.get_rect()
        rect.center = (self.x, self.y)
        surface.blit(rotated, rect)
        
        if self.show_sensors:
            for end_point in self.sensors:
                pygame.draw.line(surface, (255, 0, 0), self.center, end_point, 1)

    def reset(self, x=120, y=480, angle=180):
        self.x, self.y, self.angle = x, y, angle
        self.velocity = 0
        self.acceleration = 0
        self.update_corners()

    def check_collision(self, collision_surface):
        if not self.alive:
            return False
        for point in [self.a, self.b, self.c, self.d]:
            x, y = int(point[0]), int(point[1])
            if 0 <= x < collision_surface.get_width() and 0 <= y < collision_surface.get_height():
                if collision_surface.get_at((x, y)).a == 0:
                    self.alive = False  # ← aquí marcamos al auto como "muerto"
                    return True
        return False
