import logging
import os
from scripts.test_common_info import *
from scripts.create_test_permute.create_test_common import print_ending_mv
import re

instr = 'vmvnr'
nreg_list = [1, 2, 4, 8]


def generate_macros_vmvnr(f, vsew, lmul):
    vlen = int(os.environ['RVV_ATG_VLEN'])
    
    for nreg in nreg_list:
        emul = nreg
        evl = emul * vlen / vsew
        
        print("#define TEST_VMV%dR_OP( testnum, inst,  src_base ) "%(nreg) + " \\\n\
        TEST_CASE_VREG( testnum, v16, %d,  "%nreg + " \\\n\
            la x7, rd_origin_data; \\\n\
            vl%dre%d.v v16, (x7);"%(nreg, vsew) + " \\\n\
            la  x7, src_base; \\\n\
            vl%dre%d.v v8, (x7); "%(nreg, vsew) + " \\\n\
            inst v16, v8; \\\n\
        ) ", file=f)
        
        for n in range(0, 32):
            if n % emul != 0:
                continue
            vs2 = 24 if n == 8 else 8
            print("#define TEST_VMV%dR_OP_vd_%d( testnum, inst,  src_base )"%(nreg, n) + " \\\n\
            TEST_CASE_VREG( testnum, v%d, %d,  "%(n, nreg) + " \\\n\
                la x7, rd_origin_data; \\\n\
                vl%dre%d.v v%d, (x7);"%(nreg, vsew, n) + " \\\n\
                la  x7, src_base; \\\n\
                vl%dre%d.v v%d, (x7); "%(nreg, vsew, vs2) + " \\\n\
                inst v%d, v%d;"%(n, vs2)+" \\\n\
            ) ", file=f)
        for n in range(0, 32):
            if n % emul != 0:
                continue
            vd = 24 if n == 16 else 16
            print("#define TEST_VMV%dR_OP_vs2_%d( testnum, inst,  src_base )"%(nreg, n) + " \\\n\
            TEST_CASE_VREG( testnum, v%d, %d,  "%(vd, nreg) + " \\\n\
                la x7, rd_origin_data; \\\n\
                vl%dre%d.v v%d, (x7);"%(nreg, vsew, vd) + " \\\n\
                la  x7, src_base; \\\n\
                vl%dre%d.v v%d, (x7); "%(nreg, vsew, n) + " \\\n\
                inst v%d, v%d;"%(vd, n)+" \\\n\
            ) ", file=f)


def generate_tests_vmvnr(f, rs_val, vsew, lmul):
    vlen = int(os.environ['RVV_ATG_VLEN'])
    
    n = 0
    test_num_list = []
    for nreg in nreg_list:
        emul = nreg
        evl = int(emul * vlen / vsew)
        if evl == 0:
            return 0
        loop_num = int(len(rs_val) / evl)
        # print(len(rs_val), evl, loop_num)
        step_bytes = int(vlen * emul / 8)
        
        print("  #-------------------------------------------------------------",file=f)
        print("  # VMV%dR Tests"%nreg, file=f)
        print("  #-------------------------------------------------------------",file=f)
        
        for i in range(len(rs_val)):
            n += 1
            print("  TEST_VMV%dR_OP( %d, vmv%dr.v, rs_data+%d )"%(nreg, n, nreg, i*step_bytes), file=f)
        
        for i in range(0, 32):
            if i % emul != 0:
                continue
            k = i % loop_num
            n += 1
            print("  TEST_VMV%dR_OP_vd_%d( %d, vmv%dr.v, rs_data+%d )"%(nreg, i, n, nreg, k*step_bytes), file=f)
            n += 1
            print("  TEST_VMV%dR_OP_vs2_%d( %d, vmv%dr.v, rs_data+%d )"%(nreg, i, n, nreg, k*step_bytes), file=f)
        
        test_num_list.append(n - sum(test_num_list))
    
    return tuple(test_num_list)


def create_empty_test_vmvnr(xlen, vlen, vsew, lmul, vta, vma, output_dir):
    logging.info("Creating empty test for {}".format(instr))

    path = "%s/%s_empty.S" % (output_dir, instr)
    f = open(path, "w+")

    # Common header files
    print_common_header(instr, f)

    # Common const information
    print_common_ending(f)
    
    f.close()
    os.system("cp %s %s" % (path, output_dir))

    logging.info(
        "Creating empty test for {}: finish in {}!".format(instr, path))

    return path


def create_first_test_vmvnr(xlen, vlen, vsew, lmul, vta, vma, output_dir, rpt_path):
    logging.info("Creating first test for {}".format(instr))

    path = "%s/%s_first.S" % (output_dir, instr)
    f = open(path, "w+")

    # Common header files
    print_common_header(instr, f)

    # Extract operands
    rs1_val, rs2_val = extract_operands(f, rpt_path)

    # Generate macros to test diffrent register
    generate_macros_vmvnr(f, vsew, lmul)

    # Generate tests
    test_num_tuple = generate_tests_vmvnr(f, rs2_val, vsew, lmul)

    # Common const information
    print_ending_mv(f, rs2_val, test_num_tuple, vlen, vsew, lmul, is_vmvnr = True)
    
    f.close()
    os.system("cp %s %s" % (path, output_dir))

    logging.info(
        "Creating first test for {}: finish in {}!".format(instr, path))

    return path