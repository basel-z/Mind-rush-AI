from board import Board


# equivalent to a node in the graph
class DFSGameState:

    def __init__(self, actual_game: Board, depth: int):
        self.actual_game: Board = actual_game
        self.children = []
        self.is_done = False
        self.depth = depth

    # Take notice, that if we are on a leaf (although should be impossible) then we automatically return True
    def is_state_completely_visited(self):
        for child in self.children:
            if child.is_done == False:
                return False
        return True

    def generate_children(self):
        x = 1


# TODO: Continue
class DepthLimitedSearch:

    def __init__(self, actual_game: Board, depth_limit: int):
        self.depth_level = depth_limit
        self.actual_game = actual_game
        self.visited_nodes = {}
        self.initial_state = DFSGameState(actual_game, 0)
