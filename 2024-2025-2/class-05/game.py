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
        self.map = []
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
        pass

    def _place_walls(self):
        pass

    def _place_treasure(self):
        pass

    def _place_enemies(self):
        pass

    def _move_enemies(self):
        pass

    def _move_player(self, dx, dy):
        pass

    def _check_victory(self):
        pass

    def _draw(self, screen):
        screen.clear()
        for y in range(self.height):
            for x in range(self.width):
                screen.addch(y, x * 2, self.map[y][x].symbol)
        screen.refresh()

    def play(self, screen):
        pass


def main():
    game = Game(20, 20)
    curses.wrapper(game.play)


if __name__ == '__main__':
    main()
