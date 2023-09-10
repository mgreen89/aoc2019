from . import async_computer
from . import utils


def solve_a(inp):
  count = 0
  for x in range(50):
    for y in range(50):
      c = async_computer.Computer()
      c.init_memory_from_string(inp)
      c.run_async()
      c.send(x)
      c.send(y)
      count += c.get()

  print(count)


def get_beam(x, y, inp):
  c = async_computer.Computer()
  c.init_memory_from_string(inp)
  c.run_async()
  c.send(x)
  c.send(y)
  return c.get()


def get_beam_map_full(max_x, max_y, inp):
  beam_map = {}
  for x in range(max_x):
    for y in range(max_y):
      beam_map[(x,y)] = get_beam(x, y, inp)
  return beam_map


def get_beams_minimal(max_y, max_width, inp):
  # Find the first and last x co-ord for each y value.
  # Assume the beam moves at most 1 square to the right for
  # min and max, and never moves left.
  # Ignore the missing beams in the first few rows.
  beams = []

  if max_y is None:
    max_y = int(1e6)

  if max_width is None:
    max_width = int(1e3)

  # First row always has a single beam in.
  beams.append((0, 0))

  y = 1
  width = 1
  while y < max_y and width < max_width:
    min_x = beams[y-1][0]
    # Try the same min as as the previous row.
    val = get_beam(min_x, y, inp)
    if val == 0:
      min_x += 1

    # Try the next max from the previous row.
    max_x = beams[y-1][1]
    val = get_beam(max_x + 1, y, inp)
    if val == 1:
      max_x += 1
    
    beams.append((min_x, max_x))
    y += 1
    width = max_x - min_x

  return beams


def solve_b(inp):
  beams = get_beams_minimal(None, 250, inp)

  for i, beam in enumerate(beams):
    if beams[i + 99][0] <= beam[1] - 99:
      print(i)
      print(beams[i][0], beam[1])
      print(beams[i+99][0], beams[i+99][1])
      print(beam[1] - 99, i)
      break


def run():
  #solve_a(utils.load_input(19))
  solve_b(utils.load_input(19))