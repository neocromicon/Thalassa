import pygame
import sys
from data.scripts.GUI.OptionsKeyboard import OptionsKeyboard
from data.scripts.GUI.OptionsMouse import OptionsMouse
from data.scripts.GUI.OptionsVideo import OptionsVideo
from data.scripts.Managers.MenuManager import MenuManager
from data.scripts.Constants import BACKGROUND_PICTURE, FONT_BIG, FONT_INT_BIG, FONT_UNSELECTED_COLOR, FONT_SELECTED_COLOR, FONT_SHADOW_COLOR, FONT_TITLE_COLOR
from data.scripts.GUI.OptionsLanguage import OptionsLanguage
from data.scripts.MapGenerator.Settings import SCREEN_WIDTH, SCREEN_HEIGHT
from data.scripts.Managers.LanguageManager import LANGUAGE_MANAGER, BACK, OPTIONS_TITLE, SELECT_LANGUAGE, SELECT_VIDEO, SELECT_MOUSE, SELECT_KEYBOARD

class OptionsMenu:
    def __init__(self, screen, game_instance):
        """Initialisiert das Optionsmenü."""
        self.screen = screen
        self.game = game_instance
        self.font = pygame.font.Font(FONT_BIG, FONT_INT_BIG)
        # Sprachmanager initialisieren
        self.lang = LANGUAGE_MANAGER  # Sprache auf Deutsch setzen
        # Sprachschlüssel für die Optionen definieren
        self.options = [
            self.lang.get(SELECT_VIDEO),
            self.lang.get(SELECT_MOUSE),
            self.lang.get(SELECT_KEYBOARD),
            self.lang.get(SELECT_LANGUAGE),
            self.lang.get(BACK)
        ]
        # Visuelle Einstellungen für Menüauswahl
        self.selected_index = 0
        self.text_color = FONT_UNSELECTED_COLOR
        self.highlight_color = FONT_SELECTED_COLOR
        # Hintergrund und Rahmen des Menüs laden
        self.background_image = MenuManager.load_background(BACKGROUND_PICTURE)

    def run(self):
        """Startet das Optionsmenü und verarbeitet Benutzereingaben."""
        running = True
        while running:
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
                        if self.selected_index == len(self.options) - 1:  # Back Option
                            running = False
                    elif event.key == pygame.K_ESCAPE:
                        running = False
                elif event.type == pygame.MOUSEMOTION:
                    mouse_x, mouse_y = pygame.mouse.get_pos()
                    for index, option_rect in enumerate(self.menu_positions):
                        if option_rect.collidepoint(mouse_x, mouse_y):
                            self.selected_index = index  # Maus bewegt sich über Menüpunkt
                elif event.type == pygame.MOUSEBUTTONDOWN:
                    if event.button == 1:  # Linksklick
                        self.handle_selection()
                    if event.button == 3:  # Rechtsklick
                        running = False

    # -----------------------------------
    # Menü und Rahmen Zeichnen
    # -----------------------------------
    def draw_menu(self):
        """Zeichnet das Optionsmenü mit Schatteneffekt für den Text."""
        num_options = len(self.options)
        option_spacing = 50  # Abstand zwischen den Optionen
        padding_top_bottom = 60  # Abstand oben und unten

        title_text = self.lang.get(OPTIONS_TITLE)
        title_surface = self.font.render(title_text, True, self.text_color)
        menu_height = num_options * option_spacing + padding_top_bottom + title_surface.get_height()

        # Runde die Höhe auf das nächste Vielfache von 16
        if menu_height % 16 != 0:
            menu_height += 16 - (menu_height % 16)

        ## Box Weite berechnen
        title_text_width = self.font.size(self.lang.get(SELECT_VIDEO))[0]
        change_text_width = self.font.size(self.lang.get(SELECT_MOUSE))[0]
        restart_text_width = self.font.size(self.lang.get(SELECT_LANGUAGE))[0]
        max_text_width = max(title_text_width, change_text_width, restart_text_width)

        min_width = 400
        padding_sides = 100
        menu_width = max(max_text_width + padding_sides, min_width)

        # Runde die Breite auf das nächste Vielfache von 16
        if menu_width % 16 != 0:
            menu_width += 16 - (menu_width % 16)
            
        # Menü zentrieren
        menu_x = (SCREEN_WIDTH - menu_width) // 2
        menu_y = (SCREEN_HEIGHT - menu_height) // 2

        if self.background_image:
            self.screen.blit(pygame.transform.scale(self.background_image, (SCREEN_WIDTH, SCREEN_HEIGHT)), (0, 0))

        MenuManager.draw_window_border(self.screen)
        MenuManager.draw_boarder(self.screen, (menu_x, menu_y, menu_width, menu_height))

        # Zeichne Titel mit Schatten
        MenuManager.draw_text_with_soft_shadow_title(self, title_text, SCREEN_WIDTH // 2, menu_y + 40, FONT_TITLE_COLOR)

        # **Menüpositionen für Maussteuerung speichern**
        self.menu_positions = []

        # Zeichne Menüoptionen mit Schatten
        for index, option in enumerate(self.options):
            color = self.highlight_color if index == self.selected_index else self.text_color
            option_y = menu_y + 100 + index * option_spacing
            MenuManager.draw_text_with_soft_shadow(self, option, SCREEN_WIDTH // 2, option_y, color)

            # Rechtecke der Menüoptionen speichern für Mausinteraktion
            option_rect = pygame.Rect(SCREEN_WIDTH // 2 - 100, option_y - 20, 200, 40)
            self.menu_positions.append(option_rect)

    # -----------------------------------
    # Benutzeraktionen Verarbeiten
    # -----------------------------------
    def handle_selection(self):
        """Verarbeitet die Auswahl im Optionsmenü."""
        selected_option = self.options[self.selected_index]
        if selected_option == self.lang.get(SELECT_VIDEO):
            video_menu = OptionsVideo(self.screen, self.game)
            video_menu.run()

        if selected_option == self.lang.get(SELECT_MOUSE):
            mouse_menu = OptionsMouse(self.screen, self.game)
            mouse_menu.run()    

        if selected_option == self.lang.get(SELECT_KEYBOARD):
            keyboard_menu = OptionsKeyboard(self.screen, self.game)
            keyboard_menu.run() 

        if selected_option == self.lang.get(SELECT_LANGUAGE):
            language_menu = OptionsLanguage(self.screen, self.game)
            language_menu.run()

        elif selected_option == self.lang.get(BACK):
            print("Zurück ins Hauptmenü.")
