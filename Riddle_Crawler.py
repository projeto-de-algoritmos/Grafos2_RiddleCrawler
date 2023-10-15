import pyxel

# Botão 
class Botao:
    def __init__(self, x, y):
        self.x = x
        self.y = y
        # w = width e h = height eu acho
        self.w = 22
        self.h = 12
        self.clicked = False # Adicione um atributo para rastrear se o botão foi clicado
    
    def draw(self):


        # self.x e self.y são as coordenadas na tela, 0 é o banco de imagens, 80 e 0 é as coordenadas no banco, elf.w e self.h se refere a width e height da imagem
        pyxel.blt(self.x, self.y, 0, 80, 0, self.w, self.h)

    # Função que verifica se as coordenadas recebidas se equivalem as do botão
    def in_button(self, x, y):
        return self.x <= x <= self.x + self.w and self.y <= y <= self.y + self.h


class App:
    def __init__(self):
        pyxel.init(160, 120, title="Jogo de Escolhas", fps=60)
        pyxel.load("assets/riddle.pyxres")
        self.botao = Botao(50, 50)    
        self.far_cloud = [(-10, 75), (40, 65), (90, 60)]
        self.near_cloud = [(10, 25), (70, 35), (120, 15)]

        pyxel.mouse(True)
        pyxel.run(self.update, self.draw)

    def update(self):
        if pyxel.btnp(pyxel.KEY_Q):
            pyxel.quit()
        
        if pyxel.btn(pyxel.MOUSE_BUTTON_LEFT):
            # Se retornar as coordenadas do botão iguais as do mouse, então o botão foi clicado
            if self.botao.in_button(pyxel.mouse_x, pyxel.mouse_y):
                self.botao.clicked = True
        

    def draw(self):
     
        pyxel.cls(12)
        self.botao.draw()

        pyxel.text(30, 5, "Bem-vindo ao Riddle Crawler", 1)

        # Desenha o céu
        pyxel.blt(0, 88, 0, 0, 88, 160, 32)

        # Desenha montanha
        pyxel.blt(0, 88, 0, 0, 64, 160, 24, 12)

        # Desenha árvores
        offset = pyxel.frame_count % 160
        for i in range(2):
            pyxel.blt(i * 160 - offset, 104, 0, 0, 48, 160, 16, 12)

        # Desenha nuvens
        offset = (pyxel.frame_count // 16) % 160
        for i in range(2):
            for x, y in self.far_cloud:
                pyxel.blt(x + i * 160 - offset, y, 0, 64, 32, 32, 8, 12)
        offset = (pyxel.frame_count // 8) % 160
        for i in range(2):
            for x, y in self.near_cloud:
                pyxel.blt(x + i * 160 - offset, y, 0, 0, 32, 56, 8, 12)

        if self.botao.clicked:
            pyxel.text(self.botao.x - 30, self.botao.y + 15, "Voce clicou no botao", 1)


# Início do Jogo
App()