from src.Config.planet_templates import *
from src.SaveDataStuff.save_data import SaveData

from src.Others.camera import Camera
from src.Others.input import InputHandler

from src.InventoryStuff.inventory_screen import InventoryScreen

from src.PlanetSurfaceStuff.planet import Planet
from src.PlanetSurfaceStuff.player import *

from src.TransitionStuff.transition import TransitionScreen
from src.PlanetSurfaceStuff.enemy import Enemy
from src.PlanetSurfaceStuff.surface_settings import *

#from transition import TransitionScreen
import random

class Chunk:
    def __init__(self, cx, cy, terrain_data, object_data):
        self.cx = cx
        self.cy = cy
        self.terrain_data = terrain_data
        self.object_data = object_data
        # Futuramente: self.is_modified = False

class Level:
    '''
    Um objeto Level representa a tela quando você está na superfície de um planeta
    '''
    def __init__(self, screen, input_handler, save_data, planet):
        assert isinstance(screen, pygame.Surface)
        assert isinstance(input_handler, InputHandler)
        assert isinstance(save_data, SaveData)
        assert isinstance(planet, Planet)

        self.screen = screen
        self.input_handler = input_handler

        self.save_data = save_data
        # The Planet is now just a seed and a generator
        self.planet = planet

        self.all_sprites = pygame.sprite.Group()

        # Nave
        self.entering_ship = False
        self.ship_pos = pygame.Vector2(200, 200) #Para teste deixei uma posição fixa

        #inimigos
        self.enemy_sprites = pygame.sprite.Group()

        #Caso queira uma posição aletória opção abaixo
        #self.ship_pos = (random.randint(0, WORLD_SIZE_IN_CHUNKS[0] * CHUNK_SIZE - 1), 
        #random.randint(0, WORLD_SIZE_IN_CHUNKS[1] * CHUNK_SIZE - 1))
        
        self.ship_radius = 16
        self.sublevel = None
        
        # The player is created at a WORLD position
        self.player = Player(PLAYER_START_POS, self.all_sprites)
        
        # The camera will follow the player
        self.camera = Camera()
        
        # This dictionary will hold the active chunk data
        self.loaded_chunks = {}

        self.running = True

        self.ship_image = pygame.image.load("src/Assets/nave_old.png").convert_alpha()

        # opcional, se quiser mudar o tamanho
        self.ship_image = pygame.transform.scale(self.ship_image, (60, 60))

        inimigo1 = Enemy(pos_x=500, pos_y=500, player_ref=self.player, max_hp=3)
        inimigo2 = Enemy(pos_x=600, pos_y=400, player_ref=self.player, max_hp=3)

        self.all_sprites.add(inimigo1, inimigo2) # Para Update e Draw
        self.enemy_sprites.add(inimigo1, inimigo2) # Para Colisões

        self.debug_grid_mode = DEBUG_GRID_MODE_START # Começa ligado para você ver

        # NOVO: O "Delta File" / "Arquivo TXT"
        # Chave: (world_x, world_y), Valor: new_object_id
        # Isso armazena TODAS as mudanças feitas pelo jogador
        self.world_changes = {} 
        # Ex: self.world_changes[(100, 150)] = ObjectType.NONE # Árvore quebrou

        # NOVO: Carregador de Assets
        self.object_assets = {} # Dicionário para guardar os sprites
        self.load_object_assets()

        # Fonte para UI
        self.font = pygame.font.SysFont("arial", 24)

    def load_object_assets(self):
        print("Loading object assets...")
        for obj_type, props in OBJECT_PROPERTIES.items():
            if props['sprite_path']:
                try:
                    # CORREÇÃO 1: .convert_alpha() é crucial para transparência
                    sprite = pygame.image.load(props['sprite_path']).convert_alpha()
                    
                    # CORREÇÃO 2: NÃO escalar a imagem aqui. Carrega na resolução total.
                    # Apenas guarde o sprite original.
                    self.object_assets[obj_type] = sprite
                    print(f"Loaded asset: {props['sprite_path']}")
                except Exception as e:
                    print(f"ERROR: Could not load asset {props['sprite_path']}. Using fallback. {e}")
                    self.object_assets[obj_type] = None # Usará a cor de fallback

    def manage_chunks(self):
        """
        Loads new chunks that enter the camera's view and unloads old ones.
        """
        visible_chunks_x, visible_chunks_y = self.camera.get_visible_chunk_coords()
        
        # --- Load new chunks ---
        for cx in visible_chunks_x:
            for cy in visible_chunks_y:
                # Check if chunk is within finite world bounds
                if not (0 <= cx < WORLD_SIZE_IN_CHUNKS[0] and 0 <= cy < WORLD_SIZE_IN_CHUNKS[1]):
                    continue # Skip chunks outside the world
                    
                chunk_coord = (cx, cy)
                if chunk_coord not in self.loaded_chunks:
                    # 1. Gera o chunk "base" a partir do seed
                    terrain_data, object_data = self.planet.generate_chunk_data(cx, cy)
                    
                    # 2. Aplica o "Delta" (nossas mudanças salvas)
                    for local_y in range(CHUNK_SIZE):
                        for local_x in range(CHUNK_SIZE):
                            world_x = (cx * CHUNK_SIZE) + local_x
                            world_y = (cy * CHUNK_SIZE) + local_y
                            if (world_x, world_y) in self.world_changes:
                                # Sobrescreve o objeto gerado com nossa mudança
                                object_data[local_y][local_x] = self.world_changes[(world_x, world_y)]

                    # 3. Cria o objeto Chunk e armazena
                    new_chunk = Chunk(cx, cy, terrain_data, object_data)
                    self.loaded_chunks[chunk_coord] = new_chunk

        # --- Unload old chunks ---
        chunks_to_unload = set()
        for chunk_coord in self.loaded_chunks:
            cx, cy = chunk_coord
            if cx not in visible_chunks_x or cy not in visible_chunks_y:
                chunks_to_unload.add(chunk_coord)
                
        for chunk_coord in chunks_to_unload:
            del self.loaded_chunks[chunk_coord]

        # ATUALIZADO: draw_layers com Grid Mode

    def draw_layers(self):
        """
        Draws all layers: terrain first, then objects on top.
        """
        # CORREÇÃO DE ESCALA: TILE_SIZE agora deve ser 16 ou 32 no seu settings.py
        zoomed_tile_size = floor(TILE_SIZE * self.camera.zoom)
        if zoomed_tile_size <= 0: return 
        
        # --- PASS 1: Desenha o TERRENO ---
        for chunk_coord, chunk in self.loaded_chunks.items():
            for local_y, row in enumerate(chunk.terrain_data):
                for local_x, tile_type in enumerate(row):
                    
                    world_x = (chunk.cx * CHUNK_SIZE + local_x) * TILE_SIZE
                    world_y = (chunk.cy * CHUNK_SIZE + local_y) * TILE_SIZE
                    screen_pos = self.camera.world_to_screen(pygame.math.Vector2(world_x, world_y))
                    
                    rect = pygame.Rect(
                        floor(screen_pos.x), floor(screen_pos.y),
                        zoomed_tile_size, zoomed_tile_size
                    )
                    
                    color = colors.TILE_COLOR_MAP.get(tile_type, colors.black)
                    pygame.draw.rect(self.screen, color, rect)

                    # NOVO: Desenha o Grid de Debug
                    if self.debug_grid_mode and zoomed_tile_size > 4: # Só desenha se for visível
                        pygame.draw.rect(self.screen, colors.black, rect, 1) # '1' = contorno

        # --- PASS 2: Desenha os OBJETOS (Sprites ou Fallback) ---
        for chunk_coord, chunk in self.loaded_chunks.items():
            for local_y, row in enumerate(chunk.object_data):
                for local_x, object_type in enumerate(row):
                    
                    if object_type != ObjectType.NONE:
                        world_x = (chunk.cx * CHUNK_SIZE + local_x) * TILE_SIZE
                        world_y = (chunk.cy * CHUNK_SIZE + local_y) * TILE_SIZE
                        screen_pos = self.camera.world_to_screen(pygame.math.Vector2(world_x, world_y))
                        
                        rect = pygame.Rect(
                            floor(screen_pos.x), floor(screen_pos.y),
                            zoomed_tile_size, zoomed_tile_size
                        )

                        sprite = self.object_assets.get(object_type)
                        if sprite:
                            # CORREÇÃO 2: Escala o sprite original (full-res)
                            # para o tamanho de zoom final. Muito mais qualidade!
                            zoomed_sprite = pygame.transform.scale(sprite, (zoomed_tile_size, zoomed_tile_size))
                            self.screen.blit(zoomed_sprite, rect.topleft)
                        else:
                            color = colors.OBJECT_COLOR_MAP.get(object_type, colors.black)
                            pygame.draw.rect(self.screen, color, rect)
                        
                        # NOVO: Desenha o Grid de Debug por CIMA dos objetos também
                        if self.debug_grid_mode and zoomed_tile_size > 4:
                            pygame.draw.rect(self.screen, colors.black, rect, 1)

    def draw_sprites(self):
        """
        Draws all sprites (PLAYER, etc), correctly offset by the camera.
        """
        for sprite in self.all_sprites:
            world_rect = sprite.rect
            assert isinstance(world_rect, pygame.Rect)
            
            screen_pos = self.camera.world_to_screen(world_rect.topleft)
            zoomed_width = floor(world_rect.width * self.camera.zoom)
            zoomed_height = floor(world_rect.height * self.camera.zoom)
            
            screen_rect = pygame.Rect(
                floor(screen_pos.x),
                floor(screen_pos.y),
                zoomed_width,
                zoomed_height
            )
            self.player.draw_attacking_item(self.screen, self.camera)
            
            scaled_image = pygame.transform.scale(sprite.image, (zoomed_width, zoomed_height))
            self.screen.blit(scaled_image, screen_rect)

    def draw_ship(self):
        # Converte da posição do mundo para tela
        screen_pos = self.camera.world_to_screen(self.ship_pos)

        # Obtém o retângulo da imagem, centralizado na posição da nave
        ship_rect = self.ship_image.get_rect(center=(int(screen_pos.x), int(screen_pos.y)))

        # Desenha a imagem na tela
        self.screen.blit(self.ship_image, ship_rect)
    
    def check_ship_interaction(self):
        player_pos = self.player.position
        distance = player_pos.distance_to(self.ship_pos)
        if distance < self.ship_radius:
            return True
        return False
    
    def on_ship_interact(self):
        self.sublevel = TransitionScreen(self.screen, "Decolando...")

    def draw_hud(self):
        '''
        Desenha o texto com a quantidade de vidas do jogador, e desenha barras de vida para os inimigos
        '''
        hud_lives = self.font.render(f"VIDAS: {self.player.lives}", HUD_ANTIALIASING, HUD_COLOR)

        self.screen.blit(hud_lives, HUD_MARGIN)

        for enemy in self.enemy_sprites:
            assert isinstance(enemy, Enemy)
            enemy.draw_hp_bar(self.screen, self.camera)

    def run(self, dt):
        if self.sublevel != None:
            if isinstance(self.sublevel, TransitionScreen):
                if self.sublevel.active == False:
                    self.sublevel = None
                    self.running = False # Se terminou de transicionar, então vamos decolar, e podemos sair desta tela
                    return # Retorno direto para não desenhar esta tela
                else:
                    self.sublevel.run()
                    return
                
            if isinstance(self.sublevel, InventoryScreen):
                if not(self.sublevel.running):
                    self.sublevel = None
                else:
                    self.sublevel.run()
                    return
                    
        # Ler o input
        input = self.input_handler.get_input()

        # Features de debug
        if input.just_pressed[pygame.K_m]:
            print("Generating debug map...")
            self.generate_debug_map()
        if input.just_pressed[pygame.K_g]:
            self.debug_grid_mode = not(self.debug_grid_mode)
            print(f"Debug Grid Mode: {self.debug_grid_mode}")

        # Transições de tela
        # Checar abertura de inventário (tecla E)
        if input.just_pressed[pygame.K_e]:
            self.sublevel = InventoryScreen(self.screen, self.input_handler, self.save_data)

        if self.check_ship_interaction():
            self.on_ship_interact()

        # DETECTAR ATAQUE (Botão Esquerdo do Mouse)
        atacou = False
        if input.mouse_justpressed[0]: # [0] é o botão esquerdo
            atacou = self.attempt_attack()

        # Se atacou neste frame, desenha o ataque e checa dano
        if atacou:
            self.resolve_attack()

        self.check_enemy_collisions()

        # --- Update Phase ---
        self.camera.update(self.player.position)
        self.all_sprites.update(input, dt)
        self.manage_chunks()

        # --- Draw Phase ---
        self.screen.fill('black')
        self.draw_layers() 
        self.draw_sprites()
        self.draw_ship()
        self.draw_hud()
        
    def generate_debug_map(self):
        self.planet.generate_debug_map()

    def attempt_attack(self):
        # Verifica se o cooldown acabou
        if self.player.attack_cooldown <= 0:
            self.player.attack_cooldown = 0.5
            # Inicia a animação de ataque
            at_it_img = self.save_data.inventory[0].image
            # Redimensiona se a imagem for muito grande (Pixel art as vezes vem pequena ou enorme)
            at_it_img = pygame.transform.scale(at_it_img, ATTACKING_ITEM_IMAGE_DIMENSIONS)

            self.player.attacking = True
            self.player.attacking_item_image = at_it_img
            self.attacking_item_rect = at_it_img.get_rect()

            self.player.attack_timer = 0.0
            self.player.attack_angle = 90 # Ângulo inicial
            return True
        
        return False

    def resolve_attack(self):
        '''
        Roda uma única vez no frame em que o ataque começa (só aqui temos dano, e tudo mais). Nos demais frames, temos só a animação.
        '''
        attack_hitbox = self.player.get_attack_hitbox()
        attacking_item = self.save_data.inventory[0] # O item selecionado

        inimigos_atingidos = []
        for inimigo in self.enemy_sprites:
            assert isinstance(inimigo, Enemy)

            if attack_hitbox.colliderect(inimigo.rect):
                inimigos_atingidos.append(inimigo)

        for inimigo in inimigos_atingidos:
            assert isinstance(inimigo, Enemy)
            inimigo.take_damage(attacking_item.attack_power)
            
            # Empurrãozinho (Knockback)
            if inimigo.position != self.player.position:
                try:
                    direcao_empurrao = (inimigo.position - self.player.position).normalize()
                    inimigo.position += direcao_empurrao * 20
                except ValueError:
                    pass

    def check_enemy_collisions(self):
        '''
        Checa se um inimigo está colidindo com o jogador. Se sim, subtrai 1 à vida do jogador (pois todos os inimigos dão a mesma quantidade de dano)
        '''
        for enemy in self.enemy_sprites:
            assert isinstance(enemy, Enemy)
            r1 = enemy.rect
            r2 = self.player.rect

            if r1.colliderect(r2) and self.player.damage_cooldown == 0:
                self.player.lives -= 1
                self.player.damage_cooldown = MAX_DAMAGE_COOLDOWN