import queue

from . import async_computer
from . import utils


def run_springdroid(intcode, springscript):
  c = async_computer.Computer()
  c.init_memory_from_string(intcode)
  c.run_async()

  for line in springscript:
    for char in line:
      c.send(ord(char))
    c.send(ord("\n"))

  while not c.finished_event.isSet():
    try:
      output = c.get(timeout=10)
      if output < 256:
        print(chr(output), end="")
      else:
        print(output)
    except queue.Empty:
      pass

  # Get any remaining output.
  while True:
    try:
      output = c.get(block=False)
      if output < 256:
        print(chr(output), end="")
      else:
        print(output)
    except queue.Empty:
      break


def solve_a(inp):
  # Springscript program:
  #   - springdroids jump forward 4 spaces
  #   - always make sure landing spot is safe (AND D J)
  #   - to land on an island, jump to land on the first
  #     safe spot, i.e. when the third tile is empty (NOT C J)
  #   - always jump if the next tile is empty (NOT A J)
  springscript = [
    "NOT C J",
    "AND D J",
    "NOT A T",
    "OR T J",
    "WALK"
  ]

  run_springdroid(inp, springscript)


def solve_b(inp):
  # Springscript program:
  #   - same as part a, PLUS more failures cases:
  #
  # |  @  CD   H      |
  # |#####.##.##.#.###|
  # only jump if H is okay
  #
  # |      @ B D      |
  # |#####.##.##.#.###|
  # jump if D okay and B isn't
  #
  # |          @A     |
  # |#####.##.##.#.###|
  # (as before, jump if the next tile is a hole)
  
  springscript = [
    "NOT C J",
    "AND D J",
    "AND H J",
    "NOT B T",
    "AND D T",
    "OR T J",
    "NOT A T",
    "OR T J",
    "RUN"
  ]

  run_springdroid(inp, springscript)


def run():
  #solve_a(utils.load_input(21))
  solve_b(utils.load_input(21))