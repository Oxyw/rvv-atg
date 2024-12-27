# RISC-V Vector Automatic Tests Generator

NOTE: Test format conforms to RVV v1.0 spec.

## Branches Descriptions

This repository has two available branches:

- `new_test_format`: generates tests that are used for the RISCOF framework (no self-checking, use signature for verification).

- `master`: generates tests that contain self-checking. [stale]


## Prerequisite

1. RVV Compiler
   1. Set `gcc`, `objdump`, and `riscof` directory's path variables in file: `scripts/constants.py`

2. Spike
   1. Install Latest [https://github.com/riscv-software-src/riscv-isa-sim](https://github.com/riscv-software-src/riscv-isa-sim).
   2. Add `<spike_path>/build` to your PATH
   
   If the terminal can find `spike` command then it's successful

3. RISCV-ISAC RVV Support
   1. `git clone https://github.com/hushenwei2000/riscv-isac-rvv`
   2. `cd riscv-isac-rvv`
   3. `git checkout vetcor`  **!!!IMPORTANT!!!**
   4. `pip install . --prefix=~/.local`  # Anywhere you want  
   5. Add `~/.local` to your PATH   
   
   If the terminal can find `riscv_isac` command then it's successful

4. Sail Reference Model (If you want to run RISCOF to test)
   1. Intall sail-riscv with vector support `https://github.com/riscv/sail-riscv`. master branch
      1. sail version should be `0.16`
      1. Note that you should modify `vlen` and `elen` in `riscv_sys_control.sail` after `init_pmp()` before building. Add these two lines for example:
      ```
      vlen = 0b0011;
      elen = 0b1;
      ```
         vlen and elen encoding can be found in `riscv_vlen.sail`.


## Usage

### Generate One Instruction

```
python run.py -i <instruction> -t <type> [--vlen VLEN] [--vsew VSEW] [--lmul LMUL]
```
****
- The type shall be consistent with the instruction: i (integer), f (floating point), m (mask), p (permute), x (fix point), l (load/store)
- Supported instruction and type can be seen in `cgfs/<type>/<instruction>.yaml`
- vlen (vector register length): 32, 64, 128(default), 256, 512, 1024
- vsew (selected element width): 8, 16, 32(default), 64
- lmul (vector length multiplier): 1/8, 1/4, 1/2, 1(default), 2, 4, 8

### Generate All Tests

```
python generate_all.py
```

- This will use default parameter configuration to generate all integer instructions tests.
- Modify `runcommand_<type>` function to run different parameter.
- Modyfy `main` function to run different type of instructions.

After generating, run `python move_generate_all_elf.py` to check if the generated file is valid. If you see:
   - `No first.S for vXX`, it's OK, ignore it.
   - `No RVMODEL_DATA_END for vXX` then it means vXX you should use generate one instruction method to regenerate it. Regenerate all of them and rerun `move_generate_all_elf.py` until no `No RVMODEL_DATA_END` appear.
   - All tests will in `generate_all` folder.


## Run Tests On RISCOF

1. Modify `riscof_files/env/test_macros_vector.h`, you can select your prefered configuration and copy from `env/macros/vsewXX_lmulXX` and paste to `riscof_files/env/test_macros_vector.h`

2. `cd riscof_files`

3. Modify your reference model and DUT to be testes in `config.ini`, in current file, we use sail as reference and spike as DUT

4. Modify GCC in `sail_cSim/riscof_sail_cSim.py` and `spike/riscof_spike.py`

5. copy the `.S` test files to `test_suite`

6. 6. Modify VLEN and ELEN argument in `riscof_files/spike/riscof_spike.py` line 166: `vstring = "_zvl512b_zve64d"`, also modify VLEN macro `-DVLEN=128` in `riscof_files/spike/riscof_spike.py` line 155 and `riscof_files/sail_cSim/riscof_sail_cSim.py` line 103

7. run `riscof run --config=config.ini --suite=test_suite --env=env`

8. If run `riscof coverage` command, modify vlen arg in `riscof_files/sail_cSim/riscof_sail_cSim.py` line 121: `-v128`

## Known Bugs
- Not support floating-point vsew=16
- mask instructions lack of test different registers tests

## Support Configuration

| Parameter | Numbers                   | Current Support | Note                           |
| --------- | ------------------------- | --------------- | ------------------------------ |
| FLEN      | FP16, BF16, 32, 64        | 32, 64          |                                |
| vlen      | 128 ~ 2^16                | 128 ~ 1024      | Spike now support largest 4096 |
| vsew      | 8, 16, 32, 64             | All             |                                |
| lmul      | 1/8, 1/4, 1/2, 1, 2, 4, 8 | All             |                                |
| vta       | 0, 1                      | 0               |                                |
| vma       | 0, 1                      | 0               |                                |

### Notice of Failure Tests

- **vsew <= elen * lmul** should be satisfied!
  - By default, elen = 64.

- If there are failure tests, it is most likely because the configuration cannot be tested on that instruction. For example, testing a widening instruction when vsew=64, or testing floating point when vsew=8/16, or violating the elen-related restriction mentioned above.

## Signature

1. Save the results in Vd and CSRs, including xcsr(mstatus), fcsr and vcsr.

2. Use x20 as basereg.

3. The `arr` list in `rvmodel_data` represents the number of signatures.
   - `arr[0]`: the memory size directly stored by the instruction `vse<eew>` or `vsseg<nf>e<eew>`
   - `arr[1]`: the number of signatures stored using the macro `RVTEST_SIGUPD`
   - `arr[2]`: the number of vector registers stored by the instruction `vs<nf>r.v`