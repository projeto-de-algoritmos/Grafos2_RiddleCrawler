import pyxel
import json
import random
from graph import randomWeightedGraph, dijkstra

SCENE_TITLE = 0
SCENE_PLAY = 1
SCENE_GAMEOVER = 2

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
    # for node1, edges in graph.items():
    #     for node2, weight in edges.items():
    #         print(f"Edge ({node1}, {node2}) has weight {weight}")

    # print(f"Nodes: {num_nodes} Edges: {num_edges}")
    # print(f"Shortest path from {start_node} to {end_node}: {shortest_path}")
    # print(f"Shortest distance from {start_node} to {end_node}: {shortest_distance}")

    random.shuffle(objects)
    
    for i in range(15):
        objects[i]["node"] = i
        
    return shortest_path, graph, objects, traps

# Botão 
class Botao:
    def __init__(self, x, y, item):
        self.x = x
        self.y = y
        # w = width e h = height eu acho
        self.w = 22
        self.h = 12
        self.clicked = False # Adicione um atributo para rastrear se o botão foi clicado
        self.name = item["name"]
    
    def draw(self):
        # self.x e self.y são as coordenadas na tela, 0 é o banco de imagens, 80 e 0 é as coordenadas no banco, elf.w e self.h se refere a width e height da imagem
        pyxel.blt(self.x, self.y, 0, 80, 0, self.w, self.h)

    # Função que verifica se as coordenadas recebidas se equivalem as do botão
    def in_button(self, x, y):
        return self.x <= x <= self.x + self.w and self.y <= y <= self.y + self.h

class App:
    def __init__(self):
        thisdict = { "name": "Cadeira", "trap": True }
        pyxel.init(160, 120, title="Riddle Crawler", fps=60)
        pyxel.load("assets/riddle.pyxres")
        self.botao = Botao(50, 50, thisdict)        
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
        
        # Atualização da tela inicial para tela de jogo e gameover
        # self.background.update()
        # if self.scene == SCENE_TITLE:
        #     self.update_title_scene()
        # elif self.scene == SCENE_PLAY:
        #     self.update_play_scene()
        # elif self.scene == SCENE_GAMEOVER:
        #     self.update_gameover_scene()

        # def update_title_scene(self):
        #     if pyxel.btnp(pyxel.KEY_RETURN) or pyxel.btnp(pyxel.GAMEPAD1_BUTTON_X):
        #         self.scene = SCENE_PLAY

        # def update_play_scene(self):
        #     pass

    # FUNÇÃO QUE DESENHA O JOGO E O CENÁRIO
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
        # for i in range(2):
        #     for x, y in self.far_cloud:
        #         pyxel.blt(x + i * 160 - offset, y, 0, 64, 32, 32, 8, 12)

        offset = (pyxel.frame_count // 8) % 160
        for i in range(2):
            for x, y in self.near_cloud:
                pyxel.blt(x + i * 160 - offset, y, 0, 0, 32, 56, 8, 12)

        
        if self.botao.clicked:
            pyxel.text(self.botao.x - 30, self.botao.y + 15, "Voce clicou no botao", 1)


# Início do Jogo
App()