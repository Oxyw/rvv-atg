#define VREGWIDTH   (VLEN>>3)   // in units of #bytes
#define TESTNUM gp
#define RVTEST_VECTOR_ENABLE                                            \
  li a0, (MSTATUS_VS & (MSTATUS_VS >> 1)) |                             \
         (MSTATUS_FS & (MSTATUS_FS >> 1));                              \
  csrs mstatus, a0;                                                     \
  csrwi fcsr, 0;                                                        \
  csrwi vcsr, 0;
#define VECTOR_RVTEST_SIGUPD(basereg, vreg) vmv.x.s x1, vreg; RVTEST_SIGUPD(basereg, x1);
#define VECTOR_RVTEST_SIGUPD_F(basereg, vreg, flagreg) vfmv.f.s f1, vreg; RVTEST_SIGUPD_F(basereg, f1, flagreg);

// XCSR: xstatus (now only run in M-mode)
#define XCSR_SIGUPD(basereg) \
    csrr x1, mstatus; \
    RVTEST_SIGUPD(basereg, x1);

// FCSR: fflags, frm, fcsr
#define FCSR_SIGUPD(basereg) \
    csrr x1, fflags; \
    RVTEST_SIGUPD(basereg, x1); \
    csrr x1, frm; \
    RVTEST_SIGUPD(basereg, x1); \
    csrr x1, fcsr; \
    RVTEST_SIGUPD(basereg, x1);

// VCSR: vstart, vxsat, vxrm, vcsr, vl, vtype, vlenb
#define VCSR_SIGUPD(basereg) \
    csrr x1, vstart; \
    RVTEST_SIGUPD(basereg, x1); \
    csrr x1, vxsat; \
    RVTEST_SIGUPD(basereg, x1); \
    csrr x1, vxrm; \
    RVTEST_SIGUPD(basereg, x1); \
    csrr x1, vcsr; \
    RVTEST_SIGUPD(basereg, x1); \
    csrr x1, vl; \
    RVTEST_SIGUPD(basereg, x1); \
    csrr x1, vtype; \
    RVTEST_SIGUPD(basereg, x1); \
    csrr x1, vlenb; \
    RVTEST_SIGUPD(basereg, x1);

// Save CSRs: xcsr, fcsr, vcsr
#define XFVCSR_SIGUPD XCSR_SIGUPD(x20); FCSR_SIGUPD(x20); VCSR_SIGUPD(x20);


#define VMVXS_AND_MASK_EEW( targetreg, testreg, eew ) \
    vmv.x.s targetreg, testreg; \
    li x2, MASK_BITS(eew); \
    and targetreg, targetreg, x2;


#define TEST_CASE_FORMAT(testnum, code...) \
test_##testnum: \
    code; \
    XFVCSR_SIGUPD \
    li TESTNUM, testnum; \


#define TEST_CASE_XREG( testnum, testreg, code... ) \
test_ ## testnum: \
    code; \
    XFVCSR_SIGUPD \
    li TESTNUM, testnum; \
    RVTEST_SIGUPD(x20, testreg);
  
#define TEST_CASE_FPREG( testnum, testreg, code... ) \
test_ ## testnum: \
    code; \
    XFVCSR_SIGUPD \
    li TESTNUM, testnum; \
    frflags a1; \
    RVTEST_SIGUPD_F(x20, testreg, a1);

#define TEST_CASE_VREG( testnum, testreg, count, code... ) \
test_ ## testnum: \
    code; \
    XFVCSR_SIGUPD \
    li TESTNUM, testnum; \
    RVTEST_BASEUPD(x20); \
    vs ## count ## r.v testreg, (x20); \
    addi x20, x20, VREGWIDTH * count;


#define TEST_CASE( testnum, testreg, code... ) \
test_ ## testnum: \
    code; \
    XFVCSR_SIGUPD \
    li TESTNUM, testnum; \
    VECTOR_RVTEST_SIGUPD(x20, testreg);

#define TEST_CASE_W( testnum, testreg, code... ) \
test_ ## testnum: \
    code; \
    XFVCSR_SIGUPD \
    li TESTNUM, testnum; \
    VSET_DOUBLE_VSEW \
    VECTOR_RVTEST_SIGUPD(x20, testreg);


#define TEST_CASE_LOOP_EEW(testnum, testreg, code...) \
test_##testnum: \
    VSET_VSEW_4AVL                                  \
    code;                                           \
    XFVCSR_SIGUPD                                   \
    VSET_EEW_EMUL                                   \
    csrr x31, vstart;                               \
    csrr x30, vl;                                   \
    li TESTNUM, testnum;                            \
1 : VECTOR_RVTEST_SIGUPD(x20, testreg);             \
    addi x20, x20, REGWIDTH;                        \
    addi x31, x31, 1;                               \
    vslidedown.vi testreg, testreg, 1;              \
    bne x31, x30, 1b;                               \
    addi x20, x20, -REGWIDTH;

#define TEST_CASE_LOOP_EEW_EMUL(testnum, testreg, emul, code...) \
test_##testnum: \
    VSET_VSEW_4AVL                                               \
    code;                                                        \
    XFVCSR_SIGUPD                                                \
    VSET_EEW_EMUL##emul                                          \
    csrr x31, vstart;                                            \
    csrr x30, vl;                                                \
    li TESTNUM, testnum;                                         \
1 : VECTOR_RVTEST_SIGUPD(x20, testreg);                          \
    addi x20, x20, REGWIDTH;                                     \
    addi x31, x31, 1;                                            \
    vslidedown.vi testreg, testreg, 1;                           \
    bne x31, x30, 1b;                                            \
    addi x20, x20, -REGWIDTH;


#define TEST_CASE_LOOP( testnum, testreg, code...) \
test_ ## testnum: \
    code; \
    XFVCSR_SIGUPD \
    csrr x31, vstart; \
    csrr x30, vl; \
    li TESTNUM, testnum; \
1:  VECTOR_RVTEST_SIGUPD(x20, testreg); \
    addi x20, x20, REGWIDTH; \
    addi x31, x31, 1; \
    vslidedown.vi testreg, testreg, 1; \
    bne x31, x30, 1b; \
    addi x20, x20, -REGWIDTH; \

#define TEST_CASE_LOOP_W( testnum, testreg, code...) \
test_ ## testnum: \
    code; \
    XFVCSR_SIGUPD \
    li TESTNUM, testnum; \
    VSET_DOUBLE_VSEW_4AVL \
    csrr x31, vstart; \
    csrr x30, vl; \
1:  VECTOR_RVTEST_SIGUPD(x20, testreg); \
    addi x20, x20, REGWIDTH; \
    addi x31, x31, 1; \
    vslidedown.vi testreg, testreg, 1; \
    bne x31, x30, 1b; \
    addi x20, x20, -REGWIDTH; \
    VSET_VSEW_4AVL; 

#define TEST_CASE_LOOP_CONTINUE( testnum, testreg, code...) \
    code; \
    csrr x31, vstart; \
    csrr x30, vl; \
    li TESTNUM, testnum; \
1:  VECTOR_RVTEST_SIGUPD(x20, testreg); \
    addi x20, x20, REGWIDTH; \
    addi x31, x31, 1; \
    vslidedown.vi testreg, testreg, 1; \
    bne x31, x30, 1b; \
    addi x20, x20, -REGWIDTH; \


#define TEST_CASE_FP( testnum, testreg,  code... ) \
test_ ## testnum: \
    code; \
    XFVCSR_SIGUPD \
    li  TESTNUM, testnum; \
    frflags a1; \
    VECTOR_RVTEST_SIGUPD_F(x20, testreg, a1); \

#define TEST_CASE_W_FP( testnum, testreg,  code... ) \
test_ ## testnum: \
    code; \
    XFVCSR_SIGUPD \
    li  TESTNUM, testnum; \
    VSET_DOUBLE_VSEW \
    frflags a1; \
    VECTOR_RVTEST_SIGUPD_F(x20, testreg, a1); \

#define TEST_CASE_LOOP_FP( testnum, testreg,  code...) \
test_ ## testnum: \
    code; \
    XFVCSR_SIGUPD \
    csrr x31, vstart; \
    csrr x30, vl; \
    li TESTNUM, testnum; \
    frflags a1; \
1:  VECTOR_RVTEST_SIGUPD_F(x20, testreg, a1); \
    addi x20, x20, REGWIDTH; \
    addi x31, x31, 1; \
    vslidedown.vi testreg, testreg, 1; \
    bne x31, x30, 1b; \
    addi x20, x20, -REGWIDTH; \

#define TEST_CASE_LOOP_W_FP( testnum, testreg, code...) \
test_ ## testnum: \
    code; \
    XFVCSR_SIGUPD \
    li TESTNUM, testnum; \
    VSET_DOUBLE_VSEW_4AVL \
    csrr x31, vstart; \
    csrr x30, vl; \
    frflags a1; \
1:  VECTOR_RVTEST_SIGUPD_F(x20, testreg, a1); \
    addi x20, x20, REGWIDTH; \
    addi x31, x31, 1; \
    vslidedown.vi testreg, testreg, 1; \
    bne x31, x30, 1b; \
    addi x20, x20, -REGWIDTH; \
