from collections import namedtuple
import copy

# Immutable representation of a position
Position = namedtuple('Position', ['x', 'y'])

class GameState:
    """Represents a 15-puzzle game state"""
    
    def __init__(self, grid=None, size=4):
        """
        Initialize a game state.
        grid: 2D list where 0 represents the empty space
        size: board size (4 for 15-puzzle)
        """
        self.size = size
        if grid is None:
            # Initialize solved state: [[1,2,3,4], [5,6,7,8], ...]
            self.grid = [[i * size + j + 1 for j in range(size)] for i in range(size)]
            self.grid[size-1][size-1] = 0  # Empty space in bottom-right
        else:
            self.grid = [row[:] for row in grid]  # Deep copy
        
        self._find_empty()
        self._hash = None
    
    def _find_empty(self):
        """Find position of empty space (0)"""
        for y in range(self.size):
            for x in range(self.size):
                if self.grid[y][x] == 0:
                    self.empty_pos = Position(x, y)
                    return
    
    def __hash__(self):
        """Make state hashable for visited set"""
        if self._hash is None:
            self._hash = hash(tuple(tuple(row) for row in self.grid))
        return self._hash
    
    def __eq__(self, other):
        """Check if two states are equal"""
        if not isinstance(other, GameState):
            return False
        return self.grid == other.grid
    
    def __repr__(self):
        """String representation of state"""
        return '\n'.join(str(row) for row in self.grid)
    
    def copy(self):
        """Create a deep copy of this state"""
        return GameState([row[:] for row in self.grid], self.size)
    
    def get_possible_moves(self):
        """
        Get all possible moves (directions the empty space can move).
        Returns list of (dx, dy) tuples.
        """
        x, y = self.empty_pos
        moves = []
        
        # Empty space can move up, down, left, right
        # (moving empty space is same as moving adjacent tile)
        if y > 0:
            moves.append((0, -1))  # Move up
        if y < self.size - 1:
            moves.append((0, 1))   # Move down
        if x > 0:
            moves.append((-1, 0))  # Move left
        if x < self.size - 1:
            moves.append((1, 0))   # Move right
        
        return moves
    
    def move(self, dx, dy):
        """
        Make a move by swapping empty space with adjacent tile.
        Returns new GameState, or None if move is invalid.
        """
        x, y = self.empty_pos
        new_x, new_y = x + dx, y + dy
        
        # Check bounds
        if not (0 <= new_x < self.size and 0 <= new_y < self.size):
            return None
        
        # Create new state
        new_state = self.copy()
        
        # Swap empty space with tile
        new_state.grid[y][x], new_state.grid[new_y][new_x] = \
            new_state.grid[new_y][new_x], new_state.grid[y][x]
        
        new_state._find_empty()
        return new_state
    
    def is_solved(self):
        """Check if puzzle is in solved state"""
        expected = 1
        for y in range(self.size):
            for x in range(self.size):
                if y == self.size - 1 and x == self.size - 1:
                    return self.grid[y][x] == 0
                if self.grid[y][x] != expected:
                    return False
                expected += 1
        return True
    
    def get_flat_list(self):
        """Get flattened list representation (useful for heuristics)"""
        flat = []
        for row in self.grid:
            flat.extend(row)
        return flat
