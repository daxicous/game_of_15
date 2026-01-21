"""Example showing how to use GameState and Solver"""

from game_state import GameState
from solver import Solver
import random

# ============ Creating Game States ============

# 1. Create a solved state
solved = GameState(size=4)
print("Solved state:")
print(solved)
print()

# 2. Create a custom state
custom_grid = [
    [1, 2, 3, 4],
    [5, 6, 7, 8],
    [9, 10, 11, 12],
    [13, 14, 0, 15]  # 0 is the empty space
]
custom = GameState(custom_grid, size=4)
print("Custom state:")
print(custom)
print()

# 3. Create a shuffled random state
def shuffle_state(state, num_moves=100):
    """Create a solvable random state by making random moves"""
    current = state.copy()
    for _ in range(num_moves):
        moves = current.get_possible_moves()
        move = random.choice(moves)
        current = current.move(move[0], move[1])
    return current

random_state = shuffle_state(solved, 50)
print("Random shuffled state:")
print(random_state)
print()

# ============ Working with States ============

# Check if solved
print(f"Is solved: {random_state.is_solved()}")
print()

# Get possible moves
print(f"Possible moves: {random_state.get_possible_moves()}")
print()

# Make a move
if random_state.get_possible_moves():
    dx, dy = random_state.get_possible_moves()[0]
    new_state = random_state.move(dx, dy)
    print(f"After moving ({dx}, {dy}):")
    print(new_state)
    print()

# ============ Solving ============

# Create a simple puzzle (just a few moves from solved)
simple = shuffle_state(solved, 5)
print("Solving simple puzzle:")
print(simple)
print()

solution = Solver.solve(simple, max_iterations=10000)
if solution:
    print(f"Solution found! {len(solution)} moves:")
    print(f"Moves: {solution}")
else:
    print("No solution found")
