import itertools

from . import utils


BASE_PATTERN = (0, 1, 0, -1)


def _gen_pattern_internal(n):
  for i in itertools.cycle(BASE_PATTERN):
    for _ in range(n + 1):
      yield i

def gen_pattern(n):
  gen = _gen_pattern_internal(n)
  next(gen)
  yield from gen


def combine(ns, pattern):
  return int(str(sum(n * p for (n, p) in zip(ns, pattern)))[-1])


def solve_a(inp):
  # Convert the input into a list of integers.
  ns = [int(x) for x in inp]

  for i in range(100):
    ns = [combine(ns, gen_pattern(j)) for j in range(len(ns))]

  print("".join(str(n) for n in ns[:8]))


def solve_b(inp):
  # Length of input.
  msg_size = len(inp) * 10_000

  # Only need the last 550000 numbers.
  # Let's do 650000 for good measure, it's 1000 times the input.
  big_inp = []
  for i in range(1000):
    for j in inp:
      big_inp.append(int(j))
  big_inp = big_inp[::-1]
  portion_size = len(inp) * 1000

  print("Processing")

  for i in range(100):
    print(i)
    for j in range(1, len(big_inp)):
      big_inp[j] = (big_inp[j - 1] + big_inp[j]) % 10

  # Flip the input back into the right order.
  big_inp = big_inp[::-1]

  # Read the 8-character message from the input.
  msg_index = int(inp[:7]) - (msg_size - portion_size)

  print(big_inp[msg_index:msg_index + 8])


def test():
  s = "12345678"
  ns = [int(x) for x in s]
  for i in range(4):
    ns = [combine(ns, gen_pattern(j)) for j in range(len(ns))]
    
    print("".join(str(n) for n in ns))

  ss = {
    "80871224585914546619083218645595": "24176176",
    "19617804207202209144916044189917": "73745418",
    "69317163492948606335995924319873": "52432133",
  }

  for s in ss:
    ns = [int(x) for x in s]

    for i in range(100):
      ns = [combine(ns, gen_pattern(j)) for j in range(len(ns))]
    
    print("".join(str(n) for n in ns))


def run():
  #test()
  #solve_a(utils.load_input(16))
  solve_b(utils.load_input(16))