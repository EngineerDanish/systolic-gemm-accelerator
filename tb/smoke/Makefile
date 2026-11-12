SIM ?= icarus
TOPLEVEL_LANG = verilog
VERILOG_SOURCES = $(PWD)/../../rtl/smoke_counter.sv
COMPILE_ARGS += -g2012
TOPLEVEL = smoke_counter
COCOTB_TEST_MODULES = test_smoke_counter
include $(shell cocotb-config --makefiles)/Makefile.sim
