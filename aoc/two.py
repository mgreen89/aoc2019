import itertools

from . import utils


class OpCodeError(Exception):
  pass


class ProgramFinished(Exception):
  pass


class IntComputer:
  """
  Computer that processes IntCode.

  """
  def __init__(self):
    self.intcode = None

  def load_intcode(self, intcode):
    self.intcode = intcode[:]

  def step(self, start):
    ops = self.intcode[start:start + 4]

    if ops[0] == 1:
      # Add
      self.intcode[ops[3]] = (
        self.intcode[ops[1]] + self.intcode[ops[2]])

    elif ops[0] == 2:
      # Multiply
      self.intcode[ops[3]] = (
        self.intcode[ops[1]] * self.intcode[ops[2]])

    elif ops[0] == 99:
      # Abort
      raise ProgramFinished()

    else:
      raise OpCodeError("Invalid op code: {}".format(ops[0]))

  def run(self):
    i = 0

    try:
      while True:
        self.step(i)
        i += 4

    except ProgramFinished:
      pass

    except OpCodeError as e:
      print(str(e))


def solve_a(inp):
  intcode = [int(x) for x in inp.split(",")]
  intcode[1] = 12
  intcode[2] = 2
  c = IntComputer()
  c.load_intcode(intcode)
  c.run()
  print(c.intcode)
  print(c.intcode[0])


def solve_b(inp, target):
  intcode = [int(x) for x in inp.split(",")]
  
  c = IntComputer()

  for noun in range(100):
    for verb in range(100):
      intcode[1] = noun
      intcode[2] = verb

      c.load_intcode(intcode)
      c.run()
      
      if c.intcode[0] == target:
        print(f"Solution: {noun}, {verb}")
        print(100 * noun + verb)


def run():
  solve_a(utils.load_input(2))
  solve_b(utils.load_input(2), 19690720)
