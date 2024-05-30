shape_colors = [(0,255,255), (255,255,0), (128,0,128), (0,255,0), (255,0,0), (0,0,255), (255,165,0)]
import typing
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

class User():
    def __init__(self, username):
        self.username = username
        self.score = 0

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

class UserQueue():
    def __init__(self):
        self.queue = []
    
    def add_user(self, user):
        self.queue.append(user)

    def get_user(self):
        user = self.queue.pop(0)
        self.queue.append(user)
        return user
    
    def get_queue(self) -> list[User]:
        return self.queue
    
    def is_empty(self):
        return len(self.queue) == 0