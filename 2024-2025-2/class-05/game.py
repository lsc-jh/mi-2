import random
import time
import curses


class Tile:
    def __init__(self, symbol, walkable):
        self.symbol = symbol
        self.walkable = walkable


class Wall(Tile):
    def __init__(self):
        super().__init__("#", False)


class Empty(Tile):
    def __init__(self):
        super().__init__(" ", True)


class Treasure(Tile):
    def __init__(self):
        super().__init__("T", True)
        self.collected = False

    def collect(self):
        self.collected = True
        self.symbol = " "


class Exit(Tile):
    def __init__(self):
        super().__init__("E", True)


class Player(Tile):
    def __init__(self):
        super().__init__("P", True)


class Enemy(Tile):
    def __init__(self):
        super().__init__("E", True)


class Game:
    def __init__(self, width, height):
        self.width = width
        self.height = height
        self.map = []  # type: list[list[Tile]]
        for _ in range(height):
            tmp = []
            for _ in range(width):
                tmp.append(Empty())
            self.map.append(tmp)
        # self.map = [[Empty() for _ in range(self.width)] for _ in range(self.height)]
        self.player_pos = [1, 1]
        self.enemies = []
        self.treasure = None
        self.exit_pos = (width - 2, height - 2)
        self._init_map()

    def _init_map(self):
        self._place_walls()
        self._place_treasure()
        self._place_enemies()

        self.map[1][1] = Player()
        self.map[self.exit_pos[1]][self.exit_pos[0]] = Exit()

    def _place_walls(self):
        for i in range(self.width):
            self.map[0][i] = Wall()
            self.map[self.height - 1][i] = Wall()

        for i in range(1, self.height - 1):
            self.map[i][0] = Wall()
            self.map[i][self.width - 1] = Wall()

        for _ in range((self.width * self.height) // 6):
            x, y = random.randint(1, self.width - 2), random.randint(1, self.height - 2)
            self.map[y][x] = Wall()

    def _place_treasure(self):
        while True:
            x, y = random.randint(1, self.width - 2), random.randint(1, self.height - 2)
            if isinstance(self.map[y][x], Empty):
                self.map[y][x] = Treasure()
                self.treasure = (x, y)
                break

    def _place_enemies(self):
        for _ in range(3):
            while True:
                x, y = random.randint(1, self.width - 2), random.randint(1, self.height - 2)
                if isinstance(self.map[y][x], Empty):
                    self.map[y][x] = Enemy()
                    self.enemies.append([x, y])
                    break

    def _move_enemies(self):
        pass

    def _move_player(self, dx, dy):
        x, y = self.player_pos[0] + dx, self.player_pos[1] + dy
        tile = self.map[y][x]
        if tile.walkable:
            self.map[self.player_pos[1]][self.player_pos[0]] = Empty()
            self.player_pos = [x, y]
            self.map[y][x] = Player()

    def _check_victory(self):
        pass

    def _draw(self, screen):
        screen.clear()
        for y in range(self.height):
            for x in range(self.width):
                screen.addch(y, x * 2, self.map[y][x].symbol)
        screen.refresh()

    def play(self, screen):
        curses.curs_set(0)
        screen.nodelay(1)
        screen.timeout(200)

        while True:
            self._draw(screen)
            key = screen.getch()

            if key in [ord("w"), curses.KEY_UP]:
                self._move_player(0, -1)
            elif key in [ord("s"), curses.KEY_DOWN]:
                self._move_player(0, 1)
            elif key in [ord("a"), curses.KEY_LEFT]:
                self._move_player(-1, 0)
            elif key in [ord("d"), curses.KEY_RIGHT]:
                self._move_player(1, 0)
            elif key == ord("q"):
                break


def main():
    game = Game(20, 20)
    curses.wrapper(game.play)


if __name__ == '__main__':
    try:
        main()
    except KeyboardInterrupt:
        print("Goodbye!")
