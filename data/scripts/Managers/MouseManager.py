import pygame

from data.scripts.Managers.ShipManager import ShipManager
from data.scripts.MapGenerator.Settings import TILE_SIZE

class MouseManager:
    def __init__(self, game):
        """Initialisiert den Maus-Manager mit einer Referenz auf das Game-Objekt."""
        self.game = game
        self.right_click_start_time = None
        self.camera_moved = False
        self.right_click_held = False

    def handle_left_click(self, event, mouse_x, mouse_y):
        """Verarbeitet Linksklick-Events (Kontor auswählen, GUI-Klicks, Schiffsauswahl, Mehrfachauswahl)."""
        if event.button == 1:
            warehouse_gui = None  
            ship_gui = None
            clicked_ship = None
            clicked_warehouse = None  

            # 📌 **Prüfe, ob auf ein Kontor geklickt wurde (nun mit Insel-ID!)**
            for building in self.game.building_manager.buildings:
                if building["type"] == "office":
                    kontor_x, kontor_y = building["pos"]
                    screen_x, screen_y = self.game.camera.apply((kontor_x * TILE_SIZE, kontor_y * TILE_SIZE))
                    kontor_rect = pygame.Rect(screen_x, screen_y, TILE_SIZE, TILE_SIZE)

                    if kontor_rect.collidepoint(mouse_x, mouse_y):
                        print(f"🏛️ Kontor an ({kontor_x}, {kontor_y}) auf Insel {building['island_id']} ausgewählt!")
                        clicked_warehouse = building["warehouse"].gui  # ✅ Speichere das geklickte Kontor

            # **Falls ein Kontor geklickt wurde, alle anderen schließen**
            if clicked_warehouse:
                for building in self.game.building_manager.buildings:
                    warehouse_gui = building["warehouse"].gui
                    if warehouse_gui != clicked_warehouse:  # ❌ Alle anderen schließen
                        warehouse_gui.show_gui = False
                        warehouse_gui.manually_opened = False  

                clicked_warehouse.show_gui = True  # ✅ Nur das aktuelle Kontor öffnen
                clicked_warehouse.manually_opened = True  
                return  

            # **Falls kein Schiff oder Kontor angeklickt wurde → Schließe GUI**
            if not self.game.selected_ships:
                for building in self.game.building_manager.buildings:
                    warehouse_gui = building["warehouse"].gui
                    if warehouse_gui.show_gui and warehouse_gui.manually_opened:
                        warehouse_gui.show_gui = False  
                        warehouse_gui.manually_opened = False  
                        print("❌ Klick in die Welt → Manuell geöffnete Kontor-GUI geschlossen.")

            # 🏗 Falls ein Gebäude aktiv ist, platziere es
            if self.game.building_manager.selected_ship:
                self.game.building_manager.place_office()
                return

            # **Falls ein Schiff in der Nähe eines Kontors ist → `warehouse_gui` abrufen**
            for ship in self.game.ships:
                warehouse_gui = ship.is_near_warehouse(return_gui=True)  
                ship_gui = ship.gui
                if warehouse_gui:
                    break  

            # **Falls auf die Kontor-GUI geklickt wurde**
            if warehouse_gui and warehouse_gui.panel_rect.collidepoint(mouse_x, mouse_y):
                print("📌 Klick in der WarehouseGUI erkannt – Schiff bleibt ausgewählt.")
                warehouse_gui.handle_click((mouse_x, mouse_y))  
                return  

            # **Falls auf die Schiff-GUI geklickt wurde, Auswahl nicht aufheben**
            for ship in self.game.ships:
                if ship.gui.show_gui and ship.gui.is_hovered((mouse_x, mouse_y)):
                    print("📌 Klick in der ShipGUI erkannt – Schiff bleibt ausgewählt.")
                    ship.gui.handle_click((mouse_x, mouse_y), warehouse_gui)  
                    return  

            # 🚢 Falls auf ein Schiff geklickt wurde, wähle es aus
            for ship in self.game.ships:
                if ship.is_clicked(mouse_x, mouse_y, self.game.camera):
                    clicked_ship = ship
                    break  

            if clicked_ship:  
                if clicked_ship in self.game.selected_ships:  
                    self.game.selected_ships.remove(clicked_ship)
                    clicked_ship.selected = False  
                    clicked_ship.gui.show_gui = False
                else:
                    for ship in self.game.selected_ships:
                        ship.selected = False  
                        ship.gui.show_gui = False
                    
                    self.game.selected_ships = [clicked_ship]
                    clicked_ship.selected = True
                    clicked_ship.gui.show_gui = True
            else:  
                # Falls kein Schiff mehr aktiv ist → Slot zurücksetzen
                for ship in self.game.ships:
                    ship.gui.selected_slot = None
                # Falls kein Schiff angeklickt wurde → Mehrfachauswahl starten
                self.game.selection_start = (mouse_x, mouse_y)
                self.game.selection_active = True

        elif event.button == 3 and self.game.building_manager.selected_ship:
            print("❌ Bau-Modus abgebrochen!")
            self.game.building_manager.cancel_building()
            return
        elif event.button == 3:  # **Rechtsklick → Kamera bewegen ODER Schiffe bewegen**
            self.right_click_start_time = pygame.time.get_ticks()
            self.last_mouse_pos = pygame.mouse.get_pos()
            self.right_click_held = True
            self.camera_moved = False  
        elif event.button in [4, 5]:  # Mausrad nach oben/unten
                zoom_amount = 1 if event.button == 4 else -1
                self.game.camera.apply_zoom(zoom_amount, mouse_x, mouse_y)

    def handle_mouse_release(self, event, mouse_x, mouse_y):
        """Verarbeitet das Loslassen der Maustasten (Mehrfachauswahl & Schiffsbewegung)."""

        if event.button == 1 and self.game.selection_active:  # **Linksklick loslassen = Mehrfachauswahl**
            selection_rect = pygame.Rect(
                min(self.game.selection_start[0], mouse_x),
                min(self.game.selection_start[1], mouse_y),
                abs(self.game.selection_start[0] - mouse_x),
                abs(self.game.selection_start[1] - mouse_y)
            )

            new_selection = [ship for ship in self.game.ships if ship.is_clicked_in_rect(selection_rect, self.game.camera)]

            # **Falls keine Schiffe markiert wurden → Auswahl leeren**
            for ship in self.game.selected_ships:
                ship.selected = False
                ship.gui.show_gui = False

            self.game.selected_ships = new_selection

            if self.game.selected_ships:
                for ship in self.game.selected_ships:
                    ship.selected = True
                    ship.gui.show_gui = True

            self.game.selection_active = False  

        elif event.button == 3 and self.game.building_manager.selected_ship:
            return  # Falls ein Gebäude gebaut wird, bricht Rechtsklick nur den Bau ab.

        elif event.button == 3:  # **Rechtsklick loslassen = Schiffe bewegen**
            self.handle_ship_movement(mouse_x, mouse_y)

            self.right_click_held = False
            self.last_mouse_pos = None

    def handle_ship_movement(self, mouse_x, mouse_y):
        """Leitet die Bewegung an den ShipManager weiter und sorgt für eine Formation."""

        current_time = pygame.time.get_ticks()
        click_duration = current_time - self.right_click_start_time

        # ❌ Falls die Kamera bewegt wurde, Schiffe NICHT bewegen
        if self.camera_moved or click_duration >= 200:
            return

        # 📌 **Berechne Weltkoordinaten der Klickposition**
        world_x = (mouse_x / self.game.camera.zoom) + self.game.camera.tile_x * TILE_SIZE
        world_y = (mouse_y / self.game.camera.zoom) + self.game.camera.tile_y * TILE_SIZE

        # 🚢 **Falls mehrere Schiffe ausgewählt sind, verwende die Gruppenbewegung**
        if len(self.game.selected_ships) > 1:
            ShipManager.move_group_to(self.game, world_x, world_y)
            print("🚢 Gruppenbewegung")
        else:
            # 🚢 Einzelnes Schiff direkt bewegen
            for ship in self.game.selected_ships:
                ship.move_to(world_x, world_y)

        # **Rechtsklick-Steuerung wieder freigeben**
        self.right_click_held = False
        self.camera_moved = False  # Setzt Kamera zurück, sodass sie wieder bewegt werden kann

    def handle_mouse_motion(self, mouse_x, mouse_y):
        """Verarbeitet Mausbewegungen für Kamera & Mehrfachauswahl."""
        
        # 🟢 Falls eine Mehrfachauswahl aktiv ist, aktualisiere den Auswahlbereich
        if self.game.selection_active:
            self.game.selection_end = pygame.mouse.get_pos()

        # 🔵 Falls Rechtsklick gehalten wird → Kamera bewegen
        if self.right_click_held and self.last_mouse_pos:
            dx, dy = mouse_x - self.last_mouse_pos[0], mouse_y - self.last_mouse_pos[1]

            # **Kamera nur bewegen, wenn Maus sich genug bewegt hat**
            if abs(dx) > 2 or abs(dy) > 2:
                self.camera_moved = True  # Kamera wurde bewegt

            self.game.camera.move_with_mouse(-dx, -dy)  # Kamera bewegen
            self.last_mouse_pos = (mouse_x, mouse_y)  # Neue Mausposition speichern