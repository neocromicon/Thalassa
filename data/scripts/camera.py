import pygame
from data.scripts.Managers.SettingsManager import SettingsManager
from data.scripts.MapGenerator.Settings import SCREEN_HEIGHT, SCREEN_WIDTH, TILE_SIZE

class Camera:
    def __init__(self, width, height, map_width, map_height):
        self.tile_x, self.tile_y = 0, 0  # **Kamera speichert jetzt Tile-Koordinaten!**
        self.width, self.height = width, height  # Kartenbreite/-höhe in Tiles
        self.map_width, self.map_height = map_width, map_height
        self.zoom = 0.8  # Standard-Zoom-Level
        self.load_settings()

    def set_bounds(self, bottom_right_edge):
        """Setzt die Kamerabegrenzung, nachdem die Tilemap generiert wurde."""
        self.bottom_right_edge = bottom_right_edge

    def load_settings(self):
        """Lädt die Steuerungseinstellungen für Maus und Tastatur."""
        settings = SettingsManager.load_input_settings()
        self.mouse_sensitivity = settings["m_sensitivity"]
        self.mouse_invert = -1 if settings["m_invert"] else 1
        self.mouse_zoom_speed = settings["m_zoom_sensitivity"]
        
        self.keyboard_sensitivity = settings["k_sensitivity"]
        self.keyboard_invert = -1 if settings["k_invert"] else 1
        self.keyboard_zoom_speed = settings["k_zoom_sensitivity"]

    def move_with_keyboard(self, dx, dy):
        """Bewegt die Kamera mit der Tastatur, aber verhindert das Verlassen der Karte."""
        
        # Geschwindigkeit an Zoom anpassen
        zoom_factor = 2 / self.zoom  
        move_x = (dx * self.keyboard_sensitivity * self.keyboard_invert) / TILE_SIZE * zoom_factor
        move_y = (dy * self.keyboard_sensitivity * self.keyboard_invert) / TILE_SIZE * zoom_factor

        # **Neue Position berechnen**
        new_tile_x = self.tile_x + move_x
        new_tile_y = self.tile_y + move_y

        # **Begrenzung auf Kartenränder anwenden**
        max_x = self.map_width - (SCREEN_WIDTH / TILE_SIZE) / self.zoom
        max_y = self.map_height - (SCREEN_HEIGHT / TILE_SIZE) / self.zoom

        self.tile_x = max(0, min(max_x, new_tile_x))
        self.tile_y = max(0, min(max_y, new_tile_y))

    def move_with_mouse(self, dx, dy):
        """Bewegt die Kamera mit der Maus, aber verhindert das Verlassen der Karte."""
        
        zoom_factor = 2 / self.zoom  
        move_x = (dx * self.mouse_sensitivity * self.mouse_invert) / TILE_SIZE * zoom_factor
        move_y = (dy * self.mouse_sensitivity * self.mouse_invert) / TILE_SIZE * zoom_factor

        new_tile_x = self.tile_x + move_x
        new_tile_y = self.tile_y + move_y

        max_x = self.map_width - (SCREEN_WIDTH / TILE_SIZE) / self.zoom
        max_y = self.map_height - (SCREEN_HEIGHT / TILE_SIZE) / self.zoom

        self.tile_x = max(0, min(max_x, new_tile_x))
        self.tile_y = max(0, min(max_y, new_tile_y))

    def apply_zoom(self, zoom_amount, mouse_x, mouse_y):
        """Zoomt und verhindert, dass die Kamera das Void anzeigt."""

        old_zoom = self.zoom
        zoom_factor = 1.1 if zoom_amount > 0 else 0.9  
        self.zoom = max(0.25, min(3.5, self.zoom * zoom_factor))  

        # **Berechne das Tile unter der Maus vor dem Zoom**
        tile_x_before = self.tile_x + (mouse_x / old_zoom) / TILE_SIZE
        tile_y_before = self.tile_y + (mouse_y / old_zoom) / TILE_SIZE

        # **Setze die Kamera so, dass das Tile unter der Maus erhalten bleibt**
        self.tile_x = tile_x_before - (mouse_x / self.zoom) / TILE_SIZE
        self.tile_y = tile_y_before - (mouse_y / self.zoom) / TILE_SIZE

        # **Maximale Grenzen berechnen, um das Void zu vermeiden**
        max_x = self.map_width - (SCREEN_WIDTH / TILE_SIZE) / self.zoom
        max_y = self.map_height - (SCREEN_HEIGHT / TILE_SIZE) / self.zoom

        # **Falls die Kamera beim Zoomen an einer Ecke ist, nach innen drücken**
        self.tile_x = max(0, min(max_x, self.tile_x))
        self.tile_y = max(0, min(max_y, self.tile_y))

    def apply_zoom_with_crosshair(self, game, zoom_amount):
        """Zoomt sanft auf die Bildschirmmitte und verhindert, dass die Kamera sich falsch verschiebt."""

        old_zoom = self.zoom
        zoom_factor = 1.05 if zoom_amount > 0 else 0.95  # **Langsamer Zoom**
        self.zoom = max(0.5, min(3.5, self.zoom * zoom_factor))  # Begrenzung des Zooms

        # **1️⃣ Bildschirmmitte berechnen**
        screen_center_x = SCREEN_WIDTH / 2
        screen_center_y = SCREEN_HEIGHT / 2

        # **2️⃣ Welt-Koordinaten der Bildschirmmitte vor dem Zoom**
        world_x_before = self.tile_x * TILE_SIZE + (screen_center_x / old_zoom)
        world_y_before = self.tile_y * TILE_SIZE + (screen_center_y / old_zoom)

        # **3️⃣ Welt-Koordinaten der Bildschirmmitte nach dem Zoom**
        world_x_after = world_x_before
        world_y_after = world_y_before

        # **4️⃣ Kamera so anpassen, dass die Bildschirmmitte exakt bleibt**
        self.tile_x = (world_x_after - screen_center_x / self.zoom) / TILE_SIZE
        self.tile_y = (world_y_after - screen_center_y / self.zoom) / TILE_SIZE

        # **5️⃣ Begrenzung der Kamera auf die Kartengröße, um das Void zu verhindern**
        max_x = self.map_width - (SCREEN_WIDTH / TILE_SIZE) / self.zoom
        max_y = self.map_height - (SCREEN_HEIGHT / TILE_SIZE) / self.zoom

        self.tile_x = max(0, min(max_x, self.tile_x))
        self.tile_y = max(0, min(max_y, self.tile_y))

    def apply(self, target):
        """Korrektur: Verhindert falsche Tile-Positionierung durch Zoom"""
        world_x, world_y = target  # Zielposition in der Welt (Pixel)
        
        # Berechne die Kamera-Verschiebung in **Tiles, nicht Pixeln**
        camera_offset_x = self.tile_x * TILE_SIZE
        camera_offset_y = self.tile_y * TILE_SIZE

        # Finales Rendering-Koordinatensystem mit Zoom
        screen_x = (world_x - camera_offset_x) * self.zoom
        screen_y = (world_y - camera_offset_y) * self.zoom

        return round(screen_x), round(screen_y)

    def get_center_tile(self):
        """Gibt die aktuelle Mitte der Kamera in Tile-Koordinaten zurück."""
        world_x = self.tile_x * TILE_SIZE + (SCREEN_WIDTH / 2) / self.zoom
        world_y = self.tile_y * TILE_SIZE + (SCREEN_HEIGHT / 2) / self.zoom

        tile_x = int(world_x // TILE_SIZE)
        tile_y = int(world_y // TILE_SIZE)

        # **Sicherstellen, dass die Koordinaten innerhalb der Karte liegen**
        tile_x = max(0, min(tile_x, self.map_width - 1))
        tile_y = max(0, min(tile_y, self.map_height - 1))

        return tile_x, tile_y

    def screen_to_world(self, screen_x, screen_y):
        """Wandelt Bildschirmkoordinaten in Weltkoordinaten um (unter Berücksichtigung von Zoom & Kamera-Offset)."""
        world_x = (screen_x / self.zoom) + (self.tile_x * TILE_SIZE)
        world_y = (screen_y / self.zoom) + (self.tile_y * TILE_SIZE)
        return int(world_x), int(world_y)
