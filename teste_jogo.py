import pyxel


# Steve class é o personagem para chegar até o diamante
class Steve:
    def __init__(self, x, y):
        self.x = x
        self.y = y
        # w = width e h = height eu acho
        self.w = 8
        self.h = 8
    
    def draw(self):

        pyxel.blt(self.x, self.y, 0, 16, 0, self.w, self.h)

# Creeper class incluí servir como obstáculo para Steve
class Creeper:
    def __init__(self, x, y):
        self.x = x
        self.y = y
        self.w = 8
        self.h = 8
        
    def draw(self):
        # blt(x, y, img, u, v, w, h, [colkey])
        # Copy the region of size (w, h) from (u, v) of the image bank img (0-2) to (x, y). 
        # If negative value is set for w and/or h, it will reverse horizontally and/or vertically. If colkey is specified, treated as transparent color.
        
        pyxel.blt(self.x, self.y, 0, 0, 0, self.w, self.h)


class App:
    def __init__(self):
        pyxel.init(160, 120, title="Minecraft", fps=60)
        pyxel.load("assets/PYXEL_RESOURCE_FILE.pyxres")
        self.steve = Steve(0, 10)
        self.creeper = Creeper(0, 20)
        
        pyxel.run(self.update, self.draw)

    def update(self):
        pass

    def draw(self):
        pyxel.cls(0)
        self.steve.draw()
        self.creeper.draw()


# Início do Jogo
App()