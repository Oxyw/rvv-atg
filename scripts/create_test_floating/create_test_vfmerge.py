import logging
import os
from scripts.test_common_info import *
import re

instr = 'vfmerge'


def generate_macros_vfmerge(f, vsew, lmul):
    print("#undef TEST_FP_VF_M_OP \n\
#define TEST_FP_VF_M_OP( testnum, inst, val2, val1, mask_addr ) \\\n\
    TEST_CASE_LOOP_FP( testnum, v24,      \\\n\
        VSET_VSEW_4AVL \\\n\
        la x7, rd_origin_data; \\\n\
        vle%d.v v24, (x7);"%vsew + " \\\n\
        la x7, mask_addr; \\\n\
        vlm.v v0, (x7); \\\n\
        la x7, val2; \\\n\
        vle%d.v v8, (x7);"%vsew + " \\\n\
        la x7, val1; \\\n\
        fl%s f1, (x7);"%(('d' if vsew == 64 else 'w')) + " \\\n\
        inst v24, v8, f1, v0;  \\\n\
    )", file=f)
    for n in range(1, 32):
        if n % lmul != 0:
                continue
        print("#define TEST_FP_VF_M_OP_vd_%d( testnum, inst, val2, val1, mask_addr ) "%n + "\\\n\
        TEST_CASE_LOOP_FP( testnum, v%d,  "%n + "    \\\n\
            VSET_VSEW_4AVL \\\n\
            la x7, rd_origin_data; \\\n\
            vle%d.v v%d, (x7);"%(vsew, n) + " \\\n\
            la x7, mask_addr; \\\n\
            vlm.v v0, (x7); \\\n\
            la x7, val2; \\\n\
            vle%d.v v8, (x7);"%(vsew) + " \\\n\
            la x7, val1; \\\n\
            fl%s f1, (x7);"%('d' if vsew == 64 else 'w') + " \\\n\
            inst v%d, v8, f1, v0; "%(n) +" \\\n\
        )", file=f)
    for n in range(1, 32):
        if n % lmul != 0:
            continue
        print("#define TEST_FP_VF_M_OP_vs2_%d( testnum, inst, val2, val1, mask_addr )"%n + " \\\n\
        TEST_CASE_LOOP_FP( testnum, v24,    \\\n\
            VSET_VSEW_4AVL \\\n\
            la x7, rd_origin_data; \\\n\
            vle%d.v v24, (x7);"%vsew + " \\\n\
            la x7, mask_addr; \\\n\
            vlm.v v0, (x7); \\\n\
            la x7, val2; \\\n\
            vle%d.v v%d, (x7);"%(vsew, n) + " \\\n\
            la x7, val1; \\\n\
            fl%s f1, (x7);"%('d' if vsew == 64 else 'w') + " \\\n\
            inst v24, v%d, f1, v0; "%(n) + " \\\n\
        )", file=f)


def generate_tests_vfmerge(f, vsew, lmul, rs1_val, rs2_val):
    '''
    global rs1_val, rs2_val
    if vsew == 64:
        rs1_val = rs1_val_64
        rs2_val = rs2_val_64
    '''
    vlen = int(os.environ['RVV_ATG_VLEN'])
    vsew = int(os.environ['RVV_ATG_VSEW'])
    
    num_elem = int((vlen * lmul / vsew))
    if num_elem == 0:
        return 0
    loop_num = int(min(len(rs1_val), len(rs2_val)) / num_elem)
    step_bytes = int(vlen * lmul / 8)
    
    vlmax = num_elem
    mask_bytes = 4 * math.ceil(vlmax / 32) # 4 * num_words
    mask_num = vlmax * 2 + 4
    j = 0
    
    n = 0
    print("  #-------------------------------------------------------------",file=f)
    print("  # vfmerge.vfm Tests",file=f)
    print("  #-------------------------------------------------------------",file=f)
    
    for i in range(loop_num):        
        n += 1
        print("TEST_FP_VF_M_OP( %d, vfmerge.vfm, rs2_data+%d, rs1_data+%d, mask_data+%d);"%(n, i*step_bytes, i*step_bytes, j*mask_bytes), file=f)
        j = (j + 1) % mask_num
    
    print("  #-------------------------------------------------------------",file=f)
    print("  # vfmerge.vfm Tests (different register)",file=f)
    print("  #-------------------------------------------------------------",file=f)
    
    for i in range(1, 32):     
        if i % lmul != 0:
            continue
        k = i % loop_num  
        
        n += 1
        print("  TEST_FP_VF_M_OP_vd_%d( "%i+str(n)+", vfmerge.vfm, "+"rs2_data+%d, rs1_data+%d, mask_data+%d);"%(k*step_bytes, k*step_bytes, j*mask_bytes), file=f)
        j = (j + 1) % mask_num      
        
        n += 1
        print("  TEST_FP_VF_M_OP_vs2_%d( "%i+str(n)+", vfmerge.vfm, "+"rs2_data+%d, rs1_data+%d, mask_data+%d);"%(k*step_bytes, k*step_bytes, j*mask_bytes), file=f)
        j = (j + 1) % mask_num
    
    return n


def create_empty_test_vfmerge(xlen, vlen, vsew, lmul, vta, vma, output_dir):
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


def create_first_test_vfmerge(xlen, vlen, vsew, lmul, vta, vma, output_dir, rpt_path):
    logging.info("Creating first test for {}".format(instr))

    path = "%s/%s_first.S" % (output_dir, instr)
    f = open(path, "w+")

    # Common header files
    print_common_header(instr, f)

    # Extract operands
    rs1_val, rs2_val = extract_operands_fp(f, rpt_path)

    # Generate macros to test diffrent register
    generate_macros_vfmerge(f, vsew, lmul)

    # Generate tests
    n = generate_tests_vfmerge(f, vsew, lmul, rs1_val, rs2_val)

    # Common const information
    print_common_ending_rs1rs2rd(rs1_val, rs2_val, (0, n, 0), vsew, f)

    f.close()
    os.system("cp %s %s" % (path, output_dir))

    logging.info(
        "Creating first test for {}: finish in {}!".format(instr, path))

    return path
