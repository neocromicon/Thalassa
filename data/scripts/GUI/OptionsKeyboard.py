import pygame
import sys
from data.scripts.Managers.MenuManager import MenuManager
from data.scripts.Constants import BACKGROUND_PICTURE, FONT_BIG, FONT_INT_BIG, FONT_TITLE_COLOR
from data.scripts.Managers.SettingsManager import SettingsManager
from data.scripts.MapGenerator.Settings import SCREEN_WIDTH, SCREEN_HEIGHT
from data.scripts.Managers.LanguageManager import KEYBOARD_INVERT, KEYBOARD_SENSITIVITY, KEYBOARD_TITLE, KEYBOARD_ZOOM_SENSITIVITY, LANGUAGE_MANAGER, BACK, MOUSE_TITLE, ON, OFF

class OptionsKeyboard:
    def __init__(self, screen, game_instance):
        """Initialisiert das Maus-Einstellungsmenü."""
        self.screen = screen
        self.game = game_instance
        self.font = pygame.font.Font(FONT_BIG, FONT_INT_BIG)
        self.lang = LANGUAGE_MANAGER  # Sprachmanager

        # Maus-Einstellungen aus settings.json laden
        self.keyboard_sensitivity = SettingsManager.load_setting("keyboard_sensitivity", 0.5)
        self.keyboard_invert= SettingsManager.load_setting("keyboard_invert", False)
        self.keyboard_zoom_sensitivity = SettingsManager.load_setting("keyboard_zoom_sensitivity", 0.1)

        # Sprachschlüssel für die Optionen definieren
        self.options = [
            f"{self.lang.get(KEYBOARD_SENSITIVITY)}: {self.keyboard_sensitivity:.1f}",
            f"{self.lang.get(KEYBOARD_INVERT)}: {self.lang.get(ON) if self.keyboard_invert else self.lang.get(OFF)}",
            f"{self.lang.get(KEYBOARD_ZOOM_SENSITIVITY)}: {self.keyboard_zoom_sensitivity:.1f}",
            self.lang.get(BACK)
        ]

        # Visuelle Einstellungen für Menüauswahl
        self.selected_index = 0
        self.text_color = (255, 255, 255)
        self.highlight_color = (200, 150, 50)

        # Hintergrund und Rahmen des Menüs laden
        self.background_image = MenuManager.load_background(BACKGROUND_PICTURE)

    def run(self):
        """Startet das Maus-Einstellungsmenü und verarbeitet Benutzereingaben."""
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
                    elif event.key in (pygame.K_LEFT, pygame.K_RIGHT):
                        self.adjust_setting(event.key)
                    elif event.key == pygame.K_RETURN:
                        self.handle_selection()
                        if self.selected_index == len(self.options) - 1:  # BACK-Option
                            running = False
                    elif event.key == pygame.K_ESCAPE:
                        running = False                            

    def draw_menu(self):
        """Zeichnet das Menü für die Mauseinstellungen."""
        num_options = len(self.options)
        option_spacing = 50
        padding_top_bottom = 60

        title_text = self.lang.get(KEYBOARD_TITLE)
        title_surface = self.font.render(title_text, True, self.text_color)
        menu_height = num_options * option_spacing + padding_top_bottom + title_surface.get_height()

        if menu_height % 16 != 0:
            menu_height += 16 - (menu_height % 16)

        ## Box Weite berechnen
        keyboard_sensitivity_text_width = self.font.size(self.lang.get(KEYBOARD_SENSITIVITY))[0]
        keyboard_invert_text_width = self.font.size(self.lang.get(KEYBOARD_INVERT))[0]
        keyboard_zoom_text_width = self.font.size(self.lang.get(KEYBOARD_ZOOM_SENSITIVITY))[0]
        max_text_width = max(keyboard_sensitivity_text_width, keyboard_invert_text_width, keyboard_zoom_text_width)

        min_width = 400
        padding_sides = 100
        menu_width = max(max_text_width + padding_sides, min_width)

        if menu_width % 16 != 0:
            menu_width += 16 - (menu_width % 16)

        menu_x = (SCREEN_WIDTH - menu_width) // 2
        menu_y = (SCREEN_HEIGHT - menu_height) // 2

        if self.background_image:
            self.screen.blit(pygame.transform.scale(self.background_image, (SCREEN_WIDTH, SCREEN_HEIGHT)), (0, 0))

        MenuManager.draw_window_border(self.screen)
        MenuManager.draw_boarder(self.screen, (menu_x, menu_y, menu_width, menu_height))

        # Zeichne Titel mit Schatten
        MenuManager.draw_text_with_soft_shadow_title(self, title_text, SCREEN_WIDTH // 2, menu_y + 40, FONT_TITLE_COLOR)

        # Zeichne Menüoptionen mit Schatten
        for index, option in enumerate(self.options):
            color = self.highlight_color if index == self.selected_index else self.text_color
            option_y = menu_y + 100 + index * option_spacing
            MenuManager.draw_text_with_soft_shadow(self, option, SCREEN_WIDTH // 2, option_y, color)

    def adjust_setting(self, key):
        """Passt die Maus-Einstellungen an."""
        if self.selected_index == 0:  # Mausempfindlichkeit
            change = 0.1 if key == pygame.K_RIGHT else -0.1
            self.keyboard_sensitivity = max(0.1, min(5.0, self.keyboard_sensitivity + change))
            self.options[0] = f"{self.lang.get(KEYBOARD_SENSITIVITY)}: {self.keyboard_sensitivity:.1f}"
            SettingsManager.update_settings("keyboard_sensitivity", self.keyboard_sensitivity)

        elif self.selected_index == 1:  # Maus-Invertierung
            if key in (pygame.K_LEFT, pygame.K_RIGHT):
                self.keyboard_invert = not self.keyboard_invert
                self.options[1] = f"{self.lang.get(KEYBOARD_INVERT)}: {self.lang.get(ON) if self.keyboard_invert else self.lang.get(OFF)}"
                SettingsManager.update_settings("keyboard_invert", self.keyboard_invert)

        elif self.selected_index == 2:  # Scrollgeschwindigkeit
            change = 0.1 if key == pygame.K_RIGHT else -0.1
            self.keyboard_zoom_sensitivity = max(0.1, min(5.0, self.keyboard_zoom_sensitivity + change))
            self.options[2] = f"{self.lang.get(KEYBOARD_ZOOM_SENSITIVITY)}: {self.keyboard_zoom_sensitivity:.1f}"
            SettingsManager.update_settings("keyboard_zoom_sensitivity", self.keyboard_zoom_sensitivity)

    def handle_selection(self):
        """Verarbeitet die Auswahl im Mausmenü."""
        selected_option = self.options[self.selected_index]
        if selected_option == self.lang.get(BACK):
            print("Zurück ins Hauptmenü.")
