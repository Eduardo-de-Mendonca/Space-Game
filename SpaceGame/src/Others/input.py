import pygame

class InputFrame:
    '''
    Representa todo o input do usuário em um único frame. Isso inclui quais teclas estão sendo pressionadas e quais acabaram de ser, além de algumas informações que podem ser lidas a partir de eventos. O objeto é mutável.
    '''

    def __init__(self):
        'Constrói um InputFrame "vazio" (os atributos pressing e pressed são listas cheias de False)'

        self.pressing = []
        self.just_pressed = []
        for key in pygame.key.get_pressed():
            self.pressing.append(False)
            self.just_pressed.append(False)

        self.mousewheel_x = 0
        self.mousewheel_y = 0
        self.mouse_pressing = []
        self.mouse_justpressed = []
        for button in pygame.mouse.get_pressed():
            self.mouse_pressing.append(False)
            self.mouse_justpressed.append(False)

        self.mouse_pos = (0, 0)

class InputHandler:
    '''
    Haverá um único objeto dessa classe, lidando todo o input do jogo. O método get_input deverá ser chamado 1 vez por frame, e ele lidará com a lógica de descobrir quais teclas estão sendo apertadas e quais acabaram de ser soltas.

    Informações de eventos devem ser escritas em InputHandler.next_input.
    '''

    def __init__(self):
        self.prev_input = InputFrame()
        self.next_input = InputFrame()

    def get_input(self):
        '''
        Deve ser chamado 1 vez ao início de cada frame. Isso será feito dentro da tela relevante, e não em game.py. Retorna um objeto InputFrame
        '''
        pi = self.prev_input
        ni = self.next_input
        
        # Ler todo o input e guardar em ni
        keys = pygame.key.get_pressed()
        # keys é um vetor de buleanos, em que o índice indica a tecla e o valor indica se está sendo apertada. Na verdade, é um objeto ScancodeWrapper que se comporta dessa maneira
        ni.pressing = keys
        for k in range(len(keys)):
            # Uma tecla acabou de ser apertada se não foi apertada frame passado
            ni.just_pressed[k] = ni.pressing[k] and not(pi.pressing[k])

        # Botões do mouse
        mouse_buttons = pygame.mouse.get_pressed()
        ni.mouse_pressing = mouse_buttons
        for k in range(len(mouse_buttons)):
            ni.mouse_justpressed[k] = ni.mouse_pressing[k] and not(pi.mouse_pressing[k])
        
        # Posição do mouse
        ni.mouse_pos = pygame.mouse.get_pos()


        # O next vira o prev, para ser usado como referência no próximo frame
        self.prev_input = ni
        self.next_input = InputFrame()

        return ni