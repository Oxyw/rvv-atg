import logging
import os
from scripts.test_common_info import *
from scripts.create_test_floating.create_test_common import *
import re

instr = 'vfclass'


def generate_fdat_seg(f):
    print("fdat_rs1:", file=f)
    for i in range(len(rs1_val)):
        print("fdat_rs1_" + str(i) + ":  .word " + rs1_val[i], file=f)
    print("", file=f)
    print("fdat_rs2:", file=f)
    for i in range(len(rs2_val)):
        print("fdat_rs2_" + str(i) + ":  .word " + rs2_val[i], file=f)


def generate_macros(f, lmul):
    lmul = 1 if lmul < 1 else int(lmul)

    for n in range(1, 32):
        if n % lmul != 0 or n == 24:
            continue
        print("#define TEST_FP_HEX_1OPERAND_OP_rs1_%d( testnum, inst, flags, result, val )"%n + " \\\n\
            TEST_CASE( testnum, v24, result, \\\n\
                li x7, MASK_VSEW(val); \\\n\
                vmv.v.x v%d, x7; "%n + " \\\n\
                inst v24, v%d; "%n + " \\\n\
                frflags a1; \\\n\
                li a2, flags; \\\n\
            )", file = f)

    for n in range(1, 32):
        if n % lmul != 0 or n == 8:
            continue
        print("#define TEST_FP_HEX_1OPERAND_OP_rd_%d( testnum, inst, flags, result, val )"%n + " \\\n\
            TEST_CASE( testnum, v%d, result, "%n + " \\\n\
                li x7, MASK_VSEW(val); \\\n\
                vmv.v.x v8, x7;  \\\n\
                inst v%d, v8; "%n + " \\\n\
                frflags a1; \\\n\
                li a2, flags; \\\n\
            )", file = f)

def extract_operands(f, rpt_path):
    # Floating pooints tests don't need to extract operands, rs1 and rs2 are fixed
    return 0


def generate_tests(f, rs1_val, lmul):
    lmul = 1 if lmul < 1 else int(lmul)
    n = 1
    print("  #-------------------------------------------------------------",file=f)
    print("  # vfclass.v Tests",file=f)
    print("  #-------------------------------------------------------------",file=f)
    print("  RVTEST_SIGBASE( x12,signature_x12_1)",file=f)
    for i in range(len(rs1_val)):        
        print("TEST_FP_HEX_1OPERAND_OP( %d,  %s.v, 0xff100,               5201314,        %s );"%(n, instr, rs1_val[i]), file=f)
        n += 1
    
    print("  #-------------------------------------------------------------",file=f)
    print("  # vfclass.v Tests (different register)",file=f)
    print("  #-------------------------------------------------------------",file=f)
    print("  RVTEST_SIGBASE( x12,signature_x12_1)",file=f)

    n = n + 1
    for i in range(len(rs1_val)):
        k = i % 31 + 1  
        if k % lmul != 0 or k == 8:
            continue
        print("  TEST_FP_HEX_1OPERAND_OP_rd_%d( "%k+str(n)+",  %s.v, 0xff100, "%instr +"5201314"+ ", " +rs1_val[i]+ " );",file=f)
        n += 1

        k = i % 31 + 1
        if k % lmul != 0 or k == 24:
            continue
        print("  TEST_FP_HEX_1OPERAND_OP_rs1_%d( "%k+str(n)+",  %s.v, 0xff100, "%instr +"5201314"+ ", " +rs1_val[i]+ " );",file=f)
        n += 1

def print_ending(f):
    print("  RVTEST_SIGBASE( x20,signature_x20_2)\n\
    \n\
    TEST_VV_OP_NOUSE(32766, vadd.vv, 2, 1, 1)\n\
    TEST_PASSFAIL\n\
    #endif\n\
    \n\
    RVTEST_CODE_END\n\
    RVMODEL_HALT\n\
    \n\
    .data\n\
    RVTEST_DATA_BEGIN\n\
    \n\
    TEST_DATA\n\
    \n\
    ", file=f)

    generate_fdat_seg(f)

    print("signature_x12_0:\n\
        .fill 0,4,0xdeadbeef\n\
    \n\
    \n\
    signature_x12_1:\n\
        .fill 32,4,0xdeadbeef\n\
    \n\
    \n\
    signature_x20_0:\n\
        .fill 512,4,0xdeadbeef\n\
    \n\
    \n\
    signature_x20_1:\n\
        .fill 512,4,0xdeadbeef\n\
    \n\
    \n\
    signature_x20_2:\n\
        .fill 376,4,0xdeadbeef\n\
    \n\
    #ifdef rvtest_mtrap_routine\n\
    \n\
    mtrap_sigptr:\n\
        .fill 128,4,0xdeadbeef\n\
    \n\
    #endif\n\
    \n\
    #ifdef rvtest_gpr_save\n\
    \n\
    gpr_save:\n\
        .fill 32*(XLEN/32),4,0xdeadbeef\n\
    \n\
    #endif\n\
    \n\
    RVTEST_DATA_END\n\
    ", file=f)


def create_empty_test_vfclass(xlen, vlen, vsew, lmul, vta, vma, output_dir):
    logging.info("Creating empty test for {}".format(instr))

    path = "%s/%s_empty.S" % (output_dir, instr)
    f = open(path, "w+")

    # Common header files
    print_common_header(instr, f)

    print("  TEST_VFMVF_OP( 1,  fdat_rs1_0 );", file=f)

    # Common const information
    print_ending(f)

    f.close()
    os.system("cp %s %s" % (path, output_dir))

    logging.info(
        "Creating empty test for {}: finish in {}!".format(instr, path))

    return path


def create_first_test_vfclass(xlen, vlen, vsew, lmul, vta, vma, output_dir, rpt_path):
    logging.info("Creating first test for {}".format(instr))

    path = "%s/%s_first.S" % (output_dir, instr)
    f = open(path, "w+")

    # Common header files
    print_common_header(instr, f)

    # Extract operands
    extract_operands(f, rpt_path)

    # Generate macros to test diffrent register
    generate_macros(f, lmul)

    # Generate tests
    generate_tests(f, rs1_val, lmul)

    # Common const information
    print_ending(f)

    f.close()
    os.system("cp %s %s" % (path, output_dir))

    logging.info(
        "Creating first test for {}: finish in {}!".format(instr, path))

    return path
