import logging
import os
from scripts.test_common_info import *
from scripts.create_test_floating.create_test_common import valid_aligned_regs

instr = 'vfwcvt'
rs2_val = ['0x00000000', '0x80000000', '0x00000001', '0x80000001', '0x00000002', '0x807FFFFE', '0x007FFFFF', '0x807FFFFF', '0x00800000', '0x80800000', '0x00800001', '0x80855555', '0x7F7FFFFF', '0xFF7FFFFF', '0x3F800000', '0xBF800000', '0x00000000', '0x80000000', '0x00000001', '0x80000001', '0x00000002', '0x807FFFFE', '0x007FFFFF', '0x807FFFFF', '0x00800000', '0x80800000', '0x00800001', '0x80855555', '0x7F7FFFFF', '0xFF7FFFFF', '0x3F800000', '0xBF800000', ]


def generate_macros(f, lmul):
    lmul = 1 if lmul < 1 else int(lmul)
    for n in range(1,32):
        if n % lmul != 0: continue
        rd = valid_aligned_regs(n)[0]
        print("#define TEST_W_FP_INT_OP_2%d( testnum, inst, flags, result, val ) \\\n\
        TEST_CASE_FP_INT( testnum, v%d, flags, __riscv_double_vsew, result, val, \\\n\
            flw f0, 0(a0); \\\n\
            vfmv.s.f v%d, f0; \\\n\
            inst v%d, v%d; \\\n\
        )"%(n, rd, n, rd, n),file=f)
    for n in range(1,32):
        if n % (2*lmul) != 0: continue
        rs2 = valid_aligned_regs(n)[0]
        print("#define TEST_W_FP_INT_OP_rd%d( testnum, inst, flags, result, val ) \\\n\
        TEST_CASE_FP_INT( testnum, v%d, flags, __riscv_double_vsew, result, val, \\\n\
            flw f0, 0(a0); \\\n\
            vfmv.s.f v%d, f0; \\\n\
            inst v%d, v%d; \\\n\
        )"%(n, n, rs2, n, rs2),file=f)


def extract_operands(f, rpt_path):
    # Floating pooints tests don't need to extract operands, rs1 and rs2 are fixed
    return 0


def generate_tests(f, lmul):
    n = 1
    print("  #-------------------------------------------------------------",file=f)
    print("  # %s.xu.f.v (float to double-width unsigned integer) tests"%instr,file=f)
    print("  #-------------------------------------------------------------",file=f)
    print("  RVTEST_SIGBASE( x12,signature_x12_1)",file=f)
    for i in range(len(rs2_val)):
        n += 1
        print("  TEST_W_FP_INT_OP( "+str(n)+",  %s.xu.f.v, 0xff100, 5201314, "%instr+rs2_val[i]+" );",file=f)

    print("  #-------------------------------------------------------------",file=f)
    print("  # %s.x.f.v (float to double-width signed integer) tests"%instr,file=f)
    print("  #-------------------------------------------------------------",file=f)
    print("  RVTEST_SIGBASE( x20,signature_x20_0)",file=f)
    for i in range(len(rs2_val)):
        n += 1
        print("  TEST_W_FP_INT_OP( "+str(n)+",  %s.x.f.v, 0xff100, 5201314, "%instr+rs2_val[i]+" );",file=f)

    print("  #-------------------------------------------------------------",file=f)
    print("  # %s.rtz.xu.f.v (float to double-width unsigned integer truncating) tests"%instr,file=f)
    print("  #-------------------------------------------------------------",file=f)
    print("  RVTEST_SIGBASE( x12,signature_x12_1)",file=f)
    for i in range(len(rs2_val)):
        n += 1
        print("  TEST_W_FP_INT_OP( "+str(n)+",  %s.rtz.xu.f.v, 0xff100, 5201314, "%instr+rs2_val[i]+" );",file=f)

    print("  #-------------------------------------------------------------",file=f)
    print("  # %s.rtz.x.f.v (float to double-width signed integer truncating) tests"%instr,file=f)
    print("  #-------------------------------------------------------------",file=f)
    print("  RVTEST_SIGBASE( x20,signature_x20_0)",file=f)
    for i in range(len(rs2_val)):
        n += 1
        print("  TEST_W_FP_INT_OP( "+str(n)+",  %s.rtz.x.f.v, 0xff100, 5201314, "%instr+rs2_val[i]+" );",file=f)

    print("  #-------------------------------------------------------------",file=f)
    print("  # %s.f.xu.v (unsigned integer to double-width float) tests"%instr,file=f)
    print("  #-------------------------------------------------------------",file=f)
    print("  RVTEST_SIGBASE( x20,signature_x20_0)",file=f)
    for i in range(len(rs2_val)):
        n += 1
        print("  TEST_W_INT_FP_OP( "+str(n)+",  %s.f.xu.v, 0xff100, 5201314, "%instr+rs2_val[i]+" );",file=f)

    print("  #-------------------------------------------------------------",file=f)
    print("  # %s.f.x.v (signed integer to double-width float) tests"%instr,file=f)
    print("  #-------------------------------------------------------------",file=f)
    print("  RVTEST_SIGBASE( x12,signature_x12_1)",file=f)
    for i in range(len(rs2_val)):
        n += 1
        print("  TEST_W_INT_FP_OP( "+str(n)+",  %s.f.x.v, 0xff100, 5201314, "%instr+rs2_val[i]+" );",file=f)

    print("  #-------------------------------------------------------------",file=f)
    print("  # %s.f.f.v (single-width float to double-width float) tests"%instr,file=f)
    print("  #-------------------------------------------------------------",file=f)
    print("  RVTEST_SIGBASE( x20,signature_x20_0)",file=f)
    for i in range(len(rs2_val)):
        n += 1
        print("  TEST_W_FP_1OPERAND_OP( "+str(n)+",  %s.f.f.v, 0xff100, 5201314, "%instr+rs2_val[i]+" );",file=f)

    print("  #-------------------------------------------------------------",file=f)
    print("  # float to double-width integer Tests (different register)",file=f)
    print("  #-------------------------------------------------------------",file=f)
    print("  RVTEST_SIGBASE( x12,signature_x12_1)",file=f)
    for i in range(len(rs2_val)):     
        k = i % 31 + 1
        if k % lmul != 0: continue
        n += 1
        print("  TEST_W_FP_INT_OP_2%d( "%k+str(n)+",  %s.xu.f.v, 0xff100, 5201314, "%instr+rs2_val[i]+" );",file=f)
        
        if k % (2*lmul) != 0: continue
        n += 1
        print("  TEST_W_FP_INT_OP_rd%d( "%k+str(n)+",  %s.xu.f.v, 0xff100, 5201314, "%instr+rs2_val[i]+" );",file=f)


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


def create_empty_test_vfwcvt(xlen, vlen, vsew, lmul, vta, vma, output_dir):
    logging.info("Creating empty test for {}".format(instr))

    path = "%s/%s_empty.S" % (output_dir, instr)
    f = open(path, "w+")

    # Common header files
    print_common_header(instr, f)

    print("  TEST_W_FP_INT_OP( 1,  %s.xu.f.v, 0, 1, 1);"%instr, file=f)

    # Common const information
    print_ending(f)

    f.close()
    os.system("cp %s %s" % (path, output_dir))

    logging.info(
        "Creating empty test for {}: finish in {}!".format(instr, path))

    return path


def create_first_test_vfwcvt(xlen, vlen, vsew, lmul, vta, vma, output_dir, rpt_path):
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
    generate_tests(f, lmul)

    # Common const information
    print_ending(f)

    f.close()
    os.system("cp %s %s" % (path, output_dir))

    logging.info(
        "Creating first test for {}: finish in {}!".format(instr, path))

    return path
