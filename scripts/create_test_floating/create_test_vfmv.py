import logging
import os
from scripts.test_common_info import *
from scripts.create_test_floating.create_test_common import generate_fdat_seg
import re

instr = 'vfmv'


def generate_macros(f, vsew, lmul):
    for n in range(1, 32):
        if n % lmul != 0:
            continue
        print("#define TEST_VFMV_VF_OP_vd_%d( testnum, base ) \\\n\
        TEST_CASE_LOOP_FP( testnum, v%d,  \\\n\
            VSET_VSEW_4AVL \\\n\
            la x7, rd_origin_data; \\\n\
            vle%d.v v%d, (x7); \\\n\
            la a0, base; \\\n\
            fl%s f7, 0(a0); \\\n\
            vfmv.v.f v%d, f7; \\\n\
        )" % (n, n, vsew, n, "w" if vsew == 32 else "d", n), file=f)

    print("#define TEST_VFMV_SF_OP( testnum, base )  \\\n\
    TEST_CASE_FP( testnum, v24,  \\\n\
        VSET_VSEW_4AVL \\\n\
        la x7, rd_origin_data; \\\n\
        vle%d.v v24, (x7); \\\n\
        la a0, base; \\\n\
        fl%s f7, 0(a0); \\\n\
        vfmv.s.f v24, f7; \\\n\
    )" % (vsew, "w" if vsew == 32 else "d"), file=f)
    for n in range(1, 32):
        if n % lmul != 0:
            continue
        print("#define TEST_VFMV_FS_OP_vs_%d( testnum, base ) \\\n\
        TEST_CASE_FPREG( testnum, f8,  \\\n\
            VSET_VSEW_4AVL \\\n\
            la x7, rd_origin_data; \\\n\
            vle%d.v v%d, (x7); \\\n\
            la a0, base; \\\n\
            fl%s f7, 0(a0); \\\n\
            vfmv.s.f v%d, f7; \\\n\
            vfmv.f.s f8, v%d; \\\n\
        )" % (n, vsew, n, "w" if vsew == 32 else "d", n, n), file=f)


def generate_tests(f, lmul, rs1_val):
    n = 0
    print("  #-------------------------------------------------------------", file=f)
    print("  # vfmv.s.f Tests", file=f)
    print("  #-------------------------------------------------------------", file=f)

    for i in range(len(rs1_val)):
        n += 1
        print("  TEST_VFMV_SF_OP( " + str(n) + ",  fdat_rs1_" + str(i) + " );", file=f)

    k = 0
    
    print("  #-------------------------------------------------------------", file=f)
    print("  # vfmv.f.s / vfmv.s.f Tests (different register)", file=f)
    print("  #-------------------------------------------------------------", file=f)

    for i in range(1, 32):
        if i % lmul != 0:
            continue
        n += 1
        print("  TEST_VFMV_FS_OP_vs_%d( " %i + str(n) + ",  fdat_rs1_" + str(k) + " );", file=f)
        k = (k + 1) % len(rs1_val)
    
    single_test_num = n
    
    print("  #-------------------------------------------------------------", file=f)
    print("  # vfmv.v.f Tests (different register)", file=f)
    print("  #-------------------------------------------------------------", file=f)

    for i in range(1, 32):
        if i % lmul != 0:
            continue
        n += 1
        print("  TEST_VFMV_VF_OP_vd_%d( " %i + str(n) + ",  fdat_rs1_" + str(k) + " );", file=f)
        k = (k + 1) % len(rs1_val)
    
    loop_test_num = n - single_test_num
    return (single_test_num, loop_test_num)


def print_ending_vfmv(f, vlen, vsew, lmul, test_num_tuple, rs1_val, rs2_val):
    print("  #endif\n\
    \n\
    RVTEST_CODE_END\n\
    RVMODEL_HALT\n\
    \n\
    .data\n\
    RVTEST_DATA_BEGIN\n\
    \n\
    TEST_DATA\n\
    \n\
    ", file=f)

    generate_fdat_seg(f, rs1_val, rs2_val, vsew)
    
    print_origin_data_ending(f)

    print("\n\
    RVTEST_DATA_END\n", file=f)
    num_elem = int(vlen * lmul / vsew)
    num_tests = test_num_tuple[0] + test_num_tuple[1]
    xfvcsr_num = 11  # 1 xcsr, 3 fcsr, 7 vcsr
    print_rvmodel_data([0, (test_num_tuple[0] + num_elem * test_num_tuple[1]) + xfvcsr_num * num_tests, 0], f)


def create_empty_test_vfmv(xlen, vlen, vsew, lmul, vta, vma, output_dir):
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


def create_first_test_vfmv(xlen, vlen, vsew, lmul, vta, vma, output_dir, rpt_path):
    logging.info("Creating first test for {}".format(instr))

    path = "%s/%s_first.S" % (output_dir, instr)
    f = open(path, "w+")

    # Common header files
    print_common_header(instr, f)

    # Extract operands
    rs1_val, rs2_val = extract_operands_fp(f, rpt_path)

    # Generate macros to test diffrent register
    generate_macros(f, vsew, lmul)

    # Generate tests
    test_num_tuple = generate_tests(f, lmul, rs1_val, rs2_val)

    # Common const information
    print_ending_vfmv(f, vlen, vsew, lmul, test_num_tuple, rs1_val, rs2_val)

    f.close()
    os.system("cp %s %s" % (path, output_dir))

    logging.info(
        "Creating first test for {}: finish in {}!".format(instr, path))

    return path
