import pygame
import sys

# Initialiser Pygame
pygame.init()

# Définir la taille de la fenêtre
screen = pygame.display.set_mode((600, 400))
pygame.display.set_caption("Afficher du texte avec Pygame")

# Définir une couleur
blanc = (255, 255, 255)
noir = (0, 0, 0)

# Charger une police et définir la taille
# None = police par défaut du système
police = pygame.font.Font(None, 48)  # 48 = taille du texte

# Créer une surface contenant le texte
texte = police.render("Bonjour Pygame !", True, noir)

# Obtenir le rectangle du texte pour le centrer par exemple
texte_rect = texte.get_rect(center=(300, 200))

# Boucle principale
running = True
while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

    screen.fill(blanc)  # remplir l'écran en blanc
    screen.blit(texte, texte_rect)  # dessiner le texte
    pygame.display.flip()  # mettre à jour l'écran

pygame.quit()
sys.exit()
