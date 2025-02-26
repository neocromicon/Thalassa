import pygame

class TimeManager:
    def __init__(self):
        self.time_of_day = 0  # Wert zwischen 0 und 1 (0 = Tagesbeginn, 1 = Tagesende)
        self.cycle_speed = 0.00004458  # Geschwindigkeit des Tag-Nacht-Zyklus

    def update(self):
        """Aktualisiert den Tag-Nacht-Zyklus."""
        self.time_of_day += self.cycle_speed
        #print(f"🌅 [DEBUG] Aktueller Tag-Nacht-Zyklus: {self.time_of_day}")
        if self.time_of_day >= 1:
            self.time_of_day = 0  # Zurücksetzen, um den Zyklus erneut zu starten

    def get_night_overlay(self, screen_size):
        """Berechnet das Nacht-Overlay basierend auf der aktuellen Tageszeit."""
        # Konfiguration für die Dunkelheitsdauer
        day_start = 0.0  # Zeitpunkt für den Start (0% Nacht, also Tag)
        day_duration = 0.4  # Zeitspanne, in der es komplett hell bleibt
        night_start = 0.5  # Zeitpunkt, ab dem es langsam dunkel wird
        night_end = 0.7  # Zeitpunkt, bis zu dem es komplett dunkel ist
        fade_duration = 0.1  # Zeitspanne für den sanften Übergang

        # Berechnung des Transparenzwerts für die Nachtfärbung mit weichem Übergang
        if self.time_of_day < day_start + day_duration:
            night_intensity = 0  # Tag bleibt hell
        elif day_start + day_duration <= self.time_of_day < night_start - fade_duration:
            blend_factor = (self.time_of_day - (day_start + day_duration)) / (night_start - (day_start + day_duration))
            night_intensity = blend_factor
        elif night_start - fade_duration <= self.time_of_day < night_start:
            blend_factor = (self.time_of_day - (night_start - fade_duration)) / fade_duration
            night_intensity = blend_factor
        elif night_start <= self.time_of_day <= night_end:
            night_intensity = 1  # Maximale Nachtintensität
        elif night_end < self.time_of_day <= night_end + fade_duration:
            blend_factor = (self.time_of_day - night_end) / fade_duration
            night_intensity = 1 - blend_factor
        else:
            blend_factor = (self.time_of_day - (night_end + fade_duration)) / (1.0 - (night_end + fade_duration))
            night_intensity = max(0, 1 - blend_factor)

        # Alpha-Wert berechnen
        alpha = int(200 * night_intensity)

        #print(f"🌙 Nachtintensität: {night_intensity * 100:.2f}% (Alpha: {alpha})")

        # Nacht-Overlay erzeugen
        overlay = pygame.Surface(screen_size, pygame.SRCALPHA)
        overlay.fill((0, 0, 255, alpha // 4))  # Blautönung für die Nacht
        return overlay
