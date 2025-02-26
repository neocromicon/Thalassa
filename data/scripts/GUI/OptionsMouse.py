import pygame
import sys
from data.scripts.Managers.MenuManager import MenuManager
from data.scripts.Constants import BACKGROUND_PICTURE, FONT_BIG, FONT_INT_BIG, FONT_TITLE_COLOR
from data.scripts.Managers.SettingsManager import SettingsManager
from data.scripts.MapGenerator.Settings import SCREEN_WIDTH, SCREEN_HEIGHT
from data.scripts.Managers.LanguageManager import LANGUAGE_MANAGER, MOUSE_INVERT, MOUSE_SENSITIVITY, MOUSE_ZOOM_SENSITIVITY, BACK, MOUSE_TITLE, ON, OFF

class OptionsMouse:
    def __init__(self, screen, game_instance):
        """Initialisiert das Maus-Einstellungsmenü."""
        self.screen = screen
        self.game = game_instance
        self.font = pygame.font.Font(FONT_BIG, FONT_INT_BIG)
        self.lang = LANGUAGE_MANAGER  # Sprachmanager

        # Maus-Einstellungen aus settings.json laden
        self.mouse_sensitivity = SettingsManager.load_setting("mouse_sensitivity", 1.0)
        self.mouse_invert = SettingsManager.load_setting("mouse_invert", False)
        self.mouse_zoom_sensitivity = SettingsManager.load_setting("mouse_zoom_sensitivity", 1.0)

        # Sprachschlüssel für die Optionen definieren
        self.options = [
            f"{self.lang.get(MOUSE_SENSITIVITY)}: {self.mouse_sensitivity:.1f}",
            f"{self.lang.get(MOUSE_INVERT)}: {self.lang.get(ON) if self.mouse_invert else self.lang.get(OFF)}",
            f"{self.lang.get(MOUSE_ZOOM_SENSITIVITY)}: {self.mouse_zoom_sensitivity:.1f}",
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

        title_text = self.lang.get(MOUSE_TITLE)
        title_surface = self.font.render(title_text, True, self.text_color)
        menu_height = num_options * option_spacing + padding_top_bottom + title_surface.get_height()

        if menu_height % 16 != 0:
            menu_height += 16 - (menu_height % 16)

        ## Box Weite berechnen
        mouse_sensitivity_text_width = self.font.size(self.lang.get(MOUSE_SENSITIVITY))[0]
        mouse_invert_text_width = self.font.size(self.lang.get(MOUSE_INVERT))[0]
        mouse_zoom_text_width = self.font.size(self.lang.get(MOUSE_ZOOM_SENSITIVITY))[0]
        max_text_width = max(mouse_sensitivity_text_width, mouse_invert_text_width, mouse_zoom_text_width)

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
            self.mouse_sensitivity = max(0.1, min(5.0, self.mouse_sensitivity + change))
            self.options[0] = f"{self.lang.get(MOUSE_SENSITIVITY)}: {self.mouse_sensitivity:.1f}"
            SettingsManager.update_settings("mouse_sensitivity", self.mouse_sensitivity)

        elif self.selected_index == 1:  # Maus-Invertierung
            if key in (pygame.K_LEFT, pygame.K_RIGHT):
                self.mouse_invert = not self.mouse_invert
                self.options[1] = f"{self.lang.get(MOUSE_INVERT)}: {self.lang.get(ON) if self.mouse_invert else self.lang.get(OFF)}"
                SettingsManager.update_settings("mouse_invert", self.mouse_invert)

        elif self.selected_index == 2:  # Scrollgeschwindigkeit
            change = 0.1 if key == pygame.K_RIGHT else -0.1
            self.mouse_zoom_sensitivity = max(0.1, min(5.0, self.mouse_zoom_sensitivity + change))
            self.options[2] = f"{self.lang.get(MOUSE_ZOOM_SENSITIVITY)}: {self.mouse_zoom_sensitivity:.1f}"
            SettingsManager.update_settings("mouse_zoom_sensitivity", self.mouse_zoom_sensitivity)

    def handle_selection(self):
        """Verarbeitet die Auswahl im Mausmenü."""
        selected_option = self.options[self.selected_index]

        if self.selected_index == 0:  # Empfindlichkeit anpassen
            new_sensitivity = round(SettingsManager.load_setting("mouse_sensitivity", 1.0) + 0.1, 1)
            SettingsManager.update_settings("mouse_sensitivity", new_sensitivity)
            self.options[0] = self.lang.get(MOUSE_SENSITIVITY) + f": {new_sensitivity}"

        elif self.selected_index == 1:  # Invertierung umschalten
            new_invert = not SettingsManager.load_setting("mouse_invert", False)
            SettingsManager.update_settings("mouse_invert", new_invert)
            self.options[1] = self.lang.get(MOUSE_INVERT) + f": {'Ja' if new_invert else 'Nein'}"

        elif self.selected_index == 2:  # Scrollgeschwindigkeit anpassen
            new_scroll = round(SettingsManager.load_setting("mouse_zoom_sensitivity", 1.0) + 0.1, 1)
            SettingsManager.update_settings("mouse_zoom_sensitivity", new_scroll)
            self.options[2] = self.lang.get(MOUSE_ZOOM_SENSITIVITY) + f": {new_scroll}"

        elif selected_option == self.lang.get(BACK):
            print("Zurück ins Hauptmenü.")
