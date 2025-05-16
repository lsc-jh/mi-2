import json
import random
from typing import Dict, List
from blessed import Terminal
import asyncio
import websockets
import sys

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


class Player(Tile):
    def __init__(self, pos, term: Terminal, is_self=False):
        self.is_self = is_self
        super().__init__(BLOCK * 2, True, pos, term)

    def __str__(self):
        color = self.term.cyan2 if self.is_self else self.term.orange4
        return self._render(color=color)

    async def move(self, dx, dy, map: List[List[Tile]], ws: websockets.ClientConnection):
        new_x, new_y = self.pos.x + dx, self.pos.y + dy
        tile = map[new_y][new_x]
        if tile.walkable:
            await ws.send(json.dumps({"type": "move", "dir": "up" if dy < 0 else "down" if dy > 0 else "left" if dx < 0 else "right"}))


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
        self.enemies: Dict[str, Enemy] = {}

        self.treasure: Treasure | None = None
        self.exit: Exit | None = None
        self.map_size = (0, 0)
        self.id: str | None = None
        self.player: Player | None = None

    async def connect(self):
        async with websockets.connect(self.uri) as socket:
            print("Connected to server")
            await self.main_loop(socket)

    async def main_loop(self, socket):
        with self.term.cbreak(), self.term.hidden_cursor():
            while True:
                try:
                    message = await asyncio.wait_for(socket.recv(), timeout=0.05)
                    data = json.loads(message)

                    if data["type"] == "init":
                         self.handle_init(data)

                    if data["type"] == "state":
                        self.handle_state(data)
                except asyncio.TimeoutError:
                    pass

                key = self.term.inkey(timeout=0.01)
                if key.lower() == "q":
                    await socket.close()
                    sys.exit(0)

                key = key.lower()
                if key and self.player:
                    if key == "w":
                        await self.player.move(0, -1, self.map, socket)
                    if key == "s":
                        await self.player.move(0, 1, self.map, socket)
                    if key == "a":
                        await self.player.move(-1, 0, self.map, socket)
                    if key == "d":
                        await self.player.move(1, 0, self.map, socket)

    def handle_init(self, data):
        width = data["width"]
        height = data["height"]
        self.map_size = (width, height)
        self.map = [[Empty(Pos(j, i), self.term) for j in range(width)] for i in range(height)]
        for wall in data["walls"]:
            x, y = wall["x"], wall["y"]
            self.map[y][x] = Wall(Pos(x, y), self.term, self.map_size)

    def handle_state(self, data):
        self.id = data.get("you")
        if not self.id:
            return

        for pid, pos in data["players"].items():
            if pid in self.players:
                player = self.players[pid]
                self.map[player.pos.y][player.pos.x] = Empty(player.pos, self.term)
                player.pos.x = pos["x"]
                player.pos.y = pos["y"]
                print(player, end="", flush=True)
            else:
                player = Player(Pos(pos["x"], pos["y"]), self.term, is_self=(pid == self.id))
                self.players[pid] = player
                self.map[pos["y"]][pos["x"]] = player

        self.player = self.players.get(self.id)

        for eid, pos in data["enemies"].items():
            if eid in self.enemies:
                enemy = self.enemies[eid]
                self.map[enemy.pos.y][enemy.pos.x] = Empty(enemy.pos, self.term)
                enemy.pos.x = pos["x"]
                enemy.pos.y = pos["y"]
                print(enemy, end="", flush=True)
            else:
                enemy = Enemy(Pos(pos["x"], pos["y"]), self.term)
                self.enemies[eid] = enemy
                self.map[pos["y"]][pos["x"]] = enemy


if __name__ == '__main__':
    try:
        client = Game("ws://game-lsc.kou-gen.net")
        asyncio.run(client.connect())
    except KeyboardInterrupt:
        print("Goodbye!")
