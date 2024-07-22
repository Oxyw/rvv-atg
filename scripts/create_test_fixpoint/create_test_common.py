from scripts.test_common_info import valid_aligned_regs, get_aligned_regs
import re, os
import math

def generate_macros(f, lmul, generate_vi = False):
    vsew = int(os.environ['RVV_ATG_VSEW'])
    masked = True if os.environ['RVV_ATG_MASKED'] == "True" else False
    print("#undef TEST_FIXPOINT_VV_OP \n\
#define TEST_FIXPOINT_VV_OP( testnum, inst, vxrm_val, val2, val1, mask_addr ) \\\n\
        TEST_CASE_LOOP( testnum, v24, \\\n\
            VSET_VSEW_4AVL \\\n\
            la x7, rd_origin_data; \\\n\
            vle%d.v v24, (x7);"%vsew + " \\\n\
            %s "%("la x7, mask_addr; \\\n    vlm.v v0, (x7); \\\n  "if masked else "")+" \
            csrwi vxrm, vxrm_val; \\\n\
            la x7, val2; \\\n\
            vle%d.v v16, (x7);"%vsew + " \\\n\
            la x7, val1; \\\n\
            vle%d.v v8, (x7);"%vsew + " \\\n\
            inst v24, v16, v8%s;"%(", v0.t" if masked else "") + " \\\n\
        )", file=f)
    print("#undef TEST_FIXPOINT_VX_OP \n\
#define TEST_FIXPOINT_VX_OP( testnum, inst, vxrm_val, val2, val1, mask_addr ) \\\n\
        TEST_CASE_LOOP( testnum, v24, \\\n\
            VSET_VSEW_4AVL \\\n\
            la x7, rd_origin_data; \\\n\
            vle%d.v v24, (x7);"%vsew + " \\\n\
            %s "%("la x7, mask_addr; \\\n    vlm.v v0, (x7); \\\n  "if masked else "")+" \
            csrwi vxrm, vxrm_val; \\\n\
            la x7, val2; \\\n\
            vle%d.v v16, (x7);"%vsew + " \\\n\
            li x1, MASK_XLEN(val1); \\\n\
            inst v24, v16, x1%s;"%(", v0.t" if masked else "") + " \\\n\
        )", file=f)
    if generate_vi:
        print("#undef TEST_FIXPOINT_VI_OP \n\
    #define TEST_FIXPOINT_VI_OP( testnum, inst, vxrm_val, val2, val1, mask_addr ) \\\n\
        TEST_CASE_LOOP( testnum, v24, \\\n\
            VSET_VSEW_4AVL \\\n\
            la x7, rd_origin_data; \\\n\
            vle%d.v v24, (x7);"%vsew + " \\\n\
            %s "%("la x7, mask_addr; \\\n    vlm.v v0, (x7); \\\n  "if masked else "")+" \
            csrwi vxrm, vxrm_val; \\\n\
            la x7, val2; \\\n\
            vle%d.v v16, (x7);"%vsew + " \\\n\
            inst v24, v16, SEXT_IMM(val1)%s;"%(", v0.t" if masked else "") + " \\\n\
        )", file=f)
    
    for n in range(1, 32):
        if n % lmul != 0:
            continue
        vd, vs2 = valid_aligned_regs(n)
        print("#define TEST_FIXPOINT_VV_OP_vs1_%d( testnum, inst, vxrm_val, val2, val1, mask_addr )"%n + " \\\n\
        TEST_CASE_LOOP( testnum, v%d, "%vd + " \\\n\
            VSET_VSEW_4AVL \\\n\
            la x7, rd_origin_data; \\\n\
            vle%d.v v%d, (x7);"%(vsew, vd) + " \\\n\
            %s "%("la x7, mask_addr; \\\n    vlm.v v0, (x7); \\\n  "if masked else "")+" \
            csrwi vxrm, vxrm_val; \\\n\
            la x7, val2; \\\n\
            vle%d.v v%d, (x7);"%(vsew, vs2) + " \\\n\
            la x7, val1; \\\n\
            vle%d.v v%d, (x7);"%(vsew, n) + " \\\n\
            inst v%d, v%d, v%d%s; "%(vd, vs2, n, (", v0.t" if masked else "")) + "\\\n\
        )", file=f)
    for n in range(1, 32):
        if n % lmul != 0:
            continue
        vs1, vs2 = valid_aligned_regs(n)
        print("#define TEST_FIXPOINT_VV_OP_vd_%d( testnum, inst, vxrm_val, val2, val1, mask_addr )"%n + " \\\n\
        TEST_CASE_LOOP( testnum, v%d, "%n + " \\\n\
            VSET_VSEW_4AVL \\\n\
            la x7, rd_origin_data; \\\n\
            vle%d.v v%d, (x7);"%(vsew, n) + " \\\n\
            %s "%("la x7, mask_addr; \\\n    vlm.v v0, (x7); \\\n  "if masked else "")+" \
            csrwi vxrm, vxrm_val; \\\n\
            la x7, val2; \\\n\
            vle%d.v v%d, (x7);"%(vsew, vs2) + " \\\n\
            la x7, val1; \\\n\
            vle%d.v v%d, (x7);"%(vsew, vs1) + " \\\n\
            inst v%d, v%d, v%d%s; "%(n, vs2, vs1, (", v0.t" if masked else "")) + "\\\n\
        )", file=f)


def generate_macros_vnclip(f, lmul):
    vsew = int(os.environ['RVV_ATG_VSEW'])
    masked = True if os.environ['RVV_ATG_MASKED'] == "True" else False
    print("#undef TEST_FIXPOINT_N_VV_OP \n\
#define TEST_FIXPOINT_N_VV_OP( testnum, inst, vxrm_val, val2, val1, mask_addr ) \\\n\
        TEST_CASE_LOOP( testnum, v24, \\\n\
            VSET_VSEW_4AVL \\\n\
            la x7, rd_origin_data; \\\n\
            vle%d.v v24, (x7);"%vsew + " \\\n\
            %s "%("la x7, mask_addr; \\\n    vlm.v v0, (x7); \\\n  "if masked else "")+" \
            csrwi vxrm, vxrm_val; \\\n\
            la x7, val2; \\\n\
            vle%d.v v16, (x7);"%(64 if vsew == 64 else vsew*2) + " \\\n\
            la x7, val1; \\\n\
            vle%d.v v8, (x7);"%vsew + " \\\n\
            inst v24, v16, v8%s;"%(", v0.t" if masked else "") + "  \\\n\
        )", file=f)
    print("#undef TEST_FIXPOINT_N_VX_OP \n\
#define TEST_FIXPOINT_N_VX_OP( testnum, inst, vxrm_val, val2, val1, mask_addr ) \\\n\
        TEST_CASE_LOOP( testnum, v24, \\\n\
            VSET_VSEW_4AVL \\\n\
            la x7, rd_origin_data; \\\n\
            vle%d.v v24, (x7);"%vsew + " \\\n\
            %s "%("la x7, mask_addr; \\\n    vlm.v v0, (x7); \\\n  "if masked else "")+" \
            csrwi vxrm, vxrm_val; \\\n\
            la x7, val2; \\\n\
            vle%d.v v16, (x7);"%(64 if vsew == 64 else vsew*2) + " \\\n\
            li x1, MASK_VSEW(val1); \\\n\
            inst v24, v16, x1%s;"%(", v0.t" if masked else "") + "  \\\n\
        )", file=f)
    print("#undef TEST_FIXPOINT_N_VI_OP \n\
#define TEST_FIXPOINT_N_VI_OP( testnum, inst, vxrm_val, val2, val1, mask_addr ) \\\n\
        TEST_CASE_LOOP( testnum, v24, \\\n\
            VSET_VSEW_4AVL \\\n\
            la x7, rd_origin_data; \\\n\
            vle%d.v v24, (x7);"%vsew + " \\\n\
            %s "%("la x7, mask_addr; \\\n    vlm.v v0, (x7); \\\n  "if masked else "")+" \
            csrwi vxrm, vxrm_val; \\\n\
            la x7, val2; \\\n\
            vle%d.v v16, (x7);"%(64 if vsew == 64 else vsew*2) + " \\\n\
            inst v24, v16, SEXT_IMM(val1)%s;"%(", v0.t" if masked else "") + "  \\\n\
        )", file=f)
    
    for n in range(1, 32):
        if n % lmul != 0:
            continue
        vd, vs2 = get_aligned_regs(n, lmul, lmul, 2*lmul)
        if vd == vs2 == 0:
            continue
        print("#define TEST_FIXPOINT_N_VV_OP_vs1_%d(  testnum, inst, vxrm_val, val2, val1, mask_addr  ) "%n + "\\\n\
        TEST_CASE_LOOP( testnum, v%d, "%vd + " \\\n\
            VSET_VSEW_4AVL \\\n\
            la x7, rd_origin_data; \\\n\
            vle%d.v v%d, (x7);"%(vsew, vd) + " \\\n\
            %s "%("la x7, mask_addr; \\\n    vlm.v v0, (x7); \\\n  "if masked else "")+" \
            csrwi vxrm, vxrm_val; \\\n\
            la x7, val2; \\\n\
            vle%d.v v%d, (x7);"%(64 if vsew == 64 else vsew*2, vs2) + " \\\n\
            la x7, val1; \\\n\
            vle%d.v v%d, (x7);"%(vsew, n) + " \\\n\
            inst v%d, v%d, v%d%s; "%(vd, vs2, n, (", v0.t" if masked else "")) + " \\\n\
        )", file=f)
    for n in range(1, 32):
        if n % (lmul*2) != 0:
            continue
        vd, vs1 = get_aligned_regs(n, 2*lmul, lmul, lmul)
        if vd == vs1 == 0:
            continue
        print("#define TEST_FIXPOINT_N_VV_OP_vs2_%d(  testnum, inst, vxrm_val, val2, val1, mask_addr  ) "%n + " \\\n\
        TEST_CASE_LOOP( testnum, v%d, "%vd + " \\\n\
            VSET_VSEW_4AVL \\\n\
            la x7, rd_origin_data; \\\n\
            vle%d.v v%d, (x7);"%(vsew, vd) + " \\\n\
            %s "%("la x7, mask_addr; \\\n    vlm.v v0, (x7); \\\n  "if masked else "")+" \
            csrwi vxrm, vxrm_val; \\\n\
            la x7, val2; \\\n\
            vle%d.v v%d, (x7);"%(64 if vsew == 64 else vsew*2, n) + " \\\n\
            la x7, val1; \\\n\
            vle%d.v v%d, (x7);"%(vsew, vs1) + " \\\n\
            inst v%d, v%d, v%d%s; "%(vd, n, vs1, (", v0.t" if masked else "")) + " \\\n\
        )", file=f)
    for n in range(1, 32):
        if n % (lmul) != 0:
            continue
        vs2, vs1 = get_aligned_regs(n, lmul, 2*lmul, lmul)
        if vs2 == vs1 == 0:
            continue
        print("#define TEST_FIXPOINT_N_VV_OP_vd_%d(  testnum, inst, vxrm_val, val2, val1, mask_addr  ) "%n + " \\\n\
        TEST_CASE_LOOP( testnum, v%d, "%n + " \\\n\
            VSET_VSEW_4AVL \\\n\
            la x7, rd_origin_data; \\\n\
            vle%d.v v%d, (x7);"%(vsew, n) + " \\\n\
            %s "%("la x7, mask_addr; \\\n    vlm.v v0, (x7); \\\n  "if masked else "")+" \
            csrwi vxrm, vxrm_val; \\\n\
            la x7, val2; \\\n\
            vle%d.v v%d, (x7);"%(64 if vsew == 64 else vsew*2, vs2) + " \\\n\
            la x7, val1; \\\n\
            vle%d.v v%d, (x7);"%(vsew, vs1) + " \\\n\
            inst v%d, v%d, v%d%s; "%(n, vs2, vs1, (", v0.t" if masked else "")) + "\\\n\
        )", file=f)


def generate_tests(f, rs1_val, rs2_val, instr, lmul, generate_vi = False):
    vlen = int(os.environ['RVV_ATG_VLEN'])
    vsew = int(os.environ['RVV_ATG_VSEW'])
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
        for vxrm in range(4):
            n += 1
            print("  TEST_FIXPOINT_VV_OP( "+str(n)+",  %s.vv, %d, " %
                (instr, vxrm) + "rs2_data+%d, rs1_data+%d, mask_data+%d)"%(i*step_bytes, i*step_bytes, j*mask_bytes), file=f)
            j = (j + 1) % mask_num
    
    for i in range(1, 32):
        if i % lmul != 0:
            continue
        k = i % loop_num
        for vxrm in range(4):
            n += 1
            print("  TEST_FIXPOINT_VV_OP_vd_%d( "%i+str(n)+",  %s.vv, %d, "%(instr, vxrm) + "rs2_data+%d, rs1_data+%d, mask_data+%d)"%(k*step_bytes, k*step_bytes, j*mask_bytes),file=f)
            j = (j + 1) % mask_num
            n += 1
            print("  TEST_FIXPOINT_VV_OP_vs1_%d( "%i+str(n)+",  %s.vv, %d, "%(instr, vxrm) + "rs2_data+%d, rs1_data+%d, mask_data+%d)"%(k*step_bytes, k*step_bytes, j*mask_bytes),file=f)
            j = (j + 1) % mask_num
    
    vv_test_num = n
    
    print("  #-------------------------------------------------------------", file=f)
    print("  # VX Tests", file=f)
    print("  #-------------------------------------------------------------", file=f)
    
    for i in range(loop_num):
        for vxrm in range(4):
            n += 1
            print("  TEST_FIXPOINT_VX_OP( "+str(n)+",  %s.vx, %d, " %
                (instr, vxrm)+"rs2_data+%d, %s, mask_data+%d)"%(i*step_bytes, rs1_val[0], j*mask_bytes), file=f)
            j = (j + 1) % mask_num
    
    vx_test_num = n - vv_test_num
    
    vi_test_num = 0
    if generate_vi:
        print("  #-------------------------------------------------------------", file=f)
        print("  # VI Tests", file=f)
        print("  #-------------------------------------------------------------", file=f)
        
        for i in range(loop_num):
            for vxrm in range(4):
                n += 1
                print("  TEST_FIXPOINT_VI_OP( "+str(n)+",  %s.vi, %d, " %
                    (instr, vxrm)+"rs2_data+%d, 15, mask_data+%d)"%(i*step_bytes, j*mask_bytes), file=f)
                j = (j + 1) % mask_num
        
        vi_test_num = n - vv_test_num - vx_test_num
    
    return (vv_test_num, vx_test_num, vi_test_num)

def generate_tests_vnclip(f, rs1_val, rs2_val, instr, lmul):
    vlen = int(os.environ['RVV_ATG_VLEN'])
    vsew = int(os.environ['RVV_ATG_VSEW'])
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
    print("  # WV Tests", file=f)
    print("  #-------------------------------------------------------------", file=f)

    for i in range(loop_num):
        for vxrm in range(4):
            n += 1
            print("  TEST_FIXPOINT_N_VV_OP( "+str(n)+",  %s.wv, %d, " %
                (instr, vxrm) + "rs2_data+%d, rs1_data+%d, mask_data+%d)"%(i*step_bytes*2, i*step_bytes, j*mask_bytes), file=f)
            j = (j + 1) % mask_num
    
    for i in range(1, 32):
        if i % (lmul) != 0:
            continue
        if get_aligned_regs(i, lmul, lmul, 2*lmul) == (0, 0):
            continue
        k = i % loop_num
        for vxrm in range(4):
            n += 1
            print("  TEST_FIXPOINT_N_VV_OP_vd_%d( "%i+str(n)+",  %s.wv, %d, "%(instr, vxrm) + "rs2_data+%d, rs1_data+%d, mask_data+%d)"%(k*step_bytes*2, k*step_bytes, j*mask_bytes),file=f)
            j = (j + 1) % mask_num
            n += 1
            print("  TEST_FIXPOINT_N_VV_OP_vs1_%d( "%i+str(n)+",  %s.wv, %d, "%(instr, vxrm) + "rs2_data+%d, rs1_data+%d, mask_data+%d)"%(k*step_bytes*2, k*step_bytes, j*mask_bytes),file=f)
            j = (j + 1) % mask_num
    
    for i in range(1, 32):
        if i % (2*lmul) != 0:
            continue
        if get_aligned_regs(i, 2*lmul, lmul, lmul) == (0, 0):
            continue
        k = i % loop_num
        for vxrm in range(4):
            n += 1
            print("  TEST_FIXPOINT_N_VV_OP_vs2_%d( "%i+str(n)+",  %s.wv, %d, "%(instr, vxrm) + "rs2_data+%d, rs1_data+%d, mask_data+%d)"%(k*step_bytes*2, k*step_bytes, j*mask_bytes),file=f)
            j = (j + 1) % mask_num

    vv_test_num = n
    
    print("  #-------------------------------------------------------------", file=f)
    print("  # WX Tests", file=f)
    print("  #-------------------------------------------------------------", file=f)
    
    for i in range(loop_num):
        for vxrm in range(4):
            n += 1
            print("  TEST_FIXPOINT_N_VX_OP( "+str(n)+",  %s.wx, %d, " %
                (instr, vxrm)+"rs2_data+%d, %s, mask_data+%d)"%(i*step_bytes*2, rs1_val[0], j*mask_bytes), file=f)
            j = (j + 1) % mask_num
    
    vx_test_num = n - vv_test_num
    
    print("  #-------------------------------------------------------------", file=f)
    print("  # WI Tests", file=f)
    print("  #-------------------------------------------------------------", file=f)
    
    for i in range(loop_num):
        for vxrm in range(4):
            n += 1
            print("  TEST_FIXPOINT_N_VI_OP( "+str(n)+",  %s.wi, %d, " %
                (instr, vxrm)+"rs2_data+%d, 15, mask_data+%d)"%(i*step_bytes*2, j*mask_bytes), file=f)
            j = (j + 1) % mask_num
    
    vi_test_num = n - vv_test_num - vx_test_num
    
    return (vv_test_num, vx_test_num, vi_test_num)
  