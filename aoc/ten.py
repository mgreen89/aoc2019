import bisect
import cmath

from . import utils

# N.B. Arrays indexed by reverse co-ordinate
# i.e. arr[3][7] = (7, 3)

def input_str_to_arrs(inp):
  return [list(line) for line in inp.split("\n")]


def generate_all_asteroids(maparr):
  for i, line in enumerate(maparr):
    for j, point in enumerate(line):
      if point == "#":
        yield (j, i)


def find_max_seen(inp):
  maparr = input_str_to_arrs(inp)
  asteroids = list(generate_all_asteroids(maparr))

  # Complex axis points down.
  complex_asteroids = [complex(i, j) for (i, j) in asteroids]

  # For each asteroid, find the distance to each other asteroid as
  # a complex number.
  # Then, for each distance, if it is a multiple of any other distance,
  # remove it since it can't be seen.
  # The number of asteroid each asteroid can see is the count of the distances.
  max_seen = 0
  max_seen_i = -1
  for i, ast in enumerate(complex_asteroids):
    # Find the distances to all other asteroids.
    distances = [dest - ast for dest in complex_asteroids if dest != ast]

    # Remove the entries which are multiples of any other asteroid.
    closest = [dist
               for dist in distances
               if not any(
                 (dist/chk).real == dist/chk and (dist/chk).real > 1
                 for chk in distances
                 if chk != dist)
              ]

    if max_seen < len(closest):
      max_seen = len(closest)
      max_seen_i = i

  return max_seen, asteroids[max_seen_i]


def solve_a(inp):
  # Can definitely be sped up.
  print(find_max_seen(inp))


def solve_b(inp):
  maparr = input_str_to_arrs(inp)
  asteroids = list(generate_all_asteroids(maparr))

  # Base asteroid
  base = (26, 29)
  asteroids.remove(base)

  # Change all the co-ords to be relative to the base asteroid.
  rel_asteroids = [(x - base[0], y - base[1]) for (x, y) in asteroids]

  # Now change them all to be polar coordinates.
  rel_asteroids_polar = [cmath.polar(complex(x, y)) for (x, y) in rel_asteroids]

  # Swap the field order, then sort.
  field = sorted([(y, x) for (x, y) in rel_asteroids_polar])

  # Co-ordinates are y-reversed, therefore -pi/2 is the start argument.
  # Sweep from positive to negative, so sort in descending order of argument.
  # To find the start coordinate, it's the first in the list that has an
  # argument greater than -pi/2.
  start_i = bisect.bisect_left(field, (-cmath.pi / 2, 0))
  removed = 0
  last_removed = None
  i = start_i
  while removed < 200:
    curr_phase = field[i][0]
    last_removed = field.pop(i)
    removed += 1

    if i == len(field):
        i = 0

    # Skip over any more asteroids with the same phase.
    while field[i][0] == curr_phase:
      i += 1
      if i == len(field):
        i = 0

  # Take the last removed polar co-ords, and swap back to rectilinear.
  relative_pos = cmath.rect(last_removed[1], last_removed[0])
  print(relative_pos)

  absolute_pos = (26 + round(relative_pos.real), 29 + round(relative_pos.imag))
  print(absolute_pos)

  print(absolute_pos[0] * 100 + absolute_pos[1])


def test():
  tfield = """......#.#.
#..#.#....
..#######.
.#.#.###..
.#..#.....
..#....#.#
#..#....#.
.##.#..###
##...#..#.
.#....####"""

  print(find_max_seen(tfield))


def run():
  #test()
  #solve_a(utils.load_input(10))
  solve_b(utils.load_input(10))