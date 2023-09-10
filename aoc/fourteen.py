import collections
import dataclasses
import math
import queue
import re
from typing import Dict

from . import utils


ORE = "ORE"
FUEL = "FUEL"


@dataclasses.dataclass
class Reaction:
  inputs: Dict[str, int]
  output: str
  output_amount: int


def parse_input_to_reactions(inp):
  r = re.compile(r"([0-9]+) ([A-Z]+)")
  reactions = {}
  for line in inp.split("\n"):
    m = r.findall(line)
    assert m is not None, line

    inputs = {n: int(c) for (c, n) in m[:-1]}
    output = m[-1][1]
    output_amount = int(m[-1][0])

    reactions[output] = Reaction(inputs, output, output_amount)

  return reactions


def find_ore_required(reactions, product, amount):
  # For each reaction required to create materials, work out how many
  # sub-reactions are required to create all the reagents, until
  # reaching the base reagent ORE.
  def walk(p, a, r):
    if p == "ORE":
      r[p] += a
      return

    # Get the reaction for the product.
    reaction = reactions[p] 

    # Work out number of reactions required
    reaction_count = 0
    product_amount = r[p]

    while product_amount < a:
      reaction_count += 1
      product_amount += reaction.output_amount

    # Set the remaining product.
    r[p] = product_amount - a

    # Recurse for each reagent.
    for reagent, required in reaction.inputs.items():
      walk(reagent, required * reaction_count, r)

  reagents = collections.defaultdict(lambda: 0)
  walk(product, amount, reagents)

  return reagents[ORE]


@dataclasses.dataclass
class Order:
  product: str
  amount: int


def find_ore_req_non_recursive(reactions, product, amount):
  orders = queue.Queue()
  inventory = collections.defaultdict(lambda: 0)
  ore_required = 0

  orders.put(Order(product, amount))

  while not orders.empty():
    curr_order = orders.get()

    if curr_order.product == ORE:
      ore_required += curr_order.amount

    elif curr_order.amount < inventory[curr_order.product]:
      inventory[curr_order.product] -= curr_order.amount
  
    else:
      required_amount = curr_order.amount - inventory[curr_order.product]
      reaction = reactions[curr_order.product]
      req_reactions = math.ceil(required_amount / reaction.output_amount)

      #print("Gen {}".format(curr_order.product))

      for reagent, amount in reaction.inputs.items():
        orders.put(Order(reagent, amount * req_reactions))

      leftovers = (req_reactions * reaction.output_amount) - required_amount
      inventory[curr_order.product] = leftovers
    
  return ore_required


class OutOfOre(Exception):
  """
  Out of ore exception.

  """


def generate_fuel(reactions, starting_ore):
  reagents = collections.defaultdict(lambda: 0)
  reagents[ORE] = int(starting_ore)


  def generate(product, amount, reagents, include_existing=True):
    # Generate 'a' amount of product 'p'.

    if include_existing:
      amount_to_generate = amount - reagents[product]
    else:
      amount_to_generate = amount

    reaction = reactions[product]
    generated = 0
    while generated < amount_to_generate:
      # Run a reaction.
      for reagent, reagent_amount in reaction.inputs.items():
        # Make sure there's enough of each reagent.
        if reagent == ORE:
          if reagents[ORE] < reagent_amount:
            raise OutOfOre
        else:
          generate(reagent, reagent_amount, reagents)

        reagents[reagent] -= reagent_amount

      generated += reaction.output_amount

    reagents[product] += generated

  try:
    while True:
      generate(FUEL, 1, reagents, False)
  except OutOfOre:
    return reagents[FUEL]


def solve_a(inp):
  reactions = parse_input_to_reactions(inp)
  print(find_ore_required(reactions, FUEL, 1))
  print(find_ore_req_non_recursive(reactions, FUEL, 1))


def solve_b_brute_force(inp):
  reactions = parse_input_to_reactions(inp)
  generate_fuel(reactions, 1e12)


def solve_b_bsearch(inp):
  reactions = parse_input_to_reactions(inp)
  lower_bound = int(1e12 / 483766)
  upper_bound = lower_bound * 4

  ore_limit = int(1e12)

  while upper_bound - lower_bound > 1:
    midpoint = (upper_bound + lower_bound) // 2
    ore_req = find_ore_req_non_recursive(reactions, FUEL, midpoint)

    if ore_req > ore_limit:
      upper_bound = midpoint
    elif ore_req < ore_limit:
      lower_bound = midpoint

  print(lower_bound)
  return lower_bound


TEST1 = """157 ORE => 5 NZVS
165 ORE => 6 DCFZ
44 XJWVT, 5 KHKGT, 1 QDVJ, 29 NZVS, 9 GPVTF, 48 HKGWZ => 1 FUEL
12 HKGWZ, 1 GPVTF, 8 PSHF => 9 QDVJ
179 ORE => 7 PSHF
177 ORE => 5 HKGWZ
7 DCFZ, 7 PSHF => 2 XJWVT
165 ORE => 2 GPVTF
3 DCFZ, 7 NZVS, 5 HKGWZ, 10 PSHF => 8 KHKGT"""


TEST2 = """171 ORE => 8 CNZTR
7 ZLQW, 3 BMBT, 9 XCVML, 26 XMNCP, 1 WPTQ, 2 MZWV, 1 RJRHP => 4 PLWSL
114 ORE => 4 BHXH
14 VRPVC => 6 BMBT
6 BHXH, 18 KTJDG, 12 WPTQ, 7 PLWSL, 31 FHTLT, 37 ZDVW => 1 FUEL
6 WPTQ, 2 BMBT, 8 ZLQW, 18 KTJDG, 1 XMNCP, 6 MZWV, 1 RJRHP => 6 FHTLT
15 XDBXC, 2 LTCX, 1 VRPVC => 6 ZLQW
13 WPTQ, 10 LTCX, 3 RJRHP, 14 XMNCP, 2 MZWV, 1 ZLQW => 1 ZDVW
5 BMBT => 4 WPTQ
189 ORE => 9 KTJDG
1 MZWV, 17 XDBXC, 3 XCVML => 2 XMNCP
12 VRPVC, 27 CNZTR => 2 XDBXC
15 KTJDG, 12 BHXH => 5 XCVML
3 BHXH, 2 VRPVC => 7 MZWV
121 ORE => 7 VRPVC
7 XCVML => 6 RJRHP
5 BHXH, 4 VRPVC => 5 LTCX"""

def test_a():
  for t in [TEST1, TEST2]:
    reactions = parse_input_to_reactions(t)
    print(find_ore_required(reactions, FUEL, 1))

def test_b():
  for t in [TEST1, TEST2]:
    reactions = parse_input_to_reactions(t)
    print(generate_fuel(reactions, 1e9))


def run():
  #test_a()
  #test_b()
  solve_a(utils.load_input(14))
  #solve_b(utils.load_input(14))
  solve_b_bsearch(utils.load_input(14))