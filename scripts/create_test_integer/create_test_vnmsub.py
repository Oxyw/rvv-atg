import logging
import os
from scripts.test_common_info import *
from scripts.create_test_integer.create_test_common import  generate_macros_muladd, generate_tests_muladd
import re

instr = 'vnmsub'


def create_empty_test_vnmsub(xlen, vlen, vsew, lmul, vta, vma, output_dir):
    logging.info("Creating empty test for {}".format(instr))

    path = "%s/%s_empty.S" % (output_dir, instr)
    f = open(path, "w+")

    # Common header files
    print_common_header(instr, f)

    

    # Common const information
    print_common_ending(f)

    f.close()
    os.system("cp %s %s" % (path, output_dir))

    logging.info(
        "Creating empty test for {}: finish in {}!".format(instr, path))

    return path


def create_first_test_vnmsub(xlen, vlen, vsew, lmul, vta, vma, output_dir, rpt_path):
    logging.info("Creating first test for {}".format(instr))

    path = "%s/%s_first.S" % (output_dir, instr)
    f = open(path, "w+")

    # Common header files
    print_common_header(instr, f)

    # Extract operands
    rs1_val, rs2_val = extract_operands(f, rpt_path)

    # Generate macros to test diffrent register
    generate_macros_muladd(f, lmul)

    # Generate tests
    vv_num_tests = generate_tests_muladd(instr, f, rs1_val, rs2_val, lmul)

    # Common const information
    print_common_ending_rs1rs2rd(rs1_val, rs2_val, vv_num_tests, vsew, f)

    f.close()
    os.system("cp %s %s" % (path, output_dir))

    logging.info(
        "Creating first test for {}: finish in {}!".format(instr, path))

    return path
