import os
import json
from data.scripts.Managers.LanguageManager import UNTITLED, EMPTY_SAVE_SLOT

class SaveManager:
    def __init__(self, lang_manager):
        self.lang = lang_manager
        self.saves_cache = self.load_all_saves()

    def load_all_saves(self):
        """Lädt alle Speicherstände einmalig in den Cache."""
        saves = {}
        for i in range(1, 10):
            filename = f"save_{i}.json"
            if os.path.exists(filename):
                with open(filename, "r") as file:
                    save_data = json.load(file)
                    save_name = save_data.get("save_name", self.lang.get(UNTITLED))
                    saves[i] = save_name
            else:
                saves[i] = self.lang.get(EMPTY_SAVE_SLOT)
        return saves

    def get_existing_saves(self):
        """Gibt die Liste der Speicherstände aus dem Cache zurück."""
        return [f"Slot {i}: {name}" for i, name in self.saves_cache.items()]

    def get_existing_save_name(self, slot):
        """Gibt den Namen des Speicherstandes aus dem Cache zurück."""
        return self.saves_cache.get(slot, self.lang.get(UNTITLED))

    def refresh_saves_cache(self):
        """Aktualisiert den Cache, wenn neue Speicherstände erstellt werden."""
        self.saves_cache = self.load_all_saves()

    def save_exists(self, slot):
        """Prüft, ob der Speicherstand für den ausgewählten Slot existiert."""
        filename = f"save_{slot}.json"
        return os.path.exists(filename)
