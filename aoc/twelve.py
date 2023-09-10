import itertools
import re

from . import utils


class Moon:
  def __init__(self, x, y, z):
    self.x = x
    self.y = y
    self.z = z

    self.vx = 0
    self.vy = 0
    self.vz = 0

  def apply_gravity(self, other):
    if self.x > other.x:
      self.vx -= 1
      other.vx += 1
    elif self.x < other.x:
      self.vx += 1
      other.vx -= 1

    if self.y > other.y:
      self.vy -= 1
      other.vy += 1
    elif self.y < other.y:
      self.vy += 1
      other.vy -= 1

    if self.z > other.z:
      self.vz -= 1
      other.vz += 1
    elif self.z < other.z:
      self.vz += 1
      other.vz -= 1

  def apply_velocity(self):
    self.x += self.vx
    self.y += self.vy
    self.z += self.vz
    
  @property
  def potential_energy(self):
    return abs(self.x) + abs(self.y) + abs(self.z)

  @property
  def kinetic_energy(self):
    return abs(self.vx) + abs(self.vy) + abs(self.vz)

  @property
  def total_energy(self):
    return self.potential_energy * self.kinetic_energy

  @property
  def pos(self):
    return (self.x, self.y, self.z)

  @property
  def vel(self):
    return (self.vx, self.vy, self.vz)

  @property
  def posstr(self):
    return "pos=<x={:2d}, y={:2d}, z={:2d}>".format(self.pos)

  @property
  def velstr(self):
    return "vel=<x={:2d}, y={:2d}, z={:2d}>".format(self.vel)


def parse_input(inp):
  r = re.compile(r"<x=(?P<x>-?[0-9]+), y=(?P<y>-?[0-9]+), z=(?P<z>-?[0-9]+)>")

  moons = []
  for line in inp.split("\n"):
    m = r.match(line)
    assert m is not None

    moons.append(
      Moon(int(m.group("x")), int(m.group("y")), int(m.group("z"))))

  return moons


def energy_after_n(moons, n):
  moon_combs = list(itertools.combinations(moons, 2))

  for i in range(n):
    for c in moon_combs:
      c[0].apply_gravity(c[1])

    for m in moons:
      m.apply_velocity()

  return sum(m.total_energy for m in moons)


FIRST_PRIMES = (2, 3, 5, 7, 11, 13)
def gen_primes_to(n):
  for p in FIRST_PRIMES:
    if n > p:
      yield p

  primes = list(FIRST_PRIMES)
  i = FIRST_PRIMES[-1] + 2
  while i < n:
    if all(i % p != 0 for p in primes):
      yield i
      primes.append(i)
    i += 2


def find_prime_factors(n):
  curr = n
  for p in gen_primes_to(int(n ** 0.5) + 1):
    while curr % p == 0:
      yield p
      curr //= p

  if curr != 1:
    yield curr


def solve_a(inp):
  moons = parse_input(inp)
  print(energy_after_n(moons, 1000))


def solve_b(inp):
  moons = parse_input(inp)
  moon_combs = list(itertools.combinations(moons, 2))

  # Each dimension has its own periodicity, so track each one separately.

  x_states = {}
  y_states = {}
  z_states = {}
  i = 0

  x_offset = None
  y_offset = None
  z_offset = None
  x_periodicity = None
  y_periodicity = None
  z_periodicity = None
  
  while not all(p is not None for p in (x_periodicity, y_periodicity, z_periodicity)):

    curr_x_state = tuple((m.x, m.vx) for m in moons)
    curr_y_state = tuple((m.y, m.vy) for m in moons)
    curr_z_state = tuple((m.z, m.vz) for m in moons)

    if x_periodicity is None:
      if curr_x_state in x_states:
        x_offset = x_states[curr_x_state]
        x_periodicity = len(x_states) - x_offset

    if y_periodicity is None:
      if curr_y_state in y_states:
        y_offset = y_states[curr_y_state]
        y_periodicity = len(y_states) - y_offset

    if z_periodicity is None:
      if curr_z_state in z_states:
        z_offset = z_states[curr_z_state]
        z_periodicity = len(z_states) - z_offset

    x_states[curr_x_state] = i
    y_states[curr_y_state] = i
    z_states[curr_z_state] = i

    for c in moon_combs:
      c[0].apply_gravity(c[1])

    for m in moons:
      m.apply_velocity()

    i += 1

    if i % 10000 == 0:
      print(i, x_periodicity, y_periodicity, z_periodicity)

  print(x_periodicity)
  print(y_periodicity)
  print(z_periodicity)

  x_pfs = list(find_prime_factors(x_periodicity))
  y_pfs = list(find_prime_factors(y_periodicity))
  z_pfs = list(find_prime_factors(z_periodicity))

  lcm_pfs = {}
  for pf in itertools.chain(x_pfs, y_pfs, z_pfs):
    lcm_pfs[pf] = max(x_pfs.count(pf), y_pfs.count(pf), z_pfs.count(pf))

  lcm = 1
  for pf, count in lcm_pfs.items():
    lcm *= (pf ** count)
  print(lcm)


def solve_b_manual(x_periodicity, y_periodicity, z_periodicity):
  x_pfs = list(find_prime_factors(x_periodicity))
  y_pfs = list(find_prime_factors(y_periodicity))
  z_pfs = list(find_prime_factors(z_periodicity))

  print(x_pfs)
  print(y_pfs)
  print(z_pfs)

  lcm_pfs = {}
  for pf in itertools.chain(x_pfs, y_pfs, z_pfs):
    lcm_pfs[pf] = max(x_pfs.count(pf), y_pfs.count(pf), z_pfs.count(pf))

  lcm = 1
  for pf, count in lcm_pfs.items():
    lcm *= (pf ** count)
  print(lcm)


def test():
  s = """<x=-1, y=0, z=2>
<x=2, y=-10, z=-7>
<x=4, y=-8, z=8>
<x=3, y=5, z=-1>"""

  moons = parse_input(s)
  print(energy_after_n(moons, 10))


def run():
  #test()
  solve_a(utils.load_input(12))
  solve_b(utils.load_input(12))
  #solve_b_manual(186028, 161428, 193052)