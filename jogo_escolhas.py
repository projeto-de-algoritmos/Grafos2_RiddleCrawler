import pyxel

# Botão 
class Botao:
    def __init__(self, x, y):
        self.x = x
        self.y = y
        # w = width e h = height eu acho
        self.w = 8
        self.h = 8
        self.clicked = False # Adicione um atributo para rastrear se o botão foi clicado
    
    def draw(self):

        pyxel.text(40, 5, "Clique no botao", 7)

        pyxel.blt(self.x, self.y, 0, 32, 24, self.w, self.h)
        pyxel.blt(self.x + 8, self.y, 0, 40, 24, self.w, self.h)
        pyxel.blt(self.x, self.y + 8, 0, 32, 32, self.w, self.h)
        pyxel.blt(self.x + 8, self.y + 8, 0, 40, 32, self.w, self.h)

    def in_button(self, x, y):
        return self.x <= x <= self.x + self.w and self.y <= y <= self.y + self.h


class App:
    def __init__(self):
        pyxel.init(160, 120, title="Jogo de Escolhas", fps=60)
        pyxel.load("assets/PYXEL_RESOURCE_FILE.pyxres")
        self.botao = Botao(60, 10)    
    
        pyxel.mouse(True)
        pyxel.run(self.update, self.draw)

    def update(self):
        if pyxel.btnp(pyxel.KEY_Q):
            pyxel.quit()
        
        if pyxel.btn(pyxel.MOUSE_BUTTON_LEFT):
            if self.botao.in_button(pyxel.mouse_x, pyxel.mouse_y):
                self.botao.clicked = True
        

    def draw(self):
     
        pyxel.cls(0)
        self.botao.draw()

        if self.botao.clicked:
            pyxel.text(self.botao.x - 20, self.botao.y+15, "Voce clicou no botao", 7)


# Início do Jogo
App()