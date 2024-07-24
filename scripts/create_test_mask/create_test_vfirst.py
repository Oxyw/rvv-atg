import logging
import os
from scripts.create_test_mask.create_test_common import *
from scripts.test_common_info import *
import re

instr = 'vfirst'
num_elem = 0


def generate_walking_data_seg_vfirst(f, vsew, vlen):
    # Generate walking ones
    n = 0
    if vsew == 8:
        data_width_prefix = "byte"
    elif vsew == 16:
        data_width_prefix = "hword"
    elif vsew == 32:
        data_width_prefix = "word"
    elif vsew == 64:
        data_width_prefix = "dword"
    for i in range(num_elem + 1):
        print("walking_dat_vfirst%d:"%n, file=f)
        print_data_width_prefix(f, 64)
        print("0b", end="", file=f)
        print(i * "0", end="", file=f)
        if i != num_elem:
            print("1", end="", file=f)
        print((num_elem - i - 1) * "0", end="", file=f)
        print("", file=f)
        for i in range( vlen//64 -1):
            print(".dword\t0x0", file=f)
        n = n + 1

    for j in range(num_elem + 1):
        print("walking_dat_vfirst%d:"%n, file=f)
        print_data_width_prefix(f, 64)
        print("0b", end="", file=f)
        print(j * "1", end="", file=f)
        if j != num_elem:
            print("0", end="", file=f)
        print((num_elem - j - 1) * "1", end="", file=f)
        print("", file=f)
        for i in range( vlen//64 -1):
            print(".dword\t0x0", file=f)
        n = n + 1


def generate_macros_vfirst(f, vsew, lmul):
    lmul_1 = 1 if lmul < 1 else int(lmul)
    vlen = int(os.environ['RVV_ATG_VLEN'])
    vsew = int(os.environ['RVV_ATG_VSEW'])
    masked = True if os.environ['RVV_ATG_MASKED'] == "True" else False
    # generate the macro
    print("#undef TEST_VFIRST_OP \n\
          #define TEST_VFIRST_OP( testnum, inst,  vm_addr, mask_addr ) \\\n\
    TEST_CASE_SCALAR_SETVSEW_AFTER(testnum, x14,  \\\n\
        VSET_VSEW_4AVL \\\n\
        la  x2, vm_addr; \\\n\
        vle%d.v v16, (x2);"%vsew + " \\\n\
        %s "%("la x7, mask_addr; \\\n    vlm.v v0, (x7); \\\n  "if masked else "")+" \
        inst x14, v16%s; "%(", v0.t" if masked else "") + " \\\n\
    )", file=f)
    
    for i in range(1, 32):
        if i == 7 or i  == 16 or i == 3:
            continue
        print("#define TEST_VFIRST_OP_rs2_%d( testnum, inst,  vm_addr, mask_addr ) \\\n\
            TEST_CASE_SCALAR_SETVSEW_AFTER(testnum, x14,  \\\n\
                VSET_VSEW_4AVL \\\n\
                la  x2, vm_addr; \\\n\
                vle%d.v v%d, (x2);"%(i, vsew, i)+" \\\n\
                %s "%("la x7, mask_addr; \\\n    vlm.v v0, (x7); \\\n  "if masked else "")+" \
                inst x14, v%d%s; "%(i, (", v0.t" if masked else "")) + " \\\n\
            )", file=f)
    
    for i in range(1, 32):
        if i == 7 or i  == 16 or i == 3 or i == 20: # 20 is signature base 
            continue
        print("#define TEST_VFIRST_OP_rd_%d( testnum, inst,  vm_addr, mask_addr ) \\\n\
            TEST_CASE_SCALAR_SETVSEW_AFTER(testnum, x%d,  \\\n\
                VSET_VSEW_4AVL \\\n\
                la  x2, vm_addr; \\\n\
                vle%d.v v16, (x2);"%(i, i, vsew)+" \\\n\
                %s "%("la x7, mask_addr; \\\n    vlm.v v0, (x7); \\\n  "if masked else "")+" \
                inst x%d, v16%s; "%(i, (", v0.t" if masked else "")) + " \\\n\
            )", file=f)



def generate_tests_vfirst(f, vlen, vsew, lmul):
    num_test = 0
    num_elem = int(vlen / vsew)
    vemul = int(vsew / vsew * lmul)
    if vemul == 0:
        vemul = 1
    
    vlmax = int(vlen * lmul / vsew) # TODO
    mask_bytes = 4 * math.ceil(vlmax / 32) # 4 * num_words
    mask_num = vlmax * 2 + 4
    j = 0
    #########################vfirst####################################################################################################
    print("  #-------------------------------------------------------------",file=f)
    print("  # vfirst tests",file=f)
    print("  #-------------------------------------------------------------",file=f)
    for i in range(0, 2 * num_elem + 2):
        num_test = num_test + 1
        print("TEST_VFIRST_OP( %d, vfirst.m,  walking_dat_vfirst%d, mask_data+%d );" % (num_test, i, j*mask_bytes), file=f)
        j = (j + 1) % mask_num

    return num_test



def print_ending_vfirst(vlen, vsew, f, n):
    # generate const information
    print(" #endif\n\
    \n\
    RVTEST_CODE_END\n\
    RVMODEL_HALT\n\
    \n\
    .data\n\
    RVTEST_DATA_BEGIN\n\
    \n\
    TEST_DATA\n\
    ", file=f)

    generate_walking_data_seg_vfirst(f, vsew, vlen)
    print_mask_origin_data_ending(f)

    print("\n\
    RVTEST_DATA_END\n", file=f)
    arr = gen_arr_load(n)
    print_rvmodel_data(arr, f)


def create_empty_test_vfirst(xlen, vlen, vsew, lmul, vta, vma, output_dir):
    global num_elem
    num_elem = int(vlen / vsew)
    logging.info("Creating empty test for {}".format(instr))

    path = "%s/%s_empty.S" % (output_dir, instr)
    f = open(path, "w+")

    generate_macros_vfirst(f, vsew, lmul)

    # Common header files
    print_common_header(instr, f)

    n = generate_tests_vfirst(f, vlen, vsew, lmul)

    # Common const information
    print_ending_vfirst(vlen, vsew, f, n)

    f.close()

    logging.info(
        "Creating empty test for {}: finish in {}!".format(instr, path))

    return path
