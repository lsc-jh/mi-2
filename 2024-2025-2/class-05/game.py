import random
import time
import os
from blessed import Terminal


class Pos:

    def __init__(self, x, y):
        self.x = x
        self.y = y


class Tile:

    def __init__(self, symbol, walkable, pos: Pos):
        self.symbol = symbol
        self.walkable = walkable
        self.pos = pos


class Entity(Tile):

    def __init__(self, symbol, walkable, pos: Pos):
        super().__init__(symbol, walkable, pos)


class Wall(Tile):

    def __init__(self, pos):
        super().__init__("#", False, pos)


class Empty(Tile):

    def __init__(self, pos):
        super().__init__(" ", True, pos)


class Treasure(Tile):

    def __init__(self, pos):
        super().__init__("T", True, pos)
        self.collected = False

    def collect(self):
        self.collected = True
        self.symbol = " "


class Exit(Tile):

    def __init__(self, pos):
        super().__init__("E", True, pos)


class Player(Entity):

    def __init__(self, pos):
        super().__init__("P", True, pos)


class Enemy(Entity):

    def __init__(self, pos):
        super().__init__("E", True, pos)


class Game:

    def __init__(self, width, height):
        self.width = width
        self.height = height
        self.map = []  # type: list[list[Tile]]
        for i in range(height):
            tmp = []
            for j in range(width):
                pos = Pos(j, i)
                tmp.append(Empty(pos))  # !!!! CHANGED !!!!!
            self.map.append(tmp)
        # self.map = [[Empty() for _ in range(self.width)] for _ in range(self.height)]

        self.enemies = []
        self.treasure = None
        self.exit_pos = Pos(width - 2, height - 2)
        self.player = Player(Pos(1, 1))
        self._init_map()

    def _init_map(self):
        self._place_walls()
        self._place_treasure()
        self._place_enemies()

        self.map[self.exit_pos.y][self.exit_pos.x] = Exit(self.exit_pos)

    def _place_walls(self):
        for i in range(self.width):
            self.map[0][i] = Wall(Pos(i, 0))
            self.map[self.height - 1][i] = Wall(Pos(i, self.height - 1))

        for i in range(1, self.height - 1):
            self.map[i][0] = Wall(Pos(0, i))
            self.map[i][self.width - 1] = Wall(Pos(self.width - 1, i))

        for _ in range((self.width * self.height) // 6):
            x, y = random.randint(1, self.width - 2), random.randint(
                1, self.height - 2)
            self.map[y][x] = Wall(Pos(x, y))

    def _place_treasure(self):
        while True:
            x, y = random.randint(1, self.width - 2), random.randint(
                1, self.height - 2)
            if isinstance(self.map[y][x], Empty):
                self.map[y][x] = Treasure(Pos(x, y))
                self.treasure = (x, y)
                break

    def _place_enemies(self):
        for _ in range(3):
            while True:
                x, y = random.randint(1, self.width - 2), random.randint(
                    1, self.height - 2)
                if isinstance(self.map[y][x], Empty):
                    self.map[y][x] = Enemy(Pos(x, y))
                    self.enemies.append([x, y])
                    break

    def _move_enemies(self):
        pass

    def _move_player(self, dx, dy):
        x, y = self.player.pos.x + dx, self.player.pos.y + dy
        tile = self.map[y][x]
        if isinstance(tile, Treasure):
            tile.collect()
        if tile.walkable:
            self.map[self.player.pos.y][self.player.pos.x] = Empty(
                self.player.pos)
            self.player.pos = Pos(x, y)

    def _check_victory(self):
        pass

    def _draw(self, term: Terminal):
        print(term.clear)

        prints = []
        for y in range(self.height):
            for x in range(self.width):
                prints.append(term.move_xy(x * 2, y) + self.map[y][x].symbol)
        px, py = self.player.pos.x, self.player.pos.y
        prints.append(term.move_xy(px * 2, py) + self.player.symbol)
        for p in prints:
            print(p, end="", flush=True)

    def play(self, term: Terminal):
        while True:
            self._draw(term)
            with term.cbreak(), term.hidden_cursor():
                inp = term.inkey()
            if inp == "w":
                self._move_player(0, -1)
            elif inp == "s":
                self._move_player(0, 1)
            elif inp == "a":
                self._move_player(-1, 0)
            elif inp == "d":
                self._move_player(1, 0)
            elif inp == "q":
                break


def main():
    game = Game(20, 20)
    term = Terminal()
    game.play(term)


if __name__ == '__main__':
    try:
        main()
    except KeyboardInterrupt:
        print("Goodbye!")
