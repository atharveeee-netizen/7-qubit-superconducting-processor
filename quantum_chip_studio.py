"""
7-Qubit Superconducting Quantum Processor - Standalone Qiskit Metal GUI App
Launches the native Qiskit Metal Qt Application with interactive canvas,
component inspector, and 7-qubit lattice starter layout.
"""

import sys
import os
import math

print("=" * 70)
print("  LAUNCHING QISKIT METAL QUANTUM HARDWARE DESIGN SUITE")
print("  Architecture: 7-Qubit Transmon Lattice (IBM Heavy-Hex Inspired)")
print("=" * 70)

from qiskit_metal import designs, MetalGUI
from qiskit_metal.qlibrary.qubits.transmon_pocket_6 import TransmonPocket6
from qiskit_metal.qlibrary.tlines.meandered import RouteMeander
from qiskit_metal.qlibrary.terminations.launchpad_wb import LaunchpadWirebond

# 1. Initialize Planar 2D Chip Design
design = designs.DesignPlanar()
design.chips.main.size.size_x = "10mm"
design.chips.main.size.size_y = "10mm"

# 2. Launch the Native Qt Desktop GUI
gui = MetalGUI(design)

# 3. Create the 7-Qubit Transmon Layout
# Central tunable transmon (Q0)
q0_opts = dict(
    pos_x="0.0mm",
    pos_y="0.0mm",
    pad_width="450um",
    pad_height="30um",
    pocket_width="650um",
    pocket_height="650um",
    orientation="0"
)
q0 = TransmonPocket6(design, "Q0_Center", options=q0_opts)

# 6 Peripheral fixed-frequency transmons around the perimeter (Hexagonal layout)
radius = 2.8 # mm from center
angles = [0, 60, 120, 180, 240, 300]

for i, angle_deg in enumerate(angles, 1):
    angle_rad = math.radians(angle_deg)
    px = f"{radius * math.cos(angle_rad):.3f}mm"
    py = f"{radius * math.sin(angle_rad):.3f}mm"
    
    q_opts = dict(
        pos_x=px,
        pos_y=py,
        pad_width="450um",
        pad_height="30um",
        pocket_width="650um",
        pocket_height="650um",
        orientation=str(angle_deg)
    )
    TransmonPocket6(design, f"Q{i}", options=q_opts)

# 4. Rebuild geometry and autoscale viewport
design.rebuild()
gui.autoscale()
gui.rebuild()

print("\n[SUCCESS] 7-Qubit Lattice placed on 10mm x 10mm substrate:")
print("  - Q0_Center (Central Tunable Transmon)")
print("  - Q1 to Q6 (Peripheral Transmons at radius = 2.8mm)")
print("\nNative Qiskit Metal GUI window is now active.")
print("You can inspect, zoom, pan, and modify components directly in the GUI.")
print("Close the window when finished with your design session.")
print("=" * 70)

# Keep the Qt Application event loop running
try:
    gui.qApp.exec_()
except Exception as e:
    print(f"Application closed: {e}")
