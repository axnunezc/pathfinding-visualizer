from cmath import inf, sqrt
from sre_parse import WHITESPACE
from flask import redirect
import pygame
import math
from queue import PriorityQueue

WINDOW_LENGTH = 800
WINDOW = pygame.display.set_mode((WINDOW_LENGTH, WINDOW_LENGTH))
pygame.display.set_caption("Pathfinding Visualizer")

RED = (255, 0, 0)
GREEN = (0, 255, 0)
BLUE = (0, 0, 255)
YELLOW = (255, 255, 0)
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
PURPLE = (128, 0, 128)
ORANGE = (255, 165 ,0)
GREY = (128, 128, 128)
TURQUOISE = (64, 224, 208)

class Node:
    def __init__(self, row, col, size, rows):
        self.row = row
        self.col = col
        self.x = row * size
        self.y = col * size
        self.color = WHITE
        self.neighbors = []
        self.size = size
        self.rows = rows
       
    def get_location(self):
        return self.row, self.col
    
    def is_closed(self):
        return self.color == RED
    
    def is_open(self):
        return self.color == GREEN
    
    def is_obstacle(self):
        return self.color == BLACK
    
    def is_start(self):
        return self.color == ORANGE
    
    def is_end(self):
        return self.color == PURPLE
    
    def make_closed(self):
        self.color = RED
        
    def make_open(self):
        self.color = GREEN
        
    def make_obstacle(self):
        self.color = BLACK
        
    def make_start(self):
        self.color = ORANGE
        
    def make_end(self):
        self.color = PURPLE
        
    def mark(self):
        self.color = BLUE
    
    def reset(self):
        self.color = WHITE
        
    def draw(self, window):
        pygame.draw.rect(window, self.color, (self.x, self.y, self.size, self.size))
        
    def update_neighbors(self, grid):
        self.neighbors = []
        # up
        if self.row > 0 and not grid[self.row - 1][self.col].is_obstacle():
            self.neighbors.append(grid[self.row - 1][self.col])
        # down    
        if self.row < self.rows - 1 and not grid[self.row + 1][self.col].is_obstacle():
            self.neighbors.append(grid[self.row + 1][self.col])
        # left    
        if self.col > 0 and not grid[self.row][self.col - 1].is_obstacle():
            self.neighbors.append(grid[self.row][self.col - 1])
        # right
        if self.col < self.rows - 1 and not grid[self.row][self.col + 1].is_obstacle():
            self.neighbors.append(grid[self.row][self.col + 1])
    
    def __lt__(self, other):
        return False
    
def h(a, b):
    x1, y1 = a
    x2, y2 = b
    d = abs(x1 - x2) + abs(y1 - y2)
    return d

def show_path(origin, current, draw):
    while current in origin:
        current = origin[current]
        current.mark()
        draw()

def a_star(draw, grid, start, end):
    count = 0
    open_set = PriorityQueue()
    open_set.put((0, count, start))
    origin = {}
    g_score = {node: float("inf") for row in grid for node in row}
    g_score[start] = 0
    f_score = {node: float("inf") for row in grid for node in row}
    f_score[start] = h(start.get_location(), end.get_location())
    
    open_set_hash = {start}
    
    while not open_set.empty():
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
            
        current = open_set.get()[2]
        open_set_hash.remove(current)
        
        if current == end:
            show_path(origin, end, draw)
            return True
        
        for neighbor in current.neighbors:
            temp_g = g_score[current] + 1
            
            if temp_g < g_score[neighbor]:
                origin[neighbor] = current
                g_score[neighbor] = temp_g
                h_score = h(neighbor.get_location(), end.get_location())
                f_score[neighbor] = temp_g + h_score
                
                if neighbor not in open_set_hash:
                    count += 1
                    open_set.put((f_score[neighbor], count, neighbor))
                    open_set_hash.add(neighbor)
                    neighbor.make_open()
        
        draw()
        
        if current != start:
            current.make_closed()
            
    return False

def dijkstra(draw, grid, start, end):
    count = 0
    open_set = PriorityQueue()
    open_set.put((0, count, start))
    origin = {}
    g_score = {node: float("inf") for row in grid for node in row}
    g_score[start] = 0
    
    open_set_hash = {start}
    
    while not open_set.empty():
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
            
        current = open_set.get()[2]
        open_set_hash.remove(current)
        
        if current == end:
            show_path(origin, end, draw)
            return True
        
        for neighbor in current.neighbors:
            temp_g = g_score[current] + 1
            
            if temp_g < g_score[neighbor]:
                origin[neighbor] = current
                g_score[neighbor] = temp_g
                
                if neighbor not in open_set_hash:
                    count += 1
                    open_set.put((g_score[neighbor], count, neighbor))
                    open_set_hash.add(neighbor)
                    neighbor.make_open()
        
        draw()
        
        if current != start:
            current.make_closed()
            
    return False

def greedy_best_first_search(draw, grid, start, end):
    count = 0
    open_set = PriorityQueue()
    open_set.put((0, count, start))
    origin = {}
    h_score = {node: float("inf") for row in grid for node in row}
    h_score[start] = math.inf
    
    open_set_hash = {start}
    
    while not open_set.empty():
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                
        current = open_set.get()[2]
        
        if current == end:
            show_path(origin, end, draw)
            return True
        
        for neighbor in current.neighbors:
            h_score[neighbor] = h(neighbor.get_location(), end.get_location())
                
            if neighbor not in open_set_hash:
                count += 1
                open_set.put((h_score[neighbor], count, neighbor))
                open_set_hash.add(neighbor)
                origin[neighbor] = current
                neighbor.make_open()
        
        draw()
        
        if current != start:
            current.make_closed()
            
    return False

def bfs(draw, grid, start, end):
    count = 0
    open_set = []
    open_set.append(start)
    origin = {}
    
    open_set_hash = {start}
    
    while len(open_set) > 0:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                
        current = open_set.pop(0)
        
        if current == end:
            show_path(origin, end, draw)
            return True
        
        for neighbor in current.neighbors:
            if neighbor not in open_set_hash:
                count += 1
                open_set.append(neighbor)
                open_set_hash.add(neighbor)
                origin[neighbor] = current
                neighbor.make_open()
        
        draw()
        
        if current != start:
            current.make_closed()
            
    return False

def dfs(draw, grid, start, end):
    count = 0
    open_set = []
    open_set.append(start)
    origin = {}
    
    open_set_hash = {start}
    
    while len(open_set) > 0:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                
        current = open_set.pop()
        
        if current == end:
            show_path(origin, end, draw)
            return True
        
        for neighbor in current.neighbors:
            if neighbor not in open_set_hash:
                count += 1
                open_set.append(neighbor)
                open_set_hash.add(neighbor)
                origin[neighbor] = current
                neighbor.make_open()
        
        draw()
        
        if current != start:
            current.make_closed()
            
    return False

def make_grid(rows, length):
    grid = []
    gap = length // rows
    for i in range(rows):
        grid.append([])
        for j in range(rows):
            node = Node(i, j, gap, rows)
            grid[i].append(node)
    return grid

def draw_grid(window, rows, length):
    gap = length // rows
    for i in range(rows):
        pygame.draw.line(window, GREY, (0, i*gap), (length, i*gap))
        for j in range(rows):
            pygame.draw.line(window, GREY, (j*gap, 0), (j*gap, length))
            
def draw(window, grid, rows, length):
    window.fill(WHITE)
    
    for row in grid:
        for node in row:
            node.draw(window)
            
    draw_grid(window, rows, length)
    pygame.display.update()

def get_clicked(position, rows, length):
    gap = length // rows
    y, x = position
    
    row = y // gap
    col = x // gap
    
    return row, col

def main(window, length):
    rows = 50
    grid = make_grid(rows, length)
    
    start = None
    end = None
    
    running = True

    while running:
        draw(window, grid, rows, length)
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
 
            if pygame.mouse.get_pressed()[0]:
                position = pygame.mouse.get_pos()
                row, col = get_clicked(position, rows, length)
                node = grid[row][col]
                
                if not start and node != end:
                    start = node
                    start.make_start()
                    
                elif not end:
                    end = node
                    end.make_end()
                    
                elif node != start and node != end:
                    node.make_obstacle()
            
            elif pygame.mouse.get_pressed()[2]:
                position = pygame.mouse.get_pos()
                row, col = get_clicked(position, rows, length)
                node = grid[row][col]
                node.reset()
                
                if node == start:
                    start = None
                elif node == end:
                    end = None
                    
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_SPACE and start and end:
                    for row in grid:
                        for node in row:
                            node.update_neighbors(grid)
                            
                    greedy_best_first_search(lambda: draw(window, grid, rows, length), grid, start, end)
                    
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_c:
                    start = None
                    end = None
                    grid = make_grid(rows, length)
            
    pygame.quit()
        
main(WINDOW, WINDOW_LENGTH)