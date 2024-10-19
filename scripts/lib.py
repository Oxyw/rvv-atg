from datetime import date
import logging
import os
import subprocess
import re

from scripts.import_test_functions import *


def setup_logging(verbose):
    """Setup the root logger.

    Args:
      verbose: Verbose logging
    """
    if verbose:
        logging.basicConfig(
            format="%(asctime)s %(filename)s:%(lineno)-5s %(levelname)-8s %(message)s",
            datefmt='%a, %d %b %Y %H:%M:%S',
            level=logging.DEBUG)
    else:
        logging.basicConfig(format="%(asctime)s %(levelname)-8s %(message)s",
                            datefmt='%a, %d %b %Y %H:%M:%S',
                            level=logging.INFO)


def create_output(args):
    """ Create output directory

    Args:
      instr: Name of instruction
      output : Name of specified output directory

    Returns:
      Output directory
    """
    instr = args.i
    output = args.o
    vlen = args.vlen
    vsew = args.vsew
    lmul = args.lmul
    vta = args.vta
    vma = args.vma
    agnostic_type = args.agnostic_type
    masked = True if args.masked == "True" else False
    # Create output directory
    if output is None:
        output = str(date.today())[5:] + "-" + instr + "-vlen" + str(vlen) + "-vsew" + str(vsew) + "-lmul" + str(lmul) + ("-masked" if masked else "") + "-vta" + str(vta) + "-vma" + str(vma) + "-agnostic_type" + str(agnostic_type)
    os.system("rm -rf {}".format(output))

    logging.info("Creating output directory: {}".format(output))
    subprocess.run(["mkdir", "-p", output])

    return output


def create_cgf_path(instr, type, lmul, rvv_atg_root, output_dir):
    """ Create CGF path among exsiting CGF Files, and copy it to `output_dir`

    Args:
      instr : Name of instruction

    Returns:
      CGF path
    """
    p = ""
    if 2.0 == lmul and ("f" == type or "l" == type):
        p = str(rvv_atg_root) + "/cgfs/" + str(type) + "/lmul2/" + str(instr) + ".yaml"
    elif 4.0 == lmul and ("f" == type or "l" == type):
        p = str(rvv_atg_root) + "/cgfs/" + str(type) + "/lmul4/" + str(instr) + ".yaml"
    elif 8.0 == lmul and ("f" == type or "l" == type):
        p = str(rvv_atg_root) + "/cgfs/" + str(type) + "/lmul8/" + str(instr) + ".yaml"
    else :
        p = str(rvv_atg_root) + "/cgfs/" + str(type) + "/" + str(instr) + ".yaml"
    os.system("cp %s %s" % (p, output_dir))
    logging.info("Finding CGF for: {} in {}.".format(instr, p))
    logging.info("lmul: {}.".format(lmul))

    return p


def create_empty_test(instr, xlen, vlen, vsew, lmul, vta, vma, output_dir):
    """Create an empty test file to generate coverage report, and put empty test into `output_dir`

    Args:
      instr     : Instruction name
      xlen      : XLEN
      vlen      : Length of each vector registers, decide elements of one vector
      vsew      : Selected element width, decide width of operands and elements of one vector
      lmul      : Vector register group multiplier, decide vector registers
      vta       : Vector tail agnostic policy, decide expect results
      vma       : Vector mask elements agnostic policy, decide expect results
      output_dir: Output dir of this execution

    Return:
    Test file path
    """
    func_str = "create_empty_test_{}(xlen, vlen, vsew, lmul, vta, vma, output_dir)".format(
        instr)
    return eval(func_str)


def create_first_test(instr, xlen, vlen, vsew, lmul, vta, vma, output_dir, rpt_path):
    """Create an test file with all operands needing to be tested in the coverage report, but the expected answer is using 5201314, and put empty test into `output_dir`

    Args:
      instr     : Instruction name
      xlen      : XLEN
      vlen      : Length of each vector registers, decide elements of one vector
      vsew      : Selected element width, decide width of operands and elements of one vector
      lmul      : Vector register group multiplier, decide vector registers
      vta       : Vector tail agnostic policy, decide expect results
      vma       : Vector mask elements agnostic policy, decide expect results
      output_dir: Output dir of this execution
      rpt_path  : Path of coverate report
    Return:
    Test file path
    """
    func_str = "create_first_test_{}(xlen, vlen, vsew, lmul, vta, vma, output_dir, rpt_path)".format(
        instr)
    return eval(func_str)

integer_instr = ['vadc', 'vadd', 'vand', 'vdiv', 'vdivu', 'vmacc', 'vmadc', 'vmadd', 'vmax', 'vmaxu', 'vmerge', 'vmin', 'vminu', 'vmsbc', 'vmseq', 'vmsgt', 'vmsgtu', 'vmsle', 'vmsleu', 'vmslt', 'vmsltu', 'vmsne', 'vmulh', 'vmulhsu', 'vmulhu', 'vmul', 'vnmsac', 'vnmsub', 'vnsra', 'vnsrl', 'vor', 'vredand', 'vredmax', 'vredmaxu', 'vredmin', 'vredminu', 'vredor', 'vredsum', 'vredxor', 'vrem', 'vremu', 'vrsub', 'vsadd', 'vsaddu', 'vsbc', 'vsext', 'vsll', 'vsra', 'vsrl', 'vssub', 'vssubu', 'vsub', 'vwadd', 'vwaddu', 'vwmacc', 'vwmaccsu', 'vwmaccu', 'vwmaccus', 'vwmul', 'vwmulsu', 'vwmulu', 'vwredsum', 'vwredsumu', 'vwsub', 'vwsubu', 'vxor', 'vzext']
mask_instr = ['vfirst', 'vid', 'viota', 'vmand', 'vmandnot', 'vmnand', 'vmnor', 'vmor', 'vmornot', 'vmsbf', 'vmsif', 'vmsof', 'vmxnor', 'vmxor', 'vpopc']
floatingpoint_instr = ['vfadd', 'vfclass', 'vfcvt', 'vfdiv', 'vfmacc', 'vfmadd', 'vfmax', 'vfmerge', 'vfmin', 'vfmsac', 'vfmsub', 'vfmul', 'vfmv', 'vfncvt', 'vfnmacc', 'vfnmadd', 'vfnmsac', 'vfnmsub', 'vfrdiv', 'vfrec7', 'vfredmax', 'vfredmin', 'vfredosum', 'vfredusum', 'vfrsqrt7', 'vfrsub', 'vfsgnj', 'vfsgnjn', 'vfsgnjx', 'vfsqrt', 'vfsub', 'vfwadd', 'vfwcvt', 'vfwmacc', 'vfwmsac', 'vfwmul', 'vfwnmacc', 'vfwnmsac', 'vfwredsum', 'vfwsub', 'vmfeq', 'vmfge', 'vmfgt', 'vmfle', 'vmflt', 'vmfne']
permute_instr = ['vcompress', 'vfslide1', 'vmvnr', 'vmv', 'vrgather', 'vrgatherei16', 'vslide', 'vslide1']
fixpoint_instr = ['vaadd', 'vaaddu', 'vasub', 'vasubu', 'vnclip', 'vnclipu', 'vsmul', 'vssra', 'vssrl']
loadstore_instr = ['vle8', 'vle16', 'vle32', 'vle64', 'vlre8', 'vlre16', 'vlre32', 'vlse8', 'vlse16', 'vlse32', 'vlse64', 'vlsege8', 'vlsege16', 'vlsege32', 'vlsege64', 'vlssege8', 'vlssege16', 'vlssege32', 'vlssege64', 'vluxei8', 'vluxei16', 'vluxei32', 'vluxei64', 'vloxei8', 'vloxei16', 'vloxei32', 'vloxei64', 'vluxsegei8', 'vluxsegei16', 'vluxsegei32', 'vse8', 'vse16', 'vse32', 'vse64', 'vsre', 'vsse8', 'vsse16', 'vsse32', 'vsse64', 'vssege8', 'vssege16', 'vssege32', 'vssege64', 'vsssege8', 'vsssege16', 'vsssege32', 'vsssege64', 'vsuxei8', 'vsuxei16', 'vsuxei32', 'vsuxei64', 'vsoxei8', 'vsoxei16', 'vsoxei32', 'vsoxei64', 'vsuxsegei8', 'vsuxsegei16', 'vsuxsegei32']
def check_type(instr, type):
    if type == "i":
        valid_instr = integer_instr
    elif type == "x":
        valid_instr = fixpoint_instr
    elif type == "p":
        valid_instr = permute_instr
    elif type == "f":
        valid_instr = floatingpoint_instr
    elif type == "l":
        valid_instr = loadstore_instr
    elif type == "m":
        valid_instr = mask_instr
    else:
        return False
    if instr in valid_instr:
        return True
    else:
        return False

def check_spikelog(dir, instr):
  log = "%s/%s"%(dir, 'spike_%s_final.log'%instr)
  if os.system("grep FAIL %s"%log) == 0:
    print("Generated file is WRONG! : %s"%instr)

def rewrite_macro_vtavma(vsew, lmul, vta, vma):
  if lmul < 1:
      lmul = str(lmul).replace(".", "")
  else:
      lmul = str(int(lmul))
  print("vta, vma ", vta, vma)
  new_vtavma = '%s, %s'%('ta' if vta else 'tu', 'ma' if vma else 'mu')
  print("new_vtavma: ", new_vtavma)

  f_path_1 = os.environ["RVV_ATG_ROOT"] + '/env/macros/vsew%d_lmul%s/test_macros_vector.h'%(vsew, lmul)
  f1 = open(f_path_1, 'r')
  alllines1 = f1.readlines()
  f1.close()
  f1 = open(f_path_1,'w+')
  for eachline in alllines1:
      a = re.sub('t[au], m[au]', new_vtavma, eachline)
      f1.writelines(a)
  f1.close()
