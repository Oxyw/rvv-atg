import logging
import os
from scripts.create_test_loadstore.create_test_common import generate_macros_vlre, generate_tests_vlre
from scripts.test_common_info import *

instr = 'vlre8' # vl<nf>re8


def create_empty_test_vlre8(xlen, vlen, vsew, lmul, vta, vma, output_dir):
    logging.info("Creating empty test for {}".format(instr))

    path = "%s/%s_empty.S" % (output_dir, instr)
    f = open(path, "w+")

    # Common header files
    print_common_header(instr, f)

    # Common const information

    # Load const information
    print_load_ending(f, 8)

    f.close()
    os.system("cp %s %s" % (path, output_dir))

    logging.info(
        "Creating empty test for {}: finish in {}!".format(instr, path))

    return path


def create_first_test_vlre8(xlen, vlen, vsew, lmul, vta, vma, output_dir, rpt_path):
    logging.info("Creating first test for {}".format(instr))

    path = "%s/%s_first.S" % (output_dir, instr)
    f = open(path, "w+")

    # Common header files
    print_common_header(instr, f)
     
    # Generate macros to test diffrent register
    generate_macros_vlre(f, 8)
    
    # Generate tests
    (n, vr_num) = generate_tests_vlre(f, 8)

    # Common const information

    # Load const information
    print_load_ending(f, 8, n, is_vlr = True, seg = vr_num)

    f.close()
    os.system("cp %s %s" % (path, output_dir))

    logging.info(
        "Creating first test for {}: finish in {}!".format(instr, path))

    return path
