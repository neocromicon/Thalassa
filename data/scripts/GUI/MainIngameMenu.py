import pygame
import sys
from data.scripts.Managers.SaveManager import SaveManager
from data.scripts.Managers.MenuManager import MenuManager
from data.scripts.Constants import BACKGROUND_PICTURE, FONT_BIG, FONT_INT_BIG, FONT_TITLE_COLOR
from data.scripts.MapGenerator.Settings import SCREEN_WIDTH, SCREEN_HEIGHT
from data.scripts.GUI.OptionsMenu import OptionsMenu
from data.scripts.Managers.LanguageManager import EMPTY_SAVE_SLOT, GAME_SAVED, LANGUAGE_MANAGER, ERROR, NO_SAVE_ONSLOT, SAVE_AS, CONTINUE, SAVE_GAME, ACTION_SAVE_GAME, LOAD_GAME, ACTION_LOAD_GAME, SAVED_SLOT, SELECT_SLOT, OPTIONS, CREDITS, EXIT, UNTITLED

# ------------------------------------------
# Hauptmenü-Klasse für das Ingame-Pausenmenü
# ------------------------------------------
class MainIngameMenu:
    def __init__(self, screen, game_instance):
        """Initialisiert das Ingame-Menü mit Bildschirm und Spielinstanz."""
        self.screen = screen
        self.game = game_instance
        self.start_game = False
        # Schriftart und Menüoptionen definieren
        self.font = pygame.font.Font(FONT_BIG, FONT_INT_BIG)
        # Sprachmanager initialisieren
        self.lang = LANGUAGE_MANAGER  # Sprache auf Deutsch setzen
        # Savemanager initialisieren
        self.save_manager = SaveManager(self.lang)
        # Sprachschlüssel für die Optionen definieren
        self.options = [
            self.lang.get(CONTINUE),
            self.lang.get(SAVE_GAME),
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

    # -----------------------------------
    # Haupt-Loop des Ingame-Menüs
    # -----------------------------------
    def run(self):
        """Startet das Ingame-Menü und verarbeitet Benutzereingaben."""
        running = True
        while running and not self.start_game:
            self.draw_menu_pause()
            pygame.display.flip()

            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    sys.exit()
                elif event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_UP or event.key == pygame.K_w:
                        self.selected_index = (self.selected_index - 1) % len(self.options)
                    elif event.key == pygame.K_DOWN or event.key == pygame.K_s:
                        self.selected_index = (self.selected_index + 1) % len(self.options)
                    elif event.key == pygame.K_RETURN:
                        running = self.handle_selection()
                    elif event.key == pygame.K_ESCAPE:
                        self.game.pause_game = False  # Pausenstatus zurücksetzen
                        self.game.back_to_menu = False
                        running = False
                elif event.type == pygame.MOUSEMOTION:
                    mouse_x, mouse_y = pygame.mouse.get_pos()
                    for index, option_rect in enumerate(self.menu_positions):
                        if option_rect.collidepoint(mouse_x, mouse_y):
                            self.selected_index = index # Maus bewegt sich über Menüpunkt
                elif event.type == pygame.MOUSEBUTTONDOWN:
                    if event.button == 1:  # Linksklick
                        running = self.handle_selection()
                    elif event.button == 3:  # Rechtsklick -> Menü verlassen
                        self.game.pause_game = False  # Pausenstatus zurücksetzen
                        self.game.back_to_menu = False
                        running = False

    # -----------------------------------
    # Menü und Rahmen Zeichnen
    # -----------------------------------
    def draw_menu_pause(self):
        """Zeichnet das Haupt-Ingame-Menü mit allen Optionen."""
        # Berechne die minimale Höhe basierend auf der Anzahl der Optionen
        num_options = len(self.options)
        option_spacing = 50  # Abstand zwischen den Optionen
        padding_top_bottom = 60  # Abstand oben und unten

        menu_height = num_options * option_spacing + padding_top_bottom

        # Runde die Höhe auf das nächste Vielfache von 16
        if menu_height % 16 != 0:
            menu_height += 16 - (menu_height % 16)

        menu_width = 400
        menu_x = (SCREEN_WIDTH - menu_width) // 2
        menu_y = (SCREEN_HEIGHT - menu_height) // 2

        if self.background_image:
            self.screen.blit(pygame.transform.scale(self.background_image, (SCREEN_WIDTH, SCREEN_HEIGHT)), (0, 0))

        MenuManager.draw_window_border(self.screen)
        MenuManager.draw_boarder(self.screen, (menu_x, menu_y, menu_width, menu_height))	

        # **Menüpositionen für Maussteuerung speichern**
        self.menu_positions = []

        # Menüoptionen zeichnen            
        for index, option in enumerate(self.options):
            color = self.highlight_color if index == self.selected_index else self.text_color
            option_y = menu_y + 60 + index * 50
            MenuManager.draw_text_with_soft_shadow(self, option, SCREEN_WIDTH // 2, option_y, color)

            # Rechtecke der Menüoptionen speichern für Mausinteraktion
            option_rect = pygame.Rect(SCREEN_WIDTH // 2 - 100, option_y - 20, 200, 40)
            self.menu_positions.append(option_rect)

    def draw_menu_LoadSave(self, slots, selected_slot, action):
        """Zeichnet die Slot-Auswahl für das Speichern oder Laden mit dynamischer Breite."""
        
        # Dynamische Berechnung der Höhe basierend auf der Anzahl der Slots
        num_slots = len(slots)
        option_spacing = 50  # Abstand zwischen den Slots
        padding_top_bottom = 80  # Abstand oben und unten
        menu_height = num_slots * option_spacing + padding_top_bottom

        # Erhöhe die Höhe um ein zusätzliches Tile (16 Pixel) für mehr Abstand unten
        menu_height += 16  # Extra Abstand nach unten

        # Runde die Höhe auf das nächste Vielfache von 16
        if menu_height % 16 != 0:
            menu_height += 16 - (menu_height % 16)

        # Berechne die Breite des längsten Slot-Textes
        longest_slot_text = max(slots, key=lambda slot: self.font.size(slot)[0])
        longest_slot_width = self.font.size(longest_slot_text)[0]

        # Berechne die Breite des Titeltexts
        title_text_str = f"{action} - {self.lang.get(SELECT_SLOT)}"
        title_text_width = self.font.size(title_text_str)[0]

        # Nimm die größere Breite von Titeltext und Slot
        max_text_width = max(longest_slot_width, title_text_width)

        padding_sides = 100  # Seitlicher Puffer
        menu_width = max_text_width + padding_sides

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

        # Zeichne Titel mit Schatten
        MenuManager.draw_text_with_soft_shadow_title(self, title_text_str, SCREEN_WIDTH // 2, menu_y + 40, FONT_TITLE_COLOR)

        # **Menüpositionen für Maussteuerung speichern**
        self.menu_positions = []

        # Zeichne Menüoptionen mit Schatten
        for index, slot in enumerate(slots):
            color = self.highlight_color if (index + 1) == selected_slot else self.text_color
            option_y = menu_y + 100 + index * option_spacing
            MenuManager.draw_text_with_soft_shadow(self, slot, SCREEN_WIDTH // 2, option_y, color)

            # **Angepasste Hitbox für Maus-Interaktion**
            text_width = self.font.size(slot)[0]
            option_rect = pygame.Rect((SCREEN_WIDTH // 2) - (text_width // 2) - 10, option_y - 20, text_width + 20, 40)
            self.menu_positions.append(option_rect)

    def draw_menu_SaveToSlot(self, current_name):
        """Zeichnet das Menü zur Eingabe des Speicherstand-Namens mit dynamischer Breite."""
        # Feste Höhe, da es nur eine Eingabezeile gibt
        menu_height = 144  
        
        # Berechne die Breite des aktuellen Namens
        name_width = self.font.size(current_name)[0]

        # Berechne die Breite des Titeltexts ("Speichern unter:")
        title_text_str = self.lang.get(SAVE_AS)
        title_text_width = self.font.size(title_text_str)[0]

        # Nimm die größere Breite von Titel und Name
        max_text_width = max(name_width, title_text_width)

        # Mindestbreite und Puffer
        min_width = 400  # Mindestbreite, damit das Menü nicht zu klein wird
        padding_sides = 100

        # Berechne die endgültige Breite
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

        # **Menüpositionen für Maussteuerung speichern**
        self.menu_positions = []

        # Titel anzeigen (nach der Brechnungslogik)
        MenuManager.draw_text_with_soft_shadow_title(self, title_text_str, SCREEN_WIDTH // 2, menu_y + 40, FONT_TITLE_COLOR)

        # Namenseingabe anzeigen
        MenuManager.draw_text_with_soft_shadow(self, current_name, SCREEN_WIDTH // 2, menu_y + 100, self.text_color)

    def draw_menu_LoadError(self, slot):
        """Zeigt eine Fehlermeldung, wenn kein Speicherstand für den ausgewählten Slot existiert."""
        menu_height = 200  # Feste Höhe für die Fehlermeldung
        title_text_str = f"{self.lang.get(ERROR)}:"
        error_message = f"{self.lang.get(NO_SAVE_ONSLOT)} {slot}!"

        # Berechne die Breite basierend auf der längeren der beiden Nachrichten
        title_text_width = self.font.size(title_text_str)[0]
        error_text_width = self.font.size(error_message)[0]
        max_text_width = max(title_text_width, error_text_width)

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
        MenuManager.draw_boarder(self.screen, (menu_x, menu_y, menu_width, menu_height), reduce_rows=True)	

        # **Menüpositionen für Maussteuerung speichern**
        self.menu_positions = []

        # Titel anzeigen
        MenuManager.draw_text_with_soft_shadow_title(self, title_text_str, SCREEN_WIDTH // 2, menu_y + 40, FONT_TITLE_COLOR)

        # Fehlermeldung anzeigen
        MenuManager.draw_text_with_soft_shadow(self, error_message, SCREEN_WIDTH // 2, menu_y + 100, (255, 0, 0))

    def draw_menu_game_saved(self, slot):
        """Zeigt eine Fehlermeldung, wenn kein Speicherstand für den ausgewählten Slot existiert."""
        menu_height = 96  # Feste Höhe für die Fehlermeldung
        error_message = f"{self.lang.get(SAVED_SLOT)} {slot}!"

        # Berechne die Breite basierend auf der längeren der beiden Nachrichten
        error_text_width = self.font.size(error_message)[0]

        min_width = 400
        padding_sides = 100
        menu_width = max(error_text_width + padding_sides, min_width)

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
        MenuManager.draw_boarder(self.screen, (menu_x, menu_y, menu_width, menu_height), reduce_rows=True)	

        # Fehlermeldung anzeigen
        MenuManager.draw_text_with_soft_shadow(self, error_message, SCREEN_WIDTH // 2, menu_y + 40, (255, 0, 0))

    # -----------------------------------
    # Benutzeraktionen Verarbeiten
    # -----------------------------------
    def handle_selection(self):
        """Verarbeitet die Auswahl des Spielers im Ingame-Menü."""
        selected_option = self.options[self.selected_index]
        
        if selected_option == self.lang.get(CONTINUE):
            print("Spiel wird sofort fortgesetzt.")  # Debugging-Ausgabe
            self.game.pause_game = False  # Pausenstatus zurücksetzen
            self.game.back_to_menu = False  # Menü verlassen
            pygame.event.clear()  # Alle wartenden Events löschen, um Verzögerungen zu vermeiden
            return False  # `run()`-Schleife beenden

        if selected_option == self.lang.get(SAVE_GAME):
            slot = self.choose_slot(action=self.lang.get(ACTION_SAVE_GAME))
            if slot:
                # Bestehenden Namen aus dem SaveManager-Cache abrufen
                existing_name = self.save_manager.get_existing_save_name(slot)
                
                # Eingabefeld für neuen oder bestehenden Namen öffnen
                save_name = self.get_save_name(existing_name)
                
                # Spiel speichern
                self.game.save_game(slot=slot, save_name=save_name)
                
                # Cache aktualisieren, damit die Änderungen sofort sichtbar sind
                self.save_manager.refresh_saves_cache()
                self.show_game_is_saved(slot)

        if selected_option == self.lang.get(LOAD_GAME):
            slot = self.choose_slot(action=self.lang.get(ACTION_LOAD_GAME))
            if slot:
                # Überprüfe mit dem SaveManager, ob der Speicherstand existiert
                if not self.save_manager.save_exists(slot):
                    self.show_load_error(slot)  # Fehlermeldung anzeigen, wenn Slot leer ist
                else:
                    # Spiel laden
                    self.game.load_game(slot=slot)
                    self.start_game = True

        if selected_option == self.lang.get(OPTIONS):
            options_menu = OptionsMenu(self.screen, self.game)
            options_menu.run()
            
        if selected_option == self.lang.get(EXIT):
            pygame.quit()
            sys.exit()

    def choose_slot(self, action="Speichern"):
        """Zeigt die verfügbaren Speicherslots zur Auswahl an und ermöglicht die Steuerung per Tastatur und Maus."""
        slots = self.save_manager.get_existing_saves()  # Cache statt direkte Dateiabfrage verwenden
        selected_slot = 1
        choosing = True

        while choosing:
            self.screen.fill((0, 0, 0))
            self.draw_menu_LoadSave(slots, selected_slot, action)  # Zeichne das Menü mit Slot-Optionen
            pygame.display.flip()

            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    sys.exit()
                elif event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_UP or event.key == pygame.K_w:
                        selected_slot = (selected_slot - 2) % len(slots) + 1
                    elif event.key == pygame.K_DOWN or event.key == pygame.K_s:
                        selected_slot = selected_slot % len(slots) + 1
                    elif event.key == pygame.K_RETURN:
                        choosing = False
                    elif event.key == pygame.K_ESCAPE:
                        return None  # Abbrechen
                elif event.type == pygame.MOUSEMOTION:
                    mouse_x, mouse_y = pygame.mouse.get_pos()
                    for index, option_rect in enumerate(self.menu_positions):
                        if option_rect.collidepoint(mouse_x, mouse_y):
                            selected_slot = index + 1  # Slots sind 1-basiert
                elif event.type == pygame.MOUSEBUTTONDOWN:
                    if event.button == 1:  # Linksklick
                        choosing = False  # Slot auswählen und Menü schließen
                    elif event.button == 3:  # **Rechtsklick verlässt Menü**
                        return None  # Abbrechen
                    
        return selected_slot
    
    def show_load_error(self, slot):
        """Zeigt das Fehlermeldungs-Menü an und kehrt nach Bestätigung zum Lade-Menü zurück."""
        showing_error = True

        while showing_error:
            self.screen.fill((0, 0, 0))
            self.draw_menu_LoadError(slot)
            pygame.display.flip()

            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    sys.exit()
                elif event.type == pygame.KEYDOWN:
                    if event.key in [pygame.K_RETURN, pygame.K_ESCAPE]:  # Mit Enter oder Escape das Menü schließen
                        showing_error = False  # Beendet die Fehlermeldung
                elif event.type == pygame.MOUSEBUTTONDOWN:
                    if event.button == 3:  # **Rechtsklick verlässt Menü**
                        showing_error = False  # Beendet die Fehlermeldung

        # Nach Schließen der Fehlermeldung zum Lade-Menü zurückkehren
        slot = self.choose_slot(action=self.lang.get(ACTION_LOAD_GAME))
        if slot:
            if self.save_manager.save_exists(slot):
                self.game.load_game(slot=slot)
                self.start_game = True
            else:
                self.show_load_error(slot)  # Wenn erneut kein Speicherstand vorhanden ist, die Fehlermeldung erneut zeigen

    def show_game_is_saved(self, slot):
        """Zeigt das Fehlermeldungs-Menü an und kehrt nach Bestätigung zum Lade-Menü zurück."""
        show_game_is_saved = True

        while show_game_is_saved:
            self.screen.fill((0, 0, 0))
            self.draw_menu_game_saved(slot)
            pygame.display.flip()

            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    sys.exit()
                elif event.type == pygame.KEYDOWN:
                    if event.key in [pygame.K_RETURN, pygame.K_ESCAPE]:  # Mit Enter oder Escape das Menü schließen
                        show_game_is_saved = False  # Beendet die Fehlermeldung
                elif event.type == pygame.MOUSEBUTTONDOWN:
                    if event.button == 3:  # **Rechtsklick verlässt Menü**
                        show_game_is_saved = False  # Beendet die Fehlermeldung

    # -----------------------------------
    # Speicherstände Verwalten
    # -----------------------------------
    def get_save_name(self, existing_name=""):
        """Ermöglicht die Eingabe eines Namens für den Speicherstand, mit eigenem Menü."""

        save_name = existing_name  # Vorhandener Name wird vorausgefüllt
        save_name = "" if existing_name == self.lang.get(EMPTY_SAVE_SLOT) else existing_name
        entering = True
        allowed_chars = "abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ0123456789"
        while entering:
            self.screen.fill((0, 0, 0))
            self.draw_menu_SaveToSlot(save_name)  # Neues Menü für Namenseingabe

            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    sys.exit()
                elif event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_RETURN:
                        entering = False
                    elif event.key == pygame.K_BACKSPACE:
                        save_name = save_name[:-1]
                    elif len(save_name) < 20:  # Maximale Länge für den Namen
                        # Prüfen, ob das eingegebene Zeichen erlaubt ist
                        if event.unicode in allowed_chars:
                            save_name += event.unicode

            pygame.display.flip()

        return save_name if save_name else self.lang.get(UNTITLED)
