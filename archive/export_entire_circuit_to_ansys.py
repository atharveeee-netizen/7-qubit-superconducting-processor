import os
import sys
import shapely.geometry
from collections import OrderedDict
import numpy as np

os.environ['OMP_NUM_THREADS'] = '1'
os.environ['MKL_NUM_THREADS'] = '1'
os.environ['OPENBLAS_NUM_THREADS'] = '1'
os.environ['KMP_DUPLICATE_LIB_OK'] = 'True'

import qiskit_metal as metal
from qiskit_metal import designs, Dict
from qiskit_metal.qlibrary.qubits.transmon_pocket_6 import TransmonPocket6
from qiskit_metal.qlibrary.qubits.transmon_pocket_cl import TransmonPocketCL
from qiskit_metal.qlibrary.tlines.meandered import RouteMeander
from qiskit_metal.qlibrary.terminations.launchpad_wb import LaunchpadWirebond

def poly_to_ansys_code(name, coords, is_cut):
    code = []
    code.append(f"# Element: {name}")
    code.append("pts = ['NAME:PolylinePoints']")
    code.append("segs = ['NAME:PolylineSegments']")
    for i, (x, y) in enumerate(coords):
        code.append(f"pts.append(['NAME:PLPoint', 'X:=', '{x:.6f}mm', 'Y:=', '{y:.6f}mm', 'Z:=', '0.0mm'])")
        code.append(f"segs.append(['NAME:PLSegment', 'SegmentType:=', 'Line', 'StartIndex:=', {i}, 'NoOfPoints:=', 2])")
    code.append(f"pts.append(['NAME:PLPoint', 'X:=', '{coords[0][0]:.6f}mm', 'Y:=', '{coords[0][1]:.6f}mm', 'Z:=', '0.0mm'])")
    
    color = '(255 100 100)' if is_cut else '(200 220 255)'
    code.append("oEditor.CreatePolyline(")
    code.append("    ['NAME:PolylineParameters', 'IsPolylineCovered:=', True, 'IsPolylineClosed:=', True, pts, segs],")
    code.append("    [")
    code.append("        'NAME:Attributes',")
    code.append(f"        'Name:=', '{name}',")
    code.append("        'Flags:=', '',")
    code.append(f"        'Color:=', '{color}',")
    code.append("        'Transparency:=', 0.0,")
    code.append("        'PartCoordinateSystem:=', 'Global',")
    code.append("        'UDMId:=', '',")
    code.append("        'MaterialName:=', 'vacuum',")
    code.append("        'SolveInside:=', True")
    code.append("    ]")
    code.append(")")
    return "\n".join(code)

def generate_ansys_design_body(design, design_name, chip_size_x, chip_size_y, is_single_q4=False):
    poly_table = design.qgeometry.tables['poly']
    path_table = design.qgeometry.tables['path']
    
    lines = []
    lines.append(f"# =====================================================================")
    lines.append(f"# DESIGN: {design_name}")
    lines.append(f"# =====================================================================")
    lines.append(f"design_name = '{design_name}'")
    lines.append("try:")
    lines.append("    d_names = [d.GetName() for d in oProject.GetDesigns()]")
    lines.append("except Exception:")
    lines.append("    d_names = []")
    lines.append("if design_name in d_names:")
    lines.append("    try:")
    lines.append("        oProject.SetActiveDesign(design_name)")
    lines.append("    except Exception:")
    lines.append("        pass")
    lines.append("    try:")
    lines.append("        oDesign = oProject.GetDesign(design_name)")
    lines.append("    except Exception:")
    lines.append("        oDesign = oProject.GetActiveDesign()")
    lines.append("else:")
    lines.append("    oDesign = oProject.InsertDesign('HFSS', design_name, 'DrivenModal', '')")
    lines.append("if oDesign is None:")
    lines.append("    oDesign = oProject.GetActiveDesign()")
    lines.append("oEditor = oDesign.SetActiveEditor('3D Modeler')")
    lines.append("oBoundarySetup = oDesign.GetModule('BoundarySetup')\n")
    
    # Clean boundaries
    lines.append("try:")
    lines.append("    for b in list(oBoundarySetup.GetBoundaries()):")
    lines.append("        try:")
    lines.append("            oBoundarySetup.DeleteBoundaries([b])")
    lines.append("        except Exception:")
    lines.append("            pass")
    lines.append("except Exception:")
    lines.append("    pass\n")
    
    # Clean objects
    lines.append("try:")
    lines.append("    objs_to_del = []")
    lines.append("    try:")
    lines.append("        objs_to_del = list(oEditor.GetMatchedObjectName('*'))")
    lines.append("    except Exception:")
    lines.append("        pass")
    lines.append("    if not objs_to_del:")
    lines.append("        try:")
    lines.append("            objs_to_del = list(oEditor.GetObjectsInGroup('All Objects'))")
    lines.append("        except Exception:")
    lines.append("            pass")
    lines.append("    if objs_to_del:")
    lines.append("        oEditor.Delete(['NAME:Selections', 'Selections:=', ','.join(objs_to_del)])")
    lines.append("except Exception:")
    lines.append("    pass\n")
    
    # Substrate
    half_x = chip_size_x / 2.0
    half_y = chip_size_y / 2.0
    lines.append(f"# Substrate Box ({chip_size_x}mm x {chip_size_y}mm x 0.5mm)")
    lines.append("oEditor.CreateBox(")
    lines.append("    [")
    lines.append("        'NAME:BoxParameters',")
    lines.append(f"        'XPosition:=', '-{half_x}mm',")
    lines.append(f"        'YPosition:=', '-{half_y}mm',")
    lines.append("        'ZPosition:=', '-0.5mm',")
    lines.append(f"        'XSize:=', '{chip_size_x}mm',")
    lines.append(f"        'YSize:=', '{chip_size_y}mm',")
    lines.append("        'ZSize:=', '0.5mm'")
    lines.append("    ],")
    lines.append("    [")
    lines.append("        'NAME:Attributes',")
    lines.append("        'Name:=', 'main_sub_box',")
    lines.append("        'Flags:=', '',")
    lines.append("        'Color:=', '(160 160 170)',")
    lines.append("        'Transparency:=', 0.5,")
    lines.append("        'PartCoordinateSystem:=', 'Global',")
    lines.append("        'UDMId:=', '',")
    lines.append("        'MaterialName:=', 'silicon',")
    lines.append("        'SolveInside:=', True")
    lines.append("    ]")
    lines.append(")\n")
    
    # Ground plane
    lines.append(f"# Ground Plane Sheet ({chip_size_x}mm x {chip_size_y}mm)")
    lines.append("oEditor.CreateRectangle(")
    lines.append("    [")
    lines.append("        'NAME:RectangleParameters',")
    lines.append("        'IsCovered:=', True,")
    lines.append(f"        'XStart:=', '-{half_x}mm',")
    lines.append(f"        'YStart:=', '-{half_y}mm',")
    lines.append("        'ZStart:=', '0.0mm',")
    lines.append(f"        'Width:=', '{chip_size_x}mm',")
    lines.append(f"        'Height:=', '{chip_size_y}mm',")
    lines.append("        'WhichAxis:=', 'Z'")
    lines.append("    ],")
    lines.append("    [")
    lines.append("        'NAME:Attributes',")
    lines.append("        'Name:=', 'ground_main_plane',")
    lines.append("        'Flags:=', '',")
    lines.append("        'Color:=', '(180 180 180)',")
    lines.append("        'Transparency:=', 0.85,")
    lines.append("        'PartCoordinateSystem:=', 'Global',")
    lines.append("        'UDMId:=', '',")
    lines.append("        'MaterialName:=', 'vacuum',")
    lines.append("        'SolveInside:=', True")
    lines.append("    ]")
    lines.append(")\n")
    
    cut_names = []
    metal_names = []
    
    for idx, row in poly_table.iterrows():
        cname = design._components[row['component']].name
        ename = row['name']
        obj_name = f"{ename}_{cname}_{idx}"
        geom = row['geometry']
        coords = list(geom.exterior.coords)
        if coords[0] == coords[-1] and len(coords) > 1:
            coords = coords[:-1]
        is_cut = bool(row['subtract'])
        if is_cut:
            cut_names.append(obj_name)
        else:
            metal_names.append(obj_name)
        lines.append(poly_to_ansys_code(obj_name, coords, is_cut))
        
    for idx, row in path_table.iterrows():
        cname = design._components[row['component']].name
        ename = row['name']
        obj_name = f"{ename}_{cname}_{idx}"
        geom = row['geometry']
        width = float(row['width'])
        poly_geom = geom.buffer(width / 2.0, cap_style=shapely.geometry.CAP_STYLE.flat, join_style=shapely.geometry.JOIN_STYLE.mitre)
        if isinstance(poly_geom, shapely.geometry.MultiPolygon):
            poly_geom = poly_geom.geoms[0]
        coords = list(poly_geom.exterior.coords)
        if coords[0] == coords[-1] and len(coords) > 1:
            coords = coords[:-1]
        is_cut = bool(row['subtract'])
        if is_cut:
            cut_names.append(obj_name)
        else:
            metal_names.append(obj_name)
        lines.append(poly_to_ansys_code(obj_name, coords, is_cut))
        
    # Subtract
    lines.append("\n# Subtract All Pockets & CPW Slots from Ground Plane")
    lines.append(f"cut_list = {repr(cut_names)}")
    lines.append("try:")
    lines.append("    existing = set(oEditor.GetMatchedObjectName('*')) if hasattr(oEditor, 'GetMatchedObjectName') else set(cut_list)")
    lines.append("    valid_cuts = [c for c in cut_list if c in existing] if existing else cut_list")
    lines.append("    if valid_cuts:")
    lines.append("        oEditor.Subtract(")
    lines.append("            ['NAME:Selections', 'Blank Parts:=', 'ground_main_plane', 'Tool Parts:=', ','.join(valid_cuts)],")
    lines.append("            ['NAME:SubtractParameters', 'KeepOriginals:=', False]")
    lines.append("        )")
    lines.append("except Exception as sub_err:")
    lines.append("    print('[!] Subtract notice: ' + str(sub_err))\n")
    
    # Perfect E
    lines.append("# Assign Perfect E to Ground Plane & Metal Traces/Pads")
    lines.append(f"metal_list = ['ground_main_plane'] + {repr(metal_names)}")
    lines.append("try:")
    lines.append("    existing = set(oEditor.GetMatchedObjectName('*')) if hasattr(oEditor, 'GetMatchedObjectName') else set(metal_list)")
    lines.append("    valid_metals = [m for m in metal_list if m in existing] if existing else metal_list")
    lines.append("    if valid_metals:")
    lines.append("        oBoundarySetup.AssignPerfectE(")
    lines.append("            ['NAME:PerfE_Superconductors', 'Objects:=', valid_metals, 'InfGroundPlane:=', False]")
    lines.append("        )")
    lines.append("except Exception as pe_err:")
    lines.append("    print('[!] Perfect E notice: ' + str(pe_err))\n")
    
    # Josephson Junction on Q4
    qy_center = 0.0 if is_single_q4 else 0.87
    y_start_gap = qy_center - 0.015
    y_end_gap = qy_center + 0.015
    
    lines.append(f"# Josephson Junction 2D Sheet across 30um gap (center y={qy_center}mm)")
    lines.append("oEditor.CreateRectangle(")
    lines.append("    [")
    lines.append("        'NAME:RectangleParameters',")
    lines.append("        'IsCovered:=', True,")
    lines.append("        'XStart:=', '-0.015mm',")
    lines.append(f"        'YStart:=', '{y_start_gap:.6f}mm',")
    lines.append("        'ZStart:=', '0.0mm',")
    lines.append("        'Width:=', '0.03mm',")
    lines.append("        'Height:=', '0.03mm',")
    lines.append("        'WhichAxis:=', 'Z'")
    lines.append("    ],")
    lines.append("    [")
    lines.append("        'NAME:Attributes',")
    lines.append("        'Name:=', 'JJ_Q4_sheet',")
    lines.append("        'Flags:=', '',")
    lines.append("        'Color:=', '(255 0 0)',")
    lines.append("        'Transparency:=', 0.2,")
    lines.append("        'PartCoordinateSystem:=', 'Global',")
    lines.append("        'UDMId:=', '',")
    lines.append("        'MaterialName:=', 'vacuum',")
    lines.append("        'SolveInside:=', True")
    lines.append("    ]")
    lines.append(")")
    
    lines.append("# Visual Red Polyline across junction")
    lines.append("try:")
    lines.append("    pts_jj = ['NAME:PolylinePoints']")
    lines.append(f"    pts_jj.append(['NAME:PLPoint', 'X:=', '0.0mm', 'Y:=', '{y_start_gap:.6f}mm', 'Z:=', '0.0mm'])")
    lines.append(f"    pts_jj.append(['NAME:PLPoint', 'X:=', '0.0mm', 'Y:=', '{y_end_gap:.6f}mm', 'Z:=', '0.0mm'])")
    lines.append("    segs_jj = ['NAME:PolylineSegments']")
    lines.append("    segs_jj.append(['NAME:PLSegment', 'SegmentType:=', 'Line', 'StartIndex:=', 0, 'NoOfPoints:=', 2])")
    lines.append("    oEditor.CreatePolyline(")
    lines.append("        ['NAME:PolylineParameters', 'IsPolylineCovered:=', False, 'IsPolylineClosed:=', False, pts_jj, segs_jj],")
    lines.append("        [")
    lines.append("            'NAME:Attributes',")
    lines.append("            'Name:=', 'JJ_Q4_line',")
    lines.append("            'Flags:=', '',")
    lines.append("            'Color:=', '(255 0 0)',")
    lines.append("            'Transparency:=', 0.0,")
    lines.append("            'PartCoordinateSystem:=', 'Global',")
    lines.append("            'UDMId:=', '',")
    lines.append("            'MaterialName:=', 'vacuum',")
    lines.append("            'SolveInside:=', True")
    lines.append("        ]")
    lines.append("    )")
    lines.append("except Exception:")
    lines.append("    pass\n")
    
    lines.append("try:")
    lines.append("    oBoundarySetup.AssignLumpedRLC(")
    lines.append("        [")
    lines.append("            'NAME:Q4_Josephson_Junction',")
    lines.append("            'Objects:=', ['JJ_Q4_sheet'],")
    lines.append("            'CurrentLine:=', [")
    lines.append("                'NAME:CurrentLine',")
    lines.append(f"                'Start:=', ['0.0mm', '{y_start_gap:.6f}mm', '0.0mm'],")
    lines.append(f"                'End:=', ['0.0mm', '{y_end_gap:.6f}mm', '0.0mm']")
    lines.append("            ],")
    lines.append("            'UseResist:=', False,")
    lines.append("            'UseInduct:=', True,")
    lines.append("            'Inductance:=', '12.31nH',")
    lines.append("            'UseCap:=', True,")
    lines.append("            'Capacitance:=', '2.0fF'")
    lines.append("        ]")
    lines.append("    )")
    lines.append(f"    print('[+] Assigned Q4 Lumped RLC boundary for {design_name}!')")
    lines.append("except Exception as rlc_err:")
    lines.append("    print('[*] Note on Lumped RLC assignment: ' + str(rlc_err))\n")
    
    lines.append("oEditor.FitAll()\n")
    return "\n".join(lines)

print("[*] 1. Synthesizing Single Qubit Q4 Design (5mm x 5mm)...")
d_single = designs.DesignPlanar({}, True)
d_single.chips.main.size['size_x'] = '5mm'
d_single.chips.main.size['size_y'] = '5mm'
q4_single_opts = Dict(
    pos_x='0.0um', pos_y='0.0um', orientation='0.0', pad_width='455um', pad_height='90um', pad_gap='30um',
    pocket_width='650um', pocket_height='650um', make_CL=True, cl_gap='6um', cl_width='10um', cl_length='20um',
    cl_ground_gap='6um', cl_pocket_edge='50', cl_off_center='0um',
    connection_pads=Dict(
        a=Dict(loc_W=-1, loc_H=-1, pad_width='50um', pad_height='30um', cpw_width='10um', cpw_gap='6um'),
        b=Dict(loc_W=1,  loc_H=-1, pad_width='50um', pad_height='30um', cpw_width='10um', cpw_gap='6um')
    )
)
TransmonPocketCL(d_single, 'Q4', options=q4_single_opts)
d_single.rebuild()
single_body = generate_ansys_design_body(d_single, 'Simon_Q4_Single_Qubit', 5.0, 5.0, is_single_q4=True)

print("[*] 2. Synthesizing Full 7-Qubit Complete Processor Design (10mm x 10mm)...")
d_full = designs.DesignPlanar({}, True)
d_full.chips.main.size['size_x'] = '10mm'
d_full.chips.main.size['size_y'] = '10mm'
q4_full_opts = Dict(
    pos_x="0.0mm", pos_y="0.87mm", orientation="0.0", pad_width="455um", pad_height="90um", pad_gap="30um",
    pocket_width="650um", pocket_height="650um", make_CL=True, cl_gap="6um", cl_width="10um", cl_length="20um",
    cl_ground_gap="6um", cl_pocket_edge="50", cl_off_center="0um",
    connection_pads=Dict(
        bus_left=Dict(loc_W=-1, loc_H=-1, pad_width='50um', pad_height='30um'),
        bus_right=Dict(loc_W=1, loc_H=-1, pad_width='50um', pad_height='30um')
    )
)
TransmonPocketCL(d_full, "Q4", options=q4_full_opts)
other_qubits = {
    "Q0": Dict(pos_x="-2.5mm", pos_y="0.0mm", orientation="90.0", connection_pads=Dict(bus_top=Dict(loc_W=1, loc_H=1), readout=Dict(loc_W=-1, loc_H=-1))),
    "Q1": Dict(pos_x="-2.5mm", pos_y="1.8mm", orientation="90.0", connection_pads=Dict(bus_bot=Dict(loc_W=1, loc_H=-1), bus_right=Dict(loc_W=-1, loc_H=-1), readout=Dict(loc_W=1, loc_H=1))),
    "Q3": Dict(pos_x="-1.35mm", pos_y="0.87mm", orientation="0.0", connection_pads=Dict(bus_left=Dict(loc_W=-1, loc_H=1), bus_right=Dict(loc_W=1, loc_H=-1), readout=Dict(loc_W=1, loc_H=1))),
    "Q5": Dict(pos_x="1.35mm", pos_y="0.87mm", orientation="0.0", connection_pads=Dict(bus_left=Dict(loc_W=-1, loc_H=-1), bus_right=Dict(loc_W=1, loc_H=1), readout=Dict(loc_W=-1, loc_H=1))),
    "Q2": Dict(pos_x="2.5mm", pos_y="1.8mm", orientation="90.0", connection_pads=Dict(bus_bot=Dict(loc_W=1, loc_H=-1), bus_left=Dict(loc_W=-1, loc_H=-1), readout=Dict(loc_W=1, loc_H=1))),
    "Q6": Dict(pos_x="2.5mm", pos_y="0.0mm", orientation="90.0", connection_pads=Dict(bus_top=Dict(loc_W=1, loc_H=1), readout=Dict(loc_W=-1, loc_H=-1))),
}
for name, opts in other_qubits.items():
    opts.update(dict(pad_width="455um", pad_height="90um", pad_gap="30um", pocket_width="650um", pocket_height="650um"))
    TransmonPocket6(d_full, name, options=opts)
launchpads = {
    "LP_Q1": Dict(pos_x="-2.5mm", pos_y="4.0mm", orientation="-90.0"),
    "LP_Q3": Dict(pos_x="-1.0mm", pos_y="4.2mm", orientation="-90.0"),
    "LP_Q5": Dict(pos_x="1.0mm",  pos_y="4.2mm", orientation="-90.0"),
    "LP_Q2": Dict(pos_x="2.5mm",  pos_y="4.0mm", orientation="-90.0"),
    "LP_Q0": Dict(pos_x="-2.5mm", pos_y="-2.0mm", orientation="90.0"),
    "LP_Q6": Dict(pos_x="2.5mm",  pos_y="-2.0mm", orientation="90.0"),
}
for name, opts in launchpads.items():
    LaunchpadWirebond(d_full, name, options=opts)
readouts = [
    ("Readout_Q0", "Q0", "readout", "LP_Q0", "tie"),
    ("Readout_Q1", "Q1", "readout", "LP_Q1", "tie"),
    ("Readout_Q3", "Q3", "readout", "LP_Q3", "tie"),
    ("Readout_Q5", "Q5", "readout", "LP_Q5", "tie"),
    ("Readout_Q2", "Q2", "readout", "LP_Q2", "tie"),
    ("Readout_Q6", "Q6", "readout", "LP_Q6", "tie"),
]
for name, q_comp, q_pin, lp_comp, lp_pin in readouts:
    RouteMeander(d_full, name, options=Dict(pin_inputs=Dict(start_pin=Dict(component=q_comp, pin=q_pin), end_pin=Dict(component=lp_comp, pin=lp_pin)), fillet="0um"))
coupling_buses = [
    ("Bus_Q0_Q1", "Q0", "bus_top", "Q1", "bus_bot"),
    ("Bus_Q1_Q3", "Q1", "bus_right", "Q3", "bus_left"),
    ("Bus_Q3_Q4", "Q3", "bus_right", "Q4", "bus_left"),
    ("Bus_Q4_Q5", "Q4", "bus_right", "Q5", "bus_left"),
    ("Bus_Q5_Q2", "Q5", "bus_right", "Q2", "bus_left"),
    ("Bus_Q2_Q6", "Q2", "bus_bot", "Q6", "bus_top"),
]
for name, q_start, pin_start, q_end, pin_end in coupling_buses:
    RouteMeander(d_full, name, options=Dict(pin_inputs=Dict(start_pin=Dict(component=q_start, pin=pin_start), end_pin=Dict(component=q_end, pin=pin_end)), fillet="0um"))
d_full.rebuild()
full_body = generate_ansys_design_body(d_full, 'Simon_7Qubit_Complete_Processor', 10.0, 10.0, is_single_q4=False)

header = [
    "# =====================================================================",
    "# Ansys HFSS Standalone Python Script - Simon Quantum Hardware",
    "# =====================================================================",
    "import sys",
    "try:",
    "    import ScriptEnv",
    "    ScriptEnv.Initialize('Ansoft.ElectronicsDesktop')",
    "except Exception:",
    "    pass\n",
    "try:",
    "    oDesktop",
    "except NameError:",
    "    try:",
    "        import win32com.client",
    "        app = win32com.client.Dispatch('Ansoft.ElectronicsDesktop')",
    "        oDesktop = app.GetAppDesktop() if hasattr(app, 'GetAppDesktop') else app",
    "    except Exception as e:",
    "        print('[!] Could not get oDesktop: ' + str(e))\n",
    "try:",
    "    oDesktop.RestoreWindow()",
    "except Exception:",
    "    pass\n",
    "oProject = oDesktop.GetActiveProject()",
    "if oProject is None:",
    "    oProject = oDesktop.NewProject()",
    "    print('[+] Created new Ansys project: ' + oProject.GetName())",
    "else:",
    "    print('[+] Using active Ansys project: ' + oProject.GetName())\n"
]

header_str = "\n".join(header)

# 1. Standalone Single Qubit Q4 script
single_script = header_str + "\n" + single_body + "\nprint('[SUCCESS] Simon Single Qubit Q4 fully generated in Ansys HFSS!')\n"
single_path = r"C:\Users\noobg\Desktop\Quantum Chip - 7-Qubit Design Suite\render_single_qubit_q4_ansys.py"
with open(single_path, "w") as f:
    f.write(single_script)
print(f"[+] Written: {single_path} ({len(single_script)} bytes)")

# 2. Standalone Full 7-Qubit Processor script
full_script = header_str + "\n" + full_body + "\nprint('[SUCCESS] Simon 7-Qubit Complete Processor fully generated in Ansys HFSS!')\n"
full_path = r"C:\Users\noobg\Desktop\Quantum Chip - 7-Qubit Design Suite\render_7qubit_complete_processor_ansys.py"
with open(full_path, "w") as f:
    f.write(full_script)
print(f"[+] Written: {full_path} ({len(full_script)} bytes)")

# 3. Master unified script (Builds BOTH in active project so user can switch between them)
master_script = header_str + "\n" + single_body + "\n" + full_body + "\nprint('[SUCCESS] BOTH Simon HFSS Designs (Single Qubit Q4 AND 7-Qubit Processor) fully generated in Ansys HFSS!')\n"
master_path = r"C:\Users\noobg\Desktop\Quantum Chip - 7-Qubit Design Suite\render_in_ansys_direct.py"
with open(master_path, "w") as f:
    f.write(master_script)
print(f"[+] Written Master Script: {master_path} ({len(master_script)} bytes)")
