import os
import re
import math

mask_data_ending = [0x11111111,0x86569d27,0x429ede3d,0x20219a51,0x91a8d5fd,0xbd8f6c65,0x466250f,0xe31ffa64,0xc737ad3a,0xe54c8c1e,0x7ca660db,0x692dadf,0x2c63c847,0xfbba7ae7,0x195b62bf,0xf600a3d1,0x34b80fd4,0x3aef5ff4,0x34267ad9,0x681454c0,0x67dd3492,0xb02d663e,0xb2d3f1c5,0x824d39ae]
rd_origin_data = ["0x66da64aa","0xf682191a","0xfd2ce83f","0x67f9ab29","0x112e3ffd","0xc4d9b1e2","0x9ed4e137","0xb49ae54e","0xd075dd45","0x74daa72e","0x48324db4","0x167d97b5","0x8b536536","0xe85755eb","0x1cd86c0a","0x4c811ecf","0x8085dbf1","0x547cdce3","0x65d27882","0xb72d2ec4","0x954ee841","0xb36fd636","0xbc4988da","0xaea05c04","0xce7483a6","0xea0309d7","0x62498466","0x1cd29ac4","0x97f38b62","0x690bcf85","0x97f38b62","0x9bd83b8b"]

def get_mask_bit(index):
    return mask_data_ending[int(index / 32)] >> (index % 32) & 1


def valid_aligned_regs(reg):
    i = reg // 8
    if i == 0 or i == 3:
        return 8, 16
    elif i == 1:
        return 16, 24
    else:
        return 24, 8


def print_rvmodel_data(arr, f):
    print(" RVMODEL_DATA_BEGIN\n\
    \n\
    signature_x20_0:\n\
        .fill %d*(XLEN/32),4,0xdeadbeef\n\
    \n\
    \n\
    #ifdef rvtest_mtrap_routine\n\
    \n\
    mtrap_sigptr:\n\
        .fill 64*(XLEN/32),4,0xdeadbeef\n\
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
    RVMODEL_DATA_END\n\
    "%(arr[1]), file=f)

def generate_idx_data(f):
    vlen = int(os.environ['RVV_ATG_VLEN'])
    lmul = float(os.environ['RVV_ATG_LMUL'])
    vsew = float(os.environ['RVV_ATG_VSEW'])
    num_elem = int(vlen * lmul / vsew * 8) # 8 is max seg_size 
    print("num_elem = %d"%num_elem)
    align_step = 1 if vsew == 8 else 2 if vsew == 16 else 4 if vsew == 32 else 8
    
    print(".align 8 \n\
idx8dat:", file=f)
    for i in range(0, num_elem):
        if align_step*i > 127:
            print("    idx8dat%d:  .zero %d" % (i+1, num_elem - i + 1) * 1, file=f)
            break
        print("    idx8dat%d:  .byte %d" % (i+1, align_step*i), file=f)
    print("\n", file=f)
    
    print(".align 8 \n\
idx16dat:", file=f)
    for i in range(0, num_elem):
        if align_step*i > 32767:
            print("    idx16dat%d:   .zero %d" % (i+1, num_elem - i + 1) * 2, file=f)
            break
        print("    idx16dat%d:  .hword %d" % (i+1, align_step*i), file=f)
    print("\n", file=f)
    
    print(".align 8 \n\
idx32dat:", file=f)
    for i in range(0, num_elem):
        if align_step*i > 2147483647:
            print("    idx32dat%d:   .zero %d" % (i+1, num_elem - i + 1) * 4, file=f)
            break
        print("    idx32dat%d:  .word %d" % (i+1, align_step*i), file=f)
    print("\n", file=f)
    
    print(".align 8 \n\
idx64dat:", file=f)
    for i in range(0, num_elem):
        if align_step*i > 9223372036854775807:
            print("    idx64dat%d:   .zero %d" % (i+1, num_elem - i + 1) * 8, file=f)
            break
        print("    idx64dat%d:  .dword %d" % (i+1, align_step*i), file=f)
    print("\n\n", file=f)


def print_common_header(instr, f):
    
    masked = True if os.environ['RVV_ATG_MASKED'] == "True" else False
    print("#----------------------------------------------------------------------------- \n\
    # %s.S\n\
    #-----------------------------------------------------------------------------\n\
    #\n\
    # Test %s instructions.\n\
    #\n\n\
    #include \"model_test.h\"\n\
    #include \"arch_test.h\"\n\
    #include \"test_macros_vector.h\"\n" % (instr, instr),file=f)
    vsew = int(os.environ["RVV_ATG_VSEW"])
        
    print("RVTEST_ISA(\"RV64RV64IMAFDCVZicsr\")\n\
    \n\
    .section .text.init\n\
    .globl rvtest_entry_point\n\
    rvtest_entry_point:\n\
    \n\
    #ifdef TEST_CASE_1\n\
    \n\
    RVTEST_CASE(0,\"//check ISA:=regex(.*64.*);check ISA:=regex(.*V.*);def TEST_CASE_1=True;\",%s)\n\
    \n\
    RVMODEL_BOOT\n\
    RVTEST_CODE_BEGIN\n\
    RVTEST_VSET\n\
    \n\
    RVTEST_SIGBASE( x20,signature_x20_0)\n\
    \n\
    " % instr, file=f)


def print_common_ending(f, arr=[0,0,0]):
    print(" #endif\n\
    \n\
    RVTEST_CODE_END\n\
    RVMODEL_HALT\n\
    \n\
    .data\n\
    RVTEST_DATA_BEGIN\n\
    \n\
    TEST_DATA\n\
    \n\
    RVTEST_DATA_END\n\
    \n", file=f)
    print_rvmodel_data(arr, f)


def gen_arr_load(n, rd_data_multiplier = 1):
    vlen = int(os.environ['RVV_ATG_VLEN'])
    lmul = float(os.environ['RVV_ATG_LMUL'])
    vsew = int(os.environ['RVV_ATG_VSEW'])
    xfvcsr_num = 11  # 1 xcsr, 3 fcsr, 7 vcsr
    arr = [0, int(vlen * lmul * rd_data_multiplier / vsew) * n + xfvcsr_num * n, 0]
    return arr

def gen_arr_compute(test_num_tuple, rd_data_multiplier = 1, is_reduction = False):
    vlen = int(os.environ['RVV_ATG_VLEN'])
    lmul = float(os.environ['RVV_ATG_LMUL'])
    vsew = int(os.environ['RVV_ATG_VSEW'])
    test_num = sum(test_num_tuple)
    result_num = 1 if is_reduction else int(vlen * lmul * rd_data_multiplier / vsew)
    xfvcsr_num = 11  # 1 xcsr, 3 fcsr, 7 vcsr
    arr = [0, result_num * test_num + xfvcsr_num * test_num, 0]
    return arr


def print_common_withmask_ending(n, f, num_elem):
    print(" #endif\n\
    \n\
    RVTEST_CODE_END\n\
    RVMODEL_HALT\n\
    \n\
    .data\n\
    RVTEST_DATA_BEGIN\n\
    \n\
    TEST_DATA\n\
    \n", file=f)
    print_mask_origin_data_ending(f, num_elem)
    print("\
        RVTEST_DATA_END\n\
    \n", file=f)
    arr = gen_arr_load(n)
    print_rvmodel_data(arr, f)

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
    
    vlen = int(os.environ['RVV_ATG_VLEN'])
    lmul = float(os.environ['RVV_ATG_LMUL'])
    vsew = float(os.environ['RVV_ATG_VSEW'])
    num_elem = int(vlen * lmul / vsew)
    loop_num = int(min(len(rs1_val), len(rs2_val)) / num_elem)
    while loop_num == 0 and len(rs1_val) > 0 and len(rs2_val) > 0:
        print(len(rs1_val), len(rs2_val), num_elem, loop_num)
        rs1_val = rs1_val * 2
        rs2_val = rs2_val * 2
        loop_num = int(min(len(rs1_val), len(rs2_val)) / num_elem)
    
    return rs1_val, rs2_val

def extract_operands_fp(f, rpt_path):
    rs1_val = []
    rs2_val = []
    f = open(rpt_path)
    line = f.read()
    matchObj = re.compile(r"rs1_val ?== ?'(.*?)'")
    rs1_val = matchObj.findall(line)
    matchObj = re.compile(r"rs2_val ?== ?'(.*?)'")
    rs2_val = matchObj.findall(line)
    f.close()
    
    vlen = int(os.environ['RVV_ATG_VLEN'])
    lmul = float(os.environ['RVV_ATG_LMUL'])
    vsew = float(os.environ['RVV_ATG_VSEW'])
    num_elem = int(vlen * lmul / vsew)
    loop_num = int(min(len(rs1_val), len(rs2_val)) / num_elem)
    while loop_num == 0 and len(rs1_val) > 0 and len(rs2_val) > 0:
        print(len(rs1_val), len(rs2_val), num_elem, loop_num)
        rs1_val = rs1_val * 2
        rs2_val = rs2_val * 2
        loop_num = int(min(len(rs1_val), len(rs2_val)) / num_elem)
    
    return rs1_val, rs2_val

def is_overlap(rd, rd_mul, rs, rs_mul):
    return not ((rd > rs + rs_mul - 1) or (rd + rd_mul - 1 < rs))

def print_data_width_prefix(f, vsew):
    if vsew == 8:
        print(".byte", end="\t", file=f)
    elif vsew == 16:
        print(".hword", end="\t", file=f)
    elif vsew == 32:
        print(".word", end="\t", file=f)
    elif vsew == 64:
        print(".dword", end="\t", file=f)


def print_load_ending(f, n = 0):
    print("#endif\n\
    \n\
    RVTEST_CODE_END\n\
    RVMODEL_HALT\n\
    \n\
    .data\n\
    RVTEST_DATA_BEGIN\n\
    \n\
    TEST_DATA\n\
    \n\
    .type tdat, @object\n\
    .size tdat, 4128\n\
    .align 8 \n\
    tdat:\n\
    tdat1:  .word 0x00ff00ff\n\
    tdat2:  .word 0xff00ff00\n\
    tdat3:  .word 0x0ff00ff0\n\
    tdat4:  .word 0xf00ff00f\n\
    tdat5:  .word 0x00ff00ff\n\
    tdat6:  .word 0xff00ff00\n\
    tdat7:  .word 0x0ff00ff0\n\
    tdat8:  .word 0xf00ff00f\n\
    tdat9:  .zero 4064\n\
    tdat10:  .word 0x00ff00ff\n\
    tdat11:  .word 0xff00ff00\n\
    tdat12:  .word 0x0ff00ff0\n\
    tdat13:  .word 0xf00ff00f\n\
    tdat14:  .word 0x00ff00ff\n\
    tdat15:  .word 0xff00ff00\n\
    tdat16:  .word 0x0ff00ff0\n\
    tdat17:  .word 0xf00ff00f\n\
    \n", file=f)
    
    generate_idx_data(f)
    
    print_mask_origin_data_ending_fixed(f)
    print("\n\
    RVTEST_DATA_END\n\
    \n", file=f)
    arr = gen_arr_load(n)
    print_rvmodel_data(arr, f)

def print_loaddword_ending(f, n = 0):
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
    .type tdat, @object\n\
    .size tdat, 4128\n\
    .align 8 \n\
    tdat:\n\
    tdat1:  .dword 0x00ff00ff\n\
    tdat2:  .dword 0xff00ff00\n\
    tdat3:  .dword 0x0ff00ff0\n\
    tdat4:  .dword 0xf00ff00f\n\
    tdat5:  .dword 0x00ff00ff\n\
    tdat6:  .dword 0xff00ff00\n\
    tdat7:  .dword 0x0ff00ff0\n\
    tdat8:  .dword 0xf00ff00f\n\
    tdat9:  .zero 4064\n\
    tdat10:  .dword 0x00ff00ff\n\
    tdat11:  .dword 0xff00ff00\n\
    tdat12:  .dword 0x0ff00ff0\n\
    tdat13:  .dword 0xf00ff00f\n\
    tdat14:  .dword 0x00ff00ff\n\
    tdat15:  .dword 0xff00ff00\n\
    tdat16:  .dword 0x0ff00ff0\n\
    tdat17:  .dword 0xf00ff00f\n\
    \n", file=f)
    
    generate_idx_data(f)
    
    
    print("\n\
    RVTEST_DATA_END\n\
    \n", file=f)
    arr = gen_arr_load(n)
    print_rvmodel_data(arr, f)


def print_loadls_ending(f, n = 0):
    print("#endif\n\
    \n\
    RVTEST_CODE_END\n\
    RVMODEL_HALT\n\
    \n\
    .data\n\
    RVTEST_DATA_BEGIN\n\
    \n\
    TEST_DATA\n\
    \n\
    .type tsdat, @object\n\
    .size tsdat, 1049856\n\
    tsdat:\n\
    tsdat1:  .zero 524800\n\
    tsdat2:  .word 0x00ff00ff\n\
    tsdat3:  .word 0xff00ff00\n\
    tsdat4:  .word 0x0ff00ff0\n\
    tsdat5:  .word 0xf00ff00f\n\
    tsdat6:  .word 0x00ff00ff\n\
    tsdat7:  .word 0xff00ff00\n\
    tsdat8:  .word 0x0ff00ff0\n\
    tsdat9:  .word 0xf00ff00f\n\
    tsdat10: .zero 524800\n\
    \n\
    .type tdat, @object\n\
    .size tdat, 4128\n\
    .align 8 \n\
    tdat:\n\
    tdat1:  .word 0x00ff00ff\n\
    tdat2:  .word 0xff00ff00\n\
    tdat3:  .word 0x0ff00ff0\n\
    tdat4:  .word 0xf00ff00f\n\
    tdat5:  .word 0x00ff00ff\n\
    tdat6:  .word 0xff00ff00\n\
    tdat7:  .word 0x0ff00ff0\n\
    tdat8:  .word 0xf00ff00f\n\
    tdat9:  .zero 4064\n\
    tdat10:  .word 0x00ff00ff\n\
    tdat11:  .word 0xff00ff00\n\
    tdat12:  .word 0x0ff00ff0\n\
    tdat13:  .word 0xf00ff00f\n\
    tdat14:  .word 0x00ff00ff\n\
    tdat15:  .word 0xff00ff00\n\
    tdat16:  .word 0x0ff00ff0\n\
    tdat17:  .word 0xf00ff00f\n\
    \n", file=f)
    generate_idx_data(f)
    
    print("\n\
    RVTEST_DATA_END\n\
    \n", file=f)
    arr = gen_arr_load(n)
    print_rvmodel_data(arr, f)


def print_loadlr_ending(f, n = 0):
    print("#endif\n\
    \n\
    RVTEST_CODE_END\n\
    RVMODEL_HALT\n\
    \n\
    .data\n\
    RVTEST_DATA_BEGIN\n\
    \n\
    TEST_DATA\n\
    \n\
    .type tdat, @object\n\
    .size tdat, 8448\n\
    .align 8 \n\
    tdat:\n\
    tdat1:  .word 0x00ff00ff\n\
    tdat2:  .word 0xff00ff00\n\
    tdat3:  .word 0x0ff00ff0\n\
    tdat4:  .word 0xf00ff00f\n\
    tdat5:  .word 0x00ff00ff\n\
    tdat6:  .word 0xff00ff00\n\
    tdat7:  .word 0x0ff00ff0\n\
    tdat8:  .word 0xf00ff00f\n\
    tdta28:  .zero 7584\n\
    tdat9:  .zero 32\n\
    tdat10:  .word 0x00ff00ff\n\
    tdat11:  .word 0xff00ff00\n\
    tdat12:  .word 0x0ff00ff0\n\
    tdat13:  .word 0xf00ff00f\n\
    tdat14:  .word 0x00ff00ff\n\
    tdat15:  .word 0xff00ff00\n\
    tdat16:  .word 0x0ff00ff0\n\
    tdat17:  .word 0xf00ff00f\n\
    tdta18:  .zero 32\n\
    tdat19:  .word 0x00ff00ff\n\
    tdat20:  .word 0xff00ff00\n\
    tdat21:  .word 0x0ff00ff0\n\
    tdat22:  .word 0xf00ff00f\n\
    tdat23:  .word 0x00ff00ff\n\
    tdat24:  .word 0xff00ff00\n\
    tdat25:  .word 0x0ff00ff0\n\
    tdat26:  .word 0xf00ff00f\n\
    tdta27:  .zero 32\n\
    \n", file=f)
    print_mask_origin_data_ending_fixed(f)
    print("\n\
    RVTEST_DATA_END\n\
    \n", file=f)
    arr = gen_arr_load(n)
    print_rvmodel_data(arr, f)

def print_mask_origin_data_ending_fixed(f):
    # 24 words, mask_data + 0/64/128
    print_mask_data_ending_fixed(f)
    # 32 words, rd_origin_data + 0/64/128/192
    print_origin_data_ending(f)

def print_mask_origin_data_ending(f, num_elem):
    print_mask_data_ending(f, num_elem)
    print_origin_data_ending(f)

def print_mask_data_ending_fixed(f):
    print("\n.align 4", file=f)
    print("mask_data:", file=f)
    for i in range(len(mask_data_ending)):
        print(".word\t%s"%mask_data_ending[i], file=f)
        
def print_mask_data_ending(f, num_elem):
    print("\n.align 4", file=f)
    print("mask_data:", file=f)
    num_bytes = math.ceil(num_elem / 8) # vlm to load mask: ceil(vl/8) bytes
    num_words = math.ceil(num_bytes / 4)
    # total: 2 * num_elem + 2 + 2
    #all_one = '1' * num_elem
    #all_zero = '0' * num_elem
    for i in range(num_elem):
        walking_one = 1 << i
        walking_zero = ~(1 << i)
        for j in range(num_words):
            t1 = walking_one % (1 << 32)
            walking_one = walking_one // (1 << 32)
            print(".word\t%s"%'{:#08x}'.format(t1), file=f)
        for j in range(num_words):
            t0 = walking_zero % (1 << 32)
            walking_zero = walking_zero // (1 << 32)
            print(".word\t%s"%'{:#08x}'.format(t0), file=f)
    #all_zero
    for i in range(num_words):
        print(".word\t%s"%'{:#08x}'.format(0x0), file=f)
    #all_one
    for i in range(num_words):
        print(".word\t%s"%'{:#08x}'.format(0xffffffff), file=f)
    # checkerboard
    for i in range(num_words):
        print(".word\t%s"%'{:#08x}'.format(0x55555555), file=f)
    for i in range(num_words):
        print(".word\t%s"%'{:#08x}'.format(0xaaaaaaaa), file=f)
    
  
def print_origin_data_ending(f):
    print("\n.align 4", file=f)
    print("rd_origin_data:", file=f)
    for i in range(len(rd_origin_data)):
        print(".word\t%s"%rd_origin_data[i], file=f)


def print_common_ending_rs1rs2rd_vvvxvi(rs1_val, rs2_val, test_num_tuple, vsew, f, generate_vi = True, generate_vx = True, generate_vv = True, rs1_data_multiplier = 1, rs2_data_multiplier = 1, rd_data_multiplier = 1, is_reduction = False):
    vlen = int(os.environ['RVV_ATG_VLEN'])
    lmul = float(os.environ['RVV_ATG_LMUL'])
    num_elem = int(vlen * lmul / vsew)
    loop_num = int(min(len(rs1_val), len(rs2_val)) / num_elem)

    print("!!!!!loop_num=%d, vv_test_num=%d"%(loop_num, test_num_tuple[0]))
    print("#endif\n\
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
    print(".align %d"%(int(vsew * rs1_data_multiplier / 8)), file=f)
    print("rs1_data:", file=f)
    for i in range(len(rs1_val)):
        print_data_width_prefix(f, vsew * rs1_data_multiplier)
        print("%s"%rs1_val[i], file=f)
    
    print("\n.align %d"%(int(vsew * rs2_data_multiplier / 8)), file=f)
    print("rs2_data:", file=f)
    for i in range(len(rs2_val)):
        print_data_width_prefix(f, vsew * rs2_data_multiplier)
        print("%s"%rs2_val[i], file=f)

    if generate_vv:
        print("\n.align %d"%(int(vsew * rd_data_multiplier / 8)), file=f)
        print("rd_data_vv:", file=f)
        for i in range(test_num_tuple[0] * num_elem):
            print_data_width_prefix(f, vsew)
            print("0x5201314", file=f)

    if generate_vx:
        print("\n.align %d"%(int(vsew * rd_data_multiplier / 8)), file=f)
        print("\nrd_data_vx:", file=f)
        for i in range(test_num_tuple[1] * num_elem):
            print_data_width_prefix(f, vsew)
            print("0x5201314", file=f)

    if generate_vi:
        print("\n.align %d"%(int(vsew * rd_data_multiplier / 8)), file=f)
        print("\nrd_data_vi:", file=f)
        for i in range(test_num_tuple[2] * num_elem):
            print_data_width_prefix(f, vsew)
            print("0x5201314", file=f)
    
    print_mask_origin_data_ending(f, num_elem)
    print("\n\
    RVTEST_DATA_END\n\
    \n", file=f)
    arr = gen_arr_compute(test_num_tuple, rd_data_multiplier, is_reduction=is_reduction)
    print_rvmodel_data(arr, f)

def print_common_ending_rs1rs2rd_vw(rs1_val, rs2_val, test_num_tuple, vsew, f, rs1_data_multiplier = 1, rs2_data_multiplier = 1, rd_data_multiplier = 1, generate_wvwx = True, is_reduction = False):
    # test_num_tuple is vv_test_num, vx_test_num, wv_test_num, wx_test_num
    vlen = int(os.environ['RVV_ATG_VLEN'])
    lmul = float(os.environ['RVV_ATG_LMUL'])
    num_elem = int(vlen * lmul / vsew)
    loop_num = int(min(len(rs1_val), len(rs2_val)) / num_elem)

    print("!!!!!loop_num=%d"%(loop_num))
    print("#endif\n\
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
    print(".align %d"%(int(vsew * rs1_data_multiplier / 8)), file=f)
    print("rs1_data:", file=f)
    for i in range(len(rs1_val)):
        print_data_width_prefix(f, vsew * rs1_data_multiplier)
        print("%s"%rs1_val[i], file=f)
    
    print(".align %d"%(int(vsew * rs1_data_multiplier * 2 / 8)), file=f)
    print("rs1_data_widen:", file=f)
    for i in range(len(rs1_val)):
        print_data_width_prefix(f, vsew * rs1_data_multiplier * 2)
        print("%s"%rs1_val[i], file=f)
    
    print("\n.align %d"%(int(vsew * rs2_data_multiplier / 8)), file=f)
    print("rs2_data:", file=f)
    for i in range(len(rs2_val)):
        print_data_width_prefix(f, vsew * rs2_data_multiplier)
        print("%s"%rs2_val[i], file=f)

    print(".align %d"%(int(vsew * rs2_data_multiplier * 2 / 8)), file=f)
    print("rs2_data_widen:", file=f)
    for i in range(len(rs2_val)):
        print_data_width_prefix(f, vsew * rs2_data_multiplier * 2)
        print("%s"%rs2_val[i], file=f)

    if is_reduction == False:
        print("\n.align %d"%(int(vsew * rd_data_multiplier / 8)), file=f)
        print("rd_data_vv:", file=f)
        for i in range(test_num_tuple[0] * num_elem):
            print_data_width_prefix(f, vsew * 2)
            print("0x5201314", file=f)
        print("\nrd_data_vx:", file=f)
        for i in range(test_num_tuple[1] * num_elem):
            print_data_width_prefix(f, vsew * 2)
            print("0x5201314", file=f)

    if generate_wvwx:
        print("\n.align %d"%(int(vsew * rd_data_multiplier * 2 / 8)), file=f)
        print("\nrd_data_wv:", file=f)
        for i in range(test_num_tuple[2] * num_elem):
            print_data_width_prefix(f, vsew * 2)
            print("0x5201314", file=f)
        print("\nrd_data_wx:", file=f)
        for i in range(test_num_tuple[3] * num_elem):
            print_data_width_prefix(f, vsew * 2)
            print("0x5201314", file=f)
    
    print_mask_origin_data_ending(f, num_elem)
    print("\n\
    RVTEST_DATA_END\n\
    \n", file=f)
    arr = gen_arr_compute(test_num_tuple, rd_data_multiplier, is_reduction=is_reduction)
    print_rvmodel_data(arr, f)


def print_common_ending_rs1rs2rd_vvvfrv(rs1_val, rs2_val, test_num_tuple, vsew, f, generate_vv = True, generate_vf = True, generate_rv = False, rs1_data_multiplier = 1, rs2_data_multiplier = 1, rd_data_multiplier = 1):
    vlen = int(os.environ['RVV_ATG_VLEN'])
    lmul = float(os.environ['RVV_ATG_LMUL'])
    num_elem = int(vlen * lmul / vsew)
    loop_num = int(min(len(rs1_val), len(rs2_val)) / num_elem)
    lmul_1 = 1 if lmul < 1 else int(lmul)
    num_elem_1 = int(vlen * lmul_1 / vsew)

    print("!!!!!loop_num=%d, vv_test_num=%d"%(loop_num, test_num_tuple[0]))
    print(" #endif\n\
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
    print(".align %d"%(int(vsew * rs1_data_multiplier / 8)), file=f)
    print("rs1_data:", file=f)
    for i in range(len(rs1_val)):
        print_data_width_prefix(f, vsew * rs1_data_multiplier)
        print("%s"%rs1_val[i], file=f)
    
    print("\n.align %d"%(int(vsew * rs2_data_multiplier / 8)), file=f)
    print("rs2_data:", file=f)
    for i in range(len(rs2_val)):
        print_data_width_prefix(f, vsew * rs2_data_multiplier)
        print("%s"%rs2_val[i], file=f)

    print("\n.align %d"%(int(vsew * rd_data_multiplier / 8)), file=f)
    if generate_vv:
        print("rd_data_vv:", file=f)
        for i in range(test_num_tuple[0] * num_elem):
            print_data_width_prefix(f, vsew)
            print("0x5201314", file=f)

    if generate_vf:
        print("\nrd_data_vf:", file=f)
        for i in range(test_num_tuple[1] * num_elem):
            print_data_width_prefix(f, vsew)
            print("0x5201314", file=f)

    if generate_rv:
        print("\nrd_data_rv:", file=f)
        for i in range(test_num_tuple[2] * num_elem):
            print_data_width_prefix(f, vsew)
            print("0x5201314", file=f)
    print_mask_origin_data_ending(f, num_elem)

    print("\n\
    RVTEST_DATA_END\n\
    \n", file=f)
    arr = gen_arr_compute(test_num_tuple, rd_data_multiplier)
    print_rvmodel_data(arr, f)


def print_common_ending_rs1rs2rd_wvwf(rs1_val, rs2_val, test_num_tuple, vsew, f, generate_vv = True, generate_vf = True, rs1_data_multiplier = 1, rs2_data_multiplier = 1, rd_data_multiplier = 1, generate_wvwf = True, is_reduction = False):
    vlen = int(os.environ['RVV_ATG_VLEN'])
    lmul = float(os.environ['RVV_ATG_LMUL'])
    num_elem = int(vlen * lmul / vsew)
    loop_num = int(min(len(rs1_val), len(rs2_val)) / num_elem)
    lmul_1 = 1 if lmul < 1 else int(lmul)
    num_elem_1 = int(vlen * lmul_1 / vsew)

    print(test_num_tuple)
    print("#endif\n\
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
    print(".align %d"%(int(vsew * rs1_data_multiplier / 8)), file=f)
    print("rs1_data:", file=f)
    for i in range(len(rs1_val)):
        print_data_width_prefix(f, vsew * rs1_data_multiplier)
        print("%s"%rs1_val[i], file=f)
    
    print(".align %d"%(int(vsew * rs1_data_multiplier * 2 / 8)), file=f)
    print("rs1_data_widen:", file=f)
    for i in range(len(rs1_val)):
        print_data_width_prefix(f, vsew * rs1_data_multiplier * 2)
        print("%s"%rs1_val[i], file=f)
    
    print("\n.align %d"%(int(vsew * rs2_data_multiplier / 8)), file=f)
    print("rs2_data:", file=f)
    for i in range(len(rs2_val)):
        print_data_width_prefix(f, vsew * rs2_data_multiplier)
        print("%s"%rs2_val[i], file=f)

    print(".align %d"%(int(vsew * rs1_data_multiplier * 2 / 8)), file=f)
    print("rs2_data_widen:", file=f)
    for i in range(len(rs2_val)):
        print_data_width_prefix(f, vsew * rs2_data_multiplier * 2)
        print("%s"%rs1_val[i], file=f)

    if generate_vv:
        print("\n.align %d"%(int(vsew * rd_data_multiplier * 2 / 8)), file=f)
        print("rd_data_vv:", file=f)
        for i in range(test_num_tuple[0] * num_elem):
            print_data_width_prefix(f, vsew * 2)
            print("0x5201314", file=f)

    if generate_vf:
        print("\n.align %d"%(int(vsew * rd_data_multiplier * 2 / 8)), file=f)
        print("\nrd_data_vf:", file=f)
        for i in range(test_num_tuple[1] * num_elem):
            print_data_width_prefix(f, vsew * 2)
            print("0x5201314", file=f)

    if generate_wvwf:
        print("\n.align %d"%(int(vsew * rd_data_multiplier * 2 / 8)), file=f)
        print("\nrd_data_wv:", file=f)
        for i in range(test_num_tuple[2] * num_elem):
            print_data_width_prefix(f, vsew * 2)
            print("0x5201314", file=f)
        print("\nrd_data_wf:", file=f)
        for i in range(test_num_tuple[3] * num_elem):
            print_data_width_prefix(f, vsew * 2)
            print("0x5201314", file=f)
    
    print_mask_origin_data_ending(f, num_elem)
    print("\n\
    RVTEST_DATA_END\n\
    \n", file=f)
    arr = gen_arr_compute(test_num_tuple, rd_data_multiplier, is_reduction=is_reduction)
    print_rvmodel_data(arr, f)


def print_common_ending_rs1rs2rd_vfcvt(rs1_val, rs1_int_val, test_num_tuple, vsew, f, is_widen = False, is_narrow = False):
    vlen = int(os.environ['RVV_ATG_VLEN'])
    lmul = float(os.environ['RVV_ATG_LMUL'])
    num_elem = int(vlen * lmul / vsew)
    loop_num = int(len(rs1_val) / num_elem)
    lmul_1 = 1 if lmul < 1 else int(lmul)
    num_elem_1 = int(vlen * lmul_1 / vsew)

    print("#endif\n\
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
    rs1_data_multiplier = 2 if is_narrow else 1
    rd_data_multiplier = 2 if is_widen else 1
    print(".align %d"%(int(vsew * rs1_data_multiplier / 8)), file=f)
    print("rs1_data:", file=f)
    for i in range(len(rs1_val)):
        print_data_width_prefix(f, vsew * rs1_data_multiplier)
        print("%s"%rs1_val[i], file=f)

    print(".align %d"%(int(vsew * rs1_data_multiplier / 8)), file=f)
    print("rs1_data_int:", file=f)
    for i in range(len(rs1_int_val)):
        print_data_width_prefix(f, vsew * rs1_data_multiplier)
        print("%s"%rs1_val[i], file=f)
    
    print("\n.align %d"%(int(vsew * rd_data_multiplier / 8)), file=f)
    print("rd_data:", file=f)
    for i in range(test_num_tuple[0] * num_elem):
        print_data_width_prefix(f, vsew * rd_data_multiplier)
        print("0x5201314", file=f)

    print("\nrd_data_int:", file=f)
    for i in range(test_num_tuple[1] * num_elem):
        print_data_width_prefix(f, vsew * rd_data_multiplier)
        print("0x5201314", file=f)

    print_mask_origin_data_ending(f, num_elem)
    print("\n\
    RVTEST_DATA_END\n\
    \n", file=f)
    arr = gen_arr_compute(test_num_tuple, rd_data_multiplier)
    print_rvmodel_data(arr, f)



