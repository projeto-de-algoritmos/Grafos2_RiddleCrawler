import pyxel
import json
import random
from graph import randomWeightedGraph, dijkstra

# Variáveis que indicam a tela que o jogo está
SCENE_TITLE = 0
SCENE_PLAY = 1
SCENE_GAMEOVER = 2
SCENE_RESULT = 3

def load_bgm(msc, filename, snd1, snd2, snd3):
    # Loads a json file for 8bit BGM generator by frenchbread.
    # Each track is stored in snd1, snd2 and snd3 of the sound
    # respectively and registered in msd of the music.

    with open(filename, "rt") as file:
        bgm = json.loads(file.read())
        pyxel.sound(snd1).set(*bgm[0])
        pyxel.sound(snd2).set(*bgm[1])
        pyxel.sound(snd3).set(*bgm[2])
        pyxel.music(msc).set([snd1], [snd2], [snd3], [])

def generate_game():
    file = open("./assets/json/objects.json")
    data = json.load(file)
    objects = data["objects"]
    file.close()
    
    file = open("./assets/json/traps.json")
    data = json.load(file)
    traps = data["traps"]
    file.close()
    
    num_nodes = 15
    num_edges = num_nodes + int(num_nodes / 2)
    min_weight = 10
    max_weight = 17
    start_node = 0
    end_node = 14
    
    shortest_path = [14]

    # Loop to create a graph that has a path between 0 and 14
    while(shortest_path == [14]):
        graph = randomWeightedGraph(num_nodes, num_edges, min_weight, max_weight)
        shortest_path, shortest_distance = dijkstra(graph, start_node, end_node)
        
    # Print the edges and their weights
    for node1, edges in graph.items():
        for node2, weight in edges.items():
            print(f"Edge ({node1}, {node2}) has weight {weight}")
            

    print(f"Nodes: {num_nodes} Edges: {num_edges}")
    print(f"Shortest path from {start_node} to {end_node}: {shortest_path}")
    print(f"Shortest distance from {start_node} to {end_node}: {shortest_distance}")

    random.shuffle(objects)
    
    for i in range(15):
        objects[i]["node"] = i
        
    random.shuffle(traps)
        
    return shortest_path, graph, objects, traps

# Botão 
class Botao:
    def __init__(self, x, y, name):
        self.x = x
        self.y = y
        # w = width e h = height
        self.w = 22
        self.h = 8
        self.clicked = False # Adicione um atributo para rastrear se o botão foi clicado
        self.name = name
    
    def draw(self):
        # self.x e self.y são as coordenadas na tela, 0 é o banco de imagens, 80 e 0 é as coordenadas no banco, elf.w e self.h se refere a width e height da imagem
        pyxel.blt(self.x, self.y, 0, 80, 4, self.w, self.h)
        pyxel.text(self.x, self.y + 9, self.name, 1)

    # Função que verifica se as coordenadas recebidas se equivalem as do botão
    def in_button(self, x, y):
        return self.x <= x <= self.x + self.w and self.y <= y <= self.y + self.h

class App:
    def __init__(self): 
        # Iniciando tela e carregando assets
        pyxel.init(240, 120, title="Riddle Crawler", fps=60)
        pyxel.load("assets/riddle.pyxres")

        # Carregando Elementos da tela  
        self.near_cloud = [(10, 25), (70, 35), (120, 15)]
        
        # Atributos do balão inflável
        self.balao_x = 210
        self.balao_y = 69
        self.move_up = True
        self.move_speed = 0.2

        self.path = []
        self.counter = 0
        self.graph = []
        self.objects = []
        self.randRiddle = None
        self.traps = []
        self.reset = True
        self.answer = None
        self.guess = None
        self.hp = 50
        self.win = False
        # self.far_cloud = [(-10, 75), (40, 65), (90, 60)]

        # Variáveis para controlar a resposta do jogador e Emoji
        self.resultado_message = ""
        self.show_message = False
        self.emoji = "right"
        
        # Carregando Música do Jogo
        # pyxel.sound(0).set("a3a2c1a1", "p", "7", "s", 5)
        # pyxel.sound(1).set("a3a2c2c2", "n", "7742", "s", 10)
        # load_bgm(0, "assets/bgm_title.json", 2, 3, 4)
        # load_bgm(1, "assets/bgm_play.json", 5, 6, 7)

        # Começando na tela inicial
        self.scene = SCENE_TITLE

        # Carregando música, mouse e o jogo
        # pyxel.playm(0, loop=True)
        pyxel.mouse(True)
        pyxel.run(self.update, self.draw)

    def check_answer(self):
        if(self.answer == self.guess):
            # Acertou  
            if(self.hp < 50):
                if(self.counter == 0):
                    self.hp += 10
                else:
                    self.hp += self.graph[self.path[self.counter]][self.path[self.counter + 1]]
                    
                if(self.hp > 50):
                    self.hp = 50
            
            self.counter += 1
            self.emoji = "right"
            self.resultado_message = "ACERTOU"
            self.scene = SCENE_RESULT
            
        elif(self.guess == self.traps[0] or self.guess == self.traps[1]):
            # Errou na armadilha
            self.hp -= 25
            if(self.hp <= 0):
                # Encerra o jogo, derrota
                self.scene = SCENE_GAMEOVER    
            
            self.emoji = 'wrong'
            self.resultado_message = "ERROU"
            self.scene = SCENE_RESULT
        else:
            # Errou no grafo
            self.hp -= random.randint(10, 15)
            if(self.hp <= 0):
                self.scene = SCENE_GAMEOVER 
            
            self.emoji = 'wrong'
            self.resultado_message = "ERROU"
            self.scene = SCENE_RESULT
        
        if(self.counter == len(self.path) - 1):
            # Encerra o jogo, vitória
            self.win = True
            self.scene = SCENE_RESULT

    # FUNÇÃO QUE ATUALIZA O QUE OCORRE NO JOGO
    def update(self):
        if pyxel.btnp(pyxel.KEY_Q):
            pyxel.quit()
        # Movimento do balão
        # Verifica se o balão deve se mover para cima ou para baixo
        if self.move_up:
            self.balao_y -= self.move_speed
        else:
            self.balao_y += self.move_speed

        # Inverte a direção quando o balão atinge as alturas limite
        if self.balao_y <= 50:
            self.move_up = False
        elif self.balao_y >= 70:
            self.move_up = True

        # Atualização da tela
        if self.scene == SCENE_TITLE:
            self.update_title_scene()
        elif self.scene == SCENE_PLAY:
            self.update_play_scene()
        elif self.scene == SCENE_GAMEOVER:
            self.update_gameover_scene()
        elif self.scene == SCENE_RESULT:
            self.update_result_scene()
    

    def update_title_scene(self):
        
        self.win = False
        if pyxel.btnp(pyxel.KEY_RETURN):
            self.scene = SCENE_PLAY
        
        if(self.reset):
            self.path, self.graph, self.objects, self.traps = generate_game()
            self.randRiddle = random.randint(0, 4)
            self.reset = False
        
        self.answer = self.objects[self.path[self.counter]]["name"]
    
        name_list = []
        name_list.append(self.objects[self.path[self.counter]]["name"])
        name_list.append(self.objects[1]["name"])
        name_list.append(self.traps[0])
        name_list.append(self.traps[1])
        
        random.shuffle(name_list)
        
        self.botao1 = Botao(64, 50, name_list[0])
        self.botao2 = Botao(156, 50, name_list[1])
        self.botao3 = Botao(64, 70, name_list[2])
        self.botao4 = Botao(156, 70, name_list[3])  

    # Atualizar com a lógica dos Botões
    def update_play_scene(self):
            
        if pyxel.btn(pyxel.MOUSE_BUTTON_LEFT):
            # Se retornar as coordenadas do botão iguais as do mouse, então o botão foi clicado
            if self.botao1.in_button(pyxel.mouse_x, pyxel.mouse_y):
                self.botao1.clicked = True
                self.guess = self.botao1.name
                self.check_answer()
    
            if self.botao2.in_button(pyxel.mouse_x, pyxel.mouse_y):
                self.botao2.clicked = True
                self.guess = self.botao2.name
                self.check_answer()
            
            if self.botao3.in_button(pyxel.mouse_x, pyxel.mouse_y):
                self.botao3.clicked = True
                self.guess = self.botao3.name
                self.check_answer()
                
            if self.botao4.in_button(pyxel.mouse_x, pyxel.mouse_y):
                self.botao4.clicked = True
                self.guess = self.botao4.name
                self.check_answer()
    
    
    # Atualiza o gameover
    def update_gameover_scene(self):
        # Resetando os botões
        self.botao1.clicked = False
        self.botao2.clicked = False
        self.botao3.clicked = False
        self.botao4.clicked = False

        # Resetando o Game
        self.path = []
        self.counter = 0
        self.graph = []
        self.objects = []
        self.randRiddle = None
        self.traps = []
        self.reset = True
        self.answer = None
        self.guess = None
        self.hp = 50

        # Resetando mensagens
        self.resultado_message = ""
        self.show_message = False

        if pyxel.btnp(pyxel.KEY_RETURN):
            self.reset = True
            self.scene = SCENE_TITLE

    # atualiza com o resultado de uma resposta
    def update_result_scene(self):
        self.show_message = True
        
        # Resetando os botões
        self.botao1.clicked = False
        self.botao2.clicked = False
        self.botao3.clicked = False
        self.botao4.clicked = False
        
        # Acabou o jogo = PERDEU
        if(self.hp <= 0):
            self.scene = SCENE_GAMEOVER
        
        # Acabou o jogo = VENCEU
        if self.win == True:

            # Resetando o Game
            self.path = []
            self.counter = 0
            self.graph = []
            self.objects = []
            self.randRiddle = None
            self.traps = []
            self.reset = True
            self.answer = None
            self.guess = None
            self.hp = 50
            
            self.show_message = False
            self.resultado_message = "VOCE GANHOU!!!"

            if pyxel.btnp(pyxel.KEY_RETURN):
                self.scene = SCENE_TITLE
                
        else:
            self.answer = self.objects[self.path[self.counter]]["name"]
    
            random.shuffle(self.traps)
            name = self.objects[self.path[self.counter]]["name"]
            
            while(name == self.objects[self.path[self.counter]]["name"]):
                i = random.randint(0, 14)
                name = self.objects[i]["name"]
    
            name_list = []
            name_list.append(self.objects[self.path[self.counter]]["name"])
            name_list.append(name)
            name_list.append(self.traps[0])
            name_list.append(self.traps[1])
        
            random.shuffle(name_list)
        
            self.botao1 = Botao(64, 50, name_list[0])
            self.botao2 = Botao(156, 50, name_list[1])
            self.botao3 = Botao(64, 70, name_list[2])
            self.botao4 = Botao(156, 70, name_list[3])  

            self.randRiddle = random.randint(0, 4)
            self.guess = None
                        
            if pyxel.btnp(pyxel.KEY_RETURN):
                self.show_message = False
                self.resultado_message = ""
                self.scene = SCENE_PLAY
            

# --------------------------------------------------------------------------------------------------------------------------------
    # FUNÇÃO QUE DESENHA O JOGO E O CENÁRIO
    def draw(self):
        # Cor de fundo
        pyxel.cls(12)

        # Desenha o céu
        pyxel.blt(0, 88, 0, 0, 88, 240, 32)

        # Desenha as montanhas 
        pyxel.blt(0, 88, 0, 0, 64, 240, 24, 12)
        pyxel.blt(130, 88, 0, 0, 64, 240, 24, 12)

        # Desenha Balão
        pyxel.blt(self.balao_x, self.balao_y, 0, 152, 24, 16, 16)

        # Desenha árvores
        offset = pyxel.frame_count % 240
        for i in range(2):
            pyxel.blt(i * 240 - offset, 104, 0, 0, 48, 240, 16, 12)

        # Desenha nuvens
        offset = (pyxel.frame_count // 16) % 160

        offset = (pyxel.frame_count // 8) % 160
        for i in range(2):
            for x, y in self.near_cloud:
                pyxel.blt(x + i * 160 - offset, y, 0, 0, 32, 56, 8, 12)

        # Seção que verifica os estados do jogo para desenhar com base nisso
        if self.scene == SCENE_TITLE:
            self.draw_title_scene()
        elif self.scene == SCENE_PLAY:
            self.draw_play_scene()
        elif self.scene == SCENE_GAMEOVER:
            self.draw_gameover_scene()
        elif self.scene == SCENE_RESULT:
            self.draw_result_scene()

    # Seção das funções de desenhar de cada cena
    def draw_title_scene(self):
        
        # Desenhando título do jogo
        pyxel.text(92, 45, "RIDDLE CRAWLER", 0)
        pyxel.text(96, 55, "APERTE ENTER", 8)

        # Desenhando aranha
        pyxel.blt(111, 60, 0, 0, 0, 16, 16)

    # Desenha os cenários quando se inicia o jogo
    def draw_play_scene(self):
        pyxel.text(4, 28, self.objects[self.path[self.counter]]["riddles"][self.randRiddle], 1)
        self.botao1.draw()
        self.botao2.draw()
        self.botao3.draw()
        self.botao4.draw()
        pyxel.blt(12, 8, 0, 128, 0, 8, 8)
        pyxel.text(20, 9, f":{self.hp}", 1)

        if self.botao1.clicked:
            pyxel.text(self.botao1.x - 18, self.botao1.y + 15, "Voce clicou no botao", 1)

        if self.botao2.clicked:
            self.scene = SCENE_GAMEOVER

    def draw_gameover_scene(self):
        pyxel.text(105, 66, "GAME OVER", 8)
        pyxel.text(96, 76, "Aperte Enter", 1)

    # atualiza com o resultado de uma resposta
    def draw_result_scene(self):

        if self.win == True:
            # Emoji Win
            pyxel.blt(115, 50, 0, 187, 13, 10, 10)
            pyxel.text(92, 40, self.resultado_message, 8)
            pyxel.text(96, 65, "Aperte Enter", 11)
            
            
        # Desenho do Emoji, para inserir as duas variáveis do Emoji, é só criar uma variavel que controla isso em update
        elif self.emoji == "right" and self.win == False:
            pyxel.blt(115, 50, 0, 187, 13, 10, 10)
            pyxel.text(106, 40, self.resultado_message, 8)
            pyxel.text(96, 65, "Aperte Enter", 0)
        else:
            pyxel.blt(115, 50, 0, 187, 37, 10, 10)
            pyxel.text(110, 40, self.resultado_message, 8)
            pyxel.text(96, 65, "Aperte Enter", 0)
            
        

# ------------------------------------------------------
# Início do Jogo
App()