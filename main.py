import pygame
from data.scripts.Constants import MAIN_MENU, MAIN_INGAME_MENU, GAME_RUNNING
from data.scripts.GUI.MainMenu import MainMenu
from data.scripts.GUI.MainIngameMenu import MainIngameMenu
from data.scripts.Game import Game
from data.scripts.MapGenerator.Settings import MAP_HEIGHT, MAP_WIDTH
from data.scripts.Managers.SettingsManager import SettingsManager 

# Hauptklasse, die das Menü und das Spiel verwaltet
class ThalassaGame:
    def __init__(self):
        pygame.init()
        icon = pygame.image.load("Thalassa.ico")
        pygame.display.set_icon(icon)

        # Lade die Auflösung und den Vollbildmodus aus der settings.json
        resolution = SettingsManager.load_resolution_from_settings()
        fullscreen = SettingsManager.load_video_mode_from_settings()

        # Bildschirm entsprechend der geladenen Einstellungen initialisieren
        if fullscreen == "fullscreen":
            self.screen = pygame.display.set_mode(resolution, pygame.FULLSCREEN)
        else:
            self.screen = pygame.display.set_mode(resolution)

        pygame.display.set_caption("Thalassa")
        self.clock = pygame.time.Clock()
        self.game_state = MAIN_MENU  # Start im Hauptmenü

        # Spiel und Menüs initialisieren
        self.game = Game(self.screen, MAP_WIDTH, MAP_HEIGHT)
        self.main_menu = MainMenu(self.screen, self.game)
        self.main_ingame_menu = MainIngameMenu(self.screen, self.game)

    def run(self):
        while True:
            # FPS-Limit auf 60 Frames pro Sekunde
            self.clock.tick(60)
            # Zustand 1: Hauptmenü wird angezeigt
            if self.game_state == MAIN_MENU:
                self.main_menu.run()  # Starte das Hauptmenü
                if self.main_menu.start_game:
                    if not self.game:
                        self.game = Game(self.screen)
                        self.main_ingame_menu = MainIngameMenu(self.screen, self.game)

                    self.game_state = GAME_RUNNING

            # Zustand 2: Spiel läuft
            elif self.game_state == GAME_RUNNING:
                self.game.run()  # Starte oder setze das Spiel fort
                if self.game.back_to_menu:
                    self.game_state = MAIN_INGAME_MENU  # Öffne das Ingame-Pause-Menü bei ESC
                    self.main_ingame_menu.start_game = False  # Setze das Start-Flag des Ingame-Menüs zurück

            # Zustand 3: Ingame-Pause-Menü ist aktiv
            elif self.game_state == MAIN_INGAME_MENU:
                self.main_ingame_menu.run()  # Starte das Ingame-Menü (Pause-Menü)
                if self.main_ingame_menu.start_game:
                    self.game.pause_game = False  # Pausenstatus aufheben
                    self.game.back_to_menu = False  # Rückkehr ins Spiel ermöglichen
                    self.game_state = GAME_RUNNING  # Kehre ins Spiel zurück

if __name__ == "__main__":
    game = ThalassaGame()
    game.run()
