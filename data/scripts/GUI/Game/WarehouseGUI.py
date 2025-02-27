import pygame
from data.scripts.Managers.MenuManager import MenuManager
from data.scripts.Managers.GoodManager import GoodManager
from data.scripts.MapGenerator.Settings import SCREEN_HEIGHT, SCREEN_WIDTH

class WarehouseGUI:
    def __init__(self, warehouse):
        self.warehouse = warehouse
        self.show_gui = False
        self.manually_opened = False
        self.selected_slot = None  # 📦 Speichert den aktiv ausgewählten Slot

    def handle_click(self, mouse_pos):
        """Prüft, ob ein Slot im Kontor angeklickt wurde und speichert die Auswahl."""
        if not self.show_gui:
            print("❌ [DEBUG] `handle_click()` wurde blockiert – `show_gui = False`!")
            return False
        
        print(f"📌 [DEBUG] `handle_click()` wurde aufgerufen mit Mausposition: {mouse_pos}")

        # 📦 Prüfe, ob ein Slot im Kontor angeklickt wurde
        for i, (slot_id, slot) in enumerate(self.warehouse.slots.items()):
            col = i % 4
            row = i // 4
            slot_x = self.panel_rect.x + 24 + 10 + col * (64 + 10)
            slot_y = self.panel_rect.y + 20 + 10 + row * (64 + 10)
            slot_rect = pygame.Rect(slot_x, slot_y, 64, 64)

            print(f"🔍 [DEBUG] Prüfe Slot {slot_id}: Position {slot_x},{slot_y} | Enthält: {slot['good']}")

            if slot_rect.collidepoint(mouse_pos):
                if slot["good"]:
                    self.selected_slot = slot_id  # 🔄 **Fix: Stelle sicher, dass `selected_slot` korrekt gespeichert ist**
                    print(f"✅ [DEBUG] Kontor-Slot {self.selected_slot} mit Ware {slot['good']} ausgewählt!")
                    return True
                else:
                    print("❌ [DEBUG] Dieser Slot ist leer!")

        print("❌ [DEBUG] Kein gültiger Slot wurde geklickt.")  # 🔥 Debugging
        return False

    def draw(self, screen, ship_selected, ship_gui_y=None):
        """Zeichnet die GUI des Kontors mit dynamischer Positionierung über der Schiffs-GUI."""
        if not self.show_gui:
            return

        slot_size = 64
        padding = 10
        slot_offset_x = 24
        slot_offset_y = 20
        icon_offset = 16
        max_slots_per_row = 4

        total_slots = len(self.warehouse.slots)
        num_rows = (total_slots + max_slots_per_row - 1) // max_slots_per_row
        panel_width = 480
        panel_height = max(120, num_rows * (slot_size + padding) + 50)
        panel_x = SCREEN_WIDTH - panel_width - 20
        panel_y = SCREEN_HEIGHT - panel_height - 20  # Standardposition unten rechts

        # 🏗 Falls ein Schiff selektiert ist, positioniere die Kontor-GUI über der Schiffs-GUI
        if ship_selected and ship_gui_y is not None:
            panel_y = ship_gui_y - panel_height - 10  # 10px Abstand über der Schiffs-GUI

        # **Falls die GUI zu hoch wäre, korrigieren**
        if panel_y < 10:
            panel_y = 10

        self.panel_rect = pygame.Rect(panel_x, panel_y, panel_width, panel_height)

        # Zeichne GUI-Hintergrund
        pygame.draw.rect(screen, (40, 40, 60), self.panel_rect)
        MenuManager.draw_ship_border(screen, panel_x, panel_y, panel_width, panel_height)

        # 🎯 Zeichne Slots mit Balken
        for i, slot in enumerate(self.warehouse.slots.values()):
            col = i % max_slots_per_row
            row = i // max_slots_per_row
            slot_x = panel_x + slot_offset_x + padding + col * (slot_size + padding)
            slot_y = panel_y + slot_offset_y + padding + row * (slot_size + padding)
            slot_rect = pygame.Rect(slot_x, slot_y, slot_size, slot_size)

            # **Hintergrund ändern, wenn Slot ausgewählt ist**
            if self.selected_slot == i:
                pygame.draw.rect(screen, (120, 100, 60), slot_rect)  # **Brauner Hintergrund für Auswahl**
            else:
                pygame.draw.rect(screen, (80, 80, 100), slot_rect)
            MenuManager.draw_slot_border(screen, slot_x, slot_y, slot_size)

            if slot["good"]:
                img = GoodManager.textures[slot["good"]]
                scaled_img = pygame.transform.scale(img, (slot_size - icon_offset, slot_size - icon_offset))
                screen.blit(scaled_img, (slot_x + icon_offset // 2, slot_y + icon_offset // 2))

                # 📦 **Warenmengen-Balken zeichnen**
                max_capacity = slot["max_quantity"] if "max_quantity" in slot else 50
                filled_ratio = slot["quantity"] / max_capacity if max_capacity > 0 else 0

                bar_height = 8
                bar_width = slot_size - 16
                bar_x = slot_x + 8
                bar_y = slot_y + 8

                # Balken-Hintergrund
                pygame.draw.rect(screen, (50, 50, 50), (bar_x, bar_y, bar_width, bar_height))
                # Gefüllter Bereich
                pygame.draw.rect(screen, (255, 200, 0), (bar_x, bar_y, int(bar_width * filled_ratio), bar_height))