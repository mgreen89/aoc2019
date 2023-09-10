from typing import Optional


__all__ = (
  "load_input"
)


def load_input(number: int, part: Optional[str] = None):
  """
  Load the input for a particular puzzle.

  """
  filename = "aoc/inputs/{}{}.txt".format(
    number, part if part is not None else "")

  with open(filename) as f:
    return f.read()