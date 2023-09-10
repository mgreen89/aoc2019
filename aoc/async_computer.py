import dataclasses
import enum
import queue
import threading
from typing import *


class ComputerError(Exception):
  """
  Base class for computer error exceptions.

  """


class InvalidOpCode(ComputerError):
  """
  Exception raised when computer encounters invalid opcode.

  """
  pass


class InvalidMemoryMode(ComputerError):
  """
  Exception raised when computer hits an invalid memory mode.

  """
  pass


class InvalidAddress(ComputerError):
  """
  Exception raised when computer tries to use invalid memory address.

  """
  pass


class ProgramFinished(Exception):
  """
  Exception raised when program has finished successfully.

  """
  pass


@dataclasses.dataclass
class Operation:
  code: int
  name: str
  params: int


OPERATIONS = {
  1: Operation(1, "add", 3),
  2: Operation(2, "multiply", 3),
  3: Operation(3, "input", 1),
  4: Operation(4, "output", 1),
  5: Operation(5, "jump-if-true", 2),
  6: Operation(6, "jump-if-false", 2),
  7: Operation(7, "less-than", 3),
  8: Operation(8, "equals", 3),
  9: Operation(9, "adjust-rel-base", 1),
  99: Operation(99, "exit", 0),
}


class Computer:
  """
  Intcode computer.

  """
  MEMSIZE = 2 ** 16

  def __init__(self, memory: Optional[List[int]] = None, input_queue=None, output_queue=None):
    self.reset()
    self.init_memory(memory)

    if input_queue is not None:
      self.input_queue = input_queue
    else:
      self.input_queue = queue.Queue()
    
    if output_queue is not None:
      self.output_queue = output_queue
    else:
      self.output_queue = queue.Queue()

    self.finished_event = threading.Event()

  def reset(self):
    self.ip = 0
    self.rel_base = 0

  def init_memory(self, memory: Optional[List[int]] = None):
    self.memory = [0] * self.MEMSIZE
    if memory is not None:
      assert len(memory) < self.MEMSIZE
      self.memory[:len(memory)] = memory[:]

  def init_memory_from_string(self, memory: str):
    int_mem = [int(x) for x in memory.split(",")]
    self.init_memory(int_mem)

  def send(self, value: int, block=True, timeout=None):
    """
    Send a value into the computer.

    """
    self.input_queue.put(value, block=block, timeout=timeout)

  def get(self, block=True, timeout=None) -> int:
    """
    Get an output value from the computer.
    
    """
    return self.output_queue.get(block=block, timeout=timeout)

  @staticmethod
  def opdata_to_opcode(opdata):
      return opdata % 100

  @staticmethod
  def get_memory_mode(opdata, position):
    return (opdata // 10 ** (position + 1)) % 10

  def get_param_val(self, opdata, param_pos, param, input_param=True):
    memory_mode = self.get_memory_mode(opdata, param_pos)

    if memory_mode == 0:
      # Position mode.
      addr = param

    elif memory_mode == 1:
      # Immediate mode.
      return param

    elif memory_mode == 2:
      # Relative mode.
      addr = param + self.rel_base

    else:
      # Invalid mode.
      raise InvalidMemoryMode(memory_mode, opdata, param)
    
    if addr < 0:
      raise InvalidAddress("Address negative", addr)

    try:
      if input_param:
        return self.memory[addr]
      else:
        return addr
    except KeyError:
      raise InvalidAddress("Address out of range", addr)

  def step(self):
    opdata = self.memory[self.ip]
    op = OPERATIONS[self.opdata_to_opcode(opdata)]
    params = [self.memory[self.ip + i + 1] for i in range(op.params)]

    #print(opdata, params)

    if op.code == 1:
      # Add
      output_addr = self.get_param_val(opdata, 3, params[2], input_param=False)
      self.memory[output_addr] = (
        self.get_param_val(opdata, 1, params[0]) +
        self.get_param_val(opdata, 2, params[1]))

    elif op.code == 2:
      # Multiply
      output_addr = self.get_param_val(opdata, 3, params[2], input_param=False)
      self.memory[output_addr] = (
        self.get_param_val(opdata, 1, params[0]) *
        self.get_param_val(opdata, 2, params[1]))

    elif op.code == 3:
      # Input
      output_addr = self.get_param_val(opdata, 1, params[0], input_param=False)
      self.memory[output_addr] = self.input_queue.get()
      self.input_queue.task_done()

    elif op.code == 4:
      # Output
      output_val = self.get_param_val(opdata, 1, params[0])
      self.output_queue.put(output_val)
  
    elif op.code == 5:
      # Jump if true
      if self.get_param_val(opdata, 1, params[0]) != 0:
        self.ip = self.get_param_val(opdata, 2, params[1])
        # Don't increment IP
        return

    elif op.code == 6:
      # Jump if false
      if self.get_param_val(opdata, 1, params[0]) == 0:
        self.ip = self.get_param_val(opdata, 2, params[1])
        # Don't increment IP
        return

    elif op.code == 7:
      # Less than
      output_addr = self.get_param_val(opdata, 3, params[2], input_param=False)
      if self.get_param_val(opdata, 1, params[0]) < self.get_param_val(opdata, 2, params[1]):
        self.memory[output_addr] = 1
      else:
        self.memory[output_addr] = 0

    elif op.code == 8:
      # Equals
      output_addr = self.get_param_val(opdata, 3, params[2], input_param=False)
      if self.get_param_val(opdata, 1, params[0]) == self.get_param_val(opdata, 2, params[1]):
        self.memory[output_addr] = 1
      else:
        self.memory[output_addr] = 0

    elif op.code == 9:
      # Change relative base.
      self.rel_base += self.get_param_val(opdata, 1, params[0])
      assert self.rel_base >= 0

    elif op.code == 99:
      # Abort
      self.finished_event.set()
      raise ProgramFinished()

    else:
      raise InvalidOpCode("Invalid op code: {}".format(op.code))

    self.ip += 1 + op.params

  def run(self):
    try:
      while True:
        self.step()

    except ProgramFinished:
      pass

    except InvalidOpCode as e:
      print(str(e))

  def run_async(self):
    run_thread = threading.Thread(target=self.run)
    run_thread.start()