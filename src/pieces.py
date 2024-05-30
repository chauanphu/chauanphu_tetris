shape_colors = [(0,255,255), (255,255,0), (128,0,128), (0,255,0), (255,0,0), (0,0,255), (255,165,0)]
# Define all shapes formats
S = [
    [".....",
     ".....",
     "..00.",
     ".00..",
     "....."],
    [".....",
     "..0..",
     "..00.",
     "...0.",
     "....."]
]

Z = [
    [".....",
     ".....",
     ".00..",
     "..00.",
     "....."],
    [".....",
     "..0..",
     ".00..",
     ".0...",
     "....."]
]

I = [
    [".....",
     "..0..",
     "..0..",
     "..0..",
     "..0.."],
    [".....",
     "0000.",
     ".....",
     ".....",
     "....."]
]

O = [
    [".....",
     ".....",
     ".00..",
     ".00..",
     "....."]
]

J = [
    [".....",
     ".0...",
     ".000.",
     ".....",
     "....."],
    [".....",
     "..00.",
     "..0..",
     "..0..",
     "....."],
    [".....",
     ".....",
     ".000.",
     "...0.",
     "....."],
    [".....",
     "..0..",
     "..0..",
     ".00..",
     "....."]
]

L = [
    [".....",
     "...0.",
     ".000.",
     ".....",
     "....."],
    [".....",
     "..0..",
     "..0..",
     "..00.",
     "....."],
    [".....",
     ".....",
     ".000.",
     ".0...",
     "....."],
    [".....",
     ".00..",
     "..0..",
     "..0..",
     "....."]
]

T = [
    [".....",
     "..0..",
     ".000.",
     ".....",
     "....."],
    [".....",
     "..0..",
     "..00.",
     "..0..",
     "....."],
    [".....",
     ".....",
     ".000.",
     "..0..",
     "....."],
    [".....",
     "..0..",
     ".00..",
     "..0..",
     "....."]
]

shapes = [I, O, T, S, Z, J, L]

class Piece():
    def __init__(self, x,y, shape):
        self.x = x
        self.y = y
        self.shape = shape
        self.color = shape_colors[shapes.index(shape)]
        self.rotation = 0

class Player():
    def __init__(self, name):
        self.username = name
        self.score = 0
        self.next = None

    def get_score(self):
        return self.score

    def set_score(self, score):
        self.score = score

    def get_username(self):
        return self.username

    def set_username(self, username):
        self.username = username

    def increase_score(self, score):
        self.score += score

    def reset_score(self):
        self.score = 0
    
class PlayerQueue():
    def __init__(self):
        self.head = None
        self.tail = None

    def add_player(self, player: Player):
        if self.head == None:
            self.head = player
            self.tail = player
        else:
            self.tail.next = player
            self.tail = player
            self.tail.next = self.head

    def is_tail(self, player: Player) -> bool:
        return player == self.tail

    def peak_current(self) -> Player:
        return self.head
    
    def next_player(self) -> Player:
        if self.head == None:
            return None
        popped = self.head
        self.head = self.head.next
        self.tail.next = popped
        self.tail = popped
        return self.head

    def is_empty(self):
        return self.head == None