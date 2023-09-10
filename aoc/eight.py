from . import utils


WIDTH = 25
HEIGHT = 6


def parse_input(inp):
  image = []
  i = 0
  while i < len(inp):
    layer = []
    for row in range(HEIGHT):
      row = inp[i:i+WIDTH]
      i += WIDTH
      layer.append(row)
    image.append(layer)
  
  # Check the input was a whole number of images.
  assert i == len(inp)

  return image


def solve_a(inp):
  image = parse_input(inp)

  # Find the layer with the most zeroes.
  zero_count = [sum(row.count("0") for row in layer) for layer in image]
  min_zeroes = min(zero_count)
  min_zeroes_index = zero_count.index(min_zeroes)
  min_zeroes_layer = image[min_zeroes_index]

  # Return number of '1's multiplied by the number of '2's.
  num_ones = sum(row.count("1") for row in min_zeroes_layer)
  num_twos = sum(row.count("2") for row in min_zeroes_layer)

  print(num_ones * num_twos)


def solve_b(inp):
  image = parse_input(inp)

  # 0 - black, 1 - white, 2 transparent.
  # First layer in front, last layer at the back.
  # Therefore, for each pixel, start from the front until
  # hitting a non-transparent pixel.
  finished = [2] * WIDTH * HEIGHT

  for layer in image:
    for i, row in enumerate(layer):
      for j, pixel in enumerate(row):
        if pixel != "2" and finished[i * WIDTH + j] == 2:
          finished[i * WIDTH + j] = pixel

  for i in range(HEIGHT):
    for j in range(WIDTH):
      digit = finished[i * WIDTH + j]
      if digit == "0":
        # Black
        char = " "
      elif digit == "1":
        # White
        char = "#"
      elif digit == "2":
        # Transparent
        char = "."
      else:
        assert False
      print(char, end="")
    print()

def run():
  solve_a(utils.load_input(8))
  solve_b(utils.load_input(8))