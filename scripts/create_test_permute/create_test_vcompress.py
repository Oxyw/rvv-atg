import logging
import os
from scripts.test_common_info import *
from scripts.create_test_permute.create_test_common import *
import re

instr = 'vcompress'


def generate_macros_vcompress(f, vsew, lmul):
    print("#define TEST_VCOMPRESS_OP( testnum, inst, val2, val1 ) \\\n\
    TEST_CASE_LOOP( testnum, v16,  \\\n\
        VSET_VSEW_4AVL \\\n\
        la x7, rd_origin_data; \\\n\
        vle%d.v v16, (x7);"%(vsew) + " \\\n\
        la x7, val2; \\\n\
        vle%d.v v8, (x7);"%(vsew) + " \\\n\
        la x7, val1; \\\n\
        vlm.v v0, (x7); \\\n\
        inst v16, v8, v0; \\\n\
    )", file=f)
    
    for n in range(1, 32):
        if n % lmul != 0:
            continue
        vs2 = 16 if n == 8 else 8
        print("#define TEST_VCOMPRESS_OP_vd_%d( testnum, inst,  val2, val1 )"%n + " \\\n\
        TEST_CASE_LOOP( testnum, v%d, "%n + " \\\n\
            VSET_VSEW_4AVL \\\n\
            la x7, rd_origin_data; \\\n\
            vle%d.v v%d, (x7);"%(vsew, n) + " \\\n\
            la x7, val2; \\\n\
            vle%d.v v%d, (x7);"%(vsew, vs2) + " \\\n\
            la x7, val1; \\\n\
            vlm.v v0, (x7); \\\n\
            inst v%d, v%d, v0;"%(n, vs2)+" \\\n\
        )", file=f)
    
    for n in range(1, 32):
        if n % lmul != 0:
            continue
        vd = 24 if n == 16 else 16
        print("#define TEST_VCOMPRESS_OP_vs2_%d( testnum, inst,  val2, val1 )"%n + " \\\n\
        TEST_CASE_LOOP( testnum, v%d, "%vd + " \\\n\
            VSET_VSEW_4AVL \\\n\
            la x7, rd_origin_data; \\\n\
            vle%d.v v%d, (x7);"%(vsew, vd) + " \\\n\
            la x7, val2; \\\n\
            vle%d.v v%d, (x7);"%(vsew, n) + " \\\n\
            la x7, val1; \\\n\
            vlm.v v0, (x7); \\\n\
            inst v%d, v%d, v0;"%(vd, n)+" \\\n\
        )", file=f)

    for n in range(1, 32):
        vd, vs2 = get_aligned_regs(n, 1, lmul, lmul)
        if vd == vs2 == 0:
            continue
        print("#define TEST_VCOMPRESS_OP_vs1_%d( testnum, inst,  val2, val1 )"%n + " \\\n\
        TEST_CASE_LOOP( testnum, v%d, "%vd + " \\\n\
            VSET_VSEW_4AVL \\\n\
            la x7, rd_origin_data; \\\n\
            vle%d.v v%d, (x7);"%(vsew, vd) + " \\\n\
            la x7, val2; \\\n\
            vle%d.v v%d, (x7);"%(vsew, vs2) + " \\\n\
            la x7, val1; \\\n\
            vlm.v v%d, (x7);"%(n) + " \\\n\
            inst v%d, v%d, v%d;"%(vd, vs2, n) + " \\\n\
        )", file=f)


def generate_tests_vcompress(f, vlen, vsew, lmul, rs1_val, rs2_val):
    num_elem = int(vlen * lmul / vsew)
    if num_elem == 0:
        return 0
    loop_num = int(min(len(rs1_val), len(rs2_val) / num_elem))
    step_bytes = int(vlen * lmul / 8)
    mask_bytes = 4 * math.ceil(num_elem / 32) # 4 * num_words
    
    n = 0
    print("  #-------------------------------------------------------------", file=f)
    print("  # %s tests" % instr, file=f)
    print("  #-------------------------------------------------------------", file=f)
    
    for i in range(loop_num):
        n += 1
        print("TEST_VCOMPRESS_OP( %d,  %s.vm,  rs2_data+%d, rs1_data+%d );" % (n, instr, i*step_bytes, i*mask_bytes), file=f)
    
    print("  #-------------------------------------------------------------", file=f)
    print("  # %s Tests (different register)" % instr, file=f)
    print("  #-------------------------------------------------------------", file=f)

    for i in range(1, 32):
        if i % lmul != 0:
            continue
        k = i % loop_num
        n += 1
        print("TEST_VCOMPRESS_OP_vd_%d( %d,  %s.vm,  rs2_data+%d, rs1_data+%d );" % (
            i, n, instr, k*step_bytes, k*mask_bytes), file=f)
        n += 1
        print("TEST_VCOMPRESS_OP_vs2_%d( %d,  %s.vm,  rs2_data+%d, rs1_data+%d );" % (
            i, n, instr, k*step_bytes, k*mask_bytes), file=f)

    for i in range(1, 32):
        if get_aligned_regs(n, 1, lmul, lmul) == (0, 0):
            continue
        k = i % loop_num
        n += 1
        print("TEST_VCOMPRESS_OP_vs1_%d( %d,  %s.vm,  rs2_data+%d, rs1_data+%d );" % (
            i, n, instr,  k*step_bytes, k*mask_bytes), file=f)
        
    return n


def create_empty_test_vcompress(xlen, vlen, vsew, lmul, vta, vma, output_dir):
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


def create_first_test_vcompress(xlen, vlen, vsew, lmul, vta, vma, output_dir, rpt_path):
    logging.info("Creating first test for {}".format(instr))

    path = "%s/%s_first.S" % (output_dir, instr)
    f = open(path, "w+")

    # Common header files
    print_common_header(instr, f)
    
    # Extract operands
    rs1_val, rs2_val = extract_operands(f, rpt_path, is_rs1_mask = True)

    # Generate macros to test diffrent register
    generate_macros_vcompress(f, vsew, lmul)
    
    # Generate tests
    n = generate_tests_vcompress(f, vlen, vsew, lmul, rs1_val, rs2_val)

    # Common const information
    print_common_ending_rs1rs2rd(rs1_val, rs2_val, n, vsew, f, is_rs1_mask = True)

    f.close()
    os.system("cp %s %s" % (path, output_dir))

    logging.info(
        "Creating first test for {}: finish in {}!".format(instr, path))

    return path
