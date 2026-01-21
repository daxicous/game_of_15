import math
from game_state import GameState


class Solver:
    """Solves 15-puzzle using A* algorithm"""
    
    SIZE = 4
    
    
    def heuristic(state):
        """
        Manhattan distance heuristic.
        Sum of distances each tile needs to move to reach goal.
        """
        answer = 0
        for y in range(state.size):
            for x in range(state.size):
                val = state.grid[y][x]
                if val != 0:  # Skip empty space
                    answer += Solver.find_dist(x, y, val, state.size)
        return answer
    
    @staticmethod
    def find_dist(x, y, val, size):
        """Calculate Manhattan distance from current position to goal position"""
        # Goal position of value
        goal_x = (val - 1) % size
        goal_y = (val - 1) // size
        return abs(goal_x - x) + abs(goal_y - y)
    
    @staticmethod
    def solve(initial_state, max_iterations=None):
        """
        Solve puzzle using A* algorithm.
        Returns list of moves to reach solved state, or None if unsolvable.
        """
        if initial_state.is_solved():
            return []
        
        from heapq import heappush, heappop
        
        # Priority queue: (f_score, counter, state, path)
        counter = 0
        open_set = [(Solver.heuristic(initial_state), counter, initial_state, [])]
        closed_set = {initial_state}
        
        iterations = 0
        
        while open_set:
            if max_iterations and iterations >= max_iterations:
                return None
            
            _, _, current_state, path = heappop(open_set)
            iterations += 1
            
            if current_state.is_solved():
                return path
            
            # Try all possible moves
            for dx, dy in current_state.get_possible_moves():
                next_state = current_state.move(dx, dy)
                
                if next_state and next_state not in closed_set:
                    closed_set.add(next_state)
                    new_path = path + [(dx, dy)]
                    g_score = len(new_path)
                    h_score = Solver.heuristic(next_state)
                    f_score = g_score + h_score
                    
                    counter += 1
                    heappush(open_set, (f_score, counter, next_state, new_path))
        
        return None  # No solution found