import pygame

# Initialiser Pygame
pygame.init()

# Definer vindusstørrelse
BREDDE = 800
HØYDE = 600

# Opprett vinduet
vindu = pygame.display.set_mode((BREDDE, HØYDE))
pygame.display.set_caption("Grønt Vindu")

# Definer grønn farge (RGB-verdier)
GRØNN = (0, 255, 0)

# Hovedløkke
kjører = True
while kjører:
    for hendelse in pygame.event.get():
        if hendelse.type == pygame.QUIT:
            kjører = False
    
    # Fyll vinduet med grønn farge
    vindu.fill(GRØNN)
    
    # Oppdater skjermen
    pygame.display.flip()

# Avslutt Pygame
pygame.quit()


