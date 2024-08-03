import logging
import os
from scripts.create_test_mask.create_test_common import *
from scripts.test_common_info import *
import re

instr = 'viota'


def generate_macros_viota(f, vsew, lmul):
    masked = True if os.environ['RVV_ATG_MASKED'] == "True" else False
    
    print("#undef TEST_VIOTA_OP", file=f)
    print("#define TEST_VIOTA_OP( testnum, inst, src2_addr, mask_addr ) \\\n\
    TEST_CASE_LOOP( testnum, v16, \\\n\
        VSET_VSEW_4AVL \\\n\
        la x7, rd_origin_data; \\\n\
        vle%d.v v16, (x7);"%vsew + " \\\n\
        %s "%("la x7, mask_addr; \\\n    vlm.v v0, (x7); \\\n  "if masked else "")+" \
        la  x7, src2_addr; \\\n\
        vlm.v v8, (x7); \\\n\
        inst v16, v8%s; "%(", v0.t" if masked else "") + " \\\n\
    )", file=f)

    for n in range(1, 32):
        vd = get_aligned_reg(n, 1, lmul)
        print("#define TEST_VIOTA_OP_vs2_%d( testnum, inst, src2_addr, mask_addr )"%n + " \\\n\
        TEST_CASE_LOOP( testnum, v%d, "%vd + " \\\n\
            VSET_VSEW_4AVL \\\n\
            la x7, rd_origin_data; \\\n\
            vle%d.v v%d, (x7);"%(vsew, vd) + " \\\n\
            %s "%("la x7, mask_addr; \\\n    vlm.v v0, (x7); \\\n  "if masked else "")+" \
            la  x7, src2_addr; \\\n\
            vlm.v v%d, (x7);"%(n) + " \\\n\
            inst v%d, v%d%s; "%(vd, n, ", v0.t" if masked else "") + " \\\n\
        )", file=f)

    for n in range(1, 32):
        if n % lmul != 0:
            continue
        vs2 = get_aligned_reg(n, lmul, 1)
        print("#define TEST_VIOTA_OP_vd_%d( testnum, inst, src2_addr, mask_addr )"%n + "  \\\n\
        TEST_CASE_LOOP( testnum, v%d, "%n + "  \\\n\
            VSET_VSEW_4AVL \\\n\
            la x7, rd_origin_data; \\\n\
            vle%d.v v%d, (x7);"%(vsew, n) + " \\\n\
            %s "%("la x7, mask_addr; \\\n    vlm.v v0, (x7); \\\n  "if masked else "")+" \
            la  x7, src2_addr; \\\n\
            vlm.v v%d, (x7);"%(vs2) + " \\\n\
            inst v%d, v%d%s; "%(n, vs2, ", v0.t" if masked else "") + " \\\n\
        )", file=f)


def generate_tests_viota(instr, f, vlen, vsew, lmul):
    num_elem = int(vlen * lmul / vsew)
    if num_elem == 0:
        return 0
    
    vlmax = num_elem
    mask_bytes = 4 * math.ceil(vlmax / 32) # 4 * num_words
    mask_num = vlmax * 2 + 4
    j = 1
    
    n = 0
    print("  #-------------------------------------------------------------", file=f)
    print("  # %s tests" % instr, file=f)
    print("  #-------------------------------------------------------------", file=f)
    
    for i in range(mask_num):
        n += 1
        print("TEST_VIOTA_OP( %d,  %s.m, mask_data+%d, mask_data+%d );" % (n, instr, i*mask_bytes, j*mask_bytes), file=f)
        j = (j + 1) % mask_num

    print("  #-------------------------------------------------------------", file=f)
    print("  # %s Tests (different register)" % instr, file=f)
    print("  #-------------------------------------------------------------", file=f)

    for i in range(1, 32):
        if i % lmul == 0:
            n += 1
            print("TEST_VIOTA_OP_vd_%d( %d,  %s.m, mask_data+%d, mask_data+%d );" % (i, n, instr, (i%mask_num)*mask_bytes, j*mask_bytes), file=f)
            j = (j + 1) % mask_num
    
    for i in range(1, 32):
        n += 1
        print("TEST_VIOTA_OP_vs2_%d( %d,  %s.m, mask_data+%d, mask_data+%d );" % (i, n, instr, (i%mask_num)*mask_bytes, j*mask_bytes), file=f)
        j = (j + 1) % mask_num
    
    return n


def create_empty_test_viota(xlen, vlen, vsew, lmul, vta, vma, output_dir):
    logging.info("Creating empty test for {}".format(instr))

    path = "%s/%s_empty.S" % (output_dir, instr)
    f = open(path, "w+")

    generate_macros_viota(f, vsew, lmul)

    # Common header files
    print_common_header(instr, f)

    n = generate_tests_viota(instr, f, vlen, vsew, lmul)

    # Common const information
    print_common_ending(f, test_num = n, print_data = True)

    f.close()

    logging.info(
        "Creating empty test for {}: finish in {}!".format(instr, path))

    return path
