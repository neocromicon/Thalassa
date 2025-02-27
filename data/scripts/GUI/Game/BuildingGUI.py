import pygame
import json
from data.scripts.Constants import FONT_BIG
from data.scripts.Managers.MenuManager import MenuManager
from data.scripts.MapGenerator.Settings import SCREEN_HEIGHT

class BuildingGUI:
    """GUI zum Auswählen von Gebäuden für den Bau (1.35x Skalierung) mit stilisierten Tooltips"""

    def __init__(self, game, buildings_json_path="data/config/Buildings.json", goods_path="data/config/Goods.json"):
        self.game = game
        self.show_gui = False
        self.show_submenu = None
        self.panel_rect = None
        self.font = pygame.font.Font(FONT_BIG, 20)
        self.category_buttons = {}
        self.submenu_buttons = {}
        self.tooltip_text = None
        self.tooltip_pos = (0, 0)
        self.goods_icons = {}

        # Tooltip-Stil wie in ResourceDisplayGUI
        self.bg_color = (0, 0, 0, 180)  # Dunkler transparenter Hintergrund
        self.border_radius = 10  # Abgerundete Ecken
        self.padding = 10  # Abstand um den Text

        # Lade Gebäudedaten aus JSON
        self.categories = {
            "raw_materials": {
                "icon": pygame.image.load("data/img/Buildings/Raw_Materials.png"),
                "buildings": []
            },
            "production": {
                "icon": pygame.image.load("data/img/Buildings/Production_building.png"),
                "buildings": []
            }
        }
        self.load_buildings(buildings_json_path)
        self.load_goods_icons(goods_path)

        # 🏗 Bau-Button unten links
        self.build_button_icon = pygame.image.load("data/img/GUI/build_icon.png")
        self.build_button_rect = pygame.Rect(20, SCREEN_HEIGHT - 100, 64, 64) 

    def load_buildings(self, path):
        """Lädt die Gebäude aus der JSON-Datei und sortiert sie in Kategorien"""
        with open(path, "r") as file:
            data = json.load(file)

        for building_key, building_data in data["buildings"].items():
            if "category" in building_data and "texture" in building_data:
                category = building_data["category"]
                texture_path = f"data/img/Buildings/{building_data['texture']}"
                if category in self.categories:
                    icon = pygame.image.load(texture_path)
                    icon = pygame.transform.scale(icon, (67, 67))  # 1.35x Größe
                    self.categories[category]["buildings"].append({
                        "name": building_key,
                        "icon": icon,
                        "cost": building_data.get("cost", {})
                    })

        # Skaliere die Kategorien-Icons ebenfalls auf 67x67
        for category in self.categories.values():
            category["icon"] = pygame.transform.scale(category["icon"], (67, 67))

    def load_goods_icons(self, path):
        """Lädt die Icons für Ressourcen, um sie in den Tooltips anzuzeigen"""
        with open(path, "r") as file:
            data = json.load(file)

        for good, good_data in data["goods"].items():
            texture_path = f"data/img/Goods/{good_data['texture']}"
            self.goods_icons[good] = pygame.transform.scale(pygame.image.load(texture_path), (16, 16))  # 16x16 kleine Icons

    def toggle_gui(self):
        """Öffnet oder schließt das Baumenü."""
        self.show_gui = not self.show_gui

    def start_building_mode(self, building_name):
        """Aktiviert den Bau-Modus über den BuildingManager"""
        print(f"🏗️ Bau-Modus gestartet für {building_name}")
        self.game.building_manager.start_building_mode(building_name)

    def update_build_preview(self, mouse_pos):
        """Aktualisiert die Bau-Vorschau über den BuildingManager"""
        self.game.building_manager.update_preview(mouse_pos)

    def place_building(self):
        """Platziert das Gebäude über den BuildingManager"""
        self.game.building_manager.place_building()

    def draw(self, screen):
        """Zeichnet die Bau-GUI und den Bau-Button"""
        # 🔹 **Zeichne den Bau-Button unten links**
        screen.blit(pygame.transform.scale(self.build_button_icon, (64, 64)), (20, SCREEN_HEIGHT - 100))
        MenuManager.draw_slot_border(screen, 20, SCREEN_HEIGHT - 100, 64)  # Umrandung

        if not self.show_gui:
            return

        # 🔹 **Zeichne das Baumenü**
        panel_width = 270
        panel_height = 297
        panel_x = 20
        panel_y = SCREEN_HEIGHT - panel_height - 25
        self.panel_rect = pygame.Rect(panel_x, panel_y, panel_width, panel_height)

        pygame.draw.rect(screen, (40, 40, 60), self.panel_rect)
        MenuManager.draw_ship_border(screen, panel_x, panel_y, panel_width, panel_height)

        # Kategorien zeichnen
        y_offset = panel_y + 27
        self.category_buttons.clear()
        for key, category in self.categories.items():
            icon = category["icon"]
            button_rect = pygame.Rect(panel_x + 27, y_offset, 67, 67)
            screen.blit(icon, (panel_x + 27, y_offset))
            self.category_buttons[key] = button_rect
            y_offset += 80  

        # Falls ein Submenü geöffnet ist, zeichne es
        if self.show_submenu:
            self.draw_submenu(screen, panel_x + 108, panel_y + 27)

        # Zeige Tooltip falls aktiv
        if self.tooltip_text:
            self.draw_tooltip(screen)

    def draw_submenu(self, screen, x, y):
        """Zeichnet das aufklappbare Menü für eine Kategorie"""
        category = self.categories[self.show_submenu]
        panel_width = 216
        panel_height = 81 * len(category["buildings"]) + 27
        panel_rect = pygame.Rect(x, y, panel_width, panel_height)

        pygame.draw.rect(screen, (60, 60, 80), panel_rect)
        MenuManager.draw_ship_border(screen, x, y, panel_width, panel_height)

        self.submenu_buttons.clear()
        y_offset = y + 13
        for building in category["buildings"]:
            button_rect = pygame.Rect(x + 13, y_offset, 54, 54) 
            screen.blit(building["icon"], (x + 13, y_offset))
            
            # **Hier wird jetzt das korrekte Tupel mit (rect, cost) gespeichert!**
            self.submenu_buttons[building["name"]] = (button_rect, building["cost"])
            
            y_offset += 68

    def handle_hover(self, mouse_pos):
        """Überprüft, ob die Maus über einem Icon ist, und zeigt den Tooltip an"""
        self.tooltip_text = None

        # Kategorie-Tooltips
        for key, rect in self.category_buttons.items():
            if rect.collidepoint(mouse_pos):
                self.tooltip_text = key.replace("_", " ").capitalize()
                self.tooltip_pos = (mouse_pos[0] + 15, mouse_pos[1] + 10)
                return

        # Gebäude-Tooltips
        if self.show_submenu:
            for name, (rect, cost) in self.submenu_buttons.items():
                if rect.collidepoint(mouse_pos):
                    self.tooltip_text = (name, cost)
                    self.tooltip_pos = (mouse_pos[0] + 15, mouse_pos[1] + 10)
                    return

    def draw_tooltip(self, screen):
        """Zeichnet den Tooltip rechts neben der Maus mit zentriertem Namen und Ressourcen"""
        if isinstance(self.tooltip_text, str):
            # Kategorie-Tooltip (nur Name)
            text_surface = self.font.render(self.tooltip_text, True, (255, 255, 255))
            text_rect = text_surface.get_rect()

            # Position des Tooltips rechts neben der Maus
            tooltip_x = self.tooltip_pos[0] + 15  
            tooltip_y = self.tooltip_pos[1]  

            # Halbtransparenter Hintergrund mit abgerundeten Ecken
            tooltip_width = text_rect.width + 20
            tooltip_height = text_rect.height + 10

            tooltip_surface = pygame.Surface((tooltip_width, tooltip_height), pygame.SRCALPHA)
            pygame.draw.rect(tooltip_surface, self.bg_color, (0, 0, tooltip_width, tooltip_height), border_radius=self.border_radius)

            screen.blit(tooltip_surface, (tooltip_x, tooltip_y))
            screen.blit(text_surface, (tooltip_x + 10, tooltip_y + 5))

        else:
            # Gebäude-Tooltip mit Ressourcen unter dem Namen
            name, cost = self.tooltip_text
            text_surface = self.font.render(name, True, (255, 255, 255))
            name_rect = text_surface.get_rect()

            # Berechne die maximale Breite basierend auf Ressourcen
            total_width = max(name_rect.width, len(cost) * 42) + self.padding * 2  
            total_height = name_rect.height + 30  

            if cost:
                total_height += 20  

            # Position des Tooltips rechts neben der Maus
            tooltip_x = self.tooltip_pos[0] + 15  
            tooltip_y = self.tooltip_pos[1]  

            # Erstelle die Hintergrund-Box
            tooltip_surface = pygame.Surface((total_width, total_height), pygame.SRCALPHA)
            pygame.draw.rect(tooltip_surface, self.bg_color, (0, 0, total_width, total_height), border_radius=self.border_radius)

            # Hintergrund rendern
            screen.blit(tooltip_surface, (tooltip_x, tooltip_y))

            # Namen zentriert rendern
            name_x = tooltip_x + (total_width // 2 - name_rect.width // 2)
            screen.blit(text_surface, (name_x, tooltip_y + 5))

            # Ressourcen nebeneinander unter dem Namen zentrieren
            icon_x = tooltip_x + (total_width - (len(cost) * 42)) // 2  
            icon_y = tooltip_y + name_rect.height + 10  
            for good, amount in cost.items():
                screen.blit(self.goods_icons[good], (icon_x, icon_y))  
                amount_text = self.font.render(f"x{amount}", True, (255, 255, 255))
                screen.blit(amount_text, (icon_x + 18, icon_y))  
                icon_x += 42  

    def handle_click(self, mouse_pos):
        """Verarbeitet Mausklicks auf die GUI"""
        # Klick auf Bau-Button -> Menü öffnen/schließen
        if self.build_button_rect.collidepoint(mouse_pos):
            self.toggle_gui()
            return True

        if not self.show_gui:
            return False

        # Klick auf Hauptkategorien
        for key, rect in self.category_buttons.items():
            if rect.collidepoint(mouse_pos):
                self.show_submenu = None if self.show_submenu == key else key
                return True
            
        # Klick auf Untermenü (Gebäude)
        if self.show_submenu:
            for name, (rect, cost) in self.submenu_buttons.items():
                if rect.collidepoint(mouse_pos):
                    self.game.building_manager.start_building_mode(name)
                    return True

        return False
