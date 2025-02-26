import os
import pygame
import sys
from data.scripts.Managers.MenuManager import MenuManager
from data.scripts.Constants import BACKGROUND_PICTURE, FONT_BIG, FONT_INT_BIG, FONT_TITLE_COLOR
from data.scripts.MapGenerator.Settings import SCREEN_WIDTH, SCREEN_HEIGHT
from data.scripts.Managers.LanguageManager import CHANGE_LANG, LANGUAGE_MANAGER, RESTART_GAME, SELECT_LANGUAGE, BACK

class OptionsLanguage:
    def __init__(self, screen, game_instance):
        """Initialisiert das Sprachmenü."""
        self.screen = screen
        self.game = game_instance
        self.font = pygame.font.Font(FONT_BIG, FONT_INT_BIG)
        self.lang = LANGUAGE_MANAGER  # Sprachmanager
        # Sprachen definieren
        self.languages = {"Deutsch": "de", "English": "en"}
        # **Option Keys definieren** (für Übersetzungen und Logik)
        self.option_keys = list(self.languages.keys()) + [BACK]
        # **Übersetzte Optionen basierend auf Keys laden**
        self.options = [self.lang.get(key) for key in self.option_keys]
        # Visuelle Einstellungen für Menüauswahl
        self.selected_index = 0
        self.text_color = (255, 255, 255)
        self.highlight_color = (200, 150, 50)
        # Hintergrund und Rahmen des Menüs laden
        self.background_image = MenuManager.load_background(BACKGROUND_PICTURE)

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
    # -----------------------------------
    # Menü und Rahmen Zeichnen
    # -----------------------------------
    def draw_menu(self):
        """Zeichnet das Sprachmenü."""
        num_options = len(self.options)
        option_spacing = 50
        padding_top_bottom = 60

        title_text = self.lang.get(SELECT_LANGUAGE)
        title_surface = self.font.render(title_text, True, self.text_color)
        menu_height = num_options * option_spacing + padding_top_bottom + title_surface.get_height()

        if menu_height % 16 != 0:
            menu_height += 16 - (menu_height % 16)

        menu_width = 400
        menu_x = (SCREEN_WIDTH - menu_width) // 2
        menu_y = (SCREEN_HEIGHT - menu_height) // 2

        if self.background_image:
            self.screen.blit(pygame.transform.scale(self.background_image, (SCREEN_WIDTH, SCREEN_HEIGHT)), (0, 0))

        MenuManager.draw_window_border(self.screen)
        MenuManager.draw_boarder(self.screen, (menu_x, menu_y, menu_width, menu_height))	
        
        # Zeichne Titel mit Schatten
        title_y = menu_y + 40
        MenuManager.draw_text_with_soft_shadow_title(self, title_text, SCREEN_WIDTH // 2, title_y, FONT_TITLE_COLOR)

        # Zeichne Menüoptionen mit Schatten
        for index, option in enumerate(self.options):
            color = self.highlight_color if index == self.selected_index else self.text_color
            option_y = menu_y + 100 + index * option_spacing
            MenuManager.draw_text_with_soft_shadow(self, option, SCREEN_WIDTH // 2, option_y, color)

    def draw_menu_LanguageChanged(self, selected_language):
        """Zeigt eine Fehlermeldung, wenn kein Speicherstand für den ausgewählten Slot existiert."""
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

        title_text_str = f"{self.lang.get(CHANGE_LANG)}:"
        change_message = f"{selected_language}"
        restart_message = f"{self.lang.get(RESTART_GAME)}"
        # Berechne die Breite basierend auf der längeren der beiden Nachrichten
        title_text_width = self.font.size(title_text_str)[0]
        change_text_width = self.font.size(change_message)[0]
        restart_text_width = self.font.size(restart_message)[0]
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
        # Hintergrund und Rahmen zeichnen
        if self.background_image:
            self.screen.blit(pygame.transform.scale(self.background_image, (SCREEN_WIDTH, SCREEN_HEIGHT)), (0, 0))

        MenuManager.draw_window_border(self.screen)
        MenuManager.draw_boarder(self.screen, (menu_x, menu_y, menu_width, menu_height))
        
        # Titel anzeigen
        MenuManager.draw_text_with_soft_shadow_title(self, title_text_str, SCREEN_WIDTH // 2, menu_y + 40, FONT_TITLE_COLOR)
        # Changemeldung anzeigen
        MenuManager.draw_text_with_soft_shadow(self, change_message, SCREEN_WIDTH // 2, menu_y + 100, self.text_color)
        # Changemeldung anzeigen
        MenuManager.draw_text_with_soft_shadow(self, restart_message, SCREEN_WIDTH // 2, menu_y + 160, (255, 0, 0))
        # 4 Sekunden warten, bevor das Spiel neu startet
        pygame.display.flip()
        pygame.time.delay(4000)  

    # -----------------------------------
    # Benutzeraktionen Verarbeiten
    # -----------------------------------
    def handle_selection(self):
        """Verarbeitet die Auswahl im Sprachmenü."""
        selected_option = self.options[self.selected_index]
        
        if selected_option in self.languages:
            # Sprache setzen und speichern
            LANGUAGE_MANAGER.set_language(self.languages[selected_option])
            # Bestätigungsnachricht
            self.draw_menu_LanguageChanged(selected_option)
            # Spiel neu starten
            self.restart_game()

    def restart_game(self):
        """Startet das Spiel neu."""
        python = sys.executable  # Pfad zum Python-Interpreter
        os.execl(python, python, *sys.argv)