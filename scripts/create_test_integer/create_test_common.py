import os
import re
import math

from scripts.test_common_info import valid_aligned_regs, get_aligned_reg, get_aligned_regs


def generate_macros_vvvxvi(f, lmul, generate_vv = True, generate_vx = True, generate_vi = True):
    vsew = int(os.environ['RVV_ATG_VSEW'])
    masked = True if os.environ['RVV_ATG_MASKED'] == "True" else False
    
    if generate_vv:
        print("#define TEST_VV_OP( testnum, inst, val2, val1, mask_addr ) \\\n\
        TEST_CASE_LOOP( testnum, v24, \\\n\
            VSET_VSEW_4AVL \\\n\
            la x7, rd_origin_data; \\\n\
            vle%d.v v24, (x7);"%vsew + " \\\n\
            %s "%("la x7, mask_addr; \\\n    vlm.v v0, (x7); \\\n  "if masked else "")+" \
            la x7, val2; \\\n\
            vle%d.v v16, (x7);"%vsew + " \\\n\
            la x7, val1; \\\n\
            vle%d.v v8, (x7);"%vsew + " \\\n\
            inst v24, v16, v8%s;"%(", v0.t" if masked else "") + " \\\n\
        )", file=f)
        for n in range(1, 32):
            if n % lmul != 0:
                continue
            print("#define TEST_VV_OP_vs1_%d( testnum, inst, val2, val1, mask_addr )"%n + " \\\n\
            TEST_CASE_LOOP( testnum, v24, \\\n\
                VSET_VSEW_4AVL \\\n\
                la x7, rd_origin_data; \\\n\
                vle%d.v v24, (x7);"%vsew + " \\\n\
                %s "%("la x7, mask_addr; \\\n    vlm.v v0, (x7); \\\n  "if masked else "")+" \
                la x7, val2; \\\n\
                vle%d.v v16, (x7);"%vsew + " \\\n\
                la x7, val1; \\\n\
                vle%d.v v%d, (x7);"%(vsew, n)  + " \\\n\
                inst v24, v16, v%d%s; "%(n, (", v0.t" if masked else "")) + " \\\n\
            )", file=f)
        for n in range(1, 32):
            if n % lmul != 0:
                continue
            vs1, vs2 = valid_aligned_regs(n)            
            print("#define TEST_VV_OP_vd_%d( testnum, inst, val2, val1, mask_addr )"%n + " \\\n\
            TEST_CASE_LOOP( testnum, v%d, "%n + " \\\n\
                VSET_VSEW_4AVL \\\n\
                la x7, rd_origin_data; \\\n\
                vle%d.v v%d, (x7);"%(vsew, n) + " \\\n\
                %s "%("la x7, mask_addr; \\\n    vlm.v v0, (x7); \\\n  "if masked else "")+" \
                la x7, val2; \\\n\
                vle%d.v v%d, (x7);"%(vsew, vs2) + " \\\n\
                la x7, val1; \\\n\
                vle%d.v v%d, (x7);"%(vsew, vs1) + " \\\n\
                inst v%d, v%d, v%d%s;"%(n, vs2, vs1, (", v0.t" if masked else ""))+" \\\n\
            ) ", file=f)
    
    if generate_vx:
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
            print("#define TEST_VX_OP_vs2_%d( testnum, inst, val2, val1, mask_addr ) "%n + " \\\n\
            TEST_CASE_LOOP( testnum, v24,   \\\n\
                VSET_VSEW_4AVL \\\n\
                la x7, rd_origin_data; \\\n\
                vle%d.v v24, (x7);"%vsew + " \\\n\
                %s "%("la x7, mask_addr; \\\n    vlm.v v0, (x7); \\\n  "if masked else "")+" \
                la x7, val2; \\\n\
                vle%d.v v%d, (x7);"%(vsew, n) + " \\\n\
                li x1, MASK_XLEN(val1); \\\n\
                inst v24, v%d, x1%s; "%(n, (", v0.t" if masked else "")) + " \\\n\
            )", file=f)
        for n in range(1, 32):
            if n % lmul != 0:
                continue
            print("#define TEST_VX_OP_vd_%d( testnum, inst, val2, val1, mask_addr ) "%n + " \\\n\
            TEST_CASE_LOOP( testnum, v%d,  "%n + "\\\n\
                VSET_VSEW_4AVL \\\n\
                la x7, rd_origin_data; \\\n\
                vle%d.v v%d, (x7);"%(vsew, n) + " \\\n\
                %s "%("la x7, mask_addr; \\\n    vlm.v v0, (x7); \\\n  "if masked else "")+" \
                la x7, val2; \\\n\
                vle%d.v v8, (x7);"%(vsew) + " \\\n\
                li x1, MASK_XLEN(val1); \\\n\
                inst v%d, v8, x1%s; "%(n, (", v0.t" if masked else "")) + " \\\n\
            ) ", file=f)
    
    if generate_vi:
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


def generate_macros_vw(f, lmul, generate_wvwx = True):
    vsew = int(os.environ['RVV_ATG_VSEW'])
    masked = True if os.environ['RVV_ATG_MASKED'] == "True" else False
    
    print("#undef TEST_W_VV_OP \n\
#define TEST_W_VV_OP( testnum, inst, val2, val1, mask_addr ) \\\n\
    TEST_CASE_LOOP_W( testnum, v24, \\\n\
        VSET_VSEW_4AVL \\\n\
        la x7, rd_origin_data; \\\n\
        vle%d.v v24, (x7);"%(64 if vsew == 64 else vsew*2) + " \\\n\
        %s "%("la x7, mask_addr; \\\n    vlm.v v0, (x7); \\\n  "if masked else "")+" \
        la x7, val2; \\\n\
        vle%d.v v8, (x7);"%vsew + " \\\n\
        la x7, val1; \\\n\
        vle%d.v v16, (x7);"%vsew + " \\\n\
        inst v24, v8, v16%s;"%(", v0.t" if masked else "") + " \\\n\
    )", file=f)

    print("#undef TEST_W_VX_OP \n\
#define TEST_W_VX_OP( testnum, inst, val2, val1, mask_addr ) \\\n\
    TEST_CASE_LOOP_W( testnum, v24, \\\n\
        VSET_VSEW_4AVL \\\n\
        la x7, rd_origin_data; \\\n\
        vle%d.v v24, (x7);"%(64 if vsew == 64 else vsew*2) + " \\\n\
        %s "%("la x7, mask_addr; \\\n    vlm.v v0, (x7); \\\n  "if masked else "")+" \
        la x7, val2; \\\n\
        vle%d.v v8, (x7);"%vsew + " \\\n\
        li x1, MASK_XLEN(val1); \\\n\
        inst v24, v8, x1%s;"%(", v0.t" if masked else "") + " \\\n\
    )", file=f)

    for n in range(1, 32):
        if n % lmul != 0:
            continue
        vd, vs2 = get_aligned_regs(n, lmul, 2*lmul, lmul)
        if vd == vs2 == 0:
            continue
        print("#define TEST_W_VV_OP_vs1_%d( testnum, inst, val2, val1, mask_addr )"%n + " \\\n\
        TEST_CASE_LOOP_W( testnum, v%d, "%vd + "\\\n\
            VSET_VSEW_4AVL \\\n\
            la x7, rd_origin_data; \\\n\
            vle%d.v v%d, (x7);"%(64 if vsew == 64 else vsew*2, vd) + " \\\n\
            %s "%("la x7, mask_addr; \\\n    vlm.v v0, (x7); \\\n  "if masked else "")+" \
            la x7, val2; \\\n\
            vle%d.v v%d, (x7);"%(vsew, vs2) + " \\\n\
            la x7, val1; \\\n\
            vle%d.v v%d, (x7);"%(vsew, n) + " \\\n\
            inst v%d, v%d, v%d%s;"%(vd, vs2, n, (", v0.t" if masked else ""))+" \\\n\
        )",file=f)
    for n in range(1, 32):
        # Beacuse of the widening instruction, rd should valid for the destination’s EMUL
        if n % (2*lmul) != 0:
            continue
        vs2, vs1 = get_aligned_regs(n, 2*lmul, lmul, lmul)
        if vs2 == vs1 == 0:
            continue
        print("#define TEST_W_VV_OP_vd_%d( testnum, inst, val2, val1, mask_addr )"%n + " \\\n\
        TEST_CASE_LOOP_W( testnum, v%d, "%n + "\\\n\
            VSET_VSEW_4AVL \\\n\
            la x7, rd_origin_data; \\\n\
            vle%d.v v%d, (x7);"%(64 if vsew == 64 else vsew*2, n) + " \\\n\
            %s "%("la x7, mask_addr; \\\n    vlm.v v0, (x7); \\\n  "if masked else "")+" \
            la x7, val2; \\\n\
            vle%d.v v%d, (x7);"%(vsew, vs2) + " \\\n\
            la x7, val1; \\\n\
            vle%d.v v%d, (x7);"%(vsew, vs1) + " \\\n\
            inst v%d, v%d, v%d%s;"%(n, vs2, vs1, (", v0.t" if masked else ""))+" \\\n\
        )",file=f)
    
    if generate_wvwx:
        print("#undef TEST_W_WV_OP \n\
    #define TEST_W_WV_OP( testnum, inst, val2, val1, mask_addr ) \\\n\
        TEST_CASE_LOOP_W( testnum, v24, \\\n\
            VSET_VSEW_4AVL \\\n\
            la x7, rd_origin_data; \\\n\
            vle%d.v v24, (x7);"%(64 if vsew == 64 else vsew*2) + " \\\n\
            %s "%("la x7, mask_addr; \\\n    vlm.v v0, (x7); \\\n  "if masked else "")+" \
            la x7, val2; \\\n\
            vle%d.v v8, (x7);"%(64 if vsew == 64 else vsew*2) + " \\\n\
            la x7, val1; \\\n\
            vle%d.v v16, (x7);"%vsew + " \\\n\
            inst v24, v8, v16%s;"%(", v0.t" if masked else "") + " ; ; \\\n\
        )", file=f)
        print("#undef TEST_W_WX_OP \n\
    #define TEST_W_WX_OP( testnum, inst, val2, val1, mask_addr ) \\\n\
        TEST_CASE_LOOP_W( testnum, v24, \\\n\
            VSET_VSEW_4AVL \\\n\
            la x7, rd_origin_data; \\\n\
            vle%d.v v24, (x7);"%(64 if vsew == 64 else vsew*2) + " \\\n\
            %s "%("la x7, mask_addr; \\\n    vlm.v v0, (x7); \\\n  "if masked else "")+" \
            la x7, val2; \\\n\
            vle%d.v v8, (x7);"%(64 if vsew == 64 else vsew*2) + " \\\n\
            li x1, MASK_XLEN(val1); \\\n\
            inst v24, v8, x1%s;"%(", v0.t" if masked else "") + " ; ; \\\n\
        )", file=f)


def generate_macros_vwmacc(f, lmul, generate_vv = True):
    vsew = int(os.environ['RVV_ATG_VSEW'])
    masked = True if os.environ['RVV_ATG_MASKED'] == "True" else False
    
    print("#undef TEST_W_MA_VX_OP \n\
#define TEST_W_MA_VX_OP( testnum, inst, val1, val2, mask_addr ) \\\n\
    TEST_CASE_LOOP_W( testnum, v24, \\\n\
        VSET_VSEW_4AVL \\\n\
        la x7, rd_origin_data; \\\n\
        vle%d.v v24, (x7);"%(64 if vsew == 64 else vsew*2) + " \\\n\
        %s "%("la x7, mask_addr; \\\n    vlm.v v0, (x7); \\\n  "if masked else "")+" \
        la x7, val2; \\\n\
        vle%d.v v8, (x7);"%vsew + " \\\n\
        li x1, MASK_XLEN(val1); \\\n\
        inst v24, x1, v8%s;"%(", v0.t" if masked else "")+" ; \\\n\
    )", file=f)

    if generate_vv:
        print("#undef TEST_W_MA_VV_OP \n\
    #define TEST_W_MA_VV_OP( testnum, inst, val1, val2, mask_addr ) \\\n\
        TEST_CASE_LOOP_W( testnum, v24, \\\n\
            VSET_VSEW_4AVL \\\n\
            la x7, rd_origin_data; \\\n\
            vle%d.v v24, (x7);"%(64 if vsew == 64 else vsew*2) + " \\\n\
            %s "%("la x7, mask_addr; \\\n    vlm.v v0, (x7); \\\n  "if masked else "")+" \
            la x7, val1; \\\n\
            vle%d.v v8, (x7);"%vsew + " \\\n\
            la x7, val2; \\\n\
            vle%d.v v16, (x7);"%vsew + " \\\n\
            inst v24, v8, v16%s;"%((", v0.t" if masked else ""))+" ; \\\n\
        )", file=f)
        for n in range(1, 32):
            if n % lmul != 0:
                continue
            vd, vs2 = get_aligned_regs(n, lmul, 2*lmul, lmul)
            if vd == vs2 == 0:
                continue
            print("#define TEST_W_MA_VV_OP_vs1_%d( testnum, inst, val1, val2, mask_addr ) "%n + " \\\n\
            TEST_CASE_LOOP_W( testnum, v%d, "%vd + "\\\n\
                VSET_VSEW_4AVL \\\n\
                la x7, rd_origin_data; \\\n\
                vle%d.v v%d, (x7);"%(64 if vsew == 64 else vsew*2, vd) + " \\\n\
                %s "%("la x7, mask_addr; \\\n    vlm.v v0, (x7); \\\n  "if masked else "")+" \
                la x7, val1; \\\n\
                vle%d.v v%d, (x7);"%(vsew, n) + " \\\n\
                la x7, val2; \\\n\
                vle%d.v v%d, (x7);"%(vsew, vs2) + " \\\n\
                inst v%d, v%d, v%d%s; "%(vd, n, vs2, (", v0.t" if masked else "")) + " \\\n\
            )",file=f)
        for n in range(1, 32):
            # Beacuse of the widening instruction, rd should valid for the destination’s EMUL
            if n % (2*lmul) != 0:
                continue
            vs2, vs1 = get_aligned_regs(n, 2*lmul, lmul, lmul)
            if vs2 == vs1 == 0:
                continue
            print("#define TEST_W_MA_VV_OP_vd_%d( testnum, inst, val1, val2, mask_addr ) "%n + " \\\n\
            TEST_CASE_LOOP_W( testnum, v%d, "%n + "\\\n\
                VSET_VSEW_4AVL \\\n\
                la x7, rd_origin_data; \\\n\
                vle%d.v v%d, (x7);"%(64 if vsew == 64 else vsew*2, n) + " \\\n\
                %s "%("la x7, mask_addr; \\\n    vlm.v v0, (x7); \\\n  "if masked else "")+" \
                la x7, val1; \\\n\
                vle%d.v v%d, (x7);"%(vsew, vs1) + " \\\n\
                la x7, val2; \\\n\
                vle%d.v v%d, (x7);"%(vsew, vs2) + " \\\n\
                inst v%d, v%d, v%d%s; "%(n, vs1, vs2, (", v0.t" if masked else "")) + " \\\n\
            )",file=f)


def generate_macros_muladd(f, lmul):
    vsew = int(os.environ['RVV_ATG_VSEW'])
    masked = True if os.environ['RVV_ATG_MASKED'] == "True" else False
    
    print("#undef TEST_MA_VV_OP \n\
#define TEST_MA_VV_OP( testnum, inst, val1, val2, mask_addr ) \\\n\
    TEST_CASE_LOOP( testnum, v24, \\\n\
        VSET_VSEW_4AVL \\\n\
        la x7, rd_origin_data; \\\n\
        vle%d.v v24, (x7);"%vsew + " \\\n\
        %s "%("la x7, mask_addr; \\\n    vlm.v v0, (x7); \\\n  "if masked else "")+" \
        la x7, val1; \\\n\
        vle%d.v v16, (x7);"%vsew + " \\\n\
        la x7, val2; \\\n\
        vle%d.v v8, (x7);"%vsew + " \\\n\
        inst v24, v16, v8%s;"%(", v0.t" if masked else "") + " \\\n\
    )", file=f)
    for n in range(1, 32):
        if n % lmul != 0:
            continue
        print("#define TEST_MA_VV_OP_vs1_%d( testnum, inst, val1, val2, mask_addr ) "%n + " \\\n\
        TEST_CASE_LOOP( testnum, v24,  \\\n\
            VSET_VSEW_4AVL \\\n\
            la x7, rd_origin_data; \\\n\
            vle%d.v v24, (x7);"%vsew + " \\\n\
            %s "%("la x7, mask_addr; \\\n    vlm.v v0, (x7); \\\n  "if masked else "")+" \
            la x7, val1; \\\n\
            vle%d.v v%d, (x7);"%(vsew, n) + " \\\n\
            la x7, val2; \\\n\
            vle%d.v v16, (x7);"%vsew + " \\\n\
            inst v24, v%d, v16%s; "%(n, ", v0.t" if masked else "") + " \\\n\
        )", file=f)
    for n in range(1, 32):
        if n % lmul != 0:
            continue
        vs1, vs2 = valid_aligned_regs(n) 
        print("#define TEST_MA_VV_OP_vd_%d( testnum, inst, val1, val2, mask_addr ) "%n + " \\\n\
        TEST_CASE_LOOP( testnum, v%d, "%n + "\\\n\
            VSET_VSEW_4AVL \\\n\
            la x7, rd_origin_data; \\\n\
            vle%d.v v%d, (x7);"%(vsew, n) + " \\\n\
            %s "%("la x7, mask_addr; \\\n    vlm.v v0, (x7); \\\n  "if masked else "")+" \
            la x7, val1; \\\n\
            vle%d.v v%d, (x7);"%(vsew, vs1) + " \\\n\
            la x7, val2; \\\n\
            vle%d.v v%d, (x7);"%(vsew, vs2) + " \\\n\
            inst v%d, v%d, v%d%s; "%(n, vs1, vs2, (", v0.t" if masked else "")) + " \\\n\
        ) ", file=f)

    print("#udnef TEST_MA_VX_OP \n\
#define TEST_MA_VX_OP( testnum, inst, val1, val2, mask_addr ) \\\n\
    TEST_CASE_LOOP( testnum, v24, \\\n\
        VSET_VSEW_4AVL \\\n\
        la x7, rd_origin_data; \\\n\
        vle%d.v v24, (x7);"%vsew + " \\\n\
        %s "%("la x7, mask_addr; \\\n    vlm.v v0, (x7); \\\n  "if masked else "")+" \
        la x7, val2; \\\n\
        vle%d.v v8, (x7);"%vsew + " \\\n\
        li x1, MASK_XLEN(val1); \\\n\
        inst v24, x1, v8%s; "%(", v0.t" if masked else "") + " \\\n\
    )", file=f)


def generate_macros_vvmvxmvim(f, lmul, generate_vi=True):
    vsew = int(os.environ['RVV_ATG_VSEW'])

    print("#undef TEST_VV_M_OP \n\
#define TEST_VV_M_OP( testnum, inst, val2, val1, mask_addr ) \\\n\
    TEST_CASE_LOOP( testnum, v24, \\\n\
        VSET_VSEW_4AVL \\\n\
        la x7, rd_origin_data; \\\n\
        vle%d.v v24, (x7);"%vsew + " \\\n\
        la x7, mask_addr; \\\n\
        vlm.v v0, (x7); \\\n\
        la x7, val1; \\\n\
        vle%d.v v8, (x7);"%vsew + " \\\n\
        la x7, val2; \\\n\
        vle%d.v v16, (x7);"%vsew + " \\\n\
        inst v24, v16, v8, v0; \\\n\
    )", file=f)
    print("#undef TEST_VX_M_OP \n\
#define TEST_VX_M_OP( testnum, inst, val2, val1, mask_addr ) \\\n\
    TEST_CASE_LOOP( testnum, v24, \\\n\
        VSET_VSEW_4AVL \\\n\
        la x7, rd_origin_data; \\\n\
        vle%d.v v24, (x7);"%vsew + " \\\n\
        la x7, mask_addr; \\\n\
        vlm.v v0, (x7); \\\n\
        la x7, val2; \\\n\
        vle%d.v v8, (x7);"%vsew + " \\\n\
        li x1, MASK_VSEW(val1); \\\n\
        inst v24, v8, x1, v0; \\\n\
    )", file=f)
    
    for n in range(1, 32):
        if n % lmul != 0:
            continue
        print("#define TEST_VV_M_OP_vs1_%d( testnum, inst, val2, val1, mask_addr )"%n + " \\\n\
        TEST_CASE_LOOP( testnum, v24, \\\n\
            VSET_VSEW_4AVL \\\n\
            la x7, rd_origin_data; \\\n\
            vle%d.v v24, (x7);"%vsew + " \\\n\
            la x7, mask_addr; \\\n\
            vlm.v v0, (x7); \\\n\
            la x7, val2; \\\n\
            vle%d.v v8, (x7);"%vsew + " \\\n\
            la x7, val1; \\\n\
            vle%d.v v%d, (x7);"%(vsew, n) + " \\\n\
            inst v24, v8, v%d, v0; "%n + " \\\n\
        )", file=f)
    for n in range(1, 32):
        if n % lmul != 0:
            continue
        vs1, vs2 = valid_aligned_regs(n)
        print("#define TEST_VV_M_OP_vd_%d( testnum, inst, val2, val1, mask_addr )"%n + " \\\n\
        TEST_CASE_LOOP( testnum, v%d, "%n + " \\\n\
            VSET_VSEW_4AVL \\\n\
            la x7, rd_origin_data; \\\n\
            vle%d.v v%d, (x7);"%(vsew, n) + " \\\n\
            la x7, mask_addr; \\\n\
            vlm.v v0, (x7); \\\n\
            la x7, val1; \\\n\
            vle%d.v v%d, (x7);"%(vsew, vs1) + " \\\n\
            la x7, val2; \\\n\
            vle%d.v v%d, (x7);"%(vsew, vs2) + " \\\n\
            inst v%d, v%d, v%d, v0;"%(n, vs2, vs1)+" \\\n\
        ) ",file=f)
    
    if generate_vi:
        print("#undef TEST_VI_M_OP \n\
    #define TEST_VI_M_OP( testnum, inst, val2, val1, mask_addr ) \\\n\
        TEST_CASE_LOOP( testnum, v24, \\\n\
            VSET_VSEW_4AVL \\\n\
            la x7, rd_origin_data; \\\n\
            vle%d.v v24, (x7);"%vsew + " \\\n\
            la x7, mask_addr; \\\n\
            vlm.v v0, (x7); \\\n\
            la x7, val2; \\\n\
            vle%d.v v8, (x7);"%vsew + " \\\n\
            inst v24, v8, SEXT_IMM(val1), v0; \\\n\
        )", file=f)


def generate_macros_mask(f, lmul, generate_vv = True, generate_vx = True, generate_vi = True, is_adc_sbc = False):
    vsew = int(os.environ['RVV_ATG_VSEW'])
    masked = True if os.environ['RVV_ATG_MASKED'] == "True" else False
    mask_suffix = "v0" if is_adc_sbc else "v0.t"
    
    if generate_vv:
        print("#undef TEST_M_VV_OP \n\
    #define TEST_M_VV_OP( testnum, inst, val2, val1, mask_addr ) \\\n\
        TEST_CASE_VREG( testnum, v24, \\\n\
            VSET_VSEW_4AVL \\\n\
            la x7, rd_origin_data; \\\n\
            vle%d.v v24, (x7);"%vsew + " \\\n\
            %s "%("la x7, mask_addr; \\\n    vlm.v v0, (x7); \\\n  "if masked else "")+" \
            la x7, val1; \\\n\
            vle%d.v v8, (x7);"%vsew + " \\\n\
            la x7, val2; \\\n\
            vle%d.v v16, (x7);"%vsew + " \\\n\
            inst v24, v16, v8%s; "%(", %s"%mask_suffix if masked else "") + " \\\n\
        )", file=f)
        for n in range(1, 32):
            if n % lmul != 0:
                continue
            print("#define TEST_M_VV_OP_vs1_%d( testnum, inst, val2, val1, mask_addr )"%n + " \\\n\
            TEST_CASE_VREG( testnum, v24, \\\n\
                VSET_VSEW_4AVL \\\n\
                la x7, rd_origin_data; \\\n\
                vle%d.v v24, (x7);"%vsew + " \\\n\
                %s "%("la x7, mask_addr; \\\n    vlm.v v0, (x7); \\\n  "if masked else "")+" \
                la x7, val2; \\\n\
                vle%d.v v8, (x7);"%vsew + " \\\n\
                la x7, val1; \\\n\
                vle%d.v v%d, (x7);"%(vsew, n) + " \\\n\
                inst v24, v8, v%d%s; "%(n, (", %s"%mask_suffix if masked else "")) + " \\\n\
            )", file=f)
        for n in range(1, 32):
            # A vector mask occupies only one vector register regardless of SEW and LMUL.
            vs1, vs2 = valid_aligned_regs(n) 
            print("#define TEST_M_VV_OP_vd_%d( testnum, inst, val2, val1, mask_addr )"%n + " \\\n\
            TEST_CASE_VREG( testnum, v%d, "%n + "\\\n\
                VSET_VSEW_4AVL \\\n\
                %s "%("la x7, mask_addr; \\\n    vlm.v v0, (x7); \\\n  "if masked else "")+" \
                la x7, val1; \\\n\
                vle%d.v v%d, (x7);"%(vsew, vs1) + " \\\n\
                la x7, val2; \\\n\
                vle%d.v v%d, (x7);"%(vsew, vs2) + " \\\n\
                inst v%d, v%d, v%d%s; "%(n, vs2, vs1, (", %s"%mask_suffix if masked else "")) + "\\\n\
            ) ", file=f)

    if generate_vx:
        print("#undef TEST_M_VX_OP \n\
    #define TEST_M_VX_OP( testnum, inst, val2, val1, mask_addr ) \\\n\
        TEST_CASE_VREG( testnum, v24, \\\n\
            VSET_VSEW_4AVL \\\n\
            la x7, rd_origin_data; \\\n\
            vle%d.v v24, (x7);"%vsew + " \\\n\
            %s "%("la x7, mask_addr; \\\n    vlm.v v0, (x7); \\\n  "if masked else "")+" \
            la x7, val2; \\\n\
            vle%d.v v8, (x7);"%vsew + " \\\n\
            li x1, MASK_XLEN(val1); \\\n\
            inst v24, v8, x1%s; "%(", %s"%mask_suffix if masked else "") + " \\\n\
        )", file=f)
        for n in range(1, 32):
            if n % lmul != 0:
                continue
            print("#define TEST_M_VX_OP_vs2_%d( testnum, inst, val2, val1, mask_addr ) "%n + " \\\n\
            TEST_CASE_VREG( testnum, v24,  \\\n\
                VSET_VSEW_4AVL \\\n\
                la x7, rd_origin_data; \\\n\
                vle%d.v v24, (x7);"%vsew + " \\\n\
                %s "%("la x7, mask_addr; \\\n    vlm.v v0, (x7); \\\n  "if masked else "")+" \
                la x7, val2; \\\n\
                vle%d.v v%d, (x7);"%(vsew, n) + " \\\n\
                li x1, MASK_XLEN(val1); \\\n\
                inst v24, v%d, x1%s; "%(n, (", %s"%mask_suffix if masked else "")) + " \\\n\
            )", file=f)
        for n in range(1, 32):
            # A vector mask occupies only one vector register regardless of SEW and LMUL.
            vs = 16 if n // 8 == 1 else 8
            print("#define TEST_M_VX_OP_vd_%d( testnum, inst, val2, val1, mask_addr ) "%n + " \\\n\
            TEST_CASE_VREG( testnum, v%d, "%n + "\\\n\
                VSET_VSEW_4AVL \\\n\
                %s "%("la x7, mask_addr; \\\n    vlm.v v0, (x7); \\\n  "if masked else "")+" \
                la x7, val2; \\\n\
                vle%d.v v%d, (x7);"%(vsew, vs) + " \\\n\
                li x1, MASK_XLEN(val1); \\\n\
                inst v%d, v%d, x1%s; "%(n, vs, (", %s"%mask_suffix if masked else "")) + " \\\n\
            ) ", file=f)

    if generate_vi:
        print("#undef TEST_M_VI_OP \n\
    #define TEST_M_VI_OP( testnum, inst, val2, val1, mask_addr ) \
        TEST_CASE_VREG( testnum, v24, \
            VSET_VSEW_4AVL \\\n\
            la x7, rd_origin_data; \\\n\
            vle%d.v v24, (x7);"%vsew + " \\\n\
            %s "%("la x7, mask_addr; \\\n    vlm.v v0, (x7); \\\n  "if masked else "")+" \
            la x7, val2; \\\n\
            vle%d.v v8, (x7);"%vsew + " \\\n\
            inst v24, v8, SEXT_IMM(val1)%s; "%(", %s"%mask_suffix if masked else "") + " \\\n\
        )", file=f)


def generate_macros_vn(f, lmul):
    vsew = int(os.environ['RVV_ATG_VSEW'])
    masked = True if os.environ['RVV_ATG_MASKED'] == "True" else False

    print("#undef TEST_N_VV_OP \n\
#define TEST_N_VV_OP( testnum, inst, val2, val1, mask_addr ) \\\n\
    TEST_CASE_LOOP( testnum, v24, \\\n\
        VSET_VSEW_4AVL \\\n\
        la x7, rd_origin_data; \\\n\
        vle%d.v v24, (x7);"%vsew + " \\\n\
        %s "%("la x7, mask_addr; \\\n    vlm.v v0, (x7); \\\n  "if masked else "")+" \
        la x7, val2; \\\n\
        vle%d.v v16, (x7);"%(64 if vsew == 64 else vsew*2) + " \\\n\
        la x7, val1; \\\n\
        vle%d.v v8, (x7);"%vsew + " \\\n\
        inst v24, v16, v8%s;"%(", v0.t" if masked else "") + " \\\n\
    )", file=f)

    print("#undef TEST_N_VX_OP \n\
#define TEST_N_VX_OP( testnum, inst, val2, val1, mask_addr ) \\\n\
    TEST_CASE_LOOP( testnum, v24, \\\n\
        VSET_VSEW_4AVL \\\n\
        la x7, rd_origin_data; \\\n\
        vle%d.v v24, (x7);"%vsew + " \\\n\
        %s "%("la x7, mask_addr; \\\n    vlm.v v0, (x7); \\\n  "if masked else "")+" \
        la x7, val2; \\\n\
        vle%d.v v16, (x7);"%(64 if vsew == 64 else vsew*2) + " \\\n\
        li x1, MASK_VSEW(val1); \\\n\
        inst v24, v16, x1%s;"%(", v0.t" if masked else "") + " \\\n\
    )", file=f)

    print("#undef TEST_N_VI_OP \n\
#define TEST_N_VI_OP( testnum, inst, val2, val1, mask_addr ) \\\n\
    TEST_CASE_LOOP( testnum, v24, \\\n\
        VSET_VSEW_4AVL \\\n\
        la x7, rd_origin_data; \\\n\
        vle%d.v v24, (x7);"%vsew + " \\\n\
        %s "%("la x7, mask_addr; \\\n    vlm.v v0, (x7); \\\n  "if masked else "")+" \
        la x7, val2; \\\n\
        vle%d.v v16, (x7);"%(64 if vsew == 64 else vsew*2) + " \\\n\
        inst v24, v16, SEXT_IMM(val1)%s;"%(", v0.t" if masked else "") + " \\\n\
    )", file=f)

    for n in range(1, 32):
        if n % lmul != 0:
            continue
        vs2, vs1 = get_aligned_regs(n, lmul, 2*lmul, lmul)
        if vs2 == vs1 == 0:
            continue
        print("#define TEST_N_VV_OP_vd_%d( testnum, inst, val2, val1, mask_addr )"%n + " \\\n\
        TEST_CASE_LOOP( testnum, v%d, "%n + " \\\n\
            VSET_VSEW_4AVL \\\n\
            la x7, rd_origin_data; \\\n\
            vle%d.v v%d, (x7);"%(vsew, n) + " \\\n\
            %s "%("la x7, mask_addr; \\\n    vlm.v v0, (x7); \\\n  "if masked else "")+" \
            la x7, val2; \\\n\
            vle%d.v v%d, (x7);"%(64 if vsew == 64 else vsew*2, vs2) + " \\\n\
            la x7, val1; \\\n\
            vle%d.v v%d, (x7);"%(vsew, vs1) + " \\\n\
            inst v%d, v%d, v%d%s; "%(n, vs2, vs1, (", v0.t" if masked else "")) + " \\\n\
        ) ", file=f)
    for n in range(1, 32):
        if n % lmul != 0:
            continue
        vd, vs2 = get_aligned_regs(n, lmul, lmul, 2*lmul)
        if vd == vs2 == 0:
            continue
        print("#define TEST_N_VV_OP_vs1_%d( testnum, inst, val2, val1, mask_addr )"%n + " \\\n\
        TEST_CASE_LOOP( testnum, v%d, "%vd + "\\\n\
            VSET_VSEW_4AVL \\\n\
            la x7, rd_origin_data; \\\n\
            vle%d.v v%d, (x7);"%(vsew, vd) + " \\\n\
            %s "%("la x7, mask_addr; \\\n    vlm.v v0, (x7); \\\n  "if masked else "")+" \
            la x7, val2; \\\n\
            vle%d.v v%d, (x7);"%(64 if vsew == 64 else vsew*2, vs2) + " \\\n\
            la x7, val1; \\\n\
            vle%d.v v%d, (x7);"%(vsew, n) + " \\\n\
            inst v%d, v%d, v%d%s; "%(vd, vs2, n, (", v0.t" if masked else "")) + " \\\n\
        )", file=f)
    for n in range(1, 32):
        if n % (2*lmul) != 0:
            continue
        vd, vs1 = get_aligned_regs(n, 2*lmul, lmul, lmul)
        if vd == vs1 == 0:
            continue
        print("#define TEST_N_VV_OP_vs2_%d( testnum, inst, val2, val1, mask_addr )"%n + " \\\n\
        TEST_CASE_LOOP( testnum, v%d, "%vd + "\\\n\
            VSET_VSEW_4AVL \\\n\
            la x7, rd_origin_data; \\\n\
            vle%d.v v%d, (x7);"%(vsew, vd) + " \\\n\
            %s "%("la x7, mask_addr; \\\n    vlm.v v0, (x7); \\\n  "if masked else "")+" \
            la x7, val2; \\\n\
            vle%d.v v%d, (x7);"%(64 if vsew == 64 else vsew*2, n) + " \\\n\
            la x7, val1; \\\n\
            vle%d.v v%d, (x7);"%(vsew, vs1) + " \\\n\
            inst v%d, v%d, v%d%s; "%(vd, n, vs1, (", v0.t" if masked else "")) + " \\\n\
        )", file=f)


def generate_macros_vred(f, lmul):
    vsew = int(os.environ['RVV_ATG_VSEW'])
    masked = True if os.environ['RVV_ATG_MASKED'] == "True" else False
    
    print("#define TEST_RED_OP( testnum, inst, val1, val2, mask_addr ) \\\n\
    TEST_CASE( testnum, v24, \\\n\
        VSET_VSEW_4AVL \\\n\
        %s "%("la x7, mask_addr; \\\n    vlm.v v0, (x7); \\\n  "if masked else "")+" \
        la x7, rd_origin_data; \\\n\
        vle%d.v v24, (x7);"%vsew + " \\\n\
        la x7, val2; \\\n\
        vle%d.v v16, (x7);"%vsew + " \\\n\
        la x7, val1; \\\n\
        vle%d.v v8, (x7);"%vsew + " \\\n\
        inst v24, v16, v8%s;"%(", v0.t" if masked else "") + " \\\n\
    )", file=f)
    for n in range(1, 32):
        if n % lmul != 0:
            continue
        vs1, vd = valid_aligned_regs(n)
        print("#define TEST_RED_OP_vs2_%d( testnum, inst, val1, val2, mask_addr )"%n + " \\\n\
        TEST_CASE( testnum, v%d, "%vd + "\\\n\
            VSET_VSEW_4AVL \\\n\
            %s "%("la x7, mask_addr; \\\n    vlm.v v0, (x7); \\\n  "if masked else "")+" \
            la x7, rd_origin_data; \\\n\
            vle%d.v v%d, (x7);"%(vsew, vd) + " \\\n\
            la x7, val2; \\\n\
            vle%d.v v%d, (x7);"%(vsew, n) + " \\\n\
            la x7, val1; \\\n\
            vle%d.v v%d, (x7);"%(vsew, vs1) + " \\\n\
            inst v%d, v%d, v%d%s; "%(vd, n, vs1, (", v0.t" if masked else "")) + " \\\n\
        )", file=f)
    for n in range(1, 32):
        if n % lmul != 0:
            continue
        vs1, vs2 = valid_aligned_regs(n)
        print("#define TEST_RED_OP_vd_%d( testnum, inst, val1, val2, mask_addr )"%n + " \\\n\
        TEST_CASE( testnum, v%d, "%n + " \\\n\
            VSET_VSEW_4AVL \\\n\
            %s "%("la x7, mask_addr; \\\n    vlm.v v0, (x7); \\\n  "if masked else "")+" \
            la x7, rd_origin_data; \\\n\
            vle%d.v v%d, (x7);"%(vsew, n) + " \\\n\
            la x7, val2; \\\n\
            vle%d.v v%d, (x7);"%(vsew, vs2) + " \\\n\
            la x7, val1; \\\n\
            vle%d.v v%d, (x7);"%(vsew, vs1) + " \\\n\
            inst v%d, v%d, v%d%s; "%(n, vs2, vs1, (", v0.t" if masked else "")) + "\\\n\
        ) ", file=f)


def generate_macros_vwred(f, lmul):
    vsew = int(os.environ['RVV_ATG_VSEW'])
    masked = True if os.environ['RVV_ATG_MASKED'] == "True" else False
    # Widening Integer Reduction Instruction: vd(2*SEW), vs2(2*SEW), vs1(SEW)
    print("#define TEST_W_RED_OP( testnum, inst, val1, val2, mask_addr )  \\\n\
    TEST_CASE_W( testnum, v24, \\\n\
        VSET_VSEW_4AVL \\\n\
        %s "%("la x7, mask_addr; \\\n    vlm.v v0, (x7); \\\n  "if masked else "")+" \
        la x7, rd_origin_data; \\\n\
        vle%d.v v24, (x7);"%(vsew*2 if vsew < 64 else 64) + " \\\n\
        la x7, val2; \\\n\
        vle%d.v v8, (x7);"%(vsew*2 if vsew < 64 else 64) + " \\\n\
        la x7, val1; \\\n\
        vle%d.v v16, (x7);"%vsew + " \\\n\
        inst v24, v8, v16%s;"%(", v0.t" if masked else "") + " \\\n\
    )",file=f)    
    for n in range(1, 32):
        if n % lmul != 0:
            continue
        vd, vs2 = get_aligned_regs(n, lmul, 2*lmul, 2*lmul)
        if vd == vs2 == 0:
            continue
        print("#define TEST_W_RED_OP_vs1_%d( testnum, inst, val1, val2, mask_addr ) "%n + " \\\n\
        TEST_CASE_W( testnum, v%d, "%vd + "\\\n\
            VSET_VSEW_4AVL \\\n\
            %s "%("la x7, mask_addr; \\\n    vlm.v v0, (x7); \\\n  "if masked else "")+" \
            la x7, rd_origin_data; \\\n\
            vle%d.v v%d, (x7);"%((vsew*2 if vsew < 64 else 64), vd) + " \\\n\
            la x7, val2; \\\n\
            vle%d.v v%d, (x7);"%((vsew*2 if vsew < 64 else 64), vs2) + " \\\n\
            la x7, val1; \\\n\
            vle%d.v v%d, (x7);"%(vsew, n) + " \\\n\
            inst v%d, v%d, v%d%s; "%(vd, vs2, n, (", v0.t" if masked else "")) + " \\\n\
        )",file=f)
    for n in range(1, 32):
        if n % (2*lmul) != 0:
            continue
        vd, vs1 = get_aligned_regs(n, 2*lmul, 2*lmul, lmul)
        if vd == vs1 == 0:
            continue
        print("#define TEST_W_RED_OP_vs2_%d( testnum, inst, val1, val2, mask_addr ) "%n + " \\\n\
        TEST_CASE_W( testnum, v%d, "%vd + "\\\n\
            VSET_VSEW_4AVL \\\n\
            %s "%("la x7, mask_addr; \\\n    vlm.v v0, (x7); \\\n  "if masked else "")+" \
            la x7, rd_origin_data; \\\n\
            vle%d.v v%d, (x7);"%((vsew*2 if vsew < 64 else 64), vd) + " \\\n\
            la x7, val2; \\\n\
            vle%d.v v%d, (x7);"%((vsew*2 if vsew < 64 else 64), n) + " \\\n\
            la x7, val1; \\\n\
            vle%d.v v%d, (x7);"%(vsew, vs1) + " \\\n\
            inst v%d, v%d, v%d%s; "%(vd, n, vs1, (", v0.t" if masked else "")) + " \\\n\
        )",file=f)
    for n in range(1, 32):
        # widening instruction, vd should valid for the destination’s EMUL
        if n % (2*lmul) != 0:
            continue
        vs2, vs1 = get_aligned_regs(n, 2*lmul, 2*lmul, lmul)
        if vs2 == vs1 == 0:
            continue
        print("#define TEST_W_RED_OP_vd_%d( testnum, inst, val1, val2, mask_addr ) "%n + " \\\n\
        TEST_CASE_W( testnum, v%d, "%n + "\\\n\
            VSET_VSEW_4AVL \\\n\
            %s "%("la x7, mask_addr; \\\n    vlm.v v0, (x7); \\\n  "if masked else "")+" \
            la x7, rd_origin_data; \\\n\
            vle%d.v v%d, (x7);"%((vsew*2 if vsew < 64 else 64), n) + " \\\n\
            la x7, val2; \\\n\
            vle%d.v v%d, (x7);"%((vsew*2 if vsew < 64 else 64), vs2) + " \\\n\
            la x7, val1; \\\n\
            vle%d.v v%d, (x7);"%(vsew, vs1) + " \\\n\
            inst v%d, v%d, v%d%s; "%(n, vs2, vs1, (", v0.t" if masked else "")) + " \\\n\
        )",file=f)


def generate_macros_ext_op(f, lmul):
    vsew = int(os.environ['RVV_ATG_VSEW'])
    masked = True if os.environ['RVV_ATG_MASKED'] == "True" else False
    
    print("#undef TEST_EXT_OP \n\
#define TEST_EXT_OP( testnum, inst, val2, mask_addr ) \\\n\
    TEST_CASE_LOOP( testnum, v24,  \\\n\
        VSET_VSEW_4AVL \\\n\
        la x7, rd_origin_data; \\\n\
        vle%d.v v24, (x7);"%vsew + " \\\n\
        %s "%("la x7, mask_addr; \\\n    vlm.v v0, (x7); \\\n  "if masked else "")+" \
        la x7, val2; \\\n\
        vle%d.v v8, (x7);"%vsew + " \\\n\
        inst v24, v8%s;"%(", v0.t" if masked else "") + " \\\n\
    )", file=f)
    
    for n in range(1, 32):
        if n % lmul != 0:
            continue
        vd = get_aligned_reg(n, lmul, lmul)
        print("#define TEST_EXT_OP_vs_%d( testnum, inst, val2, mask_addr )"%n + " \\\n\
        TEST_CASE_LOOP( testnum, v24, \\\n\
            VSET_VSEW_4AVL \\\n\
            la x7, rd_origin_data; \\\n\
            vle%d.v v%d, (x7);"%(vsew, vd) + " \\\n\
            %s "%("la x7, mask_addr; \\\n    vlm.v v0, (x7); \\\n  "if masked else "")+" \
            la x7, val2; \\\n\
            vle%d.v v%d, (x7);"%(vsew, n) + " \\\n\
            inst v%d, v%d%s; "%(vd, n, ", v0.t" if masked else "") + " \\\n\
        )", file = f)

    for n in range(1, 32):
        if n % lmul != 0:
            continue
        vs = get_aligned_reg(n, lmul, lmul)
        print("#define TEST_EXT_OP_vd_%d( testnum, inst, val2, mask_addr )"%n + " \\\n\
            TEST_CASE_LOOP( testnum, v%d, "%n + " \\\n\
                VSET_VSEW_4AVL \\\n\
                la x7, rd_origin_data; \\\n\
                vle%d.v v%d, (x7);"%(vsew, n) + " \\\n\
                %s "%("la x7, mask_addr; \\\n    vlm.v v0, (x7); \\\n  "if masked else "")+" \
                la x7, val2; \\\n\
                vle%d.v v%d, (x7);"%(vsew, vs) + " \\\n\
                inst v%d, v%d%s; "%(n, vs, ", v0.t" if masked else "") + " \\\n\
            )", file = f)


def generate_tests_vvvxvi(instr, f, rs1_val, rs2_val, lmul, instr_suffix='vv', generate_vi = True, generate_vx = True, generate_vv = True):
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
    if generate_vv:
        print("  #-------------------------------------------------------------", file=f)
        print("  # VV Tests", file=f)
        print("  #-------------------------------------------------------------", file=f)
        for i in range(loop_num):
            n += 1
            print("  TEST_VV_OP( "+str(n)+",  %s.%s, "%(instr, instr_suffix) + "rs2_data+%d, rs1_data+%d, mask_data+%d)"%(i*step_bytes, i*step_bytes, j*mask_bytes), file=f)
            j = (j + 1) % mask_num
        for i in range(1, 32):     
            if i % lmul != 0:
                continue
            k = i % loop_num
            n += 1
            print("  TEST_VV_OP_vd_%d( "%i+str(n)+",  %s.%s, "%(instr, instr_suffix)+"rs2_data+%d, rs1_data+%d, mask_data+%d)"%(k*step_bytes, k*step_bytes, j*mask_bytes),file=f)
            j = (j + 1) % mask_num
            
            n += 1
            print("  TEST_VV_OP_vs1_%d( "%i+str(n)+",  %s.%s, "%(instr, instr_suffix)+"rs2_data+%d, rs1_data+%d, mask_data+%d)"%(k*step_bytes, k*step_bytes, j*mask_bytes),file=f)
            j = (j + 1) % mask_num
    vv_test_num = n

    if generate_vx:
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
    
    if generate_vi:
        print("  #-------------------------------------------------------------", file=f)
        print("  # VI Tests", file=f)
        print("  #-------------------------------------------------------------", file=f)
        for i in range(loop_num):
            n += 1
            print("  TEST_VI_OP( "+str(n)+",  %s.vi, " %instr+"rs2_data+%d, 15, mask_data+%d)"%(i*step_bytes, j*mask_bytes), file=f)
            j = (j + 1) % mask_num
    vi_test_num = n - vv_test_num - vx_test_num

    return (vv_test_num, vx_test_num, vi_test_num)


def generate_tests_vw(f, rs1_val, rs2_val, instr, lmul, instr_suffix='vv', generate_wvwx = True):
    vlen = int(os.environ['RVV_ATG_VLEN'])
    vsew = int(os.environ['RVV_ATG_VSEW'])
    
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
    print("  #-------------------------------------------------------------", file=f)
    print("  # VV Tests", file=f)
    print("  #-------------------------------------------------------------", file=f)

    for i in range(loop_num):
        n += 1
        print("  TEST_W_VV_OP( "+str(n)+",  %s.%s, " %(instr, instr_suffix)+"rs2_data+%d, rs1_data+%d, mask_data+%d)"%(i*step_bytes, i*step_bytes, j*mask_bytes), file=f)
        j = (j + 1) % mask_num
    
    for i in range(1, 32):
        if i % lmul != 0 or get_aligned_regs(i, lmul, 2*lmul, lmul) == (0, 0):
            continue
        k = i % loop_num
        n += 1
        print("  TEST_W_VV_OP_vs1_%d( "%i+str(n)+",  %s.%s, "%(instr, instr_suffix)+"rs2_data+%d, rs1_data+%d, mask_data+%d)"%(k*step_bytes, k*step_bytes, j*mask_bytes),file=f)
        j = (j + 1) % mask_num
    
    for i in range(1, 32):  
        if i % (2*lmul) != 0 or get_aligned_regs(i, 2*lmul, lmul, lmul) == (0, 0):
            continue
        k = i % loop_num
        n += 1
        print("  TEST_W_VV_OP_vd_%d( "%i+str(n)+",  %s.%s, "%(instr, instr_suffix)+"rs2_data+%d, rs1_data+%d, mask_data+%d)"%(k*step_bytes, k*step_bytes, j*mask_bytes),file=f)
        j = (j + 1) % mask_num
    
    vv_test_num = n
    
    print("  #-------------------------------------------------------------", file=f)
    print("  # VX Tests", file=f)
    print("  #-------------------------------------------------------------", file=f)
    
    for i in range(loop_num):
        n += 1
        print("  TEST_W_VX_OP( "+str(n)+",  %s.vx, " %instr+"rs2_data+%d, %s, mask_data+%d)"%(i*step_bytes, rs1_val[i], j*mask_bytes), file=f)
        j = (j + 1) % mask_num
    vx_test_num = n - vv_test_num

    wv_test_num = 0
    wx_test_num = 0
    if generate_wvwx:
        print("  #-------------------------------------------------------------", file=f)
        print("  # WV Tests", file=f)
        print("  #-------------------------------------------------------------", file=f)
        
        for i in range(loop_num):
            n += 1
            print("  TEST_W_WV_OP( "+str(n)+",  %s.wv, " %instr+"rs2_data_widen+%d, rs1_data+%d, mask_data+%d)"%(i*step_bytes_double, i*step_bytes, j*mask_bytes), file=f)
            j = (j + 1) % mask_num
        
        print("  #-------------------------------------------------------------", file=f)
        print("  # WX Tests", file=f)
        print("  #-------------------------------------------------------------", file=f)
        
        for i in range(loop_num):
            n += 1
            print("  TEST_W_WX_OP( "+str(n)+",  %s.wx, " %instr+"rs2_data_widen+%d, %s, mask_data+%d)"%(i*step_bytes_double, rs1_val[i], j*mask_bytes), file=f)
            j = (j + 1) % mask_num
        
        wv_test_num = wx_test_num = loop_num
    
    return (vv_test_num, vx_test_num, wv_test_num, wx_test_num)

    
def generate_tests_vwmacc(f, rs1_val, rs2_val, instr, lmul, generate_vv = True):
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
    if generate_vv:
        print("  #-------------------------------------------------------------", file=f)
        print("  # VV Tests", file=f)
        print("  #-------------------------------------------------------------", file=f)

        for i in range(loop_num):
            n += 1
            print("  TEST_W_MA_VV_OP( "+str(n)+",  %s.%s, " %(instr, 'vv')+"rs1_data+%d, rs2_data+%d, mask_data+%d)"%(i*step_bytes, i*step_bytes, j*mask_bytes), file=f)
            j = (j + 1) % mask_num
        
        for i in range(1, 32):
            if i % lmul != 0 or get_aligned_regs(i, lmul, 2*lmul, lmul) == (0, 0):
                continue
            k = i % loop_num
            n += 1
            print("  TEST_W_MA_VV_OP_vs1_%d( "%i+str(n)+",  %s.%s, "%(instr, 'vv')+"rs1_data+%d, rs2_data+%d, mask_data+%d)"%(k*step_bytes, k*step_bytes, j*mask_bytes),file=f)
            j = (j + 1) % mask_num
        
        for i in range(1, 32):  
            if i % (2*lmul) != 0 or get_aligned_regs(i, 2*lmul, lmul, lmul) == (0, 0):
                continue
            k = i % loop_num
            n += 1
            print("  TEST_W_MA_VV_OP_vd_%d( "%i+str(n)+",  %s.%s, "%(instr, 'vv')+"rs1_data+%d, rs2_data+%d, mask_data+%d)"%(k*step_bytes, k*step_bytes, j*mask_bytes),file=f)
            j = (j + 1) % mask_num

    vv_test_num = n
    
    print("  #-------------------------------------------------------------", file=f)
    print("  # VX Tests", file=f)
    print("  #-------------------------------------------------------------", file=f)
    
    for i in range(loop_num):
        n += 1
        print("  TEST_W_MA_VX_OP( "+str(n)+",  %s.vx, " %instr+" %s, rs2_data+%d, mask_data+%d)"%(rs1_val[i], i*step_bytes, j*mask_bytes), file=f)
        j = (j + 1) % mask_num
    vx_test_num = n - vv_test_num
    
    return (vv_test_num, vx_test_num, 0)


def generate_tests_muladd(instr, f, rs1_val, rs2_val, lmul):
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
        n += 1
        print("  TEST_MA_VV_OP( "+str(n)+",  %s.vv, " %instr + " rs1_data+%d, rs2_data+%d, mask_data+%d)"%(i*step_bytes, i*step_bytes, j*mask_bytes), file=f)
        j = (j + 1) % mask_num
    
    for i in range(1, 32):     
        if i % lmul != 0:
            continue
        k = i % loop_num
        n += 1
        print("  TEST_MA_VV_OP_vd_%d( "%i+str(n)+",  %s.vv, "%instr+ "rs1_data+%d, rs2_data+%d, mask_data+%d)"%(k*step_bytes, k*step_bytes, j*mask_bytes),file=f)
        j = (j + 1) % mask_num
        
        n += 1
        print("  TEST_MA_VV_OP_vs1_%d( "%i+str(n)+",  %s.vv, "%instr + "rs1_data+%d, rs2_data+%d, mask_data+%d)"%(k*step_bytes, k*step_bytes, j*mask_bytes),file=f)
        j = (j + 1) % mask_num

    vv_test_num = n
    
    print("  #-------------------------------------------------------------", file=f)
    print("  # VX Tests", file=f)
    print("  #-------------------------------------------------------------", file=f)
    
    for i in range(loop_num):
        n += 1
        print("  TEST_MA_VX_OP( "+str(n)+",  %s.vx, " %instr + " %s, rs2_data+%d, mask_data+%d)"%(rs1_val[i], i*step_bytes, j*mask_bytes), file=f)
        j = (j + 1) % mask_num
    vx_test_num = n - vv_test_num
    
    return (vv_test_num, vx_test_num, 0)


def generate_tests_vvmvxmvim(instr, f, rs1_val, rs2_val, lmul, generate_vi=True):
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
        n += 1
        print("  TEST_VV_M_OP( "+str(n)+",  %s.vvm, " %instr+"rs2_data+%d, rs1_data+%d, mask_data+%d)"%( i*step_bytes, i*step_bytes, j*mask_bytes), file=f)
        j = (j + 1) % mask_num
    for i in range(1, 32):     
        if i % lmul != 0:
            continue
        k = i % loop_num
        n += 1
        print("  TEST_VV_M_OP_vd_%d( "%i+str(n)+",  %s.vvm, "%instr+"rs2_data+%d, rs1_data+%d, mask_data+%d)"%(k*step_bytes, k*step_bytes, j*mask_bytes),file=f)
        j = (j + 1) % mask_num
        
        n += 1
        print("  TEST_VV_M_OP_vs1_%d( "%i+str(n)+",  %s.vvm, "%instr+"rs2_data+%d, rs1_data+%d, mask_data+%d)"%(k*step_bytes, k*step_bytes, j*mask_bytes),file=f)
        j = (j + 1) % mask_num
    vv_test_num = n
    
    print("  #-------------------------------------------------------------", file=f)
    print("  # VX Tests", file=f)
    print("  #-------------------------------------------------------------", file=f)
    
    for i in range(loop_num):
        n += 1
        print("  TEST_VX_M_OP( "+str(n)+",  %s.vxm, " %instr+" rs2_data+%d, %s, mask_data+%d)"%(i*step_bytes, rs1_val[i % len(rs1_val)], j*mask_bytes), file=f)
        j = (j + 1) % mask_num
    vx_test_num = n - vv_test_num
    
    if generate_vi:
        print("  #-------------------------------------------------------------", file=f)
        print("  # VI Tests", file=f)
        print("  #-------------------------------------------------------------", file=f)
        for i in range(loop_num):
            n += 1
            print("  TEST_VI_M_OP( "+str(n)+",  %s.vim, " %instr+"rs2_data+%d, 14, mask_data+%d)"%(i*step_bytes, j*mask_bytes), file=f)
            j = (j + 1) % mask_num
    vi_test_num = n - vv_test_num - vx_test_num

    return (vv_test_num, vx_test_num, vi_test_num)


def generate_tests_mask(instr, f, rs1_val, rs2_val, lmul, generate_vv=True, generate_vx=True, generate_vi=True, is_adc_sbc=False):
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
    
    masked = True if os.environ['RVV_ATG_MASKED'] == "True" else False
    vv_suffix = "vvm" if is_adc_sbc and masked else "vv"
    vx_suffix = "vxm" if is_adc_sbc and masked else "vx"
    vi_suffix = "vim" if is_adc_sbc and masked else "vi"
    
    n = 0
    if generate_vv:
        print("  #-------------------------------------------------------------", file=f)
        print("  # VV Tests", file=f)
        print("  #-------------------------------------------------------------", file=f)

        for i in range(loop_num):
            n += 1
            print("  TEST_M_VV_OP( "+str(n)+",  %s.%s, " %(instr, vv_suffix)+" rs2_data+%d, rs1_data+%d, mask_data+%d)"%(i*step_bytes, i*step_bytes, j*mask_bytes), file=f)
            j = (j + 1) % mask_num
        
        for i in range(1, 32): 
            k = i % loop_num
            
            n += 1
            print("  TEST_M_VV_OP_vd_%d( "%i+str(n)+",  %s.%s, "%(instr, vv_suffix)+" rs2_data+%d, rs1_data+%d, mask_data+%d)"%(k*step_bytes, k*step_bytes, j*mask_bytes),file=f)
            j = (j + 1) % mask_num
            
            if i % lmul != 0:
                continue
            n += 1
            print("  TEST_M_VV_OP_vs1_%d( "%i+str(n)+",  %s.%s, "%(instr, vv_suffix)+" rs2_data+%d, rs1_data+%d, mask_data+%d)"%(k*step_bytes, k*step_bytes, j*mask_bytes),file=f)
            j = (j + 1) % mask_num
    
    vv_test_num = n

    if generate_vx:
        print("  #-------------------------------------------------------------", file=f)
        print("  # VX Tests", file=f)
        print("  #-------------------------------------------------------------", file=f)
        
        for i in range(loop_num):
            n += 1
            print("  TEST_M_VX_OP( "+str(n)+",  %s.%s, " %(instr, vx_suffix)+" rs2_data+%d, %s, mask_data+%d)"%(i*step_bytes, rs1_val[i % len(rs1_val)], j*mask_bytes), file=f)
            j = (j + 1) % mask_num
        
        for i in range(1, 32):
            k = i % loop_num
        
            n += 1
            print("  TEST_M_VX_OP_vd_%d( "%i+str(n)+",  %s.%s, "%(instr, vx_suffix)+" rs2_data+%d, %s, mask_data+%d)"%(k*step_bytes, rs1_val[i % len(rs1_val)], j*mask_bytes),file=f)
            j = (j + 1) % mask_num
            
            if i % lmul != 0:
                continue
            n += 1
            print("  TEST_M_VX_OP_vs2_%d( "%i+str(n)+",  %s.%s, "%(instr, vx_suffix)+" rs2_data+%d, %s, mask_data+%d)"%(k*step_bytes, rs1_val[i % len(rs1_val)], j*mask_bytes),file=f)
            j = (j + 1) % mask_num
    
    vx_test_num = n - vv_test_num
    
    if generate_vi:
        print("  #-------------------------------------------------------------", file=f)
        print("  # VI Tests", file=f)
        print("  #-------------------------------------------------------------", file=f)
        
        for i in range(loop_num):
            n += 1
            print("  TEST_M_VI_OP( "+str(n)+",  %s.%s, " %(instr, vi_suffix)+" rs2_data+%d, 4, mask_data+%d)"%(i*step_bytes, j*mask_bytes), file=f)
            j = (j + 1) % mask_num
    
    vi_test_num = n - vv_test_num - vx_test_num
    
    return (vv_test_num, vx_test_num, vi_test_num)


def generate_tests_vn(instr, f, rs1_val, rs2_val, lmul):
    vlen = int(os.environ['RVV_ATG_VLEN'])
    vsew = int(os.environ['RVV_ATG_VSEW'])
    
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
    print("  #-------------------------------------------------------------", file=f)
    print("  # VV Tests", file=f)
    print("  #-------------------------------------------------------------", file=f)

    for i in range(loop_num):
        n += 1
        print("  TEST_N_VV_OP( "+str(n)+",  %s.wv, " %instr + "rs2_data+%d, rs1_data+%d, mask_data+%d)"%(i*step_bytes_double, i*step_bytes, j*mask_bytes), file=f)
        j = (j + 1) % mask_num
    
    for i in range(1, 32):
        if i % lmul != 0 or get_aligned_regs(i, lmul, 2*lmul, lmul) == (0, 0):
            continue
        k = i % loop_num
        n += 1
        print("  TEST_N_VV_OP_vd_%d( "%i+str(n)+",  %s.wv, "%instr + "rs2_data+%d, rs1_data+%d, mask_data+%d)"%(k*step_bytes_double, k*step_bytes, j*mask_bytes),file=f)
        j = (j + 1) % mask_num
    
    for i in range(1, 32):
        if i % lmul != 0 or get_aligned_regs(i, lmul, lmul, 2*lmul) == (0, 0):
            continue
        k = i % loop_num
        n += 1
        print("  TEST_N_VV_OP_vs1_%d( "%i+str(n)+",  %s.wv, "%instr + "rs2_data+%d, rs1_data+%d, mask_data+%d)"%(k*step_bytes_double, k*step_bytes, j*mask_bytes),file=f)
        j = (j + 1) % mask_num
        
    for i in range(1, 32):  
        if i % (2*lmul) != 0 or get_aligned_regs(i, 2*lmul, lmul, lmul) == (0, 0):
            continue
        k = i % loop_num
        n += 1
        print("  TEST_N_VV_OP_vs2_%d( "%i+str(n)+",  %s.wv, "%instr + "rs2_data+%d, rs1_data+%d, mask_data+%d)"%(k*step_bytes_double, k*step_bytes, j*mask_bytes),file=f)
        j = (j + 1) % mask_num
    
    vv_test_num = n
    
    print("  #-------------------------------------------------------------", file=f)
    print("  # VX Tests", file=f)
    print("  #-------------------------------------------------------------", file=f)
    
    for i in range(loop_num):
        n += 1
        print("  TEST_N_VX_OP( "+str(n)+",  %s.wx, " %instr+"rs2_data+%d, %s, mask_data+%d)"%( i*step_bytes_double, rs1_val[i % len(rs1_val)], j*mask_bytes), file=f)
        j = (j + 1) % mask_num
    vx_test_num = n - vv_test_num
    
    print("  #-------------------------------------------------------------", file=f)
    print("  # VI Tests", file=f)
    print("  #-------------------------------------------------------------", file=f)

    for i in range(loop_num):
        n += 1
        print("  TEST_N_VI_OP( "+str(n)+",  %s.wi, " %instr+" rs2_data+%d, 4, mask_data+%d)"%( i*step_bytes_double, j*mask_bytes), file=f)
        j = (j + 1) % mask_num
    vi_test_num = n - vv_test_num - vx_test_num
    
    return (vv_test_num, vx_test_num, vi_test_num)


def generate_tests_vred(instr, f, rs1_val, rs2_val, lmul, instr_suffix='vs'):
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
    print("  # %s Tests"%instr, file=f)
    print("  #-------------------------------------------------------------", file=f)

    for i in range(loop_num):
        n += 1
        print("  TEST_RED_OP( "+str(n)+",  %s.%s, " %(instr, instr_suffix)+"rs1_data+%d, rs2_data+%d, mask_data+%d)"%(i*step_bytes, i*step_bytes, j*mask_bytes), file=f)
        j = (j + 1) % mask_num
    
    for i in range(1, 32):     
        if i % lmul != 0:
            continue
        k = i % loop_num
        
        n += 1
        print("  TEST_RED_OP_vd_%d( "%i+str(n)+",  %s.%s, "%(instr, instr_suffix)+"rs1_data+%d, rs2_data+%d, mask_data+%d)"%(k*step_bytes, k*step_bytes, j*mask_bytes),file=f)
        j = (j + 1) % mask_num
        
        n += 1
        print("  TEST_RED_OP_vs2_%d( "%i+str(n)+",  %s.%s, "%(instr, instr_suffix)+"rs1_data+%d, rs2_data+%d, mask_data+%d)"%(k*step_bytes, k*step_bytes, j*mask_bytes),file=f)
        j = (j + 1) % mask_num
    
    return n


def generate_tests_vwred(f, rs1_val, rs2_val, instr, lmul, instr_suffix='vv'):
    vlen = int(os.environ['RVV_ATG_VLEN'])
    vsew = int(os.environ['RVV_ATG_VSEW'])
    
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
    print("  #-------------------------------------------------------------", file=f)
    print("  # %s Tests"%instr, file=f)
    print("  #-------------------------------------------------------------", file=f)

    for i in range(loop_num):
        n += 1
        print("  TEST_W_RED_OP( "+str(n)+",  %s.%s, " %(instr, instr_suffix)+"rs1_data+%d, rs2_data+%d, mask_data+%d)"%(i*step_bytes, i*step_bytes_double, j*mask_bytes), file=f)
        j = (j + 1) % mask_num
    
    print("  #-------------------------------------------------------------", file=f)
    print("  # %s Tests (different register)"%instr, file=f)
    print("  #-------------------------------------------------------------", file=f)
    
    for i in range(1, 32):
        if i % lmul != 0 or get_aligned_regs(i, lmul, 2*lmul, 2*lmul) == (0, 0):
            continue
        k = i % loop_num
        
        n += 1
        print("  TEST_W_RED_OP_vs1_%d( "%i+str(n)+",  %s.%s, "%(instr, instr_suffix)+"rs1_data+%d, rs2_data+%d, mask_data+%d)"%(k*step_bytes, k*step_bytes_double, j*mask_bytes),file=f)
        j = (j + 1) % mask_num
    
    for i in range(1, 32):
        if i % (2*lmul) != 0 or get_aligned_regs(i, 2*lmul, 2*lmul, lmul) == (0, 0):
            continue
        k = i % loop_num
        
        n += 1
        print("  TEST_W_RED_OP_vs2_%d( "%i+str(n)+",  %s.%s, "%(instr, instr_suffix)+"rs1_data+%d, rs2_data+%d, mask_data+%d)"%(k*step_bytes, k*step_bytes_double, j*mask_bytes),file=f)
        j = (j + 1) % mask_num
        
        n += 1
        print("  TEST_W_RED_OP_vd_%d( "%i+str(n)+",  %s.%s, "%(instr, instr_suffix)+"rs1_data+%d, rs2_data+%d, mask_data+%d)"%(k*step_bytes, k*step_bytes_double, j*mask_bytes),file=f)
        j = (j + 1) % mask_num
    
    return n


def generate_tests_ext_op(instr, f, rs1_val, rs2_val, lmul):
    vlen = int(os.environ['RVV_ATG_VLEN'])
    vsew = int(os.environ['RVV_ATG_VSEW'])
    
    num_elem = int(vlen * lmul / vsew)
    if num_elem == 0:
        return 0
    loop_num = int(len(rs2_val) / num_elem)
    step_bytes = int(vlen * lmul / 8)
    
    vlmax = num_elem
    mask_bytes = 4 * math.ceil(vlmax / 32) # 4 * num_words
    mask_num = vlmax * 2 + 4
    j = 0
    
    n = count1 = count2 = count3 = 0
    print("  #-------------------------------------------------------------",file=f)
    print("  # %s Tests"%instr,file=f)
    print("  #-------------------------------------------------------------",file=f)
    
    for i in range(loop_num):
        if int(vsew / 2) >= 8 and lmul / 2 >= 0.125: 
            n += 1
            print("TEST_EXT_OP( %d,  %s.vf2, "%(n, instr) + "rs2_data+%d, mask_data+%d);"%(i*step_bytes, j*mask_bytes), file=f)
            j = (j + 1) % mask_num
            count1 += 1
    
    for i in range(loop_num):
        if int(vsew / 4) >= 8 and lmul / 4 >= 0.125:
            n += 1
            print("TEST_EXT_OP( %d,  %s.vf4, "%(n, instr) + "rs2_data+%d, mask_data+%d);"%(i*step_bytes, j*mask_bytes), file=f)
            j = (j + 1) % mask_num
            count2 += 1
    
    for i in range(loop_num):
        if int(vsew / 8) >= 8 and lmul / 8 >= 0.125:
            n += 1
            print("TEST_EXT_OP( %d,  %s.vf8, "%(n, instr) + "rs2_data+%d, mask_data+%d);"%(i*step_bytes, j*mask_bytes), file=f)
            j = (j + 1) % mask_num
            count3 += 1
    
    print("  #-------------------------------------------------------------",file=f)
    print("  # %s Tests (different register)"%instr,file=f)
    print("  #-------------------------------------------------------------",file=f)
    test_suffix = ["vd", "vs"]
    
    for i in range(1, 32):     
        if i % lmul != 0:
            continue
        k = i % loop_num
        
        if int(vsew / 2) >= 8 and lmul / 2 >= 0.125:
            for t in test_suffix:
                n += 1
                print("TEST_EXT_OP_%s_%d( %d,  %s.vf2, "%(t, i, n, instr) + "rs2_data+%d, mask_data+%d);"%(k*step_bytes, j*mask_bytes), file=f)
                j = (j + 1) % mask_num
                count1 += 1
        
        if int(vsew / 4) >= 8 and lmul / 4 >= 0.125:
            for t in test_suffix:
                n += 1
                print("TEST_EXT_OP_%s_%d( %d,  %s.vf4, "%(t, i, n, instr) + "rs2_data+%d, mask_data+%d);"%(k*step_bytes, j*mask_bytes), file=f)
                j = (j + 1) % mask_num
                count2 += 1
        
        if int(vsew / 8) >= 8 and lmul / 8 >= 0.125:
            for t in test_suffix:
                n += 1
                print("TEST_EXT_OP_%s_%d( %d,  %s.vf8, "%(t, i, n, instr) + "rs2_data+%d, mask_data+%d);"%(k*step_bytes, j*mask_bytes), file=f)
                j = (j + 1) % mask_num
                count3 += 1
    
    return (count1, count2, count3)
