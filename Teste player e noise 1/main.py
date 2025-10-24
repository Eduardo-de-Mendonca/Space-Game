import warnings
warnings.filterwarnings('ignore', category=UserWarning, module='pygame.pkgdata')

import sys
from game import Game

if __name__ == '__main__':
    # Create an instance of the Game class
    game = Game()
    # Run the game
    game.run()
    # Exit the program
    sys.exit()

    #O jogo é um objeto de uma classe né, acho que assim que deve ser pelo que eu vi de melhor prática. Esse arquivo só roda mesmo