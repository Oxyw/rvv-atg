#include "test_macros.h"
#include "test_macros_vector_common.h"
// See LICENSE for license details.

#ifndef __TEST_MACROS_VECTOR_H
#define __TEST_MACROS_VECTOR_H

//-----------------------------------------------------------------------
// Helper macros
//-----------------------------------------------------------------------

// VSEW temporarily hard-coded to 32 bits

#define RVTEST_VSET RVTEST_VECTOR_ENABLE; vsetvli x31, x0, e32, m8, tu, mu;
#define __riscv_vsew 32
#define __e_riscv_vsew e32
#define __riscv_vsew_bytes 4
#define __riscv_double_vsew 64
#define VSEW_MASK_BITS 0x00000000ffffffff
#define DOUBLE_VSEW_MASK_BITS 0xffffffffffffffff
#define VSET_VSEW vsetivli x31, 1, e32, m8, tu, mu;
#define VSET_VSEW_4AVL vsetvli x31, x0, e32, m8, tu, mu;
#define VSET_DOUBLE_VSEW vsetivli x31, 1, e64, m8, tu, mu;
#define VSET_CONST_VSEW(eew_num) vsetivli x31, ##eew_num, m8, tu, mu;
#define VSET_DOUBLE_VSEW_4AVL vsetvli x31, x0, e64, m8, tu, mu;

#define MASK_VSEW(x)        ((x) & ((1 << (__riscv_vsew - 1) << 1) - 1))
#define MASK_EEW(x, eew)    ((x) & ((1 << (eew - 1) << 1) - 1))
#define MASK_DOUBLE_VSEW(x) ((x) & ((1 << ((__riscv_vsew * 2) - 1) << 1) - 1))
#define MASK_HALF_VSEW(x)   ((x) & ((1 << ((__riscv_vsew / 2) - 1) << 1) - 1))
#define MASK_QUART_VSEW(x)  ((x) & ((1 << ((__riscv_vsew / 4) - 1) << 1) - 1))
#define MASK_EIGHTH_VSEW(x) ((x) & ((1 << ((__riscv_vsew / 8) - 1) << 1) - 1))
#define MASK_BITS(eew)      ((-1 << (64 - eew)) >> (64 - eew))
#define MK_EEW(eew_num) e##eew_num
#define MK_VLE_INST(eew_num) vle##eew_num.v
#define MK_VSE_INST(eew_num) vse##eew_num.v

#define SEXT_HALF_TO_VSEW(x)   ((x) | (-(((x) >> ((__riscv_vsew / 2) - 1)) & 1) << ((__riscv_vsew / 2) - 1)))
#define SEXT_QUART_TO_VSEW(x)  ((x) | (-(((x) >> ((__riscv_vsew / 4) - 1)) & 1) << ((__riscv_vsew / 4) - 1)))
#define SEXT_EIGHTH_TO_VSEW(x) ((x) | (-(((x) >> ((__riscv_vsew / 8) - 1)) & 1) << ((__riscv_vsew / 8) - 1)))
#define SEXT_DOUBLE_VSEW(x)    ((x) | (-(((x) >> ((__riscv_vsew * 2) - 1)) & 1) << (__riscv_vsew - 1)))
#define ZEXT_VSEW(x)           ((x) | (x) >> (__riscv_vsew - 1))
#define ZEXT_DOUBLE_VSEW(x)    ((x) | (x) >> ((__riscv_vsew * 2) - 1))


//-----------------------------------------------------------------------
// Pass and fail code (assumes test num is in TESTNUM)
//-----------------------------------------------------------------------




//-----------------------------------------------------------------------
// Test data section
//-----------------------------------------------------------------------

#define TEST_DATA

#endif
