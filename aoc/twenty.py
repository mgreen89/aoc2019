import collections
import dataclasses
import itertools
from typing import *

from . import utils


@dataclasses.dataclass(eq=True, frozen=True)
class Tile:
  c: str
  portal: Tuple[str, bool]


def parse_input(inp):
  # Parse the input into two maps.
  maze = {}
  portals = {}

  rows = inp.split("\n")
  for y, row in enumerate(rows):
    for x, c in enumerate(row):
      maze[(x, y)] = Tile(c, None)

      if c.isupper():
        # Figure out the portal name.
        name = None
        outer = None

        if x > 0 and row[x - 1] == ".":
          # Portal name on right.
          name = c + row[x + 1]
          outer = x + 2 == len(row)
          entry = (x - 1, y)

        elif x + 1 < len(row) and row[x + 1] == ".":
          # Portal name on left.
          name = row[x - 1] + c
          outer = x - 1 == 0
          entry = (x + 1, y)

        elif y > 0 and rows[y - 1][x] == ".":
          # Portal name below.
          name = c + rows[y + 1][x]
          outer = y + 2 == len(rows)
          entry = (x, y - 1)

        elif y + 1 < len(rows) and rows[y + 1][x] == ".":
          # Portal name above.
          name = rows[y - 1][x] + c
          outer = y - 1 == 0
          entry = (x, y + 1)

        if name is not None:
          portals[(name, outer)] = entry
          maze[(x, y)] = Tile(c, (name, outer))

  return maze, portals


def bfs(maze, portals):
  # Breadth-first search.
  start = portals[("AA", True)]
  goal = portals[("ZZ", True)]

  history = collections.defaultdict(lambda: False)
  history[start] = True

  nxt = [start]
  for steps in itertools.count(1):
    if len(nxt) == 0:
      break

    current = nxt
    nxt = []
    for pos in current:
      for d in ((1,0), (-1, 0), (0, 1), (0, -1)):
        next_pos = (pos[0] + d[0], pos[1] + d[1])
        if next_pos in history or next_pos not in maze:
          # Since breadth-first search, ignore repeat positions.
          # Or areas outside the wall
          continue

        if maze[next_pos].c == "#" or maze[next_pos] == " ":
          # Ignore walls
          continue

        if next_pos == goal:
          # Done!
          return(steps)

        if maze[next_pos].c.isupper():
          # Portal - walk through it!
          portal = maze[next_pos].portal
          if portal is None:
            import pdb; pdb.set_trace()
          if portal[0] == "AA" or portal[0] == "ZZ":
            # Ignore AA and ZZ portals, they're not really portals!
            continue
          next_pos = portals[(portal[0], not portal[1])]

        history[next_pos] = True
        nxt.append(next_pos)


def solve_a(inp):
  maze, portals = parse_input(inp)

  print(bfs(maze, portals))  


def bfs_level(maze, portals):
  # Breadth-first search keeping track of levels.
  start = portals[("AA", True)] + (0, )
  goal = portals[("ZZ", True)] + (0, )

  history = collections.defaultdict(lambda: False)
  history[start] = True

  nxt = [start]
  for steps in itertools.count(1):
    if len(nxt) == 0:
      break

    current = nxt
    nxt = []
    for pos in current:
      for d in ((1,0), (-1, 0), (0, 1), (0, -1)):
        next_pos = (pos[0] + d[0], pos[1] + d[1])
        next_level = pos[2]
        next_comb = next_pos + (next_level, )
        if next_comb in history or next_pos not in maze:
          # Since breadth-first search, ignore repeat positions.
          # Or areas outside the wall
          continue

        if maze[next_pos].c == "#" or maze[next_pos] == " ":
          # Ignore walls
          continue

        if next_comb == goal:
          # Done!
          return(steps)

        if maze[next_pos].c.isupper():
          # Portal - walk through it!
          portal = maze[next_pos].portal

          if portal[0] == "AA" or portal[0] == "ZZ":
            # Ignore AA and ZZ portals, they're not really portals!
            continue

          # If the portal is inner, go a layer deeper.
          # If the portal is outer, go a layer up.
          if portal[1]:
            if next_level == 0:
              # This is actually a wall!
              continue
            next_pos = portals[(portal[0], not portal[1])]
            next_level -= 1
          else:
            if next_level > len(portals):
              # Don't need to bother with more levels than portals.
              continue
            next_pos = portals[(portal[0], not portal[1])]
            next_level += 1

        next_comb = next_pos + (next_level, )
        history[next_comb] = True
        nxt.append(next_comb)

    if steps % 1000 == 0:
      print(f"{steps} has {len(nxt)} branches in layers from {min(n[2] for n in nxt)} to {max(n[2] for n in nxt)}")
  

def solve_b(inp):
  maze, portals = parse_input(inp)
  print(bfs_level(maze, portals))


def run():
  #solve_a(utils.load_input(20))
  solve_b(utils.load_input(20)) 