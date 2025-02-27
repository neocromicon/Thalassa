import pygame
from data.scripts.Constants import FONT_BIG

class ResourceDisplayGUI:
    """Zeigt die wichtigsten Baumaterialien oben am Bildschirm an, basierend auf der nächstgelegenen Insel."""

    def __init__(self, game):
        self.game = game
        self.font = pygame.font.Font(FONT_BIG, 24)  # Standard-Schriftart
        self.icon_size = 38  # Größe der Icons
        self.padding = 10  # Abstand zwischen Elementen
        self.spacing = 20  # Dynamischer Abstand zwischen den Einträgen
        self.bg_color = (40, 40, 60, 180)  # Dunkler, leicht transparenter Hintergrund
        self.border_radius = 10  # **Abgerundete Ecken für das Panel**
        self.current_island_id = None
        self.current_resources = {}

        # Lade die Icons für Holz, Werkzeuge und Nahrung
        self.icons = { 
            "tools": pygame.image.load("data/img/Goods/tool.png"),  
            "wood": pygame.image.load("data/img/Goods/wood.png"),
            "food": pygame.image.load("data/img/Goods/food.png"),  
        }

    def update_island_resources(self):
        """Aktualisiert die Ressourcenanzeige live, während sich Warenbestände ändern."""
        island_id = self.game.debug_island_id_center_camera(self.game.screen)  # Holt die aktuelle Insel-ID

        # **Falls keine Insel erkannt wird, verstecke die Anzeige**
        if island_id is None:
            #if self.current_island_id is not None:
                #print("🌊 [DEBUG] Kamera ist über Wasser – Ressourcenanzeige ausblenden.")
            self.current_island_id = None
            self.current_resources = {}
            return

        # **Falls die Insel gewechselt hat oder sich der Bestand geändert hat → Immer aktualisieren**
        new_resources = self.get_island_inventory(island_id)

        if island_id != self.current_island_id or new_resources != self.current_resources:
            self.current_island_id = island_id
            self.current_resources = new_resources
            #print(f"🔄 [DEBUG] Insel {island_id} – Ressourcen aktualisiert: {self.current_resources}")

        # **Falls keine Waren existieren, Anzeige verstecken**
        if not any(self.current_resources.values()):
            #print(f"🚫 [DEBUG] Insel {island_id} hat keine Waren – Anzeige ausblenden.")
            self.current_resources = {}

    def get_island_inventory(self, island_id):
        """Berechnet die Gesamtmenge aller Waren in Kontoren und Markthäusern auf der Insel."""
        total_resources = {"tools": 0, "wood": 0, "food": 0}

        for building in self.game.office_manager.buildings:
            if building.get("island_id") == island_id and "warehouse" in building:
                warehouse = building["warehouse"]
                total_resources["tools"] += warehouse.get_quantity("tools")
                total_resources["wood"] += warehouse.get_quantity("wood")
                total_resources["food"] += warehouse.get_quantity("food")

        #print(f"🔢 [DEBUG] Insel {island_id} – Gesamtbestand: {total_resources}")
        return total_resources

    def draw(self, screen):
        """Zeichnet die Baumaterialien-Anzeige basierend auf der aktuellen Insel."""
        self.update_island_resources()  # 🔄 **Ressourcen immer aktualisieren**

        if not self.current_resources:
            return  # **Falls keine Ressourcen existieren, nichts zeichnen**

        # **Dynamische Berechnung der Breite basierend auf Anzahl der Ressourcen**
        panel_width = sum([(self.icon_size + self.spacing + self.font.size(str(amount))[0]) for amount in self.current_resources.values()]) + self.padding * 2
        panel_height = self.icon_size + self.padding * 2
        panel_x = (screen.get_width() - panel_width) // 2
        panel_y = self.padding

        # **Halbtransparenter Hintergrund mit abgerundeten Ecken**
        panel_surface = pygame.Surface((panel_width, panel_height), pygame.SRCALPHA)
        pygame.draw.rect(panel_surface, self.bg_color, (0, 0, panel_width, panel_height), border_radius=self.border_radius)  
        screen.blit(panel_surface, (panel_x, panel_y))

        # **Ressourcen-Icons und Werte zeichnen**
        x_offset = panel_x + self.padding
        for resource, amount in self.current_resources.items():
            # Icon anzeigen
            icon = pygame.transform.scale(self.icons[resource], (self.icon_size, self.icon_size))
            screen.blit(icon, (x_offset, panel_y + self.padding))

            # Text daneben anzeigen (dynamische Breite)
            text_surface = self.font.render(str(amount), True, (255, 255, 255))
            screen.blit(text_surface, (x_offset + self.icon_size + 5, panel_y + self.padding + 5))

            # Dynamischer Abstand für das nächste Element
            x_offset += self.icon_size + self.spacing + text_surface.get_width()

