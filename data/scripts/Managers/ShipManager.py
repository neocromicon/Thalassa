import heapq
import pygame
import os
import json
import random
import math
from data.scripts.GUI.Game.ShipsGUI import ShipGUI
from data.scripts.Managers.WarehouseManager import WarehouseManager
from data.scripts.MapGenerator.Settings import SCREEN_HEIGHT, SCREEN_WIDTH, SHIP_PATH, TILE_SIZE

class ShipManager:
    SHIP_CONFIG = None
    def __init__(self, game, tilemap, ship_type='M', is_initial_ship=True):
        if not ShipManager.SHIP_CONFIG:
            self.load_ship_config()
            
        config = ShipManager.SHIP_CONFIG['ship_types'][ship_type]
        self.game = game
        self.tilemap = tilemap
        self.ship_type = ship_type
        self.speed = config['speed']
        
        # **Starte mit Pixel-Koordinaten, nicht Tile-basiert**
        start_x, start_y = self.find_random_ocean_pixel(tilemap)
        self.pos_x = start_x
        self.pos_y = start_y
        
        self.velocity_x = 0
        self.velocity_y = 0
        self.target_queue = []
        self.direction = "S"
        self.last_position = (self.pos_x, self.pos_y)  # Speichert die letzte Position
        self.stop_timer = None  # Timer für Bewegungsstopp

        self.ship_images = {
            dir: pygame.image.load(os.path.join(SHIP_PATH, self.ship_type, img))
            for dir, img in config['graphics'].items()
        }

        self.warehouse = WarehouseManager()
        self.gui = ShipGUI(self)
        self.selected = False
        self.init_storage_slots(config["storage_slots"]) 
        # Nur bei Initialschiffen Waren hinzufügen
        if is_initial_ship:
            initial_goods = config.get('initial_goods', {})
            for good, amount in initial_goods.items():
                if not self.warehouse.add_good(good, amount):
                    print(f"Fehler: {amount} {good} passten nicht ins Lager")

    @classmethod
    def load_ship_config(cls, config_path='data/config/Ships.json'):
        try:
            with open(config_path) as f:
                cls.SHIP_CONFIG = json.load(f)
        except FileNotFoundError:
            print(f"FEHLER: Schiffskonfiguration {config_path} nicht gefunden!")
            cls.SHIP_CONFIG = {'ship_types': {}}

    def init_storage_slots(self, num_slots):
        """ Initialisiert das Inventar mit der richtigen Anzahl an Slots."""
        self.warehouse.slots = {f"slot_{i}": {"good": None, "quantity": 0, "max_quantity": 50} 
                                for i in range(num_slots)}

    def update_build_status(self, office_manager):
        """🏗 Aktualisiert, ob ein Bau möglich ist."""
        self.can_build = False  # Standard: Kann nicht bauen

        # 🏝 1. Liegt das Schiff in der Nähe einer Insel (Küste)?
        nearest_coast = self.find_nearest_coast()
        if not nearest_coast:
            return  # ❌ Kein Bau möglich

        # 📦 2. Hat das Schiff die benötigten Ressourcen?
        required_resources = office_manager.BUILDINGS_CONFIG['buildings']['office']['cost']
        has_resources = all(
            self.warehouse.get_quantity(good) >= amount
            for good, amount in required_resources.items()
        )

        # ✅ 3. Wenn Ressourcen vorhanden & Schiff nahe genug an einer Küste -> Bau möglich
        if has_resources:
            self.can_build = True

    def _is_near_warehouse_internal(self, max_distance=TILE_SIZE * 2):
        """
        Interne Version von is_near_warehouse(), die von anderen Funktionen genutzt werden kann,
        ohne eine Endlosschleife zu verursachen.
        """
        ship_x, ship_y = self.pos_x, self.pos_y  

        for building in self.game.office_manager.buildings:
            if building["type"] == "office":
                kontor_x, kontor_y = building["pos"]
                kontor_x = kontor_x * TILE_SIZE + TILE_SIZE // 2  
                kontor_y = kontor_y * TILE_SIZE + TILE_SIZE // 2

                distance = ((ship_x - kontor_x) ** 2 + (ship_y - kontor_y) ** 2) ** 0.5

                if distance < max_distance:
                    return True  # ✅ Schiff ist in der Nähe eines Kontors

        return False  # ❌ Kein Schiff in der Nähe

    def is_near_warehouse(self, max_distance=TILE_SIZE * 2, return_gui=False):
        """
        Findet das nächste Kontor in der Nähe.
        
        - `return_gui=False`  -> Gibt das `WarehouseManager` zurück (für den Warentransfer).
        - `return_gui=True`   -> Gibt die `WarehouseGUI` zurück (für das GUI-Handling).
        """
        ship_x, ship_y = self.pos_x, self.pos_y  
        nearest_warehouse = None
        nearest_gui = None

        for building in self.game.office_manager.buildings:
            if building["type"] == "office":
                kontor_x, kontor_y = building["pos"]
                kontor_x = kontor_x * TILE_SIZE + TILE_SIZE // 2  
                kontor_y = kontor_y * TILE_SIZE + TILE_SIZE // 2

                distance = ((ship_x - kontor_x) ** 2 + (ship_y - kontor_y) ** 2) ** 0.5

                if distance < max_distance:
                    nearest_warehouse = building["warehouse"]  # ✅ WarehouseManager
                    nearest_gui = nearest_warehouse.gui  # ✅ WarehouseGUI
                    if not nearest_gui.manually_opened and self in self.game.selected_ships:
                        nearest_gui.show_gui = True
                    break  

        # **Falls das Schiff sich entfernt hat, GUI schließen (sofern nicht manuell geöffnet)**
        for building in self.game.office_manager.buildings:
            warehouse_gui = building["warehouse"].gui
            ships_near_warehouse = any(ship._is_near_warehouse_internal() for ship in self.game.ships)

            if not ships_near_warehouse and not warehouse_gui.manually_opened:
                print("❌ [DEBUG] Kein Schiff mehr in der Nähe → WarehouseGUI wird geschlossen.")
                warehouse_gui.show_gui = False


        return nearest_gui if return_gui else nearest_warehouse  # ✅ Je nach Modus das richtige zurückgeben

    def find_nearest_coast(self, max_distance=3):
        """🏝 Findet das nächstgelegene Küsten-Tile in einem definierten Umkreis."""
        tile_x = int(self.pos_x // TILE_SIZE)  # **Pixel zu Tile-Koordinaten umrechnen**
        tile_y = int(self.pos_y // TILE_SIZE)

        for radius in range(1, max_distance + 1):
            for dx in range(-radius, radius + 1):
                for dy in range(-radius, radius + 1):
                    x = tile_x + dx
                    y = tile_y + dy

                    # 🛑 **Grenzprüfung**
                    if 0 <= x < self.tilemap.width and 0 <= y < self.tilemap.height:
                        if self.tilemap.map[y][x].base.startswith("Coast"):
                            return (x, y)  # ✅ Küste gefunden

        return None  # ❌ Keine Küste gefunden

    @staticmethod
    def find_random_ocean_pixel(tilemap):
        """Findet eine zufällige Pixelposition im Ozean"""
        ocean_tiles = [(x, y) for y in range(tilemap.height) for x in range(tilemap.width)
                    if tilemap.map[y][x].base.startswith("Ocean")]

        if ocean_tiles:
            tile_x, tile_y = random.choice(ocean_tiles)
            return tile_x * 32 + 16, tile_y * 32 + 16  # Zentrum des Tiles
        return 0, 0

    def find_nearby_ocean_pixel(tilemap, base_x, base_y, ships, min_distance=64, max_distance=96):
        """Findet eine zufällige Pixelposition 64-96 Pixel entfernt auf Ozean, ohne ein anderes Schiff zu treffen."""
        ocean_tiles = [(x, y) for y in range(tilemap.height) for x in range(tilemap.width)
                    if tilemap.map[y][x].base.startswith("Ocean")]

        random.shuffle(ocean_tiles)  # Zufällige Reihenfolge

        for tile_x, tile_y in ocean_tiles:
            ocean_x = tile_x * 32 + 16
            ocean_y = tile_y * 32 + 16

            # Abstand berechnen (Pixel-Ebene)
            distance = ((ocean_x - base_x) ** 2 + (ocean_y - base_y) ** 2) ** 0.5
            if min_distance <= distance <= max_distance:

                # Stelle sicher, dass kein Schiff dort ist
                if any(abs(ship.pos_x - ocean_x) < 32 and abs(ship.pos_y - ocean_y) < 32 for ship in ships):
                    continue

                return ocean_x, ocean_y  # Gültige Position gefunden

        return base_x, base_y  # Falls nichts gefunden wird, bleibt es am alten Ort

    def is_clicked(self, mouse_x, mouse_y, camera):
        """Prüft, ob das Schiff zuverlässig angeklickt wurde."""
        pos_x, pos_y = camera.apply((self.pos_x, self.pos_y))

        # Sicherstellen, dass das Schiff zentriert gezeichnet wird
        scaled_size = round(TILE_SIZE * camera.zoom)  # Skalierung an TILE_SIZE ausrichten
        ship_rect = pygame.Rect(
            pos_x - scaled_size // 2,  # Zentrierung
            pos_y - scaled_size // 2,  
            scaled_size, 
            scaled_size
        )

        return ship_rect.collidepoint(mouse_x, mouse_y)

    def is_clicked_in_rect(self, selection_rect, camera):
        """Prüft, ob das Schiff innerhalb des Auswahlrahmens liegt."""
        pos_x, pos_y = camera.apply((self.pos_x, self.pos_y))
        ship_rect = pygame.Rect(pos_x, pos_y, 32, 32)

        return selection_rect.colliderect(ship_rect)

    def is_valid_tile(self, tile):
        """Prüft, ob ein Tile befahrbar ist."""
        x, y = tile
        if 0 <= x < self.tilemap.width and 0 <= y < self.tilemap.height:
            tile_base = self.tilemap.map[y][x].base
            return tile_base.startswith(("Ocean", "Water", "Coast"))
        return False

    def find_nearest_valid_tile(self, target_x, target_y, max_radius=5):
        """Sucht das nächstgelegene befahrbare Tile um das verbotene Ziel herum."""
        for radius in range(1, max_radius + 1):
            for dx in range(-radius, radius + 1):
                for dy in range(-radius, radius + 1):
                    x = target_x + dx
                    y = target_y + dy
                    if self.is_valid_tile((x, y)):
                        print(f"✅ Alternativer Zielpunkt gefunden: ({x}, {y})")
                        return (x, y)
        return None  # Falls kein befahrbares Tile gefunden wurde

    def move_group_to(game, target_x, target_y):
        """Bewegt eine Gruppe von Schiffen und verteilt sie um das Ziel herum."""
        
        selected_ships = game.selected_ships
        num_ships = len(selected_ships)

        if num_ships == 0:
            return

        print(f"🚢 {num_ships} Schiffe bewegen sich nach ({target_x}, {target_y}) mit Formation.")

        # Offsets für Formationsanordnung (3x3, falls genug Schiffe vorhanden)
        offsets = [
            (-TILE_SIZE, -TILE_SIZE), (0, -TILE_SIZE), (TILE_SIZE, -TILE_SIZE),
            (-TILE_SIZE, 0),          (0, 0),          (TILE_SIZE, 0),
            (-TILE_SIZE, TILE_SIZE),  (0, TILE_SIZE),  (TILE_SIZE, TILE_SIZE),
        ]

        # Sortiere Schiffe nach Entfernung zum Ziel, damit nahe Schiffe zuerst zugewiesen werden
        selected_ships.sort(key=lambda ship: math.hypot(ship.pos_x - target_x, ship.pos_y - target_y))

        for index, ship in enumerate(selected_ships):
            offset_x, offset_y = offsets[index % len(offsets)]  # Wiederhole Offset-Muster falls mehr Schiffe
            new_target_x = target_x + offset_x
            new_target_y = target_y + offset_y

            # **Nur bewegen, wenn das Ziel befahrbar ist**
            if not ship.is_valid_tile((int(new_target_x // TILE_SIZE), int(new_target_y // TILE_SIZE))):
                alternative_target = ship.find_nearest_valid_tile(int(new_target_x // TILE_SIZE), int(new_target_y // TILE_SIZE))
                if alternative_target:
                    new_target_x, new_target_y = alternative_target[0] * TILE_SIZE, alternative_target[1] * TILE_SIZE
                else:
                    print(f"❌ Kein gültiger Platz für {ship.ship_type} gefunden. Schiff bleibt stehen.")
                    continue
            
            ship.move_to(new_target_x, new_target_y)
            print(f"✅ {ship.ship_type} fährt zu ({new_target_x}, {new_target_y})")

    def move_to(self, target_x, target_y):
        """Setzt eine Route zum Ziel oder zum nächstgelegenen befahrbaren Tile."""
        
        print(f"🚀 move_to aufgerufen mit Ziel: ({target_x}, {target_y})")

        start_tile = (int(self.pos_x // TILE_SIZE), int(self.pos_y // TILE_SIZE))
        target_tile = (int(target_x // TILE_SIZE), int(target_y // TILE_SIZE))

        print(f"🌍 Start-Tile: {start_tile}, Ziel-Tile: {target_tile}")

        # **Überprüfen, ob das Ziel ein Kontor ist**
        for building in self.game.office_manager.buildings:
            if building["type"] == "office" and building["pos"] == target_tile:
                print(f"❌ Ziel {target_tile} ist ein Kontor! Verschiebe Ziel...")

                # **Blickrichtung des Kontors bestimmen**
                direction = building["direction"]  # "North", "East", "South", "West"

                # **Neues Ziel basierend auf der Blickrichtung setzen**
                if direction == "North":
                    target_tile = (target_tile[0], target_tile[1] - 1)  # Oberhalb des Kontors
                elif direction == "East":
                    target_tile = (target_tile[0] + 1, target_tile[1])  # Rechts neben dem Kontor
                elif direction == "South":
                    target_tile = (target_tile[0], target_tile[1] + 1)  # Unterhalb des Kontors
                elif direction == "West":
                    target_tile = (target_tile[0] - 1, target_tile[1])  # Links neben dem Kontor

                print(f"✅ Neues Ziel: {target_tile}")

        # **Falls das Ziel nicht befahrbar ist, suche ein alternatives Ziel**
        if not self.is_valid_tile(target_tile):
            print(f"❌ Ziel {target_tile} ist nicht befahrbar! Suche Alternative...")

            new_target = self.find_nearest_valid_tile(target_tile[0], target_tile[1])
            if new_target:
                target_tile = new_target
                print(f"✅ Alternativer Zielpunkt: {target_tile}")
            else:
                print("❌ Kein alternatives Ziel gefunden!")
                return

        # **Pathfinding ausführen**
        path = self.find_path(start_tile, target_tile)

        if path:
            # Pfad in Pixel-Koordinaten umwandeln
            self.target_queue = [(x * TILE_SIZE + TILE_SIZE // 2, y * TILE_SIZE + TILE_SIZE // 2) for x, y in path]
            self.update_velocity()
            print(f"✅ Pfad gefunden: {path}")
        else:
            print(f"❌ Kein Pfad gefunden zu {target_tile}")

    def find_path(self, start, end):
        """Führt A*-Pathfinding aus und sucht eine alternative Position, falls das Ziel nicht befahrbar ist."""
        print(f"🛤️ Pathfinding von {start} nach {end} gestartet.")

        def heuristic(a, b):
            """Euklidische Distanz als Heuristik für A*."""
            return ((a[0] - b[0]) ** 2 + (a[1] - b[1]) ** 2) ** 0.5

        def is_valid(x, y):
            """Prüft, ob ein Tile befahrbar ist."""
            if 0 <= x < self.tilemap.width and 0 <= y < self.tilemap.height:
                tile_base = self.tilemap.map[y][x].base
                return tile_base.startswith(("Ocean", "Water", "Coast"))
            return False

        def find_nearest_valid_tile(target_x, target_y, max_radius=5):
            """Sucht das nächstgelegene befahrbare Tile um das verbotene Ziel herum."""
            for radius in range(1, max_radius + 1):
                for dx in range(-radius, radius + 1):
                    for dy in range(-radius, radius + 1):
                        x = target_x + dx
                        y = target_y + dy
                        if is_valid(x, y):
                            print(f"✅ Alternativer Zielpunkt gefunden: ({x}, {y})")
                            return (x, y)
            return None  # Falls kein befahrbares Tile gefunden wurde

        # Falls das Ziel nicht befahrbar ist, suche eine alternative Position
        if not is_valid(end[0], end[1]):
            print(f"❌ Ziel {end} ist nicht befahrbar! Suche Alternative...")
            new_end = find_nearest_valid_tile(end[0], end[1])

            if new_end:
                end = new_end
            else:
                print("❌ Kein alternatives Ziel gefunden!")
                return []

        print(f"🚢 Starte Pathfinding zu {end}")

        open_heap = []
        heapq.heappush(open_heap, (0, start))
        came_from = {}
        g_score = {start: 0}
        f_score = {start: heuristic(start, end)}

        while open_heap:
            _, current = heapq.heappop(open_heap)

            if current == end:
                path = []
                while current in came_from:
                    path.append(current)
                    current = came_from[current]
                path.reverse()
                print(f"✅ Path gefunden: {path}")
                return path

            for dx, dy in [(0,1), (1,0), (0,-1), (-1,0), (1,1), (-1,-1), (1,-1), (-1,1)]:
                neighbor = (current[0] + dx, current[1] + dy)
                if not is_valid(neighbor[0], neighbor[1]):
                    continue  

                move_cost = 1 if (dx == 0 or dy == 0) else 1.4142
                new_g = g_score.get(current, float('inf')) + move_cost

                if new_g < g_score.get(neighbor, float('inf')):
                    came_from[neighbor] = current
                    g_score[neighbor] = new_g
                    f_score[neighbor] = new_g + heuristic(neighbor, end)
                    heapq.heappush(open_heap, (f_score[neighbor], neighbor))

        print(f"❌ Kein Pfad zu {end} gefunden!")
        return []

    def update_velocity(self):
        """Berechnet die exakte Geschwindigkeit und Richtung zum Ziel."""
        if not self.target_queue:
            self.velocity_x, self.velocity_y = 0, 0
            return

        next_x, next_y = self.target_queue[0]
        dx = next_x - self.pos_x
        dy = next_y - self.pos_y
        distance = math.hypot(dx, dy)  # **Korrekte Distanzberechnung**

        if distance > 0.1:  # **Verhindert Stillstand oder ungenaue Bewegung**
            self.velocity_x = (dx / distance) * self.speed
            self.velocity_y = (dy / distance) * self.speed

            # **Fix: Setze Richtung anhand des Winkels**
            angle = (math.degrees(math.atan2(dy, dx)) + 360) % 360
            self.direction = self.get_direction_from_angle(angle)
        else:
            self.pos_x, self.pos_y = self.target_queue.pop(0)  # **Sofort am Ziel**
            self.update_velocity()

    def get_direction_from_angle(self, angle):
        """Berechnet die exakte Blickrichtung anhand des Bewegungswinkels"""
        
        # **Fix: Berechne den Winkel sauber im Bereich 0° bis 360°**
        angle = (angle + 360) % 360  

        # **Feinere Unterteilung für bessere Präzision**
        if 345 <= angle or angle < 15:
            return "E"   # Osten
        elif 15 <= angle < 75:
            return "SE"  # Südosten
        elif 75 <= angle < 105:
            return "S"   # Süden
        elif 105 <= angle < 165:
            return "SW"  # Südwesten
        elif 165 <= angle < 195:
            return "W"   # Westen
        elif 195 <= angle < 255:
            return "NW"  # Nordwesten
        elif 255 <= angle < 285:
            return "N"   # Norden
        elif 285 <= angle < 345:
            return "NE"  # Nordosten
        return "S"  # Falls kein Wert passt

    def update_position(self):
        """Bewegt das Schiff, stoppt es aber, falls es für eine Weile blockiert ist."""
        
        if not self.target_queue:
            return

        next_x, next_y = self.target_queue[0]
        current_time = pygame.time.get_ticks()

        # **1️⃣ Prüfen, ob das Schiff in einer Gruppe gesteuert wird**
        is_in_group = len(self.game.selected_ships) > 1

        # **2️⃣ Falls das Schiff in einer Gruppe ist und sich nicht bewegen kann**
        for other_ship in self.game.ships:
            if other_ship != self:
                dist = math.hypot(other_ship.pos_x - next_x, other_ship.pos_y - next_y)

                if dist < TILE_SIZE * 0.8:
                    if is_in_group:
                        print(f"🚨 {self.ship_type} stoppt, um Kollision mit {other_ship.ship_type} in Formation zu vermeiden.")

                        # **Starte Stop-Timer, wenn Schiff blockiert ist**
                        if self.stop_timer is None:
                            self.stop_timer = current_time  # Timer starten

                        # **Falls das Schiff 100ms blockiert war, leere die Ziel-Queue**
                        elif current_time - self.stop_timer >= 200:
                            print(f"⏳ {self.ship_type} hat sich 200ms nicht bewegt, stoppt Bewegung.")
                            self.target_queue.clear()
                            self.velocity_x, self.velocity_y = 0, 0
                            self.stop_timer = None
                        return  

                    else:
                        # 🚢 **Einzelschiff darf durch andere Schiffe hindurchfahren**
                        print(f"⚠️ {self.ship_type} fährt durch {other_ship.ship_type} hindurch.")
                        break  # **Nicht stoppen, sondern einfach weiterfahren**

        # **Falls das Schiff sich bewegt hat, Timer zurücksetzen**
        if (self.pos_x, self.pos_y) != self.last_position:
            self.stop_timer = None  # Timer löschen

        # **3️⃣ Falls das Schiff sich bewegt hat, Timer zurücksetzen**
        if (self.pos_x, self.pos_y) != self.last_position:
            self.stop_timer = None  # Timer löschen

        # **4️⃣ Falls keine Blockade vorliegt → normale Bewegung**
        self.pos_x += self.velocity_x
        self.pos_y += self.velocity_y
        self.last_position = (self.pos_x, self.pos_y)  # Position aktualisieren

        if math.hypot(self.pos_x - next_x, self.pos_y - next_y) < self.speed:
            self.pos_x, self.pos_y = self.target_queue.pop(0)
            self.update_velocity()

    def start_build_office(self):
        """Aktiviert den Bau-Modus für das Kontor."""
        if not self.game.office_manager:
            return
        
        print("🏗️ Baumenü für Kontor gestartet!")  # Debugging-Ausgabe
        self.game.office_manager.start_building_office(self)

    def transfer_to_warehouse(self, warehouse, slot_index):
        """Transferiert eine Ware vom Schiff ins Kontor der aktuellen Insel."""
        if warehouse is None:
            print("❌ Kein gültiges Kontor zum Entladen!")
            return False

        if not hasattr(warehouse, "island_id"):
            print("❌ Fehler: `warehouse` ist kein gültiger WarehouseManager!")
            return False

        island_id = warehouse.island_id
        if island_id is None:
            print("❌ Fehler: Kontor hat keine gültige Insel-ID!")
            return False

        if slot_index not in self.warehouse.slots:  # ✅ Jetzt sicher String-Index prüfen
            print(f"❌ Ungültiger Slot: {slot_index}")
            return False

        slot = self.warehouse.slots[slot_index]
        if slot["good"] is None or slot["quantity"] == 0:
            print("❌ Kein Gut zum Transferieren!")
            return False

        good_type = slot["good"]
        quantity_to_transfer = slot["quantity"]

        if warehouse.add_good(good_type, quantity_to_transfer):
            slot["quantity"] = 0
            slot["good"] = None
            print(f"✅ {quantity_to_transfer} {good_type} in Kontor auf Insel {island_id} eingelagert!")
            return True

        print(f"⚠️ Nicht genügend Platz im Kontor auf Insel {island_id}!")
        return False

    def transfer_from_warehouse(self, warehouse, slot_index):
        """Transferiert eine Ware vom Kontor ins Schiff."""
        if warehouse is None:
            print("❌ Kein gültiges Kontor zum Beladen!")
            return False

        if slot_index is None:
            print("❌ [DEBUG] Kein Slot wurde ausgewählt!")
            return False

        if isinstance(slot_index, str) and slot_index.startswith("slot_"):
            slot_index = int(slot_index.split("_")[1])

        if slot_index not in warehouse.slots:
            print(f"❌ [DEBUG] Ungültiger Slot: {slot_index}")
            return False

        slot = warehouse.slots[slot_index]  
        if slot["good"] is None or slot["quantity"] == 0:
            print(f"❌ [DEBUG] Keine Ware im Kontor-Slot {slot_index} verfügbar!")
            return False

        good_type = slot["good"]
        quantity_to_transfer = slot["quantity"]

        print(f"🔄 [DEBUG] Lade {quantity_to_transfer} {good_type} aus Kontor-Slot {slot_index} ins Schiff...")

        remaining_quantity = quantity_to_transfer
        for s_slot in self.warehouse.slots.values():
            if s_slot["good"] == good_type and s_slot["quantity"] < s_slot["max_quantity"]:
                transfer_amount = min(remaining_quantity, s_slot["max_quantity"] - s_slot["quantity"])
                s_slot["quantity"] += transfer_amount
                remaining_quantity -= transfer_amount

                if remaining_quantity == 0:
                    break  

        if remaining_quantity > 0:
            for s_slot in self.warehouse.slots.values():
                if s_slot["good"] is None:
                    s_slot["good"] = good_type
                    s_slot["quantity"] = min(remaining_quantity, s_slot["max_quantity"])
                    remaining_quantity -= s_slot["quantity"]
                    if remaining_quantity == 0:
                        break  

        slot["quantity"] -= (quantity_to_transfer - remaining_quantity)
        if slot["quantity"] == 0:
            slot["good"] = None  

        print(f"✅ [DEBUG] {quantity_to_transfer - remaining_quantity} {good_type} erfolgreich ins Schiff geladen!")

        if remaining_quantity > 0:
            print(f"⚠️ [DEBUG] Nicht genügend Platz im Schiff! {remaining_quantity} verbleiben im Kontor.")
        else:
            print(f"✅ [DEBUG] {quantity_to_transfer} {good_type} erfolgreich ins Schiff geladen!")

        warehouse.gui.selected_slot = None  

        return True

    def draw(self, screen, camera):
        """Zeichnet das Schiff in der gleichen relativen Größe wie die Tiles."""
        
        scaled_size = int(TILE_SIZE * camera.zoom)  
        image = pygame.transform.scale(
            self.ship_images[self.direction], 
            (scaled_size, scaled_size)
        )
        
        screen_x, screen_y = camera.apply((self.pos_x, self.pos_y))
        screen.blit(image, (screen_x - scaled_size // 2, screen_y - scaled_size // 2))
        
        # **Zeichne Auswahlrahmen um selektierte Schiffe**
        if self.selected:  
            pygame.draw.rect(
                screen, (255, 255, 0),  
                (screen_x - scaled_size // 2, screen_y - scaled_size // 2, scaled_size, scaled_size), 
                2  
            )
