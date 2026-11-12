"""T-00 smoke test: proves Icarus + cocotb run in the workspace."""
import cocotb
from cocotb.clock import Clock
from cocotb.triggers import ClockCycles, RisingEdge


@cocotb.test()
async def counts_and_wraps(dut):
    width = len(dut.count)
    cocotb.start_soon(Clock(dut.clk, 10, unit="ns").start())
    dut.en.value = 0
    dut.rst_n.value = 0
    await ClockCycles(dut.clk, 2)
    dut.rst_n.value = 1
    await RisingEdge(dut.clk)
    assert int(dut.count.value) == 0, "count not zero after reset"

    dut.en.value = 1
    n = (1 << width) + 5          # run past wrap-around
    await ClockCycles(dut.clk, n)
    dut.en.value = 0
    await RisingEdge(dut.clk)
    assert int(dut.count.value) == n % (1 << width), f"got {int(dut.count.value)}"
