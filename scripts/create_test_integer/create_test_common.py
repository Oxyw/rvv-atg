import os
import re
import math

from scripts.test_common_info import is_overlap, valid_aligned_regs


def generate_macros_vvvxvi(f, lmul):
    vlen = int(os.environ['RVV_ATG_VLEN'])
    vsew = int(os.environ['RVV_ATG_VSEW'])
    lmul = 1 if lmul < 1 else int(lmul)
    masked = True if os.environ['RVV_ATG_MASKED'] == "True" else False
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
    print("#define TEST_VX_OP( testnum, inst, val2, val1, mask_addr ) \\\n\
        TEST_CASE_LOOP( testnum, v16, \\\n\
            VSET_VSEW_4AVL \\\n\
            la x7, rd_origin_data; \\\n\
            vle%d.v v16, (x7);"%vsew + " \\\n\
            %s "%("la x7, mask_addr; \\\n    vlm.v v0, (x7); \\\n  "if masked else "")+" \
            la x7, val2; \\\n\
            vle%d.v v8, (x7);"%vsew + " \\\n\
            li x1, MASK_XLEN(val1); \\\n\
            inst v16, v8, x1%s;"%(", v0.t" if masked else "") + " ; \\\n\
        )", file=f)
    print("#define TEST_VI_OP( testnum, inst, val2, val1, mask_addr ) \\\n\
        TEST_CASE_LOOP( testnum, v16, \\\n\
            VSET_VSEW_4AVL \\\n\
            la x7, rd_origin_data; \\\n\
            vle%d.v v16, (x7);"%vsew + " \\\n\
            %s "%("la x7, mask_addr; \\\n    vlm.v v0, (x7); \\\n  "if masked else "")+" \
            la x7, val2; \\\n\
            vle%d.v v8, (x7);"%vsew + " \\\n\
            inst v16, v8, SEXT_IMM(val1)%s;"%(", v0.t" if masked else "") + " ; \\\n\
        )", file=f)
    for n in range(2, 32):
        if n % lmul != 0 or n == 8 or n == 16 or n == 24:
            continue
        print("#define TEST_VV_OP_1%d( testnum, inst, val2, val1, mask_addr )"%n + " \\\n\
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
        if n % lmul != 0 or n == 24:
            continue
        # Beacuse of the widening instruction, rd should valid for the destination’s EMUL
        vs2, vs1 = 16, 8
        if n == 8:
            vs2, vs1 = 24, 16
        elif n == 16:
            vs2, vs1 = 24, 8            
        print("#define TEST_VV_OP_rd%d( testnum, inst, val2, val1, mask_addr )"%n + " \\\n\
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


def generate_macros_vw(f, lmul):
    vsew = int(os.environ['RVV_ATG_VSEW'])
    lmul_1 = 1 if lmul < 1 else int(lmul)
    masked = True if os.environ['RVV_ATG_MASKED'] == "True" else False
    print("#undef TEST_W_WV_OP \n\
#define TEST_W_WV_OP( testnum, inst, val1, val2, mask_addr ) \\\n\
    TEST_CASE_LOOP_W( testnum, v24, \\\n\
        VSET_VSEW_4AVL \\\n\
        la x7, rd_origin_data; \\\n\
        vle%d.v v24, (x7);"%(64 if vsew == 64 else vsew*2) + " \\\n\
        %s "%("la x7, mask_addr; \\\n    vlm.v v0, (x7); \\\n  "if masked else "")+" \
        la x7, val1; \\\n\
        vle%d.v v8, (x7);"%(64 if vsew == 64 else vsew*2) + " \\\n\
        la x7, val2; \\\n\
        vle%d.v v16, (x7);"%vsew + " \\\n\
        inst v24, v8, v16%s;"%(", v0.t" if masked else "") + " ; ; \\\n\
    )", file=f)

    print("#undef TEST_W_WX_OP \n\
#define TEST_W_WX_OP( testnum, inst, val1, val2, mask_addr ) \\\n\
    TEST_CASE_LOOP_W( testnum, v24, \\\n\
        VSET_VSEW_4AVL \\\n\
        la x7, rd_origin_data; \\\n\
        vle%d.v v24, (x7);"%(64 if vsew == 64 else vsew*2) + " \\\n\
        %s "%("la x7, mask_addr; \\\n    vlm.v v0, (x7); \\\n  "if masked else "")+" \
        la x7, val1; \\\n\
        vle%d.v v8, (x7);"%(64 if vsew == 64 else vsew*2) + " \\\n\
        li x1, MASK_XLEN(val2); \\\n\
        inst v24, v8, x1%s;"%(", v0.t" if masked else "") + " ; ; \\\n\
    )", file=f)

    print("#undef TEST_W_VV_OP \n\
#define TEST_W_VV_OP( testnum, inst, val1, val2, mask_addr ) \\\n\
    TEST_CASE_LOOP_W( testnum, v24, \\\n\
        VSET_VSEW_4AVL \\\n\
        la x7, rd_origin_data; \\\n\
        vle%d.v v24, (x7);"%(64 if vsew == 64 else vsew*2) + " \\\n\
        %s "%("la x7, mask_addr; \\\n    vlm.v v0, (x7); \\\n  "if masked else "")+" \
        la x7, val1; \\\n\
        vle%d.v v8, (x7);"%vsew + " \\\n\
        la x7, val2; \\\n\
        vle%d.v v16, (x7);"%vsew + " \\\n\
        inst v24, v8, v16%s;"%(", v0.t" if masked else "") + " ; ; \\\n\
    )", file=f)

    print("#undef TEST_W_VX_OP \n\
#define TEST_W_VX_OP( testnum, inst, val1, val2, mask_addr ) \\\n\
    TEST_CASE_LOOP_W( testnum, v24, \\\n\
        VSET_VSEW_4AVL \\\n\
        la x7, rd_origin_data; \\\n\
        vle%d.v v24, (x7);"%(64 if vsew == 64 else vsew*2) + " \\\n\
        %s "%("la x7, mask_addr; \\\n    vlm.v v0, (x7); \\\n  "if masked else "")+" \
        la x7, val1; \\\n\
        vle%d.v v8, (x7);"%vsew + " \\\n\
        li x1, MASK_XLEN(val2); \\\n\
        inst v24, v8, x1%s;"%(", v0.t" if masked else "") + " ; ; \\\n\
    )", file=f)

    for n in range(1, 32):
        if n != 8 and n != 16 and n != 24 and n % lmul == 0:
            print("#define TEST_W_VV_OP_1%d( testnum, inst, val1, val2, mask_addr )"%n + " \\\n\
            TEST_CASE_LOOP_W( testnum, v24, \\\n\
                VSET_VSEW_4AVL \\\n\
                la x7, rd_origin_data; \\\n\
                vle%d.v v24, (x7);"%(64 if vsew == 64 else vsew*2) + " \\\n\
                %s "%("la x7, mask_addr; \\\n    vlm.v v0, (x7); \\\n  "if masked else "")+" \
                la x7, val1; \\\n\
                vle%d.v v8, (x7);"%(vsew) + " \\\n\
                la x7, val2; \\\n\
                vle%d.v v%d, (x7);"%(vsew, n) + " \\\n\
                inst v24, v8, v%d%s;"%(n, (", v0.t" if masked else ""))+" \\\n\
            )",file=f)
    for n in range(1, 32):
        # Beacuse of the widening instruction, rd should valid for the destination’s EMUL
        if n%(2*lmul) ==0 and n != 8 and n != 16 and n != 24:
            print("#define TEST_W_VV_OP_rd%d( testnum, inst, val1, val2, mask_addr )"%n + " \\\n\
            TEST_CASE_LOOP_W( testnum, v%d, "%n + "\\\n\
                VSET_VSEW_4AVL \\\n\
                la x7, rd_origin_data; \\\n\
                vle%d.v v%d, (x7);"%(64 if vsew == 64 else vsew*2, n) + " \\\n\
                %s "%("la x7, mask_addr; \\\n    vlm.v v0, (x7); \\\n  "if masked else "")+" \
                la x7, val1; \\\n\
                vle%d.v v8, (x7);"%(vsew) + " \\\n\
                la x7, val2; \\\n\
                vle%d.v v16, (x7);"%vsew + " \\\n\
                inst v%d, v8, v16%s;"%(n, (", v0.t" if masked else ""))+" \\\n\
            )",file=f)

def generate_macros_vwmacc(f, lmul):
    vsew = int(os.environ['RVV_ATG_VSEW'])
    masked = True if os.environ['RVV_ATG_MASKED'] == "True" else False
    print("#undef TEST_W_VX_OP_RV \n\
#define TEST_W_VX_OP_RV( testnum, inst, val1, val2, mask_addr ) \\\n\
    TEST_CASE_LOOP_W( testnum, v24, \\\n\
        VSET_DOUBLE_VSEW_4AVL \\\n\
        la x7, rd_origin_data; \\\n\
        vle%d.v v24, (x7);"%(64 if vsew == 64 else vsew*2) + " \\\n\
        VSET_VSEW_4AVL \\\n\
        %s "%("la x7, mask_addr; \\\n    vlm.v v0, (x7); \\\n  "if masked else "")+" \
        la x7, val2; \\\n\
        vle%d.v v8, (x7);"%vsew + " \\\n\
        li x1, MASK_XLEN(val1); \\\n\
        inst v24, x1, v8%s;"%(", v0.t" if masked else "")+" ; \\\n\
    )", file=f)

    print("#undef TEST_W_VV_OP_WITH_INIT \n\
#define TEST_W_VV_OP_WITH_INIT( testnum, inst, val1, val2, mask_addr ) \\\n\
    TEST_CASE_LOOP_W( testnum, v24, \\\n\
        VSET_DOUBLE_VSEW_4AVL \\\n\
        la x7, rd_origin_data; \\\n\
        vle%d.v v24, (x7);"%(64 if vsew == 64 else vsew*2) + " \\\n\
        VSET_VSEW_4AVL \\\n\
        %s "%("la x7, mask_addr; \\\n    vlm.v v0, (x7); \\\n  "if masked else "")+" \
        la x7, val1; \\\n\
        vle%d.v v8, (x7);"%vsew + " \\\n\
        la x7, val2; \\\n\
        vle%d.v v16, (x7);"%vsew + " \\\n\
        inst v24, v8, v16%s;"%((", v0.t" if masked else ""))+" ; \\\n\
    )", file=f)

    for n in range(2, 32):
        if n != 8 and n != 16 and n != 24 and n % lmul == 0:
            print("#define TEST_W_VV_OP_WITH_INIT_1%d( testnum, inst, val1, val2, mask_addr ) "%n + " \\\n\
            TEST_CASE_LOOP_W( testnum, v24,  \\\n\
                VSET_DOUBLE_VSEW_4AVL \\\n\
                la x7, rd_origin_data; \\\n\
                vle%d.v v24, (x7);"%(64 if vsew == 64 else vsew*2) + " \\\n\
                VSET_VSEW_4AVL \\\n\
                %s "%("la x7, mask_addr; \\\n    vlm.v v0, (x7); \\\n  "if masked else "")+" \
                la x7, val1; \\\n\
                vle%d.v v8, (x7);"%vsew + " \\\n\
                la x7, val2; \\\n\
                vle%d.v v%d, (x7);"%(vsew, n) + " \\\n\
                inst v24, v8, v%d%s; "%(n, (", v0.t" if masked else "")) + " \\\n\
                )",file=f)
    for n in range(1, 32):
        # Beacuse of the widening instruction, rd should valid for the destination’s EMUL
        if n%(2*lmul) ==0 and n != 8 and n != 16 and n != 24:
            print("#define TEST_W_VV_OP_WITH_INIT_rd%d( testnum, inst, val1, val2, mask_addr ) "%n + " \\\n\
            TEST_CASE_LOOP_W( testnum, v%d, "%n + "\\\n\
                VSET_DOUBLE_VSEW_4AVL \\\n\
                la x7, rd_origin_data; \\\n\
                vle%d.v v%d, (x7);"%(64 if vsew == 64 else vsew*2, n) + " \\\n\
                VSET_VSEW_4AVL \\\n\
                %s "%("la x7, mask_addr; \\\n    vlm.v v0, (x7); \\\n  "if masked else "")+" \
                la x7, val1; \\\n\
                vle%d.v v8, (x7);"%vsew + " \\\n\
                la x7, val2; \\\n\
                vle%d.v v16, (x7);"%vsew + " \\\n\
                inst v%d, v8, v16%s; "%(n, (", v0.t" if masked else "")) + " \\\n\
                )",file=f)

def generate_macros_muladd(f, lmul):
    lmul = 1 if lmul < 1 else int(lmul)
    vlen = int(os.environ['RVV_ATG_VLEN'])
    vsew = int(os.environ['RVV_ATG_VSEW'])
    masked = True if os.environ['RVV_ATG_MASKED'] == "True" else False
    print("#undef TEST_VV_OP_WITH_INIT \n\
#define TEST_VV_OP_WITH_INIT( testnum, inst, val1, val2, mask_addr ) \\\n\
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
        if n == 8 or n == 16 or n == 24 or n % lmul != 0:
            continue
        print("#define TEST_VV_OP_WITH_INIT_1%d( testnum, inst, val1, val2, mask_addr ) "%n + " \\\n\
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
        if n == 24 or n % lmul != 0:
            continue
        vs1, vs2 = 8, 16
        if n == 8:
            vs1, vs2 = 16, 24
        elif n == 16:
            vs1, vs2 = 8, 24  
        print("#define TEST_VV_OP_WITH_INIT_rd%d( testnum, inst, val1, val2, mask_addr ) "%n + " \\\n\
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

    print("#udnef TEST_VX_OP_RV \n\
#define TEST_VX_OP_RV( testnum, inst, val1, val2, mask_addr ) \\\n\
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

def generate_macros_vvvxvim(f, lmul):
    lmul = 1 if lmul < 1 else int(lmul)
    vlen = int(os.environ['RVV_ATG_VLEN'])
    vsew = int(os.environ['RVV_ATG_VSEW'])
    masked = True if os.environ['RVV_ATG_MASKED'] == "True" else False

    print("#undef TEST_VV_M_OP \n\
#define TEST_VV_M_OP( testnum, inst, val1, val2, mask_addr ) \\\n\
        TEST_CASE_LOOP( testnum, v24, \\\n\
            VSET_VSEW_4AVL \\\n\
            la x7, rd_origin_data; \\\n\
            vle%d.v v24, (x7);"%vsew + " \\\n\
            %s "%("la x7, mask_addr; \\\n    vlm.v v0, (x7); \\\n  "if masked else "")+" \
            la x7, val1; \\\n\
            vle%d.v v8, (x7);"%vsew + " \\\n\
            la x7, val2; \\\n\
            vle%d.v v16, (x7);"%vsew + " \\\n\
            inst v24, v8, v16, v0; \\\n\
        )", file=f)
    print("#undef TEST_VX_M_OP \n\
#define TEST_VX_M_OP( testnum, inst, val1, val2, mask_addr ) \\\n\
        TEST_CASE_LOOP( testnum, v24, \\\n\
            VSET_VSEW_4AVL \\\n\
            la x7, rd_origin_data; \\\n\
            vle%d.v v24, (x7);"%vsew + " \\\n\
            %s "%("la x7, mask_addr; \\\n    vlm.v v0, (x7); \\\n  "if masked else "")+" \
            la x7, val1; \\\n\
            vle%d.v v8, (x7);"%vsew + " \\\n\
            li x1, MASK_VSEW(val2); \\\n\
            inst v24, v8, x1, v0; \\\n\
        )", file=f)
    print("#undef TEST_VI_M_OP \n\
#define TEST_VI_M_OP( testnum, inst, val1, val2, mask_addr ) \\\n\
        TEST_CASE_LOOP( testnum, v24, \\\n\
            VSET_VSEW_4AVL \\\n\
            la x7, rd_origin_data; \\\n\
            vle%d.v v24, (x7);"%vsew + " \\\n\
            %s "%("la x7, mask_addr; \\\n    vlm.v v0, (x7); \\\n  "if masked else "")+" \
            la x7, val1; \\\n\
            vle%d.v v8, (x7);"%vsew + " \\\n\
            inst v24, v8, SEXT_IMM(val2), v0; \\\n\
        )", file=f)
    for n in range(1, 32):
        if n == 8 or n == 16 or n == 24 or n % lmul != 0:
            continue
        print("#define TEST_VV_M_OP_1%d( testnum, inst, val1, val2, mask_addr )"%n + " \\\n\
        TEST_CASE_LOOP( testnum, v24, \\\n\
            VSET_VSEW_4AVL \\\n\
            la x7, rd_origin_data; \\\n\
            vle%d.v v24, (x7);"%vsew + " \\\n\
            %s "%("la x7, mask_addr; \\\n    vlm.v v0, (x7); \\\n  "if masked else "")+" \
            la x7, val1; \\\n\
            vle%d.v v8, (x7);"%vsew + " \\\n\
            la x7, val2; \\\n\
            vle%d.v v%d, (x7);"%(vsew, n) + " \\\n\
            inst v24, v8, v%d, v0; "%n + " \\\n\
        )", file=f)
    for n in range(1, 32):
        if n == 24 or n % lmul != 0:
            continue
        # Beacuse of the widening instruction, rd should valid for the destination’s EMUL
        vs1, vs2 = 8, 16
        if n == 8:
            vs1, vs2 = 16, 24
        elif n == 16:
            vs1, vs2 = 8, 24 
        print("#define TEST_VV_M_OP_rd%d( testnum, inst, val1, val2, mask_addr )"%n + " \\\n\
        TEST_CASE_LOOP( testnum, v%d, "%n + " \\\n\
            VSET_VSEW_4AVL \\\n\
            la x7, rd_origin_data; \\\n\
            vle%d.v v%d, (x7);"%(vsew, n) + " \\\n\
            %s "%("la x7, mask_addr; \\\n    vlm.v v0, (x7); \\\n  "if masked else "")+" \
            la x7, val1; \\\n\
            vle%d.v v%d, (x7);"%(vsew, vs1) + " \\\n\
            la x7, val2; \\\n\
            vle%d.v v%d, (x7);"%(vsew, vs2) + " \\\n\
            inst v%d, v%d, v%d, v0;"%(n, vs1, vs2)+" \\\n\
        ) ",file=f)


def generate_macros_vmadc(f, lmul):
    lmul = 1 if lmul < 1 else int(lmul)
    vlen = int(os.environ['RVV_ATG_VLEN'])
    vsew = int(os.environ['RVV_ATG_VSEW'])
    masked = True if os.environ['RVV_ATG_MASKED'] == "True" else False
    print("#undef TEST_MADC_VV_OP \n\
#define TEST_MADC_VV_OP( testnum, inst, val1, val2, mask_addr ) \\\n\
        TEST_CASE_MASK_4VL( testnum, v24, \\\n\
            VSET_VSEW_4AVL \\\n\
            la x7, rd_origin_data; \\\n\
            vle%d.v v24, (x7);"%vsew + " \\\n\
            %s "%("la x7, mask_addr; \\\n    vlm.v v0, (x7); \\\n  "if masked else "")+" \
            la x7, val1; \\\n\
            vle%d.v v8, (x7);"%vsew + " \\\n\
            la x7, val2; \\\n\
            vle%d.v v16, (x7);"%vsew + " \\\n\
            inst v24, v8, v16; \\\n\
        )", file=f)

    print("#undef TEST_MADC_VX_OP \n\
#define TEST_MADC_VX_OP( testnum, inst, val1, val2, mask_addr ) \\\n\
        TEST_CASE_MASK_4VL( testnum, v24, \\\n\
            VSET_VSEW_4AVL \\\n\
            la x7, rd_origin_data; \\\n\
            vle%d.v v24, (x7);"%vsew + " \\\n\
            %s "%("la x7, mask_addr; \\\n    vlm.v v0, (x7); \\\n  "if masked else "")+" \
            la x7, val1; \\\n\
            vle%d.v v8, (x7);"%vsew + " \\\n\
            li x1, MASK_XLEN(val2); \\\n\
            inst v24, v8, x1; \\\n\
        )", file=f)

    print("#undef TEST_MADC_VI_OP \n\
#define TEST_MADC_VI_OP( testnum, inst, val1, val2, mask_addr ) \\\n\
        TEST_CASE_MASK_4VL( testnum, v24, \\\n\
            VSET_VSEW_4AVL \\\n\
            la x7, rd_origin_data; \\\n\
            vle%d.v v24, (x7);"%vsew + " \\\n\
            %s "%("la x7, mask_addr; \\\n    vlm.v v0, (x7); \\\n  "if masked else "")+" \
            la x7, val1; \\\n\
            vle%d.v v8, (x7);"%vsew + " \\\n\
            inst v24, v8, SEXT_IMM(val2); \\\n\
        )", file=f)

    print("#define TEST_MADC_VVM_OP( testnum, inst, val1, val2, mask_addr ) \\\n\
        TEST_CASE_MASK_4VL( testnum, v24, \\\n\
            VSET_VSEW_4AVL \\\n\
            la x7, rd_origin_data; \\\n\
            vle%d.v v24, (x7);"%vsew + " \\\n\
            %s "%("la x7, mask_addr; \\\n    vlm.v v0, (x7); \\\n  "if masked else "")+" \
            la x7, val1; \\\n\
            vle%d.v v8, (x7);"%vsew + " \\\n\
            la x7, val2; \\\n\
            vle%d.v v16, (x7);"%vsew + " \\\n\
            inst v24, v8, v16, v0; \\\n\
        )", file=f)

    print("#define TEST_MADC_VXM_OP( testnum, inst, val1, val2, mask_addr ) \\\n\
        TEST_CASE_MASK_4VL( testnum, v24, \\\n\
            VSET_VSEW_4AVL \\\n\
            la x7, rd_origin_data; \\\n\
            vle%d.v v24, (x7);"%vsew + " \\\n\
            %s "%("la x7, mask_addr; \\\n    vlm.v v0, (x7); \\\n  "if masked else "")+" \
            la x7, val1; \\\n\
            vle%d.v v8, (x7);"%vsew + " \\\n\
            li x1, MASK_VSEW(val2); \\\n\
            inst v24, v8, x1, v0; \\\n\
        )", file=f)

    print("#define TEST_MADC_VIM_OP( testnum, inst, val1, val2, mask_addr ) \\\n\
        TEST_CASE_MASK_4VL( testnum, v24, \\\n\
            VSET_VSEW_4AVL \\\n\
            la x7, rd_origin_data; \\\n\
            vle%d.v v24, (x7);"%vsew + " \\\n\
            %s "%("la x7, mask_addr; \\\n    vlm.v v0, (x7); \\\n  "if masked else "")+" \
            la x7, val1; \\\n\
            vle%d.v v8, (x7);"%vsew + " \\\n\
            inst v24, v8, SEXT_IMM(val2), v0; \\\n\
        )", file=f)

    for n in range(1, 32):
        if n == 8 or n == 16 or n == 24 or n % lmul != 0:
            continue
        print("#define TEST_MADC_VV_OP_1%d( testnum, inst, val2, val1, mask_addr )"%n + " \\\n\
            TEST_CASE_MASK_4VL( testnum, v24, \\\n\
                VSET_VSEW_4AVL \\\n\
                la x7, rd_origin_data; \\\n\
                vle%d.v v24, (x7);"%vsew + " \\\n\
                %s "%("la x7, mask_addr; \\\n    vlm.v v0, (x7); \\\n  "if masked else "")+" \
                la x7, val2; \\\n\
                vle%d.v v8, (x7);"%vsew + " \\\n\
                la x7, val1; \\\n\
                vle%d.v v%d, (x7);"%(vsew, n) + " \\\n\
                inst v24, v8, v%d; "%n + " \\\n\
            )", file=f)
    for n in range(1, 32):
        if n == 8 or n == 16 or n == 24 or n % (lmul * 2) != 0:
            continue
        # Beacuse of the widening instruction, rd should valid for the destination’s EMUL
        vs2, vs1 = 16, 8
        if n == 8:
            vs2, vs1 = 24, 16
        elif n == 16:
            vs2, vs1 = 24, 8
        print("#define TEST_MADC_VV_OP_rd%d( testnum, inst, val2, val1, mask_addr )"%n + " \\\n\
        TEST_CASE_MASK_4VL( testnum, v%d, "%n + "\\\n\
            VSET_VSEW_4AVL \\\n\
            la x7, rd_origin_data; \\\n\
            vle%d.v v%d, (x7);"%(vsew, n) + " \\\n\
            %s "%("la x7, mask_addr; \\\n    vlm.v v0, (x7); \\\n  "if masked else "")+" \
            la x7, val2; \\\n\
            vle%d.v v%d, (x7);"%(vsew, vs2) + " \\\n\
            la x7, val1; \\\n\
            vle%d.v v%d, (x7);"%(vsew, vs1) + " \\\n\
            inst v%d, v%d, v%d; "%(n, vs2, vs1) + " \\\n\
        ) ", file=f)

def generate_macros_vvmvxmvim(f, lmul, generate_vv = True, generate_vx = True):
    lmul_1 = 1 if lmul < 1 else int(lmul)
    vlen = int(os.environ['RVV_ATG_VLEN'])
    vsew = int(os.environ['RVV_ATG_VSEW'])
    masked = True if os.environ['RVV_ATG_MASKED'] == "True" else False
    if generate_vv:
        print("#undef TEST_VVM_OP \n\
#define TEST_VVM_OP( testnum, inst, val1, val2, mask_addr ) \\\n\
            TEST_CASE_MASK_4VL( testnum, v24, \\\n\
                VSET_VSEW_4AVL \\\n\
                la x7, rd_origin_data; \\\n\
                vle%d.v v24, (x7);"%vsew + " \\\n\
                %s "%("la x7, mask_addr; \\\n    vlm.v v0, (x7); \\\n  "if masked else "")+" \
                la x7, val1; \\\n\
                vle%d.v v8, (x7);"%vsew + " \\\n\
                la x7, val2; \\\n\
                vle%d.v v16, (x7);"%vsew + " \\\n\
                inst v24, v8, v16%s; "%(", v0.t" if masked else "") + " \\\n\
            )", file=f)
        for n in range(1, 32):
            if n == 8 or n == 16 or n == 24 or n % lmul != 0:
                continue
            print("#define TEST_VVM_OP_1%d( testnum, inst, val2, val1, mask_addr )"%n + " \\\n\
                TEST_CASE_MASK_4VL( testnum, v24, \\\n\
                VSET_VSEW_4AVL \\\n\
                la x7, rd_origin_data; \\\n\
                vle%d.v v24, (x7);"%vsew + " \\\n\
                %s "%("la x7, mask_addr; \\\n    vlm.v v0, (x7); \\\n  "if masked else "")+" \
                la x7, val1; \\\n\
                vle%d.v v8, (x7);"%vsew + " \\\n\
                la x7, val2; \\\n\
                vle%d.v v%d, (x7);"%(vsew, n) + " \\\n\
                inst v24, v8, v%d%s; "%(n, (", v0.t" if masked else "")) + " \\\n\
            )", file=f)
        for n in range(1, 32):
            if n == 8 or n == 16 or n == 24 or n % (lmul * 2) != 0:
                continue
            # Beacuse of the widening instruction, rd should valid for the destination’s EMUL
            vs2, vs1 = 16, 8
            if n == 8:
                vs2, vs1 = 24, 16
            elif n == 16:
                vs2, vs1 = 24, 8  
            print("#define TEST_VVM_OP_rd%d( testnum, inst, val2, val1, mask_addr )"%n + " \\\n\
            TEST_CASE_MASK_4VL( testnum, v%d, "%n + "\\\n\
                VSET_VSEW_4AVL \\\n\
                la x7, rd_origin_data; \\\n\
                vle%d.v v%d, (x7);"%(vsew, n) + " \\\n\
                %s "%("la x7, mask_addr; \\\n    vlm.v v0, (x7); \\\n  "if masked else "")+" \
                la x7, val1; \\\n\
                vle%d.v v%d, (x7);"%(vsew, vs1) + " \\\n\
                la x7, val2; \\\n\
                vle%d.v v%d, (x7);"%(vsew, vs2) + " \\\n\
                inst v%d, v%d, v%d%s; "%(n, vs2, vs1, (", v0.t" if masked else "")) + "\\\n\
            ) ", file=f)

    if generate_vx:
        print("#undef TEST_VXM_OP \n\
#define TEST_VXM_OP( testnum, inst, val1, val2, mask_addr ) \\\n\
            TEST_CASE_MASK_4VL( testnum, v24, \\\n\
                VSET_VSEW_4AVL \\\n\
                la x7, rd_origin_data; \\\n\
                vle%d.v v24, (x7);"%vsew + " \\\n\
                %s "%("la x7, mask_addr; \\\n    vlm.v v0, (x7); \\\n  "if masked else "")+" \
                la x7, val1; \\\n\
                vle%d.v v8, (x7);"%vsew + " \\\n\
                li x1, MASK_XLEN(val2); \\\n\
                inst v24, v8, x1%s; "%(", v0.t" if masked else "") + " \\\n\
            )", file=f)
        for n in range(1, 32):
            print("#define TEST_VXM_OP_1%d( testnum, inst, val1, val2, mask_addr ) "%n + " \\\n\
            TEST_CASE_MASK_4VL( testnum, v24,  \\\n\
                VSET_VSEW_4AVL \\\n\
                la x7, rd_origin_data; \\\n\
                vle%d.v v24, (x7);"%vsew + " \\\n\
                %s "%("la x7, mask_addr; \\\n    vlm.v v0, (x7); \\\n  "if masked else "")+" \
                la x7, val1; \\\n\
                vle%d.v v8, (x7);"%vsew + " \\\n\
                li x%d, MASK_XLEN(val2);"%n + " \\\n\
                inst v24, v8, x%d%s; "%(n, (", v0.t" if masked else "")) + " \\\n\
            )", file=f)
        for n in range(1, 32):
            vs = 16 if n == 8 else 8
            print("#define TEST_VXM_OP_rd%d( testnum, inst, val1, val2, mask_addr ) "%n + " \\\n\
            TEST_CASE_MASK_4VL( testnum, v%d, "%n + "\\\n\
                VSET_VSEW_4AVL \\\n\
                la x7, rd_origin_data; \\\n\
                vle%d.v v%d, (x7);"%(vsew, n) + " \\\n\
                %s "%("la x7, mask_addr; \\\n    vlm.v v0, (x7); \\\n  "if masked else "")+" \
                la x7, val1; \\\n\
                vle%d.v v%d, (x7);"%(vsew, vs) + " \\\n\
                li x1, MASK_XLEN(val2); \\\n\
                inst v%d, v%d, x1%s; "%(n, vs, (", v0.t" if masked else "")) + " \\\n\
            ) ", file=f)

    print("#undef TEST_VIM_OP \n\
#define TEST_VIM_OP( testnum, inst, val1, val2, mask_addr ) \
        TEST_CASE_MASK_4VL( testnum, v24, \
            VSET_VSEW_4AVL \\\n\
            la x7, rd_origin_data; \\\n\
            vle%d.v v24, (x7);"%vsew + " \\\n\
            %s "%("la x7, mask_addr; \\\n    vlm.v v0, (x7); \\\n  "if masked else "")+" \
            la x7, val1; \\\n\
            vle%d.v v8, (x7);"%vsew + " \\\n\
            inst v24, v8, SEXT_IMM(val2)%s; "%(", v0.t" if masked else "") + " \\\n\
        )", file=f)

def generate_macros_nvvnvxnvi(f, lmul):
    lmul = 1 if lmul < 1 else int(lmul)
    vlen = int(os.environ['RVV_ATG_VLEN'])
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
        print("#define TEST_N_VV_OP_1%d( testnum, inst, val2, val1, mask_addr )"%n + " \\\n\
            TEST_CASE_LOOP( testnum, v24, \\\n\
                VSET_VSEW_4AVL \\\n\
                la x7, rd_origin_data; \\\n\
                vle%d.v v24, (x7);"%vsew + " \\\n\
                %s "%("la x7, mask_addr; \\\n    vlm.v v0, (x7); \\\n  "if masked else "")+" \
                la x7, val2; \\\n\
                vle%d.v v16, (x7);"%(64 if vsew == 64 else vsew*2) + " \\\n\
                la x7, val1; \\\n\
                vle%d.v v%d, (x7);"%(vsew, n) + " \\\n\
                inst v24, v16, v%d%s; "%(n, (", v0.t" if masked else "")) + " \\\n\
            )", file=f)
    for n in range(1, 32):
        if n % lmul == 0:
            print("#define TEST_N_VV_OP_rd%d( testnum, inst, val2, val1, mask_addr )"%n + " \\\n\
            TEST_CASE_LOOP( testnum, v%d, "%n + " \\\n\
                VSET_VSEW_4AVL \\\n\
                la x7, rd_origin_data; \\\n\
                vle%d.v v%d, (x7);"%(vsew, n) + " \\\n\
                %s "%("la x7, mask_addr; \\\n    vlm.v v0, (x7); \\\n  "if masked else "")+" \
                la x7, val2; \\\n\
                vle%d.v v16, (x7);"%(64 if vsew == 64 else vsew*2) + " \\\n\
                la x7, val1; \\\n\
                vle%d.v v8, (x7);"%vsew + " \\\n\
                inst v%d, v16, v8%s; "%(n, (", v0.t" if masked else "")) + " \\\n\
            ) ", file=f)

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
        print("#define TEST_RED_OP_vs2%d( testnum, inst, val1, val2, mask_addr )"%n + " \\\n\
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
        print("#define TEST_RED_OP_vd%d( testnum, inst, val1, val2, mask_addr )"%n + " \\\n\
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
        vs2, vd = valid_aligned_regs(n)
        print("#define TEST_W_RED_OP_vs1%d( testnum, inst, val1, val2, mask_addr ) "%n + " \\\n\
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
        vs1, vd = valid_aligned_regs(n)
        print("#define TEST_W_RED_OP_vs2%d( testnum, inst, val1, val2, mask_addr ) "%n + " \\\n\
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
        vs1, vs2 = valid_aligned_regs(n)
        print("#define TEST_W_RED_OP_vd%d( testnum, inst, val1, val2, mask_addr ) "%n + " \\\n\
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
    vlen = int(os.environ['RVV_ATG_VLEN'])
    vsew = int(os.environ['RVV_ATG_VSEW'])
    masked = True if os.environ['RVV_ATG_MASKED'] == "True" else False
    lmul = 1 if lmul < 1 else int(lmul)
    print("#undef TEST_EXT_OP \n\
#define TEST_EXT_OP( testnum, inst, val1, mask_addr ) \\\n\
    TEST_CASE_LOOP( testnum, v24,  \\\n\
        VSET_VSEW_4AVL \\\n\
        la x7, rd_origin_data; \\\n\
        vle%d.v v24, (x7);"%vsew + " \\\n\
        %s "%("la x7, mask_addr; \\\n    vlm.v v0, (x7); \\\n  "if masked else "")+" \
        la x7, val1; \\\n\
        vle%d.v v8, (x7);"%vsew + " \\\n\
        inst v24, v8%s;"%(", v0.t" if masked else "") + " \\\n\
    )", file=f)
    for n in range(1, 32):
        if n % lmul != 0 or n == 24:
            continue
        print("#define TEST_EXT_OP_rs1_%d( testnum, inst, val1, mask_addr )"%n + " \\\n\
            TEST_CASE_LOOP( testnum, v24, \\\n\
                VSET_VSEW_4AVL \\\n\
                la x7, rd_origin_data; \\\n\
                vle%d.v v24, (x7);"%vsew + " \\\n\
                %s "%("la x7, mask_addr; \\\n    vlm.v v0, (x7); \\\n  "if masked else "")+" \
                la x7, val1; \\\n\
                vle%d.v v%d, (x7);"%(vsew, n) + " \\\n\
                inst v24, v%d%s; "%(n, ", v0.t" if masked else "") + " \\\n\
            )", file = f)

    for n in range(1, 32):
        if n % lmul != 0 or n == 8:
            continue
        print("#define TEST_EXT_OP_rd_%d( testnum, inst, val1, mask_addr )"%n + " \\\n\
            TEST_CASE_LOOP( testnum, v%d, "%n + " \\\n\
                VSET_VSEW_4AVL \\\n\
                la x7, rd_origin_data; \\\n\
                vle%d.v v%d, (x7);"%(vsew, n) + " \\\n\
                %s "%("la x7, mask_addr; \\\n    vlm.v v0, (x7); \\\n  "if masked else "")+" \
                la x7, val1; \\\n\
                vle%d.v v8, (x7);"%(vsew) + " \\\n\
                inst v%d, v8%s; "%(n, ", v0.t" if masked else "") + " \\\n\
            )", file = f)


def generate_tests_vvvxvi(instr, f, rs1_val, rs2_val, lmul, instr_suffix='vv', generate_vi = True, generate_vx = True, generate_vv = True):
    lmul_1 = 1 if lmul < 1 else int(lmul)
    n = 0
    vlen = int(os.environ['RVV_ATG_VLEN'])
    vsew = int(os.environ['RVV_ATG_VSEW'])
    num_elem = int((vlen * lmul / vsew))
    if num_elem == 0:
        return 0
    loop_num = int(min(len(rs1_val), len(rs2_val)) / num_elem)
    step_bytes = int(vlen * lmul / 8)
    vlmax = num_elem
    mask_bytes = 4 * math.ceil(vlmax / 32) # 4 * num_words
    mask_num = vlmax * 2 + 4
    j = 0
    if generate_vv:
        print("  #-------------------------------------------------------------", file=f)
        print("  # VV Tests", file=f)
        print("  #-------------------------------------------------------------", file=f)
        for i in range(loop_num):
            n += 1
            print("  TEST_VV_OP( "+str(n)+",  %s.%s, "%(instr, instr_suffix) + "rs2_data+%d, rs1_data+%d, mask_data+%d)"%(i*step_bytes, i*step_bytes, j*mask_bytes), file=f)
            j = (j + 1) % mask_num
        for i in range(min(32, loop_num)):     
            k = i%31+1
            if k % lmul != 0 or k == 24:
                continue
            n+=1
            print("  TEST_VV_OP_rd%d( "%k+str(n)+",  %s.%s, "%(instr, instr_suffix)+"rs2_data+%d, rs1_data+%d, mask_data+%d)"%(i*step_bytes, i*step_bytes, j*mask_bytes),file=f)
            j = (j + 1) % mask_num
            
            k = i%30+2
            if k % lmul != 0 or k == 8 or k == 16 or k == 24:
                continue
            n +=1
        
            print("  TEST_VV_OP_1%d( "%k+str(n)+",  %s.%s, "%(instr, instr_suffix)+"rs2_data+%d, rs1_data+%d, mask_data+%d)"%(i*step_bytes, i*step_bytes, j*mask_bytes),file=f)
            j = (j + 1) % mask_num
    vv_test_num = n

    if generate_vx:
        print("  #-------------------------------------------------------------", file=f)
        print("  # VX Tests", file=f)
        print("  #-------------------------------------------------------------", file=f)
        for i in range(loop_num):
            n += 1
            print("  TEST_VX_OP( "+str(n)+",  %s.vx, " %
                instr+" rs2_data+%d, %s, mask_data+%d)"%( i*step_bytes, rs1_val[0], j*mask_bytes), file=f)
            j = (j + 1) % mask_num
    vx_test_num = n - vv_test_num
    if generate_vi:
        print("  #-------------------------------------------------------------", file=f)
        print("  # VI Tests", file=f)
        print("  #-------------------------------------------------------------", file=f)
        for i in range(loop_num):
            n += 1
            print("  TEST_VI_OP( "+str(n)+",  %s.vi, " %
                instr+"rs2_data+%d, 15, mask_data+%d)"%(i*step_bytes, j*mask_bytes), file=f)
            j = (j + 1) % mask_num
    vi_test_num = n - vv_test_num - vx_test_num

    return (vv_test_num, vx_test_num, vi_test_num)

def generate_tests_vw(f, rs1_val, rs2_val, instr, lmul, instr_suffix='vv', generate_vx = True, generate_wvwx = True):
    n = 0
    vlen = int(os.environ['RVV_ATG_VLEN'])
    vsew = int(os.environ['RVV_ATG_VSEW'])
    lmul = float(os.environ['RVV_ATG_LMUL'])
    lmul_double = lmul * 2
    lmul_1 = 1 if lmul < 1 else int (lmul)
    lmul_double_1 = 1 if lmul_double < 1 else int (lmul_double)
    num_elem = int((vlen * lmul / vsew))
    if num_elem == 0:
        return 0
    loop_num = int(min(len(rs1_val), len(rs2_val)) / num_elem)
    step_bytes = int(vlen * lmul / 8)
    step_bytes_double = step_bytes * 2
    vlmax = num_elem
    mask_bytes = 4 * math.ceil(vlmax / 32) # 4 * num_words
    mask_num = vlmax * 2 + 4
    j = 0
    print("  #-------------------------------------------------------------", file=f)
    print("  # VV Tests", file=f)
    print("  #-------------------------------------------------------------", file=f)

    for i in range(loop_num):
        n += 1
        print("  TEST_W_VV_OP( "+str(n)+",  %s.%s, " %
              (instr, instr_suffix)+"rs2_data+%d, rs1_data+%d, mask_data+%d)"%(i*step_bytes, i*step_bytes, j*mask_bytes), file=f)
        j = (j + 1) % mask_num
    for i in range(min(32, loop_num)):
        k = i%31+1
        if k%(2*lmul)==0 and k != 8 and k != 16 and k != 24 and not is_overlap(k, lmul_double_1, 8, lmul_1) and not is_overlap(k, lmul_double_1, 16, lmul_1) and k != 12 and k != 20 and k != 24:
            n+=1
            print("  TEST_W_VV_OP_rd%d( "%k+str(n)+",  %s.%s, "%(instr, instr_suffix)+"rs2_data+%d, rs1_data+%d, mask_data+%d)"%(i*step_bytes, i*step_bytes, j*mask_bytes),file=f)
            j = (j + 1) % mask_num
        k = i%30+2
        if k % lmul == 0 and k != 16 and k != 8 and k != 24 and not is_overlap(24, lmul_double_1, k, lmul_1) and k != 12 and k != 20 and k != 24:
            n +=1
            print("  TEST_W_VV_OP_1%d( "%k+str(n)+",  %s.%s, "%(instr, instr_suffix)+"rs2_data+%d, rs1_data+%d, mask_data+%d)"%(i*step_bytes, i*step_bytes, j*mask_bytes),file=f)
            j = (j + 1) % mask_num

    vv_test_num = n
    if generate_vx:
        print("  #-------------------------------------------------------------", file=f)
        print("  # VX Tests", file=f)
        print("  #-------------------------------------------------------------", file=f)
        
        for i in range(loop_num):
            n += 1
            print("  TEST_W_VX_OP( "+str(n)+",  %s.vx, " %
                instr+"rs2_data+%d, %s, mask_data+%d)"%(i*step_bytes, rs1_val[i], j*mask_bytes), file=f)
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
            print("  TEST_W_WV_OP( "+str(n)+",  %s.wv, " %
                instr+"rs2_data_widen+%d, rs1_data+%d, mask_data+%d)"%(i*step_bytes_double, i*step_bytes, j*mask_bytes), file=f)
            j = (j + 1) % mask_num
        print("  #-------------------------------------------------------------", file=f)
        print("  # WX Tests", file=f)
        print("  #-------------------------------------------------------------", file=f)
        
        for i in range(loop_num):
            n += 1
            print("  TEST_W_WX_OP( "+str(n)+",  %s.wx, " %
                instr+"rs2_data_widen+%d, %s, mask_data+%d)"%(i*step_bytes_double, rs1_val[i], j*mask_bytes), file=f)
            j = (j + 1) % mask_num
        wv_test_num = wx_test_num = loop_num
    
    return (vv_test_num, vx_test_num, wv_test_num, wx_test_num)
              
def generate_tests_vwmacc(f, rs1_val, rs2_val, instr, lmul, generate_vv = True):
    lmul_1 = 1 if lmul < 1 else int(lmul)
    lmul_double_1 = 1 if (lmul * 2) < 1 else int(lmul * 2)
    n = 0
    vlen = int(os.environ['RVV_ATG_VLEN'])
    vsew = int(os.environ['RVV_ATG_VSEW'])
    num_elem = int((vlen * lmul / vsew))
    if num_elem == 0:
        return 0
    loop_num = int(min(len(rs1_val), len(rs2_val)) / num_elem)
    step_bytes = int(vlen * lmul / 8)
    step_bytes_double = step_bytes * 2
    vlmax = num_elem
    mask_bytes = 4 * math.ceil(vlmax / 32) # 4 * num_words
    mask_num = vlmax * 2 + 4
    j = 0
    
    if generate_vv:
        print("  #-------------------------------------------------------------", file=f)
        print("  # VV Tests", file=f)
        print("  #-------------------------------------------------------------", file=f)

        for i in range(loop_num):
            n += 1
            print("  TEST_W_VV_OP_WITH_INIT( "+str(n)+",  %s.%s, " %
                (instr, 'vv')+"rs2_data+%d, rs1_data+%d, mask_data+%d)"%(i*step_bytes, i*step_bytes, j*mask_bytes), file=f)
            j = (j + 1) % mask_num
        for i in range(min(32, loop_num)): 
            k = i%31+1
            if k%(2*lmul)==0 and k != 8 and k != 16 and k != 24 and not is_overlap(k, lmul_double_1, 8, lmul_1)and not is_overlap(k, lmul_double_1, 16, lmul_1) and k != 12 and k != 20 and k != 24:
                n+=1
                print("  TEST_W_VV_OP_WITH_INIT_rd%d( "%k+str(n)+",  %s.%s, "%(instr, 'vv')+"rs2_data+%d, rs1_data+%d, mask_data+%d)"%(i*step_bytes, i*step_bytes, j*mask_bytes),file=f)
                j = (j + 1) % mask_num
            
            k = i%30+2
            if k % lmul == 0 and k != 8 and k != 16 and k != 24 and not is_overlap(24, lmul_double_1, k, lmul_1) and k != 12 and k != 20 and k != 24:
                n +=1
                print("  TEST_W_VV_OP_WITH_INIT_1%d( "%k+str(n)+",  %s.%s, "%(instr, 'vv')+" rs2_data+%d, rs1_data+%d, mask_data+%d)"%(i*step_bytes, i*step_bytes, j*mask_bytes),file=f)
                j = (j + 1) % mask_num

    vv_test_num = n
    
    print("  #-------------------------------------------------------------", file=f)
    print("  # VX Tests", file=f)
    print("  #-------------------------------------------------------------", file=f)
    
    for i in range(loop_num):
        n += 1
        print("  TEST_W_VX_OP_RV( "+str(n)+",  %s.vx, " %
            instr+" %s, rs2_data+%d, mask_data+%d)"%( rs1_val[i], i*step_bytes, j*mask_bytes), file=f)
        j = (j + 1) % mask_num
    vx_test_num = n - vv_test_num
    return (vv_test_num, vx_test_num, 0)


def generate_tests_muladd(instr, f, rs1_val, rs2_val, lmul):
    lmul_1 = 1 if lmul < 1 else int(lmul)
    n = 0
    vlen = int(os.environ['RVV_ATG_VLEN'])
    vsew = int(os.environ['RVV_ATG_VSEW'])
    num_elem = int((vlen * lmul / vsew))
    if num_elem == 0:
        return 0
    loop_num = int(min(len(rs1_val), len(rs2_val)) / num_elem)
    step_bytes = int(vlen * lmul / 8)
    vlmax = num_elem
    mask_bytes = 4 * math.ceil(vlmax / 32) # 4 * num_words
    mask_num = vlmax * 2 + 4
    j = 0
    print("  #-------------------------------------------------------------", file=f)
    print("  # VV Tests", file=f)
    print("  #-------------------------------------------------------------", file=f)

    for i in range(loop_num):
        n += 1
        print("  TEST_VV_OP_WITH_INIT( "+str(n)+",  %s.vv, " %
              instr + " rs2_data+%d, rs1_data+%d, mask_data+%d)"%( i*step_bytes, i*step_bytes, j*mask_bytes), file=f)
        j = (j + 1) % mask_num
    for i in range(min(32, loop_num)):     
        k = i%31+1
        if k == 24 or k % lmul != 0 or k == 12 or k == 20 or k == 24:
            continue
        n+=1
        print("  TEST_VV_OP_WITH_INIT_rd%d( "%k+str(n)+",  %s.vv, "%instr+ "rs2_data+%d, rs1_data+%d, mask_data+%d)"%( i*step_bytes, i*step_bytes, j*mask_bytes),file=f)
        j = (j + 1) % mask_num
        
        k = i%30+2
        if k == 8 or k == 16 or k == 24 or k % lmul != 0 or k == 12 or k == 20 or k == 24:
            continue
        n +=1
        print("  TEST_VV_OP_WITH_INIT_1%d( "%k+str(n)+",  %s.vv, "%instr + " rs2_data+%d, rs1_data+%d, mask_data+%d)"%(i*step_bytes, i*step_bytes, j*mask_bytes),file=f)
        j = (j + 1) % mask_num


    vv_test_num = n
    
    print("  #-------------------------------------------------------------", file=f)
    print("  # VX Tests", file=f)
    print("  #-------------------------------------------------------------", file=f)
    
    for i in range(loop_num):
        n += 1
        print("  TEST_VX_OP_RV( "+str(n)+",  %s.vx, " %
              instr + " %s, rs1_data+%d, mask_data+%d)"%( rs1_val[0], i*step_bytes, j*mask_bytes), file=f)
        j = (j + 1) % mask_num
    vx_test_num = n - vv_test_num
    
    return (vv_test_num, vx_test_num, 0)
  

def generate_tests_vmadc(instr, f, rs1_val, rs2_val, lmul, generate_vi = True):
    lmul = 1 if lmul < 1 else int(lmul)
    n = 0
    vlen = int(os.environ['RVV_ATG_VLEN'])
    vsew = int(os.environ['RVV_ATG_VSEW'])
    num_elem = int((vlen * lmul / vsew))
    if num_elem == 0:
        return 0
    loop_num = int(min(len(rs1_val), len(rs2_val)) / num_elem)
    step_bytes = int(vlen * lmul / 8)
    vlmax = num_elem
    mask_bytes = 4 * math.ceil(vlmax / 32) # 4 * num_words
    mask_num = vlmax * 2 + 4
    j = 0
    print("  #-------------------------------------------------------------", file=f)
    print("  # VV Tests", file=f)
    print("  #-------------------------------------------------------------", file=f)

    for i in range(loop_num):
        n += 1
        print("  TEST_MADC_VV_OP( "+str(n)+",  %s.vv, " %
              instr+" rs2_data+%d, rs1_data+%d, mask_data+%d)"%(i*step_bytes, i*step_bytes, j*mask_bytes), file=f)
        j = (j + 1) % mask_num
    for i in range(min(32, loop_num)):     
        k = i%31+1
        if k == 0 or k == 8 or k == 16 or k == 24 or k % (lmul * 2) != 0 or k == 12 or k == 20 or k == 24:
            continue
        n+=1
        print("  TEST_MADC_VV_OP_rd%d( "%k+str(n)+",  %s.vv, "%instr+" rs2_data+%d, rs1_data+%d, mask_data+%d)"%(i*step_bytes, i*step_bytes, j*mask_bytes),file=f)
        j = (j + 1) % mask_num
        
        k = i%30+2
        if k == 0 or k == 8 or k == 16 or k == 24 or k % lmul != 0 or k == 12 or k == 20 or k == 24:
            continue
        n +=1
    #     print("  TEST_VVM_OP_1%d( "%k+str(n)+",  %s.vv, "%instr+rs2_val[i]+", "+rs1_val[i]+" );",file=f)
        print("  TEST_MADC_VV_OP_1%d( "%k+str(n)+",  %s.vv, "%instr+" rs2_data+%d, rs1_data+%d, mask_data+%d)"%(i*step_bytes, i*step_bytes, j*mask_bytes),file=f)
        j = (j + 1) % mask_num
    
    print("  #-------------------------------------------------------------", file=f)
    print("  # VVM Tests", file=f)
    print("  #-------------------------------------------------------------", file=f)

    for i in range(loop_num):
        n += 1
        print("  TEST_MADC_VVM_OP( "+str(n)+",  %s.vvm, " %
              instr+" rs2_data+%d, rs1_data+%d, mask_data+%d)"%(i*step_bytes, i*step_bytes, j*mask_bytes), file=f)
        j = (j + 1) % mask_num
        
    vv_test_num = n
    
    print("  #-------------------------------------------------------------", file=f)
    print("  # VX Tests", file=f)
    print("  #-------------------------------------------------------------", file=f)
    
    for i in range(loop_num):
        n += 1
        print("  TEST_MADC_VX_OP( "+str(n)+",  %s.vx, " %
               instr+" rs2_data+%d, %s, mask_data+%d)"%(i*step_bytes, rs1_val[i % len(rs1_val)], j*mask_bytes), file=f)
        j = (j + 1) % mask_num
        
    print("  #-------------------------------------------------------------", file=f)
    print("  # VXM Tests", file=f)
    print("  #-------------------------------------------------------------", file=f)

    for i in range(loop_num):
        n +=1
        print("  TEST_MADC_VXM_OP( "+str(n)+",  %s.vxm, " %
              instr+" rs2_data+%d, %s, mask_data+%d)"%(i*step_bytes, rs1_val[i % len(rs1_val)], j*mask_bytes), file=f)
        j = (j + 1) % mask_num

    vx_test_num = n - vv_test_num

    if generate_vi:
        print("  #-------------------------------------------------------------", file=f)
        print("  # VI Tests", file=f)
        print("  #-------------------------------------------------------------", file=f)

        for i in range(loop_num):
            n +=1
            print("  TEST_MADC_VI_OP( "+str(n)+",  %s.vi, " %
                instr+" rs2_data+%d, 14, mask_data+%d)"%(i*step_bytes, j*mask_bytes), file=f)
            j = (j + 1) % mask_num
            
        print("  #-------------------------------------------------------------", file=f)
        print("  # VIM Tests", file=f)
        print("  #-------------------------------------------------------------", file=f)

        for i in range(loop_num):  
            n +=1
            print("  TEST_MADC_VIM_OP( "+str(n)+",  %s.vim, " %
                instr+" rs2_data+%d, 14, mask_data+%d)"%(i*step_bytes, j*mask_bytes), file=f)     
            j = (j + 1) % mask_num

    vi_test_num = n - vv_test_num - vx_test_num

    return (vv_test_num, vx_test_num, vi_test_num)

def generate_tests_vvvxvim(instr, f, rs1_val, rs2_val, lmul, generate_vi=True):
    lmul_1 = 1 if lmul < 1 else int(lmul)
    n = 0
    vlen = int(os.environ['RVV_ATG_VLEN'])
    vsew = int(os.environ['RVV_ATG_VSEW'])
    num_elem = int((vlen * lmul / vsew))
    if num_elem == 0:
        return 0
    loop_num = int(min(len(rs1_val), len(rs2_val)) / num_elem)
    step_bytes = int(vlen * lmul / 8)
    vlmax = num_elem
    mask_bytes = 4 * math.ceil(vlmax / 32) # 4 * num_words
    mask_num = vlmax * 2 + 4
    j = 0
    print("  #-------------------------------------------------------------", file=f)
    print("  # VV Tests", file=f)
    print("  #-------------------------------------------------------------", file=f)

    for i in range(loop_num):
        n += 1
        print("  TEST_VV_M_OP( "+str(n)+",  %s.vvm, " %
              instr+"rs2_data+%d, rs1_data+%d, mask_data+%d)"%( i*step_bytes, i*step_bytes, j*mask_bytes), file=f)
        j = (j + 1) % mask_num
    for i in range(min(32, loop_num)):     
        k = i%31+1
        if k == 24 or k % lmul != 0 or k == 12 or k == 20 or k == 24:
            continue
        n+=1
        print("  TEST_VV_M_OP_rd%d( "%k+str(n)+",  %s.vvm, "%instr+"rs2_data+%d, rs1_data+%d, mask_data+%d)"%(i*step_bytes, i*step_bytes, j*mask_bytes),file=f)
        j = (j + 1) % mask_num
        
        k = i%30+2
        if k == 8 or k == 16 or k == 24 or k % lmul != 0 or k == 12 or k == 20 or k == 24:
            continue
        n +=1
        print("  TEST_VV_M_OP_1%d( "%k+str(n)+",  %s.vvm, "%instr+"rs2_data+%d, rs1_data+%d, mask_data+%d)"%(i*step_bytes, i*step_bytes, j*mask_bytes),file=f)
        j = (j + 1) % mask_num
    
    vv_test_num = n
    
    print("  #-------------------------------------------------------------", file=f)
    print("  # VX Tests", file=f)
    print("  #-------------------------------------------------------------", file=f)
    
    for i in range(loop_num):
        n += 1
        print("  TEST_VX_M_OP( "+str(n)+",  %s.vxm, " %
              instr+" rs2_data+%d, %s, mask_data+%d)"%( i*step_bytes, rs1_val[i % len(rs1_val)], j*mask_bytes), file=f)
        j = (j + 1) % mask_num
    vx_test_num = n - vv_test_num
    
    if generate_vi:
        print("  #-------------------------------------------------------------", file=f)
        print("  # VI Tests", file=f)
        print("  #-------------------------------------------------------------", file=f)

        for i in range(loop_num):
            n += 1
            print("  TEST_VI_M_OP( "+str(n)+",  %s.vim, " %
                instr+"rs2_data+%d, 14, mask_data+%d)"%(i*step_bytes, j*mask_bytes), file=f)
            j = (j + 1) % mask_num
    vi_test_num = n - vv_test_num - vx_test_num

    return (vv_test_num, vx_test_num, vi_test_num)

def generate_tests_vvmvxmvim(instr, f, rs1_val, rs2_val, lmul, generate_vv=True, generate_vx=True, generate_vi=True):
    lmul_1 = 1 if lmul < 1 else int(lmul)
    n = 0
    vlen = int(os.environ['RVV_ATG_VLEN'])
    vsew = int(os.environ['RVV_ATG_VSEW'])
    num_elem = int((vlen * lmul / vsew))
    if num_elem == 0:
        return 0
    loop_num = int(min(len(rs1_val), len(rs2_val)) / num_elem)
    step_bytes = int(vlen * lmul / 8)
    vlmax = num_elem
    mask_bytes = 4 * math.ceil(vlmax / 32) # 4 * num_words
    mask_num = vlmax * 2 + 4
    j = 0
    if generate_vv:
        print("  #-------------------------------------------------------------", file=f)
        print("  # VV Tests", file=f)
        print("  #-------------------------------------------------------------", file=f)

        for i in range(loop_num):
            n += 1
            print("  TEST_VVM_OP( "+str(n)+",  %s.vv, " %
                instr+" rs2_data+%d, rs1_data+%d, mask_data+%d)"%(i*step_bytes, i*step_bytes, j*mask_bytes), file=f)
            j = (j + 1) % mask_num
        for i in range(min(32, loop_num)): 
            k = i%31+1
            if k == 0 or k == 8 or k == 16 or k == 24 or k % (lmul * 2) != 0 or k == 12 or k == 20 or k == 24:
                continue
            n+=1
            print("  TEST_VVM_OP_rd%d( "%k+str(n)+",  %s.vv, "%instr+" rs2_data+%d, rs1_data+%d, mask_data+%d)"%(i*step_bytes, i*step_bytes, j*mask_bytes),file=f)
            j = (j + 1) % mask_num
            
            k = i%30+2
            if k == 0 or k == 8 or k == 16 or k == 24 or k % lmul != 0 or k == 12 or k == 20 or k == 24:
                continue
            n +=1
            print("  TEST_VVM_OP_1%d( "%k+str(n)+",  %s.vv, "%instr+" rs2_data+%d, rs1_data+%d, mask_data+%d)"%(i*step_bytes, i*step_bytes, j*mask_bytes),file=f)
            j = (j + 1) % mask_num
    vv_test_num = n

    if generate_vx:
        print("  #-------------------------------------------------------------", file=f)
        print("  # VX Tests", file=f)
        print("  #-------------------------------------------------------------", file=f)
        
        for i in range(loop_num):
            n += 1
            print("  TEST_VXM_OP( "+str(n)+",  %s.vx, " %
                instr+" rs2_data+%d, %s, mask_data+%d)"%(i*step_bytes, rs1_val[i % len(rs1_val)], j*mask_bytes), file=f)
            j = (j + 1) % mask_num
        for i in range(min(32, loop_num)):
            k = i%31+1
            if k == 0 or k == 24 or k % (lmul * 2) != 0 or k == 12 or k == 20 or k == 24:
                continue
            n+=1
            print("  TEST_VXM_OP_rd%d( "%k+str(n)+",  %s.vx, "%instr+" rs2_data+%d, %s, mask_data+%d)"%(i*step_bytes, rs1_val[i % len(rs1_val)], j*mask_bytes),file=f)
            j = (j + 1) % mask_num
            
            k = i%30+2
            if k == 0 or k == 8 or k == 16 or k == 24 or k % (lmul * 2) != 0 or k == 12 or k == 20 or k == 24:
                continue
            n +=1
            print("  TEST_VXM_OP_1%d( "%k+str(n)+",  %s.vx, "%instr+" rs2_data+%d, %s, mask_data+%d)"%(i*step_bytes, rs1_val[i % len(rs1_val)], j*mask_bytes),file=f)
            j = (j + 1) % mask_num

    vx_test_num = n - vv_test_num
    if generate_vi:
        print("  #-------------------------------------------------------------", file=f)
        print("  # VI Tests", file=f)
        print("  #-------------------------------------------------------------", file=f)
        
        for i in range(loop_num):
            n += 1
            print("  TEST_VIM_OP( "+str(n)+",  %s.vi, " %
                instr+" rs2_data+%d, 4, mask_data+%d)"%(i*step_bytes, j*mask_bytes), file=f)
            j = (j + 1) % mask_num
    
    vi_test_num = n - vv_test_num - vx_test_num
    return (vv_test_num, vx_test_num, vi_test_num)


def generate_tests_nvvnvxnvi(instr, f, rs1_val, rs2_val, lmul):
    lmul_1 = 1 if lmul < 1 else int(lmul)
    n = 0
    vlen = int(os.environ['RVV_ATG_VLEN'])
    vsew = int(os.environ['RVV_ATG_VSEW'])
    num_elem = int((vlen * lmul / vsew))
    if num_elem == 0:
        return 0
    loop_num = int(min(len(rs1_val), len(rs2_val)) / num_elem)
    step_bytes = int(vlen * lmul / 8)
    vlmax = num_elem
    mask_bytes = 4 * math.ceil(vlmax / 32) # 4 * num_words
    mask_num = vlmax * 2 + 4
    j = 0
    print("  #-------------------------------------------------------------", file=f)
    print("  # VV Tests", file=f)
    print("  #-------------------------------------------------------------", file=f)

    for i in range(loop_num):
        n += 1
        print("  TEST_N_VV_OP( "+str(n)+",  %s.wv, " %
              instr + "rs2_data+%d, rs1_data+%d, mask_data+%d)"%(i*step_bytes*2, i*step_bytes, j*mask_bytes), file=f)
        j = (j + 1) % mask_num
    for i in range(min(32, loop_num)):     
        k = i%31+1
        if k%lmul == 0 and k != 8 and k != 16 and k != 24 and not is_overlap(k, lmul, 16, lmul*2) and k != 12 and k != 20 and k != 24:
            n+=1
            print("  TEST_N_VV_OP_rd%d( "%k+str(n)+",  %s.wv, "%instr + "rs2_data+%d, rs1_data+%d, mask_data+%d)"%( i*step_bytes*2, i*step_bytes, j*mask_bytes),file=f)
            j = (j + 1) % mask_num
        
        k = i%30+2
        if k%lmul == 0 and k != 8 and k != 16 and k != 24 and not is_overlap(k, lmul, 16, lmul*2) and k != 12 and k != 20 and k != 24:
            n +=1
            print("  TEST_N_VV_OP_1%d( "%k+str(n)+",  %s.wv, "%instr + "rs2_data+%d, rs1_data+%d, mask_data+%d)"%( i*step_bytes*2, i*step_bytes, j*mask_bytes),file=f)
            j = (j + 1) % mask_num


    vv_test_num = n
    print("  #-------------------------------------------------------------", file=f)
    print("  # VX Tests", file=f)
    print("  #-------------------------------------------------------------", file=f)
    
    for i in range(loop_num):
        n += 1
        print("  TEST_N_VX_OP( "+str(n)+",  %s.wx, " %
              instr+"rs2_data+%d, %s, mask_data+%d)"%( i*step_bytes*2, rs1_val[i % len(rs1_val)], j*mask_bytes), file=f)
        j = (j + 1) % mask_num
    
    vx_test_num = n - vv_test_num
    
    print("  #-------------------------------------------------------------", file=f)
    print("  # VI Tests", file=f)
    print("  #-------------------------------------------------------------", file=f)

    for i in range(loop_num):
        n += 1
        print("  TEST_N_VI_OP( "+str(n)+",  %s.wi, " %
              instr+" rs2_data+%d, 4, mask_data+%d)"%( i*step_bytes*2, j*mask_bytes), file=f)
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
        print("  TEST_RED_OP( "+str(n)+",  %s.%s, " %
            (instr, instr_suffix)+"rs1_data+%d, rs2_data+%d, mask_data+%d)"%(i*step_bytes, i*step_bytes, j*mask_bytes), file=f)
        j = (j + 1) % mask_num
    
    for i in range(min(32, loop_num)):     
        k = i % 31 + 1
        if k % lmul != 0:
            continue
        n += 1
        print("  TEST_RED_OP_vd%d( "%k+str(n)+",  %s.%s, "%(instr, instr_suffix)+"rs1_data+%d, rs2_data+%d, mask_data+%d)"%(i*step_bytes, i*step_bytes, j*mask_bytes),file=f)
        j = (j + 1) % mask_num
        
        n += 1
        print("  TEST_RED_OP_vs2%d( "%k+str(n)+",  %s.%s, "%(instr, instr_suffix)+"rs1_data+%d, rs2_data+%d, mask_data+%d)"%(i*step_bytes, i*step_bytes, j*mask_bytes),file=f)
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
        print("  TEST_W_RED_OP( "+str(n)+",  %s.%s, " %
              (instr, instr_suffix)+"rs1_data+%d, rs2_data_widen+%d, mask_data+%d)"%(i*step_bytes, i*step_bytes_double, j*mask_bytes), file=f)
        j = (j + 1) % mask_num
    
    print("  #-------------------------------------------------------------", file=f)
    print("  # %s Tests (different register)"%instr, file=f)
    print("  #-------------------------------------------------------------", file=f)
    
    for i in range(min(32, loop_num)):
        k = i % 31 + 1
        
        if k % lmul != 0:
            continue
        n += 1
        print("  TEST_W_RED_OP_vs1%d( "%k+str(n)+",  %s.%s, "%(instr, instr_suffix)+"rs1_data+%d, rs2_data_widen+%d, mask_data+%d)"%(i*step_bytes, i*step_bytes_double, j*mask_bytes),file=f)
        j = (j + 1) % mask_num
        
        if k % (2*lmul) != 0:
            continue
        n += 1
        print("  TEST_W_RED_OP_vs2%d( "%k+str(n)+",  %s.%s, "%(instr, instr_suffix)+"rs1_data+%d, rs2_data_widen+%d, mask_data+%d)"%(i*step_bytes, i*step_bytes_double, j*mask_bytes),file=f)
        j = (j + 1) % mask_num
        n += 1
        print("  TEST_W_RED_OP_vd%d( "%k+str(n)+",  %s.%s, "%(instr, instr_suffix)+"rs1_data+%d, rs2_data_widen+%d, mask_data+%d)"%(i*step_bytes, i*step_bytes_double, j*mask_bytes),file=f)
        j = (j + 1) % mask_num
          
    return n

def generate_tests_ext_op(instr, f, rs1_val, rs2_val, lmul):
    vlen = int(os.environ['RVV_ATG_VLEN'])
    vsew = int(os.environ['RVV_ATG_VSEW'])
    lmul_1 = 1 if lmul < 1 else int(lmul)
    n = 0
    
    num_elem = int((vlen * lmul / vsew))
    if num_elem == 0:
        return 0
    loop_num = int(min(len(rs1_val), len(rs2_val)) / num_elem)
    step_bytes = int(vlen * lmul / 8)
    
    vlmax = num_elem
    mask_bytes = 4 * math.ceil(vlmax / 32) # 4 * num_words
    mask_num = vlmax * 2 + 4
    j = 0
    
    print("  #-------------------------------------------------------------",file=f)
    print("  # %s Tests"%instr,file=f)
    print("  #-------------------------------------------------------------",file=f)
    
    for i in range(loop_num):
        if int(vsew / 2) >= 8 and lmul / 2 >= 0.125: 
            n += 1
            print("TEST_EXT_OP( %d,  %s.vf2, "%(n, instr) + "rs1_data+%d, mask_data+%d);"%( i*step_bytes, j*mask_bytes), file=f)
            j = (j + 1) % mask_num
    count1 = n
    for i in range(loop_num):
        if int(vsew / 4) >= 8 and lmul / 4 >= 0.125:
            n += 1
            print("TEST_EXT_OP( %d,  %s.vf4, "%(n, instr) + "rs1_data+%d, mask_data+%d);"%(i*step_bytes, j*mask_bytes), file=f)
            j = (j + 1) % mask_num
    count2 = n
    for i in range(loop_num):
        if int(vsew / 8) >= 8 and lmul / 8 >= 0.125:
            n += 1
            print("TEST_EXT_OP( %d,  %s.vf8, "%(n, instr) + "rs1_data+%d, mask_data+%d);"%(i*step_bytes, j*mask_bytes), file=f)
            j = (j + 1) % mask_num
    
    print("  #-------------------------------------------------------------",file=f)
    print("  # %s Tests (different register)"%instr,file=f)
    print("  #-------------------------------------------------------------",file=f)
    

    for i in range(min(32, loop_num)):
        k = i % 31 + 1  
        if k % lmul != 0 or k == 8 or k == 12 or k == 20 or k == 24:
            continue
        if int(vsew / 2) >= 8 and lmul / 2 >= 0.125: 
            n += 1
            print("TEST_EXT_OP_rd_%d( %d,  %s.vf2, "%(k, n, instr) + "rs1_data+%d, mask_data+%d);"%( i*step_bytes, j*mask_bytes), file=f)
            j = (j + 1) % mask_num
    for i in range(min(32, loop_num)):
        k = i % 31 + 1  
        if k % lmul != 0 or k == 8 or k == 12 or k == 20 or k == 24:
            continue
        if int(vsew / 4) >= 8 and lmul / 4 >= 0.125:
            n += 1
            print("TEST_EXT_OP_rd_%d( %d,  %s.vf4, "%(k, n, instr) + "rs1_data+%d, mask_data+%d);"%( i*step_bytes, j*mask_bytes), file=f)
            j = (j + 1) % mask_num
    for i in range(min(32, loop_num)):
        k = i % 31 + 1  
        if k % lmul != 0 or k == 8 or k == 12 or k == 20 or k == 24:
            continue
        if int(vsew / 8) >= 8 and lmul / 8 >= 0.125:
            n += 1
            print("TEST_EXT_OP_rd_%d( %d,  %s.vf8, "%(k, n, instr) + "rs1_data+%d, mask_data+%d);"%( i*step_bytes, j*mask_bytes), file=f)
            j = (j + 1) % mask_num


    for i in range(min(32, loop_num)):
        k = i % 31 + 1
        if k % lmul != 0 or k == 24 or k == 12 or k == 20 or k == 24:
            continue
        if int(vsew / 2) >= 8 and lmul / 2 >= 0.125: 
            n += 1
            print("TEST_EXT_OP_rs1_%d( %d,  %s.vf2, "%(k, n, instr) + "rs1_data+%d, mask_data+%d);"%(i*step_bytes, j*mask_bytes), file=f)
            j = (j + 1) % mask_num

    for i in range(min(32, loop_num)):
        k = i % 31 + 1
        if k % lmul != 0 or k == 24 or k == 12 or k == 20 or k == 24:
            continue
        if int(vsew / 4) >= 8 and lmul / 4 >= 0.125:
            n += 1
            print("TEST_EXT_OP_rs1_%d( %d,  %s.vf4, "%(k, n, instr) + "rs1_data+%d, mask_data+%d);"%(i*step_bytes, j*mask_bytes), file=f)
            j = (j + 1) % mask_num

    for i in range(min(32, loop_num)):
        k = i % 31 + 1
        if k % lmul != 0 or k == 24 or k == 12 or k == 20 or k == 24:
            continue
        if int(vsew / 8) >= 8 and lmul / 8 >= 0.125:
            n += 1
            print("TEST_EXT_OP_rs1_%d( %d,  %s.vf8, "%(k, n, instr) + "rs1_data+%d, mask_data+%d);"%(i*step_bytes, j*mask_bytes), file=f)
            j = (j + 1) % mask_num
    
    return (n, 0, 0)
