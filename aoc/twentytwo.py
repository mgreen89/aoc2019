from . import utils


def shuffle(deck, inp):
  for l in inp.split("\n"):
    if l.startswith("deal into"):
      deck.reverse()

    elif l.startswith("deal with inc"):
      i = int(l[len("deal with increment "):])
      ndeck = [0] * len(deck)
      for j in range(len(deck)):
        ndeck[(i * j) % len(deck)] = deck[j]
      deck = ndeck

    elif l.startswith("cut"):
      i = int(l[len("cut "):])
      deck = deck[i:] + deck[:i]

    else:
      assert False, "Unknown rule"

  return deck


def solve_a(inp):
  deck_size = 10007
  deck = list(range(deck_size))
  deck = shuffle(deck, inp)
  print(deck.index(2019))


def gen_poly(deck_size, inp):
  # Convert the rules to linear polynomials of the form 
  # y = ax + b.
  # These can be combined to form a single polynomical for
  # the whole shuffle (for a single position).

  a = 1
  b = 0

  # Parse rules in reverse order (i.e. innermost first).
  for l in inp.split("\n")[::-1]:
    if l.startswith("deal into"):
      # Invert the whole polynomial
      a = -a
      b = deck_size - b - 1

    elif l.startswith("deal with inc"):
      # modinv(i, deck_size)
      i = int(l[len("deal with increment "):])

      # Fermat's little theorem
      # For any prime p, a^p = a mod p
      z = pow(i, deck_size - 2, deck_size)

      a = (a * z) % deck_size
      b = (b * z) % deck_size

    elif l.startswith("cut"):
      # Add to b
      i = int(l[len("cut "):])
      b = (b + i) % deck_size

    else:
      assert False, "Unknown rule"

  return a, b


def polypow(a, b, power, mod):
  """
  Raise a polynomial to a power with a modulus.

  """
  if power == 0:
    # End of polypow, return unchanged.
    return 1, 0

  if power % 2 == 0:
    # f^2(x) = f(f(x)) = a(ax+b) + b
    # therefore a -> a^2, b -> ab + b
    return polypow((a * a) % mod, (a * b + b) % mod, power // 2, mod)

  else:
    # Odd power.
    # f(g(x)) = a(cx + d) + b
    # therefore a -> ac, b -> ad + b
    # where g(x) = cx + d
    c, d = polypow(a, b, power - 1, mod)
    return (a * c) % mod, (a * d + b) % mod


def unshuffle(deck_size, iterations, position, inp):
  a, b = gen_poly(deck_size, inp)
  x, y = polypow(a, b, iterations, deck_size)

  return (position * x + y) % deck_size


def solve_b(inp):
  deck_size = 119315717514047
  iterations = 101741582076661
  position = 2020

  print(unshuffle(deck_size, iterations, position, inp))


def test(inp):
  pos = 2020
  deck_size = 10007
  iterations = 10
  deck = list(range(deck_size))
  for i in range(iterations):
    deck = shuffle(deck, inp)
  print(deck[pos])
  print(unshuffle(deck_size, iterations, pos, inp))

def run():
  #test(utils.load_input(22))
  solve_a(utils.load_input(22))
  solve_b(utils.load_input(22))