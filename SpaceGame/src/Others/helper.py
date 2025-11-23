import math
import pygame
from src.Config.planet_templates import colors

def map_value_to_range(value, old_min, old_max, new_min, new_max):
    """
    Maps a value from one numerical range to another.

    Args:
        value (float or int): The value to be mapped.
        old_min (float or int): The minimum value of the original range.
        old_max (float or int): The maximum value of the original range.
        new_min (float or int): The minimum value of the target range.
        new_max (float or int): The maximum value of the target range.

    Returns:
        float: The mapped value in the new range.
    """
    # Calculate the width of each range
    old_span = old_max - old_min
    new_span = new_max - new_min

    # Calculate the value's position within the old range as a 0-1 ratio
    if old_span == 0:  # Handle cases where the old range is a single point
        return new_min if value == old_min else None  # Or raise an error, depending on desired behavior
    
    value_scaled = float(value - old_min) / float(old_span)

    # Map the 0-1 ratio to the new range
    mapped_value = new_min + (value_scaled * new_span)
    return mapped_value

def draw_text(screen, text, x, y):
    assert isinstance(screen, pygame.Surface)

    font = pygame.font.SysFont('Arial', 30)
    image = font.render(text, True, colors.white)
    screen.blit(image, (x, y))

def _text_drawing_rectangle_image(text_list, font=None, text_color = colors.white):
    '''
    Retorna uma Surface que é um retângulo preto com o texto em cima. text_list é um list de strings, tal que cada uma vai em uma linha.
    '''

    if font == None:
        font = pygame.font.SysFont('Arial', 30)

    images = []
    for text in text_list:
        img = font.render(text, True, text_color)
        images.append(img)

    # Determinar o width e height do Surface que criaremos
    w = 0
    h = 0
    for img in images:
        assert isinstance(img, pygame.Surface)
        w = max(w, img.get_width())
        h += img.get_height()

    surf = pygame.Surface((w, h))
    y = 0
    for img in images:
        assert isinstance(img, pygame.Surface)
        surf.blit(img, (0, y))
        y += img.get_height()

    return surf

def draw_text_rectangle(screen, text_list, dest, font=None, text_color = colors.white):
    '''
    Desenha um retângulo preto com o texto em cima. text_list é um list de strings, tal que cada uma vai em uma linha. dest é o topleft do retângulo
    '''
    assert isinstance(screen, pygame.Surface)

    surf = _text_drawing_rectangle_image(text_list, font, text_color)

    screen.blit(surf, (dest[0], dest[1]))

def draw_text_rectangle_center(screen, text_list, dest_center, font=None, text_color = colors.white):
    '''
    Desenha um retângulo preto com o texto em cima. text_list é um list de strings, tal que cada uma vai em uma linha. dest_center é o centro do retângulo
    '''
    assert isinstance(screen, pygame.Surface)

    surf = _text_drawing_rectangle_image(text_list, font, text_color)

    w = surf.get_width()
    h = surf.get_height()
    left = dest_center[0] - w/2
    top = dest_center[1] - h/2

    screen.blit(surf, (left, top))