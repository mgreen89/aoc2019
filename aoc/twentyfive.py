import itertools
import queue

from . import async_computer
from . import utils


def run_command(c, command, print_output=False):
  for char in command:
    c.send(ord(char))
  c.send(ord("\n"))

  arr = []
  while True:
    try:
      arr.append(chr(c.get(timeout=0.1)))
    except queue.Empty:
      break

  text = "".join(arr)
  if "Unrecognized" in text or print_output:
    print(text)

  return text


def solve_a(inp):
  c = async_computer.Computer()
  c.init_memory_from_string(inp)
  c.run_async()

  # Set of commands to pick up all the items and get to the security checkpoint.
  commands = [
    "west",
    "north",
    "take easter egg",
    "south",
    "take mug",
    "east",
    "south",
    "east",
    "north",
    "take candy cane",
    "south",
    "west",
    "north",
    "east",
    "north",
    "north",
    "take hypercube",
    "south",
    "east",
    "take manifold",
    "west",
    "south",
    "take coin",
    "south",
    "east",
    "take pointer",
    "west",
    "west",
    "take astrolabe",
    "north",
    "east",
    "north"
  ]

  # Get the initial output, and drop it.
  while True:
    try:
      c.get(timeout=0.1)
    except queue.Empty:
      break

  # Get to the security checkpoint.
  for cmd in commands:
    run_command(c, cmd)

  print("At security checkpoint")

  items = [
    "astrolabe",
    "candy cane",
    "coin",
    "easter egg",
    "hypercube",
    "manifold",
    "mug",
    "pointer",
  ]

  # Drop all the items.
  for item in items:
    run_command(c, f"drop {item}")

  # Try every combination of items.
  for n in range(4, len(items)):
    for comb in itertools.combinations(items, n):
      print(comb)
      for item in comb:
        run_command(c, f"take {item}")
      
      # Try going east onto the pressure pad.
      output = run_command(c, "east")

      if "Alert!" in output and ("heavier" in output or "lighter" in output):
        # Wrong combination. Drop the items.
        for item in comb:
          run_command(c, f"drop {item}")

      else:
        # Found the right set.
        # Drop back into manual mode.
        print("Passed security!")
        print(output)

        while not c.finished_event.isSet():
          # Drop into user input
          arr = []
          while True:
            try:
              arr.append(chr(c.get(timeout=0.1)))
            except queue.Empty:
              break

          text = "".join(arr)
          print(text)

          usr_input = input()
          for char in usr_input:
            c.send(ord(char))
          c.send(ord("\n"))
        


def solve_b(inp):
  pass


def run():
  solve_a(utils.load_input(25))
  solve_b(utils.load_input(25))