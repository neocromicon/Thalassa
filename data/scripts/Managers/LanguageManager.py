from tkinter import ON
import json5
import json
import os

from data.scripts.Managers.SettingsManager import SettingsManager
from data.scripts.MapGenerator.Settings import MAP_HEIGHT, MAP_WIDTH

class LanguageManager:
    def __init__(self):
        self.language = SettingsManager.load_language()  # Sprache aus SettingsManager laden
        self.translations = {}
        self.load_language()

    def load_language_from_settings(self):
        """Lädt die Sprache aus der settings.json, Standard ist Deutsch."""
        settings_path = "settings.json"
        if os.path.exists(settings_path):
            with open(settings_path, 'r') as file:
                settings = json.load(file)
                return settings.get("language", "de")
        return "de"

    def save_language_to_settings(self):
        """Speichert die aktuelle Sprache in settings.json über den SettingsManager."""
        SettingsManager.save_language(self.language)

    def load_language(self):
        """Lädt die Sprachdatei basierend auf der gewählten Sprache."""
        path = f"data/lang/{self.language}.json5"
        if not os.path.exists(path):
            print(f"Sprachdatei '{path}' nicht gefunden. Standard auf Deutsch.")
            path = "data/lang/de.json5"

        with open(path, 'r', encoding='utf-8') as file:
            self.translations = json5.load(file)

    def get(self, key):
        """Gibt den übersetzten Text für den angegebenen Schlüssel zurück."""
        return self.translations.get(key, key)  # Fallback: Schlüssel selbst, wenn nicht gefunden

    def set_language(self, language):
        """Setzt eine neue Sprache, speichert die Änderung und lädt die neue Sprachdatei."""
        self.language = language
        self.save_language_to_settings()  # Jetzt über SettingsManager speichern
        self.load_language()

# Globale Instanz des Sprachmanagers
LANGUAGE_MANAGER = LanguageManager()

class LanguageManagerHelper:
    @staticmethod
    def reload_menu_options(menu_instance, options_keys):
        """
        Lädt die Menüoptionen basierend auf den Sprachschlüsseln neu.
        
        Args:
            menu_instance: Das Menüobjekt, dessen Optionen aktualisiert werden sollen.
            options_keys: Eine Liste von Sprachschlüsseln für die Menüoptionen.
        """
        lang = LANGUAGE_MANAGER
        menu_instance.options = [lang.get(key) for key in options_keys]        

## Haupt und PauseMenüs
NEW_GAME = "new_game"
CONTINUE = "continue"
EMPTY_SAVE_SLOT = "empty_save_slot"
SAVE_GAME = "save_game"
ACTION_SAVE_GAME = "action_save_game"
UNTITLED = "untitled"
LOAD_GAME = "load_game"
ACTION_LOAD_GAME = "action_load_game"
SELECT_SLOT = "select_slot"
SAVE_AS = "save_as"
GAME_SAVED = "game_saved"
SAVED_SLOT = "saved_slot"
OPTIONS = "options"
CREDITS = "credits"
EXIT = "exit"
##  Options Menü
SELECT_VIDEO = "select_video"
SELECT_MOUSE = "select_mouse"
SELECT_KEYBOARD = "select_keyboard"
BACK = "back"
SELECT_LANGUAGE = "select_language"
OPTIONS_TITLE = "options_title"
## Sprachen Menü
GERMAN = "german"
ENGLISCH = "english"
CHANGE_LANG = "change_lang"
RESTART_GAME = "restart_game"
## Video Menü
VIDEO_TITLE = "video_title"
SELECT_RESOLUTION = "select_resolution"
SELECT_MODE = "select_mode"
SELECT_MODEFULLSCREEN = "select_modefullscreen"
SELECT_MODEWINDOWED = "select_modewindowed"
## Maus Menü
MOUSE_TITLE = "mouse_title"
MOUSE_SENSITIVITY = "mouse_sensitivity"
MOUSE_INVERT = "mouse_invert"
MOUSE_ZOOM_SENSITIVITY = "mouse_zoom_sensitivity"
## Tastatur Menü
KEYBOARD_TITLE = "keyboard_title"
KEYBOARD_SENSITIVITY = "keyboard_sensitivity"
KEYBOARD_INVERT = "keyboard_invert"
KEYBOARD_ZOOM_SENSITIVITY = "keyboard_zoom_sensitivity"
## Generator Menü
GENERATOR_TITLE = "generator_title"
MAP_WIDTH_TEXT = "map_width_text"
MAP_HEIGHT_TEXT = "map_height_text"
TREE_CHANCE = "tree_chance"
MOUNTAIN_CHANCE = "mountain_chance"
NUM_ISLANDS = "num_islands"
SEED = "seed"
GENERATE_MAP = "generate_map"
## Bestätigungsmeldungen
ERROR = "error"
NO_SAVE_ONSLOT = "no_save_onslot"
CHANGE_MODE = "change_mode"
CHANGE_RESOLUTION = "change_resolution"
CHANGE_BOTH_RES_MODE = "change_both_res_mode"
ON = "on"
OFF = "off"