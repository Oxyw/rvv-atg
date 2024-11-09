import os
from scripts.test_common_info import get_aligned_reg, is_aligned


sreg = "x20" # signature register

def align_up(num_bytes):
    xlen = int(os.environ['RVV_ATG_XLEN'])
    mem_align = xlen // 8
    return (num_bytes + mem_align - 1) // mem_align * mem_align

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
    # TODO
    num_bytes = emul * vlen // 8
    num_bytes = align_up(num_bytes)
    
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
    vlen = int(os.environ['RVV_ATG_VLEN'])
    # TODO
    num_bytes = emul * vlen // 8
    num_bytes = align_up(num_bytes)
    
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
    
    return (n, num_bytes * n)


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


def generate_macros_vlseg(f, lmul, vsew, eew):
    emul = eew / vsew * lmul
    if emul < 0.125 or emul > 8:
        print("emul is out of range!")
        return 0
    emul_1 = max(1, emul) # (nf * emul) <= (NVPR / 4) &&  (insn.rd() + nf * emul) <= NVPR
    VSET_EEW_EMUL = get_vset_eew_emul(eew, emul)
    print("#define VSET_EEW_EMUL %s\n"%VSET_EEW_EMUL, file=f)
    
    for nf in range(2, 9):
        if emul_1 * nf > 8: # out of range
            break
        
        print("#define TEST_VLSEG%d_OP( testnum, inst, base )"%nf + " \\\n\
        TEST_CASE_LOOP_EEW( testnum, v8,   \\\n\
            la  x7, base; \\\n\
            inst v8, (x7); \\\n\
        )\\", file=f)
        for i in range(1, nf):
            print("    TEST_CASE_LOOP_CONTINUE( testnum, v%d) %s"%(8+emul_1*i, "\n" if i + 1 == nf else "\\"), file=f)
        
        for n in range(1, 32):
            if n % emul != 0:
                continue
            if n + emul_1*nf > 32:
                break
            print("#define TEST_VLSEG%d_OP_vd_%d( testnum, inst, base )"%(nf, n) + " \\\n\
            TEST_CASE_LOOP_EEW( testnum, v%d,  "%n + "\\\n\
                la  x7, base; \\\n\
                inst v%d, (x7); "%n + "\\\n\
            )\\", file=f)
            for i in range(1, nf):
                print("    TEST_CASE_LOOP_CONTINUE( testnum, v%d) %s"%(n+emul_1*i, "\n" if i + 1 == nf else "\\"), file=f)


def generate_tests_vlseg(f, rs1_val, rs2_val, lmul, vsew, eew):
    emul = eew / vsew * lmul
    if emul < 0.125 or emul > 8:
        return 0
    emul_1 = max(1, emul)
    
    n = 0
    rnd = 0
    print("  #-------------------------------------------------------------", file=f)
    print("  # vlseg<nf>e%d Tests"%eew, file=f)
    print("  #-------------------------------------------------------------", file=f)
    
    for i in range(2):
        for nf in range(2, 9):
            if emul_1 * nf > 8: # out of range
                break
            instr = "vlseg%de%d"%(nf, eew)
            n += 1
            print("  TEST_VLSEG%d_OP( "%nf+str(n)+",  %s.v, " %(instr)+"0 + tdat"+" );", file=f)
            rnd += nf
            n += 1
            print("  TEST_VLSEG%d_OP( "%nf+str(n)+",  %s.v, " %(instr)+"%d + tdat10"%(eew//8)+" );", file=f)
            rnd += nf
            n += 1
            print("  TEST_VLSEG%d_OP( "%nf+str(n)+",  %s.v, " %(instr)+"-64 + tsdat9"+" );", file=f)
            rnd += nf
            
            n += 1
            print("  TEST_VLSEG%d_OP( "%nf+str(n)+",  %sff.v, " %(instr)+"0 + tdat"+" );", file=f)
            rnd += nf
    
    for nf in range(2, 9):
        if emul_1 * nf > 8:
            break
        instr = "vlseg%de%d"%(nf, eew)
        for i in range(1, 32):
            if i % emul != 0:
                continue
            if i + emul_1*nf > 32:
                break
            n += 1
            print("  TEST_VLSEG%d_OP_vd_%d( "%(nf, i)+str(n)+",  %s.v, " %(instr)+"0 + tdat"+" );", file=f)
            rnd += nf
    
    return (n, rnd)


def generate_macros_vsseg(f, lmul, vsew, eew):
    emul = eew / vsew * lmul
    if emul < 0.125 or emul > 8:
        print("emul is out of range!")
        return 0
    vlen = int(os.environ['RVV_ATG_VLEN'])
    
    # (nf * emul) <= (NVPR / 4) &&  (insn.rd() + nf * emul) <= NVPR
    emul_1 = max(1, emul)
    for nf in range(2, 9):
        if emul_1 * nf > 8: # out of range
            break
        # TODO
        num_bytes = nf * emul * vlen // 8
        num_bytes = align_up(num_bytes)
        
        print("#define TEST_VSSEG%d_OP( testnum, load_inst, store_inst, base, sig_basereg )"%nf + " \\\n\
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
            if n + emul_1*nf > 32:
                break
            print("#define TEST_VSSEG%d_OP_vs3_%d( testnum, load_inst, store_inst, base, sig_basereg )"%(nf, n) + " \\\n\
            TEST_CASE_FORMAT( testnum, \\\n\
                la  x7, base; \\\n\
                load_inst v%d, (x7); "%n + "\\\n\
                RVTEST_BASEUPD(sig_basereg); \\\n\
                store_inst v%d, (sig_basereg); "%n + "\\\n\
                addi sig_basereg, sig_basereg, %d;"%(num_bytes) + " \\\n\
            )", file=f)


def generate_tests_vsseg(f, rs1_val, rs2_val, lmul, vsew, eew):
    emul = eew / vsew * lmul
    if emul < 0.125 or emul > 8:
        return 0
    emul_1 = max(1, emul)
    vlen = int(os.environ['RVV_ATG_VLEN'])
    
    n = 0
    footprint = 0
    print("  #-------------------------------------------------------------", file=f)
    print("  # vsseg<nf>e%d Tests"%eew, file=f)
    print("  #-------------------------------------------------------------", file=f)
    
    for i in range(2):
        for nf in range(2, 9):
            if emul_1 * nf > 8: # out of range
                break
            # TODO
            num_bytes = nf * emul * vlen // 8
            num_bytes = align_up(num_bytes)
            instr_l = "vlseg%de%d"%(nf, eew)
            instr = "vsseg%de%d"%(nf, eew)
            n += 1
            print("  TEST_VSSEG%d_OP( "%nf+str(n)+",  %s.v, %s.v, "%(instr_l, instr)+"0 + tdat, "+"%s );"%sreg, file=f)
            footprint += num_bytes
            n += 1
            print("  TEST_VSSEG%d_OP( "%nf+str(n)+",  %s.v, %s.v, "%(instr_l, instr)+"%d + tdat10, "%(eew//8)+"%s );"%sreg, file=f)
            footprint += num_bytes
            n += 1
            print("  TEST_VSSEG%d_OP( "%nf+str(n)+",  %s.v, %s.v, "%(instr_l, instr)+"-64 + tsdat9, "+"%s );"%sreg, file=f)
            footprint += num_bytes
    
    for nf in range(2, 9):
        if emul_1 * nf > 8:
            break
        # TODO
        num_bytes = nf * emul * vlen // 8
        num_bytes = align_up(num_bytes)
        instr_l = "vlseg%de%d"%(nf, eew)
        instr = "vsseg%de%d"%(nf, eew)
        for i in range(1, 32):
            if i % emul != 0:
                continue
            if i + emul_1*nf > 32:
                break
            n += 1
            print("  TEST_VSSEG%d_OP_vs3_%d( "%(nf, i)+str(n)+",  %s.v, %s.v, "%(instr_l, instr)+"0 + tdat, "+"%s );"%sreg, file=f)
            footprint += num_bytes
    
    return (n, footprint)


def generate_macros_vlsseg(f, lmul, vsew, eew):
    emul = eew / vsew * lmul
    if emul < 0.125 or emul > 8:
        print("emul is out of range!")
        return 0
    emul_1 = max(1, emul) # (nf * emul) <= (NVPR / 4) &&  (insn.rd() + nf * emul) <= NVPR
    VSET_EEW_EMUL = get_vset_eew_emul(eew, emul)
    print("#define VSET_EEW_EMUL %s\n"%VSET_EEW_EMUL, file=f)
    
    for nf in range(2, 9):
        if emul_1 * nf > 8: # out of range
            break
        
        print("#define TEST_VLSSEG%d_OP( testnum, inst, base, stride )"%nf + " \\\n\
        TEST_CASE_LOOP_EEW( testnum, v8,   \\\n\
            la  x7, base; \\\n\
            li  x8, stride; \\\n\
            inst v8, (x7), x8; \\\n\
        )\\", file=f)
        for i in range(1, nf):
            print("    TEST_CASE_LOOP_CONTINUE( testnum, v%d) %s"%(8+emul_1*i, "\n" if i + 1 == nf else "\\"), file=f)
        
        for n in range(1, 32):
            if n % emul != 0:
                continue
            if n + emul_1*nf > 32:
                break
            print("#define TEST_VLSSEG%d_OP_vd_%d( testnum, inst, base, stride )"%(nf, n) + " \\\n\
            TEST_CASE_LOOP_EEW( testnum, v%d,  "%n + "\\\n\
                la  x7, base; \\\n\
                li  x8, stride; \\\n\
                inst v%d, (x7), x8; "%n + "\\\n\
            )\\", file=f)
            for i in range(1, nf):
                print("    TEST_CASE_LOOP_CONTINUE( testnum, v%d) %s"%(n+emul_1*i, "\n" if i + 1 == nf else "\\"), file=f)


def generate_tests_vlsseg(f, rs1_val, rs2_val, lmul, vsew, eew):
    emul = eew / vsew * lmul
    if emul < 0.125 or emul > 8:
        return 0
    emul_1 = max(1, emul)
    
    n = 0
    rnd = 0
    print("  #-------------------------------------------------------------", file=f)
    print("  # vlsseg<nf>e%d Tests"%eew, file=f)
    print("  #-------------------------------------------------------------", file=f)
    
    for i in range(2):
        for nf in range(2, 9):
            if emul_1 * nf > 8: # out of range
                break
            instr = "vlsseg%de%d"%(nf, eew)
            n += 1
            print("  TEST_VLSSEG%d_OP( "%nf+str(n)+",  %s.v, " %(instr)+"0 + tdat, 0"+" );", file=f)
            rnd += nf
            n += 1
            print("  TEST_VLSSEG%d_OP( "%nf+str(n)+",  %s.v, " %(instr)+"0 + tdat10, %d"%(eew//8)+" );", file=f)
            rnd += nf
            n += 1
            print("  TEST_VLSSEG%d_OP( "%nf+str(n)+",  %s.v, " %(instr)+"0 + tsdat9, -128"+" );", file=f)
            rnd += nf
    
    for nf in range(2, 9):
        if emul_1 * nf > 8:
            break
        instr = "vlsseg%de%d"%(nf, eew)
        for i in range(1, 32):
            if i % emul != 0:
                continue
            if i + emul_1*nf > 32:
                break
            n += 1
            print("  TEST_VLSSEG%d_OP_vd_%d( "%(nf, i)+str(n)+",  %s.v, " %(instr)+"0 + tdat, %d"%(eew//8)+" );", file=f)
            rnd += nf
    
    return (n, rnd)


def generate_macros_vssseg(f, lmul, vsew, eew):
    emul = eew / vsew * lmul
    if emul < 0.125 or emul > 8:
        print("emul is out of range!")
        return 0
    emul_1 = max(1, emul) # (nf * emul) <= (NVPR / 4) &&  (insn.rd() + nf * emul) <= NVPR
    VSET_EEW_EMUL = get_vset_eew_emul(eew, emul)
    print("#define VSET_EEW_EMUL %s\n"%VSET_EEW_EMUL, file=f)
    
    for nf in range(2, 9):
        if emul_1 * nf > 8: # out of range
            break
        
        print("#define TEST_VSSSEG%d_OP( testnum, load_inst, store_inst, base, stride )"%nf + " \\\n\
        TEST_CASE_LOOP_EEW( testnum, v16,   \\\n\
            la  x7, base; \\\n\
            li  x8, stride; \\\n\
            load_inst v8, (x7), x8; \\\n\
            VSET_EEW_EMUL \\\n\
            vadd.vi v8, v8, 1; \\\n\
            VSET_VSEW_4AVL \\\n\
            store_inst v8, (x7), x8; \\\n\
            load_inst v16, (x7), x8; \\\n\
        )\\", file=f)
        for i in range(1, nf):
            print("    TEST_CASE_LOOP_CONTINUE( testnum, v%d) %s"%(16+emul_1*i, "\n" if i + 1 == nf else "\\"), file=f)
        
        for n in range(1, 32):
            if n % emul != 0:
                continue
            if n + emul_1*nf > 32:
                break
            print("#define TEST_VSSSEG%d_OP_vs3_%d( testnum, load_inst, store_inst, base, stride )"%(nf, n) + " \\\n\
            TEST_CASE_LOOP_EEW( testnum, v%d,  "%n + "\\\n\
                la  x7, base; \\\n\
                li  x8, stride; \\\n\
                load_inst v%d, (x7), x8; "%n + "\\\n\
                VSET_EEW_EMUL \\\n\
                vadd.vi v%d, v%d, 1; "%(n, n) + "\\\n\
                VSET_VSEW_4AVL \\\n\
                store_inst v%d, (x7), x8; "%n + "\\\n\
                load_inst v%d, (x7), x8; "%n + "\\\n\
            )\\", file=f)
            for i in range(1, nf):
                print("    TEST_CASE_LOOP_CONTINUE( testnum, v%d) %s"%(n+emul_1*i, "\n" if i + 1 == nf else "\\"), file=f)


def generate_tests_vssseg(f, rs1_val, rs2_val, lmul, vsew, eew):
    emul = eew / vsew * lmul
    if emul < 0.125 or emul > 8:
        return 0
    emul_1 = max(1, emul)
    
    n = 0
    rnd = 0
    print("  #-------------------------------------------------------------", file=f)
    print("  # vssseg<nf>e%d Tests"%eew, file=f)
    print("  #-------------------------------------------------------------", file=f)
    
    for i in range(2):
        for nf in range(2, 9):
            if emul_1 * nf > 8: # out of range
                break
            instr_l = "vlsseg%de%d"%(nf, eew)
            instr = "vssseg%de%d"%(nf, eew)
            n += 1
            print("  TEST_VSSSEG%d_OP( "%nf+str(n)+",  %s.v, %s.v, "%(instr_l, instr)+"0 + tdat, 0"+" );", file=f)
            rnd += nf
            n += 1
            print("  TEST_VSSSEG%d_OP( "%nf+str(n)+",  %s.v, %s.v, "%(instr_l, instr)+"0 + tdat10, %d"%(eew//8)+" );", file=f)
            rnd += nf
            n += 1
            print("  TEST_VSSSEG%d_OP( "%nf+str(n)+",  %s.v, %s.v, "%(instr_l, instr)+"0 + tsdat9, -128"+" );", file=f)
            rnd += nf
    
    for nf in range(2, 9):
        if emul_1 * nf > 8:
            break
        instr_l = "vlsseg%de%d"%(nf, eew)
        instr = "vssseg%de%d"%(nf, eew)
        for i in range(1, 32):
            if i % emul != 0:
                continue
            if i + emul_1*nf > 32:
                break
            n += 1
            print("  TEST_VSSSEG%d_OP_vs3_%d( "%(nf, i)+str(n)+",  %s.v, %s.v, "%(instr_l, instr)+"0 + tdat, %d"%(eew//8)+" );", file=f)
            rnd += nf
    
    return (n, rnd)


def generate_macros_vlxsegei(f, lmul, vsew, eew):
    emul = eew / vsew * lmul
    if emul < 0.125 or emul > 8:
        print("emul is out of range!")
        return 0
    emul_1 = max(1, emul)
    lmul_1 = max(1, lmul) # (nf * flmul) <= (NVPR / 4) &&  (insn.rd() + nf * flmul) <= NVPR
    VSET_EEW_EMUL = get_vset_eew_emul(eew, emul)
    print("#define VSET_EEW_EMUL %s\n"%VSET_EEW_EMUL, file=f)
    
    for nf in range(2, 9):
        if lmul_1 * nf > 8: # out of range
            break
        
        if 8 + emul_1*nf <= 24:
            print("#define TEST_VLXSEG%d_OP( testnum, inst, index_eew, base, offset_base )"%nf + " \\\n\
            TEST_CASE_LOOP( testnum, v24,   \\\n\
                VSET_VSEW_4AVL \\\n\
                la  x7, base; \\\n\
                la  x8, offset_base; \\\n\
                MK_VLE_INST(index_eew) v8, (x8); \\\n\
                inst v24, (x7), v8; \\\n\
            )\\", file=f)
            for i in range(1, nf):
                print("    TEST_CASE_LOOP_CONTINUE( testnum, v%d) %s"%(24+lmul_1*i, "\n" if i + 1 == nf else "\\"), file=f)
        
        for n in range(1, 32):
            if n % lmul != 0:
                continue
            if n + lmul_1*nf > 32:
                break
            vs2 = get_aligned_reg(n, lmul, emul, nf)
            if vs2 == 0:
                continue
            print("#define TEST_VLXSEG%d_OP_vd_%d( testnum, inst, index_eew, base, offset_base )"%(nf, n) + " \\\n\
            TEST_CASE_LOOP( testnum, v%d,  "%n + "\\\n\
                VSET_VSEW_4AVL \\\n\
                la  x7, base; \\\n\
                la  x8, offset_base; \\\n\
                MK_VLE_INST(index_eew) v%d, (x8); "%(vs2) + "\\\n\
                inst v%d, (x7), v%d; "%(n, vs2) + "\\\n\
            )\\", file=f)
            for i in range(1, nf):
                print("    TEST_CASE_LOOP_CONTINUE( testnum, v%d) %s"%(n+lmul_1*i, "\n" if i + 1 == nf else "\\"), file=f)
        
        for n in range(1, 32):
            if n % emul != 0:
                continue
            if n + emul_1*nf > 32:
                break
            vd = get_aligned_reg(n, emul, lmul, nf)
            if vd == 0:
                continue
            print("#define TEST_VLXSEG%d_OP_vs2_%d( testnum, inst, index_eew, base, offset_base )"%(nf, n) + " \\\n\
            TEST_CASE_LOOP( testnum, v%d,  "%vd + "\\\n\
                VSET_VSEW_4AVL \\\n\
                la  x7, base; \\\n\
                la  x8, offset_base; \\\n\
                MK_VLE_INST(index_eew) v%d, (x8); "%(n) + "\\\n\
                inst v%d, (x7), v%d; "%(vd, n) + "\\\n\
            )\\", file=f)
            for i in range(1, nf):
                print("    TEST_CASE_LOOP_CONTINUE( testnum, v%d) %s"%(vd+lmul_1*i, "\n" if i + 1 == nf else "\\"), file=f)


def generate_tests_vlxsegei(f, name, rs1_val, rs2_val, lmul, vsew, eew):
    emul = eew / vsew * lmul
    if emul < 0.125 or emul > 8:
        return 0
    emul_1 = max(1, emul)
    lmul_1 = max(1, lmul) # (nf * flmul) <= (NVPR / 4) &&  (insn.rd() + nf * flmul) <= NVPR
    
    n = 0
    rnd = 0
    print("  #-------------------------------------------------------------", file=f)
    print("  # %s<nf>ei%d Tests"%(name, eew), file=f)
    print("  #-------------------------------------------------------------", file=f)
    
    for i in range(2):
        for nf in range(2, 9):
            if lmul_1 * nf > 8 or 8 + emul_1*nf > 24: # out of range
                break
            instr = "%s%dei%d"%(name, nf, eew)
            n += 1
            print("  TEST_VLXSEG%d_OP( "%nf+str(n)+",  %s.v, %d, "%(instr, eew)+"0 + tdat, "+"idx%ddat"%eew+" );", file=f)
            rnd += nf
            n += 1
            print("  TEST_VLXSEG%d_OP( "%nf+str(n)+",  %s.v, %d, "%(instr, eew)+"%d + tdat10, "%(vsew//8)+"idx%ddat"%eew+" );", file=f)
            rnd += nf
            n += 1
            print("  TEST_VLXSEG%d_OP( "%nf+str(n)+",  %s.v, %d, "%(instr, eew)+"-4096 + tsdat9, "+"idx%ddat"%eew+" );", file=f)
            rnd += nf
    
    for nf in range(2, 9):
        if lmul_1 * nf > 8:
            break
        instr = "%s%dei%d"%(name, nf, eew)
        for i in range(1, 32):
            if i % lmul != 0:
                continue
            if i + lmul_1*nf > 32:
                break
            if get_aligned_reg(i, lmul, emul, nf) == 0:
                continue
            n += 1
            print("  TEST_VLXSEG%d_OP_vd_%d( "%(nf, i)+str(n)+",  %s.v, %d, "%(instr, eew)+"%d + tdat, "%(vsew//8)+"idx%ddat"%eew+" );", file=f)
            rnd += nf
        for i in range(1, 32):
            if i % emul != 0:
                continue
            if i + emul_1*nf > 32:
                break
            if get_aligned_reg(i, emul, lmul, nf) == 0:
                continue
            n += 1
            print("  TEST_VLXSEG%d_OP_vs2_%d( "%(nf, i)+str(n)+",  %s.v, %d, "%(instr, eew)+"%d + tdat, "%(vsew//8)+"idx%ddat"%eew+" );", file=f)
            rnd += nf
    
    return (n, rnd)


def generate_macros_vsxsegei(f, lmul, vsew, eew):
    emul = eew / vsew * lmul
    if emul < 0.125 or emul > 8:
        print("emul is out of range!")
        return 0
    emul_1 = max(1, emul)
    lmul_1 = max(1, lmul) # (nf * flmul) <= (NVPR / 4) &&  (insn.rd() + nf * flmul) <= NVPR
    VSET_EEW_EMUL = get_vset_eew_emul(eew, emul)
    print("#define VSET_EEW_EMUL %s\n"%VSET_EEW_EMUL, file=f)
    
    for nf in range(2, 9):
        if lmul_1 * nf > 8: # out of range
            break
        
        if 8 + emul_1*nf <= 16:
            print("#define TEST_VSXSEG%d_OP( testnum, load_inst, store_inst, index_eew, base, offset_base )"%nf + " \\\n\
            TEST_CASE_LOOP( testnum, v24,   \\\n\
                VSET_VSEW_4AVL \\\n\
                la  x7, base; \\\n\
                la  x8, offset_base; \\\n\
                MK_VLE_INST(index_eew) v8, (x8); \\\n\
                load_inst v16, (x7), v8; \\\n\
                vadd.vi v16, v16, 1; \\\n\
                store_inst v16, (x7), v8; \\\n\
                load_inst v24, (x7), v8; \\\n\
            )\\", file=f)
            for i in range(1, nf):
                print("    TEST_CASE_LOOP_CONTINUE( testnum, v%d) %s"%(24+lmul_1*i, "\n" if i + 1 == nf else "\\"), file=f)
        
        for n in range(1, 32):
            if n % lmul != 0:
                continue
            if n + lmul_1*nf > 32:
                break
            vs2 = get_aligned_reg(n, lmul, emul, nf)
            if vs2 == 0:
                continue
            print("#define TEST_VSXSEG%d_OP_vs3_%d( testnum, load_inst, store_inst, index_eew, base, offset_base )"%(nf, n) + " \\\n\
            TEST_CASE_LOOP( testnum, v%d,  "%n + "\\\n\
                VSET_VSEW_4AVL \\\n\
                la  x7, base; \\\n\
                la  x8, offset_base; \\\n\
                MK_VLE_INST(index_eew) v%d, (x8); "%(vs2) + "\\\n\
                load_inst v%d, (x7), v%d; "%(n, vs2) + "\\\n\
                vadd.vi v%d, v%d, 1; "%(n, n) + "\\\n\
                store_inst v%d, (x7), v%d; "%(n, vs2) + "\\\n\
                load_inst v%d, (x7), v%d; "%(n, vs2) + "\\\n\
            )\\", file=f)
            for i in range(1, nf):
                print("    TEST_CASE_LOOP_CONTINUE( testnum, v%d) %s"%(n+lmul_1*i, "\n" if i + 1 == nf else "\\"), file=f)
        
        for n in range(1, 32):
            if n % emul != 0:
                continue
            if n + emul_1*nf > 32:
                break
            vs3 = get_aligned_reg(n, emul, lmul, nf)
            if vs3 == 0:
                continue
            print("#define TEST_VSXSEG%d_OP_vs2_%d( testnum, load_inst, store_inst, index_eew, base, offset_base )"%(nf, n) + " \\\n\
            TEST_CASE_LOOP( testnum, v%d,  "%vs3 + "\\\n\
                VSET_VSEW_4AVL \\\n\
                la  x7, base; \\\n\
                la  x8, offset_base; \\\n\
                MK_VLE_INST(index_eew) v%d, (x8); "%(n) + "\\\n\
                load_inst v%d, (x7), v%d; "%(vs3, n) + "\\\n\
                vadd.vi v%d, v%d, 1; "%(vs3, vs3) + "\\\n\
                store_inst v%d, (x7), v%d; "%(vs3, n) + "\\\n\
                load_inst v%d, (x7), v%d; "%(vs3, n) + "\\\n\
            )\\", file=f)
            for i in range(1, nf):
                print("    TEST_CASE_LOOP_CONTINUE( testnum, v%d) %s"%(vs3+lmul_1*i, "\n" if i + 1 == nf else "\\"), file=f)


def generate_tests_vsxsegei(f, name, name_l, rs1_val, rs2_val, lmul, vsew, eew):
    emul = eew / vsew * lmul
    if emul < 0.125 or emul > 8:
        return 0
    emul_1 = max(1, emul)
    lmul_1 = max(1, lmul) # (nf * flmul) <= (NVPR / 4) &&  (insn.rd() + nf * flmul) <= NVPR
    
    n = 0
    rnd = 0
    print("  #-------------------------------------------------------------", file=f)
    print("  # %s<nf>ei%d Tests"%(name, eew), file=f)
    print("  #-------------------------------------------------------------", file=f)
    
    for i in range(2):
        for nf in range(2, 9):
            if lmul_1 * nf > 8 or 8 + emul_1*nf > 16: # out of range
                break
            instr = "%s%dei%d"%(name, nf, eew)
            instr_l = "%s%dei%d"%(name_l, nf, eew)
            n += 1
            print("  TEST_VSXSEG%d_OP( "%nf+str(n)+",  %s.v, %s.v, %d, "%(instr_l, instr, eew)+"0 + tdat, "+"idx%ddat"%eew+" );", file=f)
            rnd += nf
            n += 1
            print("  TEST_VSXSEG%d_OP( "%nf+str(n)+",  %s.v, %s.v, %d, "%(instr_l, instr, eew)+"%d + tdat10, "%(vsew//8)+"idx%ddat"%eew+" );", file=f)
            rnd += nf
            n += 1
            print("  TEST_VSXSEG%d_OP( "%nf+str(n)+",  %s.v, %s.v, %d, "%(instr_l, instr, eew)+"-4096 + tsdat9, "+"idx%ddat"%eew+" );", file=f)
            rnd += nf
    
    for nf in range(2, 9):
        if lmul_1 * nf > 8:
            break
        instr = "%s%dei%d"%(name, nf, eew)
        instr_l = "%s%dei%d"%(name_l, nf, eew)
        for i in range(1, 32):
            if i % lmul != 0:
                continue
            if i + lmul_1*nf > 32:
                break
            if get_aligned_reg(i, lmul, emul, nf) == 0:
                continue
            n += 1
            print("  TEST_VSXSEG%d_OP_vs3_%d( "%(nf, i)+str(n)+",  %s.v, %s.v, %d, "%(instr_l, instr, eew)+"%d + tdat, "%(vsew//8)+"idx%ddat"%eew+" );", file=f)
            rnd += nf
        for i in range(1, 32):
            if i % emul != 0:
                continue
            if i + emul_1*nf > 32:
                break
            if get_aligned_reg(i, emul, lmul, nf) == 0:
                continue
            n += 1
            print("  TEST_VSXSEG%d_OP_vs2_%d( "%(nf, i)+str(n)+",  %s.v, %s.v, %d, "%(instr_l, instr, eew)+"%d + tdat, "%(vsew//8)+"idx%ddat"%eew+" );", file=f)
            rnd += nf
    
    return (n, rnd)


def generate_macros_vlre(f, eew):
    nf_list = [1, 2, 4, 8]
    for nf in nf_list:
        VSET_EEW_EMUL = get_vset_eew_emul(eew, nf)
        print("#define VSET_EEW_EMUL%d %s\n"%(nf, VSET_EEW_EMUL), file=f)
    
    for nf in nf_list:
        print("#define TEST_VL%dRE_OP( testnum, inst, base )"%(nf) + " \\\n\
        TEST_CASE_LOOP_EEW_EMUL( testnum, v8, %d, "%(nf) + " \\\n\
            la  x7, base; \\\n\
            inst v8, (x7); \\\n\
        )", file=f)
        for n in range(1, 32):
            if not is_aligned(n, nf):
                continue
            print("#define TEST_VL%dRE_OP_vd_%d( testnum, inst, base )"%(nf, n) + " \\\n\
            TEST_CASE_LOOP_EEW_EMUL( testnum, v%d, %d, "%(n, nf) + " \\\n\
                la  x7, base; \\\n\
                inst v%d, (x7); "%n + "\\\n\
            )", file=f)


def generate_tests_vlre(f, eew):
    nf_list = [1, 2, 4, 8]
    
    n = 0
    vr_num = 0
    print("  #-------------------------------------------------------------", file=f)
    print("  # vl<nf>re%d Tests"%eew, file=f)
    print("  #-------------------------------------------------------------", file=f)

    for i in range(2):
        for nf in nf_list:
            instr = "vl%dre%d"%(nf, eew)
            n += 1
            print("  TEST_VL%dRE_OP( "%nf+str(n)+",  %s.v, " %instr+"0 + tdat"+" );", file=f)
            vr_num += nf
            n += 1
            print("  TEST_VL%dRE_OP( "%nf+str(n)+",  %s.v, " %instr+"%d + tdat"%(eew//8)+" );", file=f)
            vr_num += nf
    
    for nf in nf_list:
        for i in range(1, 32):
            if not is_aligned(i, nf):
                continue
            instr = "vl%dre%d"%(nf, eew)
            n += 1
            print("  TEST_VL%dRE_OP_vd_%d( "%(nf, i)+str(n)+",  %s.v, " %instr+"0 + tdat"+" );", file=f)
            vr_num += nf

    return (n, vr_num)
