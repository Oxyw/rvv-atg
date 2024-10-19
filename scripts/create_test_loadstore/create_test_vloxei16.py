import logging
import os
from scripts.create_test_loadstore.create_test_common import generate_macros_vlxei, generate_tests_vlxei
from scripts.test_common_info import *
import re

instr = 'vloxei16'


def create_empty_test_vloxei16(xlen, vlen, vsew, lmul, vta, vma, output_dir):
    logging.info("Creating empty test for {}".format(instr))

    path = "%s/%s_empty.S" % (output_dir, instr)
    f = open(path, "w+")

    # Common header files
    print_common_header(instr, f)

    # Common const information

    # Load const information
    print_load_ending(f, 16, print_idx = True)

    f.close()
    os.system("cp %s %s" % (path, output_dir))

    logging.info(
        "Creating empty test for {}: finish in {}!".format(instr, path))

    return path


def create_first_test_vloxei16(xlen, vlen, vsew, lmul, vta, vma, output_dir, rpt_path):
    logging.info("Creating first test for {}".format(instr))

    path = "%s/%s_first.S" % (output_dir, instr)
    f = open(path, "w+")

    # Common header files
    print_common_header(instr, f)

    # Extract operands
    rs1_val, rs2_val = extract_operands(f, rpt_path)

    # Generate macros to test diffrent register
    generate_macros_vlxei(f, lmul, vsew, 16)

    # Generate tests
    n = generate_tests_vlxei(f, instr, rs1_val, rs2_val, lmul, vsew, 16)

    # Common const information

    # Load const information
    print_load_ending(f, 16, n, print_idx = True)

    f.close()
    os.system("cp %s %s" % (path, output_dir))

    logging.info(
        "Creating first test for {}: finish in {}!".format(instr, path))

    return path