import collections

from . import utils


# Width and height of each board.
WIDTH = 5
HEIGHT = 5


# Empty layer
EMPTY_LAYER = tuple(tuple("." for i in range(WIDTH)) for j in range(HEIGHT))


def valid(x, y):
  """
  Check if the x and y coordinates are valid.

  """
  return x in range(WIDTH) and y in range(HEIGHT)


def adjacent_2d(x, y):
  """
  Return tuples for all adjacent squares.

  """
  for d in ((0, 1), (0, -1), (1, 0), (-1, 0)):
    yield (x + d[0], y + d[1])


# Compute all tiles neighbours on the same level.
ADJACENT_SAME = {
  (i, j): set((x, y) for (x, y) in adjacent_2d(i, j) if valid(x, y))
  for j in range(HEIGHT)
  for i in range(WIDTH)
}


# Computer all neighbours for inner tiles on the next level down.
# Explicitly for 5 width/height.
ADJACENT_INNER = {
  (1, 2): {(0, y) for y in range(HEIGHT)},
  (3, 2): {(WIDTH - 1, y) for y in range(HEIGHT)},
  (2, 1): {(x, 0) for x in range(WIDTH)},
  (2, 3): {(x, HEIGHT - 1) for x in range(WIDTH)},
}


# Compute all neighbours for outer tiles to the next level up.
ADJACENT_OUTER = {
  outer: {inner for inner in ADJACENT_INNER
          if outer in ADJACENT_INNER[inner]}
  for outer in set.union(*ADJACENT_INNER.values())
}


def adjacent_bugs(state, x, y, width=5, height=5):
    """
    Return the number of adjacent bugs.

    """
    bugs = 0
    if x > 0:
      if state[y][x - 1] == "#":
        bugs += 1
    
    if x < width - 1:
      if state[y][x + 1] == "#":
        bugs += 1
    
    if y > 0:
      if state[y - 1][x] == "#":
        bugs += 1

    if y < height - 1:
      if state [y + 1][x] == "#":
        bugs += 1
    
    return bugs


def evolve_square(state, x, y, width=5, height=5):
  """
  Evolve a single square in the state and return the new square.

  """
  neighbours = adjacent_bugs(state, x, y, width, height)
  if state[y][x] == "#":
    if neighbours == 1:
      return "#"
    else:
      return "."
  else:
    if neighbours == 1 or neighbours == 2:
      return "#"
    else:
      return "."


def evolve(state):
  """
  Evolve the current state according to the following rules:
    - Bug (#) dies unless exactly one bug next to it.
    - Empty square (.) with one or two adjacent bugs get populated.

  """
  return tuple(tuple(evolve_square(state, x, y) for x in range(len(line)))
               for y, line in enumerate(state))


def rating(state):
  """
  Generate the biodiverysity rating for a state.

  """
  pows = []
  for y, line in enumerate(state):
    for x, sq in enumerate(line):
      if sq == "#":
        pows.append(y * len(line) + x)

  return sum(2 ** pow for pow in pows)


def solve_a(inp):
  init_state = tuple(tuple(line) for line in inp.split("\n"))

  states = set()
  new_state = evolve(init_state)
  while new_state not in states:
    states.add(new_state)
    new_state = evolve(new_state)

  print_state(new_state)
  print(f"Rating: {rating(new_state)}")


def is_bug(tile, layer):
  """
  True if the tile is a bug in the given layer.
  
  """
  return layer[tile[1]][tile[0]] == "#"


def count_bugs(layer):
  """
  Return the number of bugs in the given layer.

  """
  return sum(1 for y in range(HEIGHT) for x in range(WIDTH) if layer[y][x] == "#")


def adjacent_bugs_layered(tile, layer, inner, outer):
  """
  Get the number of adjacent bugs over all layers.

  """
  flat_count = sum(1 for neighbour in ADJACENT_SAME[tile]
                   if is_bug(neighbour, layer))

  if inner is not None and tile in ADJACENT_INNER:
    inner_count = sum(1 for neighbour in ADJACENT_INNER[tile]
                      if is_bug(neighbour, inner))
  else:
    inner_count = 0

  if outer is not None and tile in ADJACENT_OUTER:
    outer_count = sum(1 for neighbour in ADJACENT_OUTER[tile]
                      if is_bug(neighbour, outer))
  else:
    outer_count = 0

  return flat_count + inner_count + outer_count


def evolve_tile_layered(tile, layer, inner, outer):
  """
  Evolve a single tile in a layered map.
  
  """
  if tile == (2, 2):
    # Ignore the centre square.
    return "?"

  neighbours = adjacent_bugs_layered(tile, layer, inner, outer)
  if is_bug(tile, layer):
    if neighbours == 1:
      return "#"
    else:
      return "."
  else:
    if neighbours == 1 or neighbours == 2:
      return "#"
    else:
      return "."


def evolve_layer(layer, inner, outer):
  """
  Evolve a whole layer.
  
  """
  return tuple(
    tuple(evolve_tile_layered((x, y), layer, inner, outer)
          for x in range(WIDTH))
    for y in range(HEIGHT)
  )


def evolve_all_layers(layers):
  new_layers = collections.defaultdict(lambda: EMPTY_LAYER)

  # Evolve all layers that exist, and layers +/- one level from the existing layers,
  # assuming at least one relevant layer has at least one bug. 
  min_depth = min(layers)
  max_depth = max(layers)
  for depth in range(min_depth - 1, max_depth + 2):
    layer = layers[depth]
    inner = layers[depth + 1]
    outer = layers[depth - 1]

    if count_bugs(layer) + count_bugs(inner) + count_bugs(outer) == 0:
      continue

    new_layers[depth] = evolve_layer(layer, inner, outer)

  return new_layers


def solve_b(inp):
  layers = collections.defaultdict(lambda: EMPTY_LAYER)
  layers[0] = tuple(tuple(line) for line in inp.split("\n"))

  for i in range(200):
    layers = evolve_all_layers(layers)

  # Find number of bugs present.
  num_bugs = sum(count_bugs(layer) for layer in layers.values())
  print(f"Total bugs after 200 minutes with layers: {num_bugs}")


def print_state(state):
  for line in state:
    for c in line:
      print(c, end="")
    print()


TEST_INPUT = """....#
#..#.
#..##
..#..
#...."""


def test_a():
  state = tuple(tuple(line) for line in TEST_INPUT.split("\n"))
  for i in range(5):
    print(f"State after {i} evolutions")
    print_state(state)
    state = evolve(state)
    print()


def test_b():
  layers = collections.defaultdict(lambda: EMPTY_LAYER)
  layers[0] = tuple(tuple(line) for line in TEST_INPUT.split("\n"))

  for i in range(10):
    layers = evolve_all_layers(layers)

  for i in range(-5, 6):
    print(f"Layer {i}:")
    print_state(layers[i])
    print()

def run():
  #test_a()
  #test_b()
  solve_a(utils.load_input(24))
  solve_b(utils.load_input(24))