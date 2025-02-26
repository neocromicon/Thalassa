import json
import os

class SettingsManager:
    """Verwaltet das Laden und Speichern von Einstellungen in 'settings.json'."""
    
    SETTINGS_PATH = "settings.json"

    # ------------------------------------------------------------------
    # Allgemeine Funktionen zum Laden und Speichern von Einstellungen
    # ------------------------------------------------------------------

    @staticmethod
    def load_setting(key, default_value):
        """Lädt eine einzelne Einstellung aus der settings.json oder gibt einen Standardwert zurück."""
        if os.path.exists(SettingsManager.SETTINGS_PATH):
            with open(SettingsManager.SETTINGS_PATH, 'r') as file:
                settings = json.load(file)
                return settings.get(key, default_value)
        return default_value

    @staticmethod
    def update_settings(key, value):
        """Aktualisiert einen bestimmten Wert in der settings.json, ohne andere Einstellungen zu überschreiben."""
        settings = {}

        # Existierende Einstellungen laden
        if os.path.exists(SettingsManager.SETTINGS_PATH):
            with open(SettingsManager.SETTINGS_PATH, 'r') as file:
                settings = json.load(file)

        # Wert aktualisieren oder hinzufügen
        settings[key] = value

        # Änderungen in der Datei speichern
        with open(SettingsManager.SETTINGS_PATH, 'w') as file:
            json.dump(settings, file, indent=4)

        print(f"Einstellung '{key}' wurde aktualisiert: {value}")

    # -------------------------------
    # Einstellungen für Sprache
    # -------------------------------

    @staticmethod
    def save_language(language):
        """Speichert die aktuelle Sprache in settings.json, ohne andere Einstellungen zu überschreiben."""
        SettingsManager.update_settings("language", language)
        print(f"Sprache wurde auf '{language}' gesetzt.")

    @staticmethod
    def load_language():
        """Lädt die Sprache aus settings.json, Standard ist 'de'."""
        return SettingsManager.load_setting("language", "de")

    # -------------------------------------------------
    # Einstellungen für Bildschirmauflösung und Modus
    # -------------------------------------------------

    @staticmethod
    def load_resolution_from_settings():
        """Lädt die Bildschirmauflösung aus der settings.json. Standard: 1366x768."""
        if os.path.exists(SettingsManager.SETTINGS_PATH):
            with open(SettingsManager.SETTINGS_PATH, 'r') as file:
                settings = json.load(file)
                resolution = settings.get('resolution', {'width': 1366, 'height': 768})
                return (resolution['width'], resolution['height'])
        return (1366, 768)

    @staticmethod
    def load_video_mode_from_settings():
        """Lädt den Bildschirmmodus (Fenster/Vollbild) aus der settings.json. Standard: 'windowed'."""
        if os.path.exists(SettingsManager.SETTINGS_PATH):
            with open(SettingsManager.SETTINGS_PATH, 'r') as file:
                settings = json.load(file)
                return settings.get('mode', 'windowed')
        return 'windowed'

    @staticmethod
    def save_settings(resolution, fullscreen):
        """Speichert die Bildschirmauflösung und den Bildschirmmodus in der settings.json."""
        mode = 'fullscreen' if fullscreen else 'windowed'
        settings = {
            'resolution': {'width': resolution[0], 'height': resolution[1]},
            'mode': mode
        }
        with open(SettingsManager.SETTINGS_PATH, 'w') as file:
            json.dump(settings, file, indent=4)

    @staticmethod
    def load_current_resolution_index(self):
        """Lädt die aktuelle Auflösung aus der settings.json und gibt den Index zurück."""
        if os.path.exists(SettingsManager.SETTINGS_PATH):
            with open(SettingsManager.SETTINGS_PATH, 'r') as file:
                settings = json.load(file)
                resolution = settings.get('resolution', {'width': 1366, 'height': 768})
                current_resolution = (resolution['width'], resolution['height'])

                if current_resolution in self.resolutions:
                    return self.resolutions.index(current_resolution)
        return 0

    @staticmethod
    def load_current_mode_index(self):
        """Lädt den aktuellen Bildschirmmodus aus der settings.json und gibt den Index zurück."""
        mode = SettingsManager.load_video_mode_from_settings()
        return 1 if mode == 'fullscreen' else 0  # Index 1 = Vollbild, Index 0 = Fenstermodus

    # -------------------------------
    # Einstellungen für Eingaben (Maus & Tastatur)
    # -------------------------------

    @staticmethod
    def load_input_settings():
        """Lädt die Eingabeeinstellungen für Maus und Tastatur aus der settings.json."""
        return {
            # Maus
            "m_sensitivity": SettingsManager.load_setting("mouse_sensitivity", 1.0),
            "m_invert": SettingsManager.load_setting("mouse_invert", False),
            "m_zoom_sensitivity": SettingsManager.load_setting("mouse_zoom_sensitivity", 1.0),
            # Tastatur
            "k_sensitivity": SettingsManager.load_setting("keyboard_sensitivity", 0.5),
            "k_invert": SettingsManager.load_setting("keyboard_invert", False),
            "k_zoom_sensitivity": SettingsManager.load_setting("keyboard_zoom_sensitivity", 0.1),
        }
