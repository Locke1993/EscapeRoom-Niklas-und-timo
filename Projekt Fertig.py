import pygame
import sys
import random

# Initialisiere Pygame
pygame.init()

# Fenstergröße und Titel
WIDTH, HEIGHT = 800, 600
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Weltraum Escape Room")

# Farben
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
RED = (255, 0, 0)

# Spielzustände und Variablen
class GameState:
    def __init__(self):
        self.current_scene = "title"  # Startszene ist der Titelbildschirm
        self.solved_puzzle_1 = False  # Minispiel 1 ist noch nicht gelöst
        self.solved_puzzle_2 = False  # Minispiel 2 ist noch nicht gelöst
        self.has_key = False  # Schlüssel noch nicht gefunden
        self.story_told = False  # Story wurde noch nicht erzählt

    def change_scene(self, scene_name):
        self.current_scene = scene_name

    def all_puzzles_solved(self):
        return self.solved_puzzle_1 and self.solved_puzzle_2


game_state = GameState()

# Lade das Titelbild und das Raumschiff-Bild
title_image = pygame.image.load('title_image.jpg')
title_image = pygame.transform.scale(title_image, (600, 400))  # Bildgröße anpassen
spaceship_image = pygame.image.load('ship_image.png')  # Raumschiff-Bild laden
spaceship_image = pygame.transform.scale(spaceship_image, (30, 30))  # Größe des Raumschiffs anpassen
background_number_sort_image = pygame.image.load('number_sort_background.jpg')
background_number_sort_image = pygame.transform.scale(background_number_sort_image, (600, 400))
background_labyrinth_image = pygame.image.load('labyrinth_background.jpg')
background_labyrinth_image = pygame.transform.scale(background_labyrinth_image, (600, 400))
room_background_image = pygame.image.load('room_background.jpg')
room_background_image = pygame.transform.scale(room_background_image, (WIDTH, HEIGHT))

# Hauptschleife
def main():
    clock = pygame.time.Clock()

    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()

            if event.type == pygame.MOUSEBUTTONDOWN:
                handle_click(event.pos)

            if event.type == pygame.KEYDOWN and game_state.current_scene == "story":
                # Wenn eine Taste gedrückt wird, geht es weiter zum Hauptspiel
                game_state.change_scene("room")

        # Szene zeichnen
        if game_state.current_scene == "title":
            draw_title_scene()
        elif game_state.current_scene == "story":
            draw_story_scene()
        elif game_state.current_scene == "room":
            draw_room_scene()
        elif game_state.current_scene == "win":
            draw_win_scene()

        pygame.display.flip()
        clock.tick(30)


# Szenen und Interaktionen
def draw_title_scene():
    screen.fill(BLACK)
    font = pygame.font.SysFont(None, 55)

    # Titeltext
    text = font.render('Willkommen zum Weltraum Escape Room', True, WHITE)
    screen.blit(text, (50, 50))

    # Titelbild
    screen.blit(title_image, (200, 150))

    # Aufforderung zum Starten
    start_text = font.render('Klicke, um zu starten', True, WHITE)
    screen.blit(start_text, (250, 500))

def draw_story_scene():
    screen.fill(BLACK)
    font = pygame.font.SysFont(None, 45)

    # Geschichte anzeigen
    story_text = [
        "Du bist der letzte Überlebende einer Weltraummission.",
        "Dein Raumschiff wurde beschädigt, und du musst entkommen.",
        "Löse die Rätsel, um den Ausgang zu finden.",
        "Drücke eine beliebige Taste, um das Abenteuer zu beginnen!"
    ]

    # Zeige jede Zeile der Geschichte an
    for i, line in enumerate(story_text):
        text = font.render(line, True, WHITE)
        screen.blit(text, (50, 100 + i * 60))

def draw_room_scene():
    # Zeichne das Hintergrundbild zuerst
    screen.blit(room_background_image, (0, 0))
    font = pygame.font.SysFont(None, 55)
    small_font = pygame.font.SysFont(None, 35)

    # Zeichne das Panel
    panel_rect = pygame.Rect(300, 400, 200, 100)
    pygame.draw.rect(screen, WHITE, panel_rect)
    panel_text = small_font.render('Panel', True, BLACK)
    screen.blit(panel_text, (panel_rect.x + 50, panel_rect.y + 35))

    # Zeichne die Tür
    door_rect = pygame.Rect(650, 250, 100, 200)
    pygame.draw.rect(screen, WHITE, door_rect)
    door_text = small_font.render('Tür', True, BLACK)
    screen.blit(door_text, (door_rect.x + 20, door_rect.y + 80))

    # Falls beide Puzzle gelöst wurden, zeige den Schlüssel an
    if game_state.all_puzzles_solved():
        key_rect = pygame.Rect(100, 400, 100, 50)
        pygame.draw.rect(screen, WHITE, key_rect)
        key_text = small_font.render('Schlüssel', True, BLACK)
        screen.blit(key_text, (key_rect.x + 10, key_rect.y + 10))

def draw_win_scene():
    screen.fill(BLACK)
    font = pygame.font.SysFont(None, 55)
    win_text = font.render('Du bist entkommen!', True, WHITE)
    screen.blit(win_text, (200, 250))


def handle_click(position):
    if game_state.current_scene == "title":
        game_state.change_scene("story")
    elif game_state.current_scene == "room":
        # Interaktion mit dem Panel (Minispiele starten)
        if pygame.Rect(300, 400, 200, 100).collidepoint(position):
            if not game_state.solved_puzzle_1:
                game_state.solved_puzzle_1 = play_number_sort_game()
            elif not game_state.solved_puzzle_2:
                game_state.solved_puzzle_2 = play_another_minigame()

        # Interaktion mit der Tür
        elif pygame.Rect(650, 250, 100, 200).collidepoint(position):
            if game_state.has_key:
                game_state.change_scene("win")
            else:
                print("Die Tür ist verschlossen.")

        # Interaktion mit dem Schlüssel (nachdem das Puzzle gelöst ist)
        elif game_state.all_puzzles_solved() and pygame.Rect(100, 400, 100, 50).collidepoint(position):
            game_state.has_key = True
            print("Du hast den Schlüssel gefunden!")

# Minispiel 1: Zahlen aufsteigend sortieren
def play_number_sort_game():
    popup = pygame.display.set_mode((600, 400))  # Popup-Fenster erstellen
    pygame.display.set_caption("Minispiel: Zahlen sortieren")

    # Lade das Asteroiden-Bild
    asteroid_image = pygame.image.load('asteroid.png')  # Pfad zu deinem Asteroidenbild
    asteroid_image = pygame.transform.scale(asteroid_image, (70, 70))  # Asteroiden-Bildgröße anpassen

    # 10 zufällige Zahlen zwischen 1 und 100
    unsorted_numbers = random.sample(range(1, 101), 10)  # Unsortierte Liste für die Anzeige
    sorted_numbers = sorted(unsorted_numbers)  # Sortierte Liste für den Vergleich
    current_number_index = 0  # Index des aktuellen Zielwerts in der sortierten Liste

    # Erzeuge zufällige Positionen, die sich nicht überlappen
    positions = []
    while len(positions) < 10:
        pos = (random.randint(50, 550), random.randint(50, 350))
        rect = pygame.Rect(pos[0], pos[1], 50, 50)

        # Prüfe, ob sich die neue Position mit einer bestehenden überschneidet
        if not any(r.colliderect(rect) for r in [pygame.Rect(p[0], p[1], 50, 50) for p in positions]):
            positions.append(pos)

    font = pygame.font.SysFont(None, 50)
    error_message = ""  # Fehlernachricht
    error_timer = 0  # Timer für Fehlermeldung

    while unsorted_numbers:
        popup.blit(background_number_sort_image, (0, 0))  # Hintergrundbild zeichnen

        # Ereignisbehandlung
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            if event.type == pygame.MOUSEBUTTONDOWN:
                # Überprüfen, ob eine Zahl angeklickt wurde
                for i, pos in enumerate(positions):
                    rect = pygame.Rect(pos[0], pos[1], 50, 50)
                    if rect.collidepoint(event.pos):
                        # Überprüfen, ob die geklickte Zahl der nächsten Zahl in der sortierten Liste entspricht
                        if unsorted_numbers[i] == sorted_numbers[current_number_index]:
                            del unsorted_numbers[i]  # Zahl entfernen
                            del positions[i]  # Position ebenfalls entfernen
                            current_number_index += 1  # Erhöhe den Index für die nächste Zahl
                            error_message = ""  # Fehlermeldung zurücksetzen
                        else:
                            # Fehlermeldung bei falscher Zahl
                            error_message = f"Falsche Zahl! Die richtige Zahl ist: {sorted_numbers[current_number_index]}"
                            error_timer = pygame.time.get_ticks()  # Setze Timer für Fehlermeldung
                        break

        # Zeichne die verbleibenden Zahlen auf Asteroiden
        for i, num in enumerate(unsorted_numbers):
            popup.blit(asteroid_image, positions[i])  # Zeichne den Asteroiden
            text = font.render(str(num), True, WHITE)
            popup.blit(text, (positions[i][0] + 10, positions[i][1] + 10))  # Zeichne die Zahl auf den Asteroiden

        # Fehlermeldung anzeigen, falls vorhanden, und für eine Weile anzeigen
        if error_message:
            error_font = pygame.font.SysFont(None, 35)
            error_text = error_font.render(error_message, True, RED)
            popup.blit(error_text, (150, 350))

            # Fehlermeldung nach 2 Sekunden entfernen
            if pygame.time.get_ticks() - error_timer > 2000:
                error_message = ""

        pygame.display.flip()  # Bildschirm aktualisieren
        pygame.time.Clock().tick(30)  # Bildwiederholrate

    # Wenn alle Zahlen korrekt angeklickt wurden
    pygame.display.set_mode((WIDTH, HEIGHT))  # Zurück zum Hauptfenster
    return True  # Minispiel abgeschlossen


# Minispiel 2: Labyrinthspiel
def play_another_minigame():
    popup = pygame.display.set_mode((600, 400))  # Popup-Fenster erstellen
    pygame.display.set_caption("Minispiel: Labyrinth")

    # Einfacheres Labyrinth mit größeren Gängen
    walls = [
        pygame.Rect(50, 50, 500, 10),  # Obere Wand
        pygame.Rect(50, 50, 10, 400),  # Linke Wand
        pygame.Rect(50, 440, 500, 10),  # Untere Wand
        pygame.Rect(540, 50, 10, 400),  # Rechte Wand

        # Angepasste Labyrinthwände
        pygame.Rect(250, 50, 10, 300),   # Mittlere vertikale Wand links
        pygame.Rect(350, 150, 10, 300),  # Mittlere vertikale Wand rechts
        pygame.Rect(450, 50, 10, 300),   # Rechte vertikale Wand
        pygame.Rect(150, 100, 300, 10),  # Horizontale Wand oben
        pygame.Rect(100, 300, 200, 10),  # Horizontale Wand unten links
    ]

    # Zielposition
    goal_rect = pygame.Rect(520, 360, 40, 40)  # Ziel in der rechten unteren Ecke

    # Startposition des Raumschiffs (kleiner gemacht)
    spaceship_rect = pygame.Rect(80, 80, 30, 30)  # Kleinere Größe für das Raumschiff
    spaceship_speed = 5

    font = pygame.font.SysFont(None, 50)

    clock = pygame.time.Clock()

    while True:
        popup.blit(background_labyrinth_image, (0, 0))  # Hintergrundbild zeichnen

        # Ereignisse abfragen (Schließen des Fensters)
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()

        # Tastenstatus abfragen
        keys = pygame.key.get_pressed()
        if keys[pygame.K_UP]:
            spaceship_rect.y -= spaceship_speed
        if keys[pygame.K_DOWN]:
            spaceship_rect.y += spaceship_speed
        if keys[pygame.K_LEFT]:
            spaceship_rect.x -= spaceship_speed
        if keys[pygame.K_RIGHT]:
            spaceship_rect.x += spaceship_speed

        # Überprüfen, ob das Raumschiff eine Wand berührt
        for wall in walls:
            if spaceship_rect.colliderect(wall):
                spaceship_rect.topleft = (80, 80)  # Zurücksetzen zum Start

        # Überprüfen, ob das Raumschiff das Ziel erreicht
        if spaceship_rect.colliderect(goal_rect):
            pygame.display.set_mode((WIDTH, HEIGHT))  # Zurück zum Hauptfenster
            return True  # Minispiel abgeschlossen

        # Zeichne Wände
        for wall in walls:
            pygame.draw.rect(popup, (255, 255, 255), wall)  # Weiße Wände

        # Zeichne Ziel
        pygame.draw.rect(popup, (255, 0, 0), goal_rect)  # Rotes Ziel

        # Zeichne Raumschiff
        popup.blit(spaceship_image, spaceship_rect)

        pygame.display.flip()
        clock.tick(30)  # Spielgeschwindigkeit


if __name__ == "__main__":
    main()