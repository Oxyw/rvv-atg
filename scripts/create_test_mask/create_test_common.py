import os
import math
import random
from scripts.test_common_info import print_data_width_prefix, gen_arr_compute, print_rvmodel_data, valid_aligned_regs, print_mask_data_ending, print_origin_data_ending


def generate_walking_data_seg_common(element_num, vlen, vsew, f):
    # Generate walking ones
    for i in range(element_num + 1):
        print("walking_ones_dat%d:" % i, file=f)
        for j in range(element_num):
            print("\t", end="", file=f)
            print_data_width_prefix(f, vsew)
            print("0x1" if i == j + 1 else "0x0", file=f)
        print("", file=f)

    # Generate walking zeros
    for i in range(element_num + 1):
        print("walking_zeros_dat%d:" % i, file=f)
        for j in range(element_num):
            print("\t", end="", file=f)
            print_data_width_prefix(f, vsew)
            print("0x0" if i == j + 1 else "0x1", file=f)
        print("", file=f)


def generate_macros_common(f):
    print("#define TEST_VMRL_OP( testnum, inst, sew,  src1_addr, src2_addr ) \\\n\
    TEST_CASE_VREG( testnum, v24, 1,  \\\n\
        VSET_VSEW_4AVL \\\n\
        la  x1, src1_addr; \\\n\
        MK_VLE_INST(sew) v8, (x1); \\\n\
        la  x1, src2_addr; \\\n\
        MK_VLE_INST(sew) v16, (x1); \\\n\
        vmseq.vi v1, v8, 1; \\\n\
        vmseq.vi v2, v16, 1; \\\n\
        inst v24, v2, v1; \\\n\
    )", file=f)
    for n in range(1, 32):
        print("#define TEST_VMRL_OP_vs1_%d( testnum, inst, sew,  src1_addr, src2_addr ) \\\n\
        TEST_CASE_VREG( testnum, v24, 1,  \\\n\
            VSET_VSEW_4AVL \\\n\
            la  x1, src1_addr; \\\n\
            MK_VLE_INST(sew) v8, (x1); \\\n\
            la  x1, src2_addr; \\\n\
            MK_VLE_INST(sew) v16, (x1); \\\n\
            vmseq.vi v%d, v8, 1; \\\n\
            vmseq.vi v2, v16, 1; \\\n\
            inst v24, v2, v%d; \\\n\
        )" % (n, n, n), file=f)
    for n in range(1, 32):
        vs1, vs2 = valid_aligned_regs(n)
        print("#define TEST_VMRL_OP_vd_%d( testnum, inst, sew,  src1_addr, src2_addr ) \\\n\
        TEST_CASE_VREG( testnum, v%d, 1,  \\\n\
            VSET_VSEW_4AVL \\\n\
            la  x1, src1_addr; \\\n\
            MK_VLE_INST(sew) v8, (x1); \\\n\
            la  x1, src2_addr; \\\n\
            MK_VLE_INST(sew) v16, (x1); \\\n\
            vmseq.vi v%d, v8, 1; \\\n\
            vmseq.vi v%d, v16, 1; \\\n\
            inst v%d, v%d, v%d; \\\n\
        )" % (n, n, vs1, vs2, n, vs2, vs1), file=f)


def generate_tests_common(instr, f, vlen, vsew, lmul):
    n = 0
    print("  #-------------------------------------------------------------", file=f)
    print("  # %s tests" % instr, file=f)
    print("  #-------------------------------------------------------------", file=f)
    num_elem = int(vlen * lmul / vsew)
    num_elem_plus = num_elem + 1
    num_elem_plus_square = num_elem_plus ** 2
    num_elem_plus_square_old = num_elem_plus_square
    # If there are too many tests ( > 1000), only test some of them
    percentage = 1000 / (4 * num_elem_plus_square)
    for i in range(0, num_elem_plus_square):
        if random.random() < percentage:
            n = n + 1
            print("TEST_VMRL_OP( %d,  %s.mm,  %d,   walking_ones_dat%d, walking_ones_dat%d );" % (
                n, instr, (vsew if vsew <= 64 else 64), i / num_elem_plus, i % num_elem_plus), file=f)

    for i in range(num_elem_plus_square, num_elem_plus_square * 2):
        if random.random() < percentage:
            n = n + 1
            print("TEST_VMRL_OP( %d,  %s.mm,  %d,   walking_zeros_dat%d, walking_zeros_dat%d );" % (
                n, instr, (vsew if vsew <= 64 else 64), (i - num_elem_plus_square) / num_elem_plus, (i - num_elem_plus_square) % num_elem_plus), file=f)

    num_elem_plus_square = num_elem_plus_square + num_elem_plus_square_old
    for i in range(num_elem_plus_square, num_elem_plus_square + num_elem_plus_square_old):
        if random.random() < percentage:
            n = n + 1
            print("TEST_VMRL_OP( %d,  %s.mm,  %d,   walking_ones_dat%d, walking_zeros_dat%d );" % (
                n, instr, (vsew if vsew <= 64 else 64), (i - num_elem_plus_square) / num_elem_plus, (i - num_elem_plus_square) % num_elem_plus), file=f)

    num_elem_plus_square = num_elem_plus_square + num_elem_plus_square_old
    for i in range(num_elem_plus_square, num_elem_plus_square + num_elem_plus_square_old):
        if random.random() < percentage:
            n = n + 1
            print("TEST_VMRL_OP( %d,  %s.mm,  %d,   walking_zeros_dat%d, walking_ones_dat%d );" % (
                n, instr, (vsew if vsew <= 64 else 64), (i - num_elem_plus_square) / num_elem_plus, (i - num_elem_plus_square) % num_elem_plus), file=f)
    
    # Fully Cover rs2_val
    num_elem_plus_square = num_elem_plus_square + num_elem_plus_square_old
    for i in range(num_elem_plus_square, num_elem_plus_square + num_elem_plus):
        if random.random() < percentage:
            n = n + 1
            print("TEST_VMRL_OP( %d,  %s.mm,  %d,   walking_ones_dat%d, walking_zeros_dat%d );" % (
                n, instr, (vsew if vsew <= 64 else 64), i - num_elem_plus_square, i - num_elem_plus_square), file=f)

    num_elem_plus_square = num_elem_plus_square + num_elem_plus
    for i in range(num_elem_plus_square, num_elem_plus_square + num_elem_plus):
        if random.random() < percentage:
            n = n + 1
            print("TEST_VMRL_OP( %d,  %s.mm,  %d,   walking_zeros_dat%d, walking_ones_dat%d );" % (
                n, instr, (vsew if vsew <= 64 else 64), i - num_elem_plus_square, i - num_elem_plus_square), file=f)

    return n


def print_ending_common(vlen, vsew, lmul, f, n, is_rd = False):
    xlen = int(os.environ['RVV_ATG_XLEN'])
    
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
    
    num_elem = int(vlen * lmul / vsew)
    generate_walking_data_seg_common(num_elem, int(vlen), int(vsew), f)
    
    print_mask_data_ending(f, num_elem)
    
    if is_rd:
        print_origin_data_ending(f, int(xlen / 8))
    else:
        print_origin_data_ending(f, int(vlen / 8))

    print("\n\
    RVTEST_DATA_END\n", file=f)
    arr = gen_arr_compute(n, is_reduction = is_rd, is_mask = not is_rd)
    print_rvmodel_data(arr, f)


def generate_macros_vs2(f, is_vd = True):
    masked = True if os.environ['RVV_ATG_MASKED'] == "True" else False
    # rd: vcpop, vfirst
    # vd: vmsbf, vmsif, vmsof
    destflag = "V" if is_vd else "X"
    destreg = "v16" if is_vd else "x22"
    destload = "vl1r.v" if is_vd else "ld" # TODO
    
    print("#define TEST_%sDVS2_OP( testnum, inst,  src_addr, mask_addr ) "%(destflag) + " \\\n\
    TEST_CASE_%sREG(testnum, %s, "%(destflag, destreg) + " \\\n\
        VSET_VSEW_4AVL \\\n\
        la x7, rd_origin_data; \\\n\
        %s %s, (x7);"%(destload, destreg) + " \\\n\
        la  x2, src_addr; \\\n\
        vlm.v v8, (x2); \\\n\
        %s "%("la x7, mask_addr; \\\n    vlm.v v0, (x7); \\\n  "if masked else "")+" \
        inst %s, v8%s; "%(destreg, ", v0.t" if masked else "") + " \\\n\
    )", file=f)
    
    for i in range(1, 32):
        # vd != vs2
        if is_vd and i == 16:
            destreg = "v8"
        print("#define TEST_%sDVS2_OP_vs2_%d( testnum, inst,  src_addr, mask_addr )"%(destflag, i) + " \\\n\
        TEST_CASE_%sREG(testnum, %s, "%(destflag, destreg) + " \\\n\
            VSET_VSEW_4AVL \\\n\
            la x7, rd_origin_data; \\\n\
            %s %s, (x7);"%(destload, destreg) + " \\\n\
            la  x2, src_addr; \\\n\
            vlm.v v%d, (x2);"%(i)+" \\\n\
            %s "%("la x7, mask_addr; \\\n    vlm.v v0, (x7); \\\n  "if masked else "")+" \
            inst %s, v%d%s; "%(destreg, i, (", v0.t" if masked else "")) + " \\\n\
        )", file=f)
    
    if is_vd:
        for i in range(1, 32):
            vs2 = 16 if i == 8 else 8
            print("#define TEST_VDVS2_OP_vd_%d( testnum, inst,  src_addr, mask_addr )"%i + " \\\n\
            TEST_CASE_VREG(testnum, v%d, 1, "%i + " \\\n\
                VSET_VSEW_4AVL \\\n\
                la x7, rd_origin_data; \\\n\
                vl1r.v v%d, (x7);"%i + " \\\n\
                la  x2, src_addr; \\\n\
                vlm.v v%d, (x2);"%(vs2)+" \\\n\
                %s "%("la x7, mask_addr; \\\n    vlm.v v0, (x7); \\\n  "if masked else "")+" \
                inst v%d, v%d%s; "%(i, vs2, (", v0.t" if masked else "")) + " \\\n\
            )", file=f)


def generate_tests_vs2(instr, f, vlen, vsew, lmul, is_vd = True):
    # rd: vcpop, vfirst
    # vd: vmsbf, vmsif, vmsof
    destflag = "V" if is_vd else "X"
    
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
        print("TEST_%sDVS2_OP( %d,  %s.m, mask_data+%d, mask_data+%d );" % (destflag, n, instr, i*mask_bytes, j*mask_bytes), file=f)
        j = (j + 1) % mask_num

    print("  #-------------------------------------------------------------", file=f)
    print("  # %s Tests (different register)" % instr, file=f)
    print("  #-------------------------------------------------------------", file=f)
    
    for i in range(1, 32):
        n += 1
        print("TEST_%sDVS2_OP_vs2_%d( %d,  %s.m, mask_data+%d, mask_data+%d );" % (destflag, i, n, instr, (i%mask_num)*mask_bytes, j*mask_bytes), file=f)
        j = (j + 1) % mask_num
    
    if is_vd:
        for i in range(1, 32):
            n += 1
            print("TEST_%sDVS2_OP_vd_%d( %d,  %s.m, mask_data+%d, mask_data+%d );" % (destflag, i, n, instr, (i%mask_num)*mask_bytes, j*mask_bytes), file=f)
            j = (j + 1) % mask_num
    
    return n