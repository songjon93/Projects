## Chess AI

### Introduction

The following program emulates a chess AI that attempts at making the highest-utility returning move computing a heuristic for each legal move via minimax search. Minimax search is based on a zero-sum game theory, according to which a gain for a player would mean an equally weighted loss for its enemy and vice versa.

### Codes Revisited
#### Minimax and Cutoff Test

The main objective of the AI is to find a legal move with the highest potential utility return. In order to do so, I have decided to implement a minimax search.

As discussed above, a minimax search operates under the assumption that the agent's best interest lies in maximizing the utility while the enemy's lies in minimizing it because a gain for the agent would mean a loss for its enemy and vice versa. That is, in minimax search, the agent will iterate through all its legal moves, explore possible actions the enemy can take in response to that, assume the worst, and choose the least worst case from the set of worst cases provided by the enemy.

```
def minimax_decision(self, board):
    moves = list(board.legal_moves)
    max_util = float("-inf")
    max_move = None

    for move in moves:
        board.push(move)

        util = self.transposition(board, 1)

        board.pop()

        if util > max_util:
            max_move = move
            max_util = util

    return max_move

def max_value(self, board, depth):
    self.max_called += 1

    if self.is_terminal(board) or self.is_at_max_depth(depth):
        self.max_util = self.compute_utility(board)
        return self.max_util

    moves = list(board.legal_moves)
    max_util = float("-inf")

    if str(board) in self.visited_state_my.keys():
        return self.visited_state_my[str(board)]

    for move in moves:
        board.push(move)

        util = self.transposition(board, depth + 1)

        board.pop()

        if util > max_util:
            max_util = util

    self.max_util = max_util
    return max_util

def min_value(self, board, depth):
    self.min_called += 1

    if self.is_terminal(board) or self.is_at_max_depth(depth):
        self.max_util = self.compute_utility(board)
        return self.max_util

    moves = list(board.legal_moves)
    min_util = float("inf")

    for move in moves:
        board.push(move)

        util = self.transposition(board, depth + 1)

        board.pop()
        if util < min_util:
            min_util = util

    return min_util
```

As demonstrated above, for every legal move the agent can make, the agent runs a simulation of what utility it will end up with if it carries out that move. Within the simulation, the agent and the enemy takes turn, trying to maximize and minimize utility respectively (Note that utility is not computed within these turns, it will be computed once the search reaches its end state). Once depth-first-search reaches its maximum depth or the game comes to a terminal state, the program computes the utility using `compute_utlity` function (how the program computes utility will be further discussed in the description below). And using the computed utility value, the agent makes an informed decision by taking actions that is expected to give the agent the highest utility possible.

Then, how many nodes does the search have to visit in order to find its optimal move?  

#### at max_depth = 2
```
max called 1370 times / min called 39 times / max depth reached 1370 times / transposition table used : 0 times.

r . . q k b . .
. b p . . p . .
p p . . p n p r
P P P p P . . p
. n . P . P P P
. . . . . . . .
. . . . . . . .
R N B Q K B N R
----------------
a b c d e f g h
```

#### at max_depth = 3
```
max called 1049 times / min called 24515 times / max depth reached 24478 times / transposition table used : 0 times.

r . b q k b n r
p p . n . . . p
. . . p p . . .
. P . . . p p Q
P . P p P P . .
. . . . . . . .
. . . . . . P P
R N B . K B N R
----------------
a b c d e f g h
```
#### at max_depth = 4
```
max called 282879 times / min called 10299 times / max depth reached 281878 times / transposition table used : 0 times.

r . b q k b . r
p p p p n p p p
. . . . . . . .
. . . . p . . .
. n . . P . . .
P P P P . P . .
. . . B . K P P
R N . Q . B N R
----------------
a b c d e f g h
```

As can be seen in the examples above, the number of nodes that have to be visited increases exponentially. At depth 2, `max_call()` and `min_call()` are called 1409 times, and the search recurses down to the maximum depth 1370 times. In contrast, at depth 3, `max_call()` and `min_call()` are called 25564 times while the search recurses down to the maximum depth 24478 times. At depth 4, `max_call()` and `min_call()` are called 293178 times with 281878 recursions to the maximum depth. Notice how the number of calls increase at an exponential rate as the search depth increases.

#### Evaluation Function
```
PIECE_SCORE = [0, 1, 3, 3, 5, 9, 1000]

def compute_utility(self, board):

    my_util = 0
    en_util = 0

    for piece_type in range(1, 7):
        my_util += self.PIECE_SCORE[piece_type] * len(board.pieces(piece_type, self.TURN))
        en_util += self.PIECE_SCORE[piece_type] * len(board.pieces(piece_type, not self.TURN))

    return my_util - en_util
```
As demonstrated above, each piece type has a weighted utility; pawns have a weight of 1, bishops have a weight of 3, knights have a weight of 3, rooks have a weight of 5, queen[s] has[have] a weight of 9, and a king has a weight of 1000. And the total utility of each player is computed by counting the number of each piece type {pawn, bishop, knight, rook, queen, king} and multiplying them by their weights. Once we have the agent's and the enemy's total utility, we subtract the enemy's utility from the agent's to come up with a relative measure of who's winning and by how much.

There are mainly two reasons to why I calculate material utility for both the agent and the enemy: 1) to advocate the agent to take down the enemy's pieces instead of only focusing on preserving its pieces and 2) to prevent the agent from only focusing on taking down the enemy's pieces, possibly losing its highly-weighted pieces in return to killing the enemy's rather lowly-weighted pieces.

Let's assume that we only compute the material utility of the agent. The agent will not have any incentive to move onto the other side and take down the enemy's pieces. Second, let's assume that we only compute the number of the enemy's pieces taken down. The agent may make a intuitively wrong and dangerous move, taking down the enemy's pawn and lose its queen in return. That's why in my evaluation function, I consider both gain and loss to aid the agent to make a more intuitively and relatively right decision.

```
Demonstration of the agent's intelligent move:
. . . . . . . .
. . . . . . . .
. . . . . . . .
. . . . r . p .
. . . . Q b . .
. . . . . . . .
. . . . . . . .
. . . . . . . .
----------------
a b c d e f g h

White to move

. . . . . . . .
. . . . . . . .
. . . . . . . .
. . . . r . p .
. . . Q . b . .
. . . . . . . .
. . . . . . . .
. . . . . . . .
----------------
a b c d e f g h

Black to move

Please enter your move:
f4e3
f4e3
True
. . . . . . . .
. . . . . . . .
. . . . . . . .
. . . . r . p .
. . . Q . . . .
. . . . b . . .
. . . . . . . .
. . . . . . . .
----------------
a b c d e f g h

White to move

. . . . . . . .
. . . . . . . .
. . . . . . . .
. . . . Q . p .
. . . . . . . .
. . . . b . . .
. . . . . . . .
. . . . . . . .
----------------
a b c d e f g h

At the initial state, the queen could have aimed for either a rook, or a bishop. It would have earned 5 or 3 utilities if it went for such nearsighted gain. However, as we can tell, taking down either of the two pieces would mean a loss of queen: if the queen were to take down a rook, it would be taken down by the enemy's bishop, and if the queen were to take down the enemy's bishop, it would be taken down by the enemy's pawn. Therefore, the queen here decides to take a step aside until it can make points safely. And thus, when a rook is available without any hazard ahead, the queen sweeps the rook safely.
```
#### Iterative Deepening

We can perfect our AI by deepening the search, but it would take exponentially longer per extra floor it has to explore. And given that the agent has to make its move under a time constraint in most chess matches, using iterative deepening will let the agent make an optimal move at any moment of interruption.

```
def choose_move(self, board):
    best_move = None
    max_util = float("-inf")

    for i in range(1, self.depth + 1):
        temp_ai = MinimaxAI(i)
        temp_move = temp_ai.choose_move(board)
        if temp_ai.max_util > max_util and temp_move != best_move:
            print("best move altered at depth " + str(i) + ":" + str(best_move) + " --> " + str(temp_move))
            best_move = temp_move

    return best_move
```

I have implemented iterative deepening by simply looping from 1 to `max_depth`, initializing a MinimaxAI object with the given depth value `i`, and updating the best_move at each iteration.

Below is a demonstration of how the optimal decision for the agent changes as its search depth is incremented:
```
. r b q k b . r
p . . . p p . p
n . . . . . . n
P p p p . . . .
Q P P P P p P P
. . . . . . . .
. . . . . . . .
R N B . K B N R
----------------
a b c d e f g h

White to move

best move altered at depth 1:None --> e4e5
best move altered at depth 2:e4e5 --> a5b6
. r b q k b . r
p . . . p p . p
n P . . . . . n
. . p p . . . .
Q P P P P p P P
. . . . . . . .
. . . . . . . .
R N B . K B N R
----------------
a b c d e f g h
```
As demonstrated above, the agent finds a better move when it searches down a deeper level. At depth 1, it has no clue of what consequence its action might bring about, and it naively decides to maximize its utility by taking down the enemy's pawn at `d5` with its pawn at `e4`, but at depth 2, the agent realizes that if it doesn't get rid of the pawn at `b4`, it will lose its queen; so it decides to eliminate the enemy's pawn at `b4` using en passant. And the agent doesn't change its decision even with further searches at deeper depth because it doesn't find any alternative move that can bring about more utility than the move it's found at depth 2. Let's for instance, assume that we used our queen at `a4` to get rid of the enemy's pawn at `b5`. Then, the queen would be vulnerable to attack from the enemy's rook at `b8` (meaning the agent would be at risk of losing a large amount of utility). However, if we instead have our pawn at `a5` to en passant the enemy's pawn, the enemy's king will be vulnerable to our queen's attack, which, in other words, is a "no utility loss for us".


#### Alpha-Beta Pruning

In order to decrease the number of calls to the successor nodes (`min_value()` and `max_value()`) within the minimax search, we can skip those that are proven to be worse than our least worst case via alpha-beta pruning. Alpha beta pruning works by keeping track of the minimum and the maximum value in order to stop unnecessary recursion down the tree if it finds out that it finds out that the most utility it can get out of that move is going to be smaller than what the agent is guaranteed to have.

```
def alpha_beta_decision(self, board):
    moves = list(board.legal_moves)
    moves = self.reorder(board, moves)
    max_util = float("-inf")
    max_move = None

    for move in moves:
        board.push(move)

        util = self.transposition(board, 1, float("-infinity"), float("infinity"))

        board.pop()

        if util > max_util:
            max_move = move
            max_util = util

    return max_move

def max_value(self, board, depth, alpha, beta):
    self.max_called += 1
    a = alpha
    b = beta
    if self.is_terminal(board) or self.is_at_max_depth(depth):
        return self.compute_utility(board)
    moves = list(board.legal_moves)
    moves = self.reorder(board, moves)
    max_util = float("-inf")

    for move in moves:
        board.push(move)

        util = self.transposition(board, depth + 1, a, b)

        board.pop()

        max_util = max(util, max_util)
        a = max(max_util, a)
        if a >= b:
            break

    return max_util

def min_value(self, board, depth, alpha, beta):
    self.min_called += 1
    a = alpha
    b = beta
    if self.is_terminal(board) or self.is_at_max_depth(depth):
        return self.compute_utility(board)
    moves = list(board.legal_moves)
    moves = self.reorder(board, moves)
    min_util = float("inf")

    for move in moves:
        board.push(move)

        util = self.transposition(board, depth + 1, a, b)

        board.pop()

        min_util = min(util, min_util)
        b = min(min_util, b)
        if b <= a:
            break

    return min_util
```
Alpha-Beta Pruning is intended to decrease the number of nodes explored and now let's see if it actually does. Let's take a look at how many calls alpha_beta search makes to `min_value()` and `max_value` at depth = 4 and how many times it recurses all the way down to that depth:

```
max called 108996 times / min called 7801 times / max depth reached 108231 times / transposition table used : 0 times.

r . b q k b . r
p p p p n p p p
. . . . . . . .
. . . . p . . .
. n . . P . . .
P P P P . P . .
. . . B . K P P
R N . Q . B N R
----------------
a b c d e f g h
```
The result is in sharp contrast with the result of regular minimax search at depth 4. Unlike minimax search that made 293178 calls to `min_value()` and `max_value()` and 281878 recursions to the max depth, the alpha_beta search makes 116796 calls to `min_value()` and `max_value()` and 108231 recursion to the max depth. That's nearly 1:3 in ratio.

#### Reordering
However, there are going to be cases, where the search program can't prune edges properly. In order to make the fullest use of our alpha_beta search, it will be in our best interest to reorder the list of legal moves so that we explore those moves that are likely to return us a higher utility first. Below is my reordering function:

```
    class State():
        def __init__(self, move, util):
            self.move = move
            self.util = util



        def __lt__(self, other):
            return self.util > other.util

def reorder(self, board, moves):
    if self.is_reorder:
        return moves

    queue = []
    for move in moves:
        util = 0
        catch = 4
        threat = 3
        forward = 2
        retreat = 1

        if str(move)[1] < str(move)[3]:
            util += forward if board.turn == self.TURN else retreat
        elif str(move)[3] < str(move)[1]:
            util += retreat if board.turn == self.TURN else forward
        if board.is_capture(move):
            util += catch if board.turn == self.TURN else -catch

        state = self.State(move, util)
        heappush(queue, state)

    n_moves = []

    while len(queue) > 0:
        n_moves.append(heappop(queue).move)

    return n_moves
```
So my reordering function evaluates each move within the legal moves list according to whether it captures enemy's pieces, whether it moves forward, and whether it makes a retreat. If the move capture one of enemy's pieces, its score is incremented by 4. If the move involves a forward movement, the score is incremented by 2. And if the move involves a retreat, the score is incremented by 1. And using the store as the comparison value, I sort the list using a queue and heappushing all the weighted moves into the queue. And once we've evaluated every move from the legal move list, we start heappopping from the queue until the queue is empty, appending heappopped move onto the new_move list at each iteration.

P.S. I've implemented threat cases and weighted them with a value of 3, but detecting threat cases severly slowed down the reordering process, so I decided to go without it.

Now let's see if reordering did improve our run time!
```
max called 85496 times / min called 6415 times / max depth reached 84746 times / transposition table used : 0 times.

r n . . k b n r
p . . . p p . .
. p p p . . p p
. . . . . . . .
Q . . . . . . .
N . . . P . . .
P P P P . P P P
. R B . . K N R
----------------
a b c d e f g h
```
The alpha_beta search with reordering makes 91991 calls to `min_value()` and `max_value()` and 84746 recursion to the max depth while regular alpha_beta search made 116796 calls and 108231 recursions respectively. That's approximately a 20% improvement! And, therefore, it can be stated that the reordering function made a pretty accurate evaluation of each move.

My program is capable of turning on and turning off the reordering feature; so you can try running alpha_beta search both with reordering turned on and off to see how much improvement is made to the actual run time by implementing reordering.


#### Transposition Table
Transposition Table uses the board state as a key to store the heuristic of already explored states. Doing so will prevent the agent from analyzing the already explored states. This is intrinsically identical to memoizations for search trees; remember how we prevented our search algorithm from visiting the same node over and over again by keeping a visited_set? The only difference is that while in the visited_set, we only kept track of whether the node has been visited or not, in the transposition table for chess games, we keep track of the heuristic of each board state.

```
def transposition(self, board, depth, alpha, beta):
    hsh = str(board)
    util = 0

    if board.turn != self.TURN:
        if self.is_active and hsh in self.visited_state_my.keys():
            self.trans_used += 1
            return self.visited_state_my[hsh]
        else:
            util = self.min_value(board, depth, alpha, beta)
            self.visited_state_my[hsh] = util
    else:
        if self.is_active and hsh in self.visited_state_en.keys():
            self.trans_used += 1
            return self.visited_state_en[hsh]
        else:
            util = self.max_value(board, depth, alpha, beta)
            self.visited_state_en[hsh] = util

    return util
```
As our transposition table, I decided to use a dictionary data structure. And I store the expected utility of a move onto the dictionary using the string representation of the board state as the key. And because the board states are different for when it's the enemy's turn and when it's the agent's turn, I decided to keep two transposition tables: one for the agent and one for the enemy. So, within this `transposition()` function, I check whether the current board state has been explored previously. If it has, the function will simply return the stored heuristic value for that board state, and if it hasn't, the function will make calls to either `max_value` or `min_value` depending on whose turn it is, retrieve the expected utility of that board state, and append to the dictionary the retrieved value so that the next time the agent finds itself in that board state, it returns the stored value instead of going through the recursion all over again.

Using a transposition table is expected to prevent our search function from visiting already visited board states, and theoretically should decrease the number of calls to `min_value()` and `max_value()` quite significantly. Now let's see if it does:
```
max called 21784 times / min called 2492 times / max depth reached 21024 times / transposition table used : 8711 times.

r . b q k b B .
p p . p . . p p
. . . . . . . .
. . p . p p . .
. P . . . . . .
. . . . P . P P
P P N P . . P .
R . B Q K . N R
----------------
a b c d e f g h
```
As presented above, using transposition table helps our search make much less number of calls to `max_value()` and `min_value()` and the number of `transposition_used` signify the number of times where our search function retrieved a stored heuristic value of the board state instead of making searches all the way to the max depth. In contrast to our alpha_beta search with reordered move_list, in which there were 919991 visits to the children nodes within the tree and 84747 visits to the very bottom of the tree, the alpha_beta search with transposition table implemented makes only 24276 calls to children nodes and 21024 visits to the very bottom.

However, there is a downside to our implementation of transposition table. It definitely accelerates our search, but it may return a rather inaccurate heuristic value of a board state. For instance, if the board state was reached at depth 3 while the max_depth was 4, the heuristic that will be stored in the transposition table is going to be a very short sighted one because it will only foresee one move instead of foreseeing 4 moves if there were transposition table implemented in the first place.

Even though the heuristic may be inaccurate time to time, using transposition table allows to perform the search much faster, and allow us to search down to a deeper level.


## Extra Credit
### Zobrist Hash function:
I have implemented Zobrist Hash Function. In order to do so, I first had to initialize a Zobrist table in the very beginning. The Zobrist table a 64 x 12 2d array of random integers. It can also be a 8 x 8 x 12 3d array, but I liked keeping it 2d instead of 3d. And I would compute the hash value for a board state by "xor"ing the integer values retrieved from certain indices of the zobrist table. Using this hash value, I would store onto the array(the transposition table) the computed heuristic for the board state at the index equivalent to the hash value.

```
self.zobrist_table = [[0 for i in range(12)] for j in range(64)]
for square in range(64):
   for piece in range(12):
       self.zobrist_table[square][piece] = randint(0, self.LIST_SIZE/2)

def find_hash(self, board):
   hash_val = 0
   for square in range(0, 64):
       if board.piece_at(square) is not None:
           piece = board.piece_at(square)
           piece_val = piece.piece_type - 1 if piece.color == chess.WHITE else piece.piece_type * 2 - 1
           hash_val ^= self.zobrist_table[square][piece_val]
   return hash_val
```
The Zobrist Hash can be found at AlphaBetaAI_EC of the Extra Credit Folder.

### Opening Book:

I have implemented two types of opening move known as "Ruy Lopez" and "Queen's Gambit". The user can choose between the two and toggle on/off the opening book functionality at the stage of initializing the AlphaBetaAI object. And below is an example of how to initialize the AlphaBetaAI object:  
`AlphaBetaAI(depth, is_active=False, is_silent=True, is_opening_move=True, move_type="Lopez")`

The opening move seems to aid the AlphaBetaAI at reaching the winning stage. With these opening move, AlphaBetaAI does not make meaningless repetitive move, such as moving rooks or knights back and forth. And for me, it made the AI reach the winning stage earlier than when it wasn't provided with the opening book.

```
def opening_move(self, board):
    uci = None
    if self.move_count == 0:
        if self.TURN == chess.WHITE:
            uci = chess.Move.from_uci("e2e4") if self.move_type == "Lopez" else chess.Move.from_uci("d2d4")
        else:
            uci = chess.Move.from_uci("d7d5") if self.move_type == "Lopez" else chess.Move.from_uci("e7e5")
    if self.move_count == 1:
        if self.TURN == chess.WHITE:
            uci = chess.Move.from_uci("g1f3") if self.move_type == "Lopez" else chess.Move.from_uci("c2c4")
        else:
            uci = chess.Move.from_uci("b8c6") if self.move_type == "Lopez" else chess.Move.from_uci("f7f5")
    if self.move_count == 2:
        if self.TURN == chess.WHITE:
            uci = chess.Move.from_uci("f1b5") if self.move_type == "Lopez" else self.alpha_beta_decision(board)
        else:
            uci = chess.Move.from_uci("c8g4") if self.move_type == "Lopez" else self.alpha_beta_decision(board)
    return uci
```
Opening Move can be viewed and demonstrated using the AlphaBetaAI_EC.

### Advanced More reordering:

I have improved my move ordering approach for alpha-beta search by using computed state values from the previous iteration of IDS. It was a pretty simple implementation: I take the transposition table that has the computed heuristic value for all the explored board states, and use that as my weight for moves at reordering process. Because in iterative deepening search, we are guaranteed that the transposition table will have the computed heuristic for every legal move stored in the transposition table, all I had to do was:

```
class AlphaBetaAI():
...
    def reorder(self, board, moves):
        queue = []
        i = 0
        for move in moves:
            hsh = str(move)
            if hsh in self.util_table:
                state = self.State(move, self.util_table[hsh])
            else:
                state = self.State(move, 0)
            heappush(queue, state)
        n_moves = []

        while len(queue) > 0:
            n_moves.append(heappop(queue).move)

        return n_moves


class Iterative():
    def __init__(self, depth):
        self.depth = depth

    def choose_move(self, board):
        best_move = None
        max_util = float("-inf")
        temp_table = {}

        for i in range(1, self.depth + 1):
            temp_ai = AlphaBetaAI(i)
            temp_ai.util_table = temp_table
            temp_move = temp_ai.choose_move(board)
            temp_table = temp_ai.util_table

            if temp_ai.max_util > max_util and temp_move != best_move:
                print("best move altered at depth " + str(i) + ":" + str(best_move) + " --> " + str(temp_move))
                best_move = temp_move

        return best_move
```

As demonstrated above, my iterative choose move function, loops from 1 to max_depth, and pass on the updated transposition table to the newly initialized AlphaBetaAI at each iteration --> `temp_ai = AlphaBetaAI(i)
temp_ai.util_table = temp_table`
