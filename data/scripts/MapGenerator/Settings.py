from data.scripts.Managers.SettingsManager import SettingsManager

# Bildschirmauflösung laden
SCREEN_WIDTH, SCREEN_HEIGHT = SettingsManager.load_resolution_from_settings()

# Spielfeldgröße aus den gespeicherten Einstellungen laden
TILE_SIZE = 64  # Feste Tile-Größe bleibt unverändert
ANIMATION_SPEED = 8

# Dateipfad für Grafiken
TILE_PATH = "data/img/Tilesets/Islands"
SHIP_PATH = "data/img/Entitys/Ships"

# Animation Frames
OCEAN_ANIM_FRAMES = [f"ocean_frame_{i}.png" for i in range(0, 27)]

MAP_WIDTH = 0
MAP_HEIGHT = 0