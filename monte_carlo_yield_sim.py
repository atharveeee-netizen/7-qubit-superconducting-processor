import os
import numpy as np
import matplotlib.pyplot as plt

# Set publication style
plt.rcParams['font.family'] = 'serif'
plt.rcParams['font.size'] = 11
plt.rcParams['axes.linewidth'] = 1.2
plt.rcParams['mathtext.fontset'] = 'cm'

rng = np.random.default_rng(42)
alpha = -0.330  # GHz transmon anharmonicity

def check_collisions(f, edges, ctrl_target, spectator_triples, alpha=-0.330):
    f12 = f + alpha
    # Type 1 & 3: Nearest-neighbour fundamental and half-straddling collisions
    for (a, b) in edges:
        if abs(f[a] - f[b]) < 0.017:
            return True  # Type 1 fundamental
        if abs(f[a] - f12[b]) < 0.030 or abs(f[b] - f12[a]) < 0.030:
            return True  # Type 3 half-straddling
            
    # Type 2 & 4: Control j -> Target k collisions
    for (j, k) in ctrl_target:
        if abs((f[j] + f12[j]) - 2 * f[k]) < 0.004:
            return True  # Type 2 two-photon transition
        if not (f12[j] < f[k] < f[j]):
            return True  # Type 4 full straddling condition violated
            
    # Types 5, 6, 7: Control j with two targets i and k (spectator interactions)
    for (j, i, k) in spectator_triples:
        if abs(f[i] - f[k]) < 0.017:
            return True  # Type 5 spectator fundamental
        if abs(f[i] - f12[k]) < 0.025 or abs(f12[i] - f[k]) < 0.025:
            return True  # Type 6 spectator straddling
        if abs((2 * f[j] + alpha) - (f[i] + f[k])) < 0.025:
            return True  # Type 7 higher-order spectator interaction
            
    return False

def simulate_yield(setpoints, edges, ctrl_target, triples, sigma_mhz, n=20000):
    ok = 0
    s = sigma_mhz / 1000.0
    sp = np.array(setpoints)
    for _ in range(n):
        f = sp + rng.normal(0, s, size=len(sp))
        if not check_collisions(f, edges, ctrl_target, triples):
            ok += 1
    return ok / n

# 1. Topology A: Heavy-Hex 7Q Fragment (IBM Falcon-7 style)
edgesA = [(0, 1), (1, 2), (1, 3), (3, 5), (4, 5), (5, 6)]
f1, f2, f3 = 5.00, 5.07, 5.14
spA = [f3, f1, f3, f3, f3, f2, f3]
ctA = [(0, 1), (2, 1), (3, 1), (3, 5), (4, 5), (6, 5)]
triA = [(3, 1, 5)]

# 2. Topology B: Radial-Star (40 MHz spacing)
edgesB = [(0, k) for k in range(1, 7)]
ctB = [(0, k) for k in range(1, 7)]
triB = [(0, i, k) for i in range(1, 7) for k in range(i + 1, 7)]
def spB(spacing):
    hub = 5.30
    targets = [hub - 0.080 - spacing * i for i in range(6)]
    return [hub] + targets

# 3. Topology C: Linear Chain 7Q (0-1-2-3-4-5-6)
edgesC = [(i, i+1) for i in range(6)]
ctC = [(i, i+1) for i in range(0, 6, 2)] + [(i+1, i) for i in range(1, 6, 2)]
triC = []
spC = [5.00, 5.14, 5.00, 5.14, 5.00, 5.14, 5.00]

sigmas = [5, 10, 14, 20, 30, 40, 60, 80, 100, 132]
yields_hex = []
yields_star40 = []
yields_star50 = []
yields_chain = []

print("Running Monte Carlo collision yield simulations (N=20,000 per point)...")
print(f"{'sigma (MHz)':<12} | {'Heavy-Hex 7Q':<14} | {'Star (40MHz)':<14} | {'Star (50MHz)':<14} | {'Linear Chain':<14}")
print("-" * 75)

for sg in sigmas:
    y_hex = simulate_yield(spA, edgesA, ctA, triA, sg) * 100
    y_s40 = simulate_yield(spB(0.040), edgesB, ctB, triB, sg) * 100
    y_s50 = simulate_yield(spB(0.050), edgesB, ctB, triB, sg) * 100
    y_chain = simulate_yield(spC, edgesC, ctC, triC, sg) * 100
    
    yields_hex.append(y_hex)
    yields_star40.append(y_s40)
    yields_star50.append(y_s50)
    yields_chain.append(y_chain)
    
    print(f"{sg:<12d} | {y_hex:<13.2f}% | {y_s40:<13.2f}% | {y_s50:<13.2f}% | {y_chain:<13.2f}%")

# Generate Publication-Quality Figure 1
fig, ax = plt.subplots(figsize=(7, 4.5), dpi=300)

ax.plot(sigmas, yields_hex, 'o-', color='#004488', linewidth=2.2, markersize=6, label='Heavy-Hex 7Q Fragment (IBM Falcon)')
ax.plot(sigmas, yields_chain, 's--', color='#009988', linewidth=1.8, markersize=5, label='Linear Chain 7Q')
ax.plot(sigmas, yields_star40, '^-.', color='#EE7733', linewidth=1.8, markersize=6, label='Radial-Star 7Q (40 MHz step)')
ax.plot(sigmas, yields_star50, 'v:', color='#CC3311', linewidth=1.8, markersize=6, label='Radial-Star 7Q (50 MHz step)')

# Add threshold annotations
ax.axvline(14, color='gray', linestyle=':', alpha=0.8)
ax.text(15, 85, r'IBM Laser-Annealed ($\sigma = 14\,\mathrm{MHz}$)', fontsize=9, color='#333333')

ax.axvline(40, color='gray', linestyle=':', alpha=0.8)
ax.text(41, 45, r'As-Fabricated Wafer ($\sigma = 40\,\mathrm{MHz}$)', fontsize=9, color='#333333')

ax.set_xlabel(r'Fabrication Frequency Spread $\sigma_{\mathrm{fab}}$ [MHz]', fontsize=11)
ax.set_ylabel(r'Collision-Free Yield [\%]', fontsize=11)
ax.set_title(r'7-Qubit Processor Yield vs. Fabrication Spread (Type 1--7 Framework)', fontsize=12, pad=12)
ax.set_ylim(-2, 105)
ax.set_xlim(0, 135)
ax.grid(True, linestyle='--', alpha=0.5)
ax.legend(frameon=True, facecolor='white', framealpha=0.9, fontsize=9.5, loc='upper right')

plt.tight_layout()
out_png = r'C:\Users\noobg\.gemini\antigravity-ide\scratch\fig1_yield_vs_sigma.png'
plt.savefig(out_png)
print(f"\nSaved publication-grade Figure 1 to {out_png}")
