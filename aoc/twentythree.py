import dataclasses
import queue
import threading
import time

from . import async_computer
from . import utils


@dataclasses.dataclass(frozen=True)
class Packet:
  dest: int
  src: int
  x: int
  y: int


class NIC(async_computer.Computer):
  # Replace the input and output instructions.

  def __init__(self, addr, *args, **kwargs):
    self.network_address = addr
    self.initialized = False
    self.packet = None
    self.output_dest = None
    self.output_x = None
    self.num_no_packets = 0
    self.idle = False
    super().__init__(*args, **kwargs)

  @property
  def is_idle(self):
    return self.input_queue.empty() and self.idle

  def step(self):
    opdata = self.memory[self.ip]
    op = async_computer.OPERATIONS[self.opdata_to_opcode(opdata)]
    params = [self.memory[self.ip + i + 1] for i in range(op.params)]

    #print(f"NIC {self.network_address} step, op {op.code}")

    if op.code == 3:
      if not self.initialized:
        # Send in the network address
        val = self.network_address
        self.initialized = True

      elif self.packet is not None:
        # Return the y-value from the packet.
        val = self.packet.y
        self.packet = None

      elif self.is_idle:
        # Wait on an item on the queue to prevent further processing.
        self.packet = self.input_queue.get()
        self.num_no_packets = 0
        self.idle = False
        self.input_queue.task_done()
        val = self.packet.x

      else:
        # Try and get a value from the queue immediately.
        try:
          self.packet = self.input_queue.get_nowait()
          self.num_no_packets = 0
          self.idle = False
          self.input_queue.task_done()
          val = self.packet.x
        except queue.Empty:
          self.num_no_packets += 1
          if self.num_no_packets > 100:
            self.idle = True
          val = -1

      output_addr = self.get_param_val(opdata, 1, params[0], input_param=False)
      self.memory[output_addr] = val
      self.ip += 1 + op.params

    elif op.code == 4:
      # Output
      self.idle = False
      output_val = self.get_param_val(opdata, 1, params[0])

      if self.output_dest is None:
        self.output_dest = output_val
      elif self.output_x is None:
        self.output_x = output_val
      else:
        self.output_queue.put(
          Packet(
            self.output_dest, self.network_address,
            self.output_x, output_val)
        )
        self.output_dest = None
        self.output_x = None

      self.ip += 1 + op.params

    else:
      super().step()


class Network:
  def __init__(self, num_endpoints, nic_intcode):
    self.fabric = queue.Queue()
    self.nics = [NIC(addr, nic_intcode, output_queue=self.fabric)
                 for addr in range(num_endpoints)]

  def run(self):
    for nic in self.nics:
      nic.run_async()


def solve_a(inp):
  intcode = [int(x) for x in inp.split(",")]

  net = Network(50, intcode)
  net.run()

  while True:
    packet = net.fabric.get()
    print(f"Got packet: {packet}")
    if packet.dest == 255:
      print("##############################################")
      print(packet)
      print("##############################################")
      break

    try:
      net.nics[packet.dest].send(packet)

    except IndexError:
      assert False, "Invalid address: {}".format(packet.dest)


class NATNetwork(Network):
  def __init__(self, *args, **kwargs):
    super().__init__(*args, **kwargs)
    self.nat_packet = None
    self.nat_history = [Packet(-1, -1, -99999, -99999)]
    self.nat_finished = threading.Event()

  def run_nat(self):
    while True:
      if all(nic.is_idle for nic in self.nics) and self.nat_packet is not None:
        self.nics[0].send(self.nat_packet)
        print(f"Sent NAT packet {self.nat_packet}")

        if self.nat_packet.y == self.nat_history[-1].y:
          print("###############")
          print(f"y = {self.nat_packet.y}")
          print("###############")
          self.nat_finished.set()
          return

        self.nat_history.append(self.nat_packet)

      time.sleep(0.2)

  def run_nat_async(self):
    run_thread = threading.Thread(target=self.run_nat)
    run_thread.start()
  

def solve_b(inp):
  intcode = [int(x) for x in inp.split(",")]

  net = NATNetwork(50, intcode)
  net.run()
  net.run_nat_async()

  while not net.nat_finished.isSet():
    packet = net.fabric.get()
    print(f"Got packet: {packet}")
    if packet.dest == 255:
      net.nat_packet = packet
      continue

    try:
      net.nics[packet.dest].send(packet)

    except IndexError:
      assert False, "Invalid address: {}".format(packet.dest)


def run():
  #solve_a(utils.load_input(23))
  solve_b(utils.load_input(23))