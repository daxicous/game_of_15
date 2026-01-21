import pygame
import random

from collections import defaultdict
from pygame.locals import K_w, K_a, K_s, K_d


def init():
        global clock, display
        size = 4
        pygame.init()
        display = Display(size, size)
        clock = pygame.time.Clock()

class Display:
    def __init__(self, board_height=8, board_width=8):
        self.board_height = board_height
        self.board_width = board_width
        self.width = 240
        self.height = 240
        self.screen = pygame.display.set_mode((self.width * 2, self.height * 2))
        white = pygame.color.Color("white")
        self.font = pygame.font.SysFont("Arial", 48)
        self.text_cache = {
            str(i): self.font.render(str(i), True, white)
            for i in range(1, board_height * board_width)
        }


class Model:
    def __init__(self, board_height, board_width):
        self.dt = 0
        self.walls = defaultdict(set)
        self.start = None
        self.end = None
        self.board_height = board_height
        self.board_width = board_width
        self.running = True
        self.squares = {}
        self.selected = None
        self.occupied = [[False for _ in range(board_height)] for _ in range(board_width)]
        self.state = [[0 for _ in range(board_height)] for _ in range(board_width)]
        self.hash = None
        self.visited = set()

def main():
    init()
    model = Model(display.board_height, display.board_width)
    inputs = {
        'mouse_down': False,
        'last_mouse_down': False,
        'mouse_x': 0,
        'mouse_y': 0,
        'UP': False,
        'DOWN': False,
        'RIGHT': False,
        'LEFT': False,
    }

    movement = {}
    model = load_board(model)
    g = Graph()
    step = 0

    while model.running:
        if not pygame_running():
            model.running = False
            break

        model.dt = clock.tick(60) / 1000
        inputs = update_inputs(inputs)
        model = input_handler(inputs, movement, model, g)
        model = draw_handler(model)
        update_screen()
        step += 1

#randomly generated
def load_board(model):
    grid_size = display.board_height

    coords = [(x, y) for x in range(grid_size) for y in range(grid_size)]
    squares = {}

    for i in range(1, grid_size ** 2):
        random_index = random.randint(0, len(coords) - 1)
        selected_coord = coords.pop(random_index)
        squares[selected_coord] = i
        x, y = selected_coord
        model.occupied[x][y] = True

    model.squares = squares
    return model

def update_state(model):
    if model.hash is not None:
        model.visited.add(model.hash)
    for pos, val in model.squares:
        x, y = pos
        model.state[y][x] = val
    model.hash = hash(tuple(model.state))
    return model

def draw_handler(model):
    screen = display.screen
    bgcolor = pygame.color.Color("grey")
    screen.fill(bgcolor)
    draw_squares(model)
    return model
  
def draw_squares(model):
    square_width = display.width * 2 / (display.board_width * 1.5)
    square_height = display.width * 2 / (display.board_height * 1.5)
    screen = display.screen
    blue = pygame.color.Color("aqua")
    orange = pygame.color.Color("orange")

    total_board_width = square_width * model.board_width
    total_board_height = square_height * model.board_height

    if model.selected is None:
        x2, y2 = -1, -1
    else:
        x2, y2 = model.selected

    for (x, y), value in model.squares.items():
        color = blue if (x == x2 and y == y2) else orange
        r = pygame.Rect(0, 0, square_width - 5, square_height - 5)
        r.center = (square_width * x + 50, square_height * y + 50)
        pygame.draw.rect(display.screen, color, r)
        text_surf = display.text_cache[str(value)]
        screen.blit(text_surf, (square_width * x + 30, square_height * y + 20))

def update_inputs(inputs):
        keys = pygame.key.get_pressed()
        inputs['last_mouse_down'] = inputs['mouse_down']
        inputs['mouse_down'] = pygame.mouse.get_pressed()[0]
        inputs['mouse_x'], inputs['mouse_y'] = pygame.mouse.get_pos()
        inputs['W'] = keys[K_w]
        inputs['A'] = keys[K_a]
        inputs['S'] = keys[K_s]
        inputs['D'] = keys[K_d]
        return inputs

def input_handler(inputs, movement, model, g):
    x = inputs['mouse_x']
    y = inputs['mouse_y']
    x = int(x / (display.width * 2 / (display.board_width * 1.5)))
    y = int(y / (display.width * 2 / (display.board_width * 1.5)))

    if inputs['mouse_down'] and not inputs['last_mouse_down']:
        model.selected = (x, y)

    if model.selected is None:
        return model

    x, y = model.selected
    # Move selected square if possible
    if inputs['W']:
        if 0 <= x < display.board_width and 0 <= y - 1 < display.board_height:
            if model.occupied[x][y] and not model.occupied[x][y - 1]:
                value = model.squares[(x, y)]
                del model.squares[(x, y)]
                model.occupied[x][y] = False
                model.squares[(x, y - 1)] = value
                model.occupied[x][y - 1] = True

    if inputs['A']:
        if 0 <= x - 1 < display.board_width and 0 <= y < display.board_height:
            if not model.occupied[x - 1][y]:
                value = model.squares[(x, y)]
                del model.squares[(x, y)]
                model.occupied[x][y] = False
                model.squares[(x - 1, y)] = value
                model.occupied[x - 1][y] = True

    if inputs['S']:
        if 0 <= x < display.board_width and 0 <= y + 1 < display.board_height:
            if not model.occupied[x][y + 1]:
                value = model.squares[(x, y)]
                del model.squares[(x, y)]
                model.occupied[x][y] = False
                model.squares[(x, y + 1)] = value
                model.occupied[x][y + 1] = True

    if inputs['D']:
        if 0 <= x + 1 < display.board_width and 0 <= y < display.board_height:
            if not model.occupied[x + 1][y]:
                value = model.squares[(x, y)]
                del model.squares[(x, y)]
                model.occupied[x][y] = False
                model.squares[(x + 1, y)] = value
                model.occupied[x + 1][y] = True

    return model


def update_screen():
    pygame.display.flip()
    
# undirected graph
class Graph:
    # edges are a default dict adjacency list
    # weights is a default dict mapping (v1, v2) to a weight
    def __init__(
        self, nvertices=0, edges=None, directed=False, weights=None
    ):
        self.edges = edges if edges is not None else defaultdict(set)
        if nvertices == 0:
            self.update_nvertices()
        else:
            self.v = nvertices

        if not directed:
            self.update_undirected_edges()

        self.weights = weights if weights is not None else {}

    def add_v(self, name, edge_list):
        self.v += 1
        self.edges[name] = set(edge_list)

    def add_edge(self, v1, v2):
        self.edges[v1].add(v2)

    @staticmethod
    def process_edge_line(line, edges, all_v, directed):
        vertices = list(map(eval, line))
        for v in vertices:
            all_v.add(v)
        edges[vertices[0]] = set(vertices)
        if not directed:
            for v in vertices[1:]:
                edges[v].add(vertices[0])

    @staticmethod
    def process_weight_line(line, weights, directed):
        parts = list(map(eval, line))
        v1, v2, weight = parts[0], parts[1], parts[2]
        weights[(v1, v2)] = weight
        if not directed:
            weights[(v2, v1)] = weight

    @staticmethod
    def cleanup(edges, weights, all_v):
        all_v = list(all_v)
        all_v.sort()
        index = {v: i for i, v in enumerate(all_v)}
        edges2 = defaultdict(list)
        for v, neighbors in edges.items():
            edges2[index[v]] = [index[v2] for v2 in neighbors]
        weights2 = defaultdict(int)
        for (v1, v2), weight in weights.items():
            weights2[index[v1], index[v2]] = weight
        return edges2, weights2

    @classmethod
    def from_string(cls, string, directed=False):
        lines = string.split('\n')
        edges = defaultdict(set)
        weights = defaultdict(int)
        all_v = set()
        is_weight = False

        for row in lines:
            line = row.strip()
            if str(row) == '# WEIGHTS':
                is_weight = True
                continue
            if not line:
                continue
            if line[0] == '#':
                continue
            parts = line.split()
            if is_weight:
                cls.process_weight_line(parts, weights, directed)
            else:
                cls.process_edge_line(parts, edges, all_v, directed)

        return Graph(len(all_v), edges, directed, weights)

    def update_nvertices(self):
        self.v = len(self.edges)

    def update_undirected_edges(self):
        for v, neighbors in self.edges.items():
            for v2 in neighbors:
                if v not in self.edges[v2]:
                    self.edges[v2].add(v)

    def print_edges(self, edges):
        ans = ""
        for v, neighbors in edges.items():
            ans += f"\n{v}: {neighbors}"
        return ans

    def print_weights(self, weights):
        ans = ""
        for (v1, v2), w in weights.items():
            ans += f"\n({v1}, {v2}): {w}"
        return ans

    def __repr__(self):
        return (
            f"[Graph, V={self.v}, E={self.print_edges(self.edges)}, "
            f"W={self.print_weights(self.weights)}]"
        )

    def repr2(self):
        ans = "String representation:\n"
        for v1, edges in self.edges.items():
            ans += str(v1) + " "
            for v2 in edges:
                ans += str(v2) + " "
            ans += "\n"
        return ans
        
def pygame_running():
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            return False
    return True
    
if __name__ == '__main__':
  main()