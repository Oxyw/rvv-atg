import logging
import os
from scripts.create_test_loadstore.create_test_common import generate_macros_vsxsegei, generate_tests_vsxsegei
from scripts.test_common_info import *
import re

instr = 'vsoxsegei8' # vsoxseg<nf>ei8


def create_empty_test_vsoxsegei8(xlen, vlen, vsew, lmul, vta, vma, output_dir):
    logging.info("Creating empty test for {}".format(instr))

    path = "%s/%s_empty.S" % (output_dir, instr)
    f = open(path, "w+")

    # Common header files
    print_common_header(instr, f)

    # Common const information

    # Load const information
    print_load_ending(f, 8, print_idx = True)

    f.close()
    os.system("cp %s %s" % (path, output_dir))

    logging.info(
        "Creating empty test for {}: finish in {}!".format(instr, path))

    return path


def create_first_test_vsoxsegei8(xlen, vlen, vsew, lmul, vta, vma, output_dir, rpt_path):
    logging.info("Creating first test for {}".format(instr))

    path = "%s/%s_first.S" % (output_dir, instr)
    f = open(path, "w+")

    # Common header files
    print_common_header(instr, f)

    # Extract operands
    rs1_val, rs2_val = extract_operands(f, rpt_path)

    # Generate macros to test diffrent register
    generate_macros_vsxsegei(f, lmul, vsew, 8)

    # Generate tests
    (n, rnd) = generate_tests_vsxsegei(f, 'vsoxseg', 'vluxseg', rs1_val, rs2_val, lmul, vsew, 8)

    # Common const information

    # Load const information
    print_load_ending(f, 8, n, print_idx = True, seg = rnd)

    f.close()
    os.system("cp %s %s" % (path, output_dir))

    logging.info(
        "Creating first test for {}: finish in {}!".format(instr, path))

    return path