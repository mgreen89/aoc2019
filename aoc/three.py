import functools
from . import utils


def input_to_directions(inp):
  def dir_to_complex(d):
    if d[0] == "R":
      factor = 1
    elif d[0] == "U":
      factor = 1j
    elif d[0] == "L":
      factor = -1
    elif d[0] == "D":
      factor = -1j

    return int(d[1:]) * factor

  return [[dir_to_complex(d) for d in line.split(",")]
          for line in inp.split("\n")]


def solve_a(inp):
  #lines = input_to_directions(inp)
  # Create sets of all the points on each line (quite big)
  lines = []
  for line in inp.split("\n"):
    points = set()
    curr = 0
    for move in line.split(","):
      if move[0] == "R":
        factor = 1
      elif move[0] == "U":
        factor = 1j
      elif move[0] == "L":
        factor = -1
      elif move[0] == "D":
        factor = -1j

      for i in range(int(move[1:])):
        curr += factor
        points.add(curr)

    lines.append(points)

  assert len(lines) == 2
  
  crosses = lines[0].intersection(lines[1])
  min_distance = 1000
  for cross in crosses:
    min_dist = abs(int(cross.real)) + abs(int(cross.imag))
    if min_dist < min_distance:
      min_distance = min_dist

  print(min_distance)


def solve_b(inp):
  lines = []
  for line in inp.split("\n"):
    points = []
    points_set = set()
    curr = 0
    for move in line.split(","):
      if move[0] == "R":
        factor = 1
      elif move[0] == "U":
        factor = 1j
      elif move[0] == "L":
        factor = -1
      elif move[0] == "D":
        factor = -1j

      for i in range(int(move[1:])):
        curr += factor
        points.append(curr)
        points_set.add(curr)

    lines.append((points, points_set))

  assert len(lines) == 2
  
  min_dist = 1000000
  crosses = lines[0][1].intersection(lines[1][1])
  for cross in crosses:
    dist = lines[0][0].index(cross) + lines[1][0].index(cross) + 2
    if dist < min_dist:
      min_dist = dist

  print(min_dist)


def run():
  solve_a(utils.load_input(3))
  solve_b(utils.load_input(3))