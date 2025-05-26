import pygame
import random
from PIL import Image

class Cell:
    wall_pairs = {'N': 'S', 'S': 'N', 'E': 'W', 'W': 'E'}
    def __init__(self, x, y):
        self.x, self.y = x, y
        self.walls = {'N': True, 'S': True, 'E': True, 'W': True}
        self.color = 0, 0, 0

    def has_all_walls(self):
        return all(self.walls.values())

    def knock_down_wall(self, other, wall):
        self.walls[wall] = False
        other.walls[Cell.wall_pairs[wall]] = False

class Maze:
    def __init__(self, nx, ny):
        self.nx, self.ny = nx, ny
        self.maze_map = [[Cell(x, y) for y in range(ny)] for x in range(nx)]

    def cell_at(self, x, y):
        return self.maze_map[x][y]

    def find_valid_neighbours(self, cell):
        delta = [('W', (-1, 0)), ('E', (1, 0)), ('S', (0, 1)), ('N', (0, -1))]
        neighbours = []
        for direction, (dx, dy) in delta:
            x2, y2 = cell.x + dx, cell.y + dy
            if (0 <= x2 < self.nx) and (0 <= y2 < self.ny):
                neighbour = self.cell_at(x2, y2)
                if neighbour.has_all_walls():
                    neighbours.append((direction, neighbour))
        return neighbours

class TrackGenerator:
    def __init__(self, screen):
        self.screen = screen
        self.WIDTH, self.HEIGHT = 1460, 730
        self.blockSize = 146
        self.rows = int(self.WIDTH / self.blockSize)
        self.cols = int(self.HEIGHT / self.blockSize)
        self.movex = 70
        self.movey = 85
        self.maze = Maze(self.rows, self.cols)

        self._load_images()

    def _load_images(self):
        p = 'Images/TracksMapGen/'
        self.images = {
            "Straight1": pygame.image.load(p + 'Straight1.png'),
            "Straight2": pygame.image.load(p + 'Straight2.png'),
            "Curve1": pygame.image.load(p + 'Curve1.png'),
            "Curve2": pygame.image.load(p + 'Curve2.png'),
            "Curve3": pygame.image.load(p + 'Curve3.png'),
            "Curve4": pygame.image.load(p + 'Curve4.png'),
            "Straight1Top": pygame.image.load(p + 'Straight1Top.png'),
            "Straight2Top": pygame.image.load(p + 'Straight2Top.png'),
            "Curve1Top": pygame.image.load(p + 'Curve1Top.png'),
            "Curve2Top": pygame.image.load(p + 'Curve2Top.png'),
            "Curve3Top": pygame.image.load(p + 'Curve3Top.png'),
            "Curve4Top": pygame.image.load(p + 'Curve4Top.png'),
            "Initial": pygame.image.load(p + 'Initial.png'),
            "Background": pygame.image.load(p + 'Background.png')
        }

    def generate(self):
        startx, starty = 0, 3
        current = self.maze.cell_at(startx, starty)
        trackLength = 0

        while True:
            if len(self.maze.find_valid_neighbours(current)) > 0:
                if current.x == 0 and current.y == 3:
                    old = current
                    current = self.maze.cell_at(old.x, old.y - 1)
                    old.knock_down_wall(current, "N")
                else:
                    direction = random.choice(self.maze.find_valid_neighbours(current))[0]
                    old = current
                    if direction == "N": current = self.maze.cell_at(old.x, old.y - 1)
                    elif direction == "S": current = self.maze.cell_at(old.x, old.y + 1)
                    elif direction == "E": current = self.maze.cell_at(old.x + 1, old.y)
                    elif direction == "W": current = self.maze.cell_at(old.x - 1, old.y)
                    old.knock_down_wall(current, direction)
                trackLength += 1
            else:
                if current.x == 0 and current.y == 4 and trackLength > 40:
                    self._draw_track_surface()
                    self._draw_track_top()
                    break
                else:
                    self._reset_maze()
                    current = self.maze.cell_at(startx, starty)
                    trackLength = 0

    def _draw_track_surface(self):
        self.screen.fill((0, 0, 0))
        self.maze.cell_at(0, 4).knock_down_wall(self.maze.cell_at(0, 3), "N")

        for x in range(0, self.WIDTH, self.blockSize):
            for y in range(0, self.HEIGHT, self.blockSize):
                cell = self.maze.cell_at(x // self.blockSize, y // self.blockSize)
                pos = (x + self.movex, y + self.movey)
                if not cell.walls["N"] and not cell.walls["S"]:
                    self.screen.blit(self.images["Straight2"], pos)
                elif not cell.walls["E"] and not cell.walls["W"]:
                    self.screen.blit(self.images["Straight1"], pos)
                elif not cell.walls["N"] and not cell.walls["W"]:
                    self.screen.blit(self.images["Curve3"], pos)
                elif not cell.walls["W"] and not cell.walls["S"]:
                    self.screen.blit(self.images["Curve2"], pos)
                elif not cell.walls["S"] and not cell.walls["E"]:
                    self.screen.blit(self.images["Curve1"], pos)
                elif not cell.walls["E"] and not cell.walls["N"]:
                    self.screen.blit(self.images["Curve4"], pos)

        pygame.image.save(self.screen, "randomGeneratedTrackBack.png")
        self._make_background_transparent("randomGeneratedTrackBack.png")

    def _draw_track_top(self):
        self.screen.blit(self.images["Background"], (0, 0))
        for x in range(0, self.WIDTH, self.blockSize):
            for y in range(0, self.HEIGHT, self.blockSize):
                cell = self.maze.cell_at(x // self.blockSize, y // self.blockSize)
                pos = (x + self.movex, y + self.movey)
                if x == 0 and y == 3 * self.blockSize:
                    self.screen.blit(self.images["Initial"], pos)
                elif not cell.walls["N"] and not cell.walls["S"]:
                    self.screen.blit(self.images["Straight2Top"], pos)
                elif not cell.walls["E"] and not cell.walls["W"]:
                    self.screen.blit(self.images["Straight1Top"], pos)
                elif not cell.walls["N"] and not cell.walls["W"]:
                    self.screen.blit(self.images["Curve3Top"], pos)
                elif not cell.walls["W"] and not cell.walls["S"]:
                    self.screen.blit(self.images["Curve2Top"], pos)
                elif not cell.walls["E"] and not cell.walls["N"]:
                    self.screen.blit(self.images["Curve4Top"], pos)
                elif not cell.walls["S"] and not cell.walls["E"]:
                    self.screen.blit(self.images["Curve1Top"], pos)

        pygame.image.save(self.screen, "randomGeneratedTrackFront.png")
          
    def _make_background_transparent(self, filename):
        img = Image.open(filename).convert("RGBA")
        pixdata = img.load()
        for y in range(img.size[1]):
            for x in range(img.size[0]):
                if pixdata[x, y][:3] == (0, 0, 0) or pixdata[x, y][:3] == (0, 0, 1):
                    pixdata[x, y] = (0, 0, 0, 0)
        img.save(filename)

    def _reset_maze(self):
        for x in range(self.rows):
            for y in range(self.cols):
                cell = self.maze.cell_at(x, y)
                cell.walls = {'N': True, 'S': True, 'E': True, 'W': True}
                cell.color = (0, 0, 0)
        for i in range(3, 7):
            self.maze.cell_at(i, 3).walls["N"] = False

if __name__ == "__main__": 
    pygame.init()
    screen = pygame.display.set_mode((1600, 900))
    track_gen = TrackGenerator(screen)
    track_gen.generate()