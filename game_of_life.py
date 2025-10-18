import sys
from blessed import Terminal


class Screen:
    def __init__(self):
        self.term: Terminal = Terminal()
        print(self.term.hide_cursor)

    def on(self, x: int, y: int):
        with self.term.location(x, y):
            print(self.term.black_on_white + " ")

    def off(self, x: int, y: int):
        with self.term.location(x, y):
            print(self.term.normal + " ")

    def clear(self):
        print(self.term.clear)

    def restore(self):
        self.clear()
        print(self.term.normal_cursor)


def adjacent(x: int, y: int) -> set[tuple[int, int]]:
    pos: set[tuple[int, int]] = set()
    for i in [-1, 0, 1]:
        for j in [-1, 0, 1]:
            if not (i == 0 and j == 0):
                pos.add((x + i, y + j))
    return pos


def loop(cells: set[tuple[int, int]]):
    s = Screen()

    try:
        while True:
            deads: set[tuple[int, int]] = set()
            new_cells: set[tuple[int, int]] = set()
            new_deads: set[tuple[int, int]] = set()
            s.clear()

            for c in cells:
                adjs = adjacent(*c)
                delta = adjs - cells
                deads |= delta
                live = adjs & cells
                if 2 <= len(live) <= 3:
                    new_cells.add(c)
                else:
                    new_deads.add(c)
                s.on(*c)

            for c in deads:
                adjs = adjacent(*c)
                live = adjs & cells
                if len(live) == 3:
                    new_cells.add(c)
                else:
                    new_deads.add(c)

            _ = input()

            deads = new_deads
            cells = new_cells
    except KeyboardInterrupt:
        s.restore()


glider = set(
    [
        (10, 3),
        (11, 4),
        (11, 5),
        (10, 5),
        (9, 5),
    ]
)


converge = set(
    [
        (10, 10),
        (11, 9),
        (11, 11),
        (12, 9),
        (12, 11),
        (13, 10),
        (14, 10),
    ]
)


if __name__ == "__main__":
    if len(sys.argv) == 2 and sys.argv[1] == "glider":
        loop(cells=glider)
    else:
        loop(cells=converge)
