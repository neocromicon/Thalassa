import os
from re import S
import pygame
import json
import sys

from regex import T
from data.scripts.GUI.Game.BuildingGUI import BuildingGUI
from data.scripts.GUI.Game.ResourceDisplayGUI import ResourceDisplayGUI
from data.scripts.GUI.MainIngameMenu import MainIngameMenu
from data.scripts.Managers.BuildingManager import BuildingManager
from data.scripts.Managers.OfficeManager import OfficeManager
from data.scripts.Managers.MouseManager import MouseManager
from data.scripts.Managers.ShipManager import ShipManager
from data.scripts.Managers.GoodManager import GoodManager
from data.scripts.Managers.TimeManager import TimeManager
from data.scripts.camera import Camera
from data.scripts.MapGenerator.Settings import TILE_SIZE, SCREEN_HEIGHT, SCREEN_WIDTH
from data.scripts.MapGenerator.TileMap import Tile, TileMap
from data.scripts.MapGenerator.MapRenderer import Renderer
from data.scripts.Managers.SettingsManager import SettingsManager

# Spiel-Klasse
class Game:
    def __init__(self, screen, map_width, map_height):
        print("Game-Instanz wurde erstellt!")
        self.screen = screen
        self.map_width = map_width
        self.map_height = map_height
        self.camera = Camera(self.map_width, self.map_height, self.map_width, self.map_height)
        self.renderer = Renderer()
        self.tilemap = None
        self.is_loaded = False
        self.frame = 0
        self.last_mouse_pos = None
        self.back_to_menu = False
        self.pause_game = False
        self.running = False
        self.show_crosshair = False  # Ob das Fadenkreuz sichtbar ist
        self.last_input_was_keyboard = False  # Speichert, ob die letzte Eingabe von der Tastatur war

        # **Schiff-Verwaltung**
        self.ship_manager = None
        self.ships = []
        self.selected_ships = []
        self.selection_active = False
        self.selection_start = None
        self.selection_end = None

        self.good_manager = GoodManager()
        self.office_manager = None  # Erstmal None setzen
        self.good_manager.load_goods()
        self.resource_display = ResourceDisplayGUI(self)
        self.mouse_manager = MouseManager(self)

        # Tag-Nacht-Zyklus
        self.time_manager = TimeManager()

    def set_tilemap(self, tilemap):
        """Setzt die Tilemap nach der Generierung und spawnt mehrere Schiffe."""
        self.tilemap = tilemap
        self.camera.set_bounds(self.tilemap.bottom_right_edge)
        self.office_manager = OfficeManager(self.tilemap)
        self.office_manager.validate_island_ids()
        self.building_manager = BuildingManager(self, self.tilemap)
        self.building_gui = BuildingGUI(self)
        self.renderer.load_building_textures(self.building_manager)

        # 🌊 **Erstes Schiff nur auf Ocean-Tiles spawnen**
        first_x, first_y = ShipManager.find_random_ocean_pixel(self.tilemap)
        first_ship = ShipManager(game=self, tilemap=self.tilemap, ship_type='M', is_initial_ship=True)
        first_ship.pos_x = first_x
        first_ship.pos_y = first_y

        # 🚢 **Zweites Schiff sicher 64-96 Pixel entfernt spawnen**
        second_x, second_y = ShipManager.find_nearby_ocean_pixel(self.tilemap, first_x, first_y, [first_ship])

        second_ship = ShipManager(game=self, tilemap=self.tilemap, ship_type='S', is_initial_ship=True)
        second_ship.pos_x = second_x
        second_ship.pos_y = second_y

        # Speichere die Schiffe in einer Liste
        self.ships = [first_ship, second_ship]

    def camera_to_ship(self):
        """Zentriert die Kamera direkt auf das erste Schiff in der Liste."""
        if self.ships:
            first_ship = self.ships[0]  # Erstes Schiff auswählen
            ship_x, ship_y = first_ship.pos_x, first_ship.pos_y

            # Berechne die Kameraposition in Tile-Koordinaten
            self.camera.tile_x = (ship_x / TILE_SIZE) - (SCREEN_WIDTH / TILE_SIZE) / 2
            self.camera.tile_y = (ship_y / TILE_SIZE) - (SCREEN_HEIGHT / TILE_SIZE) / 2

            # Stelle sicher, dass die Kamera nicht außerhalb der Karte startet
            self.camera.tile_x = max(0, min(self.camera.tile_x, self.tilemap.width - SCREEN_WIDTH / TILE_SIZE))
            self.camera.tile_y = max(0, min(self.camera.tile_y, self.tilemap.height - SCREEN_HEIGHT / TILE_SIZE))

    def run(self):
        self.pause_game = False  # Reset des Pause-Status bei jedem Spielstart
        self.camera.load_settings()  # **Mauseinstellungen direkt laden!**

        if self.tilemap:
            self.camera_to_ship()

        while not self.back_to_menu:
            self.handle_events()

            if not self.pause_game:  # Nur wenn das Spiel nicht pausiert ist, weiterlaufen lassen
                self.update()
                self.draw()
                pygame.display.flip()

    def draw_crosshair(self):
        """Zeichnet das Fadenkreuz in die Mitte des Bildschirms, wenn die Tastatur benutzt wird."""
        if not self.show_crosshair:
            return

        screen_center_x = self.screen.get_width() // 2
        screen_center_y = self.screen.get_height() // 2
        color = (255, 255, 255)  # Weißes Fadenkreuz

        pygame.draw.line(self.screen, color, (screen_center_x - 5, screen_center_y), (screen_center_x + 5, screen_center_y), 2)  # Horizontale Linie
        pygame.draw.line(self.screen, color, (screen_center_x, screen_center_y - 5), (screen_center_x, screen_center_y + 5), 2)  # Vertikale Linie

    def handle_events(self):
        move_speed = 50 * (1 + (self.camera.zoom - 1) * 0.5)
        crosshair_x = (self.screen.get_width() // 2 + self.camera.tile_x) / self.camera.zoom
        crosshair_y = (self.screen.get_height() // 2 + self.camera.tile_y) / self.camera.zoom
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:
                    print("ESC wurde gedrückt! Ingame-Menü wird geöffnet.")
                    self.pause_game = True  
                    menu = MainIngameMenu(self.screen, self)  # Erstelle eine Instanz des Ingame-Menüs
                    menu.run()
                if event.key == pygame.K_b:  
                    self.building_gui.show_gui = not self.building_gui.show_gui
            self.handle_mouse(event)

        keys = pygame.key.get_pressed()
        if keys[pygame.K_w] or keys[pygame.K_UP]:
            self.camera.move_with_keyboard(0, -move_speed)
            self.show_crosshair = True
            self.last_input_was_keyboard = True

        if keys[pygame.K_s] or keys[pygame.K_DOWN]:
            self.camera.move_with_keyboard(0, move_speed)
            self.show_crosshair = True
            self.last_input_was_keyboard = True

        if keys[pygame.K_a] or keys[pygame.K_LEFT]:
            self.camera.move_with_keyboard(-move_speed, 0)
            self.show_crosshair = True
            self.last_input_was_keyboard = True

        if keys[pygame.K_d] or keys[pygame.K_RIGHT]:
            self.camera.move_with_keyboard(move_speed, 0)
            self.show_crosshair = True
            self.last_input_was_keyboard = True

        if keys[pygame.K_PLUS] or keys[pygame.K_KP_PLUS]:  # "+" oder Numpad "+"
            self.camera.apply_zoom_with_crosshair(self, SettingsManager.load_setting("keyboard_zoom_sensitivity", 0.1))
            self.show_crosshair = True
            self.last_input_was_keyboard = True

        if keys[pygame.K_MINUS] or keys[pygame.K_KP_MINUS]:  # "-" oder Numpad "-"
            self.camera.apply_zoom_with_crosshair(self, -SettingsManager.load_setting("keyboard_zoom_sensitivity", 0.1))
            self.show_crosshair = True
            self.last_input_was_keyboard = True

    def handle_mouse(self, event):
        """Verarbeitet Mausbewegungen, Klicken und Zoomen mit gespeicherten Einstellungen."""
        mouse_x, mouse_y = pygame.mouse.get_pos()

        # **Sobald die Maus bewegt oder geklickt wird → Crosshair ausblenden**
        if event.type in [pygame.MOUSEBUTTONDOWN, pygame.MOUSEMOTION]:
            self.show_crosshair = False

        if self.office_manager.selected_ship:
            self.office_manager.update_preview((mouse_x, mouse_y), self.camera)

        if event.type == pygame.MOUSEBUTTONDOWN:                
            if self.building_gui.handle_click(pygame.mouse.get_pos()):
                return

            self.mouse_manager.handle_left_click(event, mouse_x, mouse_y)           

        elif event.type == pygame.MOUSEMOTION:  # 🆕 **Kamera bewegen**
            self.mouse_manager.handle_mouse_motion(mouse_x, mouse_y)
            # Falls das Baumenü aktiv ist, übergebe die Mausposition an `handle_hover()`
            if self.building_gui and self.building_gui.show_gui:
                self.building_gui.handle_hover((mouse_x, mouse_y))

            if self.building_manager.selected_building:
                self.building_manager.update_preview((mouse_x, mouse_y), self.camera)

        elif event.type == pygame.MOUSEBUTTONUP:
            self.mouse_manager.handle_mouse_release(event, mouse_x, mouse_y)
                
    def update(self):
        self.frame += 1
        self.time_manager.update()
        # Aktualisiere alle Schiffe
        for ship in self.ships:
            ship.update_position()
            
        # Aktualisiere Bau-Status für alle ausgewählten Schiffe
        if self.selected_ships:
            for ship in self.selected_ships:
                ship.update_build_status(self.office_manager)

    def debug_island_id_center_camera(self, screen):
        """Ermittelt die Insel-ID der Insel, die der Kameramitte am nächsten ist und visualisiert den Suchradius."""
        center_x, center_y = self.camera.get_center_tile()
        #print(f"📍 [DEBUG] Kameramitte auf Tile ({center_x}, {center_y})")

        # **Direkte Überprüfung der Kameraposition**
        island_id = self.tilemap.get_island_id(center_x, center_y)
        if island_id is not None:
            #print(f"🎯 [DEBUG] Kamera direkt über Insel {island_id}")
            return island_id  # Falls direkt eine Insel erkannt wurde, sofort zurückgeben!

        # **Erweiterte Suche um die Kameraposition herum**
        scan_range = 15  # 🔄 Suchradius bleibt 15 Tiles
        island_candidates = []

        for dx in range(-scan_range, scan_range + 1):
            for dy in range(-scan_range, scan_range + 1):
                tile_x, tile_y = center_x + dx, center_y + dy
                if 0 <= tile_x < self.tilemap.width and 0 <= tile_y < self.tilemap.height:
                    island_id = self.tilemap.get_island_id(tile_x, tile_y)
                    if island_id is not None:
                        distance = (dx ** 2 + dy ** 2) ** 0.5  # 🔵 Echte Distanz statt Manhattan
                        island_candidates.append((island_id, distance))

        if not island_candidates:
            #print("🌊 [DEBUG] Kamera ist über Wasser – Keine Insel erkannt.")
            return None

        # **Nächstgelegene Insel-ID bestimmen**
        closest_island = min(island_candidates, key=lambda x: x[1])[0]
        #print(f"🎯 [DEBUG] Kamera zentriert über Insel {closest_island}")

        # **Visualisierung des Suchbereichs**
        #self.draw_search_radius(screen, center_x, center_y, scan_range)

        return closest_island

    def draw(self):
        """Zeichnet das Spielgeschehen und steuert das GUI-Verhalten."""
        if not self.tilemap:
            return

        self.screen.fill((0, 87, 142))
        self.renderer.draw_map_with_camera(self.screen, self.tilemap, self.frame, self.camera, debug=False)

        # 🚢 Schiffe rendern
        for ship in self.ships:
            ship.draw(self.screen, self.camera)

        # 🏗️ Gebäude rendern
        self.office_manager.draw_buildings(self.screen, self.camera)  # 🔹 Kontore rendern
        self.building_manager.draw_buildings(self.screen, self.camera)  # 🔹 Normale Gebäude rendern

        # 🏗️ Vorschau für Bauplatz
        self.office_manager.draw_preview(self.screen, self.camera)  # 🔹 Vorschau für Kontor
        self.building_manager.draw_preview(self.screen, self.camera)  # 🔹 Vorschau für normale Gebäude

        if self.selection_active:
            # Verwende die aktuelle Mausposition, falls selection_end noch nicht gesetzt
            current_mouse_pos = pygame.mouse.get_pos()
            selection_rect = pygame.Rect(
                min(self.selection_start[0], current_mouse_pos[0]),
                min(self.selection_start[1], current_mouse_pos[1]),
                abs(self.selection_start[0] - current_mouse_pos[0]),
                abs(self.selection_start[1] - current_mouse_pos[1])
            )
            pygame.draw.rect(self.screen, (0, 255, 0), selection_rect, 2)

        # **Kontor- und Schiffs-GUI anzeigen**
        ship_gui_y = None
        if self.selected_ships:
            ship_gui = self.selected_ships[0].gui
            ship_gui.draw(self.screen)
            ship_gui_y = ship_gui.panel_rect.top  

        warehouse_gui = None
        for ship in self.selected_ships:
            warehouse_gui = ship.is_near_warehouse(return_gui=True)
            if warehouse_gui:
                break  

        if not warehouse_gui:
            for building in self.office_manager.buildings:
                if building["type"] == "office" and building["warehouse"].gui.show_gui:
                    warehouse_gui = building["warehouse"].gui
                    break

        if not self.selected_ships:
            manually_opened_warehouse = any(
                building["warehouse"].gui.manually_opened for building in self.office_manager.buildings
            )
            if not manually_opened_warehouse:
                for building in self.office_manager.buildings:
                    warehouse_gui = building["warehouse"].gui
                    warehouse_gui.show_gui = False 

        if warehouse_gui and warehouse_gui.show_gui:
            warehouse_gui.draw(self.screen, ship_selected=bool(self.selected_ships), ship_gui_y=ship_gui_y)

        # 🌙 Nacht-Overlay anwenden
        night_overlay = self.time_manager.get_night_overlay(self.screen.get_size())
        self.screen.blit(night_overlay, (0, 0))

        # 📦 Ressourcenanzeige rendern
        self.resource_display.draw(self.screen)

        # 🏗️ Gebäudemenü zeichnen
        self.building_gui.draw(self.screen)

        # 🎯 Crosshair rendern
        self.draw_crosshair()

    def save_game(self, slot=1, save_name="Unbenannt"):
        if not self.tilemap:
            print("Fehler: Keine Karte zum Speichern vorhanden!")
            return

        # Kamera-Daten
        camera_data = {
            "x": self.camera.tile_x,
            "y": self.camera.tile_y,
            "zoom": self.camera.zoom
        }

        # TileMap-Daten mit RLE-Kompression
        tilemap_data = []
        for row in self.tilemap.map:
            compressed_row = []
            current_tile = None
            count = 0

            for tile in row:
                tile_repr = (tile.base, tile.overlay)  # Repräsentation des Tiles
                
                if tile_repr == current_tile:
                    count += 1
                else:
                    if current_tile:
                        compressed_row.append({"tile": current_tile, "count": count})
                    current_tile = tile_repr
                    count = 1

            compressed_row.append({"tile": current_tile, "count": count})
            tilemap_data.append(compressed_row)

        save_data = {
            "save_name": save_name,
            "camera": camera_data,
            "tilemap": tilemap_data
        }

        filename = f"save_{slot}.json"
        with open(filename, "w") as file:
            json.dump(save_data, file, indent=4)

    def load_game(self, slot=1):
        filename = f"save_{slot}.json"
        if not os.path.exists(filename):
            print(f"Fehler: Speicherstand in Slot {slot} nicht gefunden!")
            return

        with open(filename, "r") as file:
            save_data = json.load(file)

        self.camera.tile_x = save_data["camera"]["x"]
        self.camera.tile_y = save_data["camera"]["y"]
        self.camera.zoom = save_data["camera"]["zoom"]

        decompressed_tilemap = []
        for compressed_row in save_data["tilemap"]:
            row = []
            for item in compressed_row:
                base, overlay = item["tile"]
                count = item["count"]
                row.extend([Tile(base, overlay) for _ in range(count)])
            decompressed_tilemap.append(row)

        self.tilemap = TileMap(generate=False)
        self.tilemap.load_from_data(decompressed_tilemap)

        self.is_loaded = True
        self.update()
        self.draw()
        pygame.display.flip()
