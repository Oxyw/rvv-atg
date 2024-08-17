import logging
import os
from scripts.test_common_info import *
from scripts.create_test_permute.create_test_common import print_ending_mv
import re
import math

instr = 'vmv'


def generate_macros(f, vsew, lmul):
    print("#define TEST_VMVSX_OP( testnum, result )  \\\n\
    TEST_CASE( testnum, v24,  \\\n\
        VSET_VSEW_4AVL \\\n\
        la x7, rd_origin_data; \\\n\
        vle%d.v v24, (x7);"%(vsew) + " \\\n\
        li x7, MASK_VSEW(result); \\\n\
        vmv.s.x v24, x7; \\\n\
    )", file=f)
    for n in range(1, 32):
        print("#define TEST_VMVXS_OP_%d( testnum, result )"%n + " \\\n\
        TEST_CASE_XREG( testnum, x8,  \\\n\
            VSET_VSEW_4AVL \\\n\
            la x7, rd_origin_data; \\\n\
            vle%d.v v%d, (x7);"%(vsew, n) + " \\\n\
            li x7, MASK_VSEW(result);" + " \\\n\
            li x8, 0; \\\n\
            vmv.s.x v%d, x7; "%n + " \\\n\
            vmv.x.s x8, v%d;"%n + " \\\n\
        )", file=f)
    
    for n in range(1, 32):
        if n % lmul != 0:
            continue
        vs = 16 if n == 8 else 8   # v8 as vs
        print("#define TEST_VMVVV_OP_vd_%d( testnum, val )"%n + " \\\n\
        TEST_CASE_LOOP( testnum, v%d, "%n + " \\\n\
            VSET_VSEW_4AVL \\\n\
            la x7, rd_origin_data; \\\n\
            vle%d.v v%d, (x7);"%(vsew, n) + " \\\n\
            la x7, val; \\\n\
            vle%d.v v%d, (x7);"%(vsew, vs) + " \\\n\
            vmv.v.v v%d, v%d;"%(n, vs)+" \\\n\
        )", file=f)
    for n in range(1, 32):
        if n % lmul != 0:
            continue
        vd = 16 if n == 24 else 24  # v24 as vd
        print("#define TEST_VMVVV_OP_vs_%d( testnum, val )"%n + " \\\n\
        TEST_CASE_LOOP( testnum, v%d, "%vd + " \\\n\
            VSET_VSEW_4AVL \\\n\
            la x7, rd_origin_data; \\\n\
            vle%d.v v%d, (x7);"%(vsew, vd) + " \\\n\
            la x7, val; \\\n\
            vle%d.v v%d, (x7);"%(vsew, n) + " \\\n\
            vmv.v.v v%d, v%d;"%(vd, n)+" \\\n\
        )", file=f)
    
    for n in range(1, 32):
        print("#define TEST_VMVVX_OP_vd_%d( testnum, val )"%n + " \\\n\
        TEST_CASE_LOOP( testnum, v%d, "%n + " \\\n\
            VSET_VSEW_4AVL \\\n\
            la x7, rd_origin_data; \\\n\
            vle%d.v v%d, (x7);"%(vsew, n) + " \\\n\
            li x1, MASK_XLEN(val); \\\n\
            vmv.v.x v%d, x1;"%(n)+" \\\n\
        )", file=f)
    for n in range(1, 32):
        print("#define TEST_VMVVI_OP_vd_%d( testnum, val )"%n + " \\\n\
        TEST_CASE_LOOP( testnum, v%d, "%n + " \\\n\
            VSET_VSEW_4AVL \\\n\
            la x7, rd_origin_data; \\\n\
            vle%d.v v%d, (x7);"%(vsew, n) + " \\\n\
            vmv.v.i v%d, SEXT_IMM(val);"%(n)+" \\\n\
        )", file=f)


def generate_tests(f, val, vlen, vsew, lmul):
    num_elem = int(vlen * lmul / vsew)
    if num_elem == 0:
        return 0
    
    loop_num = int(len(val) / num_elem)
    step_bytes = int(vlen * lmul / 8)

    n = 0
    print("  #-------------------------------------------------------------",file=f)
    print("  # VMV Tests",file=f)
    print("  #-------------------------------------------------------------",file=f)

    for i in range(len(val)):
        n += 1
        print("  TEST_VMVSX_OP( "+str(n)+",  "+str(val[i])+" );", file=f)
    
    print("  #-------------------------------------------------------------",file=f)
    print("  # VMVS Tests (different register)",file=f)
    print("  #-------------------------------------------------------------",file=f)
    
    for i in range(1, 32):
        # TODO: In spec, "The instructions ignore LMUL and vector register groups."
        # But if not add this condition, exception trap_illegal_instruction will occur.
        if i % lmul != 0:
            continue
        n += 1
        print("  TEST_VMVXS_OP_%d( "%i+str(n)+", "+str(val[i % len(val)])+" );",file=f)
    
    single_test_num = n
    
    print("  #-------------------------------------------------------------",file=f)
    print("  # VMVVV Tests",file=f)
    print("  #-------------------------------------------------------------",file=f)
    
    for i in range(1, 32):
        if i % lmul != 0:
            continue
        k = i % loop_num
        n += 1
        print("  TEST_VMVVV_OP_vd_%d( "%i+str(n)+",  rs_data+%d );"%(k*step_bytes), file=f)
        n += 1
        print("  TEST_VMVVV_OP_vs_%d( "%i+str(n)+",  rs_data+%d );"%(k*step_bytes), file=f)

    print("  #-------------------------------------------------------------",file=f)
    print("  # VMVVX Tests",file=f)
    print("  #-------------------------------------------------------------",file=f)

    for i in range(1, 32):
        if i % lmul == 0:
            n += 1
            print("  TEST_VMVVX_OP_vd_%d( "%i+str(n)+",  %s );"%(val[i % len(val)]), file=f)
    
    print("  #-------------------------------------------------------------",file=f)
    print("  # VMVVI Tests",file=f)
    print("  #-------------------------------------------------------------",file=f)

    for i in range(1, 32):
        if i % lmul == 0:
            n += 1
            print("  TEST_VMVVI_OP_vd_%d( "%i+str(n)+",  14 );", file=f)
    
    loop_test_num = n - single_test_num
    return (single_test_num, loop_test_num)


def create_empty_test_vmv(xlen, vlen, vsew, lmul, vta, vma, output_dir):
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


def create_first_test_vmv(xlen, vlen, vsew, lmul, vta, vma, output_dir, rpt_path):
    logging.info("Creating first test for {}".format(instr))

    path = "%s/%s_first.S" % (output_dir, instr)
    f = open(path, "w+")

    # Common header files
    print_common_header(instr, f)

    # Extract operands
    rs1_val, rs2_val = extract_operands(f, rpt_path)

    # Generate macros to test diffrent register
    generate_macros(f, vsew, lmul)

    # Generate tests
    test_num_tuple = generate_tests(f, rs1_val, vlen, vsew, lmul)

    # Common const information
    print_ending_mv(f, rs1_val, test_num_tuple, vlen, vsew, lmul)
    
    f.close()
    os.system("cp %s %s" % (path, output_dir))

    logging.info(
        "Creating first test for {}: finish in {}!".format(instr, path))

    return path
