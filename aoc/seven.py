import itertools
import queue

from . import async_computer
from . import computer
from . import utils


def try_with_input(input1, input2, memory):
  c = computer.Computer(memory)

  input_fn_called_count = 0
  def input_fn():
    nonlocal input_fn_called_count
    if input_fn_called_count == 0:
      input_fn_called_count += 1
      return input1
    else:
      return input2

  output = None
  def output_fn(out):
    nonlocal output
    output = out

  c.run(input_fn, output_fn)

  return output


def solve_a(inp):
  base_mem = [int(x) for x in inp.split(",")]

  perms = itertools.permutations([0, 1, 2, 3, 4])
  max_amplification = 0
  for perm in perms:
    last_output = 0
    for phase in perm:
      last_output = try_with_input(phase, last_output, base_mem)

    if last_output > max_amplification:
      max_amplification = last_output
  
  print(max_amplification)


def try_with_phases(base_mem, phases):
  # Set up the computers and queues such that each output leads into
  # the next input.
  queues = [queue.Queue() for i in range(5)]
  computers = [
    async_computer.Computer(
      base_mem,
      input_queue=queues[i],
      output_queue=queues[(i+1) % 5]
    )
    for i in range(5)
  ]

  # Put the initial phases into each queue.
  for i, phase in enumerate(phases):
    queues[i].put(phase)

  # Put zero into the first queue as initialization.
  queues[0].put(0)

  # Run all the computers until they end.
  for computer in computers:
    computer.run_async()

  for computer in computers:
    computer.finished_event.wait()

  # Read the output from the final queue and return it.
  return queues[0].get_nowait()


def solve_b(inp):
  base_mem = [int(x) for x in inp.split(",")]

  perms = itertools.permutations([5, 6, 7, 8, 9])
  max_output = 0
  for phases in perms:
    output = try_with_phases(base_mem, phases)
    max_output = max(output, max_output)
  
  print(max_output)
  

def run():
  #solve_a(utils.load_input(7))
  solve_b(utils.load_input(7))