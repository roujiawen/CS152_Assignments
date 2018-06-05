from itertools import product
from copy import deepcopy
import numpy as np
from Queue import LifoQueue

####################Parameters######################

DEPTH_LIMIT = 3 # Initial depth limit
MAX_STEP = 4000 # Maximum step
BOARD_SIZE = 5

####################Constants######################

ADD_NB = [(0, 1), (0, -1), (1, 0), (-1, 0)]
ADD_CO = [(1, 1), (1, -1), (-1, 1), (-1, -1)]
INF = float("inf")
INVALID_VALUES = set([INF, -INF, None])

def is_within(x, minval, maxval):
    if (minval<=x) and (x<=maxval):
        return True
    return False

def get_corners(loc):
    x, y = loc
    return [(x+add_x, y+add_y) for add_x, add_y in ADD_CO
          if is_within(x+add_x, 0, BOARD_SIZE-1) and
             is_within(y+add_y, 0, BOARD_SIZE-1)
    ]

def get_neighbors(loc):
    x, y = loc
    return [(x+add_x, y+add_y) for add_x, add_y in ADD_NB
          if is_within(x+add_x, 0, BOARD_SIZE-1) and
             is_within(y+add_y, 0, BOARD_SIZE-1)
    ]

def hashboard(state):
    code = {"empty":"0", "black": "1", "white": "2"}
    boardhash = "".join(code[state.at(loc).color] for loc in
                        product(xrange(state.size), repeat=2))
    boardhash = int(boardhash, 3) #ternary to base 10
    return boardhash

def oppo_side(color):
    if color == "white":
        return "black"
    return "white"

class Stone(object):
    def __init__(self, color, loc, chain=None):
        self.color = color
        self.loc = loc
        if chain is None:
            self.chain = Chain(color, self)
        else:
            self.chain = chain

class Empty(object):
    def __init__(self, loc):
        self.loc = loc
        self.color = "empty"

class Chain(object):
    """
    liberty_set : a list of tuples(loc).
    """
    def __init__(self, color, init_stone=None):
        self.color = color
        if init_stone is None:
            pass
        else:
            self.stones = [init_stone]
            self.liberty_set = set(get_neighbors(init_stone.loc))

    @property
    def liberty(self):
        return len(self.liberty_set)

class Board(object):
    def __init__(self):
        self.size = BOARD_SIZE
        self.chains = []
        self.board = [[Empty((i, j)) for j in xrange(BOARD_SIZE)] for i in xrange(BOARD_SIZE)]
        self.stable_areas = {"black":[[0 for j in xrange(BOARD_SIZE)] for i in xrange(BOARD_SIZE)],
            "white":[[0 for j in xrange(BOARD_SIZE)] for i in xrange(BOARD_SIZE)]}
        self.history = set()
        self.last_move = None

    def __repr__(self):
        s = ""
        for i in xrange(self.size):
            for j in xrange(self.size):
                if self.board[i][j].color == "empty":
                    s += "  "
                elif self.board[i][j].color == "black":
                    s += "x "
                else:
                    s += "o "
            s += "\n"
        return s

    def at(self, loc):
        return self.board[loc[0]][loc[1]]

    def board_put(self, loc, obj):
        self.board[loc[0]][loc[1]] = obj

    def remove(self, chain):
        for stone in chain.stones:
            loc = stone.loc
            self.board_put(loc, Empty(loc))
            # Update neighbors' liberties
            neighbors = get_neighbors(loc)
            for each_loc in neighbors:
                if self.at(each_loc).color != "empty":
                    self.at(each_loc).chain.liberty_set.add(loc)
        self.chains.remove(chain)

    def is_eye(self, loc):
        """
        Determine whether loc is an eye.
        If so, return (True, color of the eye owner, locations include surrounding stones)
        If not, return (False, None, None)

        """
        def one(color):
            nb = get_neighbors(loc)
            cr = get_corners(loc)
            both = nb+cr
            #corner or edge
            if len(nb)<4:
                if all(self.at(each).color == color for each in both):
                    return True, both+[loc]
            else:#middle
                match = [each for each in both if self.at(each).color == color]
                if (len(match)>=7) and all(self.at(each).color == color for each in nb):
                    return True, match+[loc]
            return False, None

        nb = get_neighbors(loc)
        color_count = {"black": 0, "white":0}
        for each in nb:
            nb_obj = self.at(each)
            if nb_obj.color != "empty":
                color_count[nb_obj.color] += 1
        if (color_count["black"] > 1) and (color_count["white"] > 1):
            return False, None, None
        if color_count["black"] > 1:
            yes_no, locs = one("black")
            if yes_no:
                return True, "black", locs
        elif color_count["white"] > 1:
            yes_no, locs = one("white")
            if yes_no:
                return True, "white", locs
        return False, None, None

    def find_stable_areas(self):
        """
        Find stable areas in a board.
        First generate eye_map for both colors.
        eye_map : 2D list
            0 if not an eye. Otherwise a number which is the index of the eye.
        If more than two eyes overlap or are adjacent, all are marked stable areas.
        """
        def count_unique(arr):
            return len(set([each for sublist in arr for each in sublist]))
        self.stable_areas = {"black":[[0 for j in xrange(BOARD_SIZE)] for i in xrange(BOARD_SIZE)],
            "white":[[0 for j in xrange(BOARD_SIZE)] for i in xrange(BOARD_SIZE)]}
        eye_map = {"black":[[0 for j in xrange(BOARD_SIZE)] for i in xrange(BOARD_SIZE)],
            "white":[[0 for j in xrange(BOARD_SIZE)] for i in xrange(BOARD_SIZE)]}

        stable_index = {"black": set(), "white":set()}
        for loc in product(xrange(self.size), repeat=2):
            if (self.at(loc).color == "empty"):
                yes_no, color, locs = self.is_eye(loc)
                if yes_no:
                    eyes = eye_map[color]
                    index = count_unique(eyes)
                    for each in locs:
                        eye_map[color][each[0]][each[1]] = index
                    connected = set([eyes[nb[0]][nb[1]] for each in locs for nb in get_neighbors(each)
                        if (eyes[nb[0]][nb[1]] != 0) and (eyes[nb[0]][nb[1]] != index)])
                    if len(connected)>0:
                        for each in connected:
                            stable_index[color].add(each)
                        stable_index[color].add(index)
        for loc in product(xrange(self.size), repeat=2):
            for color in ["black", "white"]:
                if (eye_map[color][loc[0]][loc[1]] in stable_index[color]):
                    self.stable_areas[color][loc[0]][loc[1]] = 1

    def put(self, color, loc):
        """
        Error code:
            -1: Success, enemy killed
            0: Success
            1: Occupied
            2: Suicide
        """
        if self.at(loc).color != "empty":
            return 1

        history = hashboard(self)
        new_stone = Stone(color, loc)
        new_chain = new_stone.chain
        self.board_put(loc, new_stone)
        neighbors = get_neighbors(loc)
        friends = []
        enemy_chains = []
        discarding = set()
        discarding.add(loc)
        for each_loc in neighbors:
            obj = self.at(each_loc)
            if obj.color != "empty":
                discarding.add(each_loc)
                if obj.color == color:
                    friends.append(obj)
                else:
                    if obj.chain not in enemy_chains:
                        enemy_chains.append(obj.chain)

        reversible = []
        chains_tbremoved = set()
        # Update current chain
        for friend in friends:
            old_chain = friend.chain
            chains_tbremoved.add(old_chain)
            if old_chain is not new_chain:
                new_chain.stones += old_chain.stones
                new_chain.liberty_set |= old_chain.liberty_set
                # Point friends towards current chain
                for each in old_chain.stones:
                    reversible.append((each, each.chain))
                    each.chain = new_chain

        new_stone.chain.liberty_set -= discarding

        # Check death
        killed_enemy = False
        for chain in enemy_chains:
            chain.liberty_set.discard(loc)
            if chain.liberty == 0:
                killed_enemy = True
                self.remove(chain)

        # Check suicide
        if (not killed_enemy) and (new_chain.liberty == 0):
            #reverse
            self.board_put(loc, Empty(loc))
            for chain in enemy_chains:
                chain.liberty_set.add(loc)
            for each, old_chain in reversible:
                each.chain = old_chain
            return 2

        # Finally the addition is certain
        self.chains = [x for x in self.chains if x not in chains_tbremoved]
        self.chains.append(new_chain)
        # Update history
        self.history.add(history)
        self.last_move = loc
        # Next turn should be opposite color
        #self.turn = oppo_side(color)
        self.find_stable_areas()
        return -1 if killed_enemy else 0

    def clone(self):
        clone_board = Board()
        for c in self.chains:
            # Initialize new chain
            clone_chain = Chain(c.color)
            # Initialize new stones
            clone_stones = [Stone(s.color, s.loc, clone_chain) for s in c.stones]
            # Set Chain attributes (stones and liberty_set)
            clone_chain.stones = clone_stones
            clone_chain.liberty_set = c.liberty_set.copy()
            # Set Board attributes (chains and board)
            clone_board.chains.append(clone_chain)
            for s in clone_stones:
                clone_board.board[s.loc[0]][s.loc[1]] = s
        return clone_board

    def deepclone(self):
        clone_board = self.clone()
        clone_board.history = deepcopy(self.history)
        clone_board.last_move = self.last_move
        return clone_board

    def is_legal(self, color, loc, extra_info=False):
        """
        Cases
        (1) not occupied
        (2) not suicidal
        (3) not a previous state
        """
        def is_equal(board1, board2):
            for row1, row2 in zip(board1, board2):
                for cell1, cell2 in zip(row1, row2):
                    if cell1 != cell2:
                        return False
            return True

        fork = self.clone()
        err_code = fork.put(color, loc)
        # Case 1 or 2
        if err_code > 0:
            return False

        # Case 3
        if hashboard(fork) in self.history:
            return False
        if extra_info:
            return True, err_code
        return True

    def is_nonstupid(self, color, loc):
        """
        Check if a move is legal by cloning a board and try putting
        a stone. If no error occurs, the move is legal.
        (1) Illegal
        (2) Filling its `eye`
        """
        def is_liberty(board, color, loc):
            for chain in board.chains:
                if (chain.color==color) and (loc in chain.liberty_set):
                    return True
            return False

        is_legal_return = self.is_legal(color, loc, extra_info=True)
        if is_legal_return is False: return False
        _, err_code = is_legal_return

        # If not illegal, check if its an eye for any chain
        for chain in self.chains:
            if (chain.color==color):
                if loc in chain.liberty_set:
                    # Check if it's legal for opponent
                    if not self.is_legal(oppo_side(color), loc):
                        # If loc is a liberty and illegal for opponent --> stupid
                        # Unless it can kill enemy, which means --> not stupid
                        if err_code != -1:
                            return False
        return True

    def count_stable_spots(self, color):
        return len([each for sublist in self.stable_areas[color] for each in sublist if each==1])

    def has_no_chance(self):
        """
        Detect whether one player has no chance of winning given current board.
        Requirement of stable area is at least 8 available spots.
        If no chance, returns score.
        Otherwise, returns 0.
        """
        if self.count_stable_spots("black")> BOARD_SIZE*BOARD_SIZE-8:
            return BOARD_SIZE*BOARD_SIZE
        if self.count_stable_spots("white")> BOARD_SIZE*BOARD_SIZE-8:
            return -BOARD_SIZE*BOARD_SIZE
        return 0

    def is_terminal(self):
        """
        Whether the board is a terminal state. If so, also returns score.
        """
        temp = self.has_no_chance()
        if temp != 0:
            return True, temp

        for loc in product(xrange(self.size), repeat=2):
            if self.at(loc).color == "empty":
                if (self.is_nonstupid("black", loc) or
                        self.is_nonstupid("white", loc)):
                    return False, None
        return True, self.score()

    def score(self):
        black_score = 0
        white_score = 0
        for loc in product(xrange(self.size), repeat=2):
            obj = self.at(loc)
            if obj.color == "empty":
                nb = get_neighbors(loc)
                color_count = {"black": 0, "white":0}
                for each in nb:
                    nb_obj = self.at(each)
                    if nb_obj.color != "empty":
                        color_count[nb_obj.color] += 1
                if (color_count["black"]>0) and (color_count["white"]>0):
                    black_score += 0.5
                    white_score += 0.5
                elif color_count["black"]>0:
                    black_score += 1
                elif color_count["white"]>0:
                    white_score += 1
            elif obj.color == "black":
                black_score += 1
            elif obj.color == "white":
                white_score += 1

        return black_score-white_score

def hashstate(state, color, code={"empty":"0", "black": "1", "white": "2"}):
    boardhash = "".join(code[state.at(loc).color] for loc in
                        product(xrange(state.size), repeat=2))
    boardhash = int(boardhash, 3) #ternary to base 10
    return (boardhash, int(code[color]), state.last_move)

def actions(state, color):
    choices = []
    for loc in product(xrange(state.size), repeat=2):
        if state.at(loc).color == "empty":
            if state.is_nonstupid(color, loc):
                fork = state.clone()
                fork.put(color, loc)
                choices.append((color, loc))
    return choices

def result(state, action):
    next_state = state.deepclone()
    next_state.put(*action)
    return next_state

def adversarial_search(state, color, alpha, beta, v):#max_value, color:black; min_value white
    global EXCEED
    # Using a stack for iterative DFS, preventing maximum recursion error
    stack = LifoQueue()
    base_level = (state, color, alpha, beta, v)
    stack.put(base_level)
    while not stack.empty():
        state, color, alpha, beta, v = stack.get()
        key = hashstate(state, color)
        if key in EXPLORED:
            pass#################EXPLORED
        else:
            global STEP
            STEP += 1
            terminal, score = state.is_terminal()
            if terminal:
                EXPLORED[key] = score
                #################TERMINAL
            elif len(state.history)>DEPTH_LIMIT:
                EXCEED = True
                EXPLORED[key] = v
            else:
                if color == "black":
                    if not hasattr(state, "action_list"):
                        state.action_list = actions(state, "black")
                    if len(state.action_list) > 0:
                        action = state.action_list[-1]
                        next_state = result(state, action)
                        next_key = hashstate(next_state, "white")
                        if next_key in EXPLORED:
                            state.action_list.pop(-1)
                            if EXPLORED[next_key] not in INVALID_VALUES:
                                v = max(v, EXPLORED[next_key])
                            if v >= beta:
                                EXPLORED[key] = v
                                ################## alpha-beta pruning
                            else:
                                alpha = max(alpha, v)
                                stack.put((state, color, alpha, beta, v))
                        else:
                            stack.put((state, color, alpha, beta, v))
                            stack.put((next_state, "white", alpha, beta, INF))
                    else:
                        EXPLORED[key] = v
                        ################## search result
                else:
                    if not hasattr(state, "action_list"):
                        state.action_list = actions(state, "white")
                    if len(state.action_list) > 0:
                        action = state.action_list[-1]
                        next_state = result(state, action)
                        next_key = hashstate(next_state, "black")
                        if next_key in EXPLORED:
                            state.action_list.pop(-1)
                            if EXPLORED[next_key] not in INVALID_VALUES:
                                v = min(v, EXPLORED[next_key])
                            if v <= alpha:
                                EXPLORED[key] = v
                                ################## alpha-beta pruning
                            else:
                                beta = min(beta, v)
                                stack.put((state, color, alpha, beta, v))
                        else:
                            stack.put((state, color, alpha, beta, v))
                            stack.put((next_state, "black", alpha, beta, -INF))
                    else:
                        EXPLORED[key] = v
    state, color, _, __, ___ = base_level
    return EXPLORED[hashstate(state, color)]

def trace_solution(state, action):
    if action is None: return []
    moves = []
    for i in range(DEPTH_LIMIT):
        moves.append(action)
        state = result(state, action)
        if action[0] == "white":
            action, _ = minimax(state)
        elif action[0] == "black":
            action, _ = maximin(state)
        if action is None:
            return moves
    return moves

def minimax(state):
    terminal, score = state.is_terminal()
    if terminal: return None, score
    best_move = None
    best_util = -INF
    for action in actions(state, "black"):
        v = adversarial_search(result(state, action), "white", -INF, INF, INF)
        if (v not in INVALID_VALUES) and (v > best_util):
            best_util = v
            best_move = action
    return best_move, best_util

def maximin(state):
    terminal, score = state.is_terminal()
    if terminal: return None, score
    best_move = None
    best_util = INF
    for action in actions(state, "white"):
        v = adversarial_search(result(state, action), "black", -INF, INF, -INF)
        if (v not in INVALID_VALUES) and (v < best_util):
            best_util = v
            best_move = action
    return best_move, best_util

def iter_deep(state, func):
    global EXPLORED
    global EXCEED
    global DEPTH_LIMIT
    global STEP
    EXPLORED = {}
    x = []
    y = []
    state.history = set()
    while True:
        EXCEED = False
        STEP = 0
        EXPLORED = {}
        move, best_util = func(state)
        print "DEPTH =", DEPTH_LIMIT, "SEARCH STEP =", STEP
        if (not EXCEED) or (STEP>MAX_STEP):
            moves = trace_solution(state, move)
            print "SOLUTION =", move, "UTILITY =", best_util
            return moves
        DEPTH_LIMIT += 1

def iter_deep_maximin(state):
    return iter_deep(state, maximin)

def iter_deep_minimax(state):
    return iter_deep(state, minimax)
