import os
from scripts.test_common_info import get_aligned_reg


sreg = "x20" # signature register

def get_vset_eew_emul(eew, emul):
    emul_map = {0.125: "f8", 0.25: "f4", 0.5: "f2", 1: "1", 2: "2", 4: "4", 8: "8"}
    vset_string = "vsetvli x31, x0, e%d, m%s, tu, mu;"%(eew, emul_map[emul])
    return vset_string


def generate_macros_vle(f, lmul, vsew, eew):
    emul = eew / vsew * lmul
    if emul < 0.125 or emul > 8:
        print("emul is out of range!")
        return 0
    VSET_EEW_EMUL = get_vset_eew_emul(eew, emul)
    print("#define VSET_EEW_EMUL %s\n"%VSET_EEW_EMUL, file=f)
    
    print("#define TEST_VLE_OP( testnum, inst, base ) \\\n\
    TEST_CASE_LOOP_EEW( testnum, v16, \\\n\
        la  x7, base; \\\n\
        inst v16, (x7); \\\n\
    )", file=f)
    for n in range(1, 32):
        if n % emul != 0:
            continue
        print("#define TEST_VLE_OP_vd_%d( testnum, inst, base )"%n + " \\\n\
        TEST_CASE_LOOP_EEW( testnum, v%d, "%n + " \\\n\
            la  x8, base; \\\n\
            inst v%d, (x8); "%n + "\\\n\
        ) ", file=f)


def generate_tests_vle(f, rs1_val, rs2_val, lmul, vsew, eew):
    emul = eew / vsew * lmul
    if emul < 0.125 or emul > 8:
        return 0
    
    n = 0
    print("  #-------------------------------------------------------------", file=f)
    print("  # vle%d Tests"%eew, file=f)
    print("  #-------------------------------------------------------------", file=f)

    for i in range(2):
        n += 1
        print("  TEST_VLE_OP( "+str(n)+",  vle%d.v, " %(eew)+"0 + tdat"+" );", file=f)
        n += 1
        print("  TEST_VLE_OP( "+str(n)+",  vle%d.v, " %(eew)+"%d + tdat"%(eew//8)+" );", file=f)
        n += 1
        print("  TEST_VLE_OP( "+str(n)+",  vle%d.v, " %(eew)+"4096 + tdat"+" );", file=f)
        n += 1
        print("  TEST_VLE_OP( "+str(n)+",  vle%d.v, " %(eew)+"-4096 + tsdat9"+" );", file=f)
        
        n += 1
        print("  TEST_VLE_OP( "+str(n)+",  vle%dff.v, " %(eew)+"0 + tdat"+" );", file=f)
    
    for i in range(1, 32):     
        if i % emul != 0:
            continue
        n += 1
        print("  TEST_VLE_OP_vd_%d( "%i+str(n)+",  vle%d.v, "%(eew)+"0 + tdat"+" );", file=f)
        
    return n


def generate_macros_vse(f, lmul, vsew, eew):
    emul = eew / vsew * lmul
    if emul < 0.125 or emul > 8:
        print("emul is out of range!")
        return 0
    vlen = int(os.environ['RVV_ATG_VLEN'])
    xlen = int(os.environ['RVV_ATG_XLEN'])
    num_bytes = max(xlen // 8, emul * vlen // 8) # TODO
    
    print("#define TEST_VSE_OP( testnum, load_inst, store_inst, base, sig_basereg ) \\\n\
    TEST_CASE_FORMAT( testnum, \\\n\
        la  x7, base; \\\n\
        load_inst v8, (x7); \\\n\
        RVTEST_BASEUPD(sig_basereg); \\\n\
        store_inst v8, (sig_basereg); \\\n\
        addi sig_basereg, sig_basereg, %d;"%(num_bytes) + " \\\n\
    )", file=f)
    for n in range(1, 32):
        if n % emul != 0:
            continue
        print("#define TEST_VSE_OP_vs3_%d( testnum, load_inst, store_inst, base, sig_basereg )"%n + " \\\n\
        TEST_CASE_FORMAT( testnum, \\\n\
            la  x7, base;  \\\n\
            load_inst v%d, (x7); "%n + " \\\n\
            RVTEST_BASEUPD(sig_basereg); \\\n\
            store_inst v%d, (sig_basereg); "%n + " \\\n\
            addi sig_basereg, sig_basereg, %d;"%(num_bytes) + " \\\n\
        )",file=f)


def generate_tests_vse(f, rs1_val, rs2_val, lmul, vsew, eew):
    emul = eew / vsew * lmul
    if emul < 0.125 or emul > 8:
        return 0
    
    n = 0
    print("  #-------------------------------------------------------------", file=f)
    print("  # vse%d Tests"%eew, file=f)
    print("  #-------------------------------------------------------------", file=f)

    for i in range(2):
        n += 1
        print("  TEST_VSE_OP( "+str(n)+", vle%d.v, vse%d.v, "%(eew, eew)+"0 + tdat, "+"%s );"%sreg, file=f)
        n += 1
        print("  TEST_VSE_OP( "+str(n)+", vle%d.v, vse%d.v, "%(eew, eew)+"4096 + tdat, "+"%s );"%sreg, file=f)
    
    for i in range(1, 32):     
        if i % emul != 0:
            continue
        n += 1
        print("  TEST_VSE_OP_vs3_%d( "%i+str(n)+", vle%d.v, vse%d.v, "%(eew, eew)+"0 + tdat, "+"%s );"%sreg, file=f)
    
    return n


def generate_macros_vlse(f, lmul, vsew, eew):
    emul = eew / vsew * lmul
    if emul < 0.125 or emul > 8:
        print("emul is out of range!")
        return 0
    VSET_EEW_EMUL = get_vset_eew_emul(eew, emul)
    print("#define VSET_EEW_EMUL %s\n"%VSET_EEW_EMUL, file=f)
    
    print("#define TEST_VLSE_OP( testnum, inst, base, stride ) \\\n\
    TEST_CASE_LOOP_EEW( testnum, v16,  \\\n\
        la  x7, base; \\\n\
        li  x8, stride; \\\n\
        inst v16, (x7), x8; \\\n\
    )", file=f)
    for n in range(1, 32):
        if n % emul != 0:
            continue
        print("#define TEST_VLSE_OP_vd_%d( testnum, inst, base, stride )"%n + " \\\n\
        TEST_CASE_LOOP_EEW( testnum, v%d,  "%n + "\\\n\
            la  x7, base; \\\n\
            li  x8, stride; \\\n\
            inst v%d, (x7), x8; "%n + "\\\n\
        ) ", file=f)


def generate_tests_vlse(f, rs1_val, rs2_val, lmul, vsew, eew):
    emul = eew / vsew * lmul
    if emul < 0.125 or emul > 8:
        return 0
    
    n = 0
    print("  #-------------------------------------------------------------", file=f)
    print("  # vlse%d Tests"%eew, file=f)
    print("  #-------------------------------------------------------------", file=f)

    for i in range(2):
        n += 1
        print("  TEST_VLSE_OP( "+str(n)+",  vlse%d.v, "%(eew)+"0 + tdat, 0"+" );", file=f)
        n += 1
        print("  TEST_VLSE_OP( "+str(n)+",  vlse%d.v, "%(eew)+"0 + tdat, %d"%(eew//8)+" );", file=f)
        n += 1
        print("  TEST_VLSE_OP( "+str(n)+",  vlse%d.v, "%(eew)+"0 + tdat, 4096"+" );", file=f)
        n += 1
        print("  TEST_VLSE_OP( "+str(n)+",  vlse%d.v, "%(eew)+"0 + tsdat9, -4096"+" );", file=f)    
    
    for i in range(1, 32):     
        if i % emul != 0:
            continue
        n += 1
        print("  TEST_VLSE_OP_vd_%d( "%i+str(n)+",  vlse%d.v, "%(eew)+"0 + tdat, %d"%(eew//8)+" );", file=f)
    
    return n


def generate_macros_vsse(f, lmul, vsew, eew):
    emul = eew / vsew * lmul
    if emul < 0.125 or emul > 8:
        print("emul is out of range!")
        return 0
    VSET_EEW_EMUL = get_vset_eew_emul(eew, emul)
    print("#define VSET_EEW_EMUL %s\n"%VSET_EEW_EMUL, file=f)
    
    print("#define TEST_VSSE_OP( testnum, load_inst, store_inst, base, stride ) \\\n\
    TEST_CASE_LOOP_EEW( testnum, v16, \\\n\
        la  x7, base; \\\n\
        li  x8, stride; \\\n\
        load_inst v8, (x7), x8; \\\n\
        VSET_EEW_EMUL \\\n\
        vadd.vi v8, v8, 1; \\\n\
        VSET_VSEW_4AVL \\\n\
        store_inst v8, (x7), x8; \\\n\
        load_inst v16, (x7), x8; \\\n\
    )", file=f)
    for n in range(1, 32):
        if n % emul != 0:
            continue
        print("#define TEST_VSSE_OP_vs3_%d( testnum, load_inst, store_inst, base, stride )"%n + " \\\n\
        TEST_CASE_LOOP_EEW( testnum, v%d,  "%n + "\\\n\
            la  x7, base; \\\n\
            li  x8, stride; \\\n\
            load_inst v%d, (x7), x8; "%n + "\\\n\
            VSET_EEW_EMUL \\\n\
            vadd.vi v%d, v%d, 1; "%(n, n) + "\\\n\
            VSET_VSEW_4AVL \\\n\
            store_inst v%d, (x7), x8; "%n + "\\\n\
            load_inst v%d, (x7), x8; "%n + "\\\n\
        )", file=f)


def generate_tests_vsse(f, rs1_val, rs2_val, lmul, vsew, eew):
    emul = eew / vsew * lmul
    if emul < 0.125 or emul > 8:
        return 0
    
    n = 0
    print("  #-------------------------------------------------------------", file=f)
    print("  # vsse%d Tests"%eew, file=f)
    print("  #-------------------------------------------------------------", file=f)

    for i in range(2):
        n += 1
        print("  TEST_VSSE_OP( "+str(n)+", vlse%d.v, vsse%d.v, "%(eew, eew)+"0 + tdat, 0"+" );", file=f)
        n += 1
        print("  TEST_VSSE_OP( "+str(n)+", vlse%d.v, vsse%d.v, "%(eew, eew)+"0 + tdat, %d"%(eew//8)+" );", file=f)
        n += 1
        print("  TEST_VSSE_OP( "+str(n)+", vlse%d.v, vsse%d.v, "%(eew, eew)+"0 + tdat, 4096"+" );", file=f)
        n += 1
        print("  TEST_VSSE_OP( "+str(n)+", vlse%d.v, vsse%d.v, "%(eew, eew)+"0 + tsdat9, -4096"+" );", file=f)
    
    for i in range(1, 32):     
        if i % emul != 0:
            continue
        n += 1
        print("  TEST_VSSE_OP_vs3_%d( "%i+str(n)+", vlse%d.v, vsse%d.v, "%(eew, eew)+"0 + tdat, %d"%(eew//8)+" );", file=f)
    
    return n


def generate_macros_vlxei(f, lmul, vsew, eew):
    emul = eew / vsew * lmul
    if emul < 0.125 or emul > 8:
        print("emul is out of range!")
        return 0
    VSET_EEW_EMUL = get_vset_eew_emul(eew, emul)
    print("#define VSET_EEW_EMUL %s\n"%VSET_EEW_EMUL, file=f)
    
    print("#define TEST_VLXEI_OP( testnum, inst, index_eew, base_data, offset_base ) \\\n\
    TEST_CASE_LOOP( testnum, v16,  \\\n\
        VSET_VSEW_4AVL \\\n\
        la  x7, base_data; \\\n\
        la  x8, offset_base; \\\n\
        MK_VLE_INST(index_eew) v8, (x8); \\\n\
        inst v16, (x7), v8; \\\n\
    )", file=f)
    for n in range(1, 32):
        if n % lmul != 0:
            continue
        vs2 = get_aligned_reg(n, lmul, emul)
        if vs2 == 0:
            continue
        print("#define TEST_VLXEI_OP_vd_%d( testnum, inst, index_eew, base, offset_base )"%n + " \\\n\
        TEST_CASE_LOOP( testnum, v%d, "%n + "\\\n\
            VSET_VSEW_4AVL \\\n\
            la  x7, base; \\\n\
            la  x8, offset_base; \\\n\
            MK_VLE_INST(index_eew) v%d, (x8); "%(vs2) + "\\\n\
            inst v%d, (x7), v%d; "%(n, vs2) + "\\\n\
        ) ", file=f)
    for n in range(1, 32):
        if n % emul != 0:
            continue
        vd = get_aligned_reg(n, emul, lmul)
        if vd == 0:
            continue
        print("#define TEST_VLXEI_OP_vs2_%d( testnum, inst, index_eew, base, offset_base )"%n + " \\\n\
        TEST_CASE_LOOP( testnum, v%d, "%vd + "\\\n\
            VSET_VSEW_4AVL \\\n\
            la  x7, base; \\\n\
            la  x8, offset_base; \\\n\
            MK_VLE_INST(index_eew) v%d, (x8); "%(n) + "\\\n\
            inst v%d, (x7), v%d; "%(vd, n) + "\\\n\
        ) ", file=f)


def generate_tests_vlxei(f, instr, rs1_val, rs2_val, lmul, vsew, eew):
    emul = eew / vsew * lmul
    if emul < 0.125 or emul > 8:
        return 0
    
    n = 0
    print("  #-------------------------------------------------------------", file=f)
    print("  # %s Tests"%instr, file=f)
    print("  #-------------------------------------------------------------", file=f)

    for i in range(2):
        n += 1
        print("  TEST_VLXEI_OP( "+str(n)+",  %s.v, %d, "%(instr, eew)+"0 + tdat"+", "+"idx%ddat"%eew+" );", file=f)
        n += 1
        print("  TEST_VLXEI_OP( "+str(n)+",  %s.v, %d, "%(instr, eew)+"%d + tdat"%(vsew//8)+", "+"idx%ddat"%eew+" );", file=f)
        n += 1
        print("  TEST_VLXEI_OP( "+str(n)+",  %s.v, %d, "%(instr, eew)+"4096 + tdat"+", "+"idx%ddat"%eew+" );", file=f)
        n += 1
        print("  TEST_VLXEI_OP( "+str(n)+",  %s.v, %d, "%(instr, eew)+"-4096 + tsdat9"+", "+"idx%ddat"%eew+" );", file=f)
    
    for i in range(1, 32):     
        if i % lmul != 0 or get_aligned_reg(i, lmul, emul) == 0:
            continue
        n += 1
        print("  TEST_VLXEI_OP_vd_%d( "%i+str(n)+",  %s.v, %d, "%(instr, eew)+"%d + tdat"%(vsew//8)+", "+"idx%ddat"%eew+" );", file=f)
    
    for i in range(1, 32):     
        if i % emul != 0 or get_aligned_reg(i, emul, lmul) == 0:
            continue
        n += 1
        print("  TEST_VLXEI_OP_vs2_%d( "%i+str(n)+",  %s.v, %d, "%(instr, eew)+"0 + tsdat1"+", "+"idx%ddat"%eew+" );", file=f)
    
    return n


def generate_macros_vsxei(f, lmul, vsew, eew):
    emul = eew / vsew * lmul
    if emul < 0.125 or emul > 8:
        print("emul is out of range!")
        return 0
    VSET_EEW_EMUL = get_vset_eew_emul(eew, emul)
    print("#define VSET_EEW_EMUL %s\n"%VSET_EEW_EMUL, file=f)
    
    print("#define TEST_VSXEI_OP( testnum, load_inst, store_inst, index_eew, base, offset_base ) \\\n\
    TEST_CASE_LOOP( testnum, v24, \\\n\
        VSET_VSEW_4AVL \\\n\
        la  x7, base; \\\n\
        la  x8, offset_base; \\\n\
        MK_VLE_INST(index_eew) v8, (x8); \\\n\
        load_inst v16, (x7), v8; \\\n\
        vadd.vi v16, v16, 1; \\\n\
        store_inst v16, (x7), v8; \\\n\
        load_inst v24, (x7), v8; \\\n\
    )", file=f)
    for n in range(1, 32):
        if n % lmul != 0:
            continue
        vs2 = get_aligned_reg(n, lmul, emul)
        if vs2 == 0:
            continue
        print("#define TEST_VSXEI_OP_vs3_%d( testnum, load_inst, store_inst, index_eew, base, offset_base )"%n + " \\\n\
        TEST_CASE_LOOP( testnum, v%d, "%n + "\\\n\
            VSET_VSEW_4AVL \\\n\
            la  x7, base; \\\n\
            la  x8, offset_base; \\\n\
            MK_VLE_INST(index_eew) v%d, (x8); "%(vs2) + "\\\n\
            load_inst v%d, (x7), v%d; "%(n, vs2) + "\\\n\
            vadd.vi v%d, v%d, 1; "%(n, n) + "\\\n\
            store_inst v%d, (x7), v%d; "%(n, vs2) + "\\\n\
            load_inst v%d, (x7), v%d; "%(n, vs2) + "\\\n\
        )",file=f)
    for n in range(1, 32):
        if n % emul != 0:
            continue
        vs3 = get_aligned_reg(n, emul, lmul)
        if vs3 == 0:
            continue
        print("#define TEST_VSXEI_OP_vs2_%d( testnum, load_inst, store_inst, index_eew, base, offset_base )"%n + " \\\n\
        TEST_CASE_LOOP( testnum, v%d, "%vs3 + "\\\n\
            VSET_VSEW_4AVL \\\n\
            la  x7, base; \\\n\
            la  x8, offset_base; \\\n\
            MK_VLE_INST(index_eew) v%d, (x8); "%(n) + "\\\n\
            load_inst v%d, (x7), v%d; "%(vs3, n) + "\\\n\
            vadd.vi v%d, v%d, 1; "%(vs3, vs3) + "\\\n\
            store_inst v%d, (x7), v%d; "%(vs3, n) + "\\\n\
            load_inst v%d, (x7), v%d; "%(vs3, n) + "\\\n\
        ) ", file=f)


def generate_tests_vsxei(f, instr, instr_l, rs1_val, rs2_val, lmul, vsew, eew):
    emul = eew / vsew * lmul
    if emul < 0.125 or emul > 8:
        return 0
    
    n = 0
    print("  #-------------------------------------------------------------", file=f)
    print("  # %s Tests"%instr, file=f)
    print("  #-------------------------------------------------------------", file=f)

    for i in range(2):
        n += 1
        print("  TEST_VSXEI_OP( "+str(n)+", %s.v, %s.v, %d, "%(instr_l, instr, eew)+"0 + tdat"+", "+"idx%ddat"%eew+" );", file=f)
        n += 1
        print("  TEST_VSXEI_OP( "+str(n)+", %s.v, %s.v, %d, "%(instr_l, instr, eew)+"%d + tdat"%(vsew//8)+", "+"idx%ddat"%eew+" );", file=f)
        n += 1
        print("  TEST_VSXEI_OP( "+str(n)+", %s.v, %s.v, %d, "%(instr_l, instr, eew)+"4096 + tdat"+", "+"idx%ddat"%eew+" );", file=f)
        n += 1
        print("  TEST_VSXEI_OP( "+str(n)+", %s.v, %s.v, %d, "%(instr_l, instr, eew)+"-4096 + tsdat9"+", "+"idx%ddat"%eew+" );", file=f)
    
    for i in range(1, 32):     
        if i % lmul != 0 or get_aligned_reg(i, lmul, emul) == 0:
            continue
        n += 1
        print("  TEST_VSXEI_OP_vs3_%d( "%i+str(n)+",  %s.v, %s.v, %d, "%(instr_l, instr, eew)+"%d + tdat"%(vsew//8)+", "+"idx%ddat"%eew+" );", file=f)
    
    for i in range(1, 32):     
        if i % emul != 0 or get_aligned_reg(i, emul, lmul) == 0:
            continue
        n += 1
        print("  TEST_VSXEI_OP_vs2_%d( "%i+str(n)+",  %s.v, %s.v, %d, "%(instr_l, instr, eew)+"0 + tsdat1"+", "+"idx%ddat"%eew+" );", file=f)
    
    return n


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














