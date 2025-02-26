import pygame

from data.scripts.Constants import FONT_SHADOW_COLOR
from data.scripts.MapGenerator.Settings import SCREEN_WIDTH, SCREEN_HEIGHT

class MenuManager:
     # ---------------------------------------
    # Ressourcen Laden (Hintergrund & Ränder)
    # ----------------------------------------
    BORDERS_CACHE = None  # 🔥 Borders werden nur einmalig gespeichert

    @classmethod
    def load_borders(cls):
        """Lädt die Bilder für die Ränder des Menüs und speichert sie in einer Klassenvariablen."""
        if cls.BORDERS_CACHE is None:  # 🔥 Nur laden, wenn noch nicht im Cache
            print("🔄 Borders werden geladen...")
            border_path_small = "data/img/GUI/Boarder_Small"
            border_path_small_trans = "data/img/GUI/Boarder_Small_Trans"
            border_path_normal_trans = "data/img/GUI/Boarder_Normal_Trans"

            cls.BORDERS_CACHE = {
                ## Small Size
                "b_s_corner_tl": pygame.image.load(f"{border_path_small}/B_S_CornerTopLeft.png"),
                "b_s_corner_tr": pygame.image.load(f"{border_path_small}/B_S_CornerTopRight.png"),
                "b_s_corner_bl": pygame.image.load(f"{border_path_small}/B_S_CornerBottomLeft.png"),
                "b_s_corner_br": pygame.image.load(f"{border_path_small}/B_S_CornerBottomRight.png"),
                "b_s_edge_tm": pygame.image.load(f"{border_path_small}/B_S_TopMiddle.png"),
                "b_s_edge_bm": pygame.image.load(f"{border_path_small}/B_S_BottomMiddle.png"),
                "b_s_edge_ml": pygame.image.load(f"{border_path_small}/B_S_MiddleLeft.png"),
                "b_s_edge_mr": pygame.image.load(f"{border_path_small}/B_S_MiddleRight.png"),
                "b_s_center": pygame.image.load(f"{border_path_small}/B_S_Center.png"),
                ## Small Size Trans
                "b_s_t_corner_tl": pygame.image.load(f"{border_path_small_trans}/B_S_T_CornerTopLeft.png"),
                "b_s_t_corner_tr": pygame.image.load(f"{border_path_small_trans}/B_S_T_CornerTopRight.png"),
                "b_s_t_corner_bl": pygame.image.load(f"{border_path_small_trans}/B_S_T_CornerBottomLeft.png"),
                "b_s_t_corner_br": pygame.image.load(f"{border_path_small_trans}/B_S_T_CornerBottomRight.png"),
                "b_s_t_edge_tm": pygame.image.load(f"{border_path_small_trans}/B_S_T_TopMiddle.png"),
                "b_s_t_edge_bm": pygame.image.load(f"{border_path_small_trans}/B_S_T_BottomMiddle.png"),
                "b_s_t_edge_ml": pygame.image.load(f"{border_path_small_trans}/B_S_T_MiddleLeft.png"),
                "b_s_t_edge_mr": pygame.image.load(f"{border_path_small_trans}/B_S_T_MiddleRight.png"),
                ## Normal Size Trans
                "b_n_t_corner_tl": pygame.image.load(f"{border_path_normal_trans}/B_N_T_CornerTopLeft.png"),
                "b_n_t_corner_tr": pygame.image.load(f"{border_path_normal_trans}/B_N_T_CornerTopRight.png"),
                "b_n_t_corner_bl": pygame.image.load(f"{border_path_normal_trans}/B_N_T_CornerBottomLeft.png"),
                "b_n_t_corner_br": pygame.image.load(f"{border_path_normal_trans}/B_N_T_CornerBottomRight.png"),
                "b_n_t_edge_tm": pygame.image.load(f"{border_path_normal_trans}/B_N_T_TopMiddle.png"),
                "b_n_t_edge_bm": pygame.image.load(f"{border_path_normal_trans}/B_N_T_BottomMiddle.png"),
                "b_n_t_edge_ml": pygame.image.load(f"{border_path_normal_trans}/B_N_T_MiddleLeft.png"),
                "b_n_t_edge_mr": pygame.image.load(f"{border_path_normal_trans}/B_N_T_MiddleRight.png"),
            }
        return cls.BORDERS_CACHE  # Immer aus dem Cache zurückgeben
    
    @staticmethod
    def load_background(path):
        """Lädt das Hintergrundbild."""
        try:
            return pygame.image.load(path).convert_alpha()
        except FileNotFoundError:
            print("Hintergrundbild nicht gefunden! Verwende dunklen Hintergrund.")
            return None

    @staticmethod
    def draw_boarder(screen, rect, border_type="b_s", reduce_rows=False):
        """Zeichnet die Ränder des Menüs mit `border_type`, ohne `self.border_images` zu verwenden."""
        borders = MenuManager.load_borders()  # Lade die Border-Bilder
        x, y, w, h = rect
        tile_size = 16  # Standardgröße der Border-Elemente

        # Falls `reduce_rows` aktiv ist, die Höhe anpassen
        adjusted_height = h - (tile_size if reduce_rows else 0)

        # **1. Ecken setzen**
        screen.blit(borders[f"{border_type}_corner_tl"], (x, y))
        screen.blit(borders[f"{border_type}_corner_tr"], (x + w - tile_size, y))
        screen.blit(borders[f"{border_type}_corner_bl"], (x, y + adjusted_height - tile_size))
        screen.blit(borders[f"{border_type}_corner_br"], (x + w - tile_size, y + adjusted_height - tile_size))

        # **2. Obere und untere Kanten**
        for i in range(tile_size, w - tile_size, tile_size):
            screen.blit(borders[f"{border_type}_edge_tm"], (x + i, y))
            screen.blit(borders[f"{border_type}_edge_bm"], (x + i, y + adjusted_height - tile_size))

        # **3. Seitliche Kanten**
        for j in range(tile_size, adjusted_height - tile_size, tile_size):
            screen.blit(borders[f"{border_type}_edge_ml"], (x, y + j))
            screen.blit(borders[f"{border_type}_edge_mr"], (x + w - tile_size, y + j))

        # **4. Zentrum füllen (falls gewünscht)**
        for i in range(tile_size, w - tile_size, tile_size):
            for j in range(tile_size, adjusted_height - tile_size, tile_size):
                if reduce_rows and j >= adjusted_height - (tile_size - 16):
                    continue  # Überspringe das Zeichnen der untersten Zeile
                screen.blit(borders[f"{border_type}_center"], (x + i, y + j))

    @staticmethod
    def draw_window_border(screen, border_type="b_n_t"):
        """Zeichnet einen Rahmen um das gesamte Fenster, ohne das Zentrum auszufüllen."""
        borders = MenuManager.load_borders()  # Lade die Border-Bilder
        tile_size = 32  # Standardgröße der Border-Elemente

        x, y, w, h = 0, 0, SCREEN_WIDTH, SCREEN_HEIGHT  # Fenster-Koordinaten

        # **Ecken setzen**
        screen.blit(borders[f"{border_type}_corner_tl"], (x, y))
        screen.blit(borders[f"{border_type}_corner_tr"], (x + w - tile_size, y))
        screen.blit(borders[f"{border_type}_corner_bl"], (x, y + h - tile_size))
        screen.blit(borders[f"{border_type}_corner_br"], (x + w - tile_size, y + h - tile_size))

        # **Kanten setzen**
        for i in range(tile_size, w - tile_size, tile_size):  # Horizontale Kanten
            screen.blit(borders[f"{border_type}_edge_tm"], (x + i, y))
            screen.blit(borders[f"{border_type}_edge_bm"], (x + i, y + h - tile_size))

        for j in range(tile_size, h - tile_size, tile_size):  # Vertikale Kanten
            screen.blit(borders[f"{border_type}_edge_ml"], (x, y + j))
            screen.blit(borders[f"{border_type}_edge_mr"], (x + w - tile_size, y + j))

    @staticmethod
    def draw_ship_border(screen, x, y, width, height, border_type="b_n_t"):
        """Zeichnet den Rahmen der GUI mit einem bestimmten Border-Typ."""
        borders = MenuManager.load_borders()  # Lade die Border-Bilder
        
        tile_size = borders[f"{border_type}_corner_tl"].get_width()

        # Ecken
        screen.blit(borders[f"{border_type}_corner_tl"], (x, y))
        screen.blit(borders[f"{border_type}_corner_tr"], (x + width - tile_size, y))
        screen.blit(borders[f"{border_type}_corner_bl"], (x, y + height - tile_size))
        screen.blit(borders[f"{border_type}_corner_br"], (x + width - tile_size, y + height - tile_size))

        # Seiten
        for i in range(tile_size, width - tile_size, tile_size):
            screen.blit(borders[f"{border_type}_edge_tm"], (x + i, y))
            screen.blit(borders[f"{border_type}_edge_bm"], (x + i, y + height - tile_size))

        for j in range(tile_size, height - tile_size, tile_size):
            screen.blit(borders[f"{border_type}_edge_ml"], (x, y + j))
            screen.blit(borders[f"{border_type}_edge_mr"], (x + width - tile_size, y + j))

    @staticmethod
    def draw_slot_border(screen, x, y, size, border_type="b_s_t"):
        """Zeichnet einen 16x16 Rahmen um einen Slot mit gewähltem Border-Typ."""
        borders = MenuManager.load_borders()  # Lade die Border-Bilder
        tile_size = 16  # Feste Größe der Borderelemente

        # **Ecken setzen**
        screen.blit(borders[f"{border_type}_corner_tl"], (x, y))
        screen.blit(borders[f"{border_type}_corner_tr"], (x + size - tile_size, y))
        screen.blit(borders[f"{border_type}_corner_bl"], (x, y + size - tile_size))
        screen.blit(borders[f"{border_type}_corner_br"], (x + size - tile_size, y + size - tile_size))

        # **Seiten setzen**
        for i in range(tile_size, size - tile_size, tile_size):
            screen.blit(borders[f"{border_type}_edge_tm"], (x + i, y))
            screen.blit(borders[f"{border_type}_edge_bm"], (x + i, y + size - tile_size))
            screen.blit(borders[f"{border_type}_edge_ml"], (x, y + i))
            screen.blit(borders[f"{border_type}_edge_mr"], (x + size - tile_size, y + i))

    @staticmethod
    def draw_text_with_soft_shadow(self, text, x, y, text_color=None, shadow_color=FONT_SHADOW_COLOR):
        """
        Zeichnet Text mit weichem Schatteneffekt.

        Args:
            text: Der anzuzeigende Text.
            x, y: Position auf dem Bildschirm.
            text_color: Farbe des Haupttextes (wenn None, wird self.text_color genutzt).
            shadow_color: Farbe des Schattens.
        """
        if text_color is None:
            text_color = self.text_color  # Standardfarbe verwenden

        offsets = [(-2, -2), (-2, 2), (2, -2), (2, 2)]  # Schatten-Offsets

        for ox, oy in offsets:
            shadow_surface = self.font.render(text, True, shadow_color)
            shadow_rect = shadow_surface.get_rect(center=(x + ox, y + oy))
            self.screen.blit(shadow_surface, shadow_rect)

        text_surface = self.font.render(text, True, text_color)
        text_rect = text_surface.get_rect(center=(x, y))
        self.screen.blit(text_surface, text_rect)

    @staticmethod
    def draw_text_with_soft_shadow_title(self, text, x, y, text_color=(192, 192, 192), shadow_color=(0, 0, 0)):
        """
        Zeichnet Text mit weichem Schatteneffekt.

        Args:
            text: Der anzuzeigende Text.
            x, y: Position auf dem Bildschirm.
            text_color: Farbe des Haupttextes.
            shadow_color: Farbe des Schattens.
        """
        offsets = [(-2, -2), (-2, 2), (2, -2), (2, 2)]  # Schatten um den Text

        for ox, oy in offsets:
            shadow_surface = self.font.render(text, True, shadow_color)
            shadow_rect = shadow_surface.get_rect(center=(x + ox, y + oy))
            self.screen.blit(shadow_surface, shadow_rect)

        text_surface = self.font.render(text, True, text_color)
        text_rect = text_surface.get_rect(center=(x, y))
        self.screen.blit(text_surface, text_rect)