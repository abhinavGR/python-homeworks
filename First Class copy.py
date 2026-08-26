import os
import random
import subprocess
import tkinter as tk

LEVELS = {
    "easy": [
        "############################",
        "#........c....p....c.......#",
        "#.####.#####.##.#####.####.#",
        "#....#..............#....#",
        "#.##.#.##.########.##.#.##.#",
        "#....#....#......#....#....#",
        "#.#.##.##.#.####.#.##.##.#.#",
        "#....#....#......#....#....#",
        "#.####.####.####.####.####.#",
        "#c..............c........c#",
        "#.#.##.####.##.####.##.#.##",
        "#....#....#....#....#....#",
        "#.#.##.##.#.####.#.##.##.#.#",
        "#....#....#......#....#....#",
        "#.####.####.####.####.####.#",
        "#...........c....c........#",
        "#.####.#####.##.#####.####.#",
        "#....#..............#....#",
        "#....##....##....##....##..#",
        "#........c....p....c......#",
        "############################",
    ],
    "medium": [
        "############################",
        "#c....#......##......#....c#",
        "#.####.#####.##.#####.####.#",
        "#....#..............#....#",
        "#.##.#.##.########.##.#.##.#",
        "#....##....##....##......#",
        "######.#####p##p#####.######",
        "#....#.##      ##.#....#   ",
        "#....#.## #### ##.#....#   ",
        "######.## #    # ##.######",
        "      .   #    #   .      ",
        "######.## #    # ##.######",
        "#....#.## #### ##.#....#   ",
        "#....#.##      ##.#....#   ",
        "######.## #### ##.######",
        "#............##............#",
        "#.####.#####.##.#####.####.#",
        "#...##..............##...#",
        "###.##.##.########.##.##.###",
        "#......##....##....##......#",
        "#.##########.##.##########.#",
        "#..........................#",
        "############################",
    ],
    "hard": [
        "############################",
        "#c..#....##....p....##....#",
        "#.##.#.####.##.####.##.#.##.#",
        "#....#....#....#....#....#.#",
        "#.####.##.#.####.#.##.####.#",
        "#....#....#....#....#....#.#",
        "#.#.####.####.##.####.####.#",
        "#.#....#....#..#....#....#.#",
        "#.###.##.##.##.##.##.##.###.#",
        "#....#....#....#....#....#.#",
        "#.#.##.####.##.####.##.##.#.#",
        "#....#......#..#......#....#",
        "#.####.####.#.####.####.####",
        "#c........#....#....#......#",
        "#.##.##.##.####.##.##.##.##.#",
        "#....#....#....#....#....#.#",
        "#.#.####.##.##.##.####.##.#.#",
        "#....#....#....#....#....#.#",
        "#.####.##.##.####.##.##.####",
        "#....#........c........#....#",
        "############################",
    ],
}


def normalize_level(level_map):
    max_width = max(len(row) for row in level_map)
    return [row.ljust(max_width, " ") for row in level_map]


LEVELS = {name: normalize_level(level_map) for name, level_map in LEVELS.items()}

BASE_CELL_SIZE = 22
BASE_WIDTH = 30 * BASE_CELL_SIZE
BASE_HEIGHT = 24 * BASE_CELL_SIZE


def play_mac_sound(filename):
    script_dir = os.path.dirname(os.path.abspath(__file__))
    full_path = os.path.join(script_dir, filename)
    if os.path.exists(full_path):
        subprocess.Popen(["afplay", full_path], stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)


class PacmanArcade:
    def __init__(self, root):
        self.root = root
        self.root.title("Pac-Man Arcade")
        self.root.geometry(f"{BASE_WIDTH}x{BASE_HEIGHT}")

        self.canvas = tk.Canvas(root, bg="black", highlightthickness=0)
        self.canvas.pack(fill="both", expand=True)

        self.paused = False
        self.game_over = False
        self.win = False
        self.mouth_open = True
        self.scale_factor = 1.0
        self.offset_x = 0
        self.offset_y = 0
        self.score = 0
        self.scared_timer = 0
        self.level_name = "easy"
        self.cols = 30
        self.rows = 24
        self.base_width = BASE_WIDTH
        self.base_height = BASE_HEIGHT
        self.started = False
        self.fullscreen = False
        self.ghost_speed = 1
        self.ghost_random = 0.08
        self.ghost_move_counter = 0
        self.game_over_timer = 0
        self.lives = 3
        self.extra_awarded = False
        self.helper = None

        self.reset_game_state()

        self.root.bind("<KeyPress>", self.handle_key)
        self.root.bind("<Configure>", self.handle_resize)

        play_mac_sound("start.wav")
        self.render_sprites()
        self.game_loop()

    def reset_game_state(self):
        self.score = 0
        self.lives = 3
        self.extra_awarded = False
        self.helper = None
        self.game_over = False
        self.win = False
        self.paused = False
        self.mouth_open = True
        self.scared_timer = 0
        self.game_over_timer = 0

        level_map = LEVELS[self.level_name]
        self.cols = len(level_map[0])
        self.rows = len(level_map)
        self.base_width = self.cols * BASE_CELL_SIZE
        self.base_height = self.rows * BASE_CELL_SIZE
        # Sync actual fullscreen state (user may have used OS fullscreen)
        try:
            current_fs = bool(self.root.attributes("-fullscreen"))
        except Exception:
            current_fs = self.fullscreen
        self.fullscreen = current_fs or self.fullscreen
        self.root.attributes("-fullscreen", self.fullscreen)
        self.ghost_speed = {"easy": 1, "medium": 1, "hard": 2}[self.level_name]
        self.ghost_random = {"easy": 0.05, "medium": 0.1, "hard": 0.18}[self.level_name]
        self.ghost_move_counter = 0
        if not self.fullscreen:
            self.root.geometry(f"{self.base_width}x{self.base_height}")

        self.grid = []
        for row_str in level_map:
            row_list = []
            for c in row_str:
                if c == "#":
                    row_list.append(1)
                elif c == ".":
                    row_list.append(2)
                elif c == "c":
                    row_list.append(3)
                elif c == "p":
                    row_list.append(4)
                else:
                    row_list.append(0)
            self.grid.append(row_list)

        pacman_spawn = self._find_center_spawn()
        self.pacman_x, self.pacman_y = pacman_spawn
        self.direction = "Left"
        self.next_direction = "Left"

        ghost_positions = [
            (1, 1),
            (self.cols - 2, 1),
            (1, self.rows - 2),
            (self.cols - 2, self.rows - 2),
        ]
        safe_ghost_positions = []
        for pos in ghost_positions:
            if pos != pacman_spawn and not self.is_wall(pos[0], pos[1]):
                safe_ghost_positions.append(pos)

        if len(safe_ghost_positions) < 4:
            safe_ghost_positions = [pos for pos in ghost_positions if not self.is_wall(pos[0], pos[1])]

        # Enforce exactly four colorful (lethal) balls and one eatable ghost for all levels
        self.ghosts = []
        used_positions = set()

        # Choose up to 4 positions for colorful balls from preferred corners first
        ball_positions = []
        for pos in safe_ghost_positions:
            if len(ball_positions) >= 4:
                break
            if pos != pacman_spawn:
                ball_positions.append(pos)

        # If not enough corner positions, scan outward for free cells
        if len(ball_positions) < 4:
            for y in range(self.rows):
                for x in range(self.cols):
                    if len(ball_positions) >= 4:
                        break
                    if (x, y) == pacman_spawn or self.is_wall(x, y):
                        continue
                    if (x, y) in ball_positions:
                        continue
                    ball_positions.append((x, y))
                if len(ball_positions) >= 4:
                    break

        colors = ["#ff0000", "#ffb8ff", "#00ffff", "#ffb852"]
        dirs = ["Right", "Left", "Right", "Left"]
        for idx, (bx, by) in enumerate(ball_positions[:4]):
            used_positions.add((bx, by))
            self.ghosts.append({
                "x": bx,
                "y": by,
                "color": colors[idx % len(colors)],
                "dir": dirs[idx % len(dirs)],
                "home": (bx, by),
                "eaten": False,
                "is_ghost": False,  # colorful balls are NOT ghosts
            })

        # Spawn a single eatable ghost at the first safe unused position
        ghost_pos = None
        for pos in safe_ghost_positions:
            if pos not in used_positions and pos != pacman_spawn:
                ghost_pos = pos
                break
        if not ghost_pos:
            for y in range(self.rows):
                for x in range(self.cols):
                    if (x, y) == pacman_spawn or self.is_wall(x, y) or (x, y) in used_positions:
                        continue
                    ghost_pos = (x, y)
                    break
                if ghost_pos:
                    break

        if ghost_pos:
            gx, gy = ghost_pos
            self.ghosts.append({
                "x": gx,
                "y": gy,
                "color": "#ffff00",
                "dir": "Left",
                "home": (gx, gy),
                "eaten": False,
                "is_ghost": True,
            })
        else:
            # fallback: one ghost at pacman spawn
            self.ghosts.append({"x": pacman_spawn[0], "y": pacman_spawn[1], "color": "#ffff00", "dir": "Left", "home": pacman_spawn, "eaten": False, "is_ghost": True})

        self.draw_maze()

    def handle_key(self, event):
        if event.keysym == "space":
            if not self.game_over and not self.win:
                self.paused = not self.paused
                self.render_sprites()
            return

        if event.keysym.lower() == "r":
            if self.started and (self.game_over or self.win):
                self.reset_game_state()
                play_mac_sound("start.wav")
            elif not self.started:
                self.started = True
                self.reset_game_state()
                play_mac_sound("start.wav")
            return

        if event.keysym in ["1", "2", "3"]:
            level_name = {"1": "easy", "2": "medium", "3": "hard"}[event.keysym]
            self.level_name = level_name
            self.started = True
            self.reset_game_state()
            play_mac_sound("start.wav")
            return

        if event.keysym.lower() == "f":
            self.fullscreen = not self.fullscreen
            self.root.attributes("-fullscreen", self.fullscreen)
            self.root.update_idletasks()
            if not self.fullscreen:
                self.root.geometry(f"{self.base_width}x{self.base_height}")
            self.draw_maze()
            return

        if event.keysym in ["Up", "Down", "Left", "Right"]:
            self.next_direction = event.keysym

    def handle_resize(self, event):
        w, h = self.root.winfo_width(), self.root.winfo_height()
        self.scale_factor = min(w / max(self.base_width, 1), h / max(self.base_height, 1))
        self.draw_maze()

    def is_wall(self, x, y):
        # Safely handle non-integer or out-of-range coordinates
        try:
            xi = int(x)
            yi = int(y)
        except Exception:
            return True
        if not (0 <= xi < self.cols and 0 <= yi < self.rows):
            return True
        try:
            return self.grid[yi][xi] == 1
        except Exception:
            return True

    def _find_center_spawn(self):
        center_x = self.cols // 2
        center_y = self.rows // 2
        for y in range(center_y - 1, center_y + 2):
            for x in range(center_x - 1, center_x + 2):
                if 0 <= x < self.cols and 0 <= y < self.rows and not self.is_wall(x, y):
                    return x, y
        return 1, 1

    def draw_maze(self):
        self.canvas.delete("all")

        cell = BASE_CELL_SIZE * self.scale_factor
        w, h = self.root.winfo_width(), self.root.winfo_height()
        # Use the current level's base dimensions so overlays stay aligned
        self.offset_x = (w - (self.base_width * self.scale_factor)) / 2
        self.offset_y = (h - (self.base_height * self.scale_factor)) / 2

        for r_idx, row in enumerate(self.grid):
            for c_idx, val in enumerate(row):
                x1 = c_idx * cell + self.offset_x
                y1 = r_idx * cell + self.offset_y

                if val == 1:
                    self.canvas.create_rectangle(
                        x1 + 2, y1 + 2, x1 + cell - 2, y1 + cell - 2,
                        outline="#2121de", width=2, fill="#2121de"
                    )
                elif val == 2:
                    r = max(2, int(3 * self.scale_factor))
                    cx, cy = x1 + cell / 2, y1 + cell / 2
                    self.canvas.create_oval(
                        cx - r, cy - r, cx + r, cy + r,
                        fill="#ffb8ae", tags=f"p_{c_idx}_{r_idx}"
                    )
                elif val == 3:
                    r = max(7, int(10 * self.scale_factor))
                    cx, cy = x1 + cell / 2, y1 + cell / 2
                    self.canvas.create_oval(
                        cx - r * 0.7, cy - r * 0.7, cx + r * 0.25, cy + r * 0.25,
                        fill="#ff1a1a", outline="#a70000", width=max(1, int(1.8 * self.scale_factor)), tags=f"p_{c_idx}_{r_idx}"
                    )
                    self.canvas.create_oval(
                        cx - r * 0.12, cy - r * 0.7, cx + r * 0.58, cy + r * 0.25,
                        fill="#ff1a1a", outline="#a70000", width=max(1, int(1.8 * self.scale_factor)), tags=f"p_{c_idx}_{r_idx}"
                    )
                    self.canvas.create_line(
                        cx - r * 0.08, cy - r * 0.85, cx + r * 0.02, cy - r * 1.25,
                        fill="#2e8b57", width=max(1, int(2 * self.scale_factor)), tags=f"p_{c_idx}_{r_idx}"
                    )
                    self.canvas.create_line(
                        cx - r * 0.34, cy - r * 0.98, cx - r * 0.12, cy - r * 1.12,
                        fill="#2e8b57", width=max(1, int(2 * self.scale_factor)), tags=f"p_{c_idx}_{r_idx}"
                    )
                elif val == 4:
                    r = max(3, int(4 * self.scale_factor))
                    cx, cy = x1 + cell / 2, y1 + cell / 2
                    self.canvas.create_oval(
                        cx - r, cy - r, cx + r, cy + r,
                        fill="#00ffff", tags=f"p_{c_idx}_{r_idx}"
                    )

    def update_pacman(self):
        dx, dy = 0, 0

        if self.next_direction == "Up":
            dy = -1
        elif self.next_direction == "Down":
            dy = 1
        elif self.next_direction == "Left":
            dx = -1
        elif self.next_direction == "Right":
            dx = 1

        if not self.is_wall(self.pacman_x + dx, self.pacman_y + dy):
            self.direction = self.next_direction
        else:
            dx, dy = 0, 0
            if self.direction == "Up":
                dy = -1
            elif self.direction == "Down":
                dy = 1
            elif self.direction == "Left":
                dx = -1
            elif self.direction == "Right":
                dx = 1

        if not self.is_wall(self.pacman_x + dx, self.pacman_y + dy):
            self.pacman_x += dx
            self.pacman_y += dy

        if not (0 <= self.pacman_x < self.cols and 0 <= self.pacman_y < self.rows):
            self.pacman_x, self.pacman_y = self._find_center_spawn()
            return

        cell_val = self.grid[self.pacman_y][self.pacman_x]
        if cell_val == 2:
            # Temporarily remove dot, award points, then respawn it after a short delay
            self.grid[self.pacman_y][self.pacman_x] = 0
            self.canvas.delete(f"p_{self.pacman_x}_{self.pacman_y}")
            self.score += 20
            play_mac_sound("munch.wav")
            # schedule dot respawn (2 seconds)
            self.root.after(2000, lambda x=self.pacman_x, y=self.pacman_y: self._respawn_dot(x, y))
        elif cell_val == 3:
            self.grid[self.pacman_y][self.pacman_x] = 0
            self.canvas.delete(f"p_{self.pacman_x}_{self.pacman_y}")
            self.score += 50
            play_mac_sound("pacman_eatfruit.wav")
        elif cell_val == 4:
            self.grid[self.pacman_y][self.pacman_x] = 0
            self.canvas.delete(f"p_{self.pacman_x}_{self.pacman_y}")
            self.score += 50
            self.scared_timer = 10 if self.level_name == "easy" else 6 if self.level_name == "medium" else 5
            play_mac_sound("pacman_eatfruit.wav")

        # Global win threshold
        if self.score >= 10000:
            self.game_over_timer = 2
            self.started = False
            self.win = True
            self.game_over = False
            self.paused = False
            self.scared_timer = 0
            self.next_direction = "Left"
            play_mac_sound("start.wav")
        # Helper Pac-Man spawns at 500 points
        if self.score >= 500 and (not self.helper or not self.helper.get("alive", False)):
            self._spawn_helper()
        # Extra life at 1600 points (one-time)
        if not self.extra_awarded and self.score >= 1600:
            self.extra_awarded = True
            self.lives += 1
            play_mac_sound("pacman_extrapac.wav")

    def _remaining_collectibles(self):
        count = 0
        for row in self.grid:
            for value in row:
                if value in (2, 3, 4):
                    count += 1
        return count

    def update_ghosts(self):
        dirs = ["Up", "Down", "Left", "Right"]
        opp = {"Up": "Down", "Down": "Up", "Left": "Right", "Right": "Left"}

        self.ghost_move_counter += 1
        if self.level_name == "easy" and self.ghost_move_counter % 2 == 1:
            if self.scared_timer > 0:
                self.scared_timer -= 1
            return

        for g in self.ghosts:
            valid = []
            for d in dirs:
                if d == opp.get(g["dir"]):
                    continue
                gx = g["x"] + (1 if d == "Right" else -1 if d == "Left" else 0)
                gy = g["y"] + (1 if d == "Down" else -1 if d == "Up" else 0)
                if not self.is_wall(gx, gy):
                    valid.append(d)

            if g.get("eaten", False):
                # Move eyes straight toward home (ignores normal pathing), one cell per update
                hx, hy = g["home"]
                if g["x"] < hx:
                    g["x"] += 1
                elif g["x"] > hx:
                    g["x"] -= 1
                if g["y"] < hy:
                    g["y"] += 1
                elif g["y"] > hy:
                    g["y"] -= 1
                if g["x"] == hx and g["y"] == hy:
                    g["eaten"] = False
                    g["dir"] = "Right"
                continue

            if not valid:
                g["dir"] = opp.get(g["dir"], "Up")
            else:
                if self.scared_timer > 0:
                    chosen = random.choice(valid)
                    g["dir"] = chosen
                else:
                    if self.level_name == "easy" and random.random() < 0.55:
                        g["dir"] = random.choice(valid)
                    else:
                        best_dir = valid[0]
                        best_dist = float("inf")
                        for d in valid:
                            nx = g["x"] + (1 if d == "Right" else -1 if d == "Left" else 0)
                            ny = g["y"] + (1 if d == "Down" else -1 if d == "Up" else 0)
                            dist = (nx - self.pacman_x) ** 2 + (ny - self.pacman_y) ** 2
                            if dist < best_dist:
                                best_dist = dist
                                best_dir = d
                        g["dir"] = random.choice(valid) if random.random() < self.ghost_random else best_dir

            if self.ghost_speed > 1:
                move_step = self.ghost_speed
            else:
                move_step = 1
            g["x"] += move_step if g["dir"] == "Right" else -move_step if g["dir"] == "Left" else 0
            g["y"] += move_step if g["dir"] == "Down" else -move_step if g["dir"] == "Up" else 0

            if g["x"] < 0:
                g["x"] = self.cols - 1
            elif g["x"] >= self.cols:
                g["x"] = 0

            if not (0 <= g["x"] < self.cols and 0 <= g["y"] < self.rows):
                g["x"], g["y"] = g["home"]
                g["dir"] = "Right"
                continue

            # Ghosts are collectible (do NOT kill the player). Colorful balls (is_ghost==False) are lethal.
            if g.get("is_ghost", False) and g["x"] == self.pacman_x and g["y"] == self.pacman_y:
                if not g.get("eaten", False):
                    g["eaten"] = True
                    self.score += 200
                    play_mac_sound("pacman_eatghost.wav")
                # eyes will move back in subsequent frames
            elif not g.get("is_ghost", False) and g["x"] == self.pacman_x and g["y"] == self.pacman_y:
                # collision with colorful ball causes death
                self.game_over_timer = 2
                self.started = False
                self.game_over = True
                self.win = False
                self.paused = False
                self.scared_timer = 0
                self.next_direction = "Left"
                play_mac_sound("death.wav")

        if self.scared_timer > 0:
            self.scared_timer -= 1

    def _get_overlay_bounds(self):
        # Center overlays inside the maze drawing area (not the full window)
        maze_w = max(1, self.base_width * self.scale_factor)
        maze_h = max(1, self.base_height * self.scale_factor)
        # max overlay size limited to maze area with some padding
        box_w = min(360, max(200, maze_w - 40))
        box_h = min(320, max(160, maze_h - 40))
        x0 = self.offset_x + (maze_w - box_w) / 2
        y0 = self.offset_y + (maze_h - box_h) / 2
        return x0, y0, x0 + box_w, y0 + box_h

    def _respawn_dot(self, x, y):
        # Safely respawn a dot if the cell is within bounds and currently empty
        try:
            if 0 <= x < self.cols and 0 <= y < self.rows and self.grid[y][x] == 0:
                self.grid[y][x] = 2
                # redraw maze so the dot appears again
                self.draw_maze()
                self.render_sprites()
        except Exception:
            pass

    def _spawn_helper(self):
        # create a helper Pac-Man that wanders and collects dots for the player
        if self.helper and self.helper.get("alive", False):
            return
        self.helper = None
        # place helper near player if possible
        hx, hy = self.pacman_x, self.pacman_y
        for dy in (0, -1, 1, -2, 2):
            for dx in (0, -1, 1, -2, 2):
                nx, ny = hx + dx, hy + dy
                if 0 <= nx < self.cols and 0 <= ny < self.rows and not self.is_wall(nx, ny):
                    self.helper = {"x": nx, "y": ny, "dir": random.choice(["Up","Down","Left","Right"]), "alive": True}
                    break
            if self.helper:
                break
        if self.helper:
            play_mac_sound("pacman_extrapac.wav")

    def _update_helper(self):
        if not self.helper or not self.helper.get("alive", False):
            return
        # simple wandering + greedy dot collection
        dirs = ["Up","Down","Left","Right"]
        best = None
        best_dist = float("inf")
        for d in dirs:
            nx = self.helper["x"] + (1 if d == "Right" else -1 if d == "Left" else 0)
            ny = self.helper["y"] + (1 if d == "Down" else -1 if d == "Up" else 0)
            if self.is_wall(nx, ny):
                continue
            # distance to nearest dot from that tile
            dist = self._dist_to_nearest_dot(nx, ny)
            if dist < best_dist:
                best_dist = dist
                best = (nx, ny, d)
        if best:
            self.helper["x"], self.helper["y"], self.helper["dir"] = best
        # collect dot if present
        hx, hy = self.helper["x"], self.helper["y"]
        if 0 <= hx < self.cols and 0 <= hy < self.rows and self.grid[hy][hx] == 2:
            self.grid[hy][hx] = 0
            self.score += 20
            play_mac_sound("munch.wav")
            # respawn dot later
            self.root.after(2000, lambda x=hx, y=hy: self._respawn_dot(x, y))

    def _dist_to_nearest_dot(self, x, y):
        best = float("inf")
        for ry in range(self.rows):
            for rx in range(self.cols):
                if self.grid[ry][rx] == 2:
                    d = abs(rx - x) + abs(ry - y)
                    if d < best:
                        best = d
        return best

    def render_sprites(self):
        self.canvas.delete("sprite")

        cell = BASE_CELL_SIZE * self.scale_factor
        px, py = self.pacman_x * cell + self.offset_x, self.pacman_y * cell + self.offset_y

        self.mouth_open = not self.mouth_open

        if self.mouth_open:
            sa = {"Right": 30, "Left": 210, "Up": 120, "Down": 300}.get(self.direction, 30)
            self.canvas.create_arc(
                px + 2, py + 2, px + cell - 2, py + cell - 2,
                fill="#ffff00", start=sa, extent=300, tags="sprite"
            )
        else:
            self.canvas.create_oval(
                px + 2, py + 2, px + cell - 2, py + cell - 2,
                fill="#ffff00", tags="sprite"
            )

        for g in self.ghosts:
            gx, gy = g["x"] * cell + self.offset_x, g["y"] * cell + self.offset_y
            if g.get("eaten", False):
                # draw disembodied eyes: two white ovals with pupils
                eye_w = max(4, int(4 * self.scale_factor))
                eye_h = max(6, int(6 * self.scale_factor))
                left_ex = gx + cell * 0.28
                right_ex = gx + cell * 0.62
                ey = gy + cell * 0.3
                self.canvas.create_oval(
                    left_ex - eye_w, ey - eye_h, left_ex + eye_w, ey + eye_h,
                    fill="#ffffff", outline="#ffffff", tags="sprite"
                )
                self.canvas.create_oval(
                    right_ex - eye_w, ey - eye_h, right_ex + eye_w, ey + eye_h,
                    fill="#ffffff", outline="#ffffff", tags="sprite"
                )
                # pupils: point toward home
                hx, hy = g["home"]
                dx = hx - g["x"]
                dy = hy - g["y"]
                pup_offset_x = 1 if dx > 0 else -1 if dx < 0 else 0
                pup_offset_y = 1 if dy > 0 else -1 if dy < 0 else 0
                pupil_r = max(2, int(2 * self.scale_factor))
                self.canvas.create_oval(
                    left_ex - pupil_r + pup_offset_x, ey - pupil_r + pup_offset_y,
                    left_ex + pupil_r + pup_offset_x, ey + pupil_r + pup_offset_y,
                    fill="#000000", tags="sprite"
                )
                self.canvas.create_oval(
                    right_ex - pupil_r + pup_offset_x, ey - pupil_r + pup_offset_y,
                    right_ex + pupil_r + pup_offset_x, ey + pupil_r + pup_offset_y,
                    fill="#000000", tags="sprite"
                )
            else:
                # If this entity is a ghost (special or bonus), draw ghost-shaped body; otherwise draw colorful circle
                if g.get("is_ghost", False) or g.get("is_bonus_ghost", False):
                    if self.scared_timer > 0 and not g.get("eaten", False):
                        fill = "#0000ff"
                    else:
                        fill = g.get("color", "#ff0000")

                    # head (half-oval)
                    self.canvas.create_arc(
                        gx + 2, gy + 2, gx + cell - 2, gy + cell - 2,
                        start=0, extent=180, style=tk.PIESLICE, fill=fill, outline=fill, tags="sprite"
                    )
                    # body rectangle under head
                    body_y0 = gy + cell * 0.25
                    body_y1 = gy + cell - 2
                    self.canvas.create_rectangle(
                        gx + 2, body_y0, gx + cell - 2, body_y1,
                        fill=fill, outline=fill, tags="sprite"
                    )
                    # scalloped bottom: carve out 3 semicircles in background color to simulate feet
                    scallop_count = 3
                    for i in range(scallop_count):
                        cx = gx + (i + 0.5) * (cell / scallop_count)
                        scallop_r = max(4, int(0.12 * cell))
                        self.canvas.create_oval(
                            cx - scallop_r, body_y1 - scallop_r, cx + scallop_r, body_y1 + scallop_r,
                            fill="black", outline="black", tags="sprite"
                        )

                    # eyes for the ghost
                    eye_w = max(4, int(3 * self.scale_factor))
                    eye_h = max(6, int(5 * self.scale_factor))
                    left_ex = gx + cell * 0.28
                    right_ex = gx + cell * 0.62
                    ey = gy + cell * 0.35
                    self.canvas.create_oval(
                        left_ex - eye_w, ey - eye_h, left_ex + eye_w, ey + eye_h,
                        fill="#ffffff", outline="#ffffff", tags="sprite"
                    )
                    self.canvas.create_oval(
                        right_ex - eye_w, ey - eye_h, right_ex + eye_w, ey + eye_h,
                        fill="#ffffff", outline="#ffffff", tags="sprite"
                    )
                    # pupils look toward pacman
                    dx = self.pacman_x - g["x"]
                    dy = self.pacman_y - g["y"]
                    pup_offset_x = 1 if dx > 0 else -1 if dx < 0 else 0
                    pup_offset_y = 1 if dy > 0 else -1 if dy < 0 else 0
                    pupil_r = max(2, int(2 * self.scale_factor))
                    self.canvas.create_oval(
                        left_ex - pupil_r + pup_offset_x, ey - pupil_r + pup_offset_y,
                        left_ex + pupil_r + pup_offset_x, ey + pupil_r + pup_offset_y,
                        fill="#000000", tags="sprite"
                    )
                    self.canvas.create_oval(
                        right_ex - pupil_r + pup_offset_x, ey - pupil_r + pup_offset_y,
                        right_ex + pupil_r + pup_offset_x, ey + pupil_r + pup_offset_y,
                        fill="#000000", tags="sprite"
                    )
                else:
                    # Non-ghost colorful balls
                    fill = g.get("color", "#ff0000")
                    self.canvas.create_oval(
                        gx + 2, gy + 2, gx + cell - 2, gy + cell - 2,
                        fill=fill, tags="sprite"
                    )

        if self.helper and self.helper.get("alive", False):
            hx = self.helper["x"] * cell + self.offset_x
            hy = self.helper["y"] * cell + self.offset_y
            self.canvas.create_arc(
                hx + 2, hy + 2, hx + cell - 2, hy + cell - 2,
                fill="#ffff00", start=30, extent=300, tags="sprite"
            )

        ts = max(12, int(16 * self.scale_factor))
        if self.started or self.game_over_timer > 0 or self.paused:
            # Responsive HUD: keep inside current level area and canvas
            maze_w = max(1, self.base_width * self.scale_factor)
            maze_h = max(1, self.base_height * self.scale_factor)
            hud_max_w = max(160, maze_w - 20)
            hud_x1 = self.offset_x + 10
            hud_x2 = hud_x1 + hud_max_w
            hud_h = 36
            # Always place HUD just inside the maze area (below top wall)
            hud_y1 = int(self.offset_y + 6)
            hud_y2 = hud_y1 + hud_h
            self.canvas.create_rectangle(
                hud_x1, hud_y1, hud_x2, hud_y2,
                fill="#000000", outline="#ffffff", width=1, tags="sprite"
            )
            self.canvas.create_text(
                hud_x1 + 15, hud_y1 + 18,
                text=f"SCORE: {self.score}", fill="white",
                font=("Courier", ts, "bold"), tags="sprite", anchor="w"
            )
            # Lives display
            self.canvas.create_text(
                hud_x1 + hud_max_w - 20, hud_y1 + 18,
                text=f"LIVES: {self.lives}", fill="#ffff00",
                font=("Courier", ts, "bold"), tags="sprite", anchor="e"
            )

        if not self.started and self.game_over_timer <= 0 and not self.game_over and not self.win:
            x0, y0, x1, y1 = self._get_overlay_bounds()
            box_w = max(1, x1 - x0)
            box_h = max(1, y1 - y0)
            # draw box
            self.canvas.create_rectangle(
                x0, y0, x1, y1,
                fill="#000000", outline="#ffffff", width=2, tags="sprite"
            )
            cx = (x0 + x1) / 2
            # compute font sizes so text fits inside box
            title_size = max(14, int(min(40, box_w / 10, box_h / 6)))
            subtitle_size = max(12, int(min(22, box_w / 20, box_h / 10)))
            option_size = max(10, int(min(20, box_w / 26, box_h / 12)))
            prompt_size = max(9, int(min(14, box_w / 30)))
            # Keep the level option layout like before, but clamp title size to fit
            # approximate character width to avoid overflow
            title_text = "PAC-MAN ARCADE"
            approx_char_width = max(6, title_size * 0.6)
            max_title_by_width = max(12, int((box_w - 30) / approx_char_width))
            if title_size > max_title_by_width:
                title_size = max_title_by_width

            # positions proportional to the original fixed offsets
            self.canvas.create_text(
                cx,
                y0 + box_h * 0.14,
                text=title_text, fill="#ffff00",
                font=("Courier", title_size, "bold"), tags="sprite"
            )
            self.canvas.create_text(
                cx,
                y0 + box_h * 0.265,
                text="CHOOSE A LEVEL", fill="white",
                font=("Courier", subtitle_size, "bold"), tags="sprite"
            )
            self.canvas.create_text(
                cx,
                y0 + box_h * 0.375,
                text="1 = EASY", fill="#00ff00",
                font=("Courier", option_size, "bold"), tags="sprite"
            )
            self.canvas.create_text(
                cx,
                y0 + box_h * 0.46875,
                text="2 = MEDIUM", fill="#ffd700",
                font=("Courier", option_size, "bold"), tags="sprite"
            )
            self.canvas.create_text(
                cx,
                y0 + box_h * 0.5625,
                text="3 = HARD", fill="#ff4d4d",
                font=("Courier", option_size, "bold"), tags="sprite"
            )
            # press prompt uses wrapping to avoid overflow
            self.canvas.create_text(
                cx,
                y0 + box_h * 0.88,
                text="PRESS 1, 2, OR 3 TO START", fill="#cccccc",
                font=("Courier", prompt_size, "bold"), width=int(box_w * 0.9), tags="sprite"
            )

        if self.game_over_timer > 0:
            x0, y0, x1, y1 = self._get_overlay_bounds()
            self.canvas.create_rectangle(
                x0, y0, x1, y1,
                fill="#000000", outline="#ffffff", width=2, tags="sprite"
            )
            cx = (x0 + x1) / 2
            box_w = max(1, x1 - x0)
            box_h = max(1, y1 - y0)
            # dynamic sizes
            title_size = max(14, int(min(40, box_w / 10, box_h / 6)))
            info_size = max(10, int(min(20, box_w / 24, box_h / 12)))
            small_size = max(9, int(min(14, box_w / 30)))

            title = "YOU WIN!" if self.win else "GAME OVER"
            title_color = "#00ff00" if self.win else "red"
            self.canvas.create_text(
                cx,
                y0 + box_h * 0.25,
                text=title, fill=title_color,
                font=("Courier", title_size, "bold"), tags="sprite"
            )
            self.canvas.create_text(
                cx,
                y0 + box_h * 0.5,
                text=f"SCORE: {self.score}", fill="white",
                font=("Courier", info_size, "bold"), tags="sprite"
            )
            self.canvas.create_text(
                cx,
                y0 + box_h * 0.7,
                text="RETURNING TO LEVEL SELECT...", fill="#cccccc",
                font=("Courier", small_size, "bold"), width=int(box_w * 0.85), tags="sprite"
            )

        if self.paused:
            self.canvas.create_text(
                self.root.winfo_width() // 2,
                self.root.winfo_height() // 2,
                text="PAUSED", fill="Yellow",
                font=("Courier", int(24 * self.scale_factor), "bold"), tags="sprite"
            )

    def game_loop(self):
        if self.game_over_timer > 0:
            self.game_over_timer -= 1 / 7.0
            if self.game_over_timer <= 0:
                self.started = False
                self.game_over_timer = 0
                self.score = 0
                self.scared_timer = 0
                self.next_direction = "Left"
                self.game_over = False
                self.win = False
                self.render_sprites()
        elif self.started and not self.game_over and not self.paused and not self.win:
            self.update_pacman()
            self.update_ghosts()
            self._update_helper()
        else:
            pass
        self.render_sprites()
        self.root.after(140, self.game_loop)


if __name__ == "__main__":
    window = tk.Tk()
    game = PacmanArcade(window)
    window.mainloop()
