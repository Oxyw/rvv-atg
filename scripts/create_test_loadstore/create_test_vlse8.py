import logging
import os
from scripts.test_common_info import *
from scripts.create_test_loadstore.create_test_common import generate_macros_vlse, generate_tests_vlse
import re

instr = 'vlse8'


def create_empty_test_vlse8(xlen, vlen, vsew, lmul, vta, vma, output_dir):
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


def create_first_test_vlse8(xlen, vlen, vsew, lmul, vta, vma, output_dir, rpt_path):
    logging.info("Creating first test for {}".format(instr))
    
    path = "%s/%s_first.S" % (output_dir, instr)
    f = open(path, "w+")
    
    # Common header files
    print_common_header(instr, f)
    
    # Extract operands
    rs1_val, rs2_val = extract_operands(f, rpt_path)
    
    # Generate macros to test diffrent register
    generate_macros_vlse(f, lmul, vsew, 8)
    
    # Generate tests
    n = generate_tests_vlse(f, rs1_val, rs2_val, lmul, vsew, 8)
    
    # Common const information
    
    # Load const information
    print_load_ending(f, 8, n)
    
    f.close()
    os.system("cp %s %s" % (path, output_dir))
    
    logging.info(
          "Creating first test for {}: finish in {}!".format(instr, path))
    
    return path
