from glob import glob
import logging
import os
from random import randint
from scripts.create_test_mask.create_test_common import *
from scripts.test_common_info import *
from scripts.create_test_permute.const_data import *
import re

instr = 'vslide1'
walking_val = []
rd_val = [3, 5, 6, 7, 9, 10, 11, 12, 13, 14, 15, 17,
          18, 19, 20, 21, 22, 23, 24, 25, 26, 27, 28, 29, 30,
          33, 35, 36, 37, 39, 40, 41, 42, 43, 44, 45, 47,
          48, 49, 50, 51, 52, 53, 54, 55, 56, 57, 58, 59, 60,
          61, 67, 71, 73, 79, 83, 89, 97, 101, 103, 105, 107, 109, 111, 113, 115] # 66
vma = False  # False to turn to undisturb
num_elem = 0
num_group_walking = 0
walking_val_grouped = []


def generate_macros_vslide1(f, vlen, vsew, lmul):
    vlen = int(os.environ['RVV_ATG_VLEN'])
    vsew = int(os.environ['RVV_ATG_VSEW'])
    lmul = 1 if lmul < 1 else int(lmul)
    masked = True if os.environ['RVV_ATG_MASKED'] == "True" else False
    
    print("#define TEST_VSLIDE1_VX_OP( testnum, inst,  rd_base, rs1, base, mask_addr ) \\\n\
        TEST_CASE_LOOP( testnum, v16,  \\\n\
            VSET_VSEW_4AVL \\\n\
            %s \
            la  x1, base; \\\n\
            vle%d.v v8, (x1); \\\n\
            la  x1, rd_base; \\\n\
            vle%d.v v16, (x1); \\\n\
            li x1, rs1; \\\n\
            inst v16, v8, x1%s; \\\n\
        )"%(("la x7, mask_addr; \\\n    vlm.v v0, (x7); \\\n  "if masked else ""), vsew, vsew, (", v0.t" if masked else "")), file=f)
    for i in range(1, 32):
        if i == 8 or i == 16 or i % lmul != 0:
            continue;
        print("#define TEST_VSLIDE1_VX_OP_rd_%d( testnum, inst,  rd_base, rs1, base, mask_addr ) \\\n\
            TEST_CASE_LOOP( testnum, v%d,  \\\n\
                VSET_VSEW_4AVL \\\n\
                %s \
                la  x1, base; \\\n\
                vle%d.v v8, (x1); \\\n\
                la  x1, rd_base; \\\n\
                vle%d.v v%d, (x1); \\\n\
                li x1, rs1; \\\n\
                inst v%d, v8, x1%s; \\\n\
            )"%(i, i, ("la x7, mask_addr; \\\n    vlm.v v0, (x7); \\\n  "if masked else ""), vsew, vsew, i, i, (", v0.t" if masked else "")), file=f)
        print("#define TEST_VSLIDE1_VX_OP_rs2_%d( testnum, inst,  rd_base, rs1, base, mask_addr ) \\\n\
            TEST_CASE_LOOP( testnum, v16,  \\\n\
                VSET_VSEW_4AVL \\\n\
                %s \
                la  x1, base; \\\n\
                vle%d.v v%d, (x1); \\\n\
                la  x1, rd_base; \\\n\
                vle%d.v v16, (x1); \\\n\
                li x1, rs1; \\\n\
                inst v16, v%d, x1%s; \\\n\
            )"%(i, ("la x7, mask_addr; \\\n    vlm.v v0, (x7); \\\n  "if masked else ""), vsew, i, vsew, i, (", v0.t" if masked else "")), file=f)
        

    for i in range(1, 32):
        if i == 1 or i == 7:
            continue;
        print("#define TEST_VSLIDE1_VX_OP_rs1_%d( testnum, inst,  rd_base, rs1, base, mask_addr ) \\\n\
            TEST_CASE_LOOP( testnum, v16,  \\\n\
                VSET_VSEW_4AVL \\\n\
                %s \
                la  x1, base; \\\n\
                vle%d.v v8, (x1); \\\n\
                la  x1, rd_base; \\\n\
                vle%d.v v16, (x1); \\\n\
                li x%d, rs1; \\\n\
                inst v16, v8, x%d%s; \\\n\
            )"%(i, ("la x7, mask_addr; \\\n    vlm.v v0, (x7); \\\n  "if masked else ""), vsew, vsew, i, i, (", v0.t" if masked else "")), file=f)


def generate_tests_vslide1(f, lmul):
    lmul = 1 if lmul < 1 else int(lmul)
    n=1
    if num_group_walking == 0:
        return 0
    vlmax = num_elem
    mask_bytes = 32 # math.ceil(vlmax / 8)
    mask_num = vlmax * 2 + 4
    j = 0
    print("  #-------------------------------------------------------------",file=f)
    print("  # vslide1up/down.vx/vf Test    ------------------------------------------",file=f)
    print("  #-------------------------------------------------------------",file=f)
    
    for i in range(num_group_walking):
        print("  TEST_VSLIDE1_VX_OP( " + str(n) + ", vslide1up.vx, rd_data, " + str(walking_val_grouped[i][0]) + ", walking_data%d, mask_data+%d );"%(i, j*mask_bytes), file=f)
        n +=1
        j = (j + 1) % mask_num
        print("  TEST_VSLIDE1_VX_OP( " + str(n) + ", vslide1down.vx, rd_data, " + str(walking_val_grouped[i][0]) + ", walking_data%d, mask_data+%d );"%(i, j*mask_bytes), file=f)
        n +=1
        j = (j + 1) % mask_num
    vx_test_num = n
    print("  #-------------------------------------------------------------",file=f)
    print("  # vslide1up/down.vx/vf Test    ------------------------------------------",file=f)
    print("  #-------------------------------------------------------------",file=f)
    
    for i in range(1, 32):
        if i != 8 and i != 16 and i % lmul == 0 and i != 24 and i != 12 and i != 20:
            print("  TEST_VSLIDE1_VX_OP_rd_%d( "%i + str(n) + ", vslide1up.vx, rd_data, " + str(walking_val_grouped[i%num_group_walking][0]) + ", walking_data%d, mask_data+%d );"%(i%num_group_walking, j*mask_bytes), file=f)
            n +=1
            j = (j + 1) % mask_num
            print("  TEST_VSLIDE1_VX_OP_rs2_%d( "%i + str(n) + ", vslide1up.vx, rd_data, " + str(walking_val_grouped[i%num_group_walking][0]) + ", walking_data%d, mask_data+%d );"%(i%num_group_walking, j*mask_bytes), file=f)
            n +=1
            j = (j + 1) % mask_num
        if i != 1 and i != 7 and i != 24 and i != 12 and i != 20:
            print("  TEST_VSLIDE1_VX_OP_rs1_%d( "%i + str(n) + ", vslide1up.vx, rd_data, " + str(walking_val_grouped[i%num_group_walking][0]) + ", walking_data%d, mask_data+%d );"%(i%num_group_walking, j*mask_bytes), file=f)
            n +=1
            j = (j + 1) % mask_num
    vi_test_num = n - vx_test_num
    return (vx_test_num, vi_test_num, 0)


def generate_dat_seg_vslide1(f, vsew):
    global rd_val
    global vma
    masked = True if os.environ['RVV_ATG_MASKED'] == "True" else False
    vma = os.environ["RVV_ATG_VMA"]
    agnostic_type = int(os.environ['RVV_ATG_AGNOSTIC_TYPE'])
    print("rd_data:", file=f)
    if vma == "True" and agnostic_type == 1:
        for i in range(num_elem):
            print_data_width_prefix(f, vsew)
            print("%d"%rd_val[i], file=f)
        print("",file=f)
        for i in range(num_group_walking):
            # generate data
            print("walking_data%d:"%i, file=f)
            for j in range(num_elem):
                print_data_width_prefix(f, vsew)
                print("%d"%walking_val_grouped[i][j], file=f)
            print("", file=f)
            '''
            # generate answer for vslide1up
            print("walking_data_slide1upans%d:"%i, file=f)
            for j in range(num_elem):
                if j == 0:
                    print_data_width_prefix(f, vsew)
                    print("%d"%(1 if (masked and get_mask_bit(j) == 0) else walking_val_grouped[i][0]), file=f)
                else:
                    print_data_width_prefix(f, vsew)
                    print("%d"%(1 if (masked and get_mask_bit(j) == 0) else walking_val_grouped[i][j-1]), file=f)
            print("", file=f)
            # generate answer for vslide1up
            print("walking_data_slide1downans%d:"%i, file=f)
            for j in range(num_elem):
                if j == num_elem - 1:
                    print_data_width_prefix(f, vsew)
                    print("%d"%(1 if (masked and get_mask_bit(j) == 0) else walking_val_grouped[i][0]), file=f)
                else:
                    print_data_width_prefix(f, vsew)
                    print("%d"%(1 if (masked and get_mask_bit(j) == 0) else walking_val_grouped[i][j+1]), file=f)
            print("", file=f)
            '''
    else:
        for i in range(num_elem):
            print_data_width_prefix(f, vsew)
            print("%d"%rd_val[i], file=f)
        print("",file=f)
        for i in range(num_group_walking):
            # generate data
            print("walking_data%d:"%i, file=f)
            for j in range(num_elem):
                print_data_width_prefix(f, vsew)
                print("%d"%walking_val_grouped[i][j], file=f)
            print("", file=f)
            '''
            # generate answer for vslide1up
            print("walking_data_slide1upans%d:"%i, file=f)
            for j in range(num_elem):
                if j == 0:
                    print_data_width_prefix(f, vsew)
                    print("%d"%(rd_val[j] if (masked and get_mask_bit(j) == 0) else walking_val_grouped[i][0]), file=f)
                else:
                    print_data_width_prefix(f, vsew)
                    print("%d"%(rd_val[j] if (masked and get_mask_bit(j) == 0) else walking_val_grouped[i][j-1]), file=f)
            print("", file=f)
            # generate answer for vslide1up
            print("walking_data_slide1downans%d:"%i, file=f)
            for j in range(num_elem):
                if j == num_elem - 1:
                    print_data_width_prefix(f, vsew)
                    print("%d"%(rd_val[j] if (masked and get_mask_bit(j) == 0) else walking_val_grouped[i][0]), file=f)
                else:
                    print_data_width_prefix(f, vsew)
                    print("%d"%(rd_val[j] if (masked and get_mask_bit(j) == 0) else walking_val_grouped[i][j+1]), file=f)
            print("", file=f)
            '''

def print_ending_vslide(f, vlen, vsew, tuples):
    print(" #endif\n\
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

    generate_dat_seg_vslide1(f, vsew)
    print_mask_origin_data_ending(f, num_elem)

    print("\n\
    RVTEST_DATA_END\n", file=f)
    arr = gen_arr_compute(tuples, 1)
    print_rvmodel_data(arr, f)


def create_empty_test_vslide1(xlen, vlen, vsew, lmul, vta, _vma, output_dir):
    logging.info("Creating empty test for {}".format(instr))
    global num_elem
    global num_group_walking
    global num_group_f
    global walking_val_grouped
    global f_val_grouped
    global rd_val
    global vma
    global walking_val
    if vsew == 8 or vsew == 16:
        walking_val = coverpoints_16
    elif vsew == 32:
        walking_val = coverpoints_32
    else:
        walking_val = coverpoints_64
    num_elem = int(vlen * lmul/ vsew)
    # Add walking_val_grouped values, need at least num_elem
    for i in range(num_elem - min(len(walking_val), len(rd_val)) + 2):
        walking_val.append(randint(-(2**(vsew-1)), 2**(vsew-1)-1))
        rd_val.append(randint(-(2**(vsew-1)), 2**(vsew-1)-1))
    if num_elem != 0:
        num_group_walking = int(len(walking_val) / num_elem)
    vma = _vma
    for i in range(num_group_walking):
        temp = []
        for j in range(num_elem):
            temp.append(walking_val[i*num_elem+j])
        walking_val_grouped.append(temp)

    path = "%s/%s_empty.S" % (output_dir, instr)
    f = open(path, "w+")

    generate_macros_vslide1(f, vlen, vsew, lmul)

    # Common header files
    print_common_header(instr, f)

    tuples = generate_tests_vslide1(f, lmul)

    # Common const information
    print_ending_vslide(f, vlen, vsew, tuples)

    f.close()

    logging.info(
        "Creating empty test for {}: finish in {}!".format(instr, path))

    return path
