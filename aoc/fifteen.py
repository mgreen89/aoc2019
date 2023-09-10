import dataclasses
import enum

from . import async_computer
from . import utils


# Move orders
class Move(enum.Enum):
  North = 1
  South = 2
  West = 3
  East = 4

  @property
  def opposite(self):
    if self is Move.North:
      return Move.South
    elif self is Move.South:
      return Move.North
    elif self is Move.West:
      return Move.East
    elif self is Move.East:
      return Move.West
    else:
      assert False

# Statuses
class Status(enum.Enum):
  HitWall = 0
  Moved = 1
  O2Location = 2


@dataclasses.dataclass(eq=True, frozen=True)
class Pos:
  x: int
  y: int

  def move(self, m: Move):
    if m is Move.North:
      return Pos(self.x, self.y + 1)

    elif m is Move.South:
      return Pos(self.x, self.y - 1)

    elif m is Move.West:
      return Pos(self.x - 1, self.y)

    elif m is Move.East:
      return Pos(self.x + 1, self.y)

    else:
      assert False
  

def explore(c, pos, history, shortest_paths, o2_location):
  #print(pos)
  for move in Move:
    shortest = shortest_paths.get(pos.move(move))
    if shortest is not None:
      # If the square has already been visited by a shorter route,
      # skip over this possible move.
      if len(history) + 1 > len(shortest):
        continue

    # Check if move is possible.
    c.send(move.value)
    status = Status(c.get())

    if status is Status.HitWall:
      # Abandon this path.
      #print("Hit wall")
      continue

    else:
      # Add this path into the history and shortest paths, and iterate.
      new_pos = pos.move(move)
      history.append(move)
      shortest_paths[new_pos] = tuple(history)
      #print("Moved {}".format(move.name))

      if o2_location is None and status is Status.O2Location:
        #print(f"O2 location: {new_pos}")
        o2_location = new_pos

      # Recurse
      o2_location = explore(c, new_pos, history, shortest_paths, o2_location)

  #print(f"Back at pos {pos}")

  # Pop off the last move.
  try:
    move = history.pop()

    # Move the robot back by doing the opposite move.
    #print("########## sending opposite move {}".format(move.opposite))
    c.send(move.opposite.value)
    c.get()
  except IndexError:
    # Must be first move.
    #assert pos == Pos(0, 0)
    pass

  return o2_location


def solve_a(inp):
  intcode = [int(x) for x in inp.split(",")]

  c = async_computer.Computer()
  c.init_memory_from_string(inp)
  c.run_async()

  pos = Pos(0, 0)
  history = []
  shortest_paths = {Pos(0, 0): ()}

  o2_location = explore(c, pos, history, shortest_paths, None)

  print(len(shortest_paths[o2_location]))
  
  return len(shortest_paths[o2_location])


def print_map(shortest_paths, o2_location):
  min_y = min(p.y for p in shortest_paths) + 1
  max_y = max(p.y for p in shortest_paths) + 1
  min_x = min(p.x for p in shortest_paths) + 1
  max_x = max(p.x for p in shortest_paths) + 1

  for y in range(max_y + 1, min_y - 2, -1):
    for x in range(min_x - 1, max_x + 2, 1):
      if Pos(x,y) == o2_location:
        print("@")
      elif Pos(x,y) in shortest_paths:
        print(" ", end="")
      else:
        print("#", end="")
    print()


def solve_b(inp):
  intcode = [int(x) for x in inp.split(",")]

  c = async_computer.Computer()
  c.init_memory_from_string(inp)
  c.run_async()

  pos = Pos(0, 0)
  history = []
  shortest_paths = {Pos(0, 0): ()}

  o2_location = explore(c, pos, history, shortest_paths, None)

  # Move the robot to the oxygen machine.
  for move in shortest_paths[o2_location]:
    c.send(move.value)
    status = Status(c.get())
    assert status in (Status.Moved, Status.O2Location)
  assert status is Status.O2Location

  # Re-explore the whole map from this new starting point.
  pos = o2_location
  history = []
  shortest_paths = {o2_location: ()}
  _ = explore(c, pos, history, shortest_paths, o2_location)

  # Find the square with the maximum path from the o2 generator.
  print(max(len(steps) for pos, steps in shortest_paths.items()))


def run():
  #solve_a(utils.load_input(15))
  solve_b(utils.load_input(15))