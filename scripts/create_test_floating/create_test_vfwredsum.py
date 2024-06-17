import logging
import os
from scripts.test_common_info import *
from scripts.create_test_floating.create_test_common import valid_aligned_regs, print_ending

instr = 'vfwredsum'  # Widening Floating-Point Reduction Instruction: vd(2*SEW), vs2(SEW), vs1(2*SEW)
'''
rs1_val = ["0x00000000", "0xBF800000", "0xBF800000", "0xBF800000", "0xBF800000", "0xBF800000", "0xBF800000", "0xBF800000", "0xBF800000", "0xBF800000", "0xBF800000", "0xBF800000", "0xBF800000", "0xBF800000", "0xBF800000", "0xBF800000", "0xBF800000", "0x3F800000", "0x3F800000", "0x3F800000", "0x3F800000", "0x3F800000", "0x3F800000", "0x3F800000", "0x3F800000", "0x3F800000", "0x3F800000", "0x3F800000", "0x3F800000", "0x3F800000", "0x3F800000", "0x3F800000", "0x3F800000", "0xFF7FFFFF", "0xFF7FFFFF", "0xFF7FFFFF", "0xFF7FFFFF", "0xFF7FFFFF", "0xFF7FFFFF", "0xFF7FFFFF", "0xFF7FFFFF", "0xFF7FFFFF", "0xFF7FFFFF", "0xFF7FFFFF", "0xFF7FFFFF", "0xFF7FFFFF", "0xFF7FFFFF", "0xFF7FFFFF", "0xFF7FFFFF", "0x7F7FFFFF", "0x7F7FFFFF", "0x7F7FFFFF", "0x7F7FFFFF", "0x7F7FFFFF", "0x7F7FFFFF", "0x7F7FFFFF", "0x7F7FFFFF", "0x7F7FFFFF", "0x7F7FFFFF", "0x7F7FFFFF", "0x7F7FFFFF", "0x7F7FFFFF", "0x7F7FFFFF", "0x7F7FFFFF", "0x7F7FFFFF", "0x80855555", "0x80855555", "0x80855555", "0x80855555", "0x80855555", "0x80855555", "0x80855555", "0x80855555", "0x80855555", "0x80855555", "0x80855555", "0x80855555", "0x80855555", "0x80855555", "0x80855555", "0x80855555", "0x00800001", "0x00800001", "0x00800001", "0x00800001", "0x00800001", "0x00800001", "0x00800001", "0x00800001", "0x00800001", "0x00800001", "0x00800001", "0x00800001", "0x00800001", "0x00800001", "0x00800001", "0x00800001", "0x80800000", "0x80800000", "0x80800000", "0x80800000", "0x80800000", "0x80800000", "0x80800000", "0x80800000", "0x80800000", "0x80800000", "0x80800000", "0x80800000", "0x80800000", "0x80800000", "0x80800000", "0x80800000", "0x00800000", "0x00800000", "0x00800000", "0x00800000", "0x00800000", "0x00800000", "0x00800000", "0x00800000", "0x00800000", "0x00800000", "0x00800000", "0x00800000", "0x00800000", "0x00800000", "0x00800000",
           "0x00800000", "0x807FFFFF", "0x807FFFFF", "0x807FFFFF", "0x807FFFFF", "0x807FFFFF", "0x807FFFFF", "0x807FFFFF", "0x807FFFFF", "0x807FFFFF", "0x807FFFFF", "0x807FFFFF", "0x807FFFFF", "0x807FFFFF", "0x807FFFFF", "0x807FFFFF", "0x807FFFFF", "0x007FFFFF", "0x007FFFFF", "0x007FFFFF", "0x007FFFFF", "0x007FFFFF", "0x007FFFFF", "0x007FFFFF", "0x007FFFFF", "0x007FFFFF", "0x007FFFFF", "0x007FFFFF", "0x007FFFFF", "0x007FFFFF", "0x007FFFFF", "0x007FFFFF", "0x007FFFFF", "0x807FFFFE", "0x807FFFFE", "0x807FFFFE", "0x807FFFFE", "0x807FFFFE", "0x807FFFFE", "0x807FFFFE", "0x807FFFFE", "0x807FFFFE", "0x807FFFFE", "0x807FFFFE", "0x807FFFFE", "0x807FFFFE", "0x807FFFFE", "0x807FFFFE", "0x807FFFFE", "0x00000002", "0x00000002", "0x00000002", "0x00000002", "0x00000002", "0x00000002", "0x00000002", "0x00000002", "0x00000002", "0x00000002", "0x00000002", "0x00000002", "0x00000002", "0x00000002", "0x00000002", "0x00000002", "0x80000001", "0x80000001", "0x80000001", "0x80000001", "0x80000001", "0x80000001", "0x80000001", "0x80000001", "0x80000001", "0x80000001", "0x80000001", "0x80000001", "0x80000001", "0x80000001", "0x80000001", "0x80000001", "0x00000001", "0x00000001", "0x00000001", "0x00000001", "0x00000001", "0x00000001", "0x00000001", "0x00000001", "0x00000001", "0x00000001", "0x00000001", "0x00000001", "0x00000001", "0x00000001", "0x00000001", "0x00000001", "0x80000000", "0x80000000", "0x80000000", "0x80000000", "0x80000000", "0x80000000", "0x80000000", "0x80000000", "0x80000000", "0x80000000", "0x80000000", "0x80000000", "0x80000000", "0x80000000", "0x80000000", "0x80000000", "0x00000000", "0x00000000", "0x00000000", "0x00000000", "0x00000000", "0x00000000", "0x00000000", "0x00000000", "0x00000000", "0x00000000", "0x00000000", "0x00000000", "0x00000000", "0x00000000", "0x00000000", ]
rs2_val = ["0x00000000", "0xBF800000", "0x3F800000", "0xFF7FFFFF", "0x7F7FFFFF", "0x80855555", "0x00800001", "0x80800000", "0x00800000", "0x807FFFFF", "0x007FFFFF", "0x807FFFFE", "0x00000002", "0x80000001", "0x00000001", "0x80000000", "0x00000000", "0xBF800000", "0x3F800000", "0xFF7FFFFF", "0x7F7FFFFF", "0x80855555", "0x00800001", "0x80800000", "0x00800000", "0x807FFFFF", "0x007FFFFF", "0x807FFFFE", "0x00000002", "0x80000001", "0x00000001", "0x80000000", "0x00000000", "0xBF800000", "0x3F800000", "0xFF7FFFFF", "0x7F7FFFFF", "0x80855555", "0x00800001", "0x80800000", "0x00800000", "0x807FFFFF", "0x007FFFFF", "0x807FFFFE", "0x00000002", "0x80000001", "0x00000001", "0x80000000", "0x00000000", "0xBF800000", "0x3F800000", "0xFF7FFFFF", "0x7F7FFFFF", "0x80855555", "0x00800001", "0x80800000", "0x00800000", "0x807FFFFF", "0x007FFFFF", "0x807FFFFE", "0x00000002", "0x80000001", "0x00000001", "0x80000000", "0x00000000", "0xBF800000", "0x3F800000", "0xFF7FFFFF", "0x7F7FFFFF", "0x80855555", "0x00800001", "0x80800000", "0x00800000", "0x807FFFFF", "0x007FFFFF", "0x807FFFFE", "0x00000002", "0x80000001", "0x00000001", "0x80000000", "0x00000000", "0xBF800000", "0x3F800000", "0xFF7FFFFF", "0x7F7FFFFF", "0x80855555", "0x00800001", "0x80800000", "0x00800000", "0x807FFFFF", "0x007FFFFF", "0x807FFFFE", "0x00000002", "0x80000001", "0x00000001", "0x80000000", "0x00000000", "0xBF800000", "0x3F800000", "0xFF7FFFFF", "0x7F7FFFFF", "0x80855555", "0x00800001", "0x80800000", "0x00800000", "0x807FFFFF", "0x007FFFFF", "0x807FFFFE", "0x00000002", "0x80000001", "0x00000001", "0x80000000", "0x00000000", "0xBF800000", "0x3F800000", "0xFF7FFFFF", "0x7F7FFFFF", "0x80855555", "0x00800001", "0x80800000", "0x00800000", "0x807FFFFF", "0x007FFFFF", "0x807FFFFE", "0x00000002", "0x80000001", "0x00000001", "0x80000000",
           "0x00000000", "0xBF800000", "0x3F800000", "0xFF7FFFFF", "0x7F7FFFFF", "0x80855555", "0x00800001", "0x80800000", "0x00800000", "0x807FFFFF", "0x007FFFFF", "0x807FFFFE", "0x00000002", "0x80000001", "0x00000001", "0x80000000", "0x00000000", "0xBF800000", "0x3F800000", "0xFF7FFFFF", "0x7F7FFFFF", "0x80855555", "0x00800001", "0x80800000", "0x00800000", "0x807FFFFF", "0x007FFFFF", "0x807FFFFE", "0x00000002", "0x80000001", "0x00000001", "0x80000000", "0x00000000", "0xBF800000", "0x3F800000", "0xFF7FFFFF", "0x7F7FFFFF", "0x80855555", "0x00800001", "0x80800000", "0x00800000", "0x807FFFFF", "0x007FFFFF", "0x807FFFFE", "0x00000002", "0x80000001", "0x00000001", "0x80000000", "0x00000000", "0xBF800000", "0x3F800000", "0xFF7FFFFF", "0x7F7FFFFF", "0x80855555", "0x00800001", "0x80800000", "0x00800000", "0x807FFFFF", "0x007FFFFF", "0x807FFFFE", "0x00000002", "0x80000001", "0x00000001", "0x80000000", "0x00000000", "0xBF800000", "0x3F800000", "0xFF7FFFFF", "0x7F7FFFFF", "0x80855555", "0x00800001", "0x80800000", "0x00800000", "0x807FFFFF", "0x007FFFFF", "0x807FFFFE", "0x00000002", "0x80000001", "0x00000001", "0x80000000", "0x00000000", "0xBF800000", "0x3F800000", "0xFF7FFFFF", "0x7F7FFFFF", "0x80855555", "0x00800001", "0x80800000", "0x00800000", "0x807FFFFF", "0x007FFFFF", "0x807FFFFE", "0x00000002", "0x80000001", "0x00000001", "0x80000000", "0x00000000", "0xBF800000", "0x3F800000", "0xFF7FFFFF", "0x7F7FFFFF", "0x80855555", "0x00800001", "0x80800000", "0x00800000", "0x807FFFFF", "0x007FFFFF", "0x807FFFFE", "0x00000002", "0x80000001", "0x00000001", "0x80000000", "0x00000000", "0xBF800000", "0x3F800000", "0xFF7FFFFF", "0x7F7FFFFF", "0x80855555", "0x00800001", "0x80800000", "0x00800000", "0x807FFFFF", "0x007FFFFF", "0x807FFFFE", "0x00000002", "0x80000001", "0x00000001", "0x80000000", ]
'''


def generate_macros_vfwred(f, vsew, lmul):
    masked = True if os.environ['RVV_ATG_MASKED'] == "True" else False
      
    print("#define TEST_W_FP_RED_OP( testnum, inst, val1, val2, mask_addr ) \\\n\
    TEST_CASE_W_FP( testnum, v24, \\\n\
        VSET_VSEW_4AVL \\\n\
        la x7, rd_origin_data; \\\n\
        vle%d.v v24, (x7);"%(vsew*2 if vsew < 64 else 64) + " \\\n\
        la x7, val1; \\\n\
        vle%d.v v8, (x7);"%(vsew*2 if vsew < 64 else 64) + " \\\n\
        la x7, val2; \\\n\
        vle%d.v v16, (x7);"%vsew + " \\\n\
        %s "%("la x7, mask_addr; \\\n    vlm.v v0, (x7); \\\n  "if masked else "")+" \
        inst v24, v16, v8%s;"%(", v0.t" if masked else "") + " \\\n\
    )", file=f)
    
    for n in range(1,32):
        if n % (2*lmul) != 0:
            continue
        rs2, rd = valid_aligned_regs(n)
        print("#define TEST_W_FP_RED_OP_rs1%d( testnum, inst, val1, val2, mask_addr ) "%n + " \\\n\
        TEST_CASE_W_FP( testnum, v%d, "%rd + "\\\n\
            VSET_VSEW_4AVL \\\n\
            la x7, rd_origin_data; \\\n\
            vle%d.v v%d, (x7);"%((vsew*2 if vsew < 64 else 64), rd) + " \\\n\
            la x7, val1; \\\n\
            vle%d.v v%d, (x7);"%((vsew*2 if vsew < 64 else 64), n) + " \\\n\
            la x7, val2; \\\n\
            vle%d.v v%d, (x7);"%(vsew, rs2) + " \\\n\
            %s "%("la x7, mask_addr; \\\n    vlm.v v0, (x7); \\\n  "if masked else "")+" \
            inst v%d, v%d, v%d%s;"%(rd, rs2, n, (", v0.t" if masked else "")) + " \\\n\
        )",file=f)
    
    for n in range(1,32):
        if n % lmul != 0:
            continue
        rs1, rd = valid_aligned_regs(n)
        print("#define TEST_W_FP_RED_OP_rs2%d( testnum, inst, val1, val2, mask_addr ) "%n + " \\\n\
        TEST_CASE_W_FP( testnum, v%d, "%rd + "\\\n\
            VSET_VSEW_4AVL \\\n\
            la x7, rd_origin_data; \\\n\
            vle%d.v v%d, (x7);"%((vsew*2 if vsew < 64 else 64), rd) + " \\\n\
            la x7, val1; \\\n\
            vle%d.v v%d, (x7);"%((vsew*2 if vsew < 64 else 64), rs1) + " \\\n\
            la x7, val2; \\\n\
            vle%d.v v%d, (x7);"%(vsew, n) + " \\\n\
            %s "%("la x7, mask_addr; \\\n    vlm.v v0, (x7); \\\n  "if masked else "")+" \
            inst v%d, v%d, v%d%s;"%(rd, n, rs1, (", v0.t" if masked else "")) + " \\\n\
        )",file=f)
    
    for n in range(1,32):
        if n % (2*lmul) != 0:
            continue
        rs1, rs2 = valid_aligned_regs(n)
        print("#define TEST_W_FP_RED_OP_rd%d( testnum, inst,  val1, val2, mask_addr ) "%n + " \\\n\
        TEST_CASE_W_FP( testnum, v%d, "%n + "\\\n\
            VSET_VSEW_4AVL \\\n\
            la x7, rd_origin_data; \\\n\
            vle%d.v v%d, (x7);"%((vsew*2 if vsew < 64 else 64), n) + " \\\n\
            la x7, val1; \\\n\
            vle%d.v v%d, (x7);"%((vsew*2 if vsew < 64 else 64), rs1) + " \\\n\
            la x7, val2; \\\n\
            vle%d.v v%d, (x7);"%(vsew, rs2) + " \\\n\
            %s "%("la x7, mask_addr; \\\n    vlm.v v0, (x7); \\\n  "if masked else "")+" \
            inst v%d, v%d, v%d%s;"%(n, rs2, rs1, (", v0.t" if masked else "")) + " \\\n\
        )",file=f)


def generate_tests_vfwred(f, vlen, vsew, lmul, rs1_val, rs2_val):
    num_elem = int(vlen * lmul / vsew)
    if num_elem == 0:
        return 0
    loop_num = int(min(len(rs1_val), len(rs2_val)) / num_elem)
    step_bytes = int(vlen * lmul / 8)
    step_bytes_double = step_bytes * 2
    
    vlmax = num_elem
    mask_bytes = 4 * math.ceil(vlmax / 32) # 4 * num_words
    mask_num = vlmax * 2 + 4
    j = 0
    
    n = 0
    print("  #-------------------------------------------------------------",file=f)
    print("  # vfwredosum Tests",file=f)
    print("  #-------------------------------------------------------------",file=f)
    
    for i in range(loop_num):
        n += 1
        print("  TEST_W_FP_RED_OP( "+str(n)+",  vfwredosum.vs,  "+"rs1_data_widen+%d, rs2_data+%d, mask_data+%d)"%(i*step_bytes_double, i*step_bytes, j*mask_bytes),file=f)
        j = (j + 1) % mask_num

    print("  #-------------------------------------------------------------",file=f)
    print("  # vfwredusum Tests",file=f)
    print("  #-------------------------------------------------------------",file=f)
    
    for i in range(loop_num):
        n += 1
        print("  TEST_W_FP_RED_OP( "+str(n)+",  vfwredusum.vs,  "+"rs1_data_widen+%d, rs2_data+%d, mask_data+%d)"%(i*step_bytes_double, i*step_bytes, j*mask_bytes),file=f)
        j = (j + 1) % mask_num

    print("  #-------------------------------------------------------------",file=f)
    print("  # vfwredosum Tests (different register)",file=f)
    print("  #-------------------------------------------------------------",file=f)
    
    for i in range(min(32, loop_num)):
        k = i % 31 + 1
        
        if k % lmul != 0:
            continue
        n += 1
        print("  TEST_W_FP_RED_OP_rs2%d( "%k+str(n)+",  vfwredosum.vs,  "+"rs1_data_widen+%d, rs2_data+%d, mask_data+%d)"%( i*step_bytes_double, i*step_bytes, j*mask_bytes),file=f)
        j = (j + 1) % mask_num
        
        if k % (2*lmul) != 0:
            continue
        n += 1
        print("  TEST_W_FP_RED_OP_rs1%d( "%k+str(n)+",  vfwredosum.vs,  "+"rs1_data_widen+%d, rs2_data+%d, mask_data+%d)"%( i*step_bytes_double, i*step_bytes, j*mask_bytes),file=f)
        j = (j + 1) % mask_num
        n += 1
        print("  TEST_W_FP_RED_OP_rd%d( "%k+str(n)+",  vfwredosum.vs,  "+"rs1_data_widen+%d, rs2_data+%d, mask_data+%d)"%( i*step_bytes_double, i*step_bytes, j*mask_bytes),file=f)
        j = (j + 1) % mask_num
    
    print("  #-------------------------------------------------------------",file=f)
    print("  # vfwredusum Tests (different register)",file=f)
    print("  #-------------------------------------------------------------",file=f)
    
    for i in range(min(32, loop_num)):
        k = i % 31 + 1
        
        if k % lmul != 0:
            continue
        n += 1
        print("  TEST_W_FP_RED_OP_rs2%d( "%k+str(n)+",  vfwredusum.vs,  "+"rs1_data_widen+%d, rs2_data+%d, mask_data+%d)"%( i*step_bytes_double, i*step_bytes, j*mask_bytes),file=f)
        j = (j + 1) % mask_num
        
        if k % (2*lmul) != 0:
            continue
        n += 1
        print("  TEST_W_FP_RED_OP_rs1%d( "%k+str(n)+",  vfwredusum.vs,  "+"rs1_data_widen+%d, rs2_data+%d, mask_data+%d)"%( i*step_bytes_double, i*step_bytes, j*mask_bytes),file=f)
        j = (j + 1) % mask_num
        n += 1
        print("  TEST_W_FP_RED_OP_rd%d( "%k+str(n)+",  vfwredusum.vs,  "+"rs1_data_widen+%d, rs2_data+%d, mask_data+%d)"%( i*step_bytes_double, i*step_bytes, j*mask_bytes),file=f)
        j = (j + 1) % mask_num
        
    return n


def create_empty_test_vfwredsum(xlen, vlen, vsew, lmul, vta, vma, output_dir):
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


def create_first_test_vfwredsum(xlen, vlen, vsew, lmul, vta, vma, output_dir, rpt_path):
    logging.info("Creating first test for {}".format(instr))

    path = "%s/%s_first.S" % (output_dir, instr)
    f = open(path, "w+")

    # Common header files
    print_common_header(instr, f)

    # Extract operands
    rs1_val, rs2_val = extract_operands_fp(f, rpt_path)

    # Generate macros to test diffrent register
    generate_macros_vfwred(f, vsew, lmul)

    # Generate tests
    n = generate_tests_vfwred(f, vlen, vsew, lmul, rs1_val, rs2_val)

    # Common const information
    print_common_ending_rs1rs2rd_wvwf(rs1_val, rs2_val, (0,0,n,0), vsew, f, generate_vv=False, generate_vf=False, generate_wvwf=False, is_reduction=True)

    f.close()
    os.system("cp %s %s" % (path, output_dir))

    logging.info(
        "Creating first test for {}: finish in {}!".format(instr, path))

    return path
