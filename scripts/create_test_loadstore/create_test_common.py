import re




def generate_vlseg_macro(f, lmul):
    print("\
    #define TEST_VLSEG1_OP( testnum, inst, eew, base ) \\\n\
        TEST_CASE_LOOP( testnum, v8,   \\\n\
            la  x1, base; \\\n\
            inst v8, (x1); \\\n\
        ) \n\
    #define TEST_VLSEG2_OP( testnum, inst, eew, base ) \\\n\
        TEST_CASE_LOOP( testnum, v8,   \\\n\
            la  x1, base; \\\n\
            inst v8, (x1); \\\n\
        ) \\\n\
        TEST_CASE_LOOP_CONTINUE( testnum, v%d) "%(8+lmul) + " \n\
    #define TEST_VLSEG3_OP( testnum, inst, eew, base ) \\\n\
        TEST_CASE_LOOP( testnum, v8,   \\\n\
            la  x1, base; \\\n\
            inst v8, (x1); \\\n\
        ) \\\n\
        TEST_CASE_LOOP_CONTINUE( testnum, v%d)"%(8+lmul) + "  \\\n\
        TEST_CASE_LOOP_CONTINUE( testnum, v%d)"%(8+lmul*2) + " \n", file=f)
    
    if 8+lmul*4 < 32:
        print("#define TEST_VLSEG4_OP( testnum, inst, eew, base ) \\\n\
        TEST_CASE_LOOP( testnum, v8,   \\\n\
            la  x1, base; \\\n\
            inst v8, (x1); \\\n\
        ) \\\n\
        TEST_CASE_LOOP_CONTINUE( testnum, v%d)"%(8+lmul*1) + "  \\\n\
        TEST_CASE_LOOP_CONTINUE( testnum, v%d)"%(8+lmul*2) + "  \\\n\
        TEST_CASE_LOOP_CONTINUE( testnum, v%d)"%(8+lmul*3) + " \n", file=f)
    
    if 8+lmul*5 < 32:
        print("\
    #define TEST_VLSEG5_OP( testnum, inst, eew, base ) \\\n\
        TEST_CASE_LOOP( testnum, v8,   \\\n\
            la  x1, base; \\\n\
            inst v8, (x1); \\\n\
        ) \\\n\
        TEST_CASE_LOOP_CONTINUE( testnum, v%d)"%(8+lmul*1) + " \\\n\
        TEST_CASE_LOOP_CONTINUE( testnum, v%d)"%(8+lmul*2) + " \\\n\
        TEST_CASE_LOOP_CONTINUE( testnum, v%d)"%(8+lmul*3) + " \\\n\
        TEST_CASE_LOOP_CONTINUE( testnum, v%d)"%(8+lmul*4) + "\n", file=f)
    
    if 8+lmul*6 < 32:
        print("\
    #define TEST_VLSEG6_OP( testnum, inst, eew, base ) \\\n\
        TEST_CASE_LOOP( testnum, v8,   \\\n\
            la  x1, base; \\\n\
            inst v8, (x1); \\\n\
        ) \\\n\
        TEST_CASE_LOOP_CONTINUE( testnum, v%d)"%(8+lmul*1) + " \\\n\
        TEST_CASE_LOOP_CONTINUE( testnum, v%d)"%(8+lmul*2) + " \\\n\
        TEST_CASE_LOOP_CONTINUE( testnum, v%d)"%(8+lmul*3) + " \\\n\
        TEST_CASE_LOOP_CONTINUE( testnum, v%d)"%(8+lmul*4) + " \\\n\
        TEST_CASE_LOOP_CONTINUE( testnum, v%d)"%(8+lmul*5) + "\n", file=f)
    
    if 8+lmul*7 < 32:
        print("#define TEST_VLSEG7_OP( testnum, inst, eew, base ) \\\n\
        TEST_CASE_LOOP( testnum, v8,   \\\n\
            la  x1, base; \\\n\
            inst v8, (x1); \\\n\
        ) \\\n\
        TEST_CASE_LOOP_CONTINUE( testnum, v%d)"%(8+lmul*1) + " \\\n\
        TEST_CASE_LOOP_CONTINUE( testnum, v%d)"%(8+lmul*2) + " \\\n\
        TEST_CASE_LOOP_CONTINUE( testnum, v%d)"%(8+lmul*3) + " \\\n\
        TEST_CASE_LOOP_CONTINUE( testnum, v%d)"%(8+lmul*4) + " \\\n\
        TEST_CASE_LOOP_CONTINUE( testnum, v%d)"%(8+lmul*5) + " \\\n\
        TEST_CASE_LOOP_CONTINUE( testnum, v%d)"%(8+lmul*6) + "\n", file=f)
    
    if 8+lmul*8 < 32:
        print("#define TEST_VLSEG8_OP( testnum, inst, eew, base ) \\\n\
        TEST_CASE_LOOP( testnum, v8,   \\\n\
            la  x1, base; \\\n\
            inst v8, (x1); \\\n\
        ) \\\n\
        TEST_CASE_LOOP_CONTINUE( testnum, v%d)"%(8+lmul*1) + " \\\n\
        TEST_CASE_LOOP_CONTINUE( testnum, v%d)"%(8+lmul*2) + " \\\n\
        TEST_CASE_LOOP_CONTINUE( testnum, v%d)"%(8+lmul*3) + " \\\n\
        TEST_CASE_LOOP_CONTINUE( testnum, v%d)"%(8+lmul*4) + " \\\n\
        TEST_CASE_LOOP_CONTINUE( testnum, v%d)"%(8+lmul*5) + " \\\n\
        TEST_CASE_LOOP_CONTINUE( testnum, v%d)"%(8+lmul*6) + " \\\n\
        TEST_CASE_LOOP_CONTINUE( testnum, v%d)"%(8+lmul*7) + " \n", file=f)

def generate_vlsseg_macro(f, lmul):
    print("\
    #define TEST_VLSSEG1_OP(  testnum, inst, eew, stride, base  ) \\\n\
        TEST_CASE_LOOP( testnum, v8,   \\\n\
            la  x1, base; \\\n\
            li  x2, stride; \\\n\
            inst v8, (x1), x2; \\\n\
        ) \n\
    #define TEST_VLSSEG2_OP(  testnum, inst, eew, stride, base  ) \\\n\
        TEST_CASE_LOOP( testnum, v8,   \\\n\
            la  x1, base; \\\n\
            li  x2, stride; \\\n\
            inst v8, (x1), x2; \\\n\
        ) \\\n\
        TEST_CASE_LOOP_CONTINUE( testnum, v%d) "%(8+lmul) + " \n\
    #define TEST_VLSSEG3_OP(  testnum, inst, eew, stride, base  ) \\\n\
        TEST_CASE_LOOP( testnum, v8,   \\\n\
            la  x1, base; \\\n\
            li  x2, stride; \\\n\
            inst v8, (x1), x2; \\\n\
        ) \\\n\
        TEST_CASE_LOOP_CONTINUE( testnum, v%d)"%(8+lmul) + "  \\\n\
        TEST_CASE_LOOP_CONTINUE( testnum, v%d)"%(8+lmul*2) + "\n", file=f)
    
    if 8+lmul*4 < 32:
        print("#define TEST_VLSSEG4_OP(  testnum, inst, eew, stride, base  ) \\\n\
        TEST_CASE_LOOP( testnum, v8,   \\\n\
            la  x1, base; \\\n\
            li  x2, stride; \\\n\
            inst v8, (x1), x2; \\\n\
        ) \\\n\
        TEST_CASE_LOOP_CONTINUE( testnum, v%d)"%(8+lmul*1) + "  \\\n\
        TEST_CASE_LOOP_CONTINUE( testnum, v%d)"%(8+lmul*2) + "  \\\n\
        TEST_CASE_LOOP_CONTINUE( testnum, v%d)"%(8+lmul*3) + " \n", file=f)
    
    if 8+lmul*5 < 32:
        print("#define TEST_VLSSEG5_OP(  testnum, inst, eew, stride, base  ) \\\n\
        TEST_CASE_LOOP( testnum, v8,   \\\n\
            la  x1, base; \\\n\
            li  x2, stride; \\\n\
            inst v8, (x1), x2; \\\n\
        ) \\\n\
        TEST_CASE_LOOP_CONTINUE( testnum, v%d)"%(8+lmul*1) + " \\\n\
        TEST_CASE_LOOP_CONTINUE( testnum, v%d)"%(8+lmul*2) + " \\\n\
        TEST_CASE_LOOP_CONTINUE( testnum, v%d)"%(8+lmul*3) + " \\\n\
        TEST_CASE_LOOP_CONTINUE( testnum, v%d)"%(8+lmul*4) + "\n", file=f)
    
    if 8+lmul*6 < 32:
        print("#define TEST_VLSSEG6_OP(  testnum, inst, eew, stride, base  ) \\\n\
        TEST_CASE_LOOP( testnum, v8,   \\\n\
            la  x1, base; \\\n\
            li  x2, stride; \\\n\
            inst v8, (x1), x2; \\\n\
        ) \\\n\
        TEST_CASE_LOOP_CONTINUE( testnum, v%d)"%(8+lmul*1) + " \\\n\
        TEST_CASE_LOOP_CONTINUE( testnum, v%d)"%(8+lmul*2) + " \\\n\
        TEST_CASE_LOOP_CONTINUE( testnum, v%d)"%(8+lmul*3) + " \\\n\
        TEST_CASE_LOOP_CONTINUE( testnum, v%d)"%(8+lmul*4) + " \\\n\
        TEST_CASE_LOOP_CONTINUE( testnum, v%d)"%(8+lmul*5) + "\n", file=f)
    
    if 8+lmul*7 < 32:
        print("#define TEST_VLSSEG7_OP(  testnum, inst, eew, stride, base  ) \\\n\
        TEST_CASE_LOOP( testnum, v8,   \\\n\
            la  x1, base; \\\n\
            li  x2, stride; \\\n\
            inst v8, (x1), x2; \\\n\
        ) \\\n\
        TEST_CASE_LOOP_CONTINUE( testnum, v%d)"%(8+lmul*1) + " \\\n\
        TEST_CASE_LOOP_CONTINUE( testnum, v%d)"%(8+lmul*2) + " \\\n\
        TEST_CASE_LOOP_CONTINUE( testnum, v%d)"%(8+lmul*3) + " \\\n\
        TEST_CASE_LOOP_CONTINUE( testnum, v%d)"%(8+lmul*4) + " \\\n\
        TEST_CASE_LOOP_CONTINUE( testnum, v%d)"%(8+lmul*5) + " \\\n\
        TEST_CASE_LOOP_CONTINUE( testnum, v%d)"%(8+lmul*6) + "\n", file=f)
    
    if 8+lmul*8 < 32:
        print("#define TEST_VLSSEG8_OP(  testnum, inst, eew, stride, base  ) \\\n\
        TEST_CASE_LOOP( testnum, v8,   \\\n\
            la  x1, base; \\\n\
            li  x2, stride; \\\n\
            inst v8, (x1), x2; \\\n\
        ) \\\n\
        TEST_CASE_LOOP_CONTINUE( testnum, v%d)"%(8+lmul*1) + " \\\n\
        TEST_CASE_LOOP_CONTINUE( testnum, v%d)"%(8+lmul*2) + " \\\n\
        TEST_CASE_LOOP_CONTINUE( testnum, v%d)"%(8+lmul*3) + " \\\n\
        TEST_CASE_LOOP_CONTINUE( testnum, v%d)"%(8+lmul*4) + " \\\n\
        TEST_CASE_LOOP_CONTINUE( testnum, v%d)"%(8+lmul*5) + " \\\n\
        TEST_CASE_LOOP_CONTINUE( testnum, v%d)"%(8+lmul*6) + " \\\n\
        TEST_CASE_LOOP_CONTINUE( testnum, v%d)"%(8+lmul*7) + " \n", file=f)

def generate_vlxeiseg_macro(f, lmul):
    print("\
    #define TEST_VLXSEG1_OP(  testnum, inst, index_eew, base_data, base_index  ) \\\n\
        TEST_CASE_LOOP( testnum, v16,   \\\n\
            la  x1, base_data; \\\n\
            la  x6, base_index; \\\n\
            MK_VLE_INST(index_eew) v8, (x6); \\\n\
            inst v16, (x1), v8; \\\n\
        ) \n\
    #define TEST_VLXSEG2_OP(  testnum, inst, index_eew, base_data, base_index  ) \\\n\
        TEST_CASE_LOOP( testnum, v16,   \\\n\
            la  x1, base_data; \\\n\
            la  x6, base_index; \\\n\
            MK_VLE_INST(index_eew) v8, (x6); \\\n\
            inst v16, (x1), v8; \\\n\
        ) \\\n\
        TEST_CASE_LOOP_CONTINUE( testnum, v%d) "%(16+lmul) + " \n", file=f)
    
    
    if 16+lmul*4 < 32:
        print("#define TEST_VLXSEG3_OP(  testnum, inst, index_eew, base_data, base_index  ) \\\n\
        TEST_CASE_LOOP( testnum, v16,   \\\n\
            la  x1, base_data; \\\n\
            la  x6, base_index; \\\n\
            MK_VLE_INST(index_eew) v8, (x6); \\\n\
            inst v16, (x1), v8; \\\n\
        ) \\\n\
        TEST_CASE_LOOP_CONTINUE( testnum, v%d)"%(16+lmul) + "  \\\n\
        TEST_CASE_LOOP_CONTINUE( testnum, v%d)"%(16+lmul*2) + "\n", file=f)
    
    if 16+lmul*4 < 32:
        print("#define TEST_VLXSEG4_OP(  testnum, inst, index_eew, base_data, base_index  ) \\\n\
        TEST_CASE_LOOP( testnum, v16,   \\\n\
            la  x1, base_data; \\\n\
            la  x6, base_index; \\\n\
            MK_VLE_INST(index_eew) v8, (x6); \\\n\
            inst v16, (x1), v8; \\\n\
        ) \\\n\
        TEST_CASE_LOOP_CONTINUE( testnum, v%d)"%(16+lmul*1) + "  \\\n\
        TEST_CASE_LOOP_CONTINUE( testnum, v%d)"%(16+lmul*2) + "  \\\n\
        TEST_CASE_LOOP_CONTINUE( testnum, v%d)"%(16+lmul*3) + " \n", file=f)
    
    if 16+lmul*5 < 32:
        print("#define TEST_VLXSEG5_OP(  testnum, inst, index_eew, base_data, base_index  ) \\\n\
        TEST_CASE_LOOP( testnum, v16,   \\\n\
            la  x1, base_data; \\\n\
            la  x6, base_index; \\\n\
            MK_VLE_INST(index_eew) v8, (x6); \\\n\
            inst v16, (x1), v8; \\\n\
        ) \\\n\
        TEST_CASE_LOOP_CONTINUE( testnum, v%d)"%(16+lmul*1) + " \\\n\
        TEST_CASE_LOOP_CONTINUE( testnum, v%d)"%(16+lmul*2) + " \\\n\
        TEST_CASE_LOOP_CONTINUE( testnum, v%d)"%(16+lmul*3) + " \\\n\
        TEST_CASE_LOOP_CONTINUE( testnum, v%d)"%(16+lmul*4) + "\n", file=f)
    
    if 16+lmul*6 < 32:
        print("#define TEST_VLXSEG6_OP(  testnum, inst, index_eew, base_data, base_index  ) \\\n\
        TEST_CASE_LOOP( testnum, v16,   \\\n\
            la  x1, base_data; \\\n\
            la  x6, base_index; \\\n\
            MK_VLE_INST(index_eew) v8, (x6); \\\n\
            inst v16, (x1), v8; \\\n\
        ) \\\n\
        TEST_CASE_LOOP_CONTINUE( testnum, v%d)"%(16+lmul*1) + " \\\n\
        TEST_CASE_LOOP_CONTINUE( testnum, v%d)"%(16+lmul*2) + " \\\n\
        TEST_CASE_LOOP_CONTINUE( testnum, v%d)"%(16+lmul*3) + " \\\n\
        TEST_CASE_LOOP_CONTINUE( testnum, v%d)"%(16+lmul*4) + " \\\n\
        TEST_CASE_LOOP_CONTINUE( testnum, v%d)"%(16+lmul*5) + "\n", file=f)
   
    if 16+lmul*7 < 32:
        print(" #define TEST_VLXSEG7_OP(  testnum, inst, index_eew, base_data, base_index  ) \\\n\
        TEST_CASE_LOOP( testnum, v16,   \\\n\
            la  x1, base_data; \\\n\
            la  x6, base_index; \\\n\
            MK_VLE_INST(index_eew) v8, (x6); \\\n\
            inst v16, (x1), v8; \\\n\
        ) \\\n\
        TEST_CASE_LOOP_CONTINUE( testnum, v%d)"%(16+lmul*1) + " \\\n\
        TEST_CASE_LOOP_CONTINUE( testnum, v%d)"%(16+lmul*2) + " \\\n\
        TEST_CASE_LOOP_CONTINUE( testnum, v%d)"%(16+lmul*3) + " \\\n\
        TEST_CASE_LOOP_CONTINUE( testnum, v%d)"%(16+lmul*4) + " \\\n\
        TEST_CASE_LOOP_CONTINUE( testnum, v%d)"%(16+lmul*5) + " \\\n\
        TEST_CASE_LOOP_CONTINUE( testnum, v%d)"%(16+lmul*6) + "\n", file=f)
    
    if 16+lmul*8 < 32:
        print("#define TEST_VLXSEG8_OP(  testnum, inst, index_eew, base_data, base_index  ) \\\n\
        TEST_CASE_LOOP( testnum, v16,   \\\n\
            la  x1, base_data; \\\n\
            la  x6, base_index; \\\n\
            MK_VLE_INST(index_eew) v8, (x6); \\\n\
            inst v16, (x1), v8; \\\n\
        ) \\\n\
        TEST_CASE_LOOP_CONTINUE( testnum, v%d)"%(16+lmul*1) + " \\\n\
        TEST_CASE_LOOP_CONTINUE( testnum, v%d)"%(16+lmul*2) + " \\\n\
        TEST_CASE_LOOP_CONTINUE( testnum, v%d)"%(16+lmul*3) + " \\\n\
        TEST_CASE_LOOP_CONTINUE( testnum, v%d)"%(16+lmul*4) + " \\\n\
        TEST_CASE_LOOP_CONTINUE( testnum, v%d)"%(16+lmul*5) + " \\\n\
        TEST_CASE_LOOP_CONTINUE( testnum, v%d)"%(16+lmul*6) + " \\\n\
        TEST_CASE_LOOP_CONTINUE( testnum, v%d)"%(16+lmul*7) + " \n", file=f)


def generate_vlre_macro(f, lmul):
    print("\
    #define TEST_VLRE1_OP( testnum, inst,  base ) \\\n\
        TEST_CASE_LOOP( testnum, v8,   \\\n\
            la  x1, base; \\\n\
            inst v8, (x1); \\\n\
        ) \n", file=f)
    
    print("#define TEST_VLRE2_OP( testnum, inst,  base ) \\\n\
        TEST_CASE_LOOP( testnum, v8,   \\\n\
            la  x1, base; \\\n\
            inst v8, (x1); \\\n\
        ) \\", file=f)
    if lmul <= 1:
        print("TEST_CASE_LOOP_CONTINUE( testnum, v%d) "%(8+1) + " \n", file=f)
    print("", file=f)
    
    print("#define TEST_VLRE4_OP( testnum, inst,  base ) \\\n\
        TEST_CASE_LOOP( testnum, v8,   \\\n\
            la  x1, base; \\\n\
            inst v8, (x1); \\\n\
        ) \\", file=f)
    if lmul <= 1:
        print("TEST_CASE_LOOP_CONTINUE( testnum, v%d)"%(8+1*1) + "  \\\n\
        TEST_CASE_LOOP_CONTINUE( testnum, v%d)"%(8+1*2) + "  \\\n\
        TEST_CASE_LOOP_CONTINUE( testnum, v%d)"%(8+1*3) + " \n", file=f)
    elif lmul == 2:
        print("TEST_CASE_LOOP_CONTINUE( testnum, v%d)"%(8+1*2) + " \n", file=f)
    print("", file=f)
    
    
    print("#define TEST_VLRE8_OP( testnum, inst,  base ) \\\n\
        TEST_CASE_LOOP( testnum, v8,   \\\n\
            la  x1, base; \\\n\
            inst v8, (x1); \\\n\
        ) \\", file=f)
    if lmul <= 1:
        print("TEST_CASE_LOOP_CONTINUE( testnum, v%d)"%(8+1*1) + " \\\n\
        TEST_CASE_LOOP_CONTINUE( testnum, v%d)"%(8+1*2) + " \\\n\
        TEST_CASE_LOOP_CONTINUE( testnum, v%d)"%(8+1*3) + " \\\n\
        TEST_CASE_LOOP_CONTINUE( testnum, v%d)"%(8+1*4) + " \\\n\
        TEST_CASE_LOOP_CONTINUE( testnum, v%d)"%(8+1*5) + " \\\n\
        TEST_CASE_LOOP_CONTINUE( testnum, v%d)"%(8+1*6) + " \\\n\
        TEST_CASE_LOOP_CONTINUE( testnum, v%d)"%(8+1*7) + " \n", file=f)
    elif lmul == 2:
        print("TEST_CASE_LOOP_CONTINUE( testnum, v%d)"%(8+1*2) + " \\\n\
        TEST_CASE_LOOP_CONTINUE( testnum, v%d)"%(8+1*4) + " \\\n\
        TEST_CASE_LOOP_CONTINUE( testnum, v%d)"%(8+1*6) + "\n", file=f)
    elif lmul == 4:
        print("TEST_CASE_LOOP_CONTINUE( testnum, v%d)"%(8+1*4) + "\n", file=f)

def generate_macros_vlseg(f, lmul, vsew, eew):
    emul = eew / vsew * lmul
    emul = 1 if emul < 1 else int(emul)
    lmul = 1 if lmul < 1 else int(lmul)
    # testreg is v8
    generate_vlseg_macro(f, lmul)
    for n in range(1, 32):
        if n == 12 or n == 20 or n == 24: # signature base registers
            continue
        print("#define TEST_VLSEG1_OP_1%d( testnum, inst, eew, base )"%n + " \\\n\
            TEST_CASE_LOOP( testnum, v8,  \\\n\
                la  x%d, base; "%n + "\\\n\
                inst v8, (x%d); "%n + "\\\n\
        )", file=f)
    for n in range(1, 31):
        # Beacuse of the widening instruction, rd should valid for the destination’s EMUL
        if n % emul == 0 and n % lmul == 0 and n!= 12 and n != 20 and n != 24:
            print("#define TEST_VLSEG1_OP_rd%d( testnum, inst, eew, base )"%n + " \\\n\
                TEST_CASE_LOOP( testnum, v%d,  "%n + "\\\n\
                    la  x2, base; \\\n\
                    inst v%d, (x2); "%n + "\\\n\
            ) ", file=f)

def generate_macros_vlsseg(f, lmul, vsew, eew):
    emul = eew / vsew * lmul
    emul = 1 if emul < 1 else int(emul)
    lmul = 1 if lmul < 1 else int(lmul)
    # testreg is v8
    generate_vlsseg_macro(f, lmul)
    for n in range(1, 32):
        if n == 12 or n == 20 or n == 24 or n == 30: # signature base registers
            continue
        print("#define TEST_VLSSEG1_OP_1%d(  testnum, inst, eew, stride, base )"%n + " \\\n\
            TEST_CASE_LOOP( testnum, v8,   \\\n\
                la  x%d, base; "%n + "\\\n\
                li  x30, stride; \\\n\
                inst v8, (x%d), x30 ; "%n + "\\\n\
        )", file=f)
    for n in range(1, 32):
        # Beacuse of the widening instruction, rd should valid for the destination’s EMUL
        if n % emul == 0 and n % lmul == 0 and n!= 12 and n != 20 and n != 24:
            print("#define TEST_VLSSEG1_OP_rd%d(  testnum, inst, eew, stride, base )"%n + " \\\n\
                TEST_CASE_LOOP( testnum, v%d,   "%n + "\\\n\
                    la  x1, base; \\\n\
                    li  x2, stride; \\\n\
                    inst v%d, (x1), x2; "%n + "\\\n\
            ) ", file=f)
    print("#define TEST_VLSSEG1_OP_130(  testnum, inst, eew, stride, base ) \\\n\
            TEST_CASE_LOOP( testnum, v16,   \\\n\
                la  x30, base; \\\n\
                li  x3, stride; \\\n\
                inst v16, (x30), x3 ; \\\n\
        )", file=f)

def generate_macros_vlxei(f, vsew, lmul):
    lmul = 1 if lmul < 1 else int(lmul)
    for n in range(2, 32):
        if n == 12 or n == 20 or n == 24:
            continue
        rs_index = 31 if n == 30 else 30
        rs_vl = 29 if n == 30 or n == 31 else 31
        print("#define TEST_VLXEI_OP_1%d( testnum, inst, index_eew, result1, result2, base_data, base_index )"%n + " \\\n\
            TEST_CASE_LOOP( testnum, v16,   \\\n\
                la  x%d, base_data; "%n + "\\\n\
                la  x%d, base_index; "%(rs_index) + "\\\n\
                vsetvli x%d, x0, MK_EEW(index_eew), tu, mu; "%(rs_vl) + "\\\n\
                MK_VLE_INST(index_eew) v8, (x%d); "%(rs_index) + "\\\n\
                VSET_VSEW_4AVL \\\n\
                inst v16, (x%d), v8; "%n + "\\\n\
        )", file=f)
    
    for n in range(1, 32):
        if n == 12 or n == 20 or n == 24:
            continue
        # Beacuse of the widening instruction, rd should valid for the destination’s EMUL
        vs = 16 if n == 8 else 8
        print("#define TEST_VLXEI_OP_rd%d( testnum, inst, index_eew, result1, result2, base_data, base_index )"%n + " \\\n\
            TEST_CASE_LOOP( testnum, v%d, "%n + "\\\n\
                la  x1, base_data; \\\n\
                la  x6, base_index; \\\n\
                vsetvli x31, x0, MK_EEW(index_eew), tu, mu; \\\n\
                MK_VLE_INST(index_eew) v%d, (x6); \\\n\
                VSET_VSEW_4AVL \\\n\
                inst v%d, (x1), v%d; "%(vs, n, vs) + "\\\n\
        ) ", file=f)


def generate_macros_vlxeiseg(f, lmul, vsew, eew):
    emul = eew / vsew * lmul
    emul = 1 if emul < 1 else int(emul)
    lmul = 1 if lmul < 1 else int(lmul)
    # testreg is v8
    generate_vlxeiseg_macro(f, lmul)
    for n in range(1,31):
        if n == 12 or n == 20 or n == 24 or n == 31: # signature base registers
            continue
        print("#define TEST_VLXSEG1_OP_1%d( testnum, inst, index_eew, base_data, base_index  )"%n + " \\\n\
        TEST_CASE_LOOP( testnum, v16,   \\\n\
            la  x%d, base_data; "%n + " \\\n\
            la  x31, base_index; \\\n\
            MK_VLE_INST(index_eew) v8, (x31);    \\\n\
            inst v16, (x%d), v8 ; "%n + " \\\n\
        )",file=f)

    for n in range(1,30):
        if n == 8 or n == 16 or n % emul != 0 or n % lmul != 0 or n == 12 or n == 20 or n == 24 or n == 30 :
            continue
        print("#define TEST_VLXSEG1_OP_rd%d( testnum, inst, index_eew, base_data, base_index )"%n + " \\\n\
        TEST_CASE_LOOP( testnum, v%d,  "%n + "\\\n\
            la  x1, base_data;  \\\n\
            la  x6, base_index; \\\n\
            MK_VLE_INST(index_eew) v8, (x6);    \\\n\
            inst v%d, (x1), v8; "%n + " \\\n\
        )",file=f)

    print("#define TEST_VLXSEG1_OP_131( testnum, inst, index_eew, base_data, base_index ) \\\n\
        TEST_CASE_LOOP( testnum, v16, \\\n\
            la  x31, base_data; \\\n\
            la  x2, base_index; \\\n\
            MK_VLE_INST(index_eew) v8, (x2);    \\\n\
            inst v16, (x31), v8 ;  \\\n\
        )",file=f)
    print("#define TEST_VLXSEG1_OP_rd30( testnum, inst, index_eew, base_data, base_index ) \\\n\
        TEST_CASE_LOOP( testnum, v30, \\\n\
            la  x1, base_data;  \\\n\
            la  x6, base_index; \\\n\
            MK_VLE_INST(index_eew) v8, (x6);    \\\n\
            inst v30, (x1), v8 ;  \\\n\
        )",file=f)


def generate_macros_vse(f, lmul, vsew, eew):
    emul = eew / vsew * lmul
    emul = 1 if emul < 1 else int(emul)
    for n in range(1,30):
        if n == 12 or n == 20 or n == 24 or n == 30: # signature base registers
            continue
        print("#define TEST_VSE_OP_1%d( testnum, load_inst, store_inst, eew, result, base )"%n + " \\\n\
        TEST_CASE_LOOP( testnum, v16,  \\\n\
            la  x%d, base; "%n + " \\\n\
            li  x30, result; \\\n\
            vmv.v.x v8, x30; \\\n\
            VSET_VSEW \\\n\
            store_inst v8, (x%d); "%n + "\\\n\
            load_inst v16, (x%d) ; "%n + " \\\n\
        )",file=f)

    for n in range(1,31):
        if n == 8 or n == 16 or n == 31 or n % emul != 0 or n == 12 or n == 20 or n == 24: 
            continue
        print("#define TEST_VSE_OP_rd%d( testnum, load_inst, store_inst, eew, result, base )"%n + " \\\n\
        TEST_CASE_LOOP( testnum, v16, " + "\\\n\
            la  x1, base;  \\\n\
            li  x30, result; \\\n\
            vmv.v.x v%d, x30;  "%n + "\\\n\
            VSET_VSEW \\\n\
            store_inst v%d, (x1); "%n + " \\\n\
            load_inst v16, (x1); \\\n\
        )",file=f)

    print("#define TEST_VSE_OP_130( testnum, load_inst, store_inst, eew, result, base ) \\\n\
        TEST_CASE_LOOP( testnum, v16,  \\\n\
            la  x30, base;  \\\n\
            li  x2, result; \\\n\
            vmv.v.x v8, x2; \\\n\
            VSET_VSEW \\\n\
            store_inst v8, (x30); \\\n\
            load_inst v16, (x30) ;  \\\n\
        )",file=f)


def generate_vsseg_macro(f, lmul):
    print("\
    #define TEST_VSSEG1_OP( testnum, load_inst, store_inst, eew,  base, source_addr ) \\\n\
        TEST_CASE_LOOP( testnum, v8,   \\\n\
            la  x1, base; \\\n\
            la  x2, source_addr; \\\n\
            vl8re32.v v16, (x2); \\\n\
            store_inst v16, (x1); \\\n\
            load_inst v8, (x1);  \\\n\
        ) \n\
    #define TEST_VSSEG2_OP( testnum, load_inst, store_inst, eew,  base, source_addr ) \\\n\
        TEST_CASE_LOOP( testnum, v8,   \\\n\
            la  x1, base; \\\n\
            la  x2, source_addr; \\\n\
            vl8re32.v v16, (x2); \\\n\
            store_inst v16, (x1); \\\n\
            load_inst v8, (x1);  \\\n\
        ) \\\n\
        TEST_CASE_LOOP_CONTINUE( testnum, v%d) "%(8+lmul) + " \n\
    #define TEST_VSSEG3_OP( testnum, load_inst, store_inst, eew,  base, source_addr ) \\\n\
        TEST_CASE_LOOP( testnum, v8,   \\\n\
            la  x1, base; \\\n\
            la  x2, source_addr; \\\n\
            vl8re32.v v16, (x2); \\\n\
            store_inst v16, (x1); \\\n\
            load_inst v8, (x1);  \\\n\
        ) \\\n\
        TEST_CASE_LOOP_CONTINUE( testnum, v%d)"%(8+lmul) + "  \\\n\
        TEST_CASE_LOOP_CONTINUE( testnum, v%d)"%(8+lmul*2) + "\n", file=f)
    
    if 8+lmul*4 < 32:
        print("#define TEST_VSSEG4_OP( testnum, load_inst, store_inst, eew,  base, source_addr ) \\\n\
        TEST_CASE_LOOP( testnum, v8,   \\\n\
            la  x1, base; \\\n\
            la  x2, source_addr; \\\n\
            vl8re32.v v16, (x2); \\\n\
            store_inst v16, (x1); \\\n\
            load_inst v8, (x1);  \\\n\
        ) \\\n\
        TEST_CASE_LOOP_CONTINUE( testnum, v%d)"%(8+lmul*1) + "  \\\n\
        TEST_CASE_LOOP_CONTINUE( testnum, v%d)"%(8+lmul*2) + "  \\\n\
        TEST_CASE_LOOP_CONTINUE( testnum, v%d)"%(8+lmul*3) + " \n", file=f)
    
    if 8+lmul*5 < 32:
        print("#define TEST_VSSEG5_OP( testnum, load_inst, store_inst, eew,  base, source_addr ) \\\n\
        TEST_CASE_LOOP( testnum, v8,   \\\n\
            la  x1, base; \\\n\
            la  x2, source_addr; \\\n\
            vl8re32.v v16, (x2); \\\n\
            store_inst v16, (x1); \\\n\
            load_inst v8, (x1);  \\\n\
        ) \\\n\
        TEST_CASE_LOOP_CONTINUE( testnum, v%d)"%(8+lmul*1) + " \\\n\
        TEST_CASE_LOOP_CONTINUE( testnum, v%d)"%(8+lmul*2) + " \\\n\
        TEST_CASE_LOOP_CONTINUE( testnum, v%d)"%(8+lmul*3) + " \\\n\
        TEST_CASE_LOOP_CONTINUE( testnum, v%d)"%(8+lmul*4) + "\n", file=f)
    
    if 8+lmul*6 < 32:
        print("#define TEST_VSSEG6_OP( testnum, load_inst, store_inst, eew,  base, source_addr ) \\\n\
        TEST_CASE_LOOP( testnum, v8,   \\\n\
            la  x1, base; \\\n\
            la  x2, source_addr; \\\n\
            vl8re32.v v16, (x2); \\\n\
            store_inst v16, (x1); \\\n\
            load_inst v8, (x1);  \\\n\
        ) \\\n\
        TEST_CASE_LOOP_CONTINUE( testnum, v%d)"%(8+lmul*1) + " \\\n\
        TEST_CASE_LOOP_CONTINUE( testnum, v%d)"%(8+lmul*2) + " \\\n\
        TEST_CASE_LOOP_CONTINUE( testnum, v%d)"%(8+lmul*3) + " \\\n\
        TEST_CASE_LOOP_CONTINUE( testnum, v%d)"%(8+lmul*4) + " \\\n\
        TEST_CASE_LOOP_CONTINUE( testnum, v%d)"%(8+lmul*5) + "\n", file=f)
    
    if 8+lmul*7 < 32:
        print("#define TEST_VSSEG7_OP( testnum, load_inst, store_inst, eew,  base, source_addr ) \\\n\
        TEST_CASE_LOOP( testnum, v8,   \\\n\
            la  x1, base; \\\n\
            la  x2, source_addr; \\\n\
            vl8re32.v v16, (x2); \\\n\
            store_inst v16, (x1); \\\n\
            load_inst v8, (x1);  \\\n\
        ) \\\n\
        TEST_CASE_LOOP_CONTINUE( testnum, v%d)"%(8+lmul*1) + " \\\n\
        TEST_CASE_LOOP_CONTINUE( testnum, v%d)"%(8+lmul*2) + " \\\n\
        TEST_CASE_LOOP_CONTINUE( testnum, v%d)"%(8+lmul*3) + " \\\n\
        TEST_CASE_LOOP_CONTINUE( testnum, v%d)"%(8+lmul*4) + " \\\n\
        TEST_CASE_LOOP_CONTINUE( testnum, v%d)"%(8+lmul*5) + " \\\n\
        TEST_CASE_LOOP_CONTINUE( testnum, v%d)"%(8+lmul*6) + "\n", file=f)
    
    if 8+lmul*8 < 32:
        print("#define TEST_VSSEG8_OP( testnum, load_inst, store_inst, eew,  base, source_addr ) \\\n\
        TEST_CASE_LOOP( testnum, v8,   \\\n\
            la  x1, base; \\\n\
            la  x2, source_addr; \\\n\
            vl8re32.v v16, (x2); \\\n\
            store_inst v16, (x1); \\\n\
            load_inst v8, (x1);  \\\n\
        ) \\\n\
        TEST_CASE_LOOP_CONTINUE( testnum, v%d)"%(8+lmul*1) + " \\\n\
        TEST_CASE_LOOP_CONTINUE( testnum, v%d)"%(8+lmul*2) + " \\\n\
        TEST_CASE_LOOP_CONTINUE( testnum, v%d)"%(8+lmul*3) + " \\\n\
        TEST_CASE_LOOP_CONTINUE( testnum, v%d)"%(8+lmul*4) + " \\\n\
        TEST_CASE_LOOP_CONTINUE( testnum, v%d)"%(8+lmul*5) + " \\\n\
        TEST_CASE_LOOP_CONTINUE( testnum, v%d)"%(8+lmul*6) + " \\\n\
        TEST_CASE_LOOP_CONTINUE( testnum, v%d)"%(8+lmul*7) + " \n", file=f)


def generate_vssseg_macro(f, lmul):
    print("\
    #define TEST_VSSSEG1_OP( testnum, load_inst, store_inst, eew, stride, base, source_addr ) \\\n\
        TEST_CASE_LOOP( testnum, v8,   \\\n\
            la  x1, base; \\\n\
            li  x2, stride; \\\n\
            la  x3, source_addr; \\\n\
            vl8re32.v v16, (x3); \\\n\
            store_inst v16, (x1), x2; \\\n\
            load_inst v8, (x1), x2;  \\\n\
        ) \n\
    #define TEST_VSSSEG2_OP( testnum, load_inst, store_inst, eew, stride, base, source_addr ) \\\n\
        TEST_CASE_LOOP( testnum, v8,   \\\n\
            la  x1, base; \\\n\
            li  x2, stride; \\\n\
            la  x3, source_addr; \\\n\
            vl8re32.v v16, (x3); \\\n\
            store_inst v16, (x1), x2; \\\n\
            load_inst v8, (x1), x2;  \\\n\
        ) \\\n\
        TEST_CASE_LOOP_CONTINUE( testnum, v%d) "%(8+lmul) + " \n\
    #define TEST_VSSSEG3_OP( testnum, load_inst, store_inst, eew, stride, base, source_addr ) \\\n\
        TEST_CASE_LOOP( testnum, v8,   \\\n\
            la  x1, base; \\\n\
            li  x2, stride; \\\n\
            la  x3, source_addr; \\\n\
            vl8re32.v v16, (x3); \\\n\
            store_inst v16, (x1), x2; \\\n\
            load_inst v8, (x1), x2;  \\\n\
        ) \\\n\
        TEST_CASE_LOOP_CONTINUE( testnum, v%d)"%(8+lmul) + "  \\\n\
        TEST_CASE_LOOP_CONTINUE( testnum, v%d)"%(8+lmul*2) + "\n", file=f)
    
    if 8+lmul*4 < 32:
        print("#define TEST_VSSSEG4_OP( testnum, load_inst, store_inst, eew, stride, base, source_addr ) \\\n\
        TEST_CASE_LOOP( testnum, v8,   \\\n\
            la  x1, base; \\\n\
            li  x2, stride; \\\n\
            la  x3, source_addr; \\\n\
            vl8re32.v v16, (x3); \\\n\
            store_inst v16, (x1), x2; \\\n\
            load_inst v8, (x1), x2;  \\\n\
        ) \\\n\
        TEST_CASE_LOOP_CONTINUE( testnum, v%d)"%(8+lmul*1) + "  \\\n\
        TEST_CASE_LOOP_CONTINUE( testnum, v%d)"%(8+lmul*2) + "  \\\n\
        TEST_CASE_LOOP_CONTINUE( testnum, v%d)"%(8+lmul*3) + " \n", file=f)
    
    if 8+lmul*5 < 32:
        print("#define TEST_VSSSEG5_OP( testnum, load_inst, store_inst, eew, stride, base, source_addr ) \\\n\
        TEST_CASE_LOOP( testnum, v8,   \\\n\
            la  x1, base; \\\n\
            li  x2, stride; \\\n\
            la  x3, source_addr; \\\n\
            vl8re32.v v16, (x3); \\\n\
            store_inst v16, (x1), x2; \\\n\
            load_inst v8, (x1), x2;  \\\n\
        ) \\\n\
        TEST_CASE_LOOP_CONTINUE( testnum, v%d)"%(8+lmul*1) + " \\\n\
        TEST_CASE_LOOP_CONTINUE( testnum, v%d)"%(8+lmul*2) + " \\\n\
        TEST_CASE_LOOP_CONTINUE( testnum, v%d)"%(8+lmul*3) + " \\\n\
        TEST_CASE_LOOP_CONTINUE( testnum, v%d)"%(8+lmul*4) + "\n", file=f)
    
    if 8+lmul*6 < 32:
        print("#define TEST_VSSSEG6_OP( testnum, load_inst, store_inst, eew, stride, base, source_addr ) \\\n\
        TEST_CASE_LOOP( testnum, v8,   \\\n\
            la  x1, base; \\\n\
            li  x2, stride; \\\n\
            la  x3, source_addr; \\\n\
            vl8re32.v v16, (x3); \\\n\
            store_inst v16, (x1), x2; \\\n\
            load_inst v8, (x1), x2;  \\\n\
        ) \\\n\
        TEST_CASE_LOOP_CONTINUE( testnum, v%d)"%(8+lmul*1) + " \\\n\
        TEST_CASE_LOOP_CONTINUE( testnum, v%d)"%(8+lmul*2) + " \\\n\
        TEST_CASE_LOOP_CONTINUE( testnum, v%d)"%(8+lmul*3) + " \\\n\
        TEST_CASE_LOOP_CONTINUE( testnum, v%d)"%(8+lmul*4) + " \\\n\
        TEST_CASE_LOOP_CONTINUE( testnum, v%d)"%(8+lmul*5) + "\n", file=f)
    
    if 8+lmul*7 < 32:
        print("#define TEST_VSSSEG7_OP( testnum, load_inst, store_inst, eew, stride, base, source_addr ) \\\n\
        TEST_CASE_LOOP( testnum, v8,   \\\n\
            la  x1, base; \\\n\
            li  x2, stride; \\\n\
            la  x3, source_addr; \\\n\
            vl8re32.v v16, (x3); \\\n\
            store_inst v16, (x1), x2; \\\n\
            load_inst v8, (x1), x2;  \\\n\
        ) \\\n\
        TEST_CASE_LOOP_CONTINUE( testnum, v%d)"%(8+lmul*1) + " \\\n\
        TEST_CASE_LOOP_CONTINUE( testnum, v%d)"%(8+lmul*2) + " \\\n\
        TEST_CASE_LOOP_CONTINUE( testnum, v%d)"%(8+lmul*3) + " \\\n\
        TEST_CASE_LOOP_CONTINUE( testnum, v%d)"%(8+lmul*4) + " \\\n\
        TEST_CASE_LOOP_CONTINUE( testnum, v%d)"%(8+lmul*5) + " \\\n\
        TEST_CASE_LOOP_CONTINUE( testnum, v%d)"%(8+lmul*6) + "\n", file=f)
    
    if 8+lmul*8 < 32:
        print("#define TEST_VSSSEG8_OP( testnum, load_inst, store_inst, eew, stride, base, source_addr ) \\\n\
        TEST_CASE_LOOP( testnum, v8,   \\\n\
            la  x1, base; \\\n\
            li  x2, stride; \\\n\
            la  x3, source_addr; \\\n\
            vl8re32.v v16, (x3); \\\n\
            store_inst v16, (x1), x2; \\\n\
            load_inst v8, (x1), x2;  \\\n\
        ) \\\n\
        TEST_CASE_LOOP_CONTINUE( testnum, v%d)"%(8+lmul*1) + " \\\n\
        TEST_CASE_LOOP_CONTINUE( testnum, v%d)"%(8+lmul*2) + " \\\n\
        TEST_CASE_LOOP_CONTINUE( testnum, v%d)"%(8+lmul*3) + " \\\n\
        TEST_CASE_LOOP_CONTINUE( testnum, v%d)"%(8+lmul*4) + " \\\n\
        TEST_CASE_LOOP_CONTINUE( testnum, v%d)"%(8+lmul*5) + " \\\n\
        TEST_CASE_LOOP_CONTINUE( testnum, v%d)"%(8+lmul*6) + " \\\n\
        TEST_CASE_LOOP_CONTINUE( testnum, v%d)"%(8+lmul*7) + " \n", file=f)


def generate_vsuxseg_macro(f, lmul):
    print("\
    #define TEST_VSXSEG1_OP( testnum, load_inst, store_inst, index_eew, base_data, base_index, source_addr ) \\\n\
        TEST_CASE_LOOP( testnum, v8,   \\\n\
            la  x1, base_data;   \\\n\
            la  x2, base_index; \\\n\
            la  x3, source_addr; \\\n\
            vl8re32.v v16, (x3); \\\n\
            MK_VLE_INST(index_eew) v24, (x2);    \\\n\
            store_inst v16, (x1), v24;" + " \\\n\
            load_inst v8, (x1), v24; \\\n\
        ) \n\
    #define TEST_VSXSEG2_OP( testnum, load_inst, store_inst, index_eew, base_data, base_index, source_addr ) \\\n\
        TEST_CASE_LOOP( testnum, v8,   \\\n\
            la  x1, base_data;   \\\n\
            la  x2, base_index; \\\n\
            la  x3, source_addr; \\\n\
            vl8re32.v v16, (x3); \\\n\
            MK_VLE_INST(index_eew) v24, (x2);    \\\n\
            store_inst v16, (x1), v24;" + " \\\n\
            load_inst v8, (x1), v24; \\\n\
        ) \\\n\
        TEST_CASE_LOOP_CONTINUE( testnum, v%d) "%(8+lmul) + " \n\
    #define TEST_VSXSEG3_OP( testnum, load_inst, store_inst, index_eew, base_data, base_index, source_addr ) \\\n\
        TEST_CASE_LOOP( testnum, v8,   \\\n\
            la  x1, base_data;   \\\n\
            la  x2, base_index; \\\n\
            la  x3, source_addr; \\\n\
            vl8re32.v v16, (x3); \\\n\
            MK_VLE_INST(index_eew) v24, (x2);    \\\n\
            store_inst v16, (x1), v24;" + " \\\n\
            load_inst v8, (x1), v24; \\\n\
        ) \\\n\
        TEST_CASE_LOOP_CONTINUE( testnum, v%d)"%(8+lmul) + "  \\\n\
        TEST_CASE_LOOP_CONTINUE( testnum, v%d)"%(8+lmul*2) + "\n", file=f)
    
    if 8+lmul*4 < 32:
        print("#define TEST_VSXSEG4_OP( testnum, load_inst, store_inst, index_eew, base_data, base_index, source_addr ) \\\n\
        TEST_CASE_LOOP( testnum, v8,   \\\n\
            la  x1, base_data;   \\\n\
            la  x2, base_index; \\\n\
            la  x3, source_addr; \\\n\
            vl8re32.v v16, (x3); \\\n\
            MK_VLE_INST(index_eew) v24, (x2);    \\\n\
            store_inst v16, (x1), v24;" + " \\\n\
            load_inst v8, (x1), v24; \\\n\
        ) \\\n\
        TEST_CASE_LOOP_CONTINUE( testnum, v%d)"%(8+lmul*1) + "  \\\n\
        TEST_CASE_LOOP_CONTINUE( testnum, v%d)"%(8+lmul*2) + "  \\\n\
        TEST_CASE_LOOP_CONTINUE( testnum, v%d)"%(8+lmul*3) + " \n", file=f)
    
    if 8+lmul*5 < 32:
        print("#define TEST_VSXSEG5_OP( testnum, load_inst, store_inst, index_eew, base_data, base_index, source_addr ) \\\n\
        TEST_CASE_LOOP( testnum, v8,   \\\n\
            la  x1, base_data;   \\\n\
            la  x2, base_index; \\\n\
            la  x3, source_addr; \\\n\
            vl8re32.v v16, (x3); \\\n\
            MK_VLE_INST(index_eew) v24, (x2);    \\\n\
            store_inst v16, (x1), v24;" + " \\\n\
            load_inst v8, (x1), v24; \\\n\
        ) \\\n\
        TEST_CASE_LOOP_CONTINUE( testnum, v%d)"%(8+lmul*1) + " \\\n\
        TEST_CASE_LOOP_CONTINUE( testnum, v%d)"%(8+lmul*2) + " \\\n\
        TEST_CASE_LOOP_CONTINUE( testnum, v%d)"%(8+lmul*3) + " \\\n\
        TEST_CASE_LOOP_CONTINUE( testnum, v%d)"%(8+lmul*4) + "\n", file=f)
    
    if 8+lmul*6 < 32:
        print("#define TEST_VSXSEG6_OP( testnum, load_inst, store_inst, eew, base ) \\\n\
        TEST_CASE_LOOP( testnum, v8,   \\\n\
            la  x1, base_data;   \\\n\
            la  x2, base_index; \\\n\
            la  x3, source_addr; \\\n\
            vl8re32.v v16, (x3); \\\n\
            MK_VLE_INST(index_eew) v24, (x2);    \\\n\
            store_inst v16, (x1), v24;" + " \\\n\
            load_inst v8, (x1), v24; \\\n\
        ) \\\n\
        TEST_CASE_LOOP_CONTINUE( testnum, v%d)"%(8+lmul*1) + " \\\n\
        TEST_CASE_LOOP_CONTINUE( testnum, v%d)"%(8+lmul*2) + " \\\n\
        TEST_CASE_LOOP_CONTINUE( testnum, v%d)"%(8+lmul*3) + " \\\n\
        TEST_CASE_LOOP_CONTINUE( testnum, v%d)"%(8+lmul*4) + " \\\n\
        TEST_CASE_LOOP_CONTINUE( testnum, v%d)"%(8+lmul*5) + "\n", file=f)
    
    if 8+lmul*7 < 32:
        print("#define TEST_VSXSEG7_OP( testnum, load_inst, store_inst, index_eew, base_data, base_index, source_addr ) \\\n\
        TEST_CASE_LOOP( testnum, v8,   \\\n\
            la  x1, base_data;   \\\n\
            la  x2, base_index; \\\n\
            la  x3, source_addr; \\\n\
            vl8re32.v v16, (x3); \\\n\
            MK_VLE_INST(index_eew) v24, (x2);    \\\n\
            store_inst v16, (x1), v24;" + " \\\n\
            load_inst v8, (x1), v24; \\\n\
        ) \\\n\
        TEST_CASE_LOOP_CONTINUE( testnum, v%d)"%(8+lmul*1) + " \\\n\
        TEST_CASE_LOOP_CONTINUE( testnum, v%d)"%(8+lmul*2) + " \\\n\
        TEST_CASE_LOOP_CONTINUE( testnum, v%d)"%(8+lmul*3) + " \\\n\
        TEST_CASE_LOOP_CONTINUE( testnum, v%d)"%(8+lmul*4) + " \\\n\
        TEST_CASE_LOOP_CONTINUE( testnum, v%d)"%(8+lmul*5) + " \\\n\
        TEST_CASE_LOOP_CONTINUE( testnum, v%d)"%(8+lmul*6) + "\n", file=f)
    
    if 8+lmul*8 < 32:
        print("#define TEST_VSXSEG8_OP( testnum, load_inst, store_inst, index_eew, base_data, base_index, source_addr ) \\\n\
        TEST_CASE_LOOP( testnum, v8,   \\\n\
            la  x1, base_data;   \\\n\
            la  x2, base_index; \\\n\
            la  x3, source_addr; \\\n\
            vl8re32.v v16, (x3); \\\n\
            MK_VLE_INST(index_eew) v24, (x2);    \\\n\
            store_inst v16, (x1), v24;" + " \\\n\
            load_inst v8, (x1), v24; \\\n\
        ) \\\n\
        TEST_CASE_LOOP_CONTINUE( testnum, v%d)"%(8+lmul*1) + " \\\n\
        TEST_CASE_LOOP_CONTINUE( testnum, v%d)"%(8+lmul*2) + " \\\n\
        TEST_CASE_LOOP_CONTINUE( testnum, v%d)"%(8+lmul*3) + " \\\n\
        TEST_CASE_LOOP_CONTINUE( testnum, v%d)"%(8+lmul*4) + " \\\n\
        TEST_CASE_LOOP_CONTINUE( testnum, v%d)"%(8+lmul*5) + " \\\n\
        TEST_CASE_LOOP_CONTINUE( testnum, v%d)"%(8+lmul*6) + " \\\n\
        TEST_CASE_LOOP_CONTINUE( testnum, v%d)"%(8+lmul*7) + " \n", file=f)


def generate_vsre_macro(f, lmul):
    print("\
    #define TEST_VSRE1_OP( testnum, load_inst, store_inst,   base, source_addr ) \\\n\
        TEST_CASE_LOOP( testnum, v8,   \\\n\
            la  x1, base; \\\n\
            la  x2, source_addr; \\\n\
            vl8re32.v v16, (x2); \\\n\
            store_inst v16, (x1); \\\n\
            load_inst v8, (x1);  \\\n\
        ) \n\
    #define TEST_VSRE2_OP( testnum, load_inst, store_inst,   base, source_addr ) \\\n\
        TEST_CASE_LOOP( testnum, v8,   \\\n\
            la  x1, base; \\\n\
            la  x2, source_addr; \\\n\
            vl8re32.v v16, (x2); \\\n\
            store_inst v16, (x1); \\\n\
            load_inst v8, (x1);  \\\n\
        ) \\", file=f)
    if lmul <= 1:
        print("TEST_CASE_LOOP_CONTINUE( testnum, v%d) "%(8+1) + " \n", file=f)
    print("", file=f)
    
    print("#define TEST_VSRE4_OP( testnum, load_inst, store_inst,   base, source_addr ) \\\n\
        TEST_CASE_LOOP( testnum, v8,   \\\n\
            la  x1, base; \\\n\
            la  x2, source_addr; \\\n\
            vl8re32.v v16, (x2); \\\n\
            store_inst v16, (x1); \\\n\
            load_inst v8, (x1);  \\\n\
        ) \\", file=f)
    if lmul <= 1:
        print("TEST_CASE_LOOP_CONTINUE( testnum, v%d)"%(8+1*1) + "  \\\n\
        TEST_CASE_LOOP_CONTINUE( testnum, v%d)"%(8+1*2) + "  \\\n\
        TEST_CASE_LOOP_CONTINUE( testnum, v%d)"%(8+1*3) + " \n", file=f)
    elif lmul == 2:
        print("TEST_CASE_LOOP_CONTINUE( testnum, v%d)"%(8+1*2) + " \n", file=f)
    print("", file=f)
    
    print("#define TEST_VSRE8_OP( testnum, load_inst, store_inst,   base, source_addr ) \\\n\
        TEST_CASE_LOOP( testnum, v8,   \\\n\
            la  x1, base; \\\n\
            la  x2, source_addr; \\\n\
            vl8re32.v v16, (x2); \\\n\
            store_inst v16, (x1); \\\n\
            load_inst v8, (x1);  \\\n\
        ) \\", file=f)
    if lmul <= 1:
        print("TEST_CASE_LOOP_CONTINUE( testnum, v%d)"%(8+1*1) + " \\\n\
        TEST_CASE_LOOP_CONTINUE( testnum, v%d)"%(8+1*2) + " \\\n\
        TEST_CASE_LOOP_CONTINUE( testnum, v%d)"%(8+1*3) + " \\\n\
        TEST_CASE_LOOP_CONTINUE( testnum, v%d)"%(8+1*4) + " \\\n\
        TEST_CASE_LOOP_CONTINUE( testnum, v%d)"%(8+1*5) + " \\\n\
        TEST_CASE_LOOP_CONTINUE( testnum, v%d)"%(8+1*6) + " \\\n\
        TEST_CASE_LOOP_CONTINUE( testnum, v%d)"%(8+1*7) + " \n", file=f)
    elif lmul == 2:
        print("TEST_CASE_LOOP_CONTINUE( testnum, v%d)"%(8+1*2) + " \\\n\
        TEST_CASE_LOOP_CONTINUE( testnum, v%d)"%(8+1*4) + " \\\n\
        TEST_CASE_LOOP_CONTINUE( testnum, v%d)"%(8+1*6) + "\n", file=f)
    elif lmul == 4:
        print("TEST_CASE_LOOP_CONTINUE( testnum, v%d)"%(8+1*4) + "\n", file=f)

def generate_macros_vsse(f):
    for n in range(1,31):
        if n == 12 or n == 20 or n == 24 or n == 29 or n == 30: # signature base registers
            continue
        print("#define TEST_VSSE_OP_1%d( testnum, load_inst, store_inst, eew, result, stride, base )"%n + " \\\n\
        TEST_CASE_LOOP( testnum, v16,  \\\n\
            la  x%d, base; "%n + " \\\n\
            li  x29, stride;  \\\n\
            li  x30, result; \\\n\
            vmv.v.x v8, x30; \\\n\
            VSET_VSEW \\\n\
            store_inst v8, (x%d), x29; "%n + "\\\n\
            load_inst v16, (x%d), x29 ; "%n + " \\\n\
        )",file=f)

    for n in range(1,31):
        if n == 12 or n == 20 or n == 24 or n == 31: # signature base registers
            continue
        print("#define TEST_VSSE_OP_rd%d( testnum, load_inst, store_inst, eew, result, stride, base )"%n + " \\\n\
        TEST_CASE_LOOP( testnum, v16,  \\\n\
            la  x1, base;  \\\n\
            li  x2, stride; \\\n\
            li  x3, result; \\\n\
            vmv.v.x v%d, x3;  "%n + "\\\n\
            VSET_VSEW \\\n\
            store_inst v%d, (x1), x2; "%n + " \\\n\
            load_inst v16, (x1), x2; \\\n\
        )",file=f)

    print("#define TEST_VSSE_OP_130( testnum, load_inst, store_inst, eew, result, stride, base ) \\\n\
        TEST_CASE_LOOP( testnum, v16,  \\\n\
            la  x30, base;  \\\n\
            li  x2, stride; \\\n\
            li  x3, result; \\\n\
            vmv.v.x v8, x3; \\\n\
            VSET_VSEW \\\n\
            store_inst v8, (x30), x2; \\\n\
            load_inst v16, (x30), x2 ;  \\\n\
        )",file=f)

    print("#define TEST_VSSE_OP_129( testnum, load_inst, store_inst, eew, result, stride, base ) \\\n\
        TEST_CASE_LOOP( testnum, v16,  \\\n\
            la  x29, base;  \\\n\
            li  x2, stride; \\\n\
            li  x3, result; \\\n\
            vmv.v.x v8, x3; \\\n\
            VSET_VSEW \\\n\
            store_inst v8, (x29), x2; \\\n\
            load_inst v16, (x29), x2 ;  \\\n\
        )",file=f)
    print("#define TEST_VSSE_OP_rd31( testnum, load_inst, store_inst, eew, result, stride, base ) \\\n\
        TEST_CASE_LOOP( testnum, v31,  \\\n\
            la  x1, base;  \\\n\
            li  x2, stride; \\\n\
            li  x3, result; \\\n\
            vmv.v.x v31, x3; \\\n\
            VSET_VSEW \\\n\
            store_inst v31, (x1), x2; \\\n\
            load_inst v1, (x1), x2;  \\\n\
        )",file=f)

def generate_macros_vsuxei(f):
    for n in range(1,30):
        if n == 12 or n == 20 or n == 24 or n == 30 or n == 31: # signature base registers
            continue
        print("#define TEST_VSXEI_OP_1%d( testnum, load_inst, store_inst, index_eew, result, base_data, base_index )"%n + " \\\n\
        TEST_CASE_LOOP( testnum, v16,  \\\n\
            la  x%d, base_data; "%n + " \\\n\
            la  x30, base_index; \\\n\
            MK_VLE_INST(index_eew) v24, (x30);    \\\n\
            li  x31, result; \\\n\
            vmv.v.x v8, x31; \\\n\
            store_inst v8, (x%d), v24;"%n + " \\\n\
            load_inst v16, (x%d), v24;"%n + " \\\n\
        )",file=f)

    for n in range(1,31):
        if n == 12 or n == 20 or n == 24 or n == 31: # signature base registers
            continue
        print("#define TEST_VSXEI_OP_rd%d( testnum, load_inst, store_inst, index_eew, result, base_data, base_index )"%n + " \\\n\
        TEST_CASE_LOOP( testnum, v16,  \\\n\
            la  x1, base_data;   \\\n\
            la  x6, base_index; \\\n\
            MK_VLE_INST(index_eew) v24, (x6);    \\\n\
            li  x3, result; \\\n\
            vmv.v.x v%d, x3; "%n + "\\\n\
            store_inst v%d, (x1), v24;"%n + " \\\n\
            load_inst v16, (x1), v24; \\\n\
        )",file=f)

    print("#define TEST_VSXEI_OP_130( testnum, load_inst, store_inst, index_eew, result, base_data, base_index ) \\\n\
        TEST_CASE_LOOP( testnum, v16,  \\\n\
            la  x30, base_data;  \\\n\
            la  x6, base_index; \\\n\
            MK_VLE_INST(index_eew) v24, (x6);    \\\n\
            li  x31, result; \\\n\
            vmv.v.x v8, x31; \\\n\
            store_inst v8, (x30), v24; \\\n\
            load_inst v16, (x30), v24; \\\n\
        )",file=f)
    print("#define TEST_VSXEI_OP_131( testnum, load_inst, store_inst, index_eew, result, base_data, base_index ) \\\n\
        TEST_CASE_LOOP( testnum, v16, \\\n\
            la  x31, base_data;  \\\n\
            la  x6, base_index; \\\n\
            MK_VLE_INST(index_eew) v24, (x6);    \\\n\
            li  x3, result; \\\n\
            vmv.v.x v8, x3; \\\n\
            store_inst v8, (x31), v24; \\\n\
            load_inst v16, (x31), v24; \\\n\
        )",file=f)
    print("#define TEST_VSXEI_OP_rd31( testnum, load_inst, store_inst, index_eew, result, base_data, base_index ) \\\n\
        TEST_CASE_LOOP( testnum, v31, \\\n\
            la  x1, base_data;   \\\n\
            la  x6, base_index; \\\n\
            MK_VLE_INST(index_eew) v2, (x6);    \\\n\
            li  x3, result; \\\n\
            vmv.v.x v31, x3; \\\n\
            store_inst v31, (x1), v2; \\\n\
            load_inst v14, (x1), v2; \\\n\
        )",file=f)

def generate_macros_vsseg(f, lmul, vsew, eew):
    emul = eew / vsew * lmul
    emul = 1 if emul < 1 else int(emul)
    lmul = 1 if lmul < 1 else int(lmul)
    generate_vsseg_macro(f,lmul)
    for n in range(1,30):
        if n == 12 or n == 20 or n == 24 or n == 30: # signature base registers
            continue
        print("#define TEST_VSSEG1_OP_1%d( testnum, load_inst, store_inst, eew, base, source_addr )"%n + " \\\n\
        TEST_CASE_LOOP( testnum, v16, \\\n\
            la  x%d, base; "%n + " \\\n\
            la  x2, source_addr; \\\n\
            vl8re32.v v8, (x2); \\\n\
            store_inst v8, (x%d); "%n + "\\\n\
            load_inst v16, (x%d); "%n + " \\\n\
        )",file=f)

    for n in range(1,31):
        if n != 8 and n != 16 and n != 24:
            continue
        print("#define TEST_VSSEG1_OP_rd%d( testnum, load_inst, store_inst, eew, base, source_addr )"%n + " \\\n\
        TEST_CASE_LOOP( testnum, v16,  \\\n\
            la  x1, base;  \\\n\
            la  x2, source_addr; \\\n\
            vl8re32.v v%d, (x2); "%n + "\\\n\
            store_inst v%d, (x1); "%n + " \\\n\
            load_inst v16, (x1); \\\n\
        )",file=f)

    print("#define TEST_VSSEG1_OP_130( testnum, load_inst, store_inst, eew, base, source_addr ) \\\n\
        TEST_CASE_LOOP( testnum, v16,  \\\n\
            la  x30, base;  \\\n\
            la  x2, source_addr; \\\n\
            vl8re32.v v8, (x2); \\\n\
            store_inst v8, (x30); \\\n\
            load_inst v16, (x30);  \\\n\
        )",file=f)

def generate_macros_vsuxseg(f, lmul, vsew, eew):
    emul = eew / vsew * lmul
    emul = 1 if emul < 1 else int(emul)
    lmul = 1 if lmul < 1 else int(lmul)
    generate_vsuxseg_macro(f,lmul)
    for n in range(1,30):
        if n == 12 or n == 20 or n == 24 or n == 30 or n == 31: # signature base registers
            continue
        print("#define TEST_VSXSEG1_OP_1%d( testnum, load_inst, store_inst, index_eew, base_data, base_index, source_addr )"%n + " \\\n\
        TEST_CASE_LOOP( testnum, v16,   \\\n\
            la  x%d, base_data; "%n + " \\\n\
            la  x30, base_index; \\\n\
            la  x3, source_addr; \\\n\
            vl8re32.v v8, (x3); \\\n\
            MK_VLE_INST(index_eew) v24, (x30);    \\\n\
            store_inst v8, (x%d), v24;"%n + " \\\n\
            load_inst v16, (x%d), v24;"%n + " \\\n\
        )",file=f)

    for n in range(1,31):
        if n != 8 and n != 16 and n != 24:
            continue
        print("#define TEST_VSXSEG1_OP_rd%d( testnum, load_inst, store_inst, index_eew, base_data, base_index, source_addr )"%n + " \\\n\
        TEST_CASE_LOOP( testnum, v16,   \\\n\
            la  x1, base_data;   \\\n\
            la  x6, base_index; \\\n\
            la  x3, source_addr; \\\n\
            vl8re32.v v%d, (x3);"%n + " \\\n\
            MK_VLE_INST(index_eew) v24, (x6);    \\\n\
            store_inst v%d, (x1), v24;"%n + " \\\n\
            load_inst v16, (x1), v24; \\\n\
        )",file=f)

    print("#define TEST_VSXSEG1_OP_130( testnum, load_inst, store_inst, index_eew, base_data, base_index, source_addr ) \\\n\
        TEST_CASE_LOOP( testnum, v16,  \\\n\
            la  x30, base_data;  \\\n\
            la  x6, base_index; \\\n\
            la  x3, source_addr; \\\n\
            vl8re32.v v8, (x3); \\\n\
            MK_VLE_INST(index_eew) v24, (x6);    \\\n\
            store_inst v8, (x30), v24; \\\n\
            load_inst v16, (x30), v24; \\\n\
        )",file=f)


def generate_macros_vssseg(f, lmul, vsew, eew):
    emul = eew / vsew * lmul
    emul = 1 if emul < 1 else int(emul)
    lmul = 1 if lmul < 1 else int(lmul)
    generate_vssseg_macro(f, lmul)
    for n in range(1,29):
        if n == 12 or n == 20 or n == 24 or n == 29 or n == 30: # signature base registers
            continue
        print("#define TEST_VSSSEG1_OP_1%d( testnum, load_inst, store_inst, eew, stride, base, source_addr  )"%n + " \\\n\
        TEST_CASE_LOOP( testnum, v16,   \\\n\
            la  x%d, base; "%n + " \\\n\
            li  x29, stride; \\\n\
            la  x3, source_addr; \\\n\
            vl8re32.v v8, (x3); \\\n\
            store_inst v8, (x%d), x29; "%n + "\\\n\
            load_inst v16, (x%d), x29; "%n + " \\\n\
        )",file=f)

    for n in range(1,31):
        if n != 8 and n != 16 and n != 24:
            continue
        print("#define TEST_VSSSEG1_OP_rd%d( testnum, load_inst, store_inst, eew, stride, base, source_addr  )"%n + " \\\n\
        TEST_CASE_LOOP( testnum, v16,  \\\n\
            la  x1, base;  \\\n\
            li  x2, stride; \\\n\
            la  x3, source_addr; \\\n\
            vl8re32.v v%d, (x3);"%n + " \\\n\
            store_inst v%d, (x1), x2; "%n + " \\\n\
            load_inst v16, (x1), x2; \\\n\
        )",file=f)

    print("#define TEST_VSSSEG1_OP_130( testnum, load_inst, store_inst, eew, stride, base, source_addr ) \\\n\
        TEST_CASE_LOOP( testnum, v16,  \\\n\
            la  x30, base;  \\\n\
            li  x2, stride; \\\n\
            la  x3, source_addr; \\\n\
            vl8re32.v v8, (x3); \\\n\
            store_inst v8, (x30), x2; \\\n\
            load_inst v16, (x30), x2;  \\\n\
        )",file=f)
    print("#define TEST_VSSSEG1_OP_129( testnum, load_inst, store_inst, eew, stride, base, source_addr ) \\\n\
        TEST_CASE_LOOP( testnum, v16,  \\\n\
            la  x29, base;  \\\n\
            li  x2, stride; \\\n\
            la  x3, source_addr; \\\n\
            vl8re32.v v8, (x3); \\\n\
            store_inst v8, (x29), x2; \\\n\
            load_inst v16, (x29), x2;  \\\n\
        )",file=f)


def generate_tests_vlre(f, vsew , eew, lmul):
    emul = eew / vsew * lmul
    if emul < 0.125 or emul > 8:
        return 0
    emul = 1 if emul < 1 else int(emul)
    n = 0
    instr1 = "vl1re%d"%(eew)
    instr2 = "vl2re%d"%(eew)
    instr4 = "vl4re%d"%(eew)
    instr8 = "vl8re%d"%(eew)
    print("  #-------------------------------------------------------------", file=f)
    print("  # VV Tests", file=f)
    print("  #-------------------------------------------------------------", file=f)

    for i in range(2):
        n += 1
        print("  TEST_VLRE1_OP( "+str(n)+",  %s.v, " %instr1+"0 + tdat"+" );", file=f)
        n += 1
        print("  TEST_VLRE2_OP( "+str(n)+",  %s.v, " %instr2+"16 + tdat"+" );", file=f)
        n += 1
        print("  TEST_VLRE4_OP( "+str(n)+",  %s.v, " %instr4+"-12 + tdat4"+" );", file=f)
        n += 1
        print("  TEST_VLRE8_OP( "+str(n)+",  %s.v, " %instr8+"0 + tdat5"+" );", file=f)
        n += 1
        print("  TEST_VLRE2_OP( "+str(n)+",  %s.v, " %instr2+"0 + tdat"+" );", file=f)
        n += 1
        print("  TEST_VLRE8_OP( "+str(n)+",  %s.v, " %instr8+"4096 + tdat5"+" );", file=f)

    return n


def generate_tests_vsre(f, vsew , lmul):
    n = 0
    
    list = [8, 16, 32, 64]
    load_ins_eew = 32
    for i in range(4):
        emul = list[i] / vsew * lmul
        if emul >= 0.125 and emul <= 8:
            load_ins_eew = list[i]
            break

    print("  #-------------------------------------------------------------", file=f)
    print("  # VV Tests", file=f)
    print("  #-------------------------------------------------------------", file=f)

    for i in range(2):
        n += 1
        print("  TEST_VSRE1_OP( "+str(n)+", vl1re%d.v, vs1r.v, "%load_ins_eew +"0 + tdat"+" , mask_data );", file=f)
        n += 1
        print("  TEST_VSRE2_OP( "+str(n)+", vl2re%d.v, vs2r.v, "%load_ins_eew +"16 + tdat"+" , mask_data );", file=f)
        n += 1
        print("  TEST_VSRE4_OP( "+str(n)+", vl4re%d.v, vs4r.v, "%load_ins_eew +"-12 + tdat4"+" , mask_data );", file=f)
        n += 1
        print("  TEST_VSRE8_OP( "+str(n)+", vl8re%d.v, vs8r.v, "%load_ins_eew +"0 + tdat5"+" , mask_data );", file=f)
        n += 1
        print("  TEST_VSRE8_OP( "+str(n)+", vl8re%d.v, vs8r.v, "%load_ins_eew +"4096 + tdat5"+" , mask_data );", file=f)

    return n














