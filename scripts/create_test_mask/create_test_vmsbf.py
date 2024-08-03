import logging
import os
from scripts.create_test_mask.create_test_common import *
from scripts.test_common_info import *
import re

instr = 'vmsbf'


def create_empty_test_vmsbf(xlen, vlen, vsew, lmul, vta, vma, output_dir):
    logging.info("Creating empty test for {}".format(instr))

    path = "%s/%s_empty.S" % (output_dir, instr)
    f = open(path, "w+")

    generate_macros_vs2(f, is_vd = True)

    # Common header files
    print_common_header(instr, f)

    n = generate_tests_vs2(instr, f, vlen, vsew, lmul, is_vd = True)

    # Common const information
    print_ending_common(vlen, vsew, lmul, f, n)

    f.close()

    logging.info(
        "Creating empty test for {}: finish in {}!".format(instr, path))

    return path
