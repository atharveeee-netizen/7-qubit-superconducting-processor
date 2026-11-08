import matplotlib.pyplot as plt
import matplotlib.patches as patches
import numpy as np

def draw_ground(ax, x, y, width=0.65, height=0.35, color='#1e293b', lw=2.0):
    """Draws a standard 3-tier RF ground symbol."""
    ax.plot([x, x], [y + height, y], color=color, lw=lw)
    ax.plot([x - width/2, x + width/2], [y, y], color=color, lw=lw)
    ax.plot([x - width*0.32, x + width*0.32], [y - height*0.38, y - height*0.38], color=color, lw=lw)
    ax.plot([x - width*0.14, x + width*0.14], [y - height*0.76, y - height*0.76], color=color, lw=lw)

def draw_capacitor(ax, x, y, vertical=True, length=0.6, gap=0.18, plate_len=0.7, color='#1e293b', lw=2.2):
    """Draws a standard parallel-plate capacitor."""
    if vertical:
        ax.plot([x, x], [y + length/2, y + gap/2], color=color, lw=lw)
        ax.plot([x - plate_len/2, x + plate_len/2], [y + gap/2, y + gap/2], color=color, lw=lw)
        ax.plot([x - plate_len/2, x + plate_len/2], [y - gap/2, y - gap/2], color=color, lw=lw)
        ax.plot([x, x], [y - gap/2, y - length/2], color=color, lw=lw)
    else:
        ax.plot([x - length/2, x - gap/2], [y, y], color=color, lw=lw)
        ax.plot([x - gap/2, x - gap/2], [y - plate_len/2, y + plate_len/2], color=color, lw=lw)
        ax.plot([x + gap/2, x + gap/2], [y - plate_len/2, y + plate_len/2], color=color, lw=lw)
        ax.plot([x + gap/2, x + length/2], [y, y], color=color, lw=lw)

def draw_inductor(ax, x, y, length=1.4, n_loops=4, radius=0.22, color='#1e293b', lw=2.2):
    """Draws a standard multi-loop inductor vertically."""
    half_l = length / 2
    y_start = y + half_l
    y_end = y - half_l
    lead = 0.22
    
    ax.plot([x, x], [y_start, y_start - lead], color=color, lw=lw)
    ax.plot([x, x], [y_end + lead, y_end], color=color, lw=lw)
    
    coil_span = (length - 2*lead)
    loop_h = coil_span / n_loops
    
    for i in range(n_loops):
        cy = (y_start - lead) - (i + 0.5) * loop_h
        theta = np.linspace(-np.pi/2, np.pi/2, 40)
        xs = x - radius * np.cos(theta)
        ys = cy + (loop_h/2) * np.sin(theta)
        ax.plot(xs, ys, color=color, lw=lw)

def draw_josephson_junction(ax, x, y, size=0.6, lead=0.4, color='#1e293b', lw=2.2):
    """Draws a standard IEEE Josephson Junction symbol (square with an X)."""
    ax.plot([x, x], [y + size/2 + lead, y + size/2], color=color, lw=lw)
    ax.plot([x, x], [y - size/2, y - size/2 - lead], color=color, lw=lw)
    
    rect = patches.Rectangle((x - size/2, y - size/2), size, size, 
                             facecolor='#ffffff', edgecolor=color, lw=lw, zorder=3)
    ax.add_patch(rect)
    ax.plot([x - size/2, x + size/2], [y - size/2, y + size/2], color=color, lw=lw, zorder=4)
    ax.plot([x - size/2, x + size/2], [y + size/2, y - size/2], color=color, lw=lw, zorder=4)

def draw_port(ax, x, y, text, subtext, is_left=True, color='#1e293b', lw=2.0):
    """Draws an RF 50-ohm coaxial port launchpad symbol."""
    w, h = 1.15, 0.72
    px = x - w if is_left else x
    rect = patches.FancyBboxPatch((px, y - h/2), w, h, boxstyle="round,pad=0.05",
                                  facecolor='#f8fafc', edgecolor=color, lw=lw, zorder=3)
    ax.add_patch(rect)
    tx = px + w/2
    ax.text(tx, y + 0.09, text, ha='center', va='center', fontsize=9.5, fontweight='bold', color=color)
    ax.text(tx, y - 0.17, subtext, ha='center', va='center', fontsize=7.5, color='#64748b')

def build_schematic():
    fig, ax = plt.subplots(figsize=(11.0, 5.0), dpi=300)
    ax.set_xlim(-0.6, 13.6)
    ax.set_ylim(-2.1, 4.1)
    ax.axis('off')
    
    # 1. Background grouping panels
    # Resonator Subsystem Panel (encapsulating C_in through Node A to right before C_c)
    res_box = patches.FancyBboxPatch((1.3, -1.85), 5.0, 5.5, boxstyle="round,pad=0.15",
                                     facecolor='#f0fdf4', edgecolor='#86efac', lw=1.6, ls='--', alpha=0.9, zorder=1)
    ax.add_patch(res_box)
    ax.text(3.8, 3.35, "Readout Resonator Subsystem", ha='center', va='center', 
            fontsize=11.0, fontweight='bold', color='#166534')
    ax.text(3.8, 3.0, "Quarter-Wave ($\lambda/4$) Distributed CPW Equivalent Tank", 
            ha='center', va='center', fontsize=8.5, color='#15803d', style='italic')

    # Transmon Subsystem Panel (starting right after C_c)
    q_box = patches.FancyBboxPatch((7.6, -1.85), 4.3, 5.5, boxstyle="round,pad=0.15",
                                   facecolor='#eff6ff', edgecolor='#93c5fd', lw=1.6, ls='--', alpha=0.9, zorder=1)
    ax.add_patch(q_box)
    ax.text(9.75, 3.35, "Transmon Qubit Subsystem", ha='center', va='center', 
            fontsize=11.0, fontweight='bold', color='#1e40af')
    ax.text(9.75, 3.0, "Non-Linear Anharmonic Artificial Atom ($E_J / E_C \\approx 50$)", 
            ha='center', va='center', fontsize=8.5, color='#2563eb', style='italic')

    # Rails and levels
    y_bus = 1.95
    y_tank_top = 1.25
    y_tank_bot = -0.55
    y_ground = -0.90
    ground_h = 0.35

    # Port 1
    draw_port(ax, 0.9, y_bus, "Port 1", "$Z_0 = 50\,\Omega$", is_left=True)
    ax.plot([0.9, 1.8], [y_bus, y_bus], color='#1e293b', lw=2.2)

    # Input Coupler C_in
    draw_capacitor(ax, 2.1, y_bus, vertical=False, length=0.6, gap=0.18, plate_len=0.7)
    ax.text(2.1, y_bus + 0.45, "$C_{\mathrm{in}} = 2.0\mathrm{\ fF}$", ha='center', va='bottom', 
            fontsize=9.5, fontweight='bold', color='#0f172a')
    ax.plot([2.4, 4.3], [y_bus, y_bus], color='#1e293b', lw=2.2)

    # Node A (Resonator Node)
    ax.scatter([4.3], [y_bus], s=45, color='#1e293b', zorder=5)
    ax.text(4.3, y_bus + 0.3, "Node A", ha='center', va='bottom', fontsize=8.5, color='#475569')

    # Drop from bus to resonator parallel branches
    ax.plot([4.3, 4.3], [y_bus, y_tank_top], color='#1e293b', lw=2.2)
    ax.plot([3.3, 5.3], [y_tank_top, y_tank_top], color='#1e293b', lw=2.2)

    # Left Branch: Inductor L_r
    draw_inductor(ax, 3.3, (y_tank_top + y_tank_bot)/2, length=1.8, n_loops=4, radius=0.22)
    ax.text(2.85, (y_tank_top + y_tank_bot)/2, "$L_r = 1.50\mathrm{\ nH}$", ha='right', va='center', 
            fontsize=9.0, fontweight='bold', color='#166534')

    # Right Branch: Capacitor C_r
    draw_capacitor(ax, 5.3, (y_tank_top + y_tank_bot)/2, vertical=True, length=1.8, gap=0.2, plate_len=0.65)
    ax.text(5.75, (y_tank_top + y_tank_bot)/2, "$C_r = 340\mathrm{\ fF}$", ha='left', va='center', 
            fontsize=9.0, fontweight='bold', color='#166534')

    # Bottom rail of Resonator Tank
    ax.plot([3.3, 5.3], [y_tank_bot, y_tank_bot], color='#1e293b', lw=2.2)
    draw_ground(ax, 4.3, y_ground, width=0.65, height=ground_h)
    ax.text(4.3, -1.35, "$\omega_r / 2\pi = 7.042\mathrm{\ GHz}$\nLoaded $Q_L \\approx 7{,}040$", ha='center', va='top', 
            fontsize=8.5, fontweight='bold', color='#166534')

    # Inter-cavity Coupling Capacitor C_c (in the gap between the two subsystems)
    ax.plot([4.3, 6.7], [y_bus, y_bus], color='#1e293b', lw=2.2)
    draw_capacitor(ax, 7.0, y_bus, vertical=False, length=0.6, gap=0.18, plate_len=0.7)
    ax.text(7.0, y_bus + 0.45, "$C_c = 4.0\mathrm{\ fF}$", ha='center', va='bottom', 
            fontsize=9.5, fontweight='bold', color='#0f172a')
    ax.text(7.0, y_bus - 0.45, "Transverse Coupling\n$g/2\pi \\approx 60\mathrm{\ MHz}$", ha='center', va='top', 
            fontsize=8.0, color='#475569', style='italic')

    # Line from C_c to Node B
    ax.plot([7.3, 9.75], [y_bus, y_bus], color='#1e293b', lw=2.2)
    ax.scatter([9.75], [y_bus], s=45, color='#1e293b', zorder=5)
    ax.text(9.75, y_bus + 0.3, "Node B", ha='center', va='bottom', fontsize=8.5, color='#475569')

    # Drop from bus to transmon parallel branches
    ax.plot([9.75, 9.75], [y_bus, y_tank_top], color='#1e293b', lw=2.2)
    ax.plot([8.75, 10.75], [y_tank_top, y_tank_top], color='#1e293b', lw=2.2)

    # Left Branch: Shunt Capacitor C_q
    draw_capacitor(ax, 8.75, (y_tank_top + y_tank_bot)/2, vertical=True, length=1.8, gap=0.2, plate_len=0.65)
    ax.text(8.3, (y_tank_top + y_tank_bot)/2, "$C_q = 70\mathrm{\ fF}$", ha='right', va='center', 
            fontsize=9.0, fontweight='bold', color='#1e40af')

    # Right Branch: Josephson Junction (Box with X)
    draw_josephson_junction(ax, 10.75, (y_tank_top + y_tank_bot)/2, size=0.6, lead=0.6)
    ax.text(11.2, (y_tank_top + y_tank_bot)/2 + 0.15, "$L_J = 10.0\mathrm{\ nH}$", ha='left', va='center', 
            fontsize=9.0, fontweight='bold', color='#1e40af')
    ax.text(11.2, (y_tank_top + y_tank_bot)/2 - 0.22, "$I_c \\approx 32.9\mathrm{\ nA}$", ha='left', va='center', 
            fontsize=8.0, color='#64748b')

    # Bottom rail of Transmon Tank
    ax.plot([8.75, 10.75], [y_tank_bot, y_tank_bot], color='#1e293b', lw=2.2)
    draw_ground(ax, 9.75, y_ground, width=0.65, height=ground_h)
    ax.text(9.75, -1.35, "$\omega_{01} / 2\pi \\approx 5.000\mathrm{\ GHz}$\nAnharmonicity $\\alpha \\approx -280\mathrm{\ MHz}$", 
            ha='center', va='top', fontsize=8.5, fontweight='bold', color='#1e40af')

    # Line from Node B to Port 2
    ax.plot([9.75, 12.1], [y_bus, y_bus], color='#1e293b', lw=2.2)
    draw_port(ax, 12.1, y_bus, "Port 2", "$Z_0 = 50\,\Omega$", is_left=False)

    plt.tight_layout()
    output_png = 'lumped_circuit_schematic.png'
    plt.savefig(output_png, dpi=300, bbox_inches='tight', facecolor='white')
    print("Successfully generated:", output_png)

if __name__ == '__main__':
    build_schematic()
