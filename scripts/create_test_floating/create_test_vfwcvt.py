import logging
import os
from scripts.test_common_info import *
from scripts.create_test_floating.create_test_common import print_ending

instr = 'vfwcvt'


def generate_macros_vfwcvt(f, lmul):
    vlen = int(os.environ['RVV_ATG_VLEN'])
    vsew = int(os.environ['RVV_ATG_VSEW'])
    lmul_1 = 1 if lmul < 1 else int(lmul)
    masked = True if os.environ['RVV_ATG_MASKED'] == "True" else False
    print("#undef TEST_FP_W_V_OP \n\
#define TEST_FP_W_V_OP( testnum, inst, val1, mask_addr ) \\\n\
    TEST_CASE_LOOP_W_FP( testnum, v24,     \\\n\
        VSET_VSEW_4AVL \\\n\
        la x7, rd_origin_data; \\\n\
        vle%d.v v24, (x7);"%(vsew*2 if vsew < 64 else 64) + " \\\n\
        %s "%("la x7, mask_addr; \\\n    vlm.v v0, (x7); \\\n  "if masked else "")+" \
        la x7, val1; \\\n\
        vle%d.v v8, (x7);"%vsew + " \\\n\
        inst v24, v8%s; "%(", v0.t" if masked else "") + " \\\n\
    )", file=f)
    for n in range(1, 32):
        if n % lmul != 0 or n == 24:
            continue
        print("#define TEST_FP_W_V_OP_rs1_%d( testnum, inst, val1, mask_addr )"%n + " \\\n\
            TEST_CASE_LOOP_W_FP( testnum, v24, \\\n\
                VSET_VSEW_4AVL \\\n\
                la x7, rd_origin_data; \\\n\
                vle%d.v v24, (x7);"%(vsew*2 if vsew < 64 else 64) + " \\\n\
                %s "%("la x7, mask_addr; \\\n    vlm.v v0, (x7); \\\n  "if masked else "")+" \
                la x7, val1; \\\n\
                vle%d.v v%d, (x7);"%(vsew, n) + " \\\n\
                inst v24, v%d%s; "%(n, ", v0.t" if masked else "") + " \\\n\
            )", file = f)

    for n in range(1, 32):
        if n % lmul != 0 or n == 8:
            continue
        print("#define TEST_FP_W_V_OP_rd_%d( testnum, inst, val1, mask_addr )"%n + " \\\n\
            TEST_CASE_LOOP_W_FP( testnum, v%d,  "%n + " \\\n\
                VSET_VSEW_4AVL \\\n\
                la x7, rd_origin_data; \\\n\
                vle%d.v v%d, (x7);"%(vsew*2 if vsew < 64 else 64, n) + " \\\n\
                %s "%("la x7, mask_addr; \\\n    vlm.v v0, (x7); \\\n  "if masked else "")+" \
                la x7, val1; \\\n\
                vle%d.v v8, (x7);"%(vsew) + " \\\n\
                inst v%d, v8%s; "%(n, ", v0.t" if masked else "") + " \\\n\
            )", file = f)


def generate_tests_vfwcvt(instr, f, lmul, rs1_val, rs2_val):
    vlen = int(os.environ['RVV_ATG_VLEN'])
    vsew = int(os.environ['RVV_ATG_VSEW'])
    '''
    global rs1_val, rs2_val, rs1_val_64, rs2_val_64
    if vsew == 64:
        rs1_val = rs1_val_64
        rs2_val = rs2_val_64
    rs1_val = list(set(rs1_val))
    rs2_val = list(set(rs2_val))
    '''

    lmul_1 = 1 if lmul < 1 else int(lmul)
    n = 0
    
    num_elem = int(vlen * lmul / vsew)
    if num_elem == 0:
        return 0
    loop_num = min(int(min(len(rs1_val), len(rs2_val)) / num_elem), 20)
    step_bytes = int(vlen * lmul / 8)
    step_bytes_double = step_bytes * 2
    
    vlmax = num_elem
    mask_bytes = 4 * math.ceil(vlmax / 32) # 4 * num_words
    mask_num = vlmax * 2 + 4
    j = 0
    
    print("  #-------------------------------------------------------------",file=f)
    print("  # vfwcvt Tests",file=f)
    print("  #-------------------------------------------------------------",file=f)
    
    # for i in range(loop_num):
    #     print("TEST_FP_W_V_OP( %d,  %s, "%(n, 'vfwcvt.xu.f.v') + "rs1_data+%d);"%(i*step_bytes), file=f)
    #     n += 1
    #     print("TEST_FP_W_V_OP( %d,  %s, "%(n, 'vfwcvt.x.f.v') + "rs1_data+%d);"%(i*step_bytes), file=f)
    #     n += 1
    #     print("TEST_FP_W_V_OP( %d,  %s, "%(n, 'vfwcvt.rtz.xu.f.v') + "rs1_data+%d);"%(i*step_bytes), file=f)
    #     n += 1
    #     print("TEST_FP_W_V_OP( %d,  %s, "%(n, 'vfwcvt.rtz.x.f.v') + "rs1_data+%d);"%(i*step_bytes), file=f)
    #     n += 1
    #     print("TEST_FP_W_V_OP( %d,  %s, "%(n, 'vfwcvt.f.f.v') + "rs1_data+%d);"%(i*step_bytes), file=f)
    #     n += 1
    
    # for i in range(loop_num):
    #     print("TEST_FP_W_V_OP( %d,  %s, "%(n, 'vfwcvt.f.xu.v') + "rs1_data_int+%d);"%(i*step_bytes), file=f)
    #     n += 1
    #     print("TEST_FP_W_V_OP( %d,  %s, "%(n, 'vfwcvt.f.x.v') + "rs1_data_int+%d);"%(i*step_bytes), file=f)
    #     n += 1
    
    print("  #-------------------------------------------------------------",file=f)
    print("  # vfwcvt Tests (different register)",file=f)
    print("  #-------------------------------------------------------------",file=f)
    

    for i in range(min(32, loop_num)):
        k = i % 31 + 1  
        if k % lmul == 0 and k != 8:
            for i in range(loop_num):
                n += 1
                print("TEST_FP_W_V_OP_rs1_%d( %d,  %s, "%(k, n, 'vfwcvt.xu.f.v') + "rs1_data+%d, mask_data+%d);"%(i*step_bytes, j*mask_bytes), file=f)
                j = (j + 1) % mask_num
                n += 1
                print("TEST_FP_W_V_OP_rs1_%d( %d,  %s, "%(k, n, 'vfwcvt.x.f.v') + "rs1_data+%d, mask_data+%d);"%(i*step_bytes, j*mask_bytes), file=f)
                j = (j + 1) % mask_num
                n += 1
                print("TEST_FP_W_V_OP_rs1_%d( %d,  %s, "%(k, n, 'vfwcvt.rtz.xu.f.v') + "rs1_data+%d, mask_data+%d);"%(i*step_bytes, j*mask_bytes), file=f)
                j = (j + 1) % mask_num
                n += 1
                print("TEST_FP_W_V_OP_rs1_%d( %d,  %s, "%(k, n, 'vfwcvt.rtz.x.f.v') + "rs1_data+%d, mask_data+%d);"%(i*step_bytes, j*mask_bytes), file=f)
                j = (j + 1) % mask_num
                n += 1
                print("TEST_FP_W_V_OP_rs1_%d( %d,  %s, "%(k, n, 'vfwcvt.f.f.v') + "rs1_data+%d, mask_data+%d);"%(i*step_bytes, j*mask_bytes), file=f)
                j = (j + 1) % mask_num
            for i in range(loop_num):
                n += 1
                print("TEST_FP_W_V_OP_rs1_%d( %d,  %s, "%(k, n, 'vfwcvt.f.xu.v') + "rs1_data_int+%d, mask_data+%d);"%(i*step_bytes, j*mask_bytes), file=f)
                j = (j + 1) % mask_num
                n += 1
                print("TEST_FP_W_V_OP_rs1_%d( %d,  %s, "%(k, n, 'vfwcvt.f.x.v') + "rs1_data_int+%d, mask_data+%d);"%(i*step_bytes, j*mask_bytes), file=f)
                j = (j + 1) % mask_num

        k = i % 31 + 1
        if k % (2*lmul) != 0 or k == 8:
            continue
        for i in range(loop_num):
            n += 1
            print("TEST_FP_W_V_OP_rd_%d( %d,  %s, "%(k, n, 'vfwcvt.x.f.v') + "rs1_data+%d, mask_data+%d);"%(i*step_bytes, j*mask_bytes), file=f)
            j = (j + 1) % mask_num
            n += 1
            print("TEST_FP_W_V_OP_rd_%d( %d,  %s, "%(k, n, 'vfwcvt.xu.f.v') + "rs1_data+%d, mask_data+%d);"%(i*step_bytes, j*mask_bytes), file=f)
            j = (j + 1) % mask_num
            n += 1
            print("TEST_FP_W_V_OP_rd_%d( %d,  %s, "%(k, n, 'vfwcvt.rtz.xu.f.v') + "rs1_data+%d, mask_data+%d);"%(i*step_bytes, j*mask_bytes), file=f)
            j = (j + 1) % mask_num
            n += 1
            print("TEST_FP_W_V_OP_rd_%d( %d,  %s, "%(k, n, 'vfwcvt.rtz.x.f.v') + "rs1_data+%d, mask_data+%d);"%(i*step_bytes, j*mask_bytes), file=f)
            j = (j + 1) % mask_num
            n += 1
            print("TEST_FP_W_V_OP_rd_%d( %d,  %s, "%(k, n, 'vfwcvt.f.f.v') + "rs1_data+%d, mask_data+%d);"%(i*step_bytes, j*mask_bytes), file=f)
            j = (j + 1) % mask_num
        for i in range(loop_num):
            n += 1
            print("TEST_FP_W_V_OP_rd_%d( %d,  %s, "%(k, n, 'vfwcvt.f.xu.v') + "rs1_data_int+%d, mask_data+%d);"%(i*step_bytes, j*mask_bytes), file=f)
            j = (j + 1) % mask_num
            n += 1
            print("TEST_FP_W_V_OP_rd_%d( %d,  %s, "%(k, n, 'vfwcvt.f.x.v') + "rs1_data_int+%d, mask_data+%d);"%(i*step_bytes, j*mask_bytes), file=f)
            j = (j + 1) % mask_num
    return (n, 0, 0)


def create_empty_test_vfwcvt(xlen, vlen, vsew, lmul, vta, vma, output_dir):
    logging.info("Creating empty test for {}".format(instr))

    path = "%s/%s_empty.S" % (output_dir, instr)
    f = open(path, "w+")

    # Common header files
    print_common_header(instr, f)


    # Common const information
    print_ending(f)

    f.close()
    os.system("cp %s %s" % (path, output_dir))

    logging.info(
        "Creating empty test for {}: finish in {}!".format(instr, path))

    return path


def create_first_test_vfwcvt(xlen, vlen, vsew, lmul, vta, vma, output_dir, rpt_path):
    logging.info("Creating first test for {}".format(instr))

    path = "%s/%s_first.S" % (output_dir, instr)
    f = open(path, "w+")

    # Common header files
    print_common_header(instr, f)

    # Extract operands
    rs1_val, rs2_val = extract_operands_fp(f, rpt_path)
    rs2_val = rs1_val

    # Generate macros to test diffrent register
    generate_macros_vfwcvt(f, lmul)

    # Generate tests
    num_tests_tuple = generate_tests_vfwcvt(instr, f, lmul, rs1_val, rs2_val)

    # Common const information
    print_common_ending_rs1rs2rd_vfcvt(rs1_val, rs2_val, num_tests_tuple, vsew, f, is_widen = True)

    f.close()
    os.system("cp %s %s" % (path, output_dir))

    logging.info(
        "Creating first test for {}: finish in {}!".format(instr, path))

    return path
