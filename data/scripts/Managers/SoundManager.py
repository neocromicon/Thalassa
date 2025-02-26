import pygame
import os

class SoundManager:
    """Verwaltet globale Soundeffekte und Musik für das Spiel."""
    
    SOUND_PATHS = {
        "click": "data/sounds/button_click.wav",
        "build": "data/sounds/build.wav",
        "ship_horn": "data/sounds/ship_horn.wav",
        "background_music": "data/music/background.ogg"
    }
    
    sounds = {}
    
    @classmethod
    def load_sounds(cls):
        """Lädt alle Sounds einmalig in den Speicher."""
        pygame.mixer.init()
        for name, path in cls.SOUND_PATHS.items():
            if os.path.exists(path):
                cls.sounds[name] = pygame.mixer.Sound(path)
            else:
                print(f"⚠ Warnung: Sounddatei '{path}' nicht gefunden!")

    @classmethod
    def play_sound(cls, sound_name, volume=1.0):
        """Spielt einen Sound aus dem Sound-Manager global ab."""
        if sound_name in cls.sounds:
            sound = cls.sounds[sound_name]
            sound.set_volume(volume)
            sound.play()
        else:
            print(f"❌ Fehler: Sound '{sound_name}' nicht geladen oder nicht vorhanden.")

    @classmethod
    def play_music(cls, sound_name, loop=-1, volume=0.5):
        """Spielt Musik im Hintergrund ab."""
        if sound_name in cls.SOUND_PATHS:
            path = cls.SOUND_PATHS[sound_name]
            if os.path.exists(path):
                pygame.mixer.music.load(path)
                pygame.mixer.music.set_volume(volume)
                pygame.mixer.music.play(loop)
            else:
                print(f"❌ Fehler: Musikdatei '{path}' nicht gefunden.")
        else:
            print(f"❌ Fehler: Musik-Sound '{sound_name}' nicht vorhanden.")

    @classmethod
    def stop_music(cls):
        """Stoppt die Hintergrundmusik."""
        pygame.mixer.music.stop()

# Lade alle Sounds beim Importieren des Moduls
SoundManager.load_sounds()
