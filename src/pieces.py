shape_list = ["I", "O", "T", "S", "Z", "J", "L"]
shape_colors = [(0,255,255), (255,255,0), (128,0,128), (0,255,0), (255,0,0), (0,0,255), (255,165,0)]

class Piece():
    def __init__(self, x,y, shape):
        self.x = x
        self.y = y
        self.shape = shape
        self.color = shape_colors[shape_list.index(shape)]
        self.rotation = 0