import queue

from . import async_computer
from . import computer
from . import utils


def solve_a(inp):
  intcode = [int(x) for x in inp.split(",")]

  c = computer.Computer(intcode)
  #c.run(output_fn=lambda i: print(chr(i), end=""))

  output = []
  c.run(output_fn=lambda i: output.append(chr(i)))

  intersection_sum = 0

  output_lines = "".join(output).rstrip("\n").split("\n")
  for i, line in enumerate(output_lines):
    print(line)
    if i == 0 or i == len(output_lines) - 1:
      continue
    for j, c in enumerate(line):
      if j == 0 or j == len(line) - 1:
        continue

      try:
        if (c == "#" and
              output_lines[i - 1][j] == "#" and
              output_lines[i + 1][j] == "#" and
              output_lines[i][j - 1] == "#" and
              output_lines[i][j + 1] == "#"):
          # Intersection
          intersection_sum += (i * j)
      except IndexError:
        # There are some extra newlines at the end.
        # Now dealt with earlier.
        raise
  
  print(intersection_sum)


def solve_b(inp):
  # Figured out manually.
  instructions = [
    "A,B,A,B,A,C,B,C,A,C",   # Main routine
    "L,6,R,12,L,6",          # Function A
    "R,12,L,10,L,4,L,6",     # Function B
    "L,10,L,10,L,4,L,6",     # Function C 
    "n",                     # Continuous video feed?
  ]

  c = async_computer.Computer()
  c.init_memory_from_string(inp)
  c.memory[0] = 2
  c.run_async()

  # Line up all the input in the queue.
  for inst in instructions:
    for char in inst:
      c.send(ord(char))
    c.send(ord("\n"))

  while not c.finished_event.isSet():
    output = c.get()
    if output <= 255:
      print(chr(output), end="")
    else:
      print(f"Integer: {output}")

  # Get any remaining output.
  # Foibles of async design :(
  # Maybe should prevent computer exiting until all output read.
  while True:
    try:
      output = c.get(block=False)
    except queue.Empty:
      break

    if output <= 255:
      print(chr(output), end="")
    else:
      print(f"Integer: {output}")


def run():
  #solve_a(utils.load_input(17))
  solve_b(utils.load_input(17))



# Full path:
# L,6,R,12,L,6,
# R,12,L,10,L,4,L,6,
# L,6,R,12,L,6,
# R,12,L,10,L,4,L,6,
# L,6,R,12,L,6,
# L,10,L,10,L,4,L,6,
# R,12,L,10,L,4,L,6,
# L,10,L,10,L,4,L,6,
# L,6,R,12,L,6,
# L,10,L,10,L,4,L,6