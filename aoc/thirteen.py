import queue

from . import async_computer
from . import utils


# Tile IDs
# 0 - empty
# 1 - wall (indestructible)
# 2 - block (can be broken)
# 3 - horiz paddle (indestructible)
# 4 - ball (moves diagonally)
TID_TO_CHR = [
  " ",
  "$",
  "#",
  "-",
  "o"
]


def print_tiles(tile_dict):
  max_x = max(x for (x, y) in tile_dict)
  max_y = max(y for (x, y) in tile_dict)

  print("Score: {}".format(tile_dict[(-1,0)]))

  for j in range(max_y + 1):
    for i in range(max_x + 1):
      print(TID_TO_CHR[tile_dict[(i, j)]], end="")
    print()


def solve_a(inp):
  c = async_computer.Computer()
  c.init_memory_from_string(inp)

  c.run_async()

  tiles = {}

  while not c.finished_event.isSet():
    x = c.get()
    y = c.get()
    tid = c.get()
    tiles[(x,y)] = tid

  num_blocks = sum(1 for pos, tid in tiles.items() if tid == 2)
  print(num_blocks)

def solve_b(inp):
  program = [int(x) for x in inp.split(",")]

  # Set memory address 0 to 2 to play for free.
  program[0] = 2

  c = async_computer.Computer()
  c.init_memory(program)

  c.run_async()

  tiles = {}
  c.send(0)

  paddle = (0, 0)
  while True:
    x = c.get()
    y = c.get()
    tid = c.get()
    tiles[(x,y)] = tid

    if tid == 3:
      paddle = (x, y)
    elif tid == 4:
      ball = (x, y)

    if x == -1:
      # Got score - end of initialization.
      break

  i = 0
  while not c.finished_event.isSet():
    if ball[0] < paddle[0]:
      c.send(-1)
    elif ball[0] > paddle[0]:
      c.send(1)
    else:
      c.send(0)

    c.input_queue.join()

    # This timing is all a bit dodgy.
    # Don't know how may values to get out before sending in another one.

    while True:
      try:
        x = c.get(timeout=0.005)
        y = c.get()
        tid = c.get()

        tiles[(x,y)] = tid

        if x == -1 and y == 0:
          print(f"Score {tid}")

        if tid == 3:
          paddle = (x, y)
        elif tid == 4:
          ball = (x, y)
      except queue.Empty:
        break

    i += 1
    if (i % 100) == 0:
      print(i)
      print_tiles(tiles)

  print(tiles[(-1,0)])


def run():
  #solve_a(utils.load_input(13))
  solve_b(utils.load_input(13))