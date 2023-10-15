import pyxel

SCENE_TITLE = 0
SCENE_PLAY = 1
SCENE_GAMEOVER = 2

def load_bgm(msc, filename, snd1, snd2, snd3):
    # Loads a json file for 8bit BGM generator by frenchbread.
    # Each track is stored in snd1, snd2 and snd3 of the sound
    # respectively and registered in msd of the music.
    import json

    with open(filename, "rt") as file:
        bgm = json.loads(file.read())
        pyxel.sound(snd1).set(*bgm[0])
        pyxel.sound(snd2).set(*bgm[1])
        pyxel.sound(snd3).set(*bgm[2])
        pyxel.music(msc).set([snd1], [snd2], [snd3], [])

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


# 
class App:
    def __init__(self):
        pyxel.init(160, 120, title="Riddle Crawler", fps=60)
        pyxel.load("assets/riddle.pyxres")
        self.botao = Botao(50, 50)    
        # self.far_cloud = [(-10, 75), (40, 65), (90, 60)]
        self.near_cloud = [(10, 25), (70, 35), (120, 15)]

        # Carregando Música do Jogo
        pyxel.sound(0).set("a3a2c1a1", "p", "7", "s", 5)
        pyxel.sound(1).set("a3a2c2c2", "n", "7742", "s", 10)
        load_bgm(0, "assets/bgm_title.json", 2, 3, 4)
        load_bgm(1, "assets/bgm_play.json", 5, 6, 7)

        # Começando na tela inicial
        self.scene = SCENE_TITLE

        # Carregando música, mouse e o jogo
        pyxel.playm(0, loop=True)
        pyxel.mouse(True)
        pyxel.run(self.update, self.draw)

    # FUNÇÃO QUE ATUALIZA O QUE OCORRE NO JOGO
    def update(self):
        if pyxel.btnp(pyxel.KEY_Q):
            pyxel.quit()
        
        if pyxel.btn(pyxel.MOUSE_BUTTON_LEFT):
             # Se retornar as coordenadas do botão iguais as do mouse, então o botão foi clicado
                if self.botao.in_button(pyxel.mouse_x, pyxel.mouse_y):
                    self.botao.clicked = True
    
         # Atualização da tela
        if self.scene == SCENE_TITLE:
            self.update_title_scene()
        elif self.scene == SCENE_PLAY:
            self.update_play_scene()
        elif self.scene == SCENE_GAMEOVER:
            self.update_gameover_scene()

    def update_title_scene(self):
        if pyxel.btnp(pyxel.KEY_RETURN) or pyxel.btnp(pyxel.GAMEPAD1_BUTTON_X):
             self.scene = SCENE_PLAY

    # Atualizar com a lógica dos Botões
    def update_play_scene(self):
        pass

    def update_gameover_scene(self):
        pass


    # FUNÇÃO QUE DESENHA O JOGO E O CENÁRIO
    def draw(self):
     
        # Cor de fundo
        pyxel.cls(12)

        # Seção que verifica os estados do jogo para desenhar com base nisso
        if self.scene == SCENE_TITLE:
            self.draw_title_scene()
        elif self.scene == SCENE_PLAY:
            self.draw_play_scene()
        elif self.scene == SCENE_GAMEOVER:
            self.draw_gameover_scene()
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
        # for i in range(2):
        #     for x, y in self.far_cloud:
        #         pyxel.blt(x + i * 160 - offset, y, 0, 64, 32, 32, 8, 12)

        offset = (pyxel.frame_count // 8) % 160
        for i in range(2):
            for x, y in self.near_cloud:
                pyxel.blt(x + i * 160 - offset, y, 0, 0, 32, 56, 8, 12)

    # Seção das funções de desenhar de cada cena
    def draw_title_scene(self):
        pyxel.text(25, 45, "Bem-vindo ao Riddle Crawler", pyxel.frame_count % 8)
        pyxel.text(55, 55, "APERTE ENTER", 8)

    def draw_play_scene(self):
        self.botao.draw()
        if self.botao.clicked:
            pyxel.text(self.botao.x - 30, self.botao.y + 15, "Voce clicou no botao", 1)

    def draw_gameover_scene(self):
        pyxel.text(43, 66, "GAME OVER", 8)
        pyxel.text(31, 126, "APERTE ENTER", 13)
        

# Início do Jogo
App()