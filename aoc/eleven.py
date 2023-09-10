import queue

from . import async_computer
from . import utils


class Printer:
  def __init__(self, program, start_square=0):
    self.white_panels = set()
    self.painted_panels = set()

    self.pos = complex(0, 0)
    self.direction = complex(0, 1)

    if start_square == 1:
      self.white_panels.add(complex(0,0))

    self.c = async_computer.Computer()
    self.c.init_memory_from_string(program)

  def run(self):
    self.c.run_async()

    while not self.c.finished_event.isSet():
      if self.pos in self.white_panels:
        self.c.send(1)
      else:
        self.c.send(0)

      # Retreive the colour.
      # 0 - black, 1 - white
      colour = self.c.get()
      if colour == 0:
        self.white_panels.discard(self.pos)
      else:
        self.white_panels.add(self.pos)
      self.painted_panels.add(self.pos)
      
      # Get the turn direction.
      # 0 - left, 1 - right
      turn = self.c.get()
      if turn == 0:
        self.direction *= 1j
      else:
        self.direction *= -1j

      # Move forward one square.
      self.pos += self.direction


def solve_a(inp):
  p = Printer(inp)
  p.run()

  print(len(p.painted_panels))


def solve_b(inp):
  p = Printer(inp, 1)
  p.run()

  # Find the min and max x and y coords of white squares.
  min_x = min(int(x.real) for x in p.white_panels)
  min_y = min(int(x.imag) for x in p.white_panels)
  max_x = max(int(x.real) for x in p.white_panels)
  max_y = max(int(x.imag) for x in p.white_panels)

  for y in range(max_y + 1, min_y - 2, -1):
    for x in range(min_x - 1, max_x + 1):
      if complex(x,y) in p.white_panels:
        print("#", end="")
      else:
        print(" ", end="")
    print()


def run():
  solve_a(utils.load_input(11))
  solve_b(utils.load_input(11))