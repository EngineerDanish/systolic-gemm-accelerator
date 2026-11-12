# mosa-rtl

Standalone SystemVerilog implementation of the MOSA paper ("High-Performance Gemmini-Based Matrix Multiplication Accelerator for Deep Learning Workloads"). Gemmini (github.com/ucb-bar/gemmini) is used as a reference only.

## Layout
- rtl/    synthesizable SystemVerilog
- tb/     cocotb testbenches (one folder per block)
- model/  Python/NumPy bit-accurate golden models and test vectors
- synth/  Vivado Tcl scripts (run on the host laptop) and report notes
- docs/   ticket handoffs, notes, paper extraction

## Toolchain (verified in T-00)
Python 3, NumPy, cocotb 2.x, Icarus Verilog 12 (-g2012), Verilator 5 for lint.

## Run the smoke test
    cd tb/smoke && make
    verilator --lint-only -Wall rtl/smoke_counter.sv
