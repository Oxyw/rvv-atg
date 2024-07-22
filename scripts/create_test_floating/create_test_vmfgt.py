import logging
import os
from scripts.create_test_floating.create_test_common import generate_macros_compare, generate_tests_compare, print_ending
from scripts.test_common_info import *
import re

instr = 'vmfgt'


def create_empty_test_vmfgt(xlen, vlen, vsew, lmul, vta, vma, output_dir):
    logging.info("Creating empty test for {}".format(instr))

    path = "%s/%s_empty.S" % (output_dir, instr)
    f = open(path, "w+")

    # Common header files
    print_common_header(instr, f)


    # Common const information
    print_ending(f)

    f.close()
    os.system("cp %s %s" % (path, output_dir))

    logging.info(
        "Creating empty test for {}: finish in {}!".format(instr, path))

    return path


def create_first_test_vmfgt(xlen, vlen, vsew, lmul, vta, vma, output_dir, rpt_path):
    logging.info("Creating first test for {}".format(instr))

    path = "%s/%s_first.S" % (output_dir, instr)
    f = open(path, "w+")

    # Common header files
    print_common_header(instr, f)

    # Extract operands
    rs1_val, rs2_val = extract_operands_fp(f, rpt_path)

    # Generate macros to test diffrent register
    generate_macros_compare(f, lmul, test_vv = False)

    # Generate macros to test diffrent register
    num_tests_tuple = generate_tests_compare(instr, f, lmul, rs1_val, rs2_val, test_vv = False)

    # Common const information
    print_common_ending_rs1rs2rd(rs1_val, rs2_val, num_tests_tuple, vsew, f, is_mask = True)

    f.close()
    os.system("cp %s %s" % (path, output_dir))

    logging.info(
        "Creating first test for {}: finish in {}!".format(instr, path))

    return path
