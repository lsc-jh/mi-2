import json
import random
from typing import Dict, List
from blessed import Terminal
import asyncio
import websockets

HORIZONTAL_WALL = "══"
TOP_LEFT_CORNER = "╔═"
TOP_RIGHT_CORNER = "═╗"
VERTICAL_WALL = "║"
BOTTOM_LEFT_CORNER = "╚═"
BOTTOM_RIGHT_CORNER = "═╝"

BLOCK = "█"

class Pos:

    def __init__(self, x, y):
        self.x = x
        self.y = y


class Tile:

    def __init__(self, symbol: str, walkable: bool, pos: Pos, term: Terminal):
        self.term = term
        self.symbol = symbol
        self.walkable = walkable
        self.pos = pos
        print(self, end="", flush=True)

    def _render(self, color=None, custom_symbol=None):
        color = color or self.term.white
        custom_symbol = custom_symbol or self.symbol
        return self.term.move_xy(self.pos.x * 2, self.pos.y) + color(custom_symbol) + self.term.normal

    def __str__(self):
        return self._render()

class Entity(Tile):

    def __init__(self, symbol: str, walkable: bool, pos: Pos, term: Terminal):
        super().__init__(symbol, walkable, pos, term)

    def move(self, dx, dy, board: list[list[Tile]]):
        pass


class Wall(Tile):

    def __init__(self, pos, term: Terminal, map_size: tuple[int, int], is_pretty=False):
        self.map_size = map_size
        self.is_pretty = is_pretty
        super().__init__("▒▒", False, pos, term)

    def _render(self, color=None, custom_symbol=None):
        return super()._render(color=self.term.ivory4, custom_symbol=custom_symbol)

    def __str__(self):
        if not self.is_pretty:
            if self.pos.y == 0 or self.pos.y == self.map_size[1] - 1:
                return self._render(custom_symbol=BLOCK*2)
            if self.pos.x == 0 or self.pos.x == self.map_size[0] - 1:
                return self._render(custom_symbol=BLOCK*2)
        if self.pos.x == 0 and self.pos.y == 0:
            return self._render(custom_symbol=TOP_LEFT_CORNER)
        if self.pos.x == self.map_size[0] - 1 and self.pos.y == 0:
            return self._render(custom_symbol=TOP_RIGHT_CORNER)
        if self.pos.x == 0 and self.pos.y == self.map_size[1] - 1:
            return self._render(custom_symbol=BOTTOM_LEFT_CORNER)
        if self.pos.x == self.map_size[0] - 1 and self.pos.y == self.map_size[1] - 1:
            return self._render(custom_symbol=BOTTOM_RIGHT_CORNER)
        if self.pos.x == 0:
            return self._render(custom_symbol=VERTICAL_WALL)
        if self.pos.x == self.map_size[0] - 1:
            return self._render(custom_symbol=" " + VERTICAL_WALL)
        if self.pos.y == 0 or self.pos.y == self.map_size[1] - 1:
            return self._render(custom_symbol=HORIZONTAL_WALL)

        return super().__str__()


class Empty(Tile):

    def __init__(self, pos, term: Terminal):
        super().__init__("  ", True, pos, term)

    def __str__(self):
        return self._render(color=self.term.on_darkolivegreen)


class Treasure(Tile):

    def __init__(self, pos, term: Terminal):
        self.collected = False
        super().__init__(BLOCK*2, True, pos, term)

    def __str__(self):
        color = self.term.gold if self.collected else self.term.sienna4
        return self._render(color=color)

    def collect(self):
        self.collected = True


class Exit(Tile):

    def __init__(self, pos, term: Terminal):
        super().__init__("XX", True, pos, term)


class Player(Entity):

    def __init__(self, pos, term: Terminal):
        super().__init__(BLOCK*2, True, pos, term)

    def __str__(self):
        return self._render(color=self.term.cyan2)

    def move(self, dx, dy, board: list[list[Tile]]):
        x, y = self.pos.x + dx, self.pos.y + dy
        tile = board[y][x]
        if tile.walkable:
            board[self.pos.y][self.pos.x] = Empty(self.pos, self.term)
            self.pos = Pos(x, y)
            board[y][x] = self
            if isinstance(tile, Treasure):
                tile.collect()
            
            if isinstance(tile, Exit):
                print(self.term.move_xy(0, 0) + self.term.green("You win!"))
                exit(0)

            if isinstance(tile, Enemy):
                print(self.term.move_xy(0, 0) + self.term.red("Game Over!"))
                exit(0)

class Enemy(Entity):

    def __init__(self, pos, term: Terminal):
        super().__init__(BLOCK*2, True, pos, term)

    def _render(self, color=None, custom_symbol=None):
        return super()._render(color=self.term.indianred1)

    def move(self, dx, dy, board):
        x, y = self.pos.x + dx, self.pos.y + dy
        tile = board[y][x]
        if tile.walkable:
            board[self.pos.y][self.pos.x] = Empty(self.pos, self.term)
            self.pos = Pos(x, y)
            board[y][x] = self
            if isinstance(tile, Player):
                print(self.term.move_xy(0, 0) + self.term.red("Game Over!"))
                exit(0)


class Game:

    def __init__(self, uri: str):
        self.term = Terminal()
        self.uri = uri
        self.map = []  # type: list[list[Tile]]
        print(self.term.home + self.term.clear, end="", flush=True)
        self.players: Dict[str, Player] = {}
        self.enemies: List[Enemy] = []
        self.treasure: Treasure | None = None
        self.exit: Exit | None = None
        self.map_size = (0, 0)
        self.id: str | None = None

    async def connect(self):
        async with websockets.connect(self.uri) as socket:
            print("Connected to server")
            
    
    
    async def main_loop(self, socket):
        with self.term.cbreak(), self.term.hidden_cursor():
            while True:
                message = await socket.recv()
                data = json.loads(message)
                print(data)

                if data["type"] == "init":
                    self.handle_init(data)

    def handle_init(self, data):
        width = data["width"]
        height = data["height"]
        self.map_size = (width, height)
        self.map = [[Empty(Pos(j, i), self.term) for j in range(width)] for i in range(height)]
        for wall in data["walls"]:
            x, y = wall
            self.map[y][x] = Wall(Pos(x, y), self.term, self.map_size)


    def _init_map(self):
        self._place_walls()
        self._place_treasure()
        self._place_enemies()

    def _place_enemies(self):
        for _ in range(10):
            enemy = self.place_random_tile(Enemy)
            self.enemies.append(enemy)

    def _place_walls(self):
        for i in range(self.width):
            self.map[0][i] = Wall(Pos(i, 0), self.term, (self.width, self.height))
            self.map[self.height - 1][i] = Wall(Pos(i, self.height - 1), self.term, (self.width, self.height))

        for i in range(1, self.height - 1):
            self.map[i][0] = Wall(Pos(0, i), self.term, (self.width, self.height))
            self.map[i][self.width - 1] = Wall(Pos(self.width - 1, i), self.term, (self.width, self.height))

        for _ in range((self.width * self.height) // 6):
            x, y = random.randint(1, self.width - 2), random.randint(
                1, self.height - 2)
            self.map[y][x] = Wall(Pos(x, y), self.term, (self.width, self.height))

    def place_random_tile(self, tile_class):
        placed = False
        while not placed:
            x, y = random.randint(1, self.width - 2), random.randint(1, self.height - 2)
            tile = self.map[y][x]
            if not isinstance(tile, Empty):
                continue
            tile = tile_class(Pos(x, y), self.term)
            self.map[y][x] = tile
            placed = True
        return tile

    def _place_treasure(self):
        self.treasure = self.place_random_tile(Treasure)

    def move_enemies(self):
        for enemy in self.enemies:
            dx, dy = random.choice([(0, 1), (0, -1), (1, 0), (-1, 0)])
            enemy.move(dx, dy, self.map)

    def _draw(self):
        if self.treasure:
            print(self.treasure)
        for enemy in self.enemies:
            print(enemy)
        print(self.player)

    def play(self):
        with self.term.cbreak(), self.term.hidden_cursor():
            while True:
                self._draw()
                inp = self.term.inkey(timeout=0.25)
                if inp == "q":
                    break
                elif inp in ["w", "W"]:
                    self.player.move(0, -1, self.map)
                elif inp in ["s", "S"]:
                    self.player.move(0, 1, self.map)
                elif inp in ["a", "A"]:
                    self.player.move(-1, 0, self.map)
                elif inp in ["d", "D"]:
                    self.player.move(1, 0, self.map)

                self.move_enemies()


if __name__ == '__main__':
    try:
        client = Game("ws://game-lsc.kou-gen.net")
        asyncio.run(client.connect())
    except KeyboardInterrupt:
        print("Goodbye!")