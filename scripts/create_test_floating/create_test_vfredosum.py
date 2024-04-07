import logging
import os
from scripts.test_common_info import *
from scripts.create_test_floating.create_test_common import generate_macros_vfred, generate_tests_vfred, print_ending

instr = 'vfredosum'


def create_empty_test_vfredosum(xlen, vlen, vsew, lmul, vta, vma, output_dir):
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


def create_first_test_vfredosum(xlen, vlen, vsew, lmul, vta, vma, output_dir, rpt_path):
    logging.info("Creating first test for {}".format(instr))

    path = "%s/%s_first.S" % (output_dir, instr)
    f = open(path, "w+")

    # Common header files
    print_common_header(instr, f)

    # Extract operands
    rs1_val, rs2_val = extract_operands_fp(f, rpt_path)

    # Generate macros to test diffrent register
    generate_macros_vfred(f, vsew, lmul, test_vv = True, test_vf = False)

    # Generate tests
    n = generate_tests_vfred(instr, f, vsew, lmul, rs1_val, rs2_val, suffix="vs", test_vv = True, test_vf = False)

    # Common const information
    print_ending(f, generate_data = True, rs1_val = rs1_val, rs2_val = rs2_val, test_tuples=(0,n,0))

    f.close()
    os.system("cp %s %s" % (path, output_dir))

    logging.info(
        "Creating first test for {}: finish in {}!".format(instr, path))

    return path
