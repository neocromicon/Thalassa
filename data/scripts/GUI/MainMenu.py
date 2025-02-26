import pygame
import sys
from data.scripts.GUI.OptionsGenerator import OptionsGenerator
from data.scripts.Managers.SaveManager import SaveManager
from data.scripts.GUI.OptionsMenu import OptionsMenu
from data.scripts.Managers.MenuManager import MenuManager
from data.scripts.Constants import BACKGROUND_PICTURE, FONT_BIG, FONT_INT_BIG
from data.scripts.MapGenerator.Settings import SCREEN_WIDTH, SCREEN_HEIGHT
from data.scripts.GUI.MainIngameMenu import MainIngameMenu
from data.scripts.Managers.LanguageManager import  LanguageManagerHelper, LANGUAGE_MANAGER, NEW_GAME, LOAD_GAME, ACTION_LOAD_GAME, OPTIONS, CREDITS, EXIT

# ------------------------------------------
# Hauptmenü-Klasse für das Spiel
# ------------------------------------------
class MainMenu:
    def __init__(self, screen, game_instance):
        """Initialisiert das Hauptmenü mit Bildschirm und Spielinstanz."""
        self.screen = screen
        self.game = game_instance
        self.start_game = False
        # Schriftart und Menüoptionen definieren
        self.font = pygame.font.Font(FONT_BIG, FONT_INT_BIG)
        # Sprachmanager initialisieren
        self.lang = LANGUAGE_MANAGER
        # Savemanager initialisieren
        self.save_manager = SaveManager(self.lang)
        # Sprachschlüssel für die Optionen definieren
        self.options = [
            self.lang.get(NEW_GAME),
            self.lang.get(LOAD_GAME),
            self.lang.get(OPTIONS),
            self.lang.get(CREDITS),
            self.lang.get(EXIT)
        ]
        # Visuelle Einstellungen für Menüauswahl
        self.selected_index = 0
        self.text_color = (255, 255, 255)
        self.highlight_color = (200, 150, 50)
        # Hintergrund und Rahmen des Menüs laden
        self.background_image = MenuManager.load_background(BACKGROUND_PICTURE)
        # Instanz von MainIngameMenu erstellen, um den Cache zu verwenden
        self.ingame_menu = MainIngameMenu(self.screen, self.game)

    # -----------------------------------
    # Haupt-Loop des Hauptmenüs
    # -----------------------------------
    def run(self):
        """Startet das Hauptmenü und verarbeitet Benutzereingaben."""
        running = True
        while running and not self.start_game:
            self.draw_menu()
            pygame.display.flip()

            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    sys.exit()
                elif event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_UP:
                        self.selected_index = (self.selected_index - 1) % len(self.options)
                    elif event.key == pygame.K_DOWN:
                        self.selected_index = (self.selected_index + 1) % len(self.options)
                    elif event.key == pygame.K_RETURN:
                        self.handle_selection()
                elif event.type == pygame.MOUSEMOTION:
                    mouse_x, mouse_y = pygame.mouse.get_pos()
                    for index, option_rect in enumerate(self.menu_positions):
                        if option_rect.collidepoint(mouse_x, mouse_y):
                            self.selected_index = index  # Maus bewegt sich über Menüpunkt
                elif event.type == pygame.MOUSEBUTTONDOWN:
                    if event.button == 1:  # Linksklick
                        self.handle_selection()
    # -----------------------------------
    # Menü und Rahmen Zeichnen
    # -----------------------------------
    def draw_menu(self):
        # Berechne die minimale Höhe basierend auf der Anzahl der Optionen
        num_options = len(self.options)
        option_spacing = 50  # Abstand zwischen den Optionen
        padding_top_bottom = 60  # Abstand oben und unten
            # **Sprache nach Rückkehr aktualisieren**
        self.lang = LANGUAGE_MANAGER  # Sprache im Hauptmenü aktualisieren

        # **Menüoptionen neu laden**
        menu_height = num_options * option_spacing + padding_top_bottom

        # Runde die Höhe auf das nächste Vielfache von 16
        if menu_height % 16 != 0:
            menu_height += 16 - (menu_height % 16)

        menu_width = 400
        menu_x = (SCREEN_WIDTH - menu_width) // 2
        menu_y = (SCREEN_HEIGHT - menu_height) // 2

        # Hintergrund zeichnen
        if self.background_image:
            self.screen.blit(pygame.transform.scale(self.background_image, (SCREEN_WIDTH, SCREEN_HEIGHT)), (0, 0))

        MenuManager.draw_window_border(self.screen)
        MenuManager.draw_boarder(self.screen, (menu_x, menu_y, menu_width, menu_height))

        # **Menüpositionen für Maussteuerung speichern**
        self.menu_positions = []  

        # Menüoptionen zeichnen            
        for index, option in enumerate(self.options):
            color = self.highlight_color if index == self.selected_index else self.text_color
            option_y = menu_y + 60 + index * option_spacing
            MenuManager.draw_text_with_soft_shadow(self, option, SCREEN_WIDTH // 2, option_y, color)

            # Rechtecke der Menüoptionen speichern für Mausinteraktion
            option_rect = pygame.Rect(SCREEN_WIDTH // 2 - 100, option_y - 20, 200, 40)
            self.menu_positions.append(option_rect)

    # -----------------------------------
    # Benutzeraktionen Verarbeiten
    # -----------------------------------
    def handle_selection(self):
        """Verarbeitet die Auswahl des Spielers im Hauptmenü."""
        selected_option = self.options[self.selected_index]
        if selected_option == self.lang.get(NEW_GAME):
            generator = OptionsGenerator(self.screen)
            generator.run()  # Ruft das Generator-Menü auf, bevor das Spiel startet         
        if selected_option == self.lang.get(LOAD_GAME):
            slot = self.ingame_menu.choose_slot(action=self.lang.get(ACTION_LOAD_GAME))
            if slot:
                if not self.save_manager.save_exists(slot):
                    self.ingame_menu.show_load_error(slot)
                else:
                    self.game.load_game(slot=slot)
                    self.start_game = True
                    
        if selected_option == self.lang.get(OPTIONS):
            options_menu = OptionsMenu(self.screen, self.game)
            options_menu.run()
            
        if selected_option == self.lang.get(EXIT):
            pygame.quit()
            sys.exit()
