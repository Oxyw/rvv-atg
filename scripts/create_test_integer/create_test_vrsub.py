import logging
import os
from scripts.test_common_info import *
import re

instr = 'vrsub'


def generate_macros(f):
    for n in range(2, 32):
        print("#define TEST_VX_OP_1%d( testnum, inst, result, val2, val1 )"%n + " \\\n\
            TEST_CASE( testnum, v16, result, \\\n\
                li x7, MASK_VSEW(val2); \\\n\
                vmv.v.x v8, x7; \\\n\
                li x%d, MASK_XLEN(val1); "%n + "\\\n\
                inst v16, v8, x%d; "%n + " \\\n\
        )", file=f)
    for n in range(1, 32):
        # Beacuse of the widening instruction, rd should valid for the destination’s EMUL
        print("#define TEST_VX_OP_rd%d( testnum, inst, result, val1, val2 )"%n + " \\\n\
            TEST_CASE( testnum, v%d, result,"%n + " \\\n\
                li x7, MASK_VSEW(val2); \\\n\
                vmv.v.x v8, x7; \\\n\
                li x1, MASK_XLEN(val1); \\\n\
                inst v%d, v8, x1; "%n + " \\\n\
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


def generate_tests(f, rs1_val, rs2_val, lmul):
    n = 1
    print("  #-------------------------------------------------------------", file=f)
    print("  # VX Tests", file=f)
    print("  #-------------------------------------------------------------", file=f)
    print("  RVTEST_SIGBASE( x12,signature_x12_1)", file=f)
    for i in range(len(rs1_val)):
        n += 1
        print("  TEST_VX_OP( "+str(n)+",  %s.vx, " %
              instr+"5201314"+", "+rs1_val[i]+", "+rs2_val[i]+" );", file=f)
    for i in range(100):     
        k = i%31+1 
        if k%lmul == 0 and k != 8 and k != 16 and k != 24:
            n+=1
            print("  TEST_VX_OP_rd%d( "%k+str(n)+",  %s.vx, "%instr+"5201314"+", "+rs1_val[i]+", "+rs2_val[i]+");",file=f)
        
        k = i%30+2
        n +=1
        print("  TEST_VX_OP_1%d( "%k+str(n)+",  %s.vx, "%instr+"5201314"+", "+rs1_val[i]+", "+rs2_val[i]+");",file=f)
        print("  #-------------------------------------------------------------", file=f)
    print("  # VI Tests", file=f)
    print("  #-------------------------------------------------------------", file=f)
    print("  RVTEST_SIGBASE( x12,signature_x12_1)", file=f)
    for i in range(len(rs1_val)):
        n += 1
        print("  TEST_VI_OP( "+str(n)+",  %s.vi, " %
              instr+"5201314"+", "+rs1_val[i]+", "+" 4 "+" );", file=f)
    


def create_empty_test_vrsub(xlen, vlen, vsew, lmul, vta, vma, output_dir):
    logging.info("Creating empty test for {}".format(instr))

    path = "%s/%s_empty.S" % (output_dir, instr)
    f = open(path, "w+")

    # Common header files
    print_common_header(instr, f)

    print("  TEST_VV_OP_NOUSE( 1, vadd.vv, 2, 1, 1 );", file=f)

    # Common const information
    print_common_ending(f)

    f.close()
    os.system("cp %s %s" % (path, output_dir))

    logging.info(
        "Creating empty test for {}: finish in {}!".format(instr, path))

    return path


def create_first_test_vrsub(xlen, vlen, vsew, lmul, vta, vma, output_dir, rpt_path):
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
    generate_tests(f, rs1_val, rs2_val, lmul)

    # Common const information
    print_common_ending(f)

    f.close()
    os.system("cp %s %s" % (path, output_dir))

    logging.info(
        "Creating first test for {}: finish in {}!".format(instr, path))

    return path
