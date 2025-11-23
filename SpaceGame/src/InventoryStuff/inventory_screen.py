import pygame
from src.Others.input import InputHandler, InputFrame

from src.SaveDataStuff.save_data import SaveData
from src.SaveDataStuff.item import Item

from src.InventoryStuff.inventory_settings import *
from src.Config.settings import *

from src.Others.helper import draw_text_rectangle

class InventoryScreen:
    '''
    Representa a tela de manejamento de inventário
    '''

    def __init__(self, screen, input_handler, save_data):
        assert isinstance(screen, pygame.Surface)
        assert isinstance(input_handler, InputHandler)
        assert isinstance(save_data, SaveData)

        # Copiar os parâmetros
        self.screen = screen
        self.input_handler = input_handler
        self.save_data = save_data

        # Demais atributos
        self.running = True

        # Pegar uma cópia da imagem da superfície agora, para desenhar no fundo
        self.background_image = self.screen.copy().convert_alpha()

    def draw_all(self, input):
        # Como vamos usar alpha, precisamos desenhar tudo em um outro Surface, e depois desenhar esse Surface na tela
        assert isinstance(input, InputFrame)

        scr = pygame.Surface((SCREEN_WIDTH, SCREEN_HEIGHT), flags=pygame.SRCALPHA)

        scr.fill('black')
        scr.blit(self.background_image, (0,0))

        overlay = pygame.Surface((SCREEN_WIDTH, SCREEN_HEIGHT))
        overlay.fill(OVERLAY_COLOR)
        overlay.set_alpha(OVERLAY_ALPHA)

        scr.blit(overlay, (0, 0))

        # Desenhar o inventário
        self.draw_inventory(scr)
        # Desenhar um texto sobre o item selecionado
        i = self.selected_item_i(input)
        inv = self.save_data.inventory
        mp = input.mouse_pos
        if 0 <= i and i < len(inv):
            #print(i)
            item = inv[i]
            assert isinstance(item, Item)

            draw_text_rectangle(
                scr,
                
                [
                    f'Poder de ataque: {item.attack_power}'
                ],
            
                (
                    mp[0],
                    mp[1]
                )
        )

        self.screen.fill('black')
        self.screen.blit(scr, (0, 0))

    def draw_inventory(self, scr):
        '''
        Desenha o inventário em cima da superfície scr, usando alpha. scr, depois, sera blittada em cima de self.screen em draw_all
        '''
        assert isinstance(scr, pygame.Surface)

        inv = self.save_data.inventory
        x = MARGIN
        y = MARGIN
        i = 0
        while i < MAX_INVENTORY_SIZE:
            rect_surf = pygame.Surface((SQUARE_WIDTH, SQUARE_WIDTH))
            rect_surf.fill(SQUARE_COLOR)
            rect_surf.set_alpha(SQUARE_ALPHA)
            scr.blit(rect_surf, (x, y))

            if i < len(inv):
                img = pygame.transform.scale(inv[i].image, (SQUARE_WIDTH, SQUARE_WIDTH))
                scr.blit(img, (x, y))

            i += 1
            if i % SQUARES_PER_LINE != 0:
                x += SQUARE_WIDTH
            else:
                x = MARGIN
                y += SQUARE_WIDTH

    def selected_item_i(self, input):
        '''
        A partir da posição do mouse, determina o índice do item selecionado do inventário
        '''
        pos = input.mouse_pos
        
        # Pegar a posição em relação ao início do inventário
        x = pos[0] - MARGIN
        y = pos[1] - MARGIN

        x_coord = x//SQUARE_WIDTH
        y_coord = y//SQUARE_WIDTH

        i = SQUARES_PER_LINE*y_coord + x_coord

        return i

    def react_click(self, input):
        '''
        Reage a um clique. Se o jogador clicou em um item, troca esse item de posição com o primeiro do inventário, assim selecionando o item
        '''
        assert isinstance(input, InputFrame)

        i = self.selected_item_i(input)
        inv = self.save_data.inventory

        """
        print(f'''
        x: {x}
        y = {y}
        x_coord = {x_coord}
        y_coord = {y_coord}
        i = {i}      
        ''')
        """

        if 0 <= i and i < len(inv):
            # Troca de posição com o item 0
            selected = inv[i]
            inv[i] = inv[0]
            inv[0] = selected

    def run(self):
        # Fase de atualização
        input = self.input_handler.get_input()

        if input.just_pressed[pygame.K_e]:
            self.running = False

        # Checar se clicou em um item
        if input.mouse_justpressed[0]:
            self.react_click(input)

        # Fase de desenho
        self.draw_all(input)