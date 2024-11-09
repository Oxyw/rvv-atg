import logging
import os
from scripts.test_common_info import *


instr = 'vsr' # vs<nf>r
nf_list = [1, 2, 4, 8]


def generate_macros_vsr(f):
    for nf in nf_list:
        print("#define TEST_VS%dR_OP( testnum, base )"%(nf) + " \\\n\
        TEST_CASE_VREG( testnum, v8, %d, "%(nf) + " \\\n\
            la  x7, base; \\\n\
            vl%dr.v v8, (x7);"%(nf) + " \\\n\
        )", file=f)
        
        for n in range(1, 32):
            if not is_aligned(n, nf):
                continue
            print("#define TEST_VS%dR_OP_vs3_%d( testnum, base )"%(nf, n) + " \\\n\
            TEST_CASE_VREG( testnum, v%d, %d, "%(n, nf) + " \\\n\
                la  x7, base; \\\n\
                vl%dr.v v%d, (x7);"%(nf, n) + " \\\n\
            )", file=f)


def generate_tests_vsr(f, vsew):
    n = 0
    vr_num = 0
    print("  #-------------------------------------------------------------", file=f)
    print("  # vs<nf>r Tests", file=f)
    print("  #-------------------------------------------------------------", file=f)

    for i in range(2):
        for nf in nf_list:
            n += 1
            print("  TEST_VS%dR_OP( "%nf+str(n)+", 0 + tdat );", file=f)
            vr_num += nf
            n += 1
            print("  TEST_VS%dR_OP( "%nf+str(n)+", %d + tdat"%(vsew//8)+" );", file=f)
            vr_num += nf
    
    for nf in nf_list:
        for i in range(1, 32):
            if not is_aligned(i, nf):
                continue
            n += 1
            print("  TEST_VS%dR_OP_vs3_%d( "%(nf, i)+str(n)+", 0 + tdat );", file=f)
            vr_num += nf

    return (n, vr_num)


def create_empty_test_vsr(xlen, vlen, vsew, lmul, vta, vma, output_dir):
    logging.info("Creating empty test for {}".format(instr))

    path = "%s/%s_empty.S" % (output_dir, instr)
    f = open(path, "w+")

    # Common header files
    print_common_header(instr, f)

    # Common const information

    # Load const information
    print_load_ending(f, vsew)

    f.close()
    os.system("cp %s %s" % (path, output_dir))

    logging.info(
        "Creating empty test for {}: finish in {}!".format(instr, path))

    return path


def create_first_test_vsr(xlen, vlen, vsew, lmul, vta, vma, output_dir, rpt_path):
    logging.info("Creating first test for {}".format(instr))

    path = "%s/%s_first.S" % (output_dir, instr)
    f = open(path, "w+")

    # Common header files
    print_common_header(instr, f)

    # Generate macros to test diffrent register
    generate_macros_vsr(f)
    
    # Generate tests
    (n, vr_num) = generate_tests_vsr(f, vsew)

    # Common const information

    # Load const information
    print_load_ending(f, vsew, n, is_vsr = True, seg = vr_num)

    f.close()
    os.system("cp %s %s" % (path, output_dir))

    logging.info(
        "Creating first test for {}: finish in {}!".format(instr, path))

    return path
