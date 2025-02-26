import os
import pygame
from data.scripts.Managers.WarehouseManager import WarehouseManager
from data.scripts.MapGenerator.Settings import TILE_SIZE

class BuildingManager:
    BUILDINGS_CONFIG = None

    def __init__(self, tilemap):
        self.tilemap = tilemap
        self.buildings = []
        self.preview_position = None
        self.preview_valid = False
        self.preview_image = None
        self.selected_ship = None  # Das Schiff, das baut

        self.load_buildings()

    def load_buildings(self, path='data/config/Buildings.json'):
        """Lädt die Gebäude-Konfigurationen und die zugehörigen Grafiken."""
        with open(path) as f:
            import json
            self.BUILDINGS_CONFIG = json.load(f)

            # ✅ Lade alle Grafiken für das Kontor (mit allen Himmelsrichtungen)
            self.textures = {}
            for building, data in self.BUILDINGS_CONFIG['buildings'].items():
                self.textures[building] = {}
                if "textures" in data:
                    for direction, filename in data["textures"].items():
                        texture_path = f"data/img/Buildings/{filename}"
                        if os.path.exists(texture_path):
                            self.textures[building][direction] = pygame.image.load(texture_path)
                        else:
                            print(f"⚠ WARNUNG: Gebäude-Textur {texture_path} nicht gefunden!")

    def start_building_office(self, ship):
        """Startet den Bauvorgang und zeigt sofort die Vorschau."""
        self.selected_ship = ship
        self.preview_position = None
        self.preview_valid = False

        # 🔥 Sofort die Vorschau aktivieren
        mouse_pos = pygame.mouse.get_pos()
        self.update_preview(mouse_pos, ship.game.camera)

    def update_preview(self, mouse_pos, camera):
        """Aktualisiert die Position und Farbe der Bauvorschau basierend auf der Mausposition."""
        if not self.selected_ship:
            return

        # 🎯 Mausposition in Weltkoordinaten umrechnen
        world_x = (mouse_pos[0] / camera.zoom) + (camera.tile_x * TILE_SIZE)
        world_y = (mouse_pos[1] / camera.zoom) + (camera.tile_y * TILE_SIZE)
        tile_x = int(world_x // TILE_SIZE)
        tile_y = int(world_y // TILE_SIZE)

        # 📏 Berechne die Distanz zum Schiff in Tiles
        ship_x, ship_y = int(self.selected_ship.pos_x // TILE_SIZE), int(self.selected_ship.pos_y // TILE_SIZE)
        distance = abs(ship_x - tile_x) + abs(ship_y - tile_y)  # Manhattan-Distanz

        if distance > 8:  # 🔥 Falls das Tile zu weit weg ist, keine Vorschau anzeigen!
            self.preview_position = None
            self.preview_valid = False
            self.preview_image = None
            return

        # 🏗️ Überprüfen, ob das Tile ein gültiger Bauplatz ist
        valid, direction = self.is_valid_office_location(tile_x, tile_y)

        # 🖼️ Setze die Vorschau-Daten
        self.preview_position = (tile_x, tile_y)
        self.preview_valid = valid
        if valid:
            self.preview_image = self.textures['office'][direction]
        else:
            self.preview_image = self.textures['office'][direction].copy()
            self.preview_image.fill((255, 0, 0, 100), special_flags=pygame.BLEND_RGBA_MULT)

    def is_valid_office_location(self, x, y):
        """Prüft, ob das Kontor hier gebaut werden kann und bestimmt die Richtung."""
        if y < 0 or y >= self.tilemap.height or x < 0 or x >= self.tilemap.width:
            return False, None

        tile = self.tilemap.map[y][x].base
        direction_map = {
            "Coast_Bottom_Middle": "South",
            "Coast_Middle_Left": "West",
            "Coast_Middle_Right": "East",
            "Coast_Top_Middle": "North",
            "Coast_South_Bottom_Middle": "South",
            "Coast_South_Middle_Left": "West",
            "Coast_South_Middle_Right": "East",
            "Coast_South_Top_Middle": "North"
        }
        return (tile in direction_map), direction_map.get(tile, "South")

    def place_office(self):
        """Platziert das Kontor und verknüpft es mit einer Insel."""
        if not self.preview_valid or not self.selected_ship:
            return

        x, y = self.preview_position

        # 📏 Berechne die Distanz zum Schiff in Tiles
        ship_x, ship_y = int(self.selected_ship.pos_x // TILE_SIZE), int(self.selected_ship.pos_y // TILE_SIZE)
        distance = abs(ship_x - x) + abs(ship_y - y)

        if distance > 8:  # 🚨 Falls das Schiff zu weit weg ist, abbrechen
            print("❌ Kontor kann nicht so weit entfernt gebaut werden!")
            return

        direction = self.is_valid_office_location(x, y)[1]

        # 🏝 Insel-ID bestimmen
        island_id = self.tilemap.get_island_id(x, y)
        if island_id is None:
            print("❌ Fehler: Dieses Tile gehört zu keiner validen Insel.")
            return

        # ❌ Überprüfen, ob bereits ein Kontor auf dieser Insel existiert
        for building in self.buildings:
            if building.get("island_id") == island_id:
                print(f"❌ Auf Insel {island_id} existiert bereits ein Kontor!")
                return

        # 📦 Überprüfen, ob das Schiff genug Ressourcen hat
        cost = self.BUILDINGS_CONFIG['buildings']['office']['cost']
        for good, amount in cost.items():
            if self.selected_ship.warehouse.get_quantity(good) < amount:
                print(f"❌ Nicht genug {good} im Schiffslager!")
                return

        # 📦 Ressourcen vom Schiff abziehen
        for good, amount in cost.items():
            self.selected_ship.warehouse.remove_good(good, amount)

        # 🏗️ Kontor in die Gebäude-Liste einfügen (mit `island_id` und `sub_id=0`)
        new_building = {
            "type": "office",
            "pos": (x, y),
            "direction": direction,
            "warehouse": WarehouseManager(self.BUILDINGS_CONFIG['buildings']['office']['storage_slots'], island_id, sub_id=0),
            "island_id": island_id,  # 🔥 Insel-ID sicher setzen!
            "sub_id": 0  # 🔥 Jedes Kontor bekommt sub_id = 0 (da es pro Insel nur eins gibt)
        }
        self.buildings.append(new_building)
        print(f"✅ Kontor gebaut an ({x}, {y}) auf Insel {island_id} mit Blickrichtung {direction}")

        # 🔥 Zurücksetzen nach dem Bau
        self.selected_ship = None
        self.preview_position = None
        self.preview_valid = False

    def validate_island_ids(self):
        """Validiert, dass jedes Gebäude eine Insel-ID hat."""
        for building in self.buildings:
            if "island_id" not in building or building["island_id"] is None:
                x, y = building["pos"]
                island_id = self.tilemap.get_island_id(x, y)
                if island_id is not None:
                    building["island_id"] = island_id
                    print(f"🔄 Gebäude an ({x}, {y}) nachträglich mit Insel {island_id} verknüpft.")

    def cancel_building(self):
        """Bricht den Bau-Modus ab und entfernt die Bauvorschau."""
        if self.selected_ship:
            print("🚫 Bau-Modus beendet, Vorschau entfernt!")
            self.selected_ship = None  # Bau-Modus deaktivieren
            self.preview_position = None
            self.preview_valid = False

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
        """Zeichnet alle gebauten Gebäude auf der Karte."""
        for building in self.buildings:
            x, y = building["pos"]
            direction = building["direction"]
            texture = self.textures["office"][direction]

            # 📏 Skaliere das Bild basierend auf dem Zoom-Level
            scaled_size = int(TILE_SIZE * camera.zoom)
            scaled_texture = pygame.transform.scale(texture, (scaled_size, scaled_size))

            # 🎯 Weltkoordinaten in Bildschirmkoordinaten umrechnen
            screen_x, screen_y = camera.apply((x * TILE_SIZE, y * TILE_SIZE))

            # 🔥 Gebäude rendern
            screen.blit(scaled_texture, (screen_x, screen_y))
