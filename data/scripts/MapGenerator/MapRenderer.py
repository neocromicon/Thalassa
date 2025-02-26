import pygame
import os
from data.scripts.MapGenerator.Settings import SCREEN_WIDTH, SCREEN_HEIGHT, TILE_PATH, TILE_SIZE, OCEAN_ANIM_FRAMES

class Renderer:
    def __init__(self):
        self.tiles = self.load_tiles()
        self.ocean_anim_frames = self.load_ocean_anim()

    def load_tiles(self):
        return {
            # North Islands
            "Water": pygame.image.load(os.path.join(TILE_PATH, "Water.png")),
            "Grass": pygame.image.load(os.path.join(TILE_PATH, "Grass.png")),
            "Mountains": pygame.image.load(os.path.join(TILE_PATH, "Mountains.png")),
            "Forest_Pines_x1_1": pygame.image.load(os.path.join(TILE_PATH, "Forest_Pines_x1_1.png")),
            "Forest_Pines_x1_2": pygame.image.load(os.path.join(TILE_PATH, "Forest_Pines_x1_2.png")),
            "Forest_Pines_x2": pygame.image.load(os.path.join(TILE_PATH, "Forest_Pines_x2.png")),
            "Forest_Pines_x3": pygame.image.load(os.path.join(TILE_PATH, "Forest_Pines_x3.png")),
            "Forest_Pines_x4": pygame.image.load(os.path.join(TILE_PATH, "Forest_Pines_x4.png")),

            "Coast_Top_Left": pygame.image.load(os.path.join(TILE_PATH, "Coast_Top_Left.png")),
            "Coast_Top_Middle": pygame.image.load(os.path.join(TILE_PATH, "Coast_Top_Middle.png")),
            "Coast_Top_Right": pygame.image.load(os.path.join(TILE_PATH, "Coast_Top_Right.png")),
            "Coast_Middle_Left": pygame.image.load(os.path.join(TILE_PATH, "Coast_Middle_Left.png")),
            "Coast_Middle_Right": pygame.image.load(os.path.join(TILE_PATH, "Coast_Middle_Right.png")),
            "Coast_Bottom_Left": pygame.image.load(os.path.join(TILE_PATH, "Coast_Bottom_Left.png")),
            "Coast_Bottom_Middle": pygame.image.load(os.path.join(TILE_PATH, "Coast_Bottom_Middle.png")),
            "Coast_Bottom_Right": pygame.image.load(os.path.join(TILE_PATH, "Coast_Bottom_Right.png")),

            "Coast_Top_Left_Curve": pygame.image.load(os.path.join(TILE_PATH, "Coast_Top_Left_Curve.png")),
            "Coast_Top_Right_Curve": pygame.image.load(os.path.join(TILE_PATH, "Coast_Top_Right_Curve.png")),
            "Coast_Bottom_Left_Curve": pygame.image.load(os.path.join(TILE_PATH, "Coast_Bottom_Left_Curve.png")),
            "Coast_Bottom_Right_Curve": pygame.image.load(os.path.join(TILE_PATH, "Coast_Bottom_Right_Curve.png")),

            # South Islands
            "South_Sand": pygame.image.load(os.path.join(TILE_PATH, "South", "South_Sand.png")),
            "South_Sand_2": pygame.image.load(os.path.join(TILE_PATH, "South", "South_Sand_2.png")),
            "South_Sand_3": pygame.image.load(os.path.join(TILE_PATH, "South", "South_Sand_3.png")),
            "South_Sand_4": pygame.image.load(os.path.join(TILE_PATH, "South", "South_Sand_4.png")),
            "South_Sand_5": pygame.image.load(os.path.join(TILE_PATH, "South", "South_Sand_5.png")),

            "Cactus_1": pygame.image.load(os.path.join(TILE_PATH, "South", "Cactus_1.png")),
            "Cactus_2": pygame.image.load(os.path.join(TILE_PATH, "South", "Cactus_2.png")),
            "Cactus_3": pygame.image.load(os.path.join(TILE_PATH, "South", "Cactus_3.png")),
            "Cactus_4": pygame.image.load(os.path.join(TILE_PATH, "South", "Cactus_4.png")),
            "Cactus_5": pygame.image.load(os.path.join(TILE_PATH, "South", "Cactus_5.png")),
            "Cactus_6": pygame.image.load(os.path.join(TILE_PATH, "South", "Cactus_6.png")),
            "Cactus_7": pygame.image.load(os.path.join(TILE_PATH, "South", "Cactus_7.png")),
            "Cactus_8": pygame.image.load(os.path.join(TILE_PATH, "South", "Cactus_8.png")),
            "Cactus_9": pygame.image.load(os.path.join(TILE_PATH, "South", "Cactus_9.png")),

            "Coast_South_Top_Left": pygame.image.load(os.path.join(TILE_PATH, "South", "South_Coast_Top_Left.png")),
            "Coast_South_Top_Middle": pygame.image.load(os.path.join(TILE_PATH, "South", "South_Coast_Top_Middle.png")),
            "Coast_South_Top_Right": pygame.image.load(os.path.join(TILE_PATH, "South", "South_Coast_Top_Right.png")),
            "Coast_South_Middle_Left": pygame.image.load(os.path.join(TILE_PATH, "South", "South_Coast_Middle_Left.png")),
            "Coast_South_Middle_Right": pygame.image.load(os.path.join(TILE_PATH, "South", "South_Coast_Middle_Right.png")),
            "Coast_South_Bottom_Left": pygame.image.load(os.path.join(TILE_PATH, "South", "South_Coast_Bottom_Left.png")),
            "Coast_South_Bottom_Middle": pygame.image.load(os.path.join(TILE_PATH, "South", "South_Coast_Bottom_Middle.png")),
            "Coast_South_Bottom_Right": pygame.image.load(os.path.join(TILE_PATH, "South", "South_Coast_Bottom_Right.png")),

            "Coast_South_Top_Left_Curve": pygame.image.load(os.path.join(TILE_PATH, "South", "South_Coast_Top_Left_Curve.png")),
            "Coast_South_Top_Right_Curve": pygame.image.load(os.path.join(TILE_PATH, "South", "South_Coast_Top_Right_Curve.png")),
            "Coast_South_Bottom_Left_Curve": pygame.image.load(os.path.join(TILE_PATH, "South", "South_Coast_Bottom_Left_Curve.png")),
            "Coast_South_Bottom_Right_Curve": pygame.image.load(os.path.join(TILE_PATH, "South", "South_Coast_Bottom_Right_Curve.png")),

            # Neue Deep-Ocean-Kacheln
            "Ocean": pygame.image.load(os.path.join(TILE_PATH, "Ocean", "Ocean.png")),
            "Ocean_Top_Middle": pygame.image.load(os.path.join(TILE_PATH, "Ocean_Top_Middle.png")),
            "Ocean_Top_Left": pygame.image.load(os.path.join(TILE_PATH, "Ocean_Top_Left.png")),
            "Ocean_Top_Right": pygame.image.load(os.path.join(TILE_PATH, "Ocean_Top_Right.png")),
            "Ocean_Middle_Left": pygame.image.load(os.path.join(TILE_PATH, "Ocean_Middle_Left.png")),
            "Ocean_Middle_Right": pygame.image.load(os.path.join(TILE_PATH, "Ocean_Middle_Right.png")),
            "Ocean_Bottom_Middle": pygame.image.load(os.path.join(TILE_PATH, "Ocean_Bottom_Middle.png")),
            "Ocean_Bottom_Left": pygame.image.load(os.path.join(TILE_PATH, "Ocean_Bottom_Left.png")),
            "Ocean_Bottom_Right": pygame.image.load(os.path.join(TILE_PATH, "Ocean_Bottom_Right.png")),
            "Ocean_Inner_Top_Right": pygame.image.load(os.path.join(TILE_PATH, "Ocean_Inner_Top_Right.png")),
            "Ocean_Inner_Top_Left": pygame.image.load(os.path.join(TILE_PATH, "Ocean_Inner_Top_Left.png")),
            "Ocean_Inner_Bottom_Right": pygame.image.load(os.path.join(TILE_PATH, "Ocean_Inner_Bottom_Right.png")),
            "Ocean_Inner_Bottom_Left": pygame.image.load(os.path.join(TILE_PATH, "Ocean_Inner_Bottom_Left.png")),
        }


    def load_ocean_anim(self):
        return [pygame.image.load(os.path.join(TILE_PATH, "Ocean_Ani", frame)) for frame in OCEAN_ANIM_FRAMES]
    
    def get_visible_area(self, camera, tilemap, screen_width, screen_height):
        """Berechnet den sichtbaren Bereich basierend auf Tile-Koordinaten mit genauerem Culling."""
        tile_size = max(1, round(TILE_SIZE * camera.zoom))  # Korrigierte Tile-Größe mit Zoom
        padding = 3  # **Minimaler Puffer für Randbereiche**

        # Berechne Start- und End-Koordinaten in Tiles
        start_x = max(0, int(camera.tile_x)) - padding
        start_y = max(0, int(camera.tile_y)) - padding
        end_x = min(tilemap.width, int(start_x + (screen_width / tile_size) + padding * 2))
        end_y = min(tilemap.height, int(start_y + (screen_height / tile_size) + padding * 2))

        return start_x, start_y, end_x, end_y

    def draw_map_with_camera(self, screen, tilemap, frame, camera, debug=False):
        """Zeichnet die Karte basierend auf der Kamera-Position und dem Zoom."""

        screen_width = SCREEN_WIDTH
        screen_height = SCREEN_HEIGHT
        start_x, start_y, end_x, end_y = self.get_visible_area(camera, tilemap, screen_width, screen_height)

        for y in range(start_y, end_y):
            for x in range(start_x, end_x):
                tile = tilemap.map[y][x]

                # **Tile-Position im Viewport mit korrektem Offset berechnen**
                pos_x, pos_y = camera.apply((x * TILE_SIZE, y * TILE_SIZE))
                scaled_size = max(1, round(TILE_SIZE * camera.zoom))
                adjusted_size = scaled_size + 1
                # **Zeichne nur, wenn das Tile tatsächlich im sichtbaren Bereich liegt**
                if -adjusted_size < pos_x < screen_width and -adjusted_size < pos_y < screen_height:
                    # Basis-Tile zeichnen
                    base_image = pygame.transform.scale(self.tiles[tile.base], (adjusted_size, adjusted_size))
                    screen.blit(base_image, (pos_x, pos_y))

                    # Overlay zeichnen
                    if tile.overlay:
                        overlay_image = pygame.transform.scale(self.tiles[tile.overlay], (adjusted_size, adjusted_size))
                        screen.blit(overlay_image, (pos_x, pos_y))

                    # Ozean-Animation zeichnen
                    if tile.base == "Ocean" and tile.ocean_anim_index is not None:
                        anim_frame = ((frame // 8) + tile.start_offset) % len(self.ocean_anim_frames)
                        anim_image = pygame.transform.scale(self.ocean_anim_frames[anim_frame], (adjusted_size, adjusted_size))
                        screen.blit(anim_image, (pos_x, pos_y))

                    # **Debugging für Küstenlinien**
                    if debug and tile.base.startswith("Coast_"):
                        rect = pygame.Rect(pos_x, pos_y, adjusted_size, adjusted_size)
                        pygame.draw.rect(screen, (255, 0, 0), rect, 1)
