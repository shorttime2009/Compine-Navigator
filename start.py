import pygame
import sys
import time
from PIL import ImageGrab  # Pour capturer l'écran
import subprocess  # Pour exécuter un autre script

# Initialisation de Pygame
pygame.init()

# Capturer l'arrière-plan actuel de l'écran
background = ImageGrab.grab()
background = background.convert("RGB")
screen_width, screen_height = background.size

# Charger l'image capturée comme surface de fond
background_surface = pygame.image.fromstring(
    background.tobytes(), background.size, background.mode
)

# Configuration de l'écran en plein écran
screen = pygame.display.set_mode((screen_width, screen_height), pygame.NOFRAME)
pygame.mouse.set_visible(False)

# Couleurs et police
WHITE = (255, 255, 255)
font = pygame.font.Font(None, 200)  # Taille de la police
text = "Compine"

# Fonction principale
def main():
    clock = pygame.time.Clock()
    display_text = ""
    alpha = 255  # Opacité initiale
    letter_index = 0  # Index pour l'animation d'écriture

    # Animation d'écriture
    while letter_index <= len(text):
        screen.blit(background_surface, (0, 0))  # Afficher l'arrière-plan

        # Ajouter une lettre à chaque itération
        display_text = text[:letter_index]
        text_surface = font.render(display_text, True, WHITE)
        text_rect = text_surface.get_rect(center=(screen_width // 2, screen_height // 2))
        screen.blit(text_surface, text_rect)

        pygame.display.update()
        time.sleep(0.2)  # Délai entre chaque lettre
        letter_index += 1

    # Animation de fade-out
    while alpha > 0:
        screen.blit(background_surface, (0, 0))  # Afficher l'arrière-plan

        # Appliquer une transparence au texte
        text_surface = font.render(text, True, WHITE)
        text_surface.set_alpha(alpha)
        text_rect = text_surface.get_rect(center=(screen_width // 2, screen_height // 2))
        screen.blit(text_surface, text_rect)

        pygame.display.update()
        alpha -= 5  # Réduire l'opacité
        time.sleep(0.05)  # Vitesse de fade-out

    pygame.quit()

    # Lancer le script Compine.py après l'animation
    subprocess.run(["python", "_main/Compine.py"])

# Exécuter le script
if __name__ == "__main__":
    main()
