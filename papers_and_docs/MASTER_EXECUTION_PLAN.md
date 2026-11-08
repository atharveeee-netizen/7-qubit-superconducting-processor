# Master Multi-Layer Execution Plan
## 7-Qubit Superconducting Transmon Processor & IEEE IMS 2027 Paper

---

### Strategy: How to Use Simon’s Videos vs. Antigravity
* **Follow Antigravity for Execution:** Follow my step-by-step guidance to execute the code, derive parameters, fix API/environment issues, compile the living LaTeX PDF manual, and push to GitHub. You will never get stuck on deprecated code or broken dependencies.
* **Use Simon’s Videos as a Visual Companion:** Watch Simon’s videos (at 1.5x speed or in the background) to gain intuitive familiarity with the concepts and hear his conversational explanations. You do not need to pause, copy code, or struggle to reproduce his bugs—we implement the production-grade, working version together.

---

### Layer 1: Physical Planar CAD Layout in Qiskit Metal (Videos 3 & 4)
* **Goal:** Create a clean, DRC-clean, physically realizable planar layout on high-resistivity silicon.
* **Milestones:**
  1. **Substrate Initialization:** Define the chip canvas ($10\text{ mm} \times 10\text{ mm}$, $500\,\mu\text{m}$ high-resistivity silicon, $\epsilon_r = 11.45$).
  2. **Transmon Pockets Placement:**
     * *Layout A (Baseline Negative Control):* The 7-qubit radial star (Simon’s topology: central hub + 6 outer petals).
     * *Layout B (Winning Primary Architecture):* The 7-qubit heavy-hex "H" fragment (IBM Falcon-7 topology: sparse degree-3 graph).
  3. **Readout Resonator Synthesis:**
     * Synthesize 7 meandered $\lambda/4$ Coplanar Waveguides (CPWs) with $W = 10\,\mu\text{m}, S = 6\,\mu\text{m}$ ($Z_0 = 50.0\,\Omega$).
     * Calculate meander lengths $l_i = v_{\text{ph}} / (4 f_{r,i})$ to stagger frequencies across $6.80\text{--}7.40\text{ GHz}$ ($100\text{ MHz}$ channel spacing).
  4. **Feedline & Couplers:**
     * Route a single shared $50\,\Omega$ CPW readout feedline using `LineTee` and `CoupledLineTee`.
     * Tune coupling capacitors ($C_c \approx 4.0\text{ fF}$) for loaded quality factor $Q_L \approx 7{,}000$.
  5. **Inter-Qubit Coupling Buses:**
     * Route capacitive CPW coupling lines between nearest-neighbor qubits according to the heavy-hex adjacency matrix.

---

### Layer 2: Electrodynamic & Hamiltonian Extraction in Ansys & pyEPR (Videos 5 & 6)
* **Goal:** Extract Maxwell capacitance matrices and diagonalize the quantum Hamiltonian.
* **Milestones:**
  1. **Ansys Q3D Extractor (Lumped Oscillator Model):**
     * Export single and coupled transmon pockets to Q3D.
     * Extract the Maxwell capacitance matrix $C_{ij}$ to verify shunt capacitance $C_\Sigma \approx 70\text{ fF}$ and charging energy $E_C/h \approx 280\text{ MHz}$.
  2. **Ansys HFSS 3D Eigenmode Solver:**
     * Simulate quarter-wave resonator eigenmode frequencies and electromagnetic field distributions.
     * Extract energy participation ratios ($p_{\text{sub}}, p_{\text{metal-air}}$) to budget dielectric loss and predict relaxation limit $T_1$.
  3. **pyEPR Quantum Quantization:**
     * Run Energy Participation Ratio analysis on the HFSS model.
     * Extract dressed qubit transition frequencies $\omega_{01}$, negative Duffing anharmonicities $\alpha_j \approx -330\text{ MHz}$, dispersive shifts $\chi_{qr}$, and cross-Kerr coefficients.

---

### Layer 3: Monte Carlo Collision-Yield Engine (Our IMS 2027 Core Novelty)
* **Goal:** Quantify fabrication yield across topologies and optimize frequency allocation.
* **Milestones:**
  1. **Multi-Topology Yield Benchmark (Figure 1 for IMS Paper):**
     * Run Monte Carlo simulation (20,000 samples/point) across $\sigma_{\text{fab}} \in [5, 132]\text{ MHz}$ for:
       1. Heavy-Hex 7Q fragment
       2. Radial-Star (40 MHz spacing)
       3. Radial-Star (50 MHz spacing)
       4. Square lattice fragment
       5. Linear chain
       6. Ring lattice
     * Prove that the Star topology yields $\sim 0.00\%$ under any realistic fabrication variance, while Heavy-Hex delivers $88.5\%$ at $\sigma = 14\text{ MHz}$.
  2. **Yield-Aware Frequency Optimizer (Figure 2 for IMS Paper):**
     * Implement a simulated annealing / greedy frequency allocator.
     * Improve heavy-hex yield at $\sigma = 40\text{ MHz}$ (the raw unannealed wafer spread) from $41.4\%$ to $>65\%$.

---

### Layer 4: Cleanroom Nanofabrication Mask Export (Video 6)
* **Goal:** Export industry-standard lithography masks ready for cleanroom fabrication.
* **Milestones:**
  1. **Multi-Layer GDSII Generation:**
     * Layer 1: Ground plane cutouts, CPW feedline, and transmon pocket pads.
     * Layer 2: Dolan-bridge Josephson junction shadow evaporation windows.
     * Layer 3: Wirebond launch pads and chip diced border.
  2. **KLayout Inspection:**
     * Inspect and verify GDSII polygon integrity, minimum feature sizes ($>2\,\mu\text{m}$ optical, $>100\,\text{nm}$ junction e-beam), and design-rule check (DRC) compliance.

---

### Layer 5: IEEE IMS 2027 Publication & $0 Travel Grant Pipeline
* **Goal:** Submit a 4-page paper to IEEE IMS 2027 and secure full travel funding.
* **Milestones:**
  1. **Draft IEEE Manuscript:**
     * 4 pages, double-blind compliant format, IEEE MTT-S template.
     * Figure 1: Yield vs. $\sigma_{\text{fab}}$ multi-topology curves.
     * Figure 2: Optimized vs. baseline heavy-hex yield curve.
     * Figure 3: Physical Qiskit Metal layout and GDSII mask.
     * Figure 4: Ansys S-parameter verification ($S_{21}$, phase step, $Z_{11}$).
  2. **Submission Deadline:** December 8, 2026.
  3. **Zero-Cost Travel Execution:**
     * Apply for the **IMS PhD/Student Sponsorship** (6 nights free hotel + free registration).
     * Apply for the **IEEE MTT-S Undergraduate Scholarship / Travel Grant** ($1,500 flight grant).
