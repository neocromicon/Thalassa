import json
import os
import pygame
import sys
from data.scripts.Managers.MenuManager import MenuManager
from data.scripts.Constants import BACKGROUND_PICTURE, FONT_BIG, FONT_INT_BIG, FONT_TITLE_COLOR
from data.scripts.Managers.SettingsManager import SettingsManager
from data.scripts.MapGenerator.Settings import SCREEN_WIDTH, SCREEN_HEIGHT
from data.scripts.Managers.LanguageManager import CHANGE_BOTH_RES_MODE, CHANGE_MODE, CHANGE_RESOLUTION, LANGUAGE_MANAGER, RESTART_GAME, SELECT_MODE, SELECT_MODEFULLSCREEN, SELECT_MODEWINDOWED, SELECT_RESOLUTION, BACK, VIDEO_TITLE

class OptionsVideo:
    def __init__(self, screen, game_instance):
        """Initialisiert das Sprachmenü."""
        self.screen = screen
        self.game = game_instance
        self.font = pygame.font.Font(FONT_BIG, FONT_INT_BIG)
        self.lang = LANGUAGE_MANAGER  # Sprachmanager
        # Verfügbare Auflösungen und Modi
        self.resolutions = [(1366, 768), (1600, 900), (1920, 1080)]
        self.modes = [self.lang.get(SELECT_MODEWINDOWED), self.lang.get(SELECT_MODEFULLSCREEN)]
        # Aktuelle Auflösung aus settings.json laden
        self.current_resolution_index = SettingsManager.load_current_resolution_index(self)
        self.current_modes_index = SettingsManager.load_current_mode_index(self)
        # Speichert ursprüngliche Werte zum Vergleich (für Neustart)
        self.original_resolution_index = self.current_resolution_index
        self.original_modes_index = self.current_modes_index
        # Sprachschlüssel für die Optionen definieren
        self.options = [
            self.lang.get(SELECT_RESOLUTION) + f": {self.get_resolution_text()}",
            self.lang.get(SELECT_MODE) + f": {self.get_mode_text()}",
            self.lang.get(BACK)
        ]
        # Visuelle Einstellungen für Menüauswahl
        self.selected_index = 0
        self.text_color = (255, 255, 255)
        self.highlight_color = (200, 150, 50)
        # Hintergrund und Rahmen des Menüs laden
        self.background_image = MenuManager.load_background(BACKGROUND_PICTURE)

    def get_resolution_text(self):
        """Gibt den Text der aktuellen Auflösung zurück."""
        res = self.resolutions[self.current_resolution_index]
        return f"{res[0]}x{res[1]}"

    def get_mode_text(self):
        """Gibt den Text der aktuellen Auflösung zurück."""
        return self.modes[self.current_modes_index]

    def run(self):
        """Startet das Sprachmenü und verarbeitet Benutzereingaben."""
        running = True
        while running:
            self.draw_menu()
            pygame.display.flip()

            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    sys.exit()
                elif event.type == pygame.KEYDOWN:
                    if event.key in (pygame.K_UP, pygame.K_w):
                        self.selected_index = (self.selected_index - 1) % len(self.options)
                    elif event.key in (pygame.K_DOWN, pygame.K_s):
                        self.selected_index = (self.selected_index + 1) % len(self.options)
                    elif event.key in (pygame.K_LEFT, pygame.K_a, pygame.K_RIGHT, pygame.K_d):
                        self.adjust_setting(event.key)
                    elif event.key == pygame.K_RETURN:
                        self.handle_selection()
                        if self.selected_index == len(self.options) - 1:  # Back Option
                            self.check_and_restart()
                            running = False
                    elif event.key == pygame.K_ESCAPE:
                        running = False
                elif event.type == pygame.MOUSEMOTION:
                    mouse_x, mouse_y = pygame.mouse.get_pos()
                    for index, option_rect in enumerate(self.menu_positions):
                        if option_rect.collidepoint(mouse_x, mouse_y):
                            self.selected_index = index  # Maus bewegt sich über Menüpunkt
                elif event.type == pygame.MOUSEBUTTONDOWN:
                    if event.button == 1:  # Linksklick -> Ändert Einstellung
                        if self.selected_index < len(self.options) - 1:  # "Zurück" nicht ändern
                            self.adjust_setting(pygame.K_RIGHT)
                        else:
                            self.check_and_restart()
                            running = False
                    elif event.button == 3:  # Rechtsklick -> Menü verlassen, Änderungen prüfen
                        self.check_and_restart()
                        running = False

        # -----------------------------------
    # Menü und Rahmen Zeichnen
    # -----------------------------------
    def draw_menu(self):
        """Zeichnet das Optionsmenü mit Mausunterstützung."""
        num_options = len(self.options)
        option_spacing = 50  # Abstand zwischen Optionen
        padding_top_bottom = 60  # Abstand oben und unten

        title_text = self.lang.get(VIDEO_TITLE)
        title_surface = self.font.render(title_text, True, self.text_color)
        menu_height = num_options * option_spacing + padding_top_bottom + title_surface.get_height()

        if menu_height % 16 != 0:
            menu_height += 16 - (menu_height % 16)

        resolution_text = self.lang.get(SELECT_RESOLUTION) + self.get_resolution_text()
        resolution_text_width = self.font.size(resolution_text)[0]
        mode_text = self.lang.get(SELECT_MODE) + self.get_mode_text()
        mode_text_width = self.font.size(mode_text)[0]
        max_text_width = max(resolution_text_width, mode_text_width)

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

        self.menu_positions = []  # Liste für Maus-Interaktion leeren

        MenuManager.draw_text_with_soft_shadow_title(self, title_text, SCREEN_WIDTH // 2, menu_y + 40, FONT_TITLE_COLOR)

        for index, option in enumerate(self.options):
            color = self.highlight_color if index == self.selected_index else self.text_color
            option_y = menu_y + 100 + index * option_spacing
            MenuManager.draw_text_with_soft_shadow(self, option, SCREEN_WIDTH // 2, option_y, color)

            option_rect = pygame.Rect(SCREEN_WIDTH // 2 - 100, option_y - 20, 200, 40)
            self.menu_positions.append(option_rect)  # Rechteck für Maus-Events speichern

    def draw_restart_message(self):
        """Zeigt eine Fehlermeldung, wenn kein Speicherstand für den ausgewählten Slot existiert."""
        # Berechne die minimale Höhe basierend auf der Anzahl der Optionen
        num_options = len(self.options)
        option_spacing = 50  # Abstand zwischen den Optionen
        padding_top_bottom = 60  # Abstand oben und unten
            # **Sprache nach Rückkehr aktualisieren**
        self.lang = LANGUAGE_MANAGER  # Sprache im Hauptmenü aktualisieren

        # **Menüoptionen neu laden**
        menu_height = num_options * option_spacing + padding_top_bottom - 60

        # Runde die Höhe auf das nächste Vielfache von 16
        if menu_height % 16 != 0:
            menu_height += 16 - (menu_height % 16)

        if self.current_resolution_index != self.original_resolution_index:
            title_text_str = f"{self.lang.get(CHANGE_RESOLUTION)}"
        if self.current_modes_index != self.original_modes_index:
            title_text_str = f"{self.lang.get(CHANGE_MODE)}"
        if self.current_resolution_index != self.original_resolution_index and self.current_modes_index != self.original_modes_index:
            title_text_str = f"{self.lang.get(CHANGE_BOTH_RES_MODE)}"
        
        restart_message = f"{self.lang.get(RESTART_GAME)}"
        # Berechne die Breite basierend auf der längeren der beiden Nachrichten
        title_text_width = self.font.size(title_text_str)[0]
        restart_text_width = self.font.size(restart_message)[0]
        max_text_width = max(title_text_width, restart_text_width)

        min_width = 400
        padding_sides = 100
        menu_width = max(max_text_width + padding_sides, min_width)

        # Runde die Breite auf das nächste Vielfache von 16
        if menu_width % 16 != 0:
            menu_width += 16 - (menu_width % 16)
        # Menü zentrieren
        menu_x = (SCREEN_WIDTH - menu_width) // 2
        menu_y = (SCREEN_HEIGHT - menu_height) // 2
        # Hintergrund und Rahmen zeichnen
        if self.background_image:
            self.screen.blit(pygame.transform.scale(self.background_image, (SCREEN_WIDTH, SCREEN_HEIGHT)), (0, 0))

        MenuManager.draw_window_border(self.screen)
        MenuManager.draw_boarder(self.screen , (menu_x, menu_y, menu_width, menu_height))
        # Titel anzeigen
        title_text = self.font.render(title_text_str, True, (255, 255, 255))
        title_rect = title_text.get_rect(center=(SCREEN_WIDTH // 2, menu_y + 40))
        self.screen.blit(title_text, title_rect)
        # Changemeldung anzeigen
        restart_text = self.font.render(restart_message, True, (255, 0, 0))
        restart_rect = restart_text.get_rect(center=(SCREEN_WIDTH // 2, menu_y + 100))
        self.screen.blit(restart_text, restart_rect)
        # 4 Sekunden warten, bevor das Spiel neu startet
        pygame.display.flip()
        pygame.time.delay(4000)  

    # -----------------------------------
    # Benutzeraktionen Verarbeiten
    # -----------------------------------
    def handle_selection(self):
        """Verarbeitet die Auswahl im Videomenü."""
        selected_option = self.options[self.selected_index]

        if selected_option == self.lang.get(BACK):
            print("Zurück ins Hauptmenü.")

    def adjust_setting(self, key):
        """Passt die Videoeinstellungen an (Tastatur & Maus)."""
        if self.selected_index == 0:  # Auflösung ändern
            if key in (pygame.K_RIGHT, pygame.K_d):
                self.current_resolution_index = (self.current_resolution_index + 1) % len(self.resolutions)
            elif key in (pygame.K_LEFT, pygame.K_a):
                self.current_resolution_index = (self.current_resolution_index - 1) % len(self.resolutions)

            self.options[0] = self.lang.get(SELECT_RESOLUTION) + f": {self.get_resolution_text()}"
            self.save_resolution_to_settings()

        elif self.selected_index == 1:  # Modus ändern
            if key in (pygame.K_RIGHT, pygame.K_d, pygame.K_LEFT, pygame.K_a):
                self.current_modes_index = (self.current_modes_index + 1) % len(self.modes)

            self.options[1] = self.lang.get(SELECT_MODE) + f": {self.get_mode_text()}"
            self.save_mode_to_settings()

    def check_and_restart(self):
        """Überprüft, ob Änderungen vorgenommen wurden, und startet das Spiel ggf. neu."""
        if self.current_resolution_index != self.original_resolution_index or self.current_modes_index != self.original_modes_index:
            self.draw_restart_message()
            self.restart_game()

    def restart_game(self):
        """Startet das Spiel neu."""
        python = sys.executable
        os.execl(python, python, *sys.argv)

    def save_resolution_to_settings(self):
        """Speichert die ausgewählte Auflösung in der settings.json."""
        selected_resolution = self.resolutions[self.current_resolution_index]
        SettingsManager.update_settings('resolution', {'width': selected_resolution[0], 'height': selected_resolution[1]})

    def save_mode_to_settings(self):
        """Speichert den ausgewählten Modus (Fenstermodus/Vollbild) in der settings.json."""
        mode = 'fullscreen' if self.current_modes_index == 1 else 'windowed'
        SettingsManager.update_settings('mode', mode)