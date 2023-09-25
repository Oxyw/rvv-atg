import logging
import os
from scripts.test_common_info import *
import re

instr = 'vle32'


def generate_macros(f):
    for n in range(2, 31):
        if n == 12 or n == 20 or n == 24: # signature base registers
            continue
        print("#define TEST_VLE_OP_1%d( testnum, inst, eew, result1, result2, base )"%n + " \\\n\
            TEST_CASE_LOAD( testnum, v16, eew, result1, result2, \\\n\
                la  x%d, base; "%n + "\\\n\
                vsetivli x31, 4, MK_EEW(eew), tu, mu; \\\n\
                inst v16, (x%d); "%n + "\\\n\
                VSET_VSEW \\\n\
        )", file=f)
    for n in range(1, 32):
        # Beacuse of the widening instruction, rd should valid for the destination’s EMUL
        print("#define TEST_VLE_OP_rd%d( testnum, inst, eew, result1, result2, base )"%n + " \\\n\
            TEST_CASE_LOAD( testnum, v%d, eew, result1, result2, "%n + "\\\n\
                la  x1, base; \\\n\
                vsetivli x31, 4, MK_EEW(eew), tu, mu; \\\n\
                inst v%d, (x1); "%n + "\\\n\
                VSET_VSEW \\\n\
        ) ", file=f)
    


def extract_operands(f, rpt_path):
    rs1_val = []
    rs2_val = []
    f = open(rpt_path)
    line = f.read()
    matchObj = re.compile('rs1_val ?== ?(-?\d+)')
    rs1_val_10 = matchObj.findall(line)
    rs1_val = ['{:#016x}'.format(int(x) & 0xffffffffffffffff)
               for x in rs1_val_10]
    matchObj = re.compile('rs2_val ?== ?(-?\d+)')
    rs2_val_10 = matchObj.findall(line)
    rs2_val = ['{:#016x}'.format(int(x) & 0xffffffffffffffff)
               for x in rs2_val_10]
    f.close()
    return rs1_val, rs2_val


def generate_tests(f, rs1_val, rs2_val, vsew, lmul):
    emul = 32 / vsew * lmul
    if emul < 0.125 or emul > 8:
        return
    emul = 1 if emul < 1 else int(emul)
    n = 1
    print("  #-------------------------------------------------------------", file=f)
    print("  # VV Tests", file=f)
    print("  #-------------------------------------------------------------", file=f)
    print("  RVTEST_SIGBASE( x12,signature_x12_1)", file=f)
    for i in range(2):
        n += 1
        print("  TEST_VLE_OP( "+str(n)+",  %s.v, " %
              instr+" 32 "+", "+"0x00ff00ff"+", "+"0xff00ff00"+" , "+"0 + tdat"+" );", file=f)
        n += 1
        print("  TEST_VLE_OP( "+str(n)+",  %s.v, " %
              instr+" 32 "+", "+"0x0ff00ff0"+", "+"0xf00ff00f"+" , "+"-4 + tdat4"+" );", file=f)
        n += 1
        print("  TEST_VLE_OP( "+str(n)+",  %sff.v, " %
              instr+" 32 "+", "+"0x00ff00ff"+", "+"0xff00ff00"+" , "+"0 + tdat"+" );", file=f)
        n += 1
        print("  TEST_VLE_OP( "+str(n)+",  %s.v, " %
              instr+" 32 "+", "+"0xff"+", "+"0x00"+" , "+"4100 + tdat"+" );", file=f)
        n += 1
        print("  TEST_VLE_OP( "+str(n)+",  %s.v, " %
              instr+" 32 "+", "+"0xff"+", "+"0x00"+" , "+"-4100 + tdat10"+" );", file=f)   
    for i in range(100):     
        k = i%31+1
        n+=1
        if( k % lmul == 0 and k % emul == 0 and k != 12 and k != 20 and k != 24):
            print("  TEST_VLE_OP_rd%d( "%k+str(n)+",  %s.v, "%instr+" 32 "+", "+"0xff00ff00"+", "+"0x0ff00ff0"+" , "+"4 + tdat"+");",file=f)
        
        k = i%30+2
        if(k == 31 or k == 12 or k == 20 or k == 24):
            continue;
        n +=1
        print("  TEST_VLE_OP_1%d( "%k+str(n)+",  %s.v, "%instr+" 32 "+", "+"0xf00ff00f"+", "+"0x00ff00ff"+" , "+"0 + tdat4"+");",file=f)
    


def create_empty_test_vle32(xlen, vlen, vsew, lmul, vta, vma, output_dir):
    logging.info("Creating empty test for {}".format(instr))

    path = "%s/%s_empty.S" % (output_dir, instr)
    f = open(path, "w+")

    # Common header files
    print_common_header(instr, f)


    # Common const information
    #print_common_ending(f)
    # Load const information
    print_load_ending(f)

    f.close()
    os.system("cp %s %s" % (path, output_dir))

    logging.info(
        "Creating empty test for {}: finish in {}!".format(instr, path))

    return path


def create_first_test_vle32(xlen, vlen, vsew, lmul, vta, vma, output_dir, rpt_path):
    logging.info("Creating first test for {}".format(instr))

    path = "%s/%s_first.S" % (output_dir, instr)
    f = open(path, "w+")

    # Common header files
    print_common_header(instr, f)

    # Extract operands
    rs1_val, rs2_val = extract_operands(f, rpt_path)

    # Generate macros to test diffrent register
    generate_macros(f)

    # Generate tests
    generate_tests(f, rs1_val, rs2_val, vsew, lmul)

    # Common const information
    # print_common_ending(f)
    # Load const information
    print_load_ending(f)

    f.close()
    os.system("cp %s %s" % (path, output_dir))

    logging.info(
        "Creating first test for {}: finish in {}!".format(instr, path))

    return path
