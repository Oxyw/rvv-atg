import logging
import os
from scripts.create_test_loadstore.create_test_common import  generate_macros_vlsseg
from scripts.test_common_info import *
import re

name = 'vlssege8'

instr = 'vlsseg2e8'
instr1 = 'vlsseg3e8'
instr2 = 'vlsseg4e8'
instr3 = 'vlsseg5e8'
instr4 = 'vlsseg6e8'
instr5 = 'vlsseg7e8'
instr6 = 'vlsseg8e8'


def generate_tests(f, rs1_val, rs2_val, vsew, lmul):
    emul = 8 / vsew * lmul
    if emul < 0.125 or emul > 8:
        return 0
    n = 0
    print("  #-------------------------------------------------------------", file=f)
    print("  # VV Tests", file=f)
    print("  #-------------------------------------------------------------", file=f)

    for i in range(2):
        if 2 * emul <= 8 and 2 + 3 * emul <= 32: # (nf * emul) <= (NVPR / 4) &&  (insn.rd() + nf * emul) <= NVPR);
            n += 1
            print("  TEST_VLSSEG2_OP( "+str(n)+",  %s.v, " %instr+" 8 "+", "+"0"+", "+"0 + tdat"+" );", file=f)
            n += 1
            print("  TEST_VLSSEG2_OP( "+str(n)+",  %s.v, " %instr+" 8 "+", "+"1"+", "+"0 + tdat"+" );", file=f)
            n += 1
            print("  TEST_VLSSEG2_OP( "+str(n)+",  %s.v, " %instr+" 8 "+", "+"2"+", "+"0 + tdat"+" );", file=f)
            n += 1
            print("  TEST_VLSSEG2_OP( "+str(n)+",  %s.v, " %instr+" 8 "+", "+"3"+", "+"0 + tdat"+" );", file=f)
            n += 1
            print("  TEST_VLSSEG2_OP( "+str(n)+",  %s.v, " %instr+" 8 "+", "+"0"+", "+"1 + tdat"+" );", file=f)
            n += 1
            print("  TEST_VLSSEG2_OP( "+str(n)+",  %s.v, " %instr+" 8 "+", "+"1"+", "+"1 + tdat"+" );", file=f)
            n += 1
            print("  TEST_VLSSEG2_OP( "+str(n)+",  %s.v, " %instr+" 8 "+", "+"2"+", "+"1 + tdat"+" );", file=f)
            n += 1
            print("  TEST_VLSSEG2_OP( "+str(n)+",  %s.v, " %instr+" 8 "+", "+"3"+", "+"1 + tdat"+" );", file=f)
            n += 1
            print("  TEST_VLSSEG2_OP( "+str(n)+",  %s.v, " %instr+" 8 "+", "+"0"+", "+"2 + tdat"+" );", file=f)
            n += 1
            print("  TEST_VLSSEG2_OP( "+str(n)+",  %s.v, " %instr+" 8 "+", "+"1"+", "+"2 + tdat"+" );", file=f)
            n += 1
            print("  TEST_VLSSEG2_OP( "+str(n)+",  %s.v, " %instr+" 8 "+", "+"2"+", "+"2 + tdat"+" );", file=f)
            n += 1
            print("  TEST_VLSSEG2_OP( "+str(n)+",  %s.v, " %instr+" 8 "+", "+"3"+", "+"2 + tdat"+" );", file=f)
            n += 1
            print("  TEST_VLSSEG2_OP( "+str(n)+",  %s.v, " %instr+" 8 "+", "+"0"+", "+"3 + tdat"+" );", file=f)
            n += 1
            print("  TEST_VLSSEG2_OP( "+str(n)+",  %s.v, " %instr+" 8 "+", "+"1"+", "+"3 + tdat"+" );", file=f)
            n += 1
            print("  TEST_VLSSEG2_OP( "+str(n)+",  %s.v, " %instr+" 8 "+", "+"2"+", "+"3 + tdat"+" );", file=f)
            n += 1
            print("  TEST_VLSSEG2_OP( "+str(n)+",  %s.v, " %instr+" 8 "+", "+"3"+", "+"3 + tdat"+" );", file=f)
            n += 1
            print("  TEST_VLSSEG2_OP( "+str(n)+",  %s.v, " %instr+" 8 "+", "+"8"+", "+"tdat14"+" );", file=f)
            n += 1
            print("  TEST_VLSSEG2_OP( "+str(n)+",  %s.v, " %instr+" 8 "+", "+"-8"+", "+"tdat14"+" );", file=f)
        if 3 * emul <= 8 and 8 + 3 * emul <= 32 and 8 + 3 * lmul<= 32: # (nf * emul) <= (NVPR / 4) &&  (insn.rd() + nf * emul) <= NVPR);
            n += 1
            print("  TEST_VLSSEG3_OP( "+str(n)+",  %s.v, " %instr1+" 8 "+", "+"1"+", "+"0 + tdat"+" );", file=f)
        if 4 * emul <= 8 and 8 + 4 * emul <= 32 and 8 + 4 * lmul<= 32: # (nf * emul) <= (NVPR / 4) &&  (insn.rd() + nf * emul) <= NVPR);
            n += 1
            print("  TEST_VLSSEG4_OP( "+str(n)+",  %s.v, " %instr2+" 8 "+", "+"1"+", "+"12 + tdat"+" );", file=f)
        if 5 * emul <= 8 and 8 + 5 * emul <= 32 and 8 + 5 * lmul<= 32: # (nf * emul) <= (NVPR / 4) &&  (insn.rd() + nf * emul) <= NVPR);
            n += 1
            print("  TEST_VLSSEG5_OP( "+str(n)+",  %s.v, " %instr3+" 8 "+", "+"1"+", "+"-12 + tdat4"+" );", file=f)
        if 6 * emul <= 8 and 8 + 6 * emul <= 32 and 8 + 6 * lmul<= 32: # (nf * emul) <= (NVPR / 4) &&  (insn.rd() + nf * emul) <= NVPR);
            n += 1
            print("  TEST_VLSSEG6_OP( "+str(n)+",  %s.v, " %instr4+" 8 "+", "+"1"+", "+"0 + tdat"+" );", file=f)
        if 7 * emul <= 8 and 8 + 7 * emul <= 32 and 8 + 7 * lmul<= 32: # (nf * emul) <= (NVPR / 4) &&  (insn.rd() + nf * emul) <= NVPR);
            n += 1
            print("  TEST_VLSSEG7_OP( "+str(n)+",  %s.v, " %instr5+" 8 "+", "+"1"+", "+"0 + tdat"+" );", file=f)
        if 8 * emul <= 8 and 8 + 8 * emul <= 32 and 8 + 8 * lmul<= 32: # (nf * emul) <= (NVPR / 4) &&  (insn.rd() + nf * emul) <= NVPR);
            n += 1
            print("  TEST_VLSSEG8_OP( "+str(n)+",  %s.v, " %instr6+" 8 "+", "+"1"+", "+"0 + tdat"+" );", file=f)
        

    if 2 * emul <= 8 and 2 + 2 * emul <= 32: # (nf * emul) <= (NVPR / 4) &&  (insn.rd() + nf * emul) <= NVPR);
        for i in range(100):     
            k = i%30+1
            if k != 8 and k != 16 and k % emul == 0 and k % lmul == 0 and k + 2 * emul <= 32 and k!= 12 and k != 20 and k !=24:
                n += 1
                print("  TEST_VLSSEG1_OP_rd%d( "%k+str(n)+",  %s.v, "%instr+" 8 "+", "+"1"+", "+"0 + tdat"+" );",file=f)
            
            k = i%30+2
            if(k == 31 or k == 12 or k == 20 or k == 24):
                continue;
            n += 1
            print("  TEST_VLSSEG1_OP_1%d( "%k+str(n)+",  %s.v, "%instr+" 8 "+", "+"1"+", "+"4 + tdat"+" );",file=f)
    return n
    


def create_empty_test_vlssege8(xlen, vlen, vsew, lmul, vta, vma, output_dir):
    logging.info("Creating empty test for {}".format(name))

    path = "%s/%s_empty.S" % (output_dir, name)
    f = open(path, "w+")

    # Common header files
    print_common_header(name, f)


    # Common const information

    # Load const information
    print_load_ending(f)

    f.close()
    os.system("cp %s %s" % (path, output_dir))

    logging.info(
        "Creating empty test for {}: finish in {}!".format(name, path))

    return path


def create_first_test_vlssege8(xlen, vlen, vsew, lmul, vta, vma, output_dir, rpt_path):
    logging.info("Creating first test for {}".format(name))

    path = "%s/%s_first.S" % (output_dir, name)
    f = open(path, "w+")

    # Common header files
    print_common_header(name, f)

    # Extract operands
    rs1_val, rs2_val = extract_operands(f, rpt_path)

    # Generate macros to test diffrent register
    generate_macros_vlsseg(f, lmul, vsew, 8)

    # Generate tests
    n = generate_tests(f, rs1_val, rs2_val, vsew, lmul)

    # Common const information

    # Load const information
    print_load_ending(f, n)

    f.close()
    os.system("cp %s %s" % (path, output_dir))

    logging.info(
        "Creating first test for {}: finish in {}!".format(name, path))

    return path
