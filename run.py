
import argparse
from ast import arg
import os

from scripts.lib import *
from scripts.replace_results import replace_results
from scripts.run_riscof_coverage import run_riscof_coverage
from scripts.run_spike import run_spike
from scripts.constants import *


def parse_args(cwd):
    """Create a command line parser.
    Returns: The created parser.
    """
    # Parse input arguments
    parser = argparse.ArgumentParser()

    parser.add_argument("--xlen", type=int, default="64",
                        help="XLEN Value for the ISA: \
                            32, 64(default)")
    parser.add_argument("--flen", type=int, default="32",
                        help="FLEN Value for the ISA: \
                            32(default), 64")
    parser.add_argument("--vlen", type=int, default="128",
                        help="Vector Register Length: \
                        32, 64, 128(default), 256, 512, 1024")
    parser.add_argument("--elen", type=int, default="64",
                        help="The maximum size of a vector element that any operation can produce or consume in bits: \
                        default = 64")
    parser.add_argument("--vsew", type=int, default="32",
                        help="Selected Element Width: \
                        8, 16, 32(default), 64")
    parser.add_argument("--lmul", type=float, default="1",
                        help="Vector Register Grouping Multiplier: \
                        0.125, 0.25, 0.5, 1(default), 2, 4, 8")
    parser.add_argument("--vta", type=int, default="0",
                        help="Vector Tail Agnostic Mode: \
                        0(undisturbed, default), 1(agnostic)")
    parser.add_argument("--vma", type=int, default="0",
                        help="Vector Mask Agnostic Mode: \
                        0(undisturbed, default), 1(agnostic)")
    parser.add_argument("--agnostic_type", type=int, default="0",
                        help="If vta or vma is 1(agnostic),  \
                        0(retain the value they previously held, default), or 1(written with 1s)")
    parser.add_argument("--masked", type=str, default="True",
                        help="If enable masked")
    parser.add_argument("-v", "--verbose", dest="verbose", action="store_true",
                        default=False,
                        help="Verbose Logging")
    parser.add_argument("-o", "--output", type=str,
                        help="Output Directory Name", dest="o")
    parser.add_argument("-i", "--instr", type=str,
                        help="One Instruction Needing to Generate Tests", dest="i")
    parser.add_argument("-t", "--type", type=str,
                        help="Type of Instruction: i, f, m, x, p, l", dest="t")
    parser.add_argument("--tool", type=str,
                        help="Tool to rgenerate log: spike(default), sail", default="spike")
    parser.add_argument("-b","--batch", type=int, default="1",
                        help="Batch mode")
    args = parser.parse_args()
    if args.vma == 0:
        args.vma = False
    else:
        args.vma = True
    if args.vta == 0:
        args.vta = False
    else:
        args.vta = True
    return args


def run_vf(cwd, args, cgf, output_dir):
    # 1. Create empty test file
    empty_test = create_empty_test(
        args.i, args.xlen, args.vlen, args.vsew, args.lmul, args.vta, args.vma, output_dir)

    # 2. Use empty tests to generate coverage report
    (rpt_empty, isac_log_empty) = run_riscof_coverage(args.i, cwd, cgf,
                                                      output_dir, empty_test, 'empty', args.xlen, args.flen, args.vlen, args.elen, args.vsew, args.lmul,  tool=args.tool)

    # 3. Generate test with not-filled result
    first_test = create_first_test(
        args.i, args.xlen, args.vlen, args.vsew, args.lmul, args.vta, args.vma, output_dir, rpt_empty)

    # 4. Run spike to generate commit info log for first test
    spike_first_log = run_spike(args.i, cwd,
        output_dir, first_test, 'first', args.xlen, args.flen, args.vlen, args.elen, args.vsew, args.lmul)


def run_integer(cwd, args, cgf, output_dir):
    # 1. Create empty test file
    empty_test = create_empty_test(
        args.i, args.xlen, args.vlen, args.vsew, args.lmul, args.vta, args.vma, output_dir)

    # 2. Use empty tests to generate coverage report
    (rpt_empty, isac_log_empty) = run_riscof_coverage(args.i, cwd, cgf,
                                                      output_dir, empty_test, 'empty', args.xlen, args.flen, args.vlen, args.elen, args.vsew, args.lmul,  tool=args.tool)

    # 3. Generate test with not-filled result
    first_test = create_first_test(
        args.i, args.xlen, args.vlen, args.vsew, args.lmul, args.vta, args.vma, output_dir, rpt_empty)

    # 4. Run spike to generate commit info log for first test
    spike_first_log = run_spike(args.i, cwd,
        output_dir, first_test, 'first', args.xlen, args.flen, args.vlen, args.elen, args.vsew, args.lmul)


def run_mask(cwd, args, cgf, output_dir):
    # 1. Create empty test file
    empty_test = create_empty_test(
        args.i, args.xlen, args.vlen, args.vsew, args.lmul, args.vta, args.vma, output_dir)

    # 2. Run spike to generate commit info log
    spike_first_log = run_spike(args.i, cwd,
        output_dir, empty_test, 'first', args.xlen, args.flen, args.vlen, args.elen, args.vsew, args.lmul)


def run_permutation(cwd, args, cgf, output_dir):
    # 1. Create empty test file
    empty_test = create_empty_test(
        args.i, args.xlen, args.vlen, args.vsew, args.lmul, args.vta, args.vma, output_dir)

    # 2. Use empty tests to generate coverage report
    (rpt_empty, isac_log_empty) = run_riscof_coverage(args.i, cwd, cgf,
                                                      output_dir, empty_test, 'empty', args.xlen, args.flen, args.vlen, args.elen, args.vsew, args.lmul,  tool=args.tool)

    # 3. Generate test with not-filled result
    first_test = create_first_test(
        args.i, args.xlen, args.vlen, args.vsew, args.lmul, args.vta, args.vma, output_dir, rpt_empty)

    # 4. Run spike to generate commit info log for first test
    spike_first_log = run_spike(args.i, cwd,
        output_dir, first_test, 'first', args.xlen, args.flen, args.vlen, args.elen, args.vsew, args.lmul)


def run_loadstore(cwd, args, cgf, output_dir):
    # 1. Create empty test file
    empty_test = create_empty_test(
        args.i, args.xlen, args.vlen, args.vsew, args.lmul, args.vta, args.vma, output_dir)

    # 2. Use empty tests to generate coverage report
    (rpt_empty, isac_log_empty) = run_riscof_coverage(args.i, cwd, cgf,
                                                      output_dir, empty_test, 'empty', args.xlen, args.flen, args.vlen, args.elen, args.vsew, args.lmul,  tool=args.tool)

    # 3. Generate test with not-filled result
    first_test = create_first_test(
        args.i, args.xlen, args.vlen, args.vsew, args.lmul, args.vta, args.vma, output_dir, rpt_empty)
    
    # 4. Run spike to generate commit info log for first test
    spike_first_log = run_spike(args.i, cwd,
        output_dir, first_test, 'first', args.xlen, args.flen, args.vlen, args.elen, args.vsew, args.lmul)


def main():
    # Full path of current dir
    cwd = os.path.dirname(os.path.realpath(__file__))
    os.environ["RVV_ATG_ROOT"] = cwd
    args = parse_args(cwd)
    setup_logging(args.verbose)
    if (args.vsew > args.elen * args.lmul):
        logging.error("(vsew <= elen * lmul) is not satisfied!")
        return
    if not check_type(args.i, args.t):
        logging.error("Invalid type or instruction!")
        return
    output_dir = create_output(args)
    cgf = create_cgf_path(args.i, args.t, args.lmul, cwd, output_dir)
    rewrite_macro_vtavma(args.vsew, args.lmul, args.vta, args.vma)
    logging.info("RVV-ATG: instr: %s, xlen: %d, vlen: %d, elen: %d, vsew: %d, lmul: %f"%(args.i, args.xlen, args.vlen, args.elen, args.vsew, args.lmul))
    os.environ["RVV_ATG_XLEN"] = str(args.xlen)
    os.environ["RVV_ATG_VLEN"] = str(args.vlen)
    os.environ["RVV_ATG_VSEW"] = str(args.vsew)
    os.environ["RVV_ATG_LMUL"] = str(args.lmul)
    os.environ["RVV_ATG_MASKED"] = str(args.masked)
    os.environ["RVV_ATG_VMA"] = str(args.vma)
    os.environ["RVV_ATG_VTA"] = str(args.vta)
    os.environ["RVV_ATG_AGNOSTIC_TYPE"] = str(args.agnostic_type)
    if args.t == "f":
        run_vf(cwd, args, cgf, output_dir)
    elif args.t == "i" or args.t == "x":
        run_integer(cwd, args, cgf,  output_dir)
    elif args.t == "m":
        run_mask(cwd, args, cgf, output_dir)
    elif args.t == "p":
        run_permutation(cwd, args, cgf, output_dir)
    elif args.t == "l":
        run_loadstore(cwd, args, cgf, output_dir)


if __name__ == "__main__":
    main()