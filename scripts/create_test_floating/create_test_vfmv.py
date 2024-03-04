import logging
import os
from scripts.test_common_info import *
from scripts.create_test_floating.create_test_common import *
import re

instr = 'vfmv'

def generate_fdat_seg(f, vsew):
    print("fdat_rs1:", file=f)
    for i in range(len(rs1_val)):
        print("fdat_rs1_" + str(i) + ":  .%s "%("word" if vsew == 32 else "dword") + rs1_val[i], file=f)
    print("", file=f)
    print("fdat_rs2:", file=f)
    for i in range(len(rs2_val)):
        print("fdat_rs2_" + str(i) + ":  .%s "%("word" if vsew == 32 else "dword") + rs2_val[i], file=f)


def generate_macros(f, vsew):
    for n in range(1, 32):
        print("#define TEST_VFMVF_OP_rs_%d( testnum, base ) \\\n\
            li TESTNUM, testnum; \\\n\
            la a0, base; \\\n\
            fl%s f%d, 0(a0); \\\n\
            vfmv.v.f v24, f%d; \\\n\
            vfmv.f.s f8, v24; \\\n\
            fcvt.w.s x8, f8; \\\n\
            fcvt.w.s x7, f%d; \n" % (n, "w" if vsew == 32 else "d", n, n, n), file=f)
    for n in range(1, 32):
        print("#define TEST_VFMVF_OP_rsrd_%d( testnum, base ) \\\n\
            li TESTNUM, testnum; \\\n\
            la a0, base; \\\n\
            fl%s f7, 0(a0); \\\n\
            vfmv.v.f v%d, f7; \\\n\
            vfmv.f.s f8, v%d; \\\n\
            fcvt.w.s x8, f8; \\\n\
            fcvt.w.s x7, f7; \n" % (n, "w" if vsew == 32 else "d", n, n), file=f)
    for n in range(1, 32):
        print("#define TEST_VFMVF_OP_rd_%d( testnum, base ) \\\n\
            li TESTNUM, testnum; \\\n\
            la a0, base; \\\n\
            fl%s f7, 0(a0); \\\n\
            vfmv.v.f v24, f7; \\\n\
            vfmv.f.s f%d, v24; \\\n\
            fcvt.w.s x8, f%d; \\\n\
            fcvt.w.s x7, f7; \n" % (n, "w" if vsew == 32 else "d", n, n), file=f)
    for n in range(1, 32):
        print("#define TEST_VFMVS_OP_rs_%d( testnum, base ) \\\n\
            li TESTNUM, testnum; \\\n\
            la a0, base; \\\n\
            fl%s f%d, 0(a0); \\\n\
            vfmv.s.f v24, f%d; \\\n\
            vfmv.f.s f8, v24; \\\n\
            fcvt.w.s x8, f8; \\\n\
            fcvt.w.s x7, f%d;\n" % (n, "w" if vsew == 32 else "d", n, n, n), file=f)
    for n in range(1, 32):
        print("#define TEST_VFMVS_OP_rsrd_%d( testnum, base ) \\\n\
            li TESTNUM, testnum; \\\n\
            la a0, base; \\\n\
            fl%s f7, 0(a0); \\\n\
            vfmv.s.f v%d, f7; \\\n\
            vfmv.f.s f8, v%d; \\\n\
            fcvt.w.s x8, f8; \\\n\
            fcvt.w.s x7, f7; \n" % (n, "w" if vsew == 32 else "d", n, n), file=f)
    for n in range(1, 32):
        print("#define TEST_VFMVS_OP_rd_%d( testnum, base ) \\\n\
            li TESTNUM, testnum; \\\n\
            la a0, base; \\\n\
            fl%s f7, 0(a0); \\\n\
            vfmv.s.f v24, f7; \\\n\
            vfmv.f.s f%d, v24; \\\n\
            fcvt.w.s x8, f%d; \\\n\
            fcvt.w.s x7, f7; \n" % (n, "w" if vsew == 32 else "d", n, n), file=f)


def generate_tests(f, lmul):
    n = 0
    print("  #-------------------------------------------------------------", file=f)
    print("  # vfmv.f.s / vfmv.v.f Tests", file=f)
    print("  #-------------------------------------------------------------", file=f)

    for i in range(len(rs1_val) - 1):
        print("  TEST_VFMVF_OP( " + str(n) + ",  fdat_rs1_" + str(i) + " );", file=f)
        n += 1
    print("  #-------------------------------------------------------------", file=f)
    print("  # vfmv.f.s / vfmv.s.f Tests", file=f)
    print("  #-------------------------------------------------------------", file=f)

    for i in range(len(rs1_val) - 1):
        print("  TEST_VFMVS_OP( " + str(n) + ",  fdat_rs2_" + str(i) + " );", file=f)
        n += 1

    print("  #-------------------------------------------------------------", file=f)
    print("  # vfmv.f.s / vfmv.v.f Tests (different register)", file=f)
    print("  #-------------------------------------------------------------", file=f)

    for i in range(1, 32):
        print("  TEST_VFMVF_OP_rs_%d( " % i + str(n) +
              ",  fdat_rs1_" + str(i) + " );", file=f)
        n += 1
        if i % lmul == 0:
            print("  TEST_VFMVF_OP_rsrd_%d( " %
                i + str(n) + ",  fdat_rs1_" + str(i) + " );", file=f)
            n += 1
        print("  TEST_VFMVF_OP_rd_%d( " % i + str(n) +
              ",  fdat_rs1_" + str(i) + " );", file=f)
        n += 1
    print("  #-------------------------------------------------------------", file=f)
    print("  # vfmv.f.s / vfmv.s.f Tests (different register)", file=f)
    print("  #-------------------------------------------------------------", file=f)

    for i in range(1, 32):
        print("  TEST_VFMVS_OP_rs_%d( " % i + str(n) +
              ",  fdat_rs1_" + str(i) + " );", file=f)
        n += 1
        if i % lmul == 0:
            print("  TEST_VFMVS_OP_rsrd_%d( " %
                i + str(n) + ",  fdat_rs1_" + str(i) + " );", file=f)
            n += 1
        print("  TEST_VFMVS_OP_rd_%d( " % i + str(n) +
              ",  fdat_rs1_" + str(i) + " );", file=f)
        n += 1
    return n


def print_ending_vfmv(f, vsew, num_tests):
    print("  #endif\n\
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

    generate_fdat_seg(f, vsew)

    print("\n\
    RVTEST_DATA_END\n", file=f)
    print_rvmodel_data([0, num_tests, 0], f)


def create_empty_test_vfmv(xlen, vlen, vsew, lmul, vta, vma, output_dir):
    logging.info("Creating empty test for {}".format(instr))

    path = "%s/%s_empty.S" % (output_dir, instr)
    f = open(path, "w+")

    # Common header files
    print_common_header(instr, f)


    # Common const information
    print_ending_vfmv(f, vsew, 0)

    f.close()
    os.system("cp %s %s" % (path, output_dir))

    logging.info(
        "Creating empty test for {}: finish in {}!".format(instr, path))

    return path


def create_first_test_vfmv(xlen, vlen, vsew, lmul, vta, vma, output_dir, rpt_path):
    logging.info("Creating first test for {}".format(instr))

    path = "%s/%s_first.S" % (output_dir, instr)
    f = open(path, "w+")

    # Common header files
    print_common_header(instr, f)

    # Generate macros to test diffrent register
    generate_macros(f, vsew)

    # Generate tests
    n = generate_tests(f, lmul)

    # Common const information
    print_ending_vfmv(f, vsew, n)

    f.close()
    os.system("cp %s %s" % (path, output_dir))

    logging.info(
        "Creating first test for {}: finish in {}!".format(instr, path))

    return path
