import logging
import os
from scripts.create_test_loadstore.create_test_common import generate_macros_vlxeiseg
from scripts.test_common_info import *
import re

name = 'vluxsegei8'

instr  = 'vluxseg2ei8'
instr1 = 'vluxseg3ei8'
instr2 = 'vluxseg4ei8'
instr3 = 'vluxseg5ei8'
instr4 = 'vluxseg6ei8'
instr5 = 'vluxseg7ei8'
instr6 = 'vluxseg8ei8'

def generate_tests(f, rs1_val, rs2_val, vsew, lmul):
    emul = 8 / vsew * lmul
    n = 1
    print("  #-------------------------------------------------------------", file=f)
    print("  # VV Tests", file=f)
    print("  #-------------------------------------------------------------", file=f)
    print("  RVTEST_SIGBASE( x12,signature_x12_1)", file=f)
    for i in range(2):
        if 2 * emul <= 8 and 2 + 3 * emul <= 32:
            n += 1
            print("  TEST_VLXSEG1_OP( "+str(n)+",  %s.v, " %instr+" 8 "+", "+"0xff"+", "+"0 + tdat"+" , "+"idx8dat"+");", file=f)
        if 3 * emul <= 8 and 8 + 3 * emul <= 32:
            n += 1
            print("  TEST_VLXSEG3_OP( "+str(n)+",  %s.v, " %instr1+" 8 "+", "+"0xff"+", "+"0x00"+", "+"0xff"+", "+"0 + tdat"+", "+"idx8dat"+" );", file=f)
        if 4 * emul <= 8 and 8 + 4 * emul <= 32:
            n += 1
            print("  TEST_VLXSEG3_OP( "+str(n)+",  %s.v, " %instr2+" 8 "+", "+"0x0f"+", "+"0xf0"+", "+"0x0f"+", "+"12 + tdat"+", "+"idx8dat"+" );", file=f)
        if 5 * emul <= 8 and 8 + 5 * emul <= 32:
            n += 1
            print("  TEST_VLXSEG3_OP( "+str(n)+",  %s.v, " %instr3+" 8 "+", "+"0xff"+", "+"0x00"+", "+"0xff"+","+"-12 + tdat4"+", "+"idx8dat"+" );", file=f)
        if 6 * emul <= 8 and 8 + 6 * emul <= 32:
            n += 1
            print("  TEST_VLXSEG3_OP( "+str(n)+",  %s.v, " %instr4+" 8 "+", "+"0x0f"+", "+"0xf0"+", "+"0x0f"+", "+"0 + tdat4"+", "+"idx8dat"+" );", file=f)
        if 7 * emul <= 8 and 8 + 7 * emul <= 32:
            n += 1
            print("  TEST_VLXSEG3_OP( "+str(n)+",  %s.v, " %instr5+" 8 "+", "+"0x0f"+", "+"0xf0"+", "+"0x0f"+", "+"0 + tdat4"+", "+"idx8dat"+" );", file=f)
        if 8 * emul <= 8 and 8 + 8 * emul <= 32:
            n += 1
            print("  TEST_VLXSEG3_OP( "+str(n)+",  %s.v, " %instr6+" 8 "+", "+"0x0f"+", "+"0xf0"+", "+"0x0f"+", "+"0 + tdat4"+", "+"idx8dat"+" );", file=f)
        

    for i in range(100):     
        k = i%30+1
        if k != 8 and k != 16 and k % emul == 0 and k + 2 * emul <= 32:
            n+=1
            print("   TEST_VLXSEG1_OP_rd%d( "%k+str(n)+",  %s.v, "%instr+"8"+", "+"0xff"+", "+"0 + tdat"+", "+"idx8dat"+");",file=f)
        
        k = i%30+2
        # if(k == 31):
        #     continue;
        n +=1
        print("  TEST_VLXSEG1_OP_1%d( "%k+str(n)+",  %s.v, "%instr+"8"+", "+"0xff"+", "+"0 + tdat"+", "+"idx8dat"+" );",file=f)
    


def create_empty_test_vluxsegei8(xlen, vlen, vsew, lmul, vta, vma, output_dir):
    logging.info("Creating empty test for {}".format(name))

    path = "%s/%s_empty.S" % (output_dir, name)
    f = open(path, "w+")

    # Common header files
    print_common_header(name, f)

    print(" TEST_VLXSEG1_OP( 3, vluxseg2ei8.v, 8, 0x00ff00ff, 0  + tdat, idx8dat );", file=f)

    # Common const information
    #print_common_ending(f)
    # Load const information
    print_load_ending(f)

    f.close()
    os.system("cp %s %s" % (path, output_dir))

    logging.info(
        "Creating empty test for {}: finish in {}!".format(name, path))

    return path


def create_first_test_vluxsegei8(xlen, vlen, vsew, lmul, vta, vma, output_dir, rpt_path):
    logging.info("Creating first test for {}".format(name))

    path = "%s/%s_first.S" % (output_dir, name)
    f = open(path, "w+")

    # Common header files
    print_common_header(name, f)

    # Extract operands
    rs1_val, rs2_val = extract_operands(f, rpt_path)

    # Generate macros to test diffrent register
    generate_macros_vlxeiseg(f, lmul, vsew, 8)

    # Generate tests
    generate_tests(f, rs1_val, rs2_val, vsew, lmul)

    # Common const information
    # print_common_ending(f)
    # Load const information
    print_load_ending(f)

    f.close()
    os.system("cp %s %s" % (path, output_dir))

    logging.info(
        "Creating first test for {}: finish in {}!".format(name, path))

    return path
