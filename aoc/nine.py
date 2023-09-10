from . import computer
from . import utils


def solve_a(inp):
  mem = [int(x) for x in inp.split(",")]

  c = computer.Computer(mem)
  c.run(input_fn=lambda: 1)


def solve_b(inp):
  mem = [int(x) for x in inp.split(",")]

  c = computer.Computer(mem)
  c.run(input_fn=lambda: 2)


def run():
  solve_a(utils.load_input(9))
  solve_b(utils.load_input(9))