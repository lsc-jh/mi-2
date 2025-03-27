import random
from blessed import Terminal


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

    def __str__(self):
        return self.term.move_xy(self.pos.x, self.pos.y) + self.symbol


class Entity(Tile):

    def __init__(self, symbol: str, walkable: bool, pos: Pos, term: Terminal):
        super().__init__(symbol, walkable, pos, term)

    def move(self, dx, dy, board: list[list[Tile]]):
        x, y = self.pos.x + dx, self.pos.y + dy
        tile = board[y][x]
        if tile.walkable:
            board[self.pos.y][self.pos.x] = Empty(self.pos)
            self.pos = Pos(x, y)


class Wall(Tile):

    def __init__(self, pos, term: Terminal):
        super().__init__("#", False, pos, term)


class Empty(Tile):

    def __init__(self, pos, term: Terminal):
        super().__init__(" ", True, pos, term)


class Treasure(Tile):

    def __init__(self, pos, term: Terminal):
        super().__init__("T", True, pos, term)
        self.collected = False

    def collect(self):
        self.collected = True
        self.symbol = " "


class Exit(Tile):

    def __init__(self, pos, term: Terminal):
        super().__init__("E", True, pos, term)


class Player(Entity):

    def __init__(self, pos, term: Terminal):
        super().__init__("P", True, pos, term)


class Enemy(Entity):

    def __init__(self, pos, term: Terminal):
        super().__init__("E", True, pos, term)


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
        prints = []
        for y in range(self.height):
            for x in range(self.width):
                prints.append(term.move_xy(x * 2, y) + self.map[y][x].symbol)
        px, py = self.player.pos.x, self.player.pos.y
        prints.append(term.move_xy(px * 2, py) + self.player.symbol)
        for p in prints:
            print(p, end="", flush=True)

    def play(self, term: Terminal):
        print(term.clear, end="", flush=True)
        with term.cbreak(), term.hidden_cursor():
            while True:
                self._draw(term)
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
