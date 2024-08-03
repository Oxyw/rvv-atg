import logging
import os
from scripts.create_test_mask.create_test_common import *
from scripts.test_common_info import *
import re

instr = 'vid'


def generate_macros_vid(f, vsew, lmul):
    masked = True if os.environ['RVV_ATG_MASKED'] == "True" else False
    
    print("#define TEST_VID_OP( testnum, inst, mask_addr ) \\\n\
    TEST_CASE_LOOP( testnum, v8, \\\n\
        VSET_VSEW_4AVL \\\n\
        la x7, rd_origin_data; \\\n\
        vle%d.v v8, (x7);"%vsew + " \\\n\
        %s "%("la x7, mask_addr; \\\n    vlm.v v0, (x7); \\\n  "if masked else "")+" \
        inst v8%s; "%(", v0.t" if masked else "") + " \\\n\
    )", file=f)
    for n in range(1, 32):
        if n % lmul != 0:
            continue
        print("#define TEST_VID_OP_vd_%d( testnum, inst, mask_addr )"%n + " \\\n\
        TEST_CASE_LOOP( testnum, v%d, "%n + " \\\n\
            VSET_VSEW_4AVL \\\n\
            la x7, rd_origin_data; \\\n\
            vle%d.v v%d, (x7);"%(vsew, n) + " \\\n\
            %s "%("la x7, mask_addr; \\\n    vlm.v v0, (x7); \\\n  "if masked else "")+" \
            inst v%d%s; "%(n, (", v0.t" if masked else "")) + " \\\n\
        )", file=f)


def generate_tests_vid(instr, f, vlen, vsew, lmul):
    num_elem = int(vlen * lmul / vsew)
    if num_elem == 0:
        return 0
    vlmax = num_elem
    mask_bytes = 4 * math.ceil(vlmax / 32) # 4 * num_words
    mask_num = vlmax * 2 + 4
    
    n = 0
    print("  #-------------------------------------------------------------", file=f)
    print("  # %s tests (different masks)" % instr, file=f)
    print("  #-------------------------------------------------------------", file=f)
    
    for i in range(mask_num):
        n += 1
        print("TEST_VID_OP( %d,  %s.v, mask_data+%d );" % (n, instr, i*mask_bytes), file=f)

    print("  #-------------------------------------------------------------", file=f)
    print("  # %s Tests (different register)" % instr, file=f)
    print("  #-------------------------------------------------------------", file=f)

    for i in range(1, 32):
        if i % lmul != 0:
            continue
        n += 1
        print("TEST_VID_OP_vd_%d( %d,  %s.v, mask_data+%d );" % (i, n, instr, (i%mask_num)*mask_bytes), file=f)
    
    return n


def create_empty_test_vid(xlen, vlen, vsew, lmul, vta, vma, output_dir):
    logging.info("Creating empty test for {}".format(instr))

    path = "%s/%s_empty.S" % (output_dir, instr)
    f = open(path, "w+")

    # Common header files
    print_common_header(instr, f)
    
    generate_macros_vid(f, vsew, lmul)

    n = generate_tests_vid(instr, f, vlen, vsew, lmul)

    # Common const information
    print_common_ending(f, test_num = n, print_data = True)

    f.close()

    logging.info(
        "Creating empty test for {}: finish in {}!".format(instr, path))

    return path
