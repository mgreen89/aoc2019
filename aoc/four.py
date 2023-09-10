import itertools

from . import utils


def solve_a(inp):
  check_min, check_max = (int(x) for x in inp.split("-"))

  possibles = []

  for i in range(check_min, check_max + 1):
    istr = str(i)
    
    # Two adjacent digits must be the same.
    if not any(a == b for a, b in zip(istr, istr[1:])):
      continue

    # Digits always increase.
    if not all(a <= b for a, b in zip(istr, istr[1:])):
      continue

    possibles.append(i)

  print(len(possibles))
  
  return possibles


def solve_b(inp):
  first_pass = solve_a(inp)

  possibles = []

  for i in first_pass:
    istr = str(i)
    gs = itertools.groupby(istr, lambda x: x)
    if any(len(list(g)) == 2 for k, g in gs):
      possibles.append(i)      

  print(len(possibles))


def run():
  solve_a(utils.load_input(4))
  solve_b(utils.load_input(4))