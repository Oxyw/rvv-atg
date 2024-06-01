from glob import glob
import logging
import os
from scripts.test_common_info import *
from scripts.create_test_permute.const_data import *
import re
import math

instr = 'vmv'

def extract_operands():
    val_10 = list(set(coverpoints_16) | set(coverpoints_32) | set(coverpoints_64))
    val = ['{:#016x}'.format(int(x) & 0xffffffffffffffff)
            for x in val_10]
    return val


def print_ending_vmv(f, val, test_num_tuple, vlen, vsew, lmul):
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

    num_elem = int(vlen * lmul / vsew)
    print(".align %d"%(int(vsew / 8)), file=f)
    print("rs_data:", file=f)

    for i in range(len(val)):
        print_data_width_prefix(f, vsew)
        print("%s"%val[i], file=f)

    print_origin_data_ending(f)

    print("\n\
    RVTEST_DATA_END\n", file=f)
    num_tests = test_num_tuple[0] + test_num_tuple[1]
    xfvcsr_num = 11  # 1 xcsr, 3 fcsr, 7 vcsr
    print_rvmodel_data([0, (test_num_tuple[0] + num_elem * test_num_tuple[1]) + xfvcsr_num * num_tests, 0], f)


def generate_macros(f, vsew, lmul):
    for n in range(1,32):
        print("#define TEST_VMVS_OP_rsrd_%d( testnum, result )"%n + " \\\n\
            TEST_CASE_X( testnum, x8,  \\\n\
                li TESTNUM, testnum; \\\n\
                li x7, MASK_VSEW(result);" + " \\\n\
                li x8, 0; \\\n\
                vmv.s.x v%d, x7; "%n + " \\\n\
                vmv.x.s x8, v%d;"%n + " \\\n\
                li x2, VSEW_MASK_BITS; \\\n\
                and x8, x8, x2; \\\n\
                )", file=f)
    lmul = 1 if lmul < 1 else int(lmul)
    for n in range(1, 32):
        if n % lmul != 0:
            continue
        vs = 16 if n == 8 else 8   # v8 as rs
        print("#define TEST_VMVVV_OP_rd%d( testnum, val )"%n + " \\\n\
            TEST_CASE_LOOP( testnum, v%d, "%n + " \\\n\
                VSET_VSEW_4AVL \\\n\
                la x7, rd_origin_data; \\\n\
                vle%d.v v%d, (x7);"%(vsew, n) + " \\\n\
                la x7, val; \\\n\
                vle%d.v v%d, (x7);"%(vsew, vs) + " \\\n\
                vmv.v.v v%d, v%d;"%(n, vs)+" \\\n\
            )", file=f)
    for n in range(1,32):
        if n % lmul != 0 or n == 8 or n == 16 or n == 24:
            continue
        vd = 24
        print("#define TEST_VMVVV_OP_rs%d( testnum, val )"%n + " \\\n\
            TEST_CASE_LOOP( testnum, v%d, "%n + " \\\n\
                VSET_VSEW_4AVL \\\n\
                la x7, rd_origin_data; \\\n\
                vle%d.v v%d, (x7);"%(vsew, vd) + " \\\n\
                la x7, val; \\\n\
                vle%d.v v%d, (x7);"%(vsew, n) + " \\\n\
                vmv.v.v v%d, v%d;"%(vd, n)+" \\\n\
            )", file=f)
    for n in range(1,32):
        print("#define TEST_VMVVX_OP_%d( testnum, val )"%n + " \\\n\
            TEST_CASE_LOOP( testnum, v%d, "%n + " \\\n\
                VSET_VSEW_4AVL \\\n\
                la x7, rd_origin_data; \\\n\
                vle%d.v v%d, (x7);"%(vsew, n) + " \\\n\
                li x1, MASK_XLEN(val); \\\n\
                vmv.v.x v%d, x1;"%(n)+" \\\n\
            )", file=f)
    for n in range(1,32):
        print("#define TEST_VMVVI_OP_%d( testnum, val )"%n + " \\\n\
            TEST_CASE_LOOP( testnum, v%d, "%n + " \\\n\
                VSET_VSEW_4AVL \\\n\
                la x7, rd_origin_data; \\\n\
                vle%d.v v%d, (x7);"%(vsew, n) + " \\\n\
                vmv.v.i v%d, SEXT_IMM(val);"%(n)+" \\\n\
            )", file=f)


def generate_tests(f, val, vlen, vsew, lmul):
    num_elem = int((vlen * lmul / vsew))
    if num_elem == 0:
        return 0
    
    loop_num = math.ceil(len(val) / num_elem)
    step_bytes = int(vlen * lmul / 8)

    n = 0
    print("  #-------------------------------------------------------------",file=f)
    print("  # VMV Tests",file=f)
    print("  #-------------------------------------------------------------",file=f)

    for i in range(len(val)):
        n += 1
        print("  TEST_VMV_OP( "+str(n)+",  "+str(val[i])+" );", file=f)
    
    print("  #-------------------------------------------------------------",file=f)
    print("  # VMVS Tests (different register)",file=f)
    print("  #-------------------------------------------------------------",file=f)
    
    for i in range(len(val)):     
        k = i % 31 + 1
        n += 1
        print("  TEST_VMVS_OP_rsrd_%d( "%k+str(n)+", "+str(val[i])+" );",file=f)
    
    single_test_num = n
    
    print("  #-------------------------------------------------------------",file=f)
    print("  # VMVVV Tests",file=f)
    print("  #-------------------------------------------------------------",file=f)
    
    for i in range(min(32, loop_num)):
        k = i % 31 + 1
        if k % lmul != 0:
            continue
        n += 1
        print("  TEST_VMVVV_OP_rd%d( "%k+str(n)+",  rs_data+%d );"%(i*step_bytes), file=f)
        k = i % 30 + 2
        if k % lmul != 0 or k == 8 or k == 16 or k == 24:
            continue
        n +=1
        print("  TEST_VMVVV_OP_rs%d( "%k+str(n)+",  rs_data+%d );"%(i*step_bytes), file=f)

    print("  #-------------------------------------------------------------",file=f)
    print("  # VMVVX Tests",file=f)
    print("  #-------------------------------------------------------------",file=f)

    for i in range(1, 32):
        if i % lmul == 0:
            n += 1
            print("  TEST_VMVVX_OP_%d( "%i+str(n)+",  %s );"%(val[i % len(val)]), file=f)
    
    print("  #-------------------------------------------------------------",file=f)
    print("  # VMVVI Tests",file=f)
    print("  #-------------------------------------------------------------",file=f)

    for i in range(1, 32):
        if i % lmul == 0:
            n += 1
            print("  TEST_VMVVI_OP_%d( "%i+str(n)+",  14 );", file=f)
    
    loop_test_num = n - single_test_num
    return (single_test_num, loop_test_num)


def create_empty_test_vmv(xlen, vlen, vsew, lmul, vta, vma, output_dir):
    logging.info("Creating first test for {}".format(instr))

    path = "%s/%s_first.S" % (output_dir, instr)
    f = open(path, "w+")

    # Common header files
    print_common_header(instr, f)

    # Extract operands
    val = extract_operands()

    # Generate macros to test diffrent register
    generate_macros(f, vsew, lmul)

    # Generate tests
    test_num_tuple = generate_tests(f, val, vlen, vsew, lmul)

    # Common const information
    print_ending_vmv(f, val, test_num_tuple , vlen, vsew, lmul)
    
    f.close()
    os.system("cp %s %s" % (path, output_dir))

    logging.info(
        "Creating first test for {}: finish in {}!".format(instr, path))

    return path
