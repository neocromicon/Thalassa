from data.scripts.GUI.Game.WarehouseGUI import WarehouseGUI


class WarehouseManager:
    def __init__(self, max_slots=5, island_id=None, sub_id=0):
        self.max_slots = max_slots
        self.slots = {i: {"good": None, "quantity": 0, "max_quantity": 50} for i in range(max_slots)}
        self.island_id = island_id  # 🔥 Speichert, zu welcher Insel das Kontor gehört
        self.sub_id = sub_id  # 🔥 Sub-ID, falls später mehrere Lager pro Insel existieren sollen
        self.gui = WarehouseGUI(self)

    def add_good(self, good_type, quantity):
        """Lagert eine Ware ins Kontor ein, erst existierende Slots auffüllen, dann neue belegen."""
        for slot in self.slots.values():
            if slot["good"] == good_type:
                addable = min(quantity, slot["max_quantity"] - slot["quantity"])
                slot["quantity"] += addable
                quantity -= addable
                if quantity == 0:
                    return True  # Alles wurde eingelagert

        # Falls noch Rest übrig ist → nächster freier Slot
        for slot_id, slot in self.slots.items():
            if slot["good"] is None:
                self.slots[slot_id] = {
                    "good": good_type,
                    "quantity": min(quantity, 50),
                    "max_quantity": 50
                }
                return True
        return False  # Kein Platz mehr

    def remove_good(self, good_type, quantity):
        """Entnimmt Waren aus dem Lager."""
        total = sum(s["quantity"] for s in self.slots.values() if s["good"] == good_type)
        if total < quantity:
            return False  # Nicht genug vorhanden

        for slot in self.slots.values():
            if slot["good"] == good_type:
                remove = min(quantity, slot["quantity"])
                slot["quantity"] -= remove
                quantity -= remove
                if slot["quantity"] == 0:
                    slot["good"] = None  # Slot leeren

        return True  # Waren erfolgreich entfernt

    def get_quantity(self, good):
        """Gibt die Gesamtmenge eines bestimmten Guts im Lager zurück."""
        return sum(slot["quantity"] for slot in self.slots.values() if slot["good"] == good)

    def get_inventory(self):
        """Gibt das gesamte Inventar dieses Kontors zurück."""
        return {slot["good"]: slot["quantity"] for slot in self.slots.values() if slot["good"] is not None}

    def get_island_inventory(self, island_id):
        """Gibt den Lagerbestand für eine gesamte Insel zurück (falls mehrere Kontore existieren sollten)."""
        if self.island_id == island_id:
            return self.get_inventory()
        return {}  # Falls das Lager nicht zur Insel gehört, gibt es keinen Bestand zurück

    def find_slot_with_good(self, good_type):
        """Findet den ersten Slot, der das gewünschte Gut enthält."""
        for slot_id, slot in self.slots.items():
            if slot["good"] == good_type and slot["quantity"] > 0:
                return slot_id
        return None  # Falls kein Slot mit der Ware gefunden wurde
