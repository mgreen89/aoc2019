from . import utils


class Body:
  all = {}

  def __new__(cls, name, *args, **kwargs):
    assert name not in cls.all, "Two bodies with same name! {}".format(name)
    inst = super().__new__(cls)
    cls.all[name] = inst
    return inst

  def __init__(self, name):
    self.name = name
    self.parent = None
    self.children = []

  def add_child(self, child):
    assert child is not None
    self.children.append(child)
    child.parent = self

  @property
  def total_orbits(self):
    if self.parent is None:
      return 0
    return self.parent.total_orbits + 1


def solve_a(inp):
  com = Body("COM")

  for line in inp.split("\n"):
    p_name, c_name = line.split(")")

    p_body = Body.all.get(p_name)
    if p_body is None:
      p_body = Body(p_name)

    c_body = Body.all.get(c_name)
    if c_body is None:
      c_body = Body(c_name)

    p_body.add_child(c_body)      
  
  total = sum(b.total_orbits for b in Body.all.values())
  print(total)


def solve_b(inp):
  # Must be run after part a.

  you = Body.all["YOU"]
  santa = Body.all["SAN"]

  # Find the common ancestor by finding all ancestors, and finding the first
  # one in common.
  you_ancestors = []
  curr = you.parent
  while curr is not None:
    you_ancestors.append(curr)
    curr = curr.parent

  santa_ancestors = []
  curr = santa.parent
  while curr is not None:
    santa_ancestors.append(curr)
    curr = curr.parent

  common_ancestor = None
  for sa in santa_ancestors:
    if sa in you_ancestors:
      common_ancestor = sa
      break

  hops = (you_ancestors.index(common_ancestor) +
          santa_ancestors.index(common_ancestor))
  print(hops)


def run():
  solve_a(utils.load_input(6))
  solve_b(utils.load_input(6))