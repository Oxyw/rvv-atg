import os
import re
import math

mask_data_ending = [0x11111111,0x86569d27,0x429ede3d,0x20219a51,0x91a8d5fd,0xbd8f6c65,0x466250f,0xe31ffa64,0xc737ad3a,0xe54c8c1e,0x7ca660db,0x692dadf,0x2c63c847,0xfbba7ae7,0x195b62bf,0xf600a3d1,0x34b80fd4,0x3aef5ff4,0x34267ad9,0x681454c0,0x67dd3492,0xb02d663e,0xb2d3f1c5,0x824d39ae]
rd_origin_data = ["0x66da64aa","0xf682191a","0xfd2ce83f","0x67f9ab29","0x112e3ffd","0xc4d9b1e2","0x9ed4e137","0xb49ae54e","0xd075dd45","0x74daa72e","0x48324db4","0x167d97b5","0x8b536536","0xe85755eb","0x1cd86c0a","0x4c811ecf","0x8085dbf1","0x547cdce3","0x65d27882","0xb72d2ec4","0x954ee841","0xb36fd636","0xbc4988da","0xaea05c04","0xce7483a6","0xea0309d7","0x62498466","0x1cd29ac4","0x97f38b62","0x690bcf85","0x97f38b62","0x9bd83b8b"]

def get_mask_bit(index):
    return mask_data_ending[int(index / 32)] >> (index % 32) & 1


def is_overlap(rd, rd_mul, rs, rs_mul):
    return ((rd <= rs + rs_mul - 1) and (rd + rd_mul - 1 >= rs))


def is_aligned(val, pos):
    return (val & (pos - 1) == 0) if pos else True


def get_aligned_reg(reg, lmul_reg, lmul_target, nf = 1):
    lmul_reg_1 = max(1, lmul_reg)
    lmul_target_1 = max(1, lmul_target)
    for i in range(1, 32):
        if i % lmul_target != 0 or i == reg:
            continue
        if i + lmul_target_1 * nf > 32:
            break
        if (i > reg + lmul_reg_1 * nf - 1) or (i + lmul_target_1 * nf - 1 < reg):
            return i
    return 0

def get_aligned_regs(reg, lmul_reg, lmul_target1, lmul_target2):
    for i in range(1, 32):
        if i % lmul_target1 != 0 or i == reg:
            continue
        for j in range(1, 32):
            if j % lmul_target2 != 0 or j == reg or i == j:
                continue
            if ((i > reg + lmul_reg - 1) or (i + lmul_target1 - 1 < reg)) and \
               ((j > reg + lmul_reg - 1) or (j + lmul_target2 - 1 < reg)) and \
               ((i + lmul_target1 - 1 < j or j + lmul_target2 - 1 < i)):
                return (i, j)
    return (0, 0)


def valid_aligned_regs(reg):
    i = reg // 8
    if i == 0 or i == 3:
        return 8, 16
    elif i == 1:
        return 16, 24
    else:
        return 24, 8


def print_rvmodel_data(arr, f):
    print("\n\
    RVMODEL_DATA_BEGIN\n\
    \n\
    signature_x20_0:\n\
        .fill %d+%d*(XLEN/32)+%d*(VLEN/32),4,0xdeadbeef\n\
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
    "%(arr[0], arr[1], arr[2]), file=f)

# TODO: include positive and negative index
def generate_idx_data(f, eew):
    vlen = int(os.environ['RVV_ATG_VLEN'])
    lmul = float(os.environ['RVV_ATG_LMUL'])
    vsew = float(os.environ['RVV_ATG_VSEW'])
    num_elem = int(vlen * lmul / vsew)
    print("num_elem = %d"%num_elem)
    align_step = 1 if vsew == 8 else 2 if vsew == 16 else 4 if vsew == 32 else 8
    
    if eew == 8:
        print(".align 8 \n idx8dat:", file=f)
        for i in range(0, num_elem):
            if align_step*i > 127:
                print("    idx8dat%d:  .zero %d" % (i+1, num_elem - i + 1) * 1, file=f)
                break
            print("    idx8dat%d:  .byte %d" % (i+1, align_step*i), file=f)
        print("\n", file=f)
    elif eew == 16:
        print(".align 8 \n idx16dat:", file=f)
        for i in range(0, num_elem):
            if align_step*i > 32767:
                print("    idx16dat%d:   .zero %d" % (i+1, num_elem - i + 1) * 2, file=f)
                break
            print("    idx16dat%d:  .hword %d" % (i+1, align_step*i), file=f)
        print("\n", file=f)
    elif eew == 32:
        print(".align 8 \n idx32dat:", file=f)
        for i in range(0, num_elem):
            if align_step*i > 2147483647:
                print("    idx32dat%d:   .zero %d" % (i+1, num_elem - i + 1) * 4, file=f)
                break
            print("    idx32dat%d:  .word %d" % (i+1, align_step*i), file=f)
        print("\n", file=f)
    elif eew == 64:
        print(".align 8 \n idx64dat:", file=f)
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


def print_common_ending(f, test_num = 0, print_data = False):
    print("\n\
    #endif\n\
    \n\
    RVTEST_CODE_END\n\
    RVMODEL_HALT\n\
    \n\
    .data\n\
    RVTEST_DATA_BEGIN\n\
    \n\
    TEST_DATA\n\
    \n", file=f)
    
    if print_data:
        print_mask_origin_data_ending(f)
    
    print("\n\
    RVTEST_DATA_END\n\
    \n", file=f)
    
    arr = gen_arr_compute(test_num)
    print_rvmodel_data(arr, f)


def gen_arr_load(n, eew, is_vse = False, is_vsr = False, is_vlr = False, seg = 1):
    vlen = int(os.environ['RVV_ATG_VLEN'])
    lmul = float(os.environ['RVV_ATG_LMUL'])
    vsew = int(os.environ['RVV_ATG_VSEW'])
    xfvcsr_num = 11  # 1 xcsr, 3 fcsr, 7 vcsr
    if is_vse: # vse<eew> and vsseg<nf>e<eew>
        arr = [seg, xfvcsr_num * n, 0]
    elif is_vsr: # vs<nf>r
        arr = [0, xfvcsr_num * n, seg]
    elif is_vlr: # vl<nf>re<eew>
        vl = int(vlen / eew)
        arr = [0, vl * seg + xfvcsr_num * n, 0]
    else:
        elem_num = int(vlen * lmul / vsew)
        if seg == 1:
            arr = [0, elem_num * n + xfvcsr_num * n, 0]
        else:
            arr = [0, elem_num * seg + xfvcsr_num * n, 0]
    return arr

def gen_arr_compute(test_num_tuple, is_reduction = False, is_mask = False):
    vlen = int(os.environ['RVV_ATG_VLEN'])
    lmul = float(os.environ['RVV_ATG_LMUL'])
    vsew = int(os.environ['RVV_ATG_VSEW'])
    
    test_num = test_num_tuple if isinstance(test_num_tuple, int) else sum(test_num_tuple)
    elem_num = int(vlen * lmul / vsew)
    xfvcsr_num = 11  # 1 xcsr, 3 fcsr, 7 vcsr
    if is_mask:
        arr = [0, xfvcsr_num * test_num, test_num]
    else:
        result_num = test_num if is_reduction else elem_num * test_num
        arr = [0, result_num + xfvcsr_num * test_num, 0]
    return arr


def extract_operands(f, rpt_path, is_rs1_mask = False, is_rs2_mask = False):
    vlen = int(os.environ['RVV_ATG_VLEN'])
    lmul = float(os.environ['RVV_ATG_LMUL'])
    vsew = float(os.environ['RVV_ATG_VSEW'])
    num_elem = int(vlen * lmul / vsew)
    
    rs1_val = []
    rs2_val = []
    f = open(rpt_path)
    line = f.read()
    
    matchObj = re.compile('rs1_val ?== ?(-?\d+)')
    rs1_val_10 = matchObj.findall(line)
    if is_rs1_mask: # No '0x' prefix
        rs1_val = [hex(int(x))[2:].zfill(8 * math.ceil(num_elem / 32)) # num_elem bits, num_elem/32 words
                   for x in rs1_val_10]
    else:
        rs1_val = ['{:#016x}'.format(int(x) & 0xffffffffffffffff)
                   for x in rs1_val_10]
    
    matchObj = re.compile('rs2_val ?== ?(-?\d+)')
    rs2_val_10 = matchObj.findall(line)
    if is_rs2_mask: # No '0x' prefix
        rs2_val = [hex(int(x))[2:].zfill(8 * math.ceil(num_elem / 32)) # num_elem bits, num_elem/32 words
                   for x in rs2_val_10]
    else:
        rs2_val = ['{:#016x}'.format(int(x) & 0xffffffffffffffff)
                    for x in rs2_val_10]
    f.close()
    
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


def print_data_width_prefix(f, vsew):
    if vsew == 8:
        print(".byte", end="\t", file=f)
    elif vsew == 16:
        print(".hword", end="\t", file=f)
    elif vsew == 32:
        print(".word", end="\t", file=f)
    elif vsew == 64:
        print(".dword", end="\t", file=f)


def print_load_ending(f, eew, n = 0, print_idx = False, is_vse = False, is_vsr = False, is_vlr = False, seg = 1):
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
    .align 8 \n\
    .type tdat, @object\n\
    .size tdat, 8256\n\
    tdat:\n\
    tdat1:  .word 0x00ff00ff\n\
    tdat2:  .word 0xff00ff00\n\
    tdat3:  .word 0x0ff00ff0\n\
    tdat4:  .word 0xf00ff00f\n\
    tdat5:  .word 0x00ff00ff\n\
    tdat6:  .word 0xff00ff00\n\
    tdat7:  .word 0x0ff00ff0\n\
    tdat8:  .word 0xf00ff00f\n\
    tdat9:  .zero 4096\n\
    tdat10:  .word 0x00ff00ff\n\
    tdat11:  .word 0xff00ff00\n\
    tdat12:  .word 0x0ff00ff0\n\
    tdat13:  .word 0xf00ff00f\n\
    tdat14:  .word 0x00ff00ff\n\
    tdat15:  .word 0xff00ff00\n\
    tdat16:  .word 0x0ff00ff0\n\
    tdat17:  .word 0xf00ff00f\n\
    tdat18:  .word 0x00ff00ff\n\
    tdat19:  .word 0xff00ff00\n\
    tdat20:  .word 0x0ff00ff0\n\
    tdat21:  .word 0xf00ff00f\n\
    tdat22:  .word 0x00ff00ff\n\
    tdat23:  .word 0xff00ff00\n\
    tdat24:  .word 0x0ff00ff0\n\
    tdat25:  .word 0xf00ff00f\n\
    tdat26:  .zero 4064\n\
    \n\
    .type tsdat, @object\n\
    .size tsdat, 1040320\n\
    tsdat:\n\
    tsdat0:  .zero 520144\n\
    tsdat1:  .word 0x00ff00ff\n\
    tsdat2:  .word 0xff00ff00\n\
    tsdat3:  .word 0x0ff00ff0\n\
    tsdat4:  .word 0xf00ff00f\n\
    tsdat5:  .word 0x00ff00ff\n\
    tsdat6:  .word 0xff00ff00\n\
    tsdat7:  .word 0x0ff00ff0\n\
    tsdat8:  .word 0xf00ff00f\n\
    tsdat9:  .zero 520144\n\
    \n", file=f)
    
    if print_idx:
        generate_idx_data(f, eew)
    
    if not(is_vsr or is_vlr):
        print_mask_origin_data_ending(f)
    
    print("\n\
    RVTEST_DATA_END\n\
    \n", file=f)
    arr = gen_arr_load(n, eew, is_vse = is_vse, is_vsr = is_vsr, is_vlr = is_vlr, seg = seg)
    print_rvmodel_data(arr, f)


def print_mask_origin_data_ending_fixed(f):
    # 24 words, mask_data + 0/64/128
    print_mask_data_ending_fixed(f)
    # 32 words, rd_origin_data + 0/64/128/192
    print_origin_data_ending_fixed(f)

def print_mask_origin_data_ending(f):
    vlen = int(os.environ['RVV_ATG_VLEN'])
    lmul = float(os.environ['RVV_ATG_LMUL'])
    vsew = float(os.environ['RVV_ATG_VSEW'])
    num_elem = int(vlen * lmul / vsew)
    step_bytes = int(vlen) # max lmul = 8, int(vlen * 8 / 8)
    print_mask_data_ending(f, num_elem)
    print_origin_data_ending(f, step_bytes)


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


def print_origin_data_ending_fixed(f):
    print("\n.align 4", file=f)
    print("rd_origin_data:", file=f)
    for i in range(len(rd_origin_data)):
        print(".word\t%s"%rd_origin_data[i], file=f)

def print_origin_data_ending(f, step_bytes):
    word_num = math.ceil(step_bytes / 4)
    print("\n.align 4", file=f)
    print("rd_origin_data:", file=f)
    for i in range(word_num):
        print(".word\t0xdeadbeef", file=f)


def print_common_ending_rs1rs2rd(rs1_val, rs2_val, test_num_tuple, vsew, f, rs1_data_multiplier = 1, rs2_data_multiplier = 1, rd_data_multiplier = 1, generate_date_widen = False, is_reduction = False, is_mask = False, is_rs1_mask = False, is_rs2_mask = False):
    print(test_num_tuple)
    print("\n\
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
    
    if is_rs1_mask:
        print(".align 4", file=f)
        print("rs1_data:", file=f)
        for hex_str in rs1_val:
            hex_str = hex_str[2:] if hex_str.startswith('0x') else hex_str
            words = [hex_str[i:i+8] for i in range(0, len(hex_str), 8)]
            words.reverse()
            for word in words:
                print(".word\t0x%s" % word, file=f)
    else:
        print(".align %d"%(int(vsew * rs1_data_multiplier / 8)), file=f)
        print("rs1_data:", file=f)
        for i in range(len(rs1_val)):
            print_data_width_prefix(f, vsew * rs1_data_multiplier)
            print("%s"%rs1_val[i], file=f)
        if generate_date_widen:
            print(".align %d"%(int(vsew * rs1_data_multiplier * 2 / 8)), file=f)
            print("rs1_data_widen:", file=f)
            for i in range(len(rs1_val)):
                print_data_width_prefix(f, vsew * rs1_data_multiplier * 2)
                print("%s"%rs1_val[i], file=f)
    
    if is_rs2_mask:
        print(".align 4", file=f)
        print("rs2_data:", file=f)
        for hex_str in rs2_val:
            hex_str = hex_str[2:] if hex_str.startswith('0x') else hex_str
            words = [hex_str[i:i+8] for i in range(0, len(hex_str), 8)]
            words.reverse()
            for word in words:
                print(".word\t0x%s" % word, file=f)
    else:
        print("\n.align %d"%(int(vsew * rs2_data_multiplier / 8)), file=f)
        print("rs2_data:", file=f)
        for i in range(len(rs2_val)):
            print_data_width_prefix(f, vsew * rs2_data_multiplier)
            print("%s"%rs2_val[i], file=f)
        if generate_date_widen:
            print(".align %d"%(int(vsew * rs1_data_multiplier * 2 / 8)), file=f)
            print("rs2_data_widen:", file=f)
            for i in range(len(rs2_val)):
                print_data_width_prefix(f, vsew * rs2_data_multiplier * 2)
                print("%s"%rs1_val[i], file=f)
    
    print_mask_origin_data_ending(f)
    print("\n\
    RVTEST_DATA_END\n\
    \n", file=f)
    arr = gen_arr_compute(test_num_tuple, is_reduction=is_reduction, is_mask=is_mask)
    print_rvmodel_data(arr, f)


def print_common_ending_rs1rs2rd_vfcvt(rs_val, rs_int_val, test_num_tuple, vsew, f, is_widen = False, is_narrow = False):
    print("\n\
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
    rs_data_multiplier = 2 if is_narrow else 1
    rd_data_multiplier = 2 if is_widen else 1
    print(".align %d"%(int(vsew * rs_data_multiplier / 8)), file=f)
    print("rs_data:", file=f)
    for i in range(len(rs_val)):
        print_data_width_prefix(f, vsew * rs_data_multiplier)
        print("%s"%rs_val[i], file=f)

    print(".align %d"%(int(vsew * rs_data_multiplier / 8)), file=f)
    print("rs_data_int:", file=f)
    for i in range(len(rs_int_val)):
        print_data_width_prefix(f, vsew * rs_data_multiplier)
        print("%s"%rs_val[i], file=f)

    print_mask_origin_data_ending(f)
    print("\n\
    RVTEST_DATA_END\n\
    \n", file=f)
    arr = gen_arr_compute(test_num_tuple)
    print_rvmodel_data(arr, f)


