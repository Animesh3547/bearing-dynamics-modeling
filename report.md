# Physics-Based Bearing Dynamics: Progress Report

**Student:** Animesh (IIITDM Kurnool) | **Date Range:** 2026-10-08 to 2026-10-18  
**Current Status:**  5 DOF  code has been genrated . validation and fine tuning remains.  
**future_workflow:** After this model good fidelity is achived then => Focusing on signal processing(DSP) on both experimental and simulateed data . Thus chance to get to know what actual Vibration signal represents => ML ( Encoders) 

---

## 2026-10-16

### Accomplished
used .ivp and state space to plot simple damping equations  and working on the 5dof health model. ( created one code for that , finetuning and validation of the data is not done yet.)


### Result / Validation
generated some plots as shared in github plot folder.

### Next Immediate Step
the fine tune and validaiton of the 5 dof model

---

## 2026-10-18

### Accomplished
- **Formulated kinematic benchmarks** for N205EM bearing at 1200 RPM (**BPFO = 108.1 Hz**, **Delta_t = 9.25 ms**).
- **Exported steady-state signals** to compressed binary format (`.npz`) to preserve 64-bit numerical precision.
- **Implemented diagnostic DSP pipeline** combining bandpass filtering, Hilbert transform demodulation, and windowing.

### Result / Validation
- **Validated time-domain peak spacing** at exactly **9.25 ms**, confirming roller orbital kinematics.

### Next Immediate Step
- Execute **Phase 5 localized fault injection** code to simulate outer race spall impacts.
