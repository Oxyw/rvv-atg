from scripts.test_common_info import *


# including walking_ones, walking_zeros and special_dataset
coverpoints_16 = [-32768, -21846, -21845, -16385, -8193, -4097, -2049, -1025, -513, -257, -181, -180, -129, -65, -33, -17, -9, -5, -3, -2, 0, 1, 2, 3, 4, 5, 6, 8, 16, 32, 64, 128, 180, 181, 182, 256, 512, 1024, 2048, 4096, 8192, 13106, 13107, 13108, 16384, 21844, 21845, 21846, 26213, 26214, 26215, 32767]

coverpoints_32 = [-2147483648, -1431655766, -1431655765, -1073741825, -536870913, -268435457, -134217729, -67108865, -33554433, -16777217, -8388609, -4194305, -2097153, -1048577, -524289, -262145, -131073, -65537, -46340, -46339, -32769, -16385, -8193, -4097, -2049, -1025, -513, -257, -129, -65, -33, -17, -9, -5, -3, -2, 0, 1, 2, 3, 4, 5, 6, 8, 16, 32, 64, 128, 256, 512, 1024, 2048, 4096, 8192, 16384, 32768, 46339, 46340, 46341, 65536, 131072, 262144, 524288, 1048576, 2097152, 4194304, 8388608, 16777216, 33554432, 67108864, 134217728, 268435456, 536870912, 858993458, 858993459, 858993460, 1073741824, 1431655764, 1431655765, 1431655766, 1717986917, 1717986918, 1717986919, 2147483647]

coverpoints_64 = [-9223372036854775808, -6148914691236517206, -6148914691236517205, -4611686018427387905, -2305843009213693953, -1152921504606846977, -576460752303423489, -288230376151711745, -144115188075855873, -72057594037927937, -36028797018963969, -18014398509481985, -9007199254740993, -4503599627370497, -2251799813685249, -1125899906842625, -562949953421313, -281474976710657, -140737488355329, -70368744177665, -35184372088833, -17592186044417, -8796093022209, -4398046511105, -2199023255553, -1099511627777, -549755813889, -274877906945, -137438953473, -68719476737, -34359738369, -17179869185, -8589934593, -4294967297, -3037000499, -3037000498, -2147483649, -1073741825, -536870913, -268435457, -134217729, -67108865, -33554433, -16777217, -8388609, -4194305, -2097153, -1048577, -524289, -262145, -131073, -65537, -32769, -16385, -8193, -4097, -2049, -1025, -513, -257, -129, -65, -33, -17, -9, -5, -3, -2, 0, 1, 2, 3, 4, 5, 6, 8, 16, 32, 64, 128, 256, 512, 1024, 2048, 4096, 8192, 16384, 32768, 65536, 131072, 262144, 524288, 1048576, 2097152, 4194304, 8388608, 16777216, 33554432, 67108864, 134217728, 268435456, 536870912, 1073741824, 2147483648, 3037000498, 3037000499, 3037000500, 4294967296, 8589934592, 17179869184, 34359738368, 68719476736, 137438953472, 274877906944, 549755813888, 1099511627776, 2199023255552, 4398046511104, 8796093022208, 17592186044416, 35184372088832, 70368744177664, 140737488355328, 281474976710656, 562949953421312, 1125899906842624, 2251799813685248, 4503599627370496, 9007199254740992, 18014398509481984, 36028797018963968, 72057594037927936, 144115188075855872, 288230376151711744, 576460752303423488, 1152921504606846976, 2305843009213693952, 3689348814741910322, 3689348814741910323, 3689348814741910324, 4611686018427387904, 6148914691236517204, 6148914691236517205, 6148914691236517206, 7378697629483820645, 7378697629483820646, 7378697629483820647, 9223372036854775807]

def extract_operands_const():
    val_10 = list(set(coverpoints_16) | set(coverpoints_32) | set(coverpoints_64))
    val = ['{:#016x}'.format(int(x) & 0xffffffffffffffff)
            for x in val_10]
    return val



def print_ending_mv(f, rs_val, test_num_tuple, vlen, vsew, lmul, is_fp = False, is_vmvnr = False, print_mask = False):
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
    
    if is_fp:
        print(".align %d"%(8 if vsew == 64 else 4), file=f)
        print("fdat_rs:", file=f)
        for i in range(len(rs_val)):
            print("fdat_rs_" + str(i) + ":  .%s "%("dword" if vsew == 64 else "word") + rs_val[i], file=f)
    else:
        print(".align %d"%(int(vsew / 8)), file=f)
        print("rs_data:", file=f)
        for i in range(len(rs_val)):
            print_data_width_prefix(f, vsew)
            print("%s"%rs_val[i], file=f)

    if (print_mask):
        print_mask_origin_data_ending(f)
    else:
        print_origin_data_ending(f, int(vlen * lmul / 8))

    print("\n\
    RVTEST_DATA_END\n", file=f)
    num_elem = int(vlen * lmul / vsew)
    print(test_num_tuple)
    num_tests = sum(test_num_tuple)
    xfvcsr_num = 11  # 1 xcsr, 3 fcsr, 7 vcsr
    
    if is_vmvnr:
        vreg_num = sum(value * (2 ** index) for index, value in enumerate(test_num_tuple))
        arr = [0, xfvcsr_num * num_tests, vreg_num]
    else:
        arr = [0, (test_num_tuple[0] + num_elem * test_num_tuple[1]) + xfvcsr_num * num_tests, 0]
    print_rvmodel_data(arr, f)


def generate_macros_vslide(f, vsew, lmul, generate_vx = True, generate_vi = False):
    masked = True if os.environ['RVV_ATG_MASKED'] == "True" else False
    
    if generate_vx:
        print("#define TEST_VX_OP( testnum, inst, val2, val1, mask_addr ) \\\n\
        TEST_CASE_LOOP( testnum, v16, \\\n\
            VSET_VSEW_4AVL \\\n\
            la x7, rd_origin_data; \\\n\
            vle%d.v v16, (x7);"%vsew + " \\\n\
            %s "%("la x7, mask_addr; \\\n        vlm.v v0, (x7); \\\n  "if masked else "")+" \
            la x7, val2; \\\n\
            vle%d.v v8, (x7);"%vsew + " \\\n\
            li x1, MASK_XLEN(val1); \\\n\
            inst v16, v8, x1%s;"%(", v0.t" if masked else "") + " \\\n\
        )", file=f)
        for n in range(1, 32):
            if n % lmul != 0:
                continue
            vd = 24 if n == 16 else 16
            print("#define TEST_VX_OP_vs2_%d( testnum, inst, val2, val1, mask_addr ) "%n + " \\\n\
            TEST_CASE_LOOP( testnum, v%d,  "%vd + "    \\\n\
                VSET_VSEW_4AVL \\\n\
                la x7, rd_origin_data; \\\n\
                vle%d.v v%d, (x7);"%(vsew, vd) + " \\\n\
                %s "%("la x7, mask_addr; \\\n        vlm.v v0, (x7); \\\n  "if masked else "")+" \
                la x7, val2; \\\n\
                vle%d.v v%d, (x7);"%(vsew, n) + " \\\n\
                li x1, MASK_XLEN(val1); \\\n\
                inst v%d, v%d, x1%s; "%(vd, n, (", v0.t" if masked else "")) + " \\\n\
            )", file=f)
        for n in range(1, 32):
            if n % lmul != 0:
                continue
            vs2 = 24 if n == 8 else 8
            print("#define TEST_VX_OP_vd_%d( testnum, inst, val2, val1, mask_addr ) "%n + " \\\n\
            TEST_CASE_LOOP( testnum, v%d,  "%n + "\\\n\
                VSET_VSEW_4AVL \\\n\
                la x7, rd_origin_data; \\\n\
                vle%d.v v%d, (x7);"%(vsew, n) + " \\\n\
                %s "%("la x7, mask_addr; \\\n        vlm.v v0, (x7); \\\n  "if masked else "")+" \
                la x7, val2; \\\n\
                vle%d.v v%d, (x7);"%(vsew, vs2) + " \\\n\
                li x1, MASK_XLEN(val1); \\\n\
                inst v%d, v%d, x1%s; "%(n, vs2, (", v0.t" if masked else "")) + " \\\n\
            ) ", file=f)
    
    if generate_vi:
        print("#define TEST_VI_OP( testnum, inst, val2, val1, mask_addr ) \\\n\
        TEST_CASE_LOOP( testnum, v16, \\\n\
            VSET_VSEW_4AVL \\\n\
            la x7, rd_origin_data; \\\n\
            vle%d.v v16, (x7);"%vsew + " \\\n\
            %s "%("la x7, mask_addr; \\\n        vlm.v v0, (x7); \\\n  "if masked else "")+" \
            la x7, val2; \\\n\
            vle%d.v v8, (x7);"%vsew + " \\\n\
            inst v16, v8, SEXT_IMM(val1)%s;"%(", v0.t" if masked else "") + " \\\n\
        )", file=f)


def generate_tests_vslide(instr, direction, f, vsew, lmul, rs1_val, rs2_val, generate_vx = True, generate_vi = False):
    vlen = int(os.environ['RVV_ATG_VLEN'])
    
    num_elem = int(vlen * lmul / vsew)
    if num_elem == 0:
        return 0
    loop_num = int(min(len(rs1_val), len(rs2_val)) / num_elem)
    step_bytes = int(vlen * lmul / 8)
    vlmax = num_elem
    mask_bytes = 4 * math.ceil(vlmax / 32) # 4 * num_words
    mask_num = vlmax * 2 + 4
    j = 0
    
    n = 0
    if generate_vx:
        print("  #-------------------------------------------------------------", file=f)
        print("  # VX Tests", file=f)
        print("  #-------------------------------------------------------------", file=f)
        for i in range(loop_num):
            for dirct in direction:
                n += 1
                print("  TEST_VX_OP( "+str(n)+",  %s%s.vx, " %(instr, dirct)+" rs2_data+%d, %s, mask_data+%d)"%(i*step_bytes, rs1_val[i], j*mask_bytes), file=f)
                j = (j + 1) % mask_num
        
        for i in range(1, 32):     
            if i % lmul != 0:
                continue
            k = i % loop_num
            for dirct in direction:
                n += 1
                print("  TEST_VX_OP_vd_%d( "%i+str(n)+",  %s%s.vx, "%(instr, dirct)+" rs2_data+%d, %s, mask_data+%d)"%(k*step_bytes, rs1_val[i % len(rs1_val)], j*mask_bytes),file=f)
                j = (j + 1) % mask_num
                n += 1
                print("  TEST_VX_OP_vs2_%d( "%i+str(n)+",  %s%s.vx, "%(instr, dirct)+" rs2_data+%d, %s, mask_data+%d)"%(k*step_bytes, rs1_val[i % len(rs1_val)], j*mask_bytes),file=f)
                j = (j + 1) % mask_num
    vx_test_num = n
    
    if generate_vi:
        print("  #-------------------------------------------------------------", file=f)
        print("  # VI Tests", file=f)
        print("  #-------------------------------------------------------------", file=f)
        for i in range(loop_num):
            for dirct in direction:
                n += 1
                print("  TEST_VI_OP( "+str(n)+",  %s%s.vi, " %(instr, dirct)+"rs2_data+%d, 7, mask_data+%d)"%(i*step_bytes, j*mask_bytes), file=f)
                j = (j + 1) % mask_num
    vi_test_num = n - vx_test_num
    
    return (0, vx_test_num, vi_test_num)


def generate_macros_vrgather(f, vsew, lmul, is_ei16 = False):
    masked = True if os.environ['RVV_ATG_MASKED'] == "True" else False
    
    eew1 = 16 if is_ei16 else vsew
    emul1 = (16 / vsew) * lmul if is_ei16 else lmul
    
    print("#define TEST_VV_OP( testnum, inst, val2, val1, mask_addr ) \\\n\
    TEST_CASE_LOOP( testnum, v24, \\\n\
        VSET_VSEW_4AVL \\\n\
        la x7, rd_origin_data; \\\n\
        vle%d.v v24, (x7);"%vsew + " \\\n\
        %s "%("la x7, mask_addr; \\\n    vlm.v v0, (x7); \\\n  "if masked else "")+" \
        la x7, val2; \\\n\
        vle%d.v v16, (x7);"%vsew + " \\\n\
        la x7, val1; \\\n\
        vle%d.v v8, (x7);"%eew1 + " \\\n\
        inst v24, v16, v8%s;"%(", v0.t" if masked else "") + " \\\n\
    )", file=f)
    for n in range(1, 32):
        if n % emul1 != 0:
            continue
        vd, vs2 = get_aligned_regs(n, emul1, lmul, lmul)
        if vd == vs2 == 0:
            continue
        print("#define TEST_VV_OP_vs1_%d( testnum, inst, val2, val1, mask_addr )"%n + " \\\n\
        TEST_CASE_LOOP( testnum, v%d, "%vd + " \\\n\
            VSET_VSEW_4AVL \\\n\
            la x7, rd_origin_data; \\\n\
            vle%d.v v%d, (x7);"%(vsew, vd) + " \\\n\
            %s "%("la x7, mask_addr; \\\n    vlm.v v0, (x7); \\\n  "if masked else "")+" \
            la x7, val2; \\\n\
            vle%d.v v%d, (x7);"%(vsew, vs2) + " \\\n\
            la x7, val1; \\\n\
            vle%d.v v%d, (x7);"%(eew1, n)  + " \\\n\
            inst v%d, v%d, v%d%s; "%(vd, vs2, n, (", v0.t" if masked else "")) + " \\\n\
        )", file=f)
    for n in range(1, 32):
        if n % lmul != 0:
            continue
        vs2, vs1 = get_aligned_regs(n, lmul, lmul, emul1)
        if vs2 == vs1 == 0:
            continue          
        print("#define TEST_VV_OP_vd_%d( testnum, inst, val2, val1, mask_addr )"%n + " \\\n\
        TEST_CASE_LOOP( testnum, v%d, "%n + " \\\n\
            VSET_VSEW_4AVL \\\n\
            la x7, rd_origin_data; \\\n\
            vle%d.v v%d, (x7);"%(vsew, n) + " \\\n\
            %s "%("la x7, mask_addr; \\\n    vlm.v v0, (x7); \\\n  "if masked else "")+" \
            la x7, val2; \\\n\
            vle%d.v v%d, (x7);"%(vsew, vs2) + " \\\n\
            la x7, val1; \\\n\
            vle%d.v v%d, (x7);"%(eew1, vs1) + " \\\n\
            inst v%d, v%d, v%d%s;"%(n, vs2, vs1, (", v0.t" if masked else ""))+" \\\n\
        ) ", file=f)
    
    if is_ei16 == False:
        print("#define TEST_VX_OP( testnum, inst, val2, val1, mask_addr ) \\\n\
        TEST_CASE_LOOP( testnum, v16, \\\n\
            VSET_VSEW_4AVL \\\n\
            la x7, rd_origin_data; \\\n\
            vle%d.v v16, (x7);"%vsew + " \\\n\
            %s "%("la x7, mask_addr; \\\n    vlm.v v0, (x7); \\\n  "if masked else "")+" \
            la x7, val2; \\\n\
            vle%d.v v8, (x7);"%vsew + " \\\n\
            li x1, MASK_XLEN(val1); \\\n\
            inst v16, v8, x1%s;"%(", v0.t" if masked else "") + " \\\n\
        )", file=f)
        for n in range(1, 32):
            if n % lmul != 0:
                continue
            vd = 24 if n == 16 else 16
            print("#define TEST_VX_OP_vs2_%d( testnum, inst, val2, val1, mask_addr ) "%n + " \\\n\
            TEST_CASE_LOOP( testnum, v%d,  "%vd + "    \\\n\
                VSET_VSEW_4AVL \\\n\
                la x7, rd_origin_data; \\\n\
                vle%d.v v%d, (x7);"%(vsew, vd) + " \\\n\
                %s "%("la x7, mask_addr; \\\n        vlm.v v0, (x7); \\\n  "if masked else "")+" \
                la x7, val2; \\\n\
                vle%d.v v%d, (x7);"%(vsew, n) + " \\\n\
                li x1, MASK_XLEN(val1); \\\n\
                inst v%d, v%d, x1%s; "%(vd, n, (", v0.t" if masked else "")) + " \\\n\
            )", file=f)
        for n in range(1, 32):
            if n % lmul != 0:
                continue
            vs2 = 24 if n == 8 else 8
            print("#define TEST_VX_OP_vd_%d( testnum, inst, val2, val1, mask_addr ) "%n + " \\\n\
            TEST_CASE_LOOP( testnum, v%d,  "%n + "\\\n\
                VSET_VSEW_4AVL \\\n\
                la x7, rd_origin_data; \\\n\
                vle%d.v v%d, (x7);"%(vsew, n) + " \\\n\
                %s "%("la x7, mask_addr; \\\n        vlm.v v0, (x7); \\\n  "if masked else "")+" \
                la x7, val2; \\\n\
                vle%d.v v%d, (x7);"%(vsew, vs2) + " \\\n\
                li x1, MASK_XLEN(val1); \\\n\
                inst v%d, v%d, x1%s; "%(n, vs2, (", v0.t" if masked else "")) + " \\\n\
            ) ", file=f)
        
        print("#define TEST_VI_OP( testnum, inst, val2, val1, mask_addr ) \\\n\
        TEST_CASE_LOOP( testnum, v16, \\\n\
            VSET_VSEW_4AVL \\\n\
            la x7, rd_origin_data; \\\n\
            vle%d.v v16, (x7);"%vsew + " \\\n\
            %s "%("la x7, mask_addr; \\\n    vlm.v v0, (x7); \\\n  "if masked else "")+" \
            la x7, val2; \\\n\
            vle%d.v v8, (x7);"%vsew + " \\\n\
            inst v16, v8, SEXT_IMM(val1)%s;"%(", v0.t" if masked else "") + " \\\n\
        )", file=f)


def generate_tests_vrgather(instr, f, rs1_val, rs2_val, vsew, lmul, is_ei16 = False):
    vlen = int(os.environ['RVV_ATG_VLEN'])
    
    eew1 = 16 if is_ei16 else vsew
    emul1 = (16 / vsew) * lmul if is_ei16 else lmul
    
    num_elem = int(vlen * lmul / vsew)
    if num_elem == 0:
        return 0
    loop_num = int(min(len(rs1_val), len(rs2_val)) / num_elem)
    step_bytes = int(vlen * lmul / 8)
    
    vlmax = num_elem
    mask_bytes = 4 * math.ceil(vlmax / 32) # 4 * num_words
    mask_num = vlmax * 2 + 4
    j = 0
    
    n = 0
    
    print("  #-------------------------------------------------------------", file=f)
    print("  # VV Tests", file=f)
    print("  #-------------------------------------------------------------", file=f)
    for i in range(loop_num):
        n += 1
        print("  TEST_VV_OP( "+str(n)+",  %s.vv, "%instr + "rs2_data+%d, rs1_data+%d, mask_data+%d)"%(i*step_bytes, i*step_bytes, j*mask_bytes), file=f)
        j = (j + 1) % mask_num
    for i in range(1, 32):     
        if i % lmul != 0 or get_aligned_regs(i, lmul, lmul, emul1) == (0, 0):
            continue
        k = i % loop_num
        n += 1
        print("  TEST_VV_OP_vd_%d( "%i+str(n)+",  %s.vv, "%instr+"rs2_data+%d, rs1_data+%d, mask_data+%d)"%(k*step_bytes, k*step_bytes, j*mask_bytes),file=f)
        j = (j + 1) % mask_num
    for i in range(1, 32):     
        if i % emul1 != 0 or get_aligned_regs(i, emul1, lmul, lmul) == (0, 0):
            continue
        k = i % loop_num
        n += 1
        print("  TEST_VV_OP_vs1_%d( "%i+str(n)+",  %s.vv, "%instr+"rs2_data+%d, rs1_data+%d, mask_data+%d)"%(k*step_bytes, k*step_bytes, j*mask_bytes),file=f)
        j = (j + 1) % mask_num
    vv_test_num = n

    if is_ei16 == False:
        print("  #-------------------------------------------------------------", file=f)
        print("  # VX Tests", file=f)
        print("  #-------------------------------------------------------------", file=f)
        for i in range(loop_num):
            n += 1
            print("  TEST_VX_OP( "+str(n)+",  %s.vx, " %instr+" rs2_data+%d, %s, mask_data+%d)"%(i*step_bytes, rs1_val[i], j*mask_bytes), file=f)
            j = (j + 1) % mask_num
        for i in range(1, 32):     
            if i % lmul != 0:
                continue
            k = i % loop_num
            n += 1
            print("  TEST_VX_OP_vd_%d( "%i+str(n)+",  %s.vx, "%instr+" rs2_data+%d, %s, mask_data+%d)"%(k*step_bytes, rs1_val[i % len(rs1_val)], j*mask_bytes),file=f)
            j = (j + 1) % mask_num
            
            n += 1
            print("  TEST_VX_OP_vs2_%d( "%i+str(n)+",  %s.vx, "%instr+" rs2_data+%d, %s, mask_data+%d)"%(k*step_bytes, rs1_val[i % len(rs1_val)], j*mask_bytes),file=f)
            j = (j + 1) % mask_num
    vx_test_num = n - vv_test_num
    
    if is_ei16 == False:
        print("  #-------------------------------------------------------------", file=f)
        print("  # VI Tests", file=f)
        print("  #-------------------------------------------------------------", file=f)
        for i in range(loop_num):
            n += 1
            print("  TEST_VI_OP( "+str(n)+",  %s.vi, " %instr+"rs2_data+%d, 9, mask_data+%d)"%(i*step_bytes, j*mask_bytes), file=f)
            j = (j + 1) % mask_num
    vi_test_num = n - vv_test_num - vx_test_num

    return (vv_test_num, vx_test_num, vi_test_num)
