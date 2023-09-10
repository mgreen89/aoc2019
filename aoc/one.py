from . import utils


def get_fuel_for_mass(mass):
  return max([0, mass // 3 - 2])


def get_total_fuel_for_mass(mass):
  total_fuel = 0
  new_fuel = get_fuel_for_mass(mass)

  while new_fuel > 0:
    total_fuel += new_fuel
    new_fuel = get_fuel_for_mass(new_fuel)

  return total_fuel


def solve_a(inp):
  return sum(get_fuel_for_mass(int(x)) for x in inp.split("\n"))


def solve_b(inp):
  return sum(get_total_fuel_for_mass(int(x)) for x in inp.split("\n"))


def run():
  print(solve_a(utils.load_input(1)))
  print(solve_b(utils.load_input(1)))