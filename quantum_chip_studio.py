"""
7-Qubit Superconducting Quantum Processor - Standalone Qiskit Metal GUI App
Architecture: IBM 7-Qubit Heavy-Hex / Planar Grid (Matching Simon's Layout & IBM Falcon)
Topology:
    Q0 ----- Q1 ----- Q2
             |
             Q3 (Coupler Hub)
             |
    Q4 ----- Q5 ----- Q6
"""

import sys
import os

print("=" * 70)
print("  LAUNCHING QISKIT METAL QUANTUM HARDWARE DESIGN SUITE")
print("  Architecture: 7-Qubit Planar Heavy-Hex Lattice (Simon / IBM Architecture)")
print("=" * 70)

from qiskit_metal import designs, MetalGUI
from qiskit_metal.qlibrary.qubits.transmon_pocket_6 import TransmonPocket6

# 1. Initialize Planar 2D Chip Design (10mm x 10mm Silicon Substrate)
design = designs.DesignPlanar()
design.chips.main.size.size_x = "10mm"
design.chips.main.size.size_y = "10mm"

# 2. Launch the Native Qt Desktop GUI
gui = MetalGUI(design)

# 3. Define 7-Qubit Planar Lattice (Matching Simon's Grid & IBM Heavy-Hex)
# Coordinates in mm relative to chip center (0, 0)
qubit_coords = {
    "Q0": (-2.5,  2.0, 0),
    "Q1": ( 0.0,  2.0, 0),
    "Q2": ( 2.5,  2.0, 0),
    "Q3": ( 0.0,  0.0, 0),   # Central connection transmon
    "Q4": (-2.5, -2.0, 0),
    "Q5": ( 0.0, -2.0, 0),
    "Q6": ( 2.5, -2.0, 0)
}

qubits = {}
for name, (x, y, orientation) in qubit_coords.items():
    options = dict(
        pos_x=f"{x}mm",
        pos_y=f"{y}mm",
        orientation=orientation,
        pad_width="400um",
        pad_height="280um",
        pad_gap="30um",
        pocket_width="650um",
        pocket_height="650um"
    )
    qubits[name] = TransmonPocket6(design, name, options=options)

# 4. Rebuild geometry and autoscale viewport
design.rebuild()
gui.autoscale()
gui.rebuild()

print("\n[SUCCESS] 7-Qubit Planar Heavy-Hex Lattice placed on 10mm x 10mm substrate:")
print("  Top Row:    Q0 (-2.5, 2.0), Q1 (0.0, 2.0), Q2 (2.5, 2.0)")
print("  Middle:     Q3 (0.0, 0.0)")
print("  Bottom Row: Q4 (-2.5, -2.0), Q5 (0.0, -2.0), Q6 (2.5, -2.0)")
print("\nNative Qiskit Metal GUI window is now active.")
print("Close the window when finished with your design session.")
print("=" * 70)

# Keep the Qt Application event loop running
try:
    gui.qApp.exec_()
except Exception as e:
    print(f"Application closed: {e}")
