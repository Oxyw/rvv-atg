import logging
import os
from scripts.test_common_info import *
from scripts.create_test_floating.create_test_common import generate_macros_vfcvt, generate_tests_vfcvt
import re

instr = 'vfncvt'
suffix_list_f = ['xu.f.w', 'x.f.w', 'rtz.xu.f.w', 'rtz.x.f.w', 'f.f.w', 'rod.f.f.w']
suffix_list_i = ['f.xu.w', 'f.x.w']
suffix_list = [suffix_list_f, suffix_list_i]


def create_empty_test_vfncvt(xlen, vlen, vsew, lmul, vta, vma, output_dir):
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


def create_first_test_vfncvt(xlen, vlen, vsew, lmul, vta, vma, output_dir, rpt_path):
    logging.info("Creating first test for {}".format(instr))

    path = "%s/%s_first.S" % (output_dir, instr)
    f = open(path, "w+")

    # Common header files
    print_common_header(instr, f)

    # Extract operands
    rs1_val, rs2_val = extract_operands_fp(f, rpt_path)
    rs2_val = rs1_val

    # Generate macros to test diffrent register
    generate_macros_vfcvt(f, lmul, is_narrow=True)

    # Generate tests
    num_tests_tuple = generate_tests_vfcvt(instr, suffix_list, f, lmul, rs1_val, rs2_val, is_narrow=True)

    # Common const information
    print_common_ending_rs1rs2rd_vfcvt(rs1_val, rs2_val, num_tests_tuple, vsew, f, is_narrow = True)

    f.close()
    os.system("cp %s %s" % (path, output_dir))

    logging.info(
        "Creating first test for {}: finish in {}!".format(instr, path))

    return path
