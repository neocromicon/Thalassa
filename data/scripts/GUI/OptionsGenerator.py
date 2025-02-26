import pygame
import sys
import random
import importlib
import data.scripts.MapGenerator.Settings as Settings
from data.scripts.Constants import BACKGROUND_PICTURE, FONT_BIG, FONT_INT_BIG, FONT_TITLE_COLOR
from data.scripts.Managers.MenuManager import MenuManager
from data.scripts.MapGenerator.Settings import SCREEN_WIDTH, SCREEN_HEIGHT
from data.scripts.Managers.SettingsManager import SettingsManager
from data.scripts.Managers.LanguageManager import GENERATOR_TITLE, LANGUAGE_MANAGER, BACK, MAP_WIDTH_TEXT, MAP_HEIGHT_TEXT, TREE_CHANCE, MOUNTAIN_CHANCE, NUM_ISLANDS, SEED, GENERATE_MAP
from data.scripts.MapGenerator.TileMap import TileMap
from data.scripts.Game import Game

class OptionsGenerator:
    def __init__(self, screen):
        self.screen = screen
        self.font = pygame.font.Font(FONT_BIG, FONT_INT_BIG)
        self.lang = LANGUAGE_MANAGER
        
        # Standardwerte aus Settings laden
        self.map_width = SettingsManager.load_setting("MAP_WIDTH", 80)
        self.map_height = SettingsManager.load_setting("MAP_HEIGHT", 60)
        self.tree_chance = SettingsManager.load_setting("TREE_SPAWN_CHANCE", 0.15)
        self.mountain_chance = SettingsManager.load_setting("MOUNTAIN_SPAWN_CHANCE", 0.08)
        self.num_islands = SettingsManager.load_setting("NUM_ISLANDS", [5, 8])

        # Hier laden wir den zuletzt benutzten Seed; default = ""
        self.seed = SettingsManager.load_setting("SEED", "")

        self.options = [
            self.lang.get(MAP_WIDTH_TEXT) + f":  {self.map_width}",
            self.lang.get(MAP_HEIGHT_TEXT) + f": {self.map_height}",
            self.lang.get(TREE_CHANCE) + f": {self.tree_chance:.2f}",
            self.lang.get(MOUNTAIN_CHANCE) + f": {self.mountain_chance:.2f}",
            self.lang.get(NUM_ISLANDS) + f": {self.num_islands[0]} - {self.num_islands[1]}",
            self.lang.get(SEED) + f": {self.seed}",
            self.lang.get(GENERATE_MAP),
            self.lang.get(BACK)
        ]
        self.preview_map = None  
        self.input_mode = False
        # Visuelle Einstellungen für Menüauswahl
        self.selected_index = 0
        self.text_color = (255, 255, 255)
        self.highlight_color = (200, 150, 50)
        # Hintergrund und Rahmen des Menüs laden
        self.background_image = MenuManager.load_background(BACKGROUND_PICTURE)

    def run(self):
        running = True
        while running:
            self.draw_menu()
            pygame.display.flip()

            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    sys.exit()

                elif event.type == pygame.KEYDOWN:
                    # Wenn wir im Seed-Eingabemodus sind, behandeln wir Tasten anders
                    if self.input_mode and self.selected_index == 5:
                        running = self.handle_seed_input(event)
                    else:
                        running = self.handle_normal_input(event)

                elif event.type == pygame.MOUSEMOTION:
                    mouse_x, mouse_y = pygame.mouse.get_pos()
                    for index, option_rect in enumerate(self.menu_positions):
                        if option_rect.collidepoint(mouse_x, mouse_y):
                            self.selected_index = index

                elif event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
                    if self.input_mode and self.selected_index == 5:
                        # Falls du auch per Maus-Klick Input beenden willst
                        self.input_mode = False
                        self.update_options()
                    else:
                        running = self.handle_selection()
        # Ende while running

    def handle_normal_input(self, event):
        """Steuert normales Navigieren im Menü (wenn wir nicht im Text-Eingabemodus sind)."""
        if event.key in (pygame.K_UP, pygame.K_w):
            self.selected_index = (self.selected_index - 1) % len(self.options)
        elif event.key in (pygame.K_DOWN, pygame.K_s):
            self.selected_index = (self.selected_index + 1) % len(self.options)
        elif event.key in (pygame.K_LEFT, pygame.K_a, pygame.K_RIGHT, pygame.K_d):
            self.adjust_setting(event.key)
        elif event.key == pygame.K_RETURN:
            return self.handle_selection()
        elif event.key == pygame.K_ESCAPE:
            return False
        return True

    def handle_seed_input(self, event):
        """
        Hier behandeln wir gezielt die Tasten, wenn wir den Seed als Text eintippen.
        So kann man Ziffern, Backspace usw. eingeben.
        """
        if event.key == pygame.K_RETURN:
            # Eingabemodus beenden
            self.input_mode = False
            self.update_options()
            return True

        elif event.key == pygame.K_BACKSPACE:
            # letztes Zeichen löschen
            if len(self.seed) > 0:
                self.seed = self.seed[:-1]
                self.update_options()

        else:
            # Beliebige andere Taste -> wir nehmen nur 0-9, Minuszeichen, ...
            # Je nach Bedarf anpassen, ob du z.B. negative Seeds erlauben willst
            char = event.unicode
            if char.isdigit() or char == "-":
                self.seed += char
                self.update_options()

        return True

    def handle_selection(self):
        if self.selected_index == len(self.options) - 1:  
            # Letzte Option -> BACK
            return False
        elif self.selected_index == len(self.options) - 2:
            # "Generate Map"
            self.save_settings()
            self.generate_map()
            self.start_game = True
            return False
        elif self.selected_index == 5:
            # Seed-Option ausgewählt -> Text-Eingabemodus starten
            self.input_mode = True
            return True

        return True

    def draw_menu(self):
        num_options = len(self.options)
        option_spacing = 50  # Abstand zwischen Optionen
        padding_top_bottom = 60  # Abstand oben und unten

        title_text = self.lang.get(GENERATOR_TITLE)
        title_surface = self.font.render(title_text, True, self.text_color)
        menu_height = num_options * option_spacing + padding_top_bottom + title_surface.get_height()

        if menu_height % 16 != 0:
            menu_height += 16 - (menu_height % 16)

        min_width = 800
        padding_sides = 100
        menu_width = max(padding_sides, min_width)

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
            self.menu_positions.append(option_rect) 

        self.draw_map_preview()

    def adjust_setting(self, key):
        if self.selected_index == 0:  
            # Width
            self.map_width = max(40, self.map_width + (10 if key in (pygame.K_RIGHT, pygame.K_d) else -10))
        elif self.selected_index == 1:  
            # Height
            self.map_height = max(30, self.map_height + (10 if key in (pygame.K_RIGHT, pygame.K_d) else -10))
        elif self.selected_index == 2:  
            # Tree chance
            self.tree_chance = round(max(0, min(1, self.tree_chance + (0.01 if key in (pygame.K_RIGHT, pygame.K_d) else -0.01))), 2)
        elif self.selected_index == 3:  
            # Mountain chance
            self.mountain_chance = round(max(0, min(1, self.mountain_chance + (0.01 if key in (pygame.K_RIGHT, pygame.K_d) else -0.01))), 2)
        elif self.selected_index == 4:  
            # num_islands
            min_val, max_val = self.num_islands
            min_val = max(1, min_val + (1 if key in (pygame.K_RIGHT, pygame.K_d) else -1))
            max_val = max(min_val, max_val + (1 if key in (pygame.K_RIGHT, pygame.K_d) else -1))
            self.num_islands = [min_val, max_val]

        self.update_options()

    def update_options(self):
        """Aktualisiert die Anzeige der Menüoptionen nach einer Änderung."""
        self.options = [
            self.lang.get(MAP_WIDTH_TEXT) + f":  {self.map_width}",
            self.lang.get(MAP_HEIGHT_TEXT) + f": {self.map_height}",
            self.lang.get(TREE_CHANCE) + f": {self.tree_chance:.2f}",
            self.lang.get(MOUNTAIN_CHANCE) + f": {self.mountain_chance:.2f}",
            self.lang.get(NUM_ISLANDS) + f": {self.num_islands[0]} - {self.num_islands[1]}",
            self.lang.get(SEED) + f": {self.seed}",
            self.lang.get(GENERATE_MAP),
            self.lang.get(BACK)
        ]

    def draw_map_preview(self):
        if self.preview_map is None:
            return
        
        preview_x, preview_y = SCREEN_WIDTH - 300, SCREEN_HEIGHT // 4
        tile_size = 4
        for y, row in enumerate(self.preview_map.map):
            for x, tile in enumerate(row):
                # ACHTUNG: In deinem Code schreibst du "GRASS" groß; 
                # in Tile() hast du "Grass" => evtl. anpassen
                color = (139, 69, 19) if tile.base.upper().startswith("Grass") else (0, 0, 255)
                pygame.draw.rect(self.screen, color,
                                 (preview_x + x * tile_size, 
                                  preview_y + y * tile_size, 
                                  tile_size, tile_size))

    def save_settings(self):
        """Speichert die gewählten Werte in den globalen Einstellungen."""
        SettingsManager.update_settings("MAP_WIDTH", self.map_width)
        SettingsManager.update_settings("MAP_HEIGHT", self.map_height)
        SettingsManager.update_settings("TREE_SPAWN_CHANCE", self.tree_chance)
        SettingsManager.update_settings("MOUNTAIN_SPAWN_CHANCE", self.mountain_chance)
        SettingsManager.update_settings("NUM_ISLANDS", self.num_islands)
        SettingsManager.update_settings("SEED", self.seed)

    def generate_map(self):
        """
        Erstellt die Vorschaukarte (und startet anschließend das Game).
        Wenn self.seed leer ist, verwenden wir keinen festen Seed
        => random.seed(None) => truly random
        """
        if self.seed.strip():
            # Falls der Nutzer etwas eingegeben hat, versuchen wir, es als int zu interpretieren
            try:
                int_seed = int(self.seed)
                random.seed(int_seed)
            except ValueError:
                # Falls es kein int war -> nimm lieber random
                random.seed(None)
        else:
            # Wenn seed leer -> truly random
            random.seed(None)
        
        self.preview_map = TileMap(
            map_width=self.map_width,
            map_height=self.map_height,
            tree_chance=self.tree_chance,
            mountain_chance=self.mountain_chance,
            num_islands=self.num_islands,
            seed=None,        # <-- Du setzt hier None => Dann wird in TileMap entweder seed=None verarbeitet,
                              #     oder du benutzt dort "random.seed()" direkt. 
                              #     Du kannst die Logik in TileMap.__init__ anpassen, wenn gewollt.
            generate=True
        )

        Settings.MAP_WIDTH = self.map_width
        Settings.MAP_HEIGHT = self.map_height
        
        game = Game(self.screen, self.map_width, self.map_height)
        game.tilemap = self.preview_map
        game.set_tilemap(self.preview_map)
        game.run()
