import os
import pygame
from data.scripts.Managers.WarehouseManager import WarehouseManager
from data.scripts.MapGenerator.Settings import TILE_SIZE

class BuildingManager:
    BUILDINGS_CONFIG = None

    def __init__(self, game, tilemap):
        self.game = game
        self.tilemap = tilemap
        self.buildings = []
        self.preview_position = None
        self.preview_valid = False
        self.preview_image = None
        self.selected_building = None  # Das aktuell ausgewählte Gebäude

        self.load_buildings()

    def load_buildings(self, path='data/config/Buildings.json'):
        """Lädt die Gebäude-Konfigurationen und die zugehörigen Grafiken."""
        with open(path) as f:
            import json
            self.BUILDINGS_CONFIG = json.load(f)

        self.textures = {}
        for building, data in self.BUILDINGS_CONFIG['buildings'].items():
            if "texture" in data:  # ✅ Normale Gebäude mit einer einzigen Textur
                texture_path = f"data/img/Buildings/{data['texture']}"
                if os.path.exists(texture_path):
                    self.textures[building] = pygame.image.load(texture_path)
                else:
                    print(f"⚠ WARNUNG: Gebäude-Textur {texture_path} nicht gefunden!")

    def start_building_mode(self, building_name):
        """Aktiviert den Bau-Modus für ein Gebäude."""
        if building_name in self.BUILDINGS_CONFIG['buildings']:
            self.selected_building = self.BUILDINGS_CONFIG['buildings'][building_name]
            self.preview_image = self.textures[building_name].copy()
            self.preview_image.set_alpha(150)  # Transparenter Vorschau-Effekt
            print(f"🏗️ Bau-Modus für {building_name} gestartet")

    def update_preview(self, mouse_pos, camera):
        """Aktualisiert die Position und Gültigkeit der Bauvorschau basierend auf der Mausposition."""
        if not self.selected_building:
            return

        # 🎯 Mausposition in Weltkoordinaten umrechnen
        world_x = (mouse_pos[0] / camera.zoom) + (camera.tile_x * TILE_SIZE)
        world_y = (mouse_pos[1] / camera.zoom) + (camera.tile_y * TILE_SIZE)
        tile_x = int(world_x // TILE_SIZE)
        tile_y = int(world_y // TILE_SIZE)

        # 🏗️ Überprüfe, ob das Tile ein gültiger Bauplatz ist
        if 0 <= tile_x < self.tilemap.width and 0 <= tile_y < self.tilemap.height:
            tile_base = self.tilemap.map[tile_y][tile_x].base
            self.preview_valid = tile_base in ["Grass", "South_Sand"]
        else:
            self.preview_valid = False

        self.preview_position = (tile_x, tile_y)

    def place_building(self):
        """Platziert das Gebäude auf der Karte mit dem richtigen Hauptschlüssel."""
        if not self.selected_building or not self.preview_valid or not self.preview_position:
            print("❌ Kein gültiger Bauplatz!")
            return

        x, y = self.preview_position
        cost = self.selected_building["cost"]

        # 🏝 Insel-ID bestimmen
        island_id = self.tilemap.get_island_id(x, y)
        if island_id is None:
            print("❌ Kann nicht bauen – keine Insel erkannt!")
            return

        # 🔍 **Kontor auf der Insel finden**
        kontor = self.game.office_manager.get_office_by_island(island_id)
        if not kontor:
            print("❌ Kein Kontor auf dieser Insel!")
            return

        warehouse = kontor["warehouse"]

        # 📦 **Überprüfen, ob genug Ressourcen vorhanden sind**
        for resource, amount in cost.items():
            if warehouse.get_quantity(resource) < amount:
                print(f"❌ Nicht genug {resource} im Lager!")
                return

        # 📦 **Ressourcen abziehen**
        for resource, amount in cost.items():
            warehouse.remove_good(resource, amount)

        # 🔑 **Hauptschlüssel aus `BUILDINGS_CONFIG` finden**
        building_key = None
        for key, value in self.BUILDINGS_CONFIG["buildings"].items():
            if value == self.selected_building:
                building_key = key
                break

        if not building_key:
            print("❌ Fehler: Kein gültiger Gebäude-Schlüssel gefunden!")
            return

        # 🏗 **Gebäude platzieren mit Hauptschlüssel**
        new_building = {
            "type": building_key,  # ✅ Hauptschlüssel verwenden (z. B. "lumberjack" statt "Holzfäller")
            "pos": (x, y),
            "island_id": island_id
        }
        self.buildings.append(new_building)
        self.tilemap.map[y][x].overlay = building_key  # 🔥 Gebäude als Overlay setzen!
        print(f"✅ {building_key} erfolgreich gebaut an {x}, {y} auf Insel {island_id}")

        # 🚫 **Bau-Modus beenden**
        self.selected_building = None
        self.preview_position = None

    def cancel_building(self):
        """Bricht den Bau-Modus ab und entfernt die Bauvorschau."""
        if self.selected_building:
            print(f"🚫 Bau-Modus für {self.selected_building['name']} abgebrochen!")
        
        self.selected_building = None  # Bau-Modus deaktivieren
        self.preview_position = None
        self.preview_valid = False
        self.preview_image = None

    def draw_preview(self, screen, camera):
        """Zeichnet die Bauvorschau für das Kontor mit Skalierung & richtiger Position."""
        if not self.preview_position or not self.preview_image:
            return

        tile_x, tile_y = self.preview_position
        screen_x, screen_y = camera.apply((tile_x * TILE_SIZE, tile_y * TILE_SIZE))

        # 📏 Skaliere das Bild basierend auf dem Zoom-Level
        scaled_size = int(TILE_SIZE * camera.zoom)
        preview_scaled = pygame.transform.scale(self.preview_image, (scaled_size, scaled_size))

        # 🔥 Zeichne das skaliertes Bild an der richtigen Position
        screen.blit(preview_scaled, (screen_x, screen_y))

    def draw_buildings(self, screen, camera):
        """Zeichnet alle gebauten Gebäude. (Verhindert doppelte Anzeige)"""
        for building in self.buildings:
            x, y = building["pos"]

            # **Fix: Zeichne das Gebäude nur, wenn es nicht schon als Overlay in der Tilemap existiert**
            if self.tilemap.map[y][x].overlay != building["type"]:
                texture = self.textures[building["type"]]

                # 📏 **Fix: Skaliere das Bild nicht mit der Zoomstufe**
                scaled_texture = pygame.transform.scale(texture, (TILE_SIZE, TILE_SIZE))
                screen_x, screen_y = camera.apply((x * TILE_SIZE, y * TILE_SIZE))

                screen.blit(scaled_texture, (screen_x, screen_y))