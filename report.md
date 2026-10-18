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
- for N205EM bearing at 1200 RPM (**BPFO = 108.1 Hz**, **Delta_t = 9.25 ms**).  and fig"05_verification_result.png"   plot A is showing peak at a spcaing of 9.25ms ...
- genrated the signal and compressed it in  binary format (`.npz`) to preserve 64-bit numerical precision. it was done using "04_healthy_5dof_bearing_dynamics".
- For plot B i was not able to guess how the fft and peaks should look as it was not as i expected so i tries usung  hibert transform , and demoudulatin hoping that i can see the bpfo peak from the resonace but it failed ,  I WILL LOOK INTO IT MORE .

### Result / Validation
-  spacing can be seen  at exactly **9.25 ms**, confirming roller orbital kinematics.

### Next Immediate Step
- to  execute  **localized fault injection** code to simulate outer race spall impacts.
