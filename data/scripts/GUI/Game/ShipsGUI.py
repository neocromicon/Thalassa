from winsound import PlaySound
import pygame
from data.scripts.Constants import FONT_BIG
from data.scripts.Managers.MenuManager import MenuManager
from data.scripts.Managers.GoodManager import GoodManager
from data.scripts.Managers.SoundManager import SoundManager
from data.scripts.MapGenerator.Settings import SCREEN_HEIGHT, SCREEN_WIDTH, TILE_SIZE

class ShipGUI:
    def __init__(self, ship):
        self.ship = ship
        self.show_gui = False
        self.build_button_rect = None
        self.panel_rect = None
        self.font = pygame.font.Font(FONT_BIG, 12)
        
        # Laden der Rahmenbilder für die GUI
        self.kontor_icon = pygame.image.load("data/img/Buildings/Kontor_South.png")  # Originalfarbig
        self.kontor_icon_gray = self.grayscale(self.kontor_icon)  # Graue Version
        # Speichert den aktuell angeklickten Slot (None = nichts ausgewählt)
        self.selected_slot = None  
        self.unload_button_rect = None
        self.load_button_rect = None
        # Lade die Icons für Be- und Entladen
        self.load_icons()

    def grayscale(self, image):
        """Gibt eine graue Version eines Bildes zurück."""
        gray = pygame.Surface(image.get_size(), pygame.SRCALPHA)
        for x in range(image.get_width()):
            for y in range(image.get_height()):
                pixel = image.get_at((x, y))
                avg = sum(pixel[:3]) // 3
                gray.set_at((x, y), (avg, avg, avg, pixel[3]))
        return gray

    def load_icons(self):
        """Lädt die Icons für Be- und Entladen."""
        self.load_icon = pygame.image.load("data/img/GUI/load.png")  # Beladen
        self.unload_icon = pygame.image.load("data/img/GUI/unload.png")  # Entladen

    def draw(self, screen):
        """Zeichnet die GUI unten rechts am Bildschirm mit mehreren Reihen für die Slots."""
        if not self.show_gui:
            return

        slot_size = 64
        padding = 10
        slot_offset_x = 24
        slot_offset_y = 20
        icon_offset = 16  # **Offset für die Icons der Waren**
        max_slots_per_row = 4
        
        total_slots = len(self.ship.warehouse.slots)
        num_rows = (total_slots + max_slots_per_row - 1) // max_slots_per_row  # **Berechnet benötigte Reihen**

        panel_width = 480  # **Feste Breite**
        panel_height = max(120, num_rows * (slot_size + padding) + 50)  # **Dynamische Höhe**
        
        panel_x = SCREEN_WIDTH - panel_width - 20
        panel_y = SCREEN_HEIGHT - panel_height - 20
        self.panel_rect = pygame.Rect(panel_x, panel_y, panel_width, panel_height)

        # Hintergrund füllen mit dunklem Grau
        pygame.draw.rect(screen, (40, 40, 60), self.panel_rect)

        # Rahmen um die GUI zeichnen
        MenuManager.draw_ship_border(screen, panel_x, panel_y, panel_width, panel_height)

        # Slots zeichnen (mit mehreren Reihen + Offset)
        for i, slot in enumerate(self.ship.warehouse.slots.values()):
            col = i % max_slots_per_row  # **Berechnet Spaltenindex**
            row = i // max_slots_per_row  # **Berechnet Reihenindex**

            slot_x = panel_x + slot_offset_x + padding + col * (slot_size + padding)
            slot_y = panel_y + slot_offset_y + padding + row * (slot_size + padding)
            slot_rect = pygame.Rect(slot_x, slot_y, slot_size, slot_size)

            # **Hintergrund ändern, wenn Slot ausgewählt ist**
            if self.selected_slot == f"slot_{i}":
                pygame.draw.rect(screen, (100, 100, 150), slot_rect)  # **Blauer Hintergrund für Auswahl**
            else:
                pygame.draw.rect(screen, (80, 80, 100), slot_rect)
            MenuManager.draw_slot_border(screen, slot_x, slot_y, slot_size)

            if slot["good"]:
                img = GoodManager.textures[slot["good"]]
                scaled_img = pygame.transform.scale(img, (slot_size - icon_offset, slot_size - icon_offset))  # **Skalierung für Offset**
                screen.blit(scaled_img, (slot_x + icon_offset // 2, slot_y + icon_offset // 2))  # **Offset für zentrierte Position**

                # Warenmengen-Balken zeichnen
                max_capacity = slot["max_quantity"] if "max_quantity" in slot else 50  # Standardwert auf 50 setzen
                filled_ratio = slot["quantity"] / max_capacity if max_capacity > 0 else 0
                
                bar_height = 8  # **Höhe des Balkens**
                bar_width = slot_size - 16  # **Länge des Balkens**
                bar_x = slot_x + 8  # **Leichter Innenabstand**
                bar_y = slot_y + 8  # **Oben im Slot mit 4 Pixel Abstand nach unten**

                # Balken-Hintergrund
                pygame.draw.rect(screen, (50, 50, 50), (bar_x, bar_y, bar_width, bar_height))
                # Gefüllter Bereich
                pygame.draw.rect(screen, (255, 200, 0), (bar_x, bar_y, int(bar_width * filled_ratio), bar_height))

        # Kontor-Bauen-Icon mit Offset zeichnen
        kontor_x = panel_x + panel_width - slot_size - padding - slot_offset_x
        kontor_y = panel_y + padding + slot_offset_x
        kontor_img = self.kontor_icon if self.ship.can_build else self.kontor_icon_gray
        screen.blit(pygame.transform.scale(kontor_img, (slot_size - icon_offset, slot_size - icon_offset)), 
                    (kontor_x + icon_offset // 2, kontor_y + icon_offset // 2))

        self.build_button_rect = pygame.Rect(kontor_x, kontor_y, slot_size, slot_size)

        # 🔄 **Pfeile nur anzeigen, wenn ein Slot ausgewählt wurde**
        warehouse = self.ship.is_near_warehouse(return_gui=False)
        if warehouse:
            #print("📌 Pfeile werden angezeigt, weil das Schiff in der Nähe eines Kontors ist und ein Slot ausgewählt wurde.")

            row = 2 // 4
            first_slot_y = panel_y + 60 + row * (64 + 10)

            button_x, button_y = self.build_button_rect.x, self.build_button_rect.y

            arrow_x = button_x - 48
            arrow_y = (first_slot_y + button_y) // 2

            screen.blit(pygame.transform.scale(self.unload_icon, (32, 32)), (arrow_x, arrow_y - 20))
            screen.blit(pygame.transform.scale(self.load_icon, (32, 32)), (arrow_x, arrow_y + 20))

            self.unload_button_rect = pygame.Rect(arrow_x, arrow_y - 20, 32, 32)
            self.load_button_rect = pygame.Rect(arrow_x, arrow_y + 20, 32, 32)

        else:
            self.unload_button_rect = None
            self.load_button_rect = None

    def is_hovered(self, mouse_pos):
        """Prüft, ob die Maus sich über der GUI befindet."""
        return self.panel_rect and self.panel_rect.collidepoint(mouse_pos)

    def handle_click(self, mouse_pos, warehouse_gui):
        """Verhindert das Starten des Bau-Modus, falls der Button ausgegraut ist."""
        if self.build_button_rect and self.build_button_rect.collidepoint(mouse_pos):
            if not self.ship.can_build:  # 🚨 Falls Button grau ist, keine Aktion!
                print("❌ Bau nicht möglich – Button ist ausgegraut!")
                return False
            self.ship.start_build_office()
            return True
        
        # 📦 Prüfe, ob ein Slot im Schiff angeklickt wurde
        for i, slot in enumerate(self.ship.warehouse.slots.values()):
            col = i % 4
            row = i // 4
            slot_x = self.panel_rect.x + 24 + 10 + col * (64 + 10)
            slot_y = self.panel_rect.y + 20 + 10 + row * (64 + 10)
            slot_rect = pygame.Rect(slot_x, slot_y, 64, 64)

            if slot_rect.collidepoint(mouse_pos):
                if slot["good"]:  
                    self.selected_slot = f"slot_{i}"  
                    print(f"📦 [DEBUG] Schiff-Slot {self.selected_slot} mit Ware {slot['good']} ausgewählt!")
                else:
                    print("❌ Dieser Slot ist leer!")
                return True  

        # **Falls auf einen Lade-/Entladebutton geklickt wurde**
        if self.unload_button_rect and self.unload_button_rect.collidepoint(mouse_pos):
            if self.selected_slot:
                SoundManager.play_sound("click")
                print(f"📦 Ware aus Schiff-Slot {self.selected_slot} wird ins Kontor entladen!")
                return self.ship.transfer_to_warehouse(warehouse_gui.warehouse, self.selected_slot)

        if self.load_button_rect and self.load_button_rect.collidepoint(mouse_pos):
            if warehouse_gui.selected_slot is not None:
                SoundManager.play_sound("click")
                print(f"📦 Ware aus Kontor-Slot {warehouse_gui.selected_slot} wird ins Schiff geladen!")
                return self.ship.transfer_from_warehouse(warehouse_gui.warehouse, warehouse_gui.selected_slot)

        return False
