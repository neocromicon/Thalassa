import random
from collections import deque

class Tile:
    def __init__(self, base="Ocean"):
        self._base = base  # 🏆 Basis-Typ als private Variable speichern
        self.navigable_mask = None
        self.set_navigation_mask()
        self.overlay = None
        self.ocean_anim_index = None
        self.start_offset = 0
    
    def set_ocean_animation(self, offset):
        self.ocean_anim_index = offset
        self.start_offset = offset

    def set_navigation_mask(self):
        """Definiert befahrbare Bereiche basierend auf dem Tile-Typ."""
        # Nur untere 50% befahrbar (0 = blockiert, 1 = befahrbar)
        #if self._base != "Ocean":
            #print(f"🛠 Setze Navigationsmaske für {self._base}") 

        # Standardmäßig alles befahrbar für Wasser
        self.navigable_mask = None

        if self._base == "Coast_Bottom_Left":
            self.navigable_mask = [
                [0, 0, 0, 0],
                [1, 1, 1, 0],
                [1, 1, 1, 0],
                [1, 1, 1, 0]
            ]
        if self._base == "Coast_Bottom_Left_Curve":
            self.navigable_mask = [
                [0, 0, 0, 0],
                [1, 1, 1, 0],
                [1, 1, 1, 0],
                [1, 1, 1, 0]
            ]
        if self._base == "Coast_Bottom_Middle":
            self.navigable_mask = [
                [0, 0, 0, 0],
                [1, 1, 1, 1],
                [1, 1, 1, 1],
                [1, 1, 1, 1]
            ]
        if self._base == "Coast_Bottom_Right":
            self.navigable_mask = [
                [0, 0, 0, 1],
                [0, 0, 0, 1],
                [0, 0, 0, 1],
                [1, 1, 1, 1]
            ]
        if self._base == "Coast_Bottom_Right_Curve":
            self.navigable_mask = [
                [0, 0, 0, 0],
                [0, 1, 1, 1],
                [0, 1, 1, 1],
                [0, 1, 1, 1]
            ]
        if self._base == "Coast_Middle_Left":
            self.navigable_mask = [
                [1, 1, 1, 0],
                [1, 1, 1, 0],
                [1, 1, 1, 0],
                [1, 1, 1, 0]
            ]
        if self._base == "Coast_Middle_Right":
            self.navigable_mask = [
                [0, 1, 1, 1],
                [0, 1, 1, 1],
                [0, 1, 1, 1],
                [0, 1, 1, 1]
            ]
        if self._base == "Coast_Top_Left":
            self.navigable_mask = [
                [1, 1, 1, 1],
                [1, 1, 1, 1],
                [1, 1, 1, 0],
                [1, 1, 0, 0]
            ]
        if self._base == "Coast_Top_Left_Curve":
            self.navigable_mask = [
                [1, 1, 1, 0],
                [1, 1, 1, 0],
                [1, 1, 1, 0],
                [1, 1, 1, 0]
            ]
        if self._base == "Coast_Top_Middle":
            self.navigable_mask = [
                [1, 1, 1, 1],
                [1, 1, 1, 1],
                [1, 1, 1, 1],
                [1, 1, 1, 1]
            ]
        if self._base == "Coast_Top_Right":
            self.navigable_mask = [
                [1, 1, 1, 1],
                [1, 1, 1, 1],
                [0, 1, 1, 1],
                [0, 0, 1, 1]
            ]
        if self._base == "Coast_Top_Right_Curve":
            self.navigable_mask = [
                [0, 1, 1, 1],
                [0, 1, 1, 1],
                [0, 1, 1, 1],
                [0, 1, 1, 1]
            ]
        if self._base == "Coast_South_Bottom_Left":
            self.navigable_mask = [
                [0, 0, 0, 0],
                [1, 1, 1, 0],
                [1, 1, 1, 0],
                [1, 1, 1, 0]
            ]
        if self._base == "Coast_South_Bottom_Left_Curve":
            self.navigable_mask = [
                [0, 0, 0, 0],
                [1, 1, 1, 0],
                [1, 1, 1, 0],
                [1, 1, 1, 0]
            ]
        if self._base == "Coast_South_Bottom_Middle":
            self.navigable_mask = [
                [0, 0, 0, 0],
                [1, 1, 1, 1],
                [1, 1, 1, 1],
                [1, 1, 1, 1]
            ]
        if self._base == "Coast_South_Bottom_Right":
            self.navigable_mask = [
                [0, 0, 0, 1],
                [0, 0, 0, 1],
                [0, 0, 0, 1],
                [1, 1, 1, 1]
            ]
        if self._base == "Coast_South_Bottom_Right_Curve":
            self.navigable_mask = [
                [0, 0, 0, 0],
                [0, 1, 1, 1],
                [0, 1, 1, 1],
                [0, 1, 1, 1]
            ]
        if self._base == "Coast_South_Middle_Left":
            self.navigable_mask = [
                [1, 1, 1, 0],
                [1, 1, 1, 0],
                [1, 1, 1, 0],
                [1, 1, 1, 0]
            ]
        if self._base == "Coast_South_Middle_Right":
            self.navigable_mask = [
                [0, 1, 1, 1],
                [0, 1, 1, 1],
                [0, 1, 1, 1],
                [0, 1, 1, 1]
            ]
        if self._base == "Coast_South_Top_Left":
            self.navigable_mask = [
                [1, 1, 1, 1],
                [1, 1, 1, 1],
                [1, 1, 1, 0],
                [1, 1, 0, 0]
            ]
        if self._base == "Coast_South_Top_Left_Curve":
            self.navigable_mask = [
                [1, 1, 1, 0],
                [1, 1, 1, 0],
                [1, 1, 1, 0],
                [1, 1, 1, 0]
            ]
        if self._base == "Coast_South_Top_Middle":
            self.navigable_mask = [
                [1, 1, 1, 1],
                [1, 1, 1, 1],
                [1, 1, 1, 1],
                [1, 1, 1, 1]
            ]
        if self._base == "Coast_South_Top_Right":
            self.navigable_mask = [
                [1, 1, 1, 1],
                [1, 1, 1, 1],
                [0, 1, 1, 1],
                [0, 0, 1, 1]
            ]
        if self._base == "Coast_South_Top_Right_Curve":
            self.navigable_mask = [
                [0, 1, 1, 1],
                [0, 1, 1, 1],
                [0, 1, 1, 1],
                [0, 1, 1, 1]
            ]

    @property
    def base(self):
        return self._base

    @base.setter
    def base(self, new_base):
        """🏆 Automatische Aktualisierung der Navigationsmaske beim Setzen von `base`."""
        if self._base != new_base:
            self._base = new_base
            self.set_navigation_mask()  # 🚀 Jedes Mal aufrufen, wenn `base` geändert wird!

class TileMap:
    def __init__(self, map_width, map_height, tree_chance, mountain_chance, num_islands, seed=None, generate=True):
        """
        width, height: Kartengröße in Tiles
        tree_chance, mountain_chance: aktuell optional, falls du Bäume/Berge später platzieren willst
        num_islands: fester int oder Range [min,max]
        self.seed: reproduzierbare Seeds
        generate: wenn True => ruft am Ende automatisch generate_world() auf
        """
        self.width = map_width
        self.height = map_height
        self.tree_chance = tree_chance
        self.mountain_chance = mountain_chance
        self.blocked = [[False]*self.width for _ in range(self.height)]
        self.map = [[None for _ in range(self.width)] for _ in range(self.height)]  # Dummy-Initialisierung
        self.island_cache = {}

        if isinstance(num_islands, list):
            self.num_islands = random.randint(num_islands[0], num_islands[1])
        else:
            self.num_islands = num_islands

        self.seed = seed

        if self.seed is not None:
            random.seed(self.seed)
            
        self.map = [[Tile("Ocean") for _ in range(map_width)] for _ in range(map_height)]

        if generate:
            self.generate_world()
            print(f"Fertige Welt mit Seed: {self.seed}")

    def generate_world(self):
        """
        Gesamte Weltgenerierung in einem Aufruf:
          1) Inseln per BFS generieren
          2) Eingeschlossenes Wasser füllen
          3) Zu kleine Inseln entfernen
          4) 1-2 Durchläufe Smoothing
          5) Coastlines
          6) (Optional) Bäume / Berge
        """
        self._generate_islands()
        self._ensure_minimum_islands()
        self._fill_enclosed_water()
        self._remove_small_islands(threshold=20)
        self._smooth_islands(iterations=3, land_threshold=2)
        self._remove_land_spikes(min_neighbors=2, iterations=100)
        self._apply_coastlines()
        self._apply_south_coastlines()
        self._create_water_border()
        self._apply_ocean_transitions()
        self._finalize_ocean_border(border_margin=3)
        self._generate_forest_and_mountains()  
        self._add_ocean_animation(chance=0.1)
        self.bottom_right_edge = self.find_bottom_right_edge()
        print(f"Rechte unterste Kante gefunden bei: {self.bottom_right_edge}")

    # ----------------------------------------------------------------
    # (1) Inseln per BFS
    # ----------------------------------------------------------------
    def _generate_islands(self):
        MIN_ISLAND_SIZE = 50
        LAND_EXPANSION_CHANCE = 0.46
        BORDER_MARGIN = 8  # min. Abstand vom Rand
        MID_LINE = self.height // 2  # Trennlinie zwischen Nord & Süd

        # 1) blocked-Array anlegen (alles False am Anfang)
        self.blocked = [[False]*self.width for _ in range(self.height)]

        # 2) Schleife für mehrere Inseln
        for _ in range(self.num_islands):
            # a) Seed finden, das nicht blockiert ist
            start_tile = self._find_seed(BORDER_MARGIN)
            
            if not start_tile:
                # Keinen gültigen Platz mehr gefunden => Abbruch
                break

            sx, sy = start_tile
            is_north = sy < MID_LINE  # Entscheidet das Biom

            if is_north:
                base_tile = "Grass"
            else:
                base_tile = "South_Sand"

            self.map[sy][sx].base = base_tile

            # c) BFS-Ausbreitung
            land_tiles = self._expand_island((sx, sy), LAND_EXPANSION_CHANCE, BORDER_MARGIN, base_tile)

            # d) Komplettes Landmass (inklusive BFS-Ausbreitung) einsammeln
            total_landmass = self._collect_landmass(sx, sy)

            # Inselgröße checken
            if len(total_landmass) < MIN_ISLAND_SIZE:
                # zu klein => verwerfen
                for (x, y) in total_landmass:
                    self.map[y][x].base = "Ocean"
            else:
                # e) Wenn Insel OK, blockiere Umkreis
                self._mark_blocked_area(total_landmass, distance=12)

    def _find_seed(self, margin, max_tries=1000):
        """
        Sucht zufällig ein "Ocean"-Tile, das 
        a) mind. 'margin' Tiles vom Rand entfernt ist
        b) NICHT in blocked[] steht
        """
        for _ in range(max_tries):
            x = random.randint(margin, self.width - margin - 1)
            y = random.randint(margin, self.height - margin - 1)

            if not self.blocked[y][x]:  # <-- Neu: skippe geblockte Tiles
                if self.map[y][x].base == "Ocean":
                    return (x, y)

        return None


    def _expand_island(self, start_seed, chance, margin, base_tile):
        stack = [start_seed]
        created_land = []  # Hier merken wir uns neue Land-Tiles

        # Bestimme Trennlinie
        MID_LINE = self.height // 2
        is_north = start_seed[1] < MID_LINE  # Biom des Start-Tiles

        while stack:
            cx, cy = stack.pop()

            # Check der 4 Nachbarn
            for nx, ny in [(cx, cy - 1), (cx, cy + 1), (cx - 1, cy), (cx + 1, cy)]:
                if margin <= nx < self.width - margin and margin <= ny < self.height - margin:
                    
                    # Biom-Grenze beachten:
                    # - Nördliche Inseln dürfen nicht nach Süden wachsen
                    # - Südliche Inseln dürfen nicht nach Norden wachsen
                    if is_north and ny >= MID_LINE:
                        continue  # Nord-Insel => nicht nach Süden!
                    if not is_north and ny < MID_LINE:
                        continue  # Süd-Insel => nicht nach Norden!

                    # 1) Noch Water?
                    # 2) Nicht blocked?
                    # 3) Chance erfüllt?
                    if (self.map[ny][nx].base == "Ocean" 
                        and not self.blocked[ny][nx]
                        and random.random() < chance):
                        
                        self.map[ny][nx].base = base_tile  # Nutzt Biom-abhängige Basis
                        created_land.append((nx, ny))
                        stack.append((nx, ny))

        return created_land

    def _mark_blocked_area(self, land_tiles, distance=6):
        """
        Markiert alle Tiles im Umkreis von `distance` um land_tiles herum
        als True in self.blocked, damit dort keine neue Insel entstehen kann.
        """
        queue = deque()
        
        # Multi-Source: alle Land-Tiles kommen mit dist=0 in die Queue
        for (lx, ly) in land_tiles:
            queue.append((lx, ly, 0))
            self.blocked[ly][lx] = True  # Land selbst ist selbstverständlich geblockt
        
        while queue:
            cx, cy, dist = queue.popleft()
            if dist >= distance:
                continue

            for nx, ny in [(cx-1, cy), (cx+1, cy), (cx, cy-1), (cx, cy+1)]:
                if 0 <= nx < self.width and 0 <= ny < self.height:
                    if not self.blocked[ny][nx]:
                        # Markieren
                        self.blocked[ny][nx] = True
                        queue.append((nx, ny, dist+1))

    def _remove_land_spikes(self, min_neighbors=2, iterations=5):
        """
        Entfernt alle 'Landspitzen' (einzelne oder schlecht verbundene Land-Tiles).
        - `"Grass"`-Spitzen werden entfernt, wenn sie zu wenige Nachbarn haben.
        - `"South_Sand"`-Spitzen werden ebenfalls entfernt, aber unabhängig von Gras.
        - Stellt sicher, dass Gras-Inseln nicht in Wüsten übergehen und umgekehrt.
        """
        for _ in range(iterations):
            changed = False
            
            # Kopie der aktuellen Map, um Veränderungen erst am Ende zu übernehmen
            new_map = [[tile.base for tile in row] for row in self.map]
            
            for y in range(1, self.height - 1):
                for x in range(1, self.width - 1):
                    current_tile = self.map[y][x].base
                    
                    # Prüfe nur Land-Tiles ("Grass" oder "South_Sand")
                    if current_tile in ["Grass", "South_Sand"]:
                        neighbors_same_biome = 0
                        
                        # Zähle Nachbarn des **gleichen Bioms**
                        for nx, ny in [(x, y-1), (x, y+1), (x-1, y), (x+1, y)]:
                            if 0 <= nx < self.width and 0 <= ny < self.height:
                                if self.map[ny][nx].base == current_tile:  # Gleicher Biom-Typ?
                                    neighbors_same_biome += 1
                        
                        # Weniger als `min_neighbors` Nachbarn? → Wird zu Wasser
                        if neighbors_same_biome < min_neighbors:
                            new_map[y][x] = "Ocean"
                            changed = True
            
            # Übernehme die Änderungen aus new_map
            for y in range(self.height):
                for x in range(self.width):
                    self.map[y][x].base = new_map[y][x]
            
            # Falls keine Änderungen mehr nötig sind, abbrechen
            if not changed:
                break

    def _ensure_minimum_islands(self):
        """
        Überprüft, ob mindestens eine Insel pro Himmelsrichtung existiert.
        Falls nicht, wird eine neue Insel erzwungen.
        """
        MID_LINE = self.height // 2
        has_north_island = False
        has_south_island = False

        # **Prüfe bestehende Inseln**
        for y in range(self.height):
            for x in range(self.width):
                if self.map[y][x].base == "Grass":
                    has_north_island = has_north_island or (y < MID_LINE)
                if self.map[y][x].base == "South_Sand":
                    has_south_island = has_south_island or (y >= MID_LINE)

        # **Falls keine Nordinsel existiert, erstelle eine**
        if not has_north_island:
            print("⚠️ Keine Nordinsel gefunden – Erzeuge eine neue!")
            self._force_create_island(north=True)

        # **Falls keine Südinsel existiert, erstelle eine**
        if not has_south_island:
            print("⚠️ Keine Südinsel gefunden – Erzeuge eine neue!")
            self._force_create_island(north=False)

    def _force_create_island(self, north=True):
        """
        Erstellt eine garantierte Insel, falls keine in der Region existiert.
        - `north=True` → Erzeugt eine Nordinsel ("Grass").
        - `north=False` → Erzeugt eine Südinsel ("South_Sand").
        """
        MID_LINE = self.height // 2
        MIN_ISLAND_SIZE = 50
        LAND_EXPANSION_CHANCE = 0.50  # Höhere Chance für schnellere Expansion

        # **Bestimme Startbereich**
        if north:
            y_range = (5, MID_LINE - 5)  # Nordhälfte
            base_tile = "Grass"
        else:
            y_range = (MID_LINE + 5, self.height - 5)  # Südhälfte
            base_tile = "South_Sand"

        # **Finde einen zufälligen Seed-Punkt in der Region**
        for _ in range(1000):  # Max. 1000 Versuche
            sx = random.randint(10, self.width - 10)
            sy = random.randint(*y_range)

            if self.map[sy][sx].base == "Ocean":
                break
        else:
            print("❌ Konnte keine passende Startposition für erzwungene Insel finden!")
            return

        # **Insel starten**
        self.map[sy][sx].base = base_tile
        land_tiles = self._expand_island((sx, sy), LAND_EXPANSION_CHANCE, margin=8, base_tile=base_tile)

        # **Falls zu klein, weite die Insel aus**
        total_landmass = self._collect_landmass(sx, sy)
        if len(total_landmass) < MIN_ISLAND_SIZE:
            print(f"🛠️ Erweiterung der erzwungenen Insel (aktuell: {len(total_landmass)} Tiles)...")
            for _ in range(5):  # 5 zusätzliche Expansionsversuche
                land_tiles.extend(self._expand_island((sx, sy), LAND_EXPANSION_CHANCE + 0.1, margin=6, base_tile=base_tile))
                total_landmass = self._collect_landmass(sx, sy)
                if len(total_landmass) >= MIN_ISLAND_SIZE:
                    break

        # **Erfolgreiche Inselmarkierung**
        self._mark_blocked_area(total_landmass, distance=10)
        print(f"✅ Erfolgreich erzwungene {base_tile}-Insel mit {len(total_landmass)} Tiles generiert!")

    # ----------------------------------------------------------------
    # (2) Eingeschlossenes Wasser => Land
    # ----------------------------------------------------------------
    def _fill_enclosed_water(self):
        """
        Findet "eingeschlossenes Wasser" und wandelt es in Land um.
        Sorgt dafür, dass der Rand nicht verändert wird.
        Biome bleiben getrennt: 
        - Nördliche Inseln (oben) -> Grass
        - Südliche Inseln (unten) -> South_Sand
        """
        visited = [[False] * self.width for _ in range(self.height)]
        queue = deque()

        # Rand als "sicheres Wasser" markieren
        for x in range(self.width):
            if self.map[0][x].base == "Ocean":
                queue.append((x, 0))
            if self.map[self.height-1][x].base == "Ocean":
                queue.append((x, self.height-1))

        for y in range(self.height):
            if self.map[y][0].base == "Ocean":
                queue.append((0, y))
            if self.map[y][self.width-1].base == "Ocean":
                queue.append((self.width-1, y))

        # BFS vom Rand, um echtes Wasser zu markieren
        while queue:
            cx, cy = queue.popleft()
            if not (0 <= cx < self.width and 0 <= cy < self.height):
                continue
            if visited[cy][cx]:
                continue
            if self.map[cy][cx].base == "Ocean":
                visited[cy][cx] = True
                for nx, ny in [(cx, cy-1), (cx, cy+1), (cx-1, cy), (cx+1, cy)]:
                    if 0 <= nx < self.width and 0 <= ny < self.height:
                        if not visited[ny][nx] and self.map[ny][nx].base == "Ocean":
                            queue.append((nx, ny))

        # **Ersetze eingeschlossenes Wasser durch das passende Biom**
        MID_LINE = self.height // 2

        for y in range(2, self.height - 2):  # Rand bleibt unangetastet
            for x in range(2, self.width - 2):
                if self.map[y][x].base == "Ocean" and not visited[y][x]:
                    # **Obere Hälfte = Grass, Untere Hälfte = South_Sand**
                    self.map[y][x].base = "Grass" if y < MID_LINE else "South_Sand"


    # ----------------------------------------------------------------
    # (3) Zu kleine Inseln entfernen
    # ----------------------------------------------------------------
    def _remove_small_islands(self, threshold=6):
        """
        Entfernt alle Inseln (zusammenhängende Landmassen) < threshold Tiles.
        Trennung von Biomen:
        - Kleine Gras-Inseln (nördlich) werden entfernt
        - Kleine Wüsten-Inseln (südlich) werden ebenfalls entfernt
        """
        visited = [[False] * self.width for _ in range(self.height)]

        for y in range(self.height):
            for x in range(self.width):
                if not visited[y][x] and (self.map[y][x].base == "Grass" or self.map[y][x].base == "South_Sand"):
                    chunk = self._collect_landmass(x, y)
                    for (cx, cy) in chunk:
                        visited[cy][cx] = True
                    if len(chunk) < threshold:
                        for (cx, cy) in chunk:
                            self.map[cy][cx].base = "Ocean"

    def _collect_landmass(self, sx, sy):
        """
        BFS: Liefert alle Land-Tiles, die mit (sx, sy) verbunden sind.
        Jetzt mit Unterstützung für **beide Biome**.
        """
        biome_type = self.map[sy][sx].base
        if biome_type not in ["Grass", "South_Sand"]:
            return []

        visited = set()
        visited.add((sx, sy))
        queue = deque([(sx, sy)])
        land_tiles = []

        while queue:
            cx, cy = queue.popleft()
            for nx, ny in [(cx, cy-1), (cx, cy+1), (cx-1, cy), (cx+1, cy)]:
                if 0 <= nx < self.width and 0 <= ny < self.height:
                    if (nx, ny) not in visited and self.map[ny][nx].base == biome_type:
                        visited.add((nx, ny))
                        queue.append((nx, ny))
                        land_tiles.append((nx, ny))

        return land_tiles

    # ----------------------------------------------------------------
    # (4) Smoothing
    # ----------------------------------------------------------------
    def _smooth_islands(self, iterations=2, land_threshold=3):
        """
        Jeder Durchlauf:
        - Ein Tile wird zu Land, wenn >= land_threshold Nachbarn (N/E/S/W) Land sind.
        - Sonst wird es zu Wasser. => Weniger Zacken / Landzungen.
        - Biome bleiben sauber getrennt!
        """
        for _ in range(iterations):
            old_map = [[self.map[y][x].base for x in range(self.width)] for y in range(self.height)]

            for y in range(1, self.height - 1):
                for x in range(1, self.width - 1):
                    current_tile = old_map[y][x]

                    # **Bestimme das Biom anhand der Trennlinie**
                    MID_LINE = self.height // 2
                    is_north = y < MID_LINE
                    land_type = "Grass" if is_north else "South_Sand"

                    # Zähle benachbarte Land-Tiles des passenden Bioms
                    neighbors_land = 0
                    if old_map[y-1][x] == land_type: neighbors_land += 1
                    if old_map[y+1][x] == land_type: neighbors_land += 1
                    if old_map[y][x-1] == land_type: neighbors_land += 1
                    if old_map[y][x+1] == land_type: neighbors_land += 1

                    # Setze das Tile je nach Nachbar-Anzahl
                    if neighbors_land >= land_threshold:
                        self.map[y][x].base = land_type  # Passendes Biom verwenden
                    else:
                        self.map[y][x].base = "Ocean"  # Alles andere bleibt Wasser


    def _create_water_border(self):
        """ Erstellt eine 4-6 Tiles breite Wasserzone um jede Insel herum. """
        for y in range(4, self.height - 4):
            for x in range(4, self.width - 4):
                if self.map[y][x].base == "Grass":
                    for dy in range(-3, 4):
                        for dx in range(-3, 4):
                            nx, ny = x + dx, y + dy
                            if 0 <= nx < self.width and 0 <= ny < self.height:
                                if self.map[ny][nx].base == "Ocean":
                                    self.map[ny][nx].base = "Water"
                elif self.map[y][x].base == "South_Sand":
                    for dy in range(-3, 4):
                        for dx in range(-3, 4):
                            nx, ny = x + dx, y + dy
                            if 0 <= nx < self.width and 0 <= ny < self.height:
                                if self.map[ny][nx].base == "Ocean":
                                    self.map[ny][nx].base = "Water"

    # ----------------------------------------------------------------
    # (5) Coastlines
    # ----------------------------------------------------------------
    def _apply_coastlines(self):
        """
        Einfache Reihenfolge:
         - Ecken (N+E, N+W, S+E, S+W)
         - Seiten (N, E, S, W)
         - Sonst diagonal, falls water_count=0 und diagonal=True
        """
        for y in range(1, self.height - 1):
            for x in range(1, self.width - 1):
                if self.map[y][x].base == "Grass":
                    n = (self.map[y-1][x].base == "Ocean")
                    e = (self.map[y][x+1].base == "Ocean")
                    s = (self.map[y+1][x].base == "Ocean")
                    w = (self.map[y][x-1].base == "Ocean")
                    ne = (self.map[y-1][x+1].base == "Ocean")
                    nw = (self.map[y-1][x-1].base == "Ocean")
                    se = (self.map[y+1][x+1].base == "Ocean")
                    sw = (self.map[y+1][x-1].base == "Ocean")

                    water_count = sum([n,e,s,w])

                    if water_count >= 1:
                        # Ecken
                        if n and w:
                            self.map[y][x].base = "Coast_Top_Left"
                        elif n and e:
                            self.map[y][x].base = "Coast_Top_Right"
                        elif s and w:
                            self.map[y][x].base = "Coast_Bottom_Left"
                        elif s and e:
                            self.map[y][x].base = "Coast_Bottom_Right"
                        # Seiten
                        elif n:
                            self.map[y][x].base = "Coast_Top_Middle"
                        elif s:
                            self.map[y][x].base = "Coast_Bottom_Middle"
                        elif e:
                            self.map[y][x].base = "Coast_Middle_Right"
                        elif w:
                            self.map[y][x].base = "Coast_Middle_Left"
                        self.map[y][x].set_navigation_mask() 
                    else:
                        # Wasser_Count=0 => N,E,S,W sind alles Land
                        # Wir prüfen nun, ob GENAU EINE diagonale Richtung Wasser ist
                        diagonals = (ne, nw, se, sw)  # True/False pro Diagonal
                        count_diags = sum(diagonals)

                        if count_diags == 1:
                            # Dann bestimmen wir, WELCHE Diagonale True ist
                            ne_water, nw_water, se_water, sw_water = diagonals
                            if ne_water:
                                self.map[y][x].base = "Coast_Top_Right_Curve"
                            elif nw_water:
                                self.map[y][x].base = "Coast_Top_Left_Curve"
                            elif se_water:
                                self.map[y][x].base = "Coast_Bottom_Right_Curve"
                            elif sw_water:
                                self.map[y][x].base = "Coast_Bottom_Left_Curve"
                            self.map[y][x].set_navigation_mask() 
                        # Sonst (z.B. 2 diagonalen = Water oder 0) bleibt Grass
                            # sonst => bleibt Grass

    def _apply_south_coastlines(self):
        """
        Einfache Reihenfolge:
         - Ecken (N+E, N+W, S+E, S+W)
         - Seiten (N, E, S, W)
         - Sonst diagonal, falls water_count=0 und diagonal=True
        """
        for y in range(1, self.height - 1):
            for x in range(1, self.width - 1):
                if self.map[y][x].base == "South_Sand":
                    n = (self.map[y-1][x].base == "Ocean")
                    e = (self.map[y][x+1].base == "Ocean")
                    s = (self.map[y+1][x].base == "Ocean")
                    w = (self.map[y][x-1].base == "Ocean")
                    ne = (self.map[y-1][x+1].base == "Ocean")
                    nw = (self.map[y-1][x-1].base == "Ocean")
                    se = (self.map[y+1][x+1].base == "Ocean")
                    sw = (self.map[y+1][x-1].base == "Ocean")

                    water_count = sum([n,e,s,w])

                    if water_count >= 1:
                        # Ecken
                        if n and w:
                            self.map[y][x].base = "Coast_South_Top_Left"
                        elif n and e:
                            self.map[y][x].base = "Coast_South_Top_Right"
                        elif s and w:
                            self.map[y][x].base = "Coast_South_Bottom_Left"
                        elif s and e:
                            self.map[y][x].base = "Coast_South_Bottom_Right"
                        # Seiten
                        elif n:
                            self.map[y][x].base = "Coast_South_Top_Middle"
                        elif s:
                            self.map[y][x].base = "Coast_South_Bottom_Middle"
                        elif e:
                            self.map[y][x].base = "Coast_South_Middle_Right"
                        elif w:
                            self.map[y][x].base = "Coast_South_Middle_Left"
                        self.map[y][x].set_navigation_mask() 
                    else:
                        # Wasser_Count=0 => N,E,S,W sind alles Land
                        # Wir prüfen nun, ob GENAU EINE diagonale Richtung Wasser ist
                        diagonals = (ne, nw, se, sw)  # True/False pro Diagonal
                        count_diags = sum(diagonals)

                        if count_diags == 1:
                            # Dann bestimmen wir, WELCHE Diagonale True ist
                            ne_water, nw_water, se_water, sw_water = diagonals
                            if ne_water:
                                self.map[y][x].base = "Coast_South_Top_Right_Curve"
                            elif nw_water:
                                self.map[y][x].base = "Coast_South_Top_Left_Curve"
                            elif se_water:
                                self.map[y][x].base = "Coast_South_Bottom_Right_Curve"
                            elif sw_water:
                                self.map[y][x].base = "Coast_South_Bottom_Left_Curve"
                            self.map[y][x].set_navigation_mask() 
                        # Sonst (z.B. 2 diagonalen = Water oder 0) bleibt Grass
                            # sonst => bleibt Grass

    def _apply_ocean_transitions(self):
        """ Erstellt Übergangstexturen zwischen Wasser und Ozean und entfernt Ocean_XXX_XXX an den Rändern. """
        for y in range(1, self.height - 1):
            for x in range(1, self.width - 1):
                if self.map[y][x].base == "Water":
                    neighbors = {
                        "N": self.map[y - 1][x].base == "Ocean",
                        "S": self.map[y + 1][x].base == "Ocean",
                        "E": self.map[y][x + 1].base == "Ocean",
                        "W": self.map[y][x - 1].base == "Ocean",
                        "NE": self.map[y - 1][x + 1].base == "Ocean",
                        "NW": self.map[y - 1][x - 1].base == "Ocean",
                        "SE": self.map[y + 1][x + 1].base == "Ocean",
                        "SW": self.map[y + 1][x - 1].base == "Ocean",
                    }

                    # Stelle sicher, dass Ocean_XXX_XXX nicht an den Rändern der Karte erscheint
                    if x <= 1 or x >= self.width - 2 or y <= 1 or y >= self.height - 2:
                        continue  # Skippe Ocean_XXX_XXX Platzierung am Rand

                    # Horizontale und vertikale Übergänge
                    if neighbors["N"]:
                        self.map[y][x].base = "Ocean_Top_Middle"
                    if neighbors["S"]:
                        self.map[y][x].base = "Ocean_Bottom_Middle"
                    if neighbors["E"]:
                        self.map[y][x].base = "Ocean_Middle_Right"
                    if neighbors["W"]:
                        self.map[y][x].base = "Ocean_Middle_Left"

                    # Diagonale Übergänge (Kanten)
                    if neighbors["N"] and neighbors["W"]:
                        self.map[y][x].base = "Ocean_Top_Left"
                    if neighbors["N"] and neighbors["E"]:
                        self.map[y][x].base = "Ocean_Top_Right"
                    if neighbors["S"] and neighbors["W"]:
                        self.map[y][x].base = "Ocean_Bottom_Left"
                    if neighbors["S"] and neighbors["E"]:
                        self.map[y][x].base = "Ocean_Bottom_Right"

                    # Innere Diagonale Übergänge (Ecken)
                    if neighbors["NE"] and not (neighbors["N"] or neighbors["E"]):
                        self.map[y][x].base = "Ocean_Inner_Top_Right"
                    if neighbors["NW"] and not (neighbors["N"] or neighbors["W"]):
                        self.map[y][x].base = "Ocean_Inner_Top_Left"
                    if neighbors["SE"] and not (neighbors["S"] or neighbors["E"]):
                        self.map[y][x].base = "Ocean_Inner_Bottom_Right"
                    if neighbors["SW"] and not (neighbors["S"] or neighbors["W"]):
                        self.map[y][x].base = "Ocean_Inner_Bottom_Left"

    # ----------------------------------------------------------------
    # (6) Wasseranimation
    # ----------------------------------------------------------------
    def _add_ocean_animation(self, chance=0.03):
        """
        Fügt eine Animation zu bestimmten Ozean-Tiles hinzu, aber NICHT auf Ocean_2, Ocean_3, Ocean_4, Ocean_5.
        """
        for y in range(1, self.height - 1):
            for x in range(1, self.width - 1):
                if self.map[y][x].base.startswith("Ocean"):  # Nur Standard-Ocean-Tile bekommt Animation
                    if random.random() < chance:
                        self.map[y][x].set_ocean_animation(random.randint(0, 23))

    # ----------------------------------------------------------------
    # (Optional) Bäume & Berge
    # ----------------------------------------------------------------
    def _generate_forest_and_mountains(self):
        """
        Erstellt Wälder und Gebirge auf der Karte.
        - Wälder (Forest_Pines) basieren auf `tree_chance`
        - Gebirge (Mountains) werden in Clustern von 4-6 Tiles generiert.
        - 10% der Inseln haben KEINE Mountains.
        """
        visited = set()  # Merkt sich bereits platzierte Gebirge
        island_mountain_skip = {}  # Speichert, ob eine Insel Mountains haben darf

        # Iteriere über alle Landmassen (Inseln)
        for y in range(1, self.height - 1):
            for x in range(1, self.width - 1):
                if self.map[y][x].base.startswith("Grass"):
                    island_id = self.get_island_id(x, y)

                    # Falls Insel noch nicht bewertet wurde, entscheide zufällig, ob sie Mountains haben darf
                    if island_id not in island_mountain_skip:
                        island_mountain_skip[island_id] = random.random() > 0.10  # 90% Chance für Mountains

                    r = random.random()

                    # 🌲 Wälder (normale Baum-Generierung)
                    if r < self.tree_chance:
                        self._generate_forest_cluster(x, y, visited)

                    # ⛰️ Gebirge nur, wenn die Insel Mountains haben darf
                    elif r < (self.tree_chance + self.mountain_chance) and island_mountain_skip[island_id]:
                        if (x, y) not in visited:  # Stelle ist noch nicht belegt
                            self._generate_mountain_cluster(x, y, visited)
                elif self.map[y][x].base.startswith("South_Sand"):
                    island_id = self.get_island_id(x, y)
                    r = random.random()
                    if r < (self.mountain_chance):
                        if (x, y) not in visited:  # Stelle ist noch nicht belegt
                            self._generate_mountain_cluster(x, y, visited)
                    # 🌵 Sand-Variationen hinzufügen
                    self._generate_sand_variations(x, y)
                    self._generate_cactus(x, y)

    def _generate_sand_variations(self, x, y):
        """
        Erstellt zufällige Sand-Variationen auf Wüsteninseln.
        - South_Sand_1 bis South_Sand_5 werden zufällig verteilt.
        """
        sand_variants = ["South_Sand_2", "South_Sand_3", "South_Sand_4", "South_Sand_5"]

        if self.map[y][x].base.startswith("South_Sand"):
            self.map[y][x].overlay = random.choice(sand_variants)  # Wähle eine zufällige Sand-Variante               

    def _generate_cactus(self, x, y):
        """
        Erstellt zufällige Cactus-Variationen auf Wüsteninseln.
        - Cactus_1 bis Cactus_9 werden zufällig verteilt.
        """
        cactus_variants = ["Cactus_1", "Cactus_2", "Cactus_3", "Cactus_4", "Cactus_5", "Cactus_6", "Cactus_7", "Cactus_8", "Cactus_9"]

        if self.map[y][x].base.startswith("South_Sand"):
            if random.random() < 0.08:
                self.map[y][x].overlay = random.choice(cactus_variants)  # Wähle eine zufällige Sand-Variante 

    def _generate_forest_cluster(self, start_x, start_y, visited, min_size=2, max_size=4):
        """
        Erstellt einen dynamischen Wald mit mehreren Dichte-Stufen:
        - `x4` dichter Wald (Mittelpunkt)
        - `x3` mitteldichter Wald (um x4)
        - `x2` lockerer Wald (um x3)
        - `x1` vereinzelt verstreute Bäume (um x2)
        """
        if self.map[start_y][start_x].base != "Grass":
            return  # Nur auf Grass generieren

        stack = [(start_x, start_y)]
        cluster_size = random.randint(min_size, max_size)
        created_forest = set()

        # **Schritt 1: Erstelle den dichten Kern (`x4`)**
        while stack and len(created_forest) < cluster_size:
            cx, cy = stack.pop()

            if (cx, cy) in visited or self.map[cy][cx].base != "Grass":
                continue  # Schon belegt oder kein Grass

            self.map[cy][cx].overlay = "Forest_Pines_x4"
            visited.add((cx, cy))
            created_forest.add((cx, cy))

            # Nachbarn sammeln
            neighbors = [(cx+1, cy), (cx-1, cy), (cx, cy+1), (cx, cy-1)]
            random.shuffle(neighbors)
            stack.extend(neighbors)

        # **Schritt 2: Erstelle mitteldichten Wald (`x3`) um `x4`**
        mid_layer = set()
        for x, y in created_forest:
            for nx, ny in [(x+1, y), (x-1, y), (x, y+1), (x, y-1)]:
                if (nx, ny) not in created_forest and (nx, ny) not in visited and self._is_valid_forest_tile(nx, ny):
                    if random.random() < 0.7:
                        self.map[ny][nx].overlay = "Forest_Pines_x3"
                        visited.add((nx, ny))
                        mid_layer.add((nx, ny))

        # **Schritt 3: Erstelle leichten Wald (`x2`) um `x3`**
        outer_layer = set()
        for x, y in mid_layer:
            for nx, ny in [(x+1, y), (x-1, y), (x, y+1), (x, y-1)]:
                if (nx, ny) not in mid_layer and (nx, ny) not in created_forest and (nx, ny) not in visited and self._is_valid_forest_tile(nx, ny):
                    if random.random() < 0.5:
                        self.map[ny][nx].overlay = "Forest_Pines_x2"
                        visited.add((nx, ny))
                        outer_layer.add((nx, ny))

        # **Schritt 4: Vereinzelte Bäume (`x1`) um `x2`**
        for x, y in outer_layer:
            for nx, ny in [(x+1, y), (x-1, y), (x, y+1), (x, y-1)]:
                if (nx, ny) not in outer_layer and (nx, ny) not in mid_layer and (nx, ny) not in created_forest and (nx, ny) not in visited and self._is_valid_forest_tile(nx, ny):
                    if random.random() < 0.2:  # 50% Chance für ein einzelnes `x1`
                        if random.random() < 0.5:
                            self.map[ny][nx].overlay = "Forest_Pines_x1_1"
                            visited.add((nx, ny))
                        else:
                            self.map[ny][nx].overlay = "Forest_Pines_x1_2"
                            visited.add((nx, ny))

    def _is_valid_forest_tile(self, x, y):
        """Prüft, ob ein Tile für einen Baum geeignet ist."""
        return 1 <= x < self.width - 1 and 1 <= y < self.height - 1 and self.map[y][x].base == "Grass"

    def _generate_mountain_cluster(self, start_x, start_y, visited, min_size=2, max_size=6, retries=10):
        """
        Erstellt einen zusammenhängenden Gebirgs-Cluster an der Position (start_x, start_y).
        - Clustergröße: 2-6 Tiles auf Grass, 10% größere Cluster auf South_Sand.
        - Berge werden **nicht** über Biom-Grenzen hinweg ausgedehnt.
        - Falls keine Expansion möglich ist, wird **bis zu 10-mal eine neue Startposition gesucht**.
        """
        base_biome = self.map[start_y][start_x].base

        # Berge können nur auf "Grass" oder "South_Sand" generiert werden
        if base_biome not in ["Grass", "South_Sand"]:
            return  

        # 10% größere Cluster für Wüstenbiome
        size_multiplier = 1.0 if base_biome == "South_Sand" else 1.0
        cluster_size = max(2, int(random.randint(min_size, max_size) * size_multiplier))

        # Mehrere Versuche, eine gute Position zu finden
        for _ in range(retries):
            if self.map[start_y][start_x].base == base_biome and (start_x, start_y) not in visited:
                break  # Gültige Startposition gefunden
            start_x, start_y = random.randint(1, self.width - 2), random.randint(1, self.height - 2)

        stack = [(start_x, start_y)]
        created_mountains = []

        while stack and len(created_mountains) < cluster_size:
            cx, cy = stack.pop()

            # Prüfen, ob das Tile bereits genutzt wurde oder nicht im gleichen Biom ist
            if (cx, cy) in visited or self.map[cy][cx].base != base_biome:
                continue  

            self.map[cy][cx].overlay = "Mountains"
            visited.add((cx, cy))
            created_mountains.append((cx, cy))

            # Nachbarn prüfen und zufällig erweitern
            neighbors = [(cx+1, cy), (cx-1, cy), (cx, cy+1), (cx, cy-1)]
            random.shuffle(neighbors)  

            for nx, ny in neighbors:
                if 1 <= nx < self.width - 1 and 1 <= ny < self.height - 1:
                    if (nx, ny) not in visited and self.map[ny][nx].base == base_biome:
                        stack.append((nx, ny))

        # Falls kein Berg generiert wurde, erzwungene Platzierung an der Startposition
        if not created_mountains:
            self.map[start_y][start_x].overlay = "Mountains"
            visited.add((start_x, start_y))

    def _finalize_ocean_border(self, border_margin=4):
        """
        Setzt den Rand der Karte in einer Breite von `border_margin` erneut auf reinen "Ocean",
        um Fehler bei Ocean_XXX_XXX Tiles zu vermeiden.
        """
        for y in range(self.height):
            for x in range(self.width):
                if x < border_margin or x >= self.width - border_margin or y < border_margin or y >= self.height - border_margin:
                    self.map[y][x].base = "Ocean"  # Hard Reset auf reinen Ozean

    def find_bottom_right_edge(self):
        """
        Bestimmt die äußerste rechte untere Kante der generierten Karte.

        Returns:
            (int, int): x- und y-Koordinaten des rechten unteren Kanten-Tiles.
        """
        for y in range(self.height - 1, -1, -1):  # Von unten nach oben
            for x in range(self.width - 1, -1, -1):  # Von rechts nach links
                if self.map[y][x].base != "Ocean":  # Land oder Wasser gefunden
                    return (x, y)

        # Falls nur Ozean existiert, nehmen wir die Karte selbst als Grenze
        return (self.width - 1, self.height - 1)
    
    def get_island_id(self, x, y):
        """Findet die Insel-ID für ein bestimmtes Tile, speichert Ergebnisse im Cache."""
        if not (0 <= x < self.width and 0 <= y < self.height):
            return None

        # Falls die Insel-ID bereits im Cache ist, gib sie sofort zurück
        if (x, y) in self.island_cache:
            return self.island_cache[(x, y)]

        # BFS (Breadth-First Search) zur Bestimmung der zusammenhängenden Insel
        visited = set()
        queue = [(x, y)]
        land_tiles = []

        while queue:
            cx, cy = queue.pop(0)
            if (cx, cy) in visited or not (0 <= cx < self.width and 0 <= cy < self.height):
                continue
            if not self.map[cy][cx].base.startswith("Grass") and not self.map[cy][cx].base.startswith("Coast"):
                continue  # Kein Land oder Küste = Keine Insel

            visited.add((cx, cy))
            land_tiles.append((cx, cy))

            # Alle benachbarten Tiles hinzufügen
            neighbors = [(cx+1, cy), (cx-1, cy), (cx, cy+1), (cx, cy-1)]
            queue.extend(neighbors)

        if not land_tiles:
            return None  # 🚫 **Kein Land gefunden**

        # Erzeuge eine eindeutige Insel-ID als Hash der enthaltenen Tiles
        island_id = hash(frozenset(land_tiles))

        # **Speichere ALLE Tiles der Insel im Cache**
        for tile in land_tiles:
            self.island_cache[tile] = island_id

        return island_id