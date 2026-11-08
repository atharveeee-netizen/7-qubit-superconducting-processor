# =====================================================================
# Ansys HFSS Standalone Python Script - Simon's 7-Qubit Quantum Processor
# Reference: Simon Quantum Hardware Masterclass (57:45)
# Can be run directly inside Ansys Electronics Desktop via Tools -> Run Script
# Or launched automatically from Windows command line.
# =====================================================================
import sys
try:
    import ScriptEnv
    ScriptEnv.Initialize('Ansoft.ElectronicsDesktop')
except Exception:
    pass

try:
    oDesktop
except NameError:
    try:
        import win32com.client
        app = win32com.client.Dispatch('Ansoft.ElectronicsDesktop')
        oDesktop = app.GetAppDesktop() if hasattr(app, 'GetAppDesktop') else app
    except Exception as e:
        print('[!] Could not get oDesktop: ' + str(e))

try:
    oDesktop.RestoreWindow()
except Exception:
    pass

oProject = oDesktop.GetActiveProject()
if oProject is None:
    oProject = oDesktop.NewProject()
    print('[+] Created new Ansys project: ' + oProject.GetName())
else:
    print('[+] Using active Ansys project: ' + oProject.GetName())

design_name = 'Simon_7Qubit_Processor'
try:
    design_names = [d.GetName() for d in oProject.GetDesigns()]
except Exception:
    design_names = []

if design_name in design_names:
    oDesign = oProject.SetActiveDesign(design_name)
else:
    oDesign = oProject.InsertDesign('HFSS', design_name, 'DrivenModal', '')

if oDesign is None:
    oDesign = oProject.GetActiveDesign()

oEditor = oDesign.SetActiveEditor('3D Modeler')
oBoundarySetup = oDesign.GetModule('BoundarySetup')

# Clean any previous objects for fresh build
try:
    all_objs = oEditor.GetObjectsInGroup('All Objects')
    if all_objs:
        oEditor.Delete(['NAME:Selections', 'Selections:=', ','.join(all_objs)])
except Exception:
    pass

# --- 1. Silicon Substrate Box ---
oEditor.CreateBox(
    [
        'NAME:BoxParameters',
        'XPosition:=', '-5.0mm',
        'YPosition:=', '-5.0mm',
        'ZPosition:=', '-0.5mm',
        'XSize:=', '10.0mm',
        'YSize:=', '10.0mm',
        'ZSize:=', '0.5mm'
    ],
    [
        'NAME:Attributes',
        'Name:=', 'main_sub_box',
        'Flags:=', '',
        'Color:=', '(160 160 170)',
        'Transparency:=', 0.5,
        'PartCoordinateSystem:=', 'Global',
        'UDMId:=', '',
        'MaterialName:=', 'silicon',
        'SolveInside:=', True
    ]
)

# --- 2. Ground Plane Sheet (0.85 Transparency matching Simon's video) ---
oEditor.CreateRectangle(
    [
        'NAME:RectangleParameters',
        'IsCovered:=', True,
        'XStart:=', '-5.0mm',
        'YStart:=', '-5.0mm',
        'ZStart:=', '0.0mm',
        'Width:=', '10.0mm',
        'Height:=', '10.0mm',
        'WhichAxis:=', 'Z'
    ],
    [
        'NAME:Attributes',
        'Name:=', 'ground_main_plane',
        'Flags:=', '',
        'Color:=', '(180 180 180)',
        'Transparency:=', 0.85,
        'PartCoordinateSystem:=', 'Global',
        'UDMId:=', '',
        'MaterialName:=', 'vacuum',
        'SolveInside:=', True
    ]
)

# --- 3. Transmon Pads & Pockets ---
# Element: pad_top_Q4_0
pts = ['NAME:PolylinePoints']
segs = ['NAME:PolylineSegments']
pts.append(['NAME:PLPoint', 'X:=', '-0.227500mm', 'Y:=', '0.885000mm', 'Z:=', '0.0mm'])
segs.append(['NAME:PLSegment', 'SegmentType:=', 'Line', 'StartIndex:=', 0, 'NoOfPoints:=', 2])
pts.append(['NAME:PLPoint', 'X:=', '0.227500mm', 'Y:=', '0.885000mm', 'Z:=', '0.0mm'])
segs.append(['NAME:PLSegment', 'SegmentType:=', 'Line', 'StartIndex:=', 1, 'NoOfPoints:=', 2])
pts.append(['NAME:PLPoint', 'X:=', '0.227500mm', 'Y:=', '0.975000mm', 'Z:=', '0.0mm'])
segs.append(['NAME:PLSegment', 'SegmentType:=', 'Line', 'StartIndex:=', 2, 'NoOfPoints:=', 2])
pts.append(['NAME:PLPoint', 'X:=', '-0.227500mm', 'Y:=', '0.975000mm', 'Z:=', '0.0mm'])
segs.append(['NAME:PLSegment', 'SegmentType:=', 'Line', 'StartIndex:=', 3, 'NoOfPoints:=', 2])
pts.append(['NAME:PLPoint', 'X:=', '-0.227500mm', 'Y:=', '0.885000mm', 'Z:=', '0.0mm'])
oEditor.CreatePolyline(
    ['NAME:PolylineParameters', 'IsPolylineCovered:=', True, 'IsPolylineClosed:=', True, pts, segs],
    [
        'NAME:Attributes',
        'Name:=', 'pad_top_Q4_0',
        'Flags:=', '',
        'Color:=', '(200 220 255)',
        'Transparency:=', 0.0,
        'PartCoordinateSystem:=', 'Global',
        'UDMId:=', '',
        'MaterialName:=', 'vacuum',
        'SolveInside:=', True
    ]
)
# Element: pad_bot_Q4_1
pts = ['NAME:PolylinePoints']
segs = ['NAME:PolylineSegments']
pts.append(['NAME:PLPoint', 'X:=', '-0.227500mm', 'Y:=', '0.765000mm', 'Z:=', '0.0mm'])
segs.append(['NAME:PLSegment', 'SegmentType:=', 'Line', 'StartIndex:=', 0, 'NoOfPoints:=', 2])
pts.append(['NAME:PLPoint', 'X:=', '0.227500mm', 'Y:=', '0.765000mm', 'Z:=', '0.0mm'])
segs.append(['NAME:PLSegment', 'SegmentType:=', 'Line', 'StartIndex:=', 1, 'NoOfPoints:=', 2])
pts.append(['NAME:PLPoint', 'X:=', '0.227500mm', 'Y:=', '0.855000mm', 'Z:=', '0.0mm'])
segs.append(['NAME:PLSegment', 'SegmentType:=', 'Line', 'StartIndex:=', 2, 'NoOfPoints:=', 2])
pts.append(['NAME:PLPoint', 'X:=', '-0.227500mm', 'Y:=', '0.855000mm', 'Z:=', '0.0mm'])
segs.append(['NAME:PLSegment', 'SegmentType:=', 'Line', 'StartIndex:=', 3, 'NoOfPoints:=', 2])
pts.append(['NAME:PLPoint', 'X:=', '-0.227500mm', 'Y:=', '0.765000mm', 'Z:=', '0.0mm'])
oEditor.CreatePolyline(
    ['NAME:PolylineParameters', 'IsPolylineCovered:=', True, 'IsPolylineClosed:=', True, pts, segs],
    [
        'NAME:Attributes',
        'Name:=', 'pad_bot_Q4_1',
        'Flags:=', '',
        'Color:=', '(200 220 255)',
        'Transparency:=', 0.0,
        'PartCoordinateSystem:=', 'Global',
        'UDMId:=', '',
        'MaterialName:=', 'vacuum',
        'SolveInside:=', True
    ]
)
# Element: rect_pk_Q4_2
pts = ['NAME:PolylinePoints']
segs = ['NAME:PolylineSegments']
pts.append(['NAME:PLPoint', 'X:=', '-0.325000mm', 'Y:=', '0.545000mm', 'Z:=', '0.0mm'])
segs.append(['NAME:PLSegment', 'SegmentType:=', 'Line', 'StartIndex:=', 0, 'NoOfPoints:=', 2])
pts.append(['NAME:PLPoint', 'X:=', '0.325000mm', 'Y:=', '0.545000mm', 'Z:=', '0.0mm'])
segs.append(['NAME:PLSegment', 'SegmentType:=', 'Line', 'StartIndex:=', 1, 'NoOfPoints:=', 2])
pts.append(['NAME:PLPoint', 'X:=', '0.325000mm', 'Y:=', '1.195000mm', 'Z:=', '0.0mm'])
segs.append(['NAME:PLSegment', 'SegmentType:=', 'Line', 'StartIndex:=', 2, 'NoOfPoints:=', 2])
pts.append(['NAME:PLPoint', 'X:=', '-0.325000mm', 'Y:=', '1.195000mm', 'Z:=', '0.0mm'])
segs.append(['NAME:PLSegment', 'SegmentType:=', 'Line', 'StartIndex:=', 3, 'NoOfPoints:=', 2])
pts.append(['NAME:PLPoint', 'X:=', '-0.325000mm', 'Y:=', '0.545000mm', 'Z:=', '0.0mm'])
oEditor.CreatePolyline(
    ['NAME:PolylineParameters', 'IsPolylineCovered:=', True, 'IsPolylineClosed:=', True, pts, segs],
    [
        'NAME:Attributes',
        'Name:=', 'rect_pk_Q4_2',
        'Flags:=', '',
        'Color:=', '(255 100 100)',
        'Transparency:=', 0.0,
        'PartCoordinateSystem:=', 'Global',
        'UDMId:=', '',
        'MaterialName:=', 'vacuum',
        'SolveInside:=', True
    ]
)
# Element: bus_left_connector_pad_Q4_3
pts = ['NAME:PolylinePoints']
segs = ['NAME:PolylineSegments']
pts.append(['NAME:PLPoint', 'X:=', '-0.177500mm', 'Y:=', '0.750000mm', 'Z:=', '0.0mm'])
segs.append(['NAME:PLSegment', 'SegmentType:=', 'Line', 'StartIndex:=', 0, 'NoOfPoints:=', 2])
pts.append(['NAME:PLPoint', 'X:=', '-0.227500mm', 'Y:=', '0.750000mm', 'Z:=', '0.0mm'])
segs.append(['NAME:PLSegment', 'SegmentType:=', 'Line', 'StartIndex:=', 1, 'NoOfPoints:=', 2])
pts.append(['NAME:PLPoint', 'X:=', '-0.227500mm', 'Y:=', '0.720000mm', 'Z:=', '0.0mm'])
segs.append(['NAME:PLSegment', 'SegmentType:=', 'Line', 'StartIndex:=', 2, 'NoOfPoints:=', 2])
pts.append(['NAME:PLPoint', 'X:=', '-0.177500mm', 'Y:=', '0.720000mm', 'Z:=', '0.0mm'])
segs.append(['NAME:PLSegment', 'SegmentType:=', 'Line', 'StartIndex:=', 3, 'NoOfPoints:=', 2])
pts.append(['NAME:PLPoint', 'X:=', '-0.177500mm', 'Y:=', '0.750000mm', 'Z:=', '0.0mm'])
oEditor.CreatePolyline(
    ['NAME:PolylineParameters', 'IsPolylineCovered:=', True, 'IsPolylineClosed:=', True, pts, segs],
    [
        'NAME:Attributes',
        'Name:=', 'bus_left_connector_pad_Q4_3',
        'Flags:=', '',
        'Color:=', '(200 220 255)',
        'Transparency:=', 0.0,
        'PartCoordinateSystem:=', 'Global',
        'UDMId:=', '',
        'MaterialName:=', 'vacuum',
        'SolveInside:=', True
    ]
)
# Element: bus_right_connector_pad_Q4_4
pts = ['NAME:PolylinePoints']
segs = ['NAME:PolylineSegments']
pts.append(['NAME:PLPoint', 'X:=', '0.177500mm', 'Y:=', '0.750000mm', 'Z:=', '0.0mm'])
segs.append(['NAME:PLSegment', 'SegmentType:=', 'Line', 'StartIndex:=', 0, 'NoOfPoints:=', 2])
pts.append(['NAME:PLPoint', 'X:=', '0.227500mm', 'Y:=', '0.750000mm', 'Z:=', '0.0mm'])
segs.append(['NAME:PLSegment', 'SegmentType:=', 'Line', 'StartIndex:=', 1, 'NoOfPoints:=', 2])
pts.append(['NAME:PLPoint', 'X:=', '0.227500mm', 'Y:=', '0.720000mm', 'Z:=', '0.0mm'])
segs.append(['NAME:PLSegment', 'SegmentType:=', 'Line', 'StartIndex:=', 2, 'NoOfPoints:=', 2])
pts.append(['NAME:PLPoint', 'X:=', '0.177500mm', 'Y:=', '0.720000mm', 'Z:=', '0.0mm'])
segs.append(['NAME:PLSegment', 'SegmentType:=', 'Line', 'StartIndex:=', 3, 'NoOfPoints:=', 2])
pts.append(['NAME:PLPoint', 'X:=', '0.177500mm', 'Y:=', '0.750000mm', 'Z:=', '0.0mm'])
oEditor.CreatePolyline(
    ['NAME:PolylineParameters', 'IsPolylineCovered:=', True, 'IsPolylineClosed:=', True, pts, segs],
    [
        'NAME:Attributes',
        'Name:=', 'bus_right_connector_pad_Q4_4',
        'Flags:=', '',
        'Color:=', '(200 220 255)',
        'Transparency:=', 0.0,
        'PartCoordinateSystem:=', 'Global',
        'UDMId:=', '',
        'MaterialName:=', 'vacuum',
        'SolveInside:=', True
    ]
)
# Element: cl_metal_Q4_5
pts = ['NAME:PolylinePoints']
segs = ['NAME:PolylineSegments']
pts.append(['NAME:PLPoint', 'X:=', '-0.010000mm', 'Y:=', '0.453000mm', 'Z:=', '0.0mm'])
segs.append(['NAME:PLSegment', 'SegmentType:=', 'Line', 'StartIndex:=', 0, 'NoOfPoints:=', 2])
pts.append(['NAME:PLPoint', 'X:=', '-0.010000mm', 'Y:=', '0.523000mm', 'Z:=', '0.0mm'])
segs.append(['NAME:PLSegment', 'SegmentType:=', 'Line', 'StartIndex:=', 1, 'NoOfPoints:=', 2])
pts.append(['NAME:PLPoint', 'X:=', '-0.020000mm', 'Y:=', '0.523000mm', 'Z:=', '0.0mm'])
segs.append(['NAME:PLSegment', 'SegmentType:=', 'Line', 'StartIndex:=', 2, 'NoOfPoints:=', 2])
pts.append(['NAME:PLPoint', 'X:=', '-0.020000mm', 'Y:=', '0.533000mm', 'Z:=', '0.0mm'])
segs.append(['NAME:PLSegment', 'SegmentType:=', 'Line', 'StartIndex:=', 3, 'NoOfPoints:=', 2])
pts.append(['NAME:PLPoint', 'X:=', '-0.010000mm', 'Y:=', '0.533000mm', 'Z:=', '0.0mm'])
segs.append(['NAME:PLSegment', 'SegmentType:=', 'Line', 'StartIndex:=', 4, 'NoOfPoints:=', 2])
pts.append(['NAME:PLPoint', 'X:=', '0.000000mm', 'Y:=', '0.533000mm', 'Z:=', '0.0mm'])
segs.append(['NAME:PLSegment', 'SegmentType:=', 'Line', 'StartIndex:=', 5, 'NoOfPoints:=', 2])
pts.append(['NAME:PLPoint', 'X:=', '0.000000mm', 'Y:=', '0.523000mm', 'Z:=', '0.0mm'])
segs.append(['NAME:PLSegment', 'SegmentType:=', 'Line', 'StartIndex:=', 6, 'NoOfPoints:=', 2])
pts.append(['NAME:PLPoint', 'X:=', '0.000000mm', 'Y:=', '0.453000mm', 'Z:=', '0.0mm'])
segs.append(['NAME:PLSegment', 'SegmentType:=', 'Line', 'StartIndex:=', 7, 'NoOfPoints:=', 2])
pts.append(['NAME:PLPoint', 'X:=', '-0.010000mm', 'Y:=', '0.453000mm', 'Z:=', '0.0mm'])
oEditor.CreatePolyline(
    ['NAME:PolylineParameters', 'IsPolylineCovered:=', True, 'IsPolylineClosed:=', True, pts, segs],
    [
        'NAME:Attributes',
        'Name:=', 'cl_metal_Q4_5',
        'Flags:=', '',
        'Color:=', '(200 220 255)',
        'Transparency:=', 0.0,
        'PartCoordinateSystem:=', 'Global',
        'UDMId:=', '',
        'MaterialName:=', 'vacuum',
        'SolveInside:=', True
    ]
)
# Element: cl_etcher_Q4_6
pts = ['NAME:PolylinePoints']
segs = ['NAME:PolylineSegments']
pts.append(['NAME:PLPoint', 'X:=', '-0.016000mm', 'Y:=', '0.447000mm', 'Z:=', '0.0mm'])
segs.append(['NAME:PLSegment', 'SegmentType:=', 'Line', 'StartIndex:=', 0, 'NoOfPoints:=', 2])
pts.append(['NAME:PLPoint', 'X:=', '-0.016000mm', 'Y:=', '0.517000mm', 'Z:=', '0.0mm'])
segs.append(['NAME:PLSegment', 'SegmentType:=', 'Line', 'StartIndex:=', 1, 'NoOfPoints:=', 2])
pts.append(['NAME:PLPoint', 'X:=', '-0.026000mm', 'Y:=', '0.517000mm', 'Z:=', '0.0mm'])
segs.append(['NAME:PLSegment', 'SegmentType:=', 'Line', 'StartIndex:=', 2, 'NoOfPoints:=', 2])
pts.append(['NAME:PLPoint', 'X:=', '-0.026000mm', 'Y:=', '0.539000mm', 'Z:=', '0.0mm'])
segs.append(['NAME:PLSegment', 'SegmentType:=', 'Line', 'StartIndex:=', 3, 'NoOfPoints:=', 2])
pts.append(['NAME:PLPoint', 'X:=', '0.006000mm', 'Y:=', '0.539000mm', 'Z:=', '0.0mm'])
segs.append(['NAME:PLSegment', 'SegmentType:=', 'Line', 'StartIndex:=', 4, 'NoOfPoints:=', 2])
pts.append(['NAME:PLPoint', 'X:=', '0.006000mm', 'Y:=', '0.447000mm', 'Z:=', '0.0mm'])
segs.append(['NAME:PLSegment', 'SegmentType:=', 'Line', 'StartIndex:=', 5, 'NoOfPoints:=', 2])
pts.append(['NAME:PLPoint', 'X:=', '-0.016000mm', 'Y:=', '0.447000mm', 'Z:=', '0.0mm'])
oEditor.CreatePolyline(
    ['NAME:PolylineParameters', 'IsPolylineCovered:=', True, 'IsPolylineClosed:=', True, pts, segs],
    [
        'NAME:Attributes',
        'Name:=', 'cl_etcher_Q4_6',
        'Flags:=', '',
        'Color:=', '(255 100 100)',
        'Transparency:=', 0.0,
        'PartCoordinateSystem:=', 'Global',
        'UDMId:=', '',
        'MaterialName:=', 'vacuum',
        'SolveInside:=', True
    ]
)
# Element: pad_top_Q0_7
pts = ['NAME:PolylinePoints']
segs = ['NAME:PolylineSegments']
pts.append(['NAME:PLPoint', 'X:=', '-2.515000mm', 'Y:=', '-0.227500mm', 'Z:=', '0.0mm'])
segs.append(['NAME:PLSegment', 'SegmentType:=', 'Line', 'StartIndex:=', 0, 'NoOfPoints:=', 2])
pts.append(['NAME:PLPoint', 'X:=', '-2.515000mm', 'Y:=', '0.227500mm', 'Z:=', '0.0mm'])
segs.append(['NAME:PLSegment', 'SegmentType:=', 'Line', 'StartIndex:=', 1, 'NoOfPoints:=', 2])
pts.append(['NAME:PLPoint', 'X:=', '-2.605000mm', 'Y:=', '0.227500mm', 'Z:=', '0.0mm'])
segs.append(['NAME:PLSegment', 'SegmentType:=', 'Line', 'StartIndex:=', 2, 'NoOfPoints:=', 2])
pts.append(['NAME:PLPoint', 'X:=', '-2.605000mm', 'Y:=', '-0.227500mm', 'Z:=', '0.0mm'])
segs.append(['NAME:PLSegment', 'SegmentType:=', 'Line', 'StartIndex:=', 3, 'NoOfPoints:=', 2])
pts.append(['NAME:PLPoint', 'X:=', '-2.515000mm', 'Y:=', '-0.227500mm', 'Z:=', '0.0mm'])
oEditor.CreatePolyline(
    ['NAME:PolylineParameters', 'IsPolylineCovered:=', True, 'IsPolylineClosed:=', True, pts, segs],
    [
        'NAME:Attributes',
        'Name:=', 'pad_top_Q0_7',
        'Flags:=', '',
        'Color:=', '(200 220 255)',
        'Transparency:=', 0.0,
        'PartCoordinateSystem:=', 'Global',
        'UDMId:=', '',
        'MaterialName:=', 'vacuum',
        'SolveInside:=', True
    ]
)
# Element: pad_bot_Q0_8
pts = ['NAME:PolylinePoints']
segs = ['NAME:PolylineSegments']
pts.append(['NAME:PLPoint', 'X:=', '-2.395000mm', 'Y:=', '-0.227500mm', 'Z:=', '0.0mm'])
segs.append(['NAME:PLSegment', 'SegmentType:=', 'Line', 'StartIndex:=', 0, 'NoOfPoints:=', 2])
pts.append(['NAME:PLPoint', 'X:=', '-2.395000mm', 'Y:=', '0.227500mm', 'Z:=', '0.0mm'])
segs.append(['NAME:PLSegment', 'SegmentType:=', 'Line', 'StartIndex:=', 1, 'NoOfPoints:=', 2])
pts.append(['NAME:PLPoint', 'X:=', '-2.485000mm', 'Y:=', '0.227500mm', 'Z:=', '0.0mm'])
segs.append(['NAME:PLSegment', 'SegmentType:=', 'Line', 'StartIndex:=', 2, 'NoOfPoints:=', 2])
pts.append(['NAME:PLPoint', 'X:=', '-2.485000mm', 'Y:=', '-0.227500mm', 'Z:=', '0.0mm'])
segs.append(['NAME:PLSegment', 'SegmentType:=', 'Line', 'StartIndex:=', 3, 'NoOfPoints:=', 2])
pts.append(['NAME:PLPoint', 'X:=', '-2.395000mm', 'Y:=', '-0.227500mm', 'Z:=', '0.0mm'])
oEditor.CreatePolyline(
    ['NAME:PolylineParameters', 'IsPolylineCovered:=', True, 'IsPolylineClosed:=', True, pts, segs],
    [
        'NAME:Attributes',
        'Name:=', 'pad_bot_Q0_8',
        'Flags:=', '',
        'Color:=', '(200 220 255)',
        'Transparency:=', 0.0,
        'PartCoordinateSystem:=', 'Global',
        'UDMId:=', '',
        'MaterialName:=', 'vacuum',
        'SolveInside:=', True
    ]
)
# Element: rect_pk_Q0_9
pts = ['NAME:PolylinePoints']
segs = ['NAME:PolylineSegments']
pts.append(['NAME:PLPoint', 'X:=', '-2.175000mm', 'Y:=', '-0.325000mm', 'Z:=', '0.0mm'])
segs.append(['NAME:PLSegment', 'SegmentType:=', 'Line', 'StartIndex:=', 0, 'NoOfPoints:=', 2])
pts.append(['NAME:PLPoint', 'X:=', '-2.175000mm', 'Y:=', '0.325000mm', 'Z:=', '0.0mm'])
segs.append(['NAME:PLSegment', 'SegmentType:=', 'Line', 'StartIndex:=', 1, 'NoOfPoints:=', 2])
pts.append(['NAME:PLPoint', 'X:=', '-2.825000mm', 'Y:=', '0.325000mm', 'Z:=', '0.0mm'])
segs.append(['NAME:PLSegment', 'SegmentType:=', 'Line', 'StartIndex:=', 2, 'NoOfPoints:=', 2])
pts.append(['NAME:PLPoint', 'X:=', '-2.825000mm', 'Y:=', '-0.325000mm', 'Z:=', '0.0mm'])
segs.append(['NAME:PLSegment', 'SegmentType:=', 'Line', 'StartIndex:=', 3, 'NoOfPoints:=', 2])
pts.append(['NAME:PLPoint', 'X:=', '-2.175000mm', 'Y:=', '-0.325000mm', 'Z:=', '0.0mm'])
oEditor.CreatePolyline(
    ['NAME:PolylineParameters', 'IsPolylineCovered:=', True, 'IsPolylineClosed:=', True, pts, segs],
    [
        'NAME:Attributes',
        'Name:=', 'rect_pk_Q0_9',
        'Flags:=', '',
        'Color:=', '(255 100 100)',
        'Transparency:=', 0.0,
        'PartCoordinateSystem:=', 'Global',
        'UDMId:=', '',
        'MaterialName:=', 'vacuum',
        'SolveInside:=', True
    ]
)
# Element: bus_top_connector_pad_Q0_10
pts = ['NAME:PolylinePoints']
segs = ['NAME:PolylineSegments']
pts.append(['NAME:PLPoint', 'X:=', '-2.620000mm', 'Y:=', '0.102500mm', 'Z:=', '0.0mm'])
segs.append(['NAME:PLSegment', 'SegmentType:=', 'Line', 'StartIndex:=', 0, 'NoOfPoints:=', 2])
pts.append(['NAME:PLPoint', 'X:=', '-2.620000mm', 'Y:=', '0.227500mm', 'Z:=', '0.0mm'])
segs.append(['NAME:PLSegment', 'SegmentType:=', 'Line', 'StartIndex:=', 1, 'NoOfPoints:=', 2])
pts.append(['NAME:PLPoint', 'X:=', '-2.650000mm', 'Y:=', '0.227500mm', 'Z:=', '0.0mm'])
segs.append(['NAME:PLSegment', 'SegmentType:=', 'Line', 'StartIndex:=', 2, 'NoOfPoints:=', 2])
pts.append(['NAME:PLPoint', 'X:=', '-2.650000mm', 'Y:=', '0.102500mm', 'Z:=', '0.0mm'])
segs.append(['NAME:PLSegment', 'SegmentType:=', 'Line', 'StartIndex:=', 3, 'NoOfPoints:=', 2])
pts.append(['NAME:PLPoint', 'X:=', '-2.620000mm', 'Y:=', '0.102500mm', 'Z:=', '0.0mm'])
oEditor.CreatePolyline(
    ['NAME:PolylineParameters', 'IsPolylineCovered:=', True, 'IsPolylineClosed:=', True, pts, segs],
    [
        'NAME:Attributes',
        'Name:=', 'bus_top_connector_pad_Q0_10',
        'Flags:=', '',
        'Color:=', '(200 220 255)',
        'Transparency:=', 0.0,
        'PartCoordinateSystem:=', 'Global',
        'UDMId:=', '',
        'MaterialName:=', 'vacuum',
        'SolveInside:=', True
    ]
)
# Element: readout_connector_pad_Q0_11
pts = ['NAME:PolylinePoints']
segs = ['NAME:PolylineSegments']
pts.append(['NAME:PLPoint', 'X:=', '-2.380000mm', 'Y:=', '-0.102500mm', 'Z:=', '0.0mm'])
segs.append(['NAME:PLSegment', 'SegmentType:=', 'Line', 'StartIndex:=', 0, 'NoOfPoints:=', 2])
pts.append(['NAME:PLPoint', 'X:=', '-2.380000mm', 'Y:=', '-0.227500mm', 'Z:=', '0.0mm'])
segs.append(['NAME:PLSegment', 'SegmentType:=', 'Line', 'StartIndex:=', 1, 'NoOfPoints:=', 2])
pts.append(['NAME:PLPoint', 'X:=', '-2.350000mm', 'Y:=', '-0.227500mm', 'Z:=', '0.0mm'])
segs.append(['NAME:PLSegment', 'SegmentType:=', 'Line', 'StartIndex:=', 2, 'NoOfPoints:=', 2])
pts.append(['NAME:PLPoint', 'X:=', '-2.350000mm', 'Y:=', '-0.102500mm', 'Z:=', '0.0mm'])
segs.append(['NAME:PLSegment', 'SegmentType:=', 'Line', 'StartIndex:=', 3, 'NoOfPoints:=', 2])
pts.append(['NAME:PLPoint', 'X:=', '-2.380000mm', 'Y:=', '-0.102500mm', 'Z:=', '0.0mm'])
oEditor.CreatePolyline(
    ['NAME:PolylineParameters', 'IsPolylineCovered:=', True, 'IsPolylineClosed:=', True, pts, segs],
    [
        'NAME:Attributes',
        'Name:=', 'readout_connector_pad_Q0_11',
        'Flags:=', '',
        'Color:=', '(200 220 255)',
        'Transparency:=', 0.0,
        'PartCoordinateSystem:=', 'Global',
        'UDMId:=', '',
        'MaterialName:=', 'vacuum',
        'SolveInside:=', True
    ]
)
# Element: pad_top_Q1_12
pts = ['NAME:PolylinePoints']
segs = ['NAME:PolylineSegments']
pts.append(['NAME:PLPoint', 'X:=', '-2.515000mm', 'Y:=', '1.572500mm', 'Z:=', '0.0mm'])
segs.append(['NAME:PLSegment', 'SegmentType:=', 'Line', 'StartIndex:=', 0, 'NoOfPoints:=', 2])
pts.append(['NAME:PLPoint', 'X:=', '-2.515000mm', 'Y:=', '2.027500mm', 'Z:=', '0.0mm'])
segs.append(['NAME:PLSegment', 'SegmentType:=', 'Line', 'StartIndex:=', 1, 'NoOfPoints:=', 2])
pts.append(['NAME:PLPoint', 'X:=', '-2.605000mm', 'Y:=', '2.027500mm', 'Z:=', '0.0mm'])
segs.append(['NAME:PLSegment', 'SegmentType:=', 'Line', 'StartIndex:=', 2, 'NoOfPoints:=', 2])
pts.append(['NAME:PLPoint', 'X:=', '-2.605000mm', 'Y:=', '1.572500mm', 'Z:=', '0.0mm'])
segs.append(['NAME:PLSegment', 'SegmentType:=', 'Line', 'StartIndex:=', 3, 'NoOfPoints:=', 2])
pts.append(['NAME:PLPoint', 'X:=', '-2.515000mm', 'Y:=', '1.572500mm', 'Z:=', '0.0mm'])
oEditor.CreatePolyline(
    ['NAME:PolylineParameters', 'IsPolylineCovered:=', True, 'IsPolylineClosed:=', True, pts, segs],
    [
        'NAME:Attributes',
        'Name:=', 'pad_top_Q1_12',
        'Flags:=', '',
        'Color:=', '(200 220 255)',
        'Transparency:=', 0.0,
        'PartCoordinateSystem:=', 'Global',
        'UDMId:=', '',
        'MaterialName:=', 'vacuum',
        'SolveInside:=', True
    ]
)
# Element: pad_bot_Q1_13
pts = ['NAME:PolylinePoints']
segs = ['NAME:PolylineSegments']
pts.append(['NAME:PLPoint', 'X:=', '-2.395000mm', 'Y:=', '1.572500mm', 'Z:=', '0.0mm'])
segs.append(['NAME:PLSegment', 'SegmentType:=', 'Line', 'StartIndex:=', 0, 'NoOfPoints:=', 2])
pts.append(['NAME:PLPoint', 'X:=', '-2.395000mm', 'Y:=', '2.027500mm', 'Z:=', '0.0mm'])
segs.append(['NAME:PLSegment', 'SegmentType:=', 'Line', 'StartIndex:=', 1, 'NoOfPoints:=', 2])
pts.append(['NAME:PLPoint', 'X:=', '-2.485000mm', 'Y:=', '2.027500mm', 'Z:=', '0.0mm'])
segs.append(['NAME:PLSegment', 'SegmentType:=', 'Line', 'StartIndex:=', 2, 'NoOfPoints:=', 2])
pts.append(['NAME:PLPoint', 'X:=', '-2.485000mm', 'Y:=', '1.572500mm', 'Z:=', '0.0mm'])
segs.append(['NAME:PLSegment', 'SegmentType:=', 'Line', 'StartIndex:=', 3, 'NoOfPoints:=', 2])
pts.append(['NAME:PLPoint', 'X:=', '-2.395000mm', 'Y:=', '1.572500mm', 'Z:=', '0.0mm'])
oEditor.CreatePolyline(
    ['NAME:PolylineParameters', 'IsPolylineCovered:=', True, 'IsPolylineClosed:=', True, pts, segs],
    [
        'NAME:Attributes',
        'Name:=', 'pad_bot_Q1_13',
        'Flags:=', '',
        'Color:=', '(200 220 255)',
        'Transparency:=', 0.0,
        'PartCoordinateSystem:=', 'Global',
        'UDMId:=', '',
        'MaterialName:=', 'vacuum',
        'SolveInside:=', True
    ]
)
# Element: rect_pk_Q1_14
pts = ['NAME:PolylinePoints']
segs = ['NAME:PolylineSegments']
pts.append(['NAME:PLPoint', 'X:=', '-2.175000mm', 'Y:=', '1.475000mm', 'Z:=', '0.0mm'])
segs.append(['NAME:PLSegment', 'SegmentType:=', 'Line', 'StartIndex:=', 0, 'NoOfPoints:=', 2])
pts.append(['NAME:PLPoint', 'X:=', '-2.175000mm', 'Y:=', '2.125000mm', 'Z:=', '0.0mm'])
segs.append(['NAME:PLSegment', 'SegmentType:=', 'Line', 'StartIndex:=', 1, 'NoOfPoints:=', 2])
pts.append(['NAME:PLPoint', 'X:=', '-2.825000mm', 'Y:=', '2.125000mm', 'Z:=', '0.0mm'])
segs.append(['NAME:PLSegment', 'SegmentType:=', 'Line', 'StartIndex:=', 2, 'NoOfPoints:=', 2])
pts.append(['NAME:PLPoint', 'X:=', '-2.825000mm', 'Y:=', '1.475000mm', 'Z:=', '0.0mm'])
segs.append(['NAME:PLSegment', 'SegmentType:=', 'Line', 'StartIndex:=', 3, 'NoOfPoints:=', 2])
pts.append(['NAME:PLPoint', 'X:=', '-2.175000mm', 'Y:=', '1.475000mm', 'Z:=', '0.0mm'])
oEditor.CreatePolyline(
    ['NAME:PolylineParameters', 'IsPolylineCovered:=', True, 'IsPolylineClosed:=', True, pts, segs],
    [
        'NAME:Attributes',
        'Name:=', 'rect_pk_Q1_14',
        'Flags:=', '',
        'Color:=', '(255 100 100)',
        'Transparency:=', 0.0,
        'PartCoordinateSystem:=', 'Global',
        'UDMId:=', '',
        'MaterialName:=', 'vacuum',
        'SolveInside:=', True
    ]
)
# Element: bus_bot_connector_pad_Q1_15
pts = ['NAME:PolylinePoints']
segs = ['NAME:PolylineSegments']
pts.append(['NAME:PLPoint', 'X:=', '-2.380000mm', 'Y:=', '1.902500mm', 'Z:=', '0.0mm'])
segs.append(['NAME:PLSegment', 'SegmentType:=', 'Line', 'StartIndex:=', 0, 'NoOfPoints:=', 2])
pts.append(['NAME:PLPoint', 'X:=', '-2.380000mm', 'Y:=', '2.027500mm', 'Z:=', '0.0mm'])
segs.append(['NAME:PLSegment', 'SegmentType:=', 'Line', 'StartIndex:=', 1, 'NoOfPoints:=', 2])
pts.append(['NAME:PLPoint', 'X:=', '-2.350000mm', 'Y:=', '2.027500mm', 'Z:=', '0.0mm'])
segs.append(['NAME:PLSegment', 'SegmentType:=', 'Line', 'StartIndex:=', 2, 'NoOfPoints:=', 2])
pts.append(['NAME:PLPoint', 'X:=', '-2.350000mm', 'Y:=', '1.902500mm', 'Z:=', '0.0mm'])
segs.append(['NAME:PLSegment', 'SegmentType:=', 'Line', 'StartIndex:=', 3, 'NoOfPoints:=', 2])
pts.append(['NAME:PLPoint', 'X:=', '-2.380000mm', 'Y:=', '1.902500mm', 'Z:=', '0.0mm'])
oEditor.CreatePolyline(
    ['NAME:PolylineParameters', 'IsPolylineCovered:=', True, 'IsPolylineClosed:=', True, pts, segs],
    [
        'NAME:Attributes',
        'Name:=', 'bus_bot_connector_pad_Q1_15',
        'Flags:=', '',
        'Color:=', '(200 220 255)',
        'Transparency:=', 0.0,
        'PartCoordinateSystem:=', 'Global',
        'UDMId:=', '',
        'MaterialName:=', 'vacuum',
        'SolveInside:=', True
    ]
)
# Element: bus_right_connector_pad_Q1_16
pts = ['NAME:PolylinePoints']
segs = ['NAME:PolylineSegments']
pts.append(['NAME:PLPoint', 'X:=', '-2.380000mm', 'Y:=', '1.697500mm', 'Z:=', '0.0mm'])
segs.append(['NAME:PLSegment', 'SegmentType:=', 'Line', 'StartIndex:=', 0, 'NoOfPoints:=', 2])
pts.append(['NAME:PLPoint', 'X:=', '-2.380000mm', 'Y:=', '1.572500mm', 'Z:=', '0.0mm'])
segs.append(['NAME:PLSegment', 'SegmentType:=', 'Line', 'StartIndex:=', 1, 'NoOfPoints:=', 2])
pts.append(['NAME:PLPoint', 'X:=', '-2.350000mm', 'Y:=', '1.572500mm', 'Z:=', '0.0mm'])
segs.append(['NAME:PLSegment', 'SegmentType:=', 'Line', 'StartIndex:=', 2, 'NoOfPoints:=', 2])
pts.append(['NAME:PLPoint', 'X:=', '-2.350000mm', 'Y:=', '1.697500mm', 'Z:=', '0.0mm'])
segs.append(['NAME:PLSegment', 'SegmentType:=', 'Line', 'StartIndex:=', 3, 'NoOfPoints:=', 2])
pts.append(['NAME:PLPoint', 'X:=', '-2.380000mm', 'Y:=', '1.697500mm', 'Z:=', '0.0mm'])
oEditor.CreatePolyline(
    ['NAME:PolylineParameters', 'IsPolylineCovered:=', True, 'IsPolylineClosed:=', True, pts, segs],
    [
        'NAME:Attributes',
        'Name:=', 'bus_right_connector_pad_Q1_16',
        'Flags:=', '',
        'Color:=', '(200 220 255)',
        'Transparency:=', 0.0,
        'PartCoordinateSystem:=', 'Global',
        'UDMId:=', '',
        'MaterialName:=', 'vacuum',
        'SolveInside:=', True
    ]
)
# Element: readout_connector_pad_Q1_17
pts = ['NAME:PolylinePoints']
segs = ['NAME:PolylineSegments']
pts.append(['NAME:PLPoint', 'X:=', '-2.620000mm', 'Y:=', '1.902500mm', 'Z:=', '0.0mm'])
segs.append(['NAME:PLSegment', 'SegmentType:=', 'Line', 'StartIndex:=', 0, 'NoOfPoints:=', 2])
pts.append(['NAME:PLPoint', 'X:=', '-2.620000mm', 'Y:=', '2.027500mm', 'Z:=', '0.0mm'])
segs.append(['NAME:PLSegment', 'SegmentType:=', 'Line', 'StartIndex:=', 1, 'NoOfPoints:=', 2])
pts.append(['NAME:PLPoint', 'X:=', '-2.650000mm', 'Y:=', '2.027500mm', 'Z:=', '0.0mm'])
segs.append(['NAME:PLSegment', 'SegmentType:=', 'Line', 'StartIndex:=', 2, 'NoOfPoints:=', 2])
pts.append(['NAME:PLPoint', 'X:=', '-2.650000mm', 'Y:=', '1.902500mm', 'Z:=', '0.0mm'])
segs.append(['NAME:PLSegment', 'SegmentType:=', 'Line', 'StartIndex:=', 3, 'NoOfPoints:=', 2])
pts.append(['NAME:PLPoint', 'X:=', '-2.620000mm', 'Y:=', '1.902500mm', 'Z:=', '0.0mm'])
oEditor.CreatePolyline(
    ['NAME:PolylineParameters', 'IsPolylineCovered:=', True, 'IsPolylineClosed:=', True, pts, segs],
    [
        'NAME:Attributes',
        'Name:=', 'readout_connector_pad_Q1_17',
        'Flags:=', '',
        'Color:=', '(200 220 255)',
        'Transparency:=', 0.0,
        'PartCoordinateSystem:=', 'Global',
        'UDMId:=', '',
        'MaterialName:=', 'vacuum',
        'SolveInside:=', True
    ]
)
# Element: pad_top_Q3_18
pts = ['NAME:PolylinePoints']
segs = ['NAME:PolylineSegments']
pts.append(['NAME:PLPoint', 'X:=', '-1.577500mm', 'Y:=', '0.885000mm', 'Z:=', '0.0mm'])
segs.append(['NAME:PLSegment', 'SegmentType:=', 'Line', 'StartIndex:=', 0, 'NoOfPoints:=', 2])
pts.append(['NAME:PLPoint', 'X:=', '-1.122500mm', 'Y:=', '0.885000mm', 'Z:=', '0.0mm'])
segs.append(['NAME:PLSegment', 'SegmentType:=', 'Line', 'StartIndex:=', 1, 'NoOfPoints:=', 2])
pts.append(['NAME:PLPoint', 'X:=', '-1.122500mm', 'Y:=', '0.975000mm', 'Z:=', '0.0mm'])
segs.append(['NAME:PLSegment', 'SegmentType:=', 'Line', 'StartIndex:=', 2, 'NoOfPoints:=', 2])
pts.append(['NAME:PLPoint', 'X:=', '-1.577500mm', 'Y:=', '0.975000mm', 'Z:=', '0.0mm'])
segs.append(['NAME:PLSegment', 'SegmentType:=', 'Line', 'StartIndex:=', 3, 'NoOfPoints:=', 2])
pts.append(['NAME:PLPoint', 'X:=', '-1.577500mm', 'Y:=', '0.885000mm', 'Z:=', '0.0mm'])
oEditor.CreatePolyline(
    ['NAME:PolylineParameters', 'IsPolylineCovered:=', True, 'IsPolylineClosed:=', True, pts, segs],
    [
        'NAME:Attributes',
        'Name:=', 'pad_top_Q3_18',
        'Flags:=', '',
        'Color:=', '(200 220 255)',
        'Transparency:=', 0.0,
        'PartCoordinateSystem:=', 'Global',
        'UDMId:=', '',
        'MaterialName:=', 'vacuum',
        'SolveInside:=', True
    ]
)
# Element: pad_bot_Q3_19
pts = ['NAME:PolylinePoints']
segs = ['NAME:PolylineSegments']
pts.append(['NAME:PLPoint', 'X:=', '-1.577500mm', 'Y:=', '0.765000mm', 'Z:=', '0.0mm'])
segs.append(['NAME:PLSegment', 'SegmentType:=', 'Line', 'StartIndex:=', 0, 'NoOfPoints:=', 2])
pts.append(['NAME:PLPoint', 'X:=', '-1.122500mm', 'Y:=', '0.765000mm', 'Z:=', '0.0mm'])
segs.append(['NAME:PLSegment', 'SegmentType:=', 'Line', 'StartIndex:=', 1, 'NoOfPoints:=', 2])
pts.append(['NAME:PLPoint', 'X:=', '-1.122500mm', 'Y:=', '0.855000mm', 'Z:=', '0.0mm'])
segs.append(['NAME:PLSegment', 'SegmentType:=', 'Line', 'StartIndex:=', 2, 'NoOfPoints:=', 2])
pts.append(['NAME:PLPoint', 'X:=', '-1.577500mm', 'Y:=', '0.855000mm', 'Z:=', '0.0mm'])
segs.append(['NAME:PLSegment', 'SegmentType:=', 'Line', 'StartIndex:=', 3, 'NoOfPoints:=', 2])
pts.append(['NAME:PLPoint', 'X:=', '-1.577500mm', 'Y:=', '0.765000mm', 'Z:=', '0.0mm'])
oEditor.CreatePolyline(
    ['NAME:PolylineParameters', 'IsPolylineCovered:=', True, 'IsPolylineClosed:=', True, pts, segs],
    [
        'NAME:Attributes',
        'Name:=', 'pad_bot_Q3_19',
        'Flags:=', '',
        'Color:=', '(200 220 255)',
        'Transparency:=', 0.0,
        'PartCoordinateSystem:=', 'Global',
        'UDMId:=', '',
        'MaterialName:=', 'vacuum',
        'SolveInside:=', True
    ]
)
# Element: rect_pk_Q3_20
pts = ['NAME:PolylinePoints']
segs = ['NAME:PolylineSegments']
pts.append(['NAME:PLPoint', 'X:=', '-1.675000mm', 'Y:=', '0.545000mm', 'Z:=', '0.0mm'])
segs.append(['NAME:PLSegment', 'SegmentType:=', 'Line', 'StartIndex:=', 0, 'NoOfPoints:=', 2])
pts.append(['NAME:PLPoint', 'X:=', '-1.025000mm', 'Y:=', '0.545000mm', 'Z:=', '0.0mm'])
segs.append(['NAME:PLSegment', 'SegmentType:=', 'Line', 'StartIndex:=', 1, 'NoOfPoints:=', 2])
pts.append(['NAME:PLPoint', 'X:=', '-1.025000mm', 'Y:=', '1.195000mm', 'Z:=', '0.0mm'])
segs.append(['NAME:PLSegment', 'SegmentType:=', 'Line', 'StartIndex:=', 2, 'NoOfPoints:=', 2])
pts.append(['NAME:PLPoint', 'X:=', '-1.675000mm', 'Y:=', '1.195000mm', 'Z:=', '0.0mm'])
segs.append(['NAME:PLSegment', 'SegmentType:=', 'Line', 'StartIndex:=', 3, 'NoOfPoints:=', 2])
pts.append(['NAME:PLPoint', 'X:=', '-1.675000mm', 'Y:=', '0.545000mm', 'Z:=', '0.0mm'])
oEditor.CreatePolyline(
    ['NAME:PolylineParameters', 'IsPolylineCovered:=', True, 'IsPolylineClosed:=', True, pts, segs],
    [
        'NAME:Attributes',
        'Name:=', 'rect_pk_Q3_20',
        'Flags:=', '',
        'Color:=', '(255 100 100)',
        'Transparency:=', 0.0,
        'PartCoordinateSystem:=', 'Global',
        'UDMId:=', '',
        'MaterialName:=', 'vacuum',
        'SolveInside:=', True
    ]
)
# Element: bus_left_connector_pad_Q3_21
pts = ['NAME:PolylinePoints']
segs = ['NAME:PolylineSegments']
pts.append(['NAME:PLPoint', 'X:=', '-1.452500mm', 'Y:=', '0.990000mm', 'Z:=', '0.0mm'])
segs.append(['NAME:PLSegment', 'SegmentType:=', 'Line', 'StartIndex:=', 0, 'NoOfPoints:=', 2])
pts.append(['NAME:PLPoint', 'X:=', '-1.577500mm', 'Y:=', '0.990000mm', 'Z:=', '0.0mm'])
segs.append(['NAME:PLSegment', 'SegmentType:=', 'Line', 'StartIndex:=', 1, 'NoOfPoints:=', 2])
pts.append(['NAME:PLPoint', 'X:=', '-1.577500mm', 'Y:=', '1.020000mm', 'Z:=', '0.0mm'])
segs.append(['NAME:PLSegment', 'SegmentType:=', 'Line', 'StartIndex:=', 2, 'NoOfPoints:=', 2])
pts.append(['NAME:PLPoint', 'X:=', '-1.452500mm', 'Y:=', '1.020000mm', 'Z:=', '0.0mm'])
segs.append(['NAME:PLSegment', 'SegmentType:=', 'Line', 'StartIndex:=', 3, 'NoOfPoints:=', 2])
pts.append(['NAME:PLPoint', 'X:=', '-1.452500mm', 'Y:=', '0.990000mm', 'Z:=', '0.0mm'])
oEditor.CreatePolyline(
    ['NAME:PolylineParameters', 'IsPolylineCovered:=', True, 'IsPolylineClosed:=', True, pts, segs],
    [
        'NAME:Attributes',
        'Name:=', 'bus_left_connector_pad_Q3_21',
        'Flags:=', '',
        'Color:=', '(200 220 255)',
        'Transparency:=', 0.0,
        'PartCoordinateSystem:=', 'Global',
        'UDMId:=', '',
        'MaterialName:=', 'vacuum',
        'SolveInside:=', True
    ]
)
# Element: bus_right_connector_pad_Q3_22
pts = ['NAME:PolylinePoints']
segs = ['NAME:PolylineSegments']
pts.append(['NAME:PLPoint', 'X:=', '-1.247500mm', 'Y:=', '0.750000mm', 'Z:=', '0.0mm'])
segs.append(['NAME:PLSegment', 'SegmentType:=', 'Line', 'StartIndex:=', 0, 'NoOfPoints:=', 2])
pts.append(['NAME:PLPoint', 'X:=', '-1.122500mm', 'Y:=', '0.750000mm', 'Z:=', '0.0mm'])
segs.append(['NAME:PLSegment', 'SegmentType:=', 'Line', 'StartIndex:=', 1, 'NoOfPoints:=', 2])
pts.append(['NAME:PLPoint', 'X:=', '-1.122500mm', 'Y:=', '0.720000mm', 'Z:=', '0.0mm'])
segs.append(['NAME:PLSegment', 'SegmentType:=', 'Line', 'StartIndex:=', 2, 'NoOfPoints:=', 2])
pts.append(['NAME:PLPoint', 'X:=', '-1.247500mm', 'Y:=', '0.720000mm', 'Z:=', '0.0mm'])
segs.append(['NAME:PLSegment', 'SegmentType:=', 'Line', 'StartIndex:=', 3, 'NoOfPoints:=', 2])
pts.append(['NAME:PLPoint', 'X:=', '-1.247500mm', 'Y:=', '0.750000mm', 'Z:=', '0.0mm'])
oEditor.CreatePolyline(
    ['NAME:PolylineParameters', 'IsPolylineCovered:=', True, 'IsPolylineClosed:=', True, pts, segs],
    [
        'NAME:Attributes',
        'Name:=', 'bus_right_connector_pad_Q3_22',
        'Flags:=', '',
        'Color:=', '(200 220 255)',
        'Transparency:=', 0.0,
        'PartCoordinateSystem:=', 'Global',
        'UDMId:=', '',
        'MaterialName:=', 'vacuum',
        'SolveInside:=', True
    ]
)
# Element: readout_connector_pad_Q3_23
pts = ['NAME:PolylinePoints']
segs = ['NAME:PolylineSegments']
pts.append(['NAME:PLPoint', 'X:=', '-1.247500mm', 'Y:=', '0.990000mm', 'Z:=', '0.0mm'])
segs.append(['NAME:PLSegment', 'SegmentType:=', 'Line', 'StartIndex:=', 0, 'NoOfPoints:=', 2])
pts.append(['NAME:PLPoint', 'X:=', '-1.122500mm', 'Y:=', '0.990000mm', 'Z:=', '0.0mm'])
segs.append(['NAME:PLSegment', 'SegmentType:=', 'Line', 'StartIndex:=', 1, 'NoOfPoints:=', 2])
pts.append(['NAME:PLPoint', 'X:=', '-1.122500mm', 'Y:=', '1.020000mm', 'Z:=', '0.0mm'])
segs.append(['NAME:PLSegment', 'SegmentType:=', 'Line', 'StartIndex:=', 2, 'NoOfPoints:=', 2])
pts.append(['NAME:PLPoint', 'X:=', '-1.247500mm', 'Y:=', '1.020000mm', 'Z:=', '0.0mm'])
segs.append(['NAME:PLSegment', 'SegmentType:=', 'Line', 'StartIndex:=', 3, 'NoOfPoints:=', 2])
pts.append(['NAME:PLPoint', 'X:=', '-1.247500mm', 'Y:=', '0.990000mm', 'Z:=', '0.0mm'])
oEditor.CreatePolyline(
    ['NAME:PolylineParameters', 'IsPolylineCovered:=', True, 'IsPolylineClosed:=', True, pts, segs],
    [
        'NAME:Attributes',
        'Name:=', 'readout_connector_pad_Q3_23',
        'Flags:=', '',
        'Color:=', '(200 220 255)',
        'Transparency:=', 0.0,
        'PartCoordinateSystem:=', 'Global',
        'UDMId:=', '',
        'MaterialName:=', 'vacuum',
        'SolveInside:=', True
    ]
)
# Element: pad_top_Q5_24
pts = ['NAME:PolylinePoints']
segs = ['NAME:PolylineSegments']
pts.append(['NAME:PLPoint', 'X:=', '1.122500mm', 'Y:=', '0.885000mm', 'Z:=', '0.0mm'])
segs.append(['NAME:PLSegment', 'SegmentType:=', 'Line', 'StartIndex:=', 0, 'NoOfPoints:=', 2])
pts.append(['NAME:PLPoint', 'X:=', '1.577500mm', 'Y:=', '0.885000mm', 'Z:=', '0.0mm'])
segs.append(['NAME:PLSegment', 'SegmentType:=', 'Line', 'StartIndex:=', 1, 'NoOfPoints:=', 2])
pts.append(['NAME:PLPoint', 'X:=', '1.577500mm', 'Y:=', '0.975000mm', 'Z:=', '0.0mm'])
segs.append(['NAME:PLSegment', 'SegmentType:=', 'Line', 'StartIndex:=', 2, 'NoOfPoints:=', 2])
pts.append(['NAME:PLPoint', 'X:=', '1.122500mm', 'Y:=', '0.975000mm', 'Z:=', '0.0mm'])
segs.append(['NAME:PLSegment', 'SegmentType:=', 'Line', 'StartIndex:=', 3, 'NoOfPoints:=', 2])
pts.append(['NAME:PLPoint', 'X:=', '1.122500mm', 'Y:=', '0.885000mm', 'Z:=', '0.0mm'])
oEditor.CreatePolyline(
    ['NAME:PolylineParameters', 'IsPolylineCovered:=', True, 'IsPolylineClosed:=', True, pts, segs],
    [
        'NAME:Attributes',
        'Name:=', 'pad_top_Q5_24',
        'Flags:=', '',
        'Color:=', '(200 220 255)',
        'Transparency:=', 0.0,
        'PartCoordinateSystem:=', 'Global',
        'UDMId:=', '',
        'MaterialName:=', 'vacuum',
        'SolveInside:=', True
    ]
)
# Element: pad_bot_Q5_25
pts = ['NAME:PolylinePoints']
segs = ['NAME:PolylineSegments']
pts.append(['NAME:PLPoint', 'X:=', '1.122500mm', 'Y:=', '0.765000mm', 'Z:=', '0.0mm'])
segs.append(['NAME:PLSegment', 'SegmentType:=', 'Line', 'StartIndex:=', 0, 'NoOfPoints:=', 2])
pts.append(['NAME:PLPoint', 'X:=', '1.577500mm', 'Y:=', '0.765000mm', 'Z:=', '0.0mm'])
segs.append(['NAME:PLSegment', 'SegmentType:=', 'Line', 'StartIndex:=', 1, 'NoOfPoints:=', 2])
pts.append(['NAME:PLPoint', 'X:=', '1.577500mm', 'Y:=', '0.855000mm', 'Z:=', '0.0mm'])
segs.append(['NAME:PLSegment', 'SegmentType:=', 'Line', 'StartIndex:=', 2, 'NoOfPoints:=', 2])
pts.append(['NAME:PLPoint', 'X:=', '1.122500mm', 'Y:=', '0.855000mm', 'Z:=', '0.0mm'])
segs.append(['NAME:PLSegment', 'SegmentType:=', 'Line', 'StartIndex:=', 3, 'NoOfPoints:=', 2])
pts.append(['NAME:PLPoint', 'X:=', '1.122500mm', 'Y:=', '0.765000mm', 'Z:=', '0.0mm'])
oEditor.CreatePolyline(
    ['NAME:PolylineParameters', 'IsPolylineCovered:=', True, 'IsPolylineClosed:=', True, pts, segs],
    [
        'NAME:Attributes',
        'Name:=', 'pad_bot_Q5_25',
        'Flags:=', '',
        'Color:=', '(200 220 255)',
        'Transparency:=', 0.0,
        'PartCoordinateSystem:=', 'Global',
        'UDMId:=', '',
        'MaterialName:=', 'vacuum',
        'SolveInside:=', True
    ]
)
# Element: rect_pk_Q5_26
pts = ['NAME:PolylinePoints']
segs = ['NAME:PolylineSegments']
pts.append(['NAME:PLPoint', 'X:=', '1.025000mm', 'Y:=', '0.545000mm', 'Z:=', '0.0mm'])
segs.append(['NAME:PLSegment', 'SegmentType:=', 'Line', 'StartIndex:=', 0, 'NoOfPoints:=', 2])
pts.append(['NAME:PLPoint', 'X:=', '1.675000mm', 'Y:=', '0.545000mm', 'Z:=', '0.0mm'])
segs.append(['NAME:PLSegment', 'SegmentType:=', 'Line', 'StartIndex:=', 1, 'NoOfPoints:=', 2])
pts.append(['NAME:PLPoint', 'X:=', '1.675000mm', 'Y:=', '1.195000mm', 'Z:=', '0.0mm'])
segs.append(['NAME:PLSegment', 'SegmentType:=', 'Line', 'StartIndex:=', 2, 'NoOfPoints:=', 2])
pts.append(['NAME:PLPoint', 'X:=', '1.025000mm', 'Y:=', '1.195000mm', 'Z:=', '0.0mm'])
segs.append(['NAME:PLSegment', 'SegmentType:=', 'Line', 'StartIndex:=', 3, 'NoOfPoints:=', 2])
pts.append(['NAME:PLPoint', 'X:=', '1.025000mm', 'Y:=', '0.545000mm', 'Z:=', '0.0mm'])
oEditor.CreatePolyline(
    ['NAME:PolylineParameters', 'IsPolylineCovered:=', True, 'IsPolylineClosed:=', True, pts, segs],
    [
        'NAME:Attributes',
        'Name:=', 'rect_pk_Q5_26',
        'Flags:=', '',
        'Color:=', '(255 100 100)',
        'Transparency:=', 0.0,
        'PartCoordinateSystem:=', 'Global',
        'UDMId:=', '',
        'MaterialName:=', 'vacuum',
        'SolveInside:=', True
    ]
)
# Element: bus_left_connector_pad_Q5_27
pts = ['NAME:PolylinePoints']
segs = ['NAME:PolylineSegments']
pts.append(['NAME:PLPoint', 'X:=', '1.247500mm', 'Y:=', '0.750000mm', 'Z:=', '0.0mm'])
segs.append(['NAME:PLSegment', 'SegmentType:=', 'Line', 'StartIndex:=', 0, 'NoOfPoints:=', 2])
pts.append(['NAME:PLPoint', 'X:=', '1.122500mm', 'Y:=', '0.750000mm', 'Z:=', '0.0mm'])
segs.append(['NAME:PLSegment', 'SegmentType:=', 'Line', 'StartIndex:=', 1, 'NoOfPoints:=', 2])
pts.append(['NAME:PLPoint', 'X:=', '1.122500mm', 'Y:=', '0.720000mm', 'Z:=', '0.0mm'])
segs.append(['NAME:PLSegment', 'SegmentType:=', 'Line', 'StartIndex:=', 2, 'NoOfPoints:=', 2])
pts.append(['NAME:PLPoint', 'X:=', '1.247500mm', 'Y:=', '0.720000mm', 'Z:=', '0.0mm'])
segs.append(['NAME:PLSegment', 'SegmentType:=', 'Line', 'StartIndex:=', 3, 'NoOfPoints:=', 2])
pts.append(['NAME:PLPoint', 'X:=', '1.247500mm', 'Y:=', '0.750000mm', 'Z:=', '0.0mm'])
oEditor.CreatePolyline(
    ['NAME:PolylineParameters', 'IsPolylineCovered:=', True, 'IsPolylineClosed:=', True, pts, segs],
    [
        'NAME:Attributes',
        'Name:=', 'bus_left_connector_pad_Q5_27',
        'Flags:=', '',
        'Color:=', '(200 220 255)',
        'Transparency:=', 0.0,
        'PartCoordinateSystem:=', 'Global',
        'UDMId:=', '',
        'MaterialName:=', 'vacuum',
        'SolveInside:=', True
    ]
)
# Element: bus_right_connector_pad_Q5_28
pts = ['NAME:PolylinePoints']
segs = ['NAME:PolylineSegments']
pts.append(['NAME:PLPoint', 'X:=', '1.452500mm', 'Y:=', '0.990000mm', 'Z:=', '0.0mm'])
segs.append(['NAME:PLSegment', 'SegmentType:=', 'Line', 'StartIndex:=', 0, 'NoOfPoints:=', 2])
pts.append(['NAME:PLPoint', 'X:=', '1.577500mm', 'Y:=', '0.990000mm', 'Z:=', '0.0mm'])
segs.append(['NAME:PLSegment', 'SegmentType:=', 'Line', 'StartIndex:=', 1, 'NoOfPoints:=', 2])
pts.append(['NAME:PLPoint', 'X:=', '1.577500mm', 'Y:=', '1.020000mm', 'Z:=', '0.0mm'])
segs.append(['NAME:PLSegment', 'SegmentType:=', 'Line', 'StartIndex:=', 2, 'NoOfPoints:=', 2])
pts.append(['NAME:PLPoint', 'X:=', '1.452500mm', 'Y:=', '1.020000mm', 'Z:=', '0.0mm'])
segs.append(['NAME:PLSegment', 'SegmentType:=', 'Line', 'StartIndex:=', 3, 'NoOfPoints:=', 2])
pts.append(['NAME:PLPoint', 'X:=', '1.452500mm', 'Y:=', '0.990000mm', 'Z:=', '0.0mm'])
oEditor.CreatePolyline(
    ['NAME:PolylineParameters', 'IsPolylineCovered:=', True, 'IsPolylineClosed:=', True, pts, segs],
    [
        'NAME:Attributes',
        'Name:=', 'bus_right_connector_pad_Q5_28',
        'Flags:=', '',
        'Color:=', '(200 220 255)',
        'Transparency:=', 0.0,
        'PartCoordinateSystem:=', 'Global',
        'UDMId:=', '',
        'MaterialName:=', 'vacuum',
        'SolveInside:=', True
    ]
)
# Element: readout_connector_pad_Q5_29
pts = ['NAME:PolylinePoints']
segs = ['NAME:PolylineSegments']
pts.append(['NAME:PLPoint', 'X:=', '1.247500mm', 'Y:=', '0.990000mm', 'Z:=', '0.0mm'])
segs.append(['NAME:PLSegment', 'SegmentType:=', 'Line', 'StartIndex:=', 0, 'NoOfPoints:=', 2])
pts.append(['NAME:PLPoint', 'X:=', '1.122500mm', 'Y:=', '0.990000mm', 'Z:=', '0.0mm'])
segs.append(['NAME:PLSegment', 'SegmentType:=', 'Line', 'StartIndex:=', 1, 'NoOfPoints:=', 2])
pts.append(['NAME:PLPoint', 'X:=', '1.122500mm', 'Y:=', '1.020000mm', 'Z:=', '0.0mm'])
segs.append(['NAME:PLSegment', 'SegmentType:=', 'Line', 'StartIndex:=', 2, 'NoOfPoints:=', 2])
pts.append(['NAME:PLPoint', 'X:=', '1.247500mm', 'Y:=', '1.020000mm', 'Z:=', '0.0mm'])
segs.append(['NAME:PLSegment', 'SegmentType:=', 'Line', 'StartIndex:=', 3, 'NoOfPoints:=', 2])
pts.append(['NAME:PLPoint', 'X:=', '1.247500mm', 'Y:=', '0.990000mm', 'Z:=', '0.0mm'])
oEditor.CreatePolyline(
    ['NAME:PolylineParameters', 'IsPolylineCovered:=', True, 'IsPolylineClosed:=', True, pts, segs],
    [
        'NAME:Attributes',
        'Name:=', 'readout_connector_pad_Q5_29',
        'Flags:=', '',
        'Color:=', '(200 220 255)',
        'Transparency:=', 0.0,
        'PartCoordinateSystem:=', 'Global',
        'UDMId:=', '',
        'MaterialName:=', 'vacuum',
        'SolveInside:=', True
    ]
)
# Element: pad_top_Q2_30
pts = ['NAME:PolylinePoints']
segs = ['NAME:PolylineSegments']
pts.append(['NAME:PLPoint', 'X:=', '2.485000mm', 'Y:=', '1.572500mm', 'Z:=', '0.0mm'])
segs.append(['NAME:PLSegment', 'SegmentType:=', 'Line', 'StartIndex:=', 0, 'NoOfPoints:=', 2])
pts.append(['NAME:PLPoint', 'X:=', '2.485000mm', 'Y:=', '2.027500mm', 'Z:=', '0.0mm'])
segs.append(['NAME:PLSegment', 'SegmentType:=', 'Line', 'StartIndex:=', 1, 'NoOfPoints:=', 2])
pts.append(['NAME:PLPoint', 'X:=', '2.395000mm', 'Y:=', '2.027500mm', 'Z:=', '0.0mm'])
segs.append(['NAME:PLSegment', 'SegmentType:=', 'Line', 'StartIndex:=', 2, 'NoOfPoints:=', 2])
pts.append(['NAME:PLPoint', 'X:=', '2.395000mm', 'Y:=', '1.572500mm', 'Z:=', '0.0mm'])
segs.append(['NAME:PLSegment', 'SegmentType:=', 'Line', 'StartIndex:=', 3, 'NoOfPoints:=', 2])
pts.append(['NAME:PLPoint', 'X:=', '2.485000mm', 'Y:=', '1.572500mm', 'Z:=', '0.0mm'])
oEditor.CreatePolyline(
    ['NAME:PolylineParameters', 'IsPolylineCovered:=', True, 'IsPolylineClosed:=', True, pts, segs],
    [
        'NAME:Attributes',
        'Name:=', 'pad_top_Q2_30',
        'Flags:=', '',
        'Color:=', '(200 220 255)',
        'Transparency:=', 0.0,
        'PartCoordinateSystem:=', 'Global',
        'UDMId:=', '',
        'MaterialName:=', 'vacuum',
        'SolveInside:=', True
    ]
)
# Element: pad_bot_Q2_31
pts = ['NAME:PolylinePoints']
segs = ['NAME:PolylineSegments']
pts.append(['NAME:PLPoint', 'X:=', '2.605000mm', 'Y:=', '1.572500mm', 'Z:=', '0.0mm'])
segs.append(['NAME:PLSegment', 'SegmentType:=', 'Line', 'StartIndex:=', 0, 'NoOfPoints:=', 2])
pts.append(['NAME:PLPoint', 'X:=', '2.605000mm', 'Y:=', '2.027500mm', 'Z:=', '0.0mm'])
segs.append(['NAME:PLSegment', 'SegmentType:=', 'Line', 'StartIndex:=', 1, 'NoOfPoints:=', 2])
pts.append(['NAME:PLPoint', 'X:=', '2.515000mm', 'Y:=', '2.027500mm', 'Z:=', '0.0mm'])
segs.append(['NAME:PLSegment', 'SegmentType:=', 'Line', 'StartIndex:=', 2, 'NoOfPoints:=', 2])
pts.append(['NAME:PLPoint', 'X:=', '2.515000mm', 'Y:=', '1.572500mm', 'Z:=', '0.0mm'])
segs.append(['NAME:PLSegment', 'SegmentType:=', 'Line', 'StartIndex:=', 3, 'NoOfPoints:=', 2])
pts.append(['NAME:PLPoint', 'X:=', '2.605000mm', 'Y:=', '1.572500mm', 'Z:=', '0.0mm'])
oEditor.CreatePolyline(
    ['NAME:PolylineParameters', 'IsPolylineCovered:=', True, 'IsPolylineClosed:=', True, pts, segs],
    [
        'NAME:Attributes',
        'Name:=', 'pad_bot_Q2_31',
        'Flags:=', '',
        'Color:=', '(200 220 255)',
        'Transparency:=', 0.0,
        'PartCoordinateSystem:=', 'Global',
        'UDMId:=', '',
        'MaterialName:=', 'vacuum',
        'SolveInside:=', True
    ]
)
# Element: rect_pk_Q2_32
pts = ['NAME:PolylinePoints']
segs = ['NAME:PolylineSegments']
pts.append(['NAME:PLPoint', 'X:=', '2.825000mm', 'Y:=', '1.475000mm', 'Z:=', '0.0mm'])
segs.append(['NAME:PLSegment', 'SegmentType:=', 'Line', 'StartIndex:=', 0, 'NoOfPoints:=', 2])
pts.append(['NAME:PLPoint', 'X:=', '2.825000mm', 'Y:=', '2.125000mm', 'Z:=', '0.0mm'])
segs.append(['NAME:PLSegment', 'SegmentType:=', 'Line', 'StartIndex:=', 1, 'NoOfPoints:=', 2])
pts.append(['NAME:PLPoint', 'X:=', '2.175000mm', 'Y:=', '2.125000mm', 'Z:=', '0.0mm'])
segs.append(['NAME:PLSegment', 'SegmentType:=', 'Line', 'StartIndex:=', 2, 'NoOfPoints:=', 2])
pts.append(['NAME:PLPoint', 'X:=', '2.175000mm', 'Y:=', '1.475000mm', 'Z:=', '0.0mm'])
segs.append(['NAME:PLSegment', 'SegmentType:=', 'Line', 'StartIndex:=', 3, 'NoOfPoints:=', 2])
pts.append(['NAME:PLPoint', 'X:=', '2.825000mm', 'Y:=', '1.475000mm', 'Z:=', '0.0mm'])
oEditor.CreatePolyline(
    ['NAME:PolylineParameters', 'IsPolylineCovered:=', True, 'IsPolylineClosed:=', True, pts, segs],
    [
        'NAME:Attributes',
        'Name:=', 'rect_pk_Q2_32',
        'Flags:=', '',
        'Color:=', '(255 100 100)',
        'Transparency:=', 0.0,
        'PartCoordinateSystem:=', 'Global',
        'UDMId:=', '',
        'MaterialName:=', 'vacuum',
        'SolveInside:=', True
    ]
)
# Element: bus_bot_connector_pad_Q2_33
pts = ['NAME:PolylinePoints']
segs = ['NAME:PolylineSegments']
pts.append(['NAME:PLPoint', 'X:=', '2.620000mm', 'Y:=', '1.902500mm', 'Z:=', '0.0mm'])
segs.append(['NAME:PLSegment', 'SegmentType:=', 'Line', 'StartIndex:=', 0, 'NoOfPoints:=', 2])
pts.append(['NAME:PLPoint', 'X:=', '2.620000mm', 'Y:=', '2.027500mm', 'Z:=', '0.0mm'])
segs.append(['NAME:PLSegment', 'SegmentType:=', 'Line', 'StartIndex:=', 1, 'NoOfPoints:=', 2])
pts.append(['NAME:PLPoint', 'X:=', '2.650000mm', 'Y:=', '2.027500mm', 'Z:=', '0.0mm'])
segs.append(['NAME:PLSegment', 'SegmentType:=', 'Line', 'StartIndex:=', 2, 'NoOfPoints:=', 2])
pts.append(['NAME:PLPoint', 'X:=', '2.650000mm', 'Y:=', '1.902500mm', 'Z:=', '0.0mm'])
segs.append(['NAME:PLSegment', 'SegmentType:=', 'Line', 'StartIndex:=', 3, 'NoOfPoints:=', 2])
pts.append(['NAME:PLPoint', 'X:=', '2.620000mm', 'Y:=', '1.902500mm', 'Z:=', '0.0mm'])
oEditor.CreatePolyline(
    ['NAME:PolylineParameters', 'IsPolylineCovered:=', True, 'IsPolylineClosed:=', True, pts, segs],
    [
        'NAME:Attributes',
        'Name:=', 'bus_bot_connector_pad_Q2_33',
        'Flags:=', '',
        'Color:=', '(200 220 255)',
        'Transparency:=', 0.0,
        'PartCoordinateSystem:=', 'Global',
        'UDMId:=', '',
        'MaterialName:=', 'vacuum',
        'SolveInside:=', True
    ]
)
# Element: bus_left_connector_pad_Q2_34
pts = ['NAME:PolylinePoints']
segs = ['NAME:PolylineSegments']
pts.append(['NAME:PLPoint', 'X:=', '2.620000mm', 'Y:=', '1.697500mm', 'Z:=', '0.0mm'])
segs.append(['NAME:PLSegment', 'SegmentType:=', 'Line', 'StartIndex:=', 0, 'NoOfPoints:=', 2])
pts.append(['NAME:PLPoint', 'X:=', '2.620000mm', 'Y:=', '1.572500mm', 'Z:=', '0.0mm'])
segs.append(['NAME:PLSegment', 'SegmentType:=', 'Line', 'StartIndex:=', 1, 'NoOfPoints:=', 2])
pts.append(['NAME:PLPoint', 'X:=', '2.650000mm', 'Y:=', '1.572500mm', 'Z:=', '0.0mm'])
segs.append(['NAME:PLSegment', 'SegmentType:=', 'Line', 'StartIndex:=', 2, 'NoOfPoints:=', 2])
pts.append(['NAME:PLPoint', 'X:=', '2.650000mm', 'Y:=', '1.697500mm', 'Z:=', '0.0mm'])
segs.append(['NAME:PLSegment', 'SegmentType:=', 'Line', 'StartIndex:=', 3, 'NoOfPoints:=', 2])
pts.append(['NAME:PLPoint', 'X:=', '2.620000mm', 'Y:=', '1.697500mm', 'Z:=', '0.0mm'])
oEditor.CreatePolyline(
    ['NAME:PolylineParameters', 'IsPolylineCovered:=', True, 'IsPolylineClosed:=', True, pts, segs],
    [
        'NAME:Attributes',
        'Name:=', 'bus_left_connector_pad_Q2_34',
        'Flags:=', '',
        'Color:=', '(200 220 255)',
        'Transparency:=', 0.0,
        'PartCoordinateSystem:=', 'Global',
        'UDMId:=', '',
        'MaterialName:=', 'vacuum',
        'SolveInside:=', True
    ]
)
# Element: readout_connector_pad_Q2_35
pts = ['NAME:PolylinePoints']
segs = ['NAME:PolylineSegments']
pts.append(['NAME:PLPoint', 'X:=', '2.380000mm', 'Y:=', '1.902500mm', 'Z:=', '0.0mm'])
segs.append(['NAME:PLSegment', 'SegmentType:=', 'Line', 'StartIndex:=', 0, 'NoOfPoints:=', 2])
pts.append(['NAME:PLPoint', 'X:=', '2.380000mm', 'Y:=', '2.027500mm', 'Z:=', '0.0mm'])
segs.append(['NAME:PLSegment', 'SegmentType:=', 'Line', 'StartIndex:=', 1, 'NoOfPoints:=', 2])
pts.append(['NAME:PLPoint', 'X:=', '2.350000mm', 'Y:=', '2.027500mm', 'Z:=', '0.0mm'])
segs.append(['NAME:PLSegment', 'SegmentType:=', 'Line', 'StartIndex:=', 2, 'NoOfPoints:=', 2])
pts.append(['NAME:PLPoint', 'X:=', '2.350000mm', 'Y:=', '1.902500mm', 'Z:=', '0.0mm'])
segs.append(['NAME:PLSegment', 'SegmentType:=', 'Line', 'StartIndex:=', 3, 'NoOfPoints:=', 2])
pts.append(['NAME:PLPoint', 'X:=', '2.380000mm', 'Y:=', '1.902500mm', 'Z:=', '0.0mm'])
oEditor.CreatePolyline(
    ['NAME:PolylineParameters', 'IsPolylineCovered:=', True, 'IsPolylineClosed:=', True, pts, segs],
    [
        'NAME:Attributes',
        'Name:=', 'readout_connector_pad_Q2_35',
        'Flags:=', '',
        'Color:=', '(200 220 255)',
        'Transparency:=', 0.0,
        'PartCoordinateSystem:=', 'Global',
        'UDMId:=', '',
        'MaterialName:=', 'vacuum',
        'SolveInside:=', True
    ]
)
# Element: pad_top_Q6_36
pts = ['NAME:PolylinePoints']
segs = ['NAME:PolylineSegments']
pts.append(['NAME:PLPoint', 'X:=', '2.485000mm', 'Y:=', '-0.227500mm', 'Z:=', '0.0mm'])
segs.append(['NAME:PLSegment', 'SegmentType:=', 'Line', 'StartIndex:=', 0, 'NoOfPoints:=', 2])
pts.append(['NAME:PLPoint', 'X:=', '2.485000mm', 'Y:=', '0.227500mm', 'Z:=', '0.0mm'])
segs.append(['NAME:PLSegment', 'SegmentType:=', 'Line', 'StartIndex:=', 1, 'NoOfPoints:=', 2])
pts.append(['NAME:PLPoint', 'X:=', '2.395000mm', 'Y:=', '0.227500mm', 'Z:=', '0.0mm'])
segs.append(['NAME:PLSegment', 'SegmentType:=', 'Line', 'StartIndex:=', 2, 'NoOfPoints:=', 2])
pts.append(['NAME:PLPoint', 'X:=', '2.395000mm', 'Y:=', '-0.227500mm', 'Z:=', '0.0mm'])
segs.append(['NAME:PLSegment', 'SegmentType:=', 'Line', 'StartIndex:=', 3, 'NoOfPoints:=', 2])
pts.append(['NAME:PLPoint', 'X:=', '2.485000mm', 'Y:=', '-0.227500mm', 'Z:=', '0.0mm'])
oEditor.CreatePolyline(
    ['NAME:PolylineParameters', 'IsPolylineCovered:=', True, 'IsPolylineClosed:=', True, pts, segs],
    [
        'NAME:Attributes',
        'Name:=', 'pad_top_Q6_36',
        'Flags:=', '',
        'Color:=', '(200 220 255)',
        'Transparency:=', 0.0,
        'PartCoordinateSystem:=', 'Global',
        'UDMId:=', '',
        'MaterialName:=', 'vacuum',
        'SolveInside:=', True
    ]
)
# Element: pad_bot_Q6_37
pts = ['NAME:PolylinePoints']
segs = ['NAME:PolylineSegments']
pts.append(['NAME:PLPoint', 'X:=', '2.605000mm', 'Y:=', '-0.227500mm', 'Z:=', '0.0mm'])
segs.append(['NAME:PLSegment', 'SegmentType:=', 'Line', 'StartIndex:=', 0, 'NoOfPoints:=', 2])
pts.append(['NAME:PLPoint', 'X:=', '2.605000mm', 'Y:=', '0.227500mm', 'Z:=', '0.0mm'])
segs.append(['NAME:PLSegment', 'SegmentType:=', 'Line', 'StartIndex:=', 1, 'NoOfPoints:=', 2])
pts.append(['NAME:PLPoint', 'X:=', '2.515000mm', 'Y:=', '0.227500mm', 'Z:=', '0.0mm'])
segs.append(['NAME:PLSegment', 'SegmentType:=', 'Line', 'StartIndex:=', 2, 'NoOfPoints:=', 2])
pts.append(['NAME:PLPoint', 'X:=', '2.515000mm', 'Y:=', '-0.227500mm', 'Z:=', '0.0mm'])
segs.append(['NAME:PLSegment', 'SegmentType:=', 'Line', 'StartIndex:=', 3, 'NoOfPoints:=', 2])
pts.append(['NAME:PLPoint', 'X:=', '2.605000mm', 'Y:=', '-0.227500mm', 'Z:=', '0.0mm'])
oEditor.CreatePolyline(
    ['NAME:PolylineParameters', 'IsPolylineCovered:=', True, 'IsPolylineClosed:=', True, pts, segs],
    [
        'NAME:Attributes',
        'Name:=', 'pad_bot_Q6_37',
        'Flags:=', '',
        'Color:=', '(200 220 255)',
        'Transparency:=', 0.0,
        'PartCoordinateSystem:=', 'Global',
        'UDMId:=', '',
        'MaterialName:=', 'vacuum',
        'SolveInside:=', True
    ]
)
# Element: rect_pk_Q6_38
pts = ['NAME:PolylinePoints']
segs = ['NAME:PolylineSegments']
pts.append(['NAME:PLPoint', 'X:=', '2.825000mm', 'Y:=', '-0.325000mm', 'Z:=', '0.0mm'])
segs.append(['NAME:PLSegment', 'SegmentType:=', 'Line', 'StartIndex:=', 0, 'NoOfPoints:=', 2])
pts.append(['NAME:PLPoint', 'X:=', '2.825000mm', 'Y:=', '0.325000mm', 'Z:=', '0.0mm'])
segs.append(['NAME:PLSegment', 'SegmentType:=', 'Line', 'StartIndex:=', 1, 'NoOfPoints:=', 2])
pts.append(['NAME:PLPoint', 'X:=', '2.175000mm', 'Y:=', '0.325000mm', 'Z:=', '0.0mm'])
segs.append(['NAME:PLSegment', 'SegmentType:=', 'Line', 'StartIndex:=', 2, 'NoOfPoints:=', 2])
pts.append(['NAME:PLPoint', 'X:=', '2.175000mm', 'Y:=', '-0.325000mm', 'Z:=', '0.0mm'])
segs.append(['NAME:PLSegment', 'SegmentType:=', 'Line', 'StartIndex:=', 3, 'NoOfPoints:=', 2])
pts.append(['NAME:PLPoint', 'X:=', '2.825000mm', 'Y:=', '-0.325000mm', 'Z:=', '0.0mm'])
oEditor.CreatePolyline(
    ['NAME:PolylineParameters', 'IsPolylineCovered:=', True, 'IsPolylineClosed:=', True, pts, segs],
    [
        'NAME:Attributes',
        'Name:=', 'rect_pk_Q6_38',
        'Flags:=', '',
        'Color:=', '(255 100 100)',
        'Transparency:=', 0.0,
        'PartCoordinateSystem:=', 'Global',
        'UDMId:=', '',
        'MaterialName:=', 'vacuum',
        'SolveInside:=', True
    ]
)
# Element: bus_top_connector_pad_Q6_39
pts = ['NAME:PolylinePoints']
segs = ['NAME:PolylineSegments']
pts.append(['NAME:PLPoint', 'X:=', '2.380000mm', 'Y:=', '0.102500mm', 'Z:=', '0.0mm'])
segs.append(['NAME:PLSegment', 'SegmentType:=', 'Line', 'StartIndex:=', 0, 'NoOfPoints:=', 2])
pts.append(['NAME:PLPoint', 'X:=', '2.380000mm', 'Y:=', '0.227500mm', 'Z:=', '0.0mm'])
segs.append(['NAME:PLSegment', 'SegmentType:=', 'Line', 'StartIndex:=', 1, 'NoOfPoints:=', 2])
pts.append(['NAME:PLPoint', 'X:=', '2.350000mm', 'Y:=', '0.227500mm', 'Z:=', '0.0mm'])
segs.append(['NAME:PLSegment', 'SegmentType:=', 'Line', 'StartIndex:=', 2, 'NoOfPoints:=', 2])
pts.append(['NAME:PLPoint', 'X:=', '2.350000mm', 'Y:=', '0.102500mm', 'Z:=', '0.0mm'])
segs.append(['NAME:PLSegment', 'SegmentType:=', 'Line', 'StartIndex:=', 3, 'NoOfPoints:=', 2])
pts.append(['NAME:PLPoint', 'X:=', '2.380000mm', 'Y:=', '0.102500mm', 'Z:=', '0.0mm'])
oEditor.CreatePolyline(
    ['NAME:PolylineParameters', 'IsPolylineCovered:=', True, 'IsPolylineClosed:=', True, pts, segs],
    [
        'NAME:Attributes',
        'Name:=', 'bus_top_connector_pad_Q6_39',
        'Flags:=', '',
        'Color:=', '(200 220 255)',
        'Transparency:=', 0.0,
        'PartCoordinateSystem:=', 'Global',
        'UDMId:=', '',
        'MaterialName:=', 'vacuum',
        'SolveInside:=', True
    ]
)
# Element: readout_connector_pad_Q6_40
pts = ['NAME:PolylinePoints']
segs = ['NAME:PolylineSegments']
pts.append(['NAME:PLPoint', 'X:=', '2.620000mm', 'Y:=', '-0.102500mm', 'Z:=', '0.0mm'])
segs.append(['NAME:PLSegment', 'SegmentType:=', 'Line', 'StartIndex:=', 0, 'NoOfPoints:=', 2])
pts.append(['NAME:PLPoint', 'X:=', '2.620000mm', 'Y:=', '-0.227500mm', 'Z:=', '0.0mm'])
segs.append(['NAME:PLSegment', 'SegmentType:=', 'Line', 'StartIndex:=', 1, 'NoOfPoints:=', 2])
pts.append(['NAME:PLPoint', 'X:=', '2.650000mm', 'Y:=', '-0.227500mm', 'Z:=', '0.0mm'])
segs.append(['NAME:PLSegment', 'SegmentType:=', 'Line', 'StartIndex:=', 2, 'NoOfPoints:=', 2])
pts.append(['NAME:PLPoint', 'X:=', '2.650000mm', 'Y:=', '-0.102500mm', 'Z:=', '0.0mm'])
segs.append(['NAME:PLSegment', 'SegmentType:=', 'Line', 'StartIndex:=', 3, 'NoOfPoints:=', 2])
pts.append(['NAME:PLPoint', 'X:=', '2.620000mm', 'Y:=', '-0.102500mm', 'Z:=', '0.0mm'])
oEditor.CreatePolyline(
    ['NAME:PolylineParameters', 'IsPolylineCovered:=', True, 'IsPolylineClosed:=', True, pts, segs],
    [
        'NAME:Attributes',
        'Name:=', 'readout_connector_pad_Q6_40',
        'Flags:=', '',
        'Color:=', '(200 220 255)',
        'Transparency:=', 0.0,
        'PartCoordinateSystem:=', 'Global',
        'UDMId:=', '',
        'MaterialName:=', 'vacuum',
        'SolveInside:=', True
    ]
)
# Element: launch_pad_LP_Q1_41
pts = ['NAME:PolylinePoints']
segs = ['NAME:PolylineSegments']
pts.append(['NAME:PLPoint', 'X:=', '-2.495000mm', 'Y:=', '4.000000mm', 'Z:=', '0.0mm'])
segs.append(['NAME:PLSegment', 'SegmentType:=', 'Line', 'StartIndex:=', 0, 'NoOfPoints:=', 2])
pts.append(['NAME:PLPoint', 'X:=', '-2.460000mm', 'Y:=', '4.122000mm', 'Z:=', '0.0mm'])
segs.append(['NAME:PLSegment', 'SegmentType:=', 'Line', 'StartIndex:=', 1, 'NoOfPoints:=', 2])
pts.append(['NAME:PLPoint', 'X:=', '-2.460000mm', 'Y:=', '4.202000mm', 'Z:=', '0.0mm'])
segs.append(['NAME:PLSegment', 'SegmentType:=', 'Line', 'StartIndex:=', 2, 'NoOfPoints:=', 2])
pts.append(['NAME:PLPoint', 'X:=', '-2.540000mm', 'Y:=', '4.202000mm', 'Z:=', '0.0mm'])
segs.append(['NAME:PLSegment', 'SegmentType:=', 'Line', 'StartIndex:=', 3, 'NoOfPoints:=', 2])
pts.append(['NAME:PLPoint', 'X:=', '-2.540000mm', 'Y:=', '4.122000mm', 'Z:=', '0.0mm'])
segs.append(['NAME:PLSegment', 'SegmentType:=', 'Line', 'StartIndex:=', 4, 'NoOfPoints:=', 2])
pts.append(['NAME:PLPoint', 'X:=', '-2.505000mm', 'Y:=', '4.000000mm', 'Z:=', '0.0mm'])
segs.append(['NAME:PLSegment', 'SegmentType:=', 'Line', 'StartIndex:=', 5, 'NoOfPoints:=', 2])
pts.append(['NAME:PLPoint', 'X:=', '-2.505000mm', 'Y:=', '3.975000mm', 'Z:=', '0.0mm'])
segs.append(['NAME:PLSegment', 'SegmentType:=', 'Line', 'StartIndex:=', 6, 'NoOfPoints:=', 2])
pts.append(['NAME:PLPoint', 'X:=', '-2.495000mm', 'Y:=', '3.975000mm', 'Z:=', '0.0mm'])
segs.append(['NAME:PLSegment', 'SegmentType:=', 'Line', 'StartIndex:=', 7, 'NoOfPoints:=', 2])
pts.append(['NAME:PLPoint', 'X:=', '-2.495000mm', 'Y:=', '4.000000mm', 'Z:=', '0.0mm'])
oEditor.CreatePolyline(
    ['NAME:PolylineParameters', 'IsPolylineCovered:=', True, 'IsPolylineClosed:=', True, pts, segs],
    [
        'NAME:Attributes',
        'Name:=', 'launch_pad_LP_Q1_41',
        'Flags:=', '',
        'Color:=', '(200 220 255)',
        'Transparency:=', 0.0,
        'PartCoordinateSystem:=', 'Global',
        'UDMId:=', '',
        'MaterialName:=', 'vacuum',
        'SolveInside:=', True
    ]
)
# Element: pocket_LP_Q1_42
pts = ['NAME:PolylinePoints']
segs = ['NAME:PolylineSegments']
pts.append(['NAME:PLPoint', 'X:=', '-2.489000mm', 'Y:=', '4.000000mm', 'Z:=', '0.0mm'])
segs.append(['NAME:PLSegment', 'SegmentType:=', 'Line', 'StartIndex:=', 0, 'NoOfPoints:=', 2])
pts.append(['NAME:PLPoint', 'X:=', '-2.402000mm', 'Y:=', '4.122000mm', 'Z:=', '0.0mm'])
segs.append(['NAME:PLSegment', 'SegmentType:=', 'Line', 'StartIndex:=', 1, 'NoOfPoints:=', 2])
pts.append(['NAME:PLPoint', 'X:=', '-2.402000mm', 'Y:=', '4.260000mm', 'Z:=', '0.0mm'])
segs.append(['NAME:PLSegment', 'SegmentType:=', 'Line', 'StartIndex:=', 2, 'NoOfPoints:=', 2])
pts.append(['NAME:PLPoint', 'X:=', '-2.598000mm', 'Y:=', '4.260000mm', 'Z:=', '0.0mm'])
segs.append(['NAME:PLSegment', 'SegmentType:=', 'Line', 'StartIndex:=', 3, 'NoOfPoints:=', 2])
pts.append(['NAME:PLPoint', 'X:=', '-2.598000mm', 'Y:=', '4.122000mm', 'Z:=', '0.0mm'])
segs.append(['NAME:PLSegment', 'SegmentType:=', 'Line', 'StartIndex:=', 4, 'NoOfPoints:=', 2])
pts.append(['NAME:PLPoint', 'X:=', '-2.511000mm', 'Y:=', '4.000000mm', 'Z:=', '0.0mm'])
segs.append(['NAME:PLSegment', 'SegmentType:=', 'Line', 'StartIndex:=', 5, 'NoOfPoints:=', 2])
pts.append(['NAME:PLPoint', 'X:=', '-2.511000mm', 'Y:=', '3.975000mm', 'Z:=', '0.0mm'])
segs.append(['NAME:PLSegment', 'SegmentType:=', 'Line', 'StartIndex:=', 6, 'NoOfPoints:=', 2])
pts.append(['NAME:PLPoint', 'X:=', '-2.489000mm', 'Y:=', '3.975000mm', 'Z:=', '0.0mm'])
segs.append(['NAME:PLSegment', 'SegmentType:=', 'Line', 'StartIndex:=', 7, 'NoOfPoints:=', 2])
pts.append(['NAME:PLPoint', 'X:=', '-2.489000mm', 'Y:=', '4.000000mm', 'Z:=', '0.0mm'])
oEditor.CreatePolyline(
    ['NAME:PolylineParameters', 'IsPolylineCovered:=', True, 'IsPolylineClosed:=', True, pts, segs],
    [
        'NAME:Attributes',
        'Name:=', 'pocket_LP_Q1_42',
        'Flags:=', '',
        'Color:=', '(255 100 100)',
        'Transparency:=', 0.0,
        'PartCoordinateSystem:=', 'Global',
        'UDMId:=', '',
        'MaterialName:=', 'vacuum',
        'SolveInside:=', True
    ]
)
# Element: launch_pad_LP_Q3_43
pts = ['NAME:PolylinePoints']
segs = ['NAME:PolylineSegments']
pts.append(['NAME:PLPoint', 'X:=', '-0.995000mm', 'Y:=', '4.200000mm', 'Z:=', '0.0mm'])
segs.append(['NAME:PLSegment', 'SegmentType:=', 'Line', 'StartIndex:=', 0, 'NoOfPoints:=', 2])
pts.append(['NAME:PLPoint', 'X:=', '-0.960000mm', 'Y:=', '4.322000mm', 'Z:=', '0.0mm'])
segs.append(['NAME:PLSegment', 'SegmentType:=', 'Line', 'StartIndex:=', 1, 'NoOfPoints:=', 2])
pts.append(['NAME:PLPoint', 'X:=', '-0.960000mm', 'Y:=', '4.402000mm', 'Z:=', '0.0mm'])
segs.append(['NAME:PLSegment', 'SegmentType:=', 'Line', 'StartIndex:=', 2, 'NoOfPoints:=', 2])
pts.append(['NAME:PLPoint', 'X:=', '-1.040000mm', 'Y:=', '4.402000mm', 'Z:=', '0.0mm'])
segs.append(['NAME:PLSegment', 'SegmentType:=', 'Line', 'StartIndex:=', 3, 'NoOfPoints:=', 2])
pts.append(['NAME:PLPoint', 'X:=', '-1.040000mm', 'Y:=', '4.322000mm', 'Z:=', '0.0mm'])
segs.append(['NAME:PLSegment', 'SegmentType:=', 'Line', 'StartIndex:=', 4, 'NoOfPoints:=', 2])
pts.append(['NAME:PLPoint', 'X:=', '-1.005000mm', 'Y:=', '4.200000mm', 'Z:=', '0.0mm'])
segs.append(['NAME:PLSegment', 'SegmentType:=', 'Line', 'StartIndex:=', 5, 'NoOfPoints:=', 2])
pts.append(['NAME:PLPoint', 'X:=', '-1.005000mm', 'Y:=', '4.175000mm', 'Z:=', '0.0mm'])
segs.append(['NAME:PLSegment', 'SegmentType:=', 'Line', 'StartIndex:=', 6, 'NoOfPoints:=', 2])
pts.append(['NAME:PLPoint', 'X:=', '-0.995000mm', 'Y:=', '4.175000mm', 'Z:=', '0.0mm'])
segs.append(['NAME:PLSegment', 'SegmentType:=', 'Line', 'StartIndex:=', 7, 'NoOfPoints:=', 2])
pts.append(['NAME:PLPoint', 'X:=', '-0.995000mm', 'Y:=', '4.200000mm', 'Z:=', '0.0mm'])
oEditor.CreatePolyline(
    ['NAME:PolylineParameters', 'IsPolylineCovered:=', True, 'IsPolylineClosed:=', True, pts, segs],
    [
        'NAME:Attributes',
        'Name:=', 'launch_pad_LP_Q3_43',
        'Flags:=', '',
        'Color:=', '(200 220 255)',
        'Transparency:=', 0.0,
        'PartCoordinateSystem:=', 'Global',
        'UDMId:=', '',
        'MaterialName:=', 'vacuum',
        'SolveInside:=', True
    ]
)
# Element: pocket_LP_Q3_44
pts = ['NAME:PolylinePoints']
segs = ['NAME:PolylineSegments']
pts.append(['NAME:PLPoint', 'X:=', '-0.989000mm', 'Y:=', '4.200000mm', 'Z:=', '0.0mm'])
segs.append(['NAME:PLSegment', 'SegmentType:=', 'Line', 'StartIndex:=', 0, 'NoOfPoints:=', 2])
pts.append(['NAME:PLPoint', 'X:=', '-0.902000mm', 'Y:=', '4.322000mm', 'Z:=', '0.0mm'])
segs.append(['NAME:PLSegment', 'SegmentType:=', 'Line', 'StartIndex:=', 1, 'NoOfPoints:=', 2])
pts.append(['NAME:PLPoint', 'X:=', '-0.902000mm', 'Y:=', '4.460000mm', 'Z:=', '0.0mm'])
segs.append(['NAME:PLSegment', 'SegmentType:=', 'Line', 'StartIndex:=', 2, 'NoOfPoints:=', 2])
pts.append(['NAME:PLPoint', 'X:=', '-1.098000mm', 'Y:=', '4.460000mm', 'Z:=', '0.0mm'])
segs.append(['NAME:PLSegment', 'SegmentType:=', 'Line', 'StartIndex:=', 3, 'NoOfPoints:=', 2])
pts.append(['NAME:PLPoint', 'X:=', '-1.098000mm', 'Y:=', '4.322000mm', 'Z:=', '0.0mm'])
segs.append(['NAME:PLSegment', 'SegmentType:=', 'Line', 'StartIndex:=', 4, 'NoOfPoints:=', 2])
pts.append(['NAME:PLPoint', 'X:=', '-1.011000mm', 'Y:=', '4.200000mm', 'Z:=', '0.0mm'])
segs.append(['NAME:PLSegment', 'SegmentType:=', 'Line', 'StartIndex:=', 5, 'NoOfPoints:=', 2])
pts.append(['NAME:PLPoint', 'X:=', '-1.011000mm', 'Y:=', '4.175000mm', 'Z:=', '0.0mm'])
segs.append(['NAME:PLSegment', 'SegmentType:=', 'Line', 'StartIndex:=', 6, 'NoOfPoints:=', 2])
pts.append(['NAME:PLPoint', 'X:=', '-0.989000mm', 'Y:=', '4.175000mm', 'Z:=', '0.0mm'])
segs.append(['NAME:PLSegment', 'SegmentType:=', 'Line', 'StartIndex:=', 7, 'NoOfPoints:=', 2])
pts.append(['NAME:PLPoint', 'X:=', '-0.989000mm', 'Y:=', '4.200000mm', 'Z:=', '0.0mm'])
oEditor.CreatePolyline(
    ['NAME:PolylineParameters', 'IsPolylineCovered:=', True, 'IsPolylineClosed:=', True, pts, segs],
    [
        'NAME:Attributes',
        'Name:=', 'pocket_LP_Q3_44',
        'Flags:=', '',
        'Color:=', '(255 100 100)',
        'Transparency:=', 0.0,
        'PartCoordinateSystem:=', 'Global',
        'UDMId:=', '',
        'MaterialName:=', 'vacuum',
        'SolveInside:=', True
    ]
)
# Element: launch_pad_LP_Q5_45
pts = ['NAME:PolylinePoints']
segs = ['NAME:PolylineSegments']
pts.append(['NAME:PLPoint', 'X:=', '1.005000mm', 'Y:=', '4.200000mm', 'Z:=', '0.0mm'])
segs.append(['NAME:PLSegment', 'SegmentType:=', 'Line', 'StartIndex:=', 0, 'NoOfPoints:=', 2])
pts.append(['NAME:PLPoint', 'X:=', '1.040000mm', 'Y:=', '4.322000mm', 'Z:=', '0.0mm'])
segs.append(['NAME:PLSegment', 'SegmentType:=', 'Line', 'StartIndex:=', 1, 'NoOfPoints:=', 2])
pts.append(['NAME:PLPoint', 'X:=', '1.040000mm', 'Y:=', '4.402000mm', 'Z:=', '0.0mm'])
segs.append(['NAME:PLSegment', 'SegmentType:=', 'Line', 'StartIndex:=', 2, 'NoOfPoints:=', 2])
pts.append(['NAME:PLPoint', 'X:=', '0.960000mm', 'Y:=', '4.402000mm', 'Z:=', '0.0mm'])
segs.append(['NAME:PLSegment', 'SegmentType:=', 'Line', 'StartIndex:=', 3, 'NoOfPoints:=', 2])
pts.append(['NAME:PLPoint', 'X:=', '0.960000mm', 'Y:=', '4.322000mm', 'Z:=', '0.0mm'])
segs.append(['NAME:PLSegment', 'SegmentType:=', 'Line', 'StartIndex:=', 4, 'NoOfPoints:=', 2])
pts.append(['NAME:PLPoint', 'X:=', '0.995000mm', 'Y:=', '4.200000mm', 'Z:=', '0.0mm'])
segs.append(['NAME:PLSegment', 'SegmentType:=', 'Line', 'StartIndex:=', 5, 'NoOfPoints:=', 2])
pts.append(['NAME:PLPoint', 'X:=', '0.995000mm', 'Y:=', '4.175000mm', 'Z:=', '0.0mm'])
segs.append(['NAME:PLSegment', 'SegmentType:=', 'Line', 'StartIndex:=', 6, 'NoOfPoints:=', 2])
pts.append(['NAME:PLPoint', 'X:=', '1.005000mm', 'Y:=', '4.175000mm', 'Z:=', '0.0mm'])
segs.append(['NAME:PLSegment', 'SegmentType:=', 'Line', 'StartIndex:=', 7, 'NoOfPoints:=', 2])
pts.append(['NAME:PLPoint', 'X:=', '1.005000mm', 'Y:=', '4.200000mm', 'Z:=', '0.0mm'])
oEditor.CreatePolyline(
    ['NAME:PolylineParameters', 'IsPolylineCovered:=', True, 'IsPolylineClosed:=', True, pts, segs],
    [
        'NAME:Attributes',
        'Name:=', 'launch_pad_LP_Q5_45',
        'Flags:=', '',
        'Color:=', '(200 220 255)',
        'Transparency:=', 0.0,
        'PartCoordinateSystem:=', 'Global',
        'UDMId:=', '',
        'MaterialName:=', 'vacuum',
        'SolveInside:=', True
    ]
)
# Element: pocket_LP_Q5_46
pts = ['NAME:PolylinePoints']
segs = ['NAME:PolylineSegments']
pts.append(['NAME:PLPoint', 'X:=', '1.011000mm', 'Y:=', '4.200000mm', 'Z:=', '0.0mm'])
segs.append(['NAME:PLSegment', 'SegmentType:=', 'Line', 'StartIndex:=', 0, 'NoOfPoints:=', 2])
pts.append(['NAME:PLPoint', 'X:=', '1.098000mm', 'Y:=', '4.322000mm', 'Z:=', '0.0mm'])
segs.append(['NAME:PLSegment', 'SegmentType:=', 'Line', 'StartIndex:=', 1, 'NoOfPoints:=', 2])
pts.append(['NAME:PLPoint', 'X:=', '1.098000mm', 'Y:=', '4.460000mm', 'Z:=', '0.0mm'])
segs.append(['NAME:PLSegment', 'SegmentType:=', 'Line', 'StartIndex:=', 2, 'NoOfPoints:=', 2])
pts.append(['NAME:PLPoint', 'X:=', '0.902000mm', 'Y:=', '4.460000mm', 'Z:=', '0.0mm'])
segs.append(['NAME:PLSegment', 'SegmentType:=', 'Line', 'StartIndex:=', 3, 'NoOfPoints:=', 2])
pts.append(['NAME:PLPoint', 'X:=', '0.902000mm', 'Y:=', '4.322000mm', 'Z:=', '0.0mm'])
segs.append(['NAME:PLSegment', 'SegmentType:=', 'Line', 'StartIndex:=', 4, 'NoOfPoints:=', 2])
pts.append(['NAME:PLPoint', 'X:=', '0.989000mm', 'Y:=', '4.200000mm', 'Z:=', '0.0mm'])
segs.append(['NAME:PLSegment', 'SegmentType:=', 'Line', 'StartIndex:=', 5, 'NoOfPoints:=', 2])
pts.append(['NAME:PLPoint', 'X:=', '0.989000mm', 'Y:=', '4.175000mm', 'Z:=', '0.0mm'])
segs.append(['NAME:PLSegment', 'SegmentType:=', 'Line', 'StartIndex:=', 6, 'NoOfPoints:=', 2])
pts.append(['NAME:PLPoint', 'X:=', '1.011000mm', 'Y:=', '4.175000mm', 'Z:=', '0.0mm'])
segs.append(['NAME:PLSegment', 'SegmentType:=', 'Line', 'StartIndex:=', 7, 'NoOfPoints:=', 2])
pts.append(['NAME:PLPoint', 'X:=', '1.011000mm', 'Y:=', '4.200000mm', 'Z:=', '0.0mm'])
oEditor.CreatePolyline(
    ['NAME:PolylineParameters', 'IsPolylineCovered:=', True, 'IsPolylineClosed:=', True, pts, segs],
    [
        'NAME:Attributes',
        'Name:=', 'pocket_LP_Q5_46',
        'Flags:=', '',
        'Color:=', '(255 100 100)',
        'Transparency:=', 0.0,
        'PartCoordinateSystem:=', 'Global',
        'UDMId:=', '',
        'MaterialName:=', 'vacuum',
        'SolveInside:=', True
    ]
)
# Element: launch_pad_LP_Q2_47
pts = ['NAME:PolylinePoints']
segs = ['NAME:PolylineSegments']
pts.append(['NAME:PLPoint', 'X:=', '2.505000mm', 'Y:=', '4.000000mm', 'Z:=', '0.0mm'])
segs.append(['NAME:PLSegment', 'SegmentType:=', 'Line', 'StartIndex:=', 0, 'NoOfPoints:=', 2])
pts.append(['NAME:PLPoint', 'X:=', '2.540000mm', 'Y:=', '4.122000mm', 'Z:=', '0.0mm'])
segs.append(['NAME:PLSegment', 'SegmentType:=', 'Line', 'StartIndex:=', 1, 'NoOfPoints:=', 2])
pts.append(['NAME:PLPoint', 'X:=', '2.540000mm', 'Y:=', '4.202000mm', 'Z:=', '0.0mm'])
segs.append(['NAME:PLSegment', 'SegmentType:=', 'Line', 'StartIndex:=', 2, 'NoOfPoints:=', 2])
pts.append(['NAME:PLPoint', 'X:=', '2.460000mm', 'Y:=', '4.202000mm', 'Z:=', '0.0mm'])
segs.append(['NAME:PLSegment', 'SegmentType:=', 'Line', 'StartIndex:=', 3, 'NoOfPoints:=', 2])
pts.append(['NAME:PLPoint', 'X:=', '2.460000mm', 'Y:=', '4.122000mm', 'Z:=', '0.0mm'])
segs.append(['NAME:PLSegment', 'SegmentType:=', 'Line', 'StartIndex:=', 4, 'NoOfPoints:=', 2])
pts.append(['NAME:PLPoint', 'X:=', '2.495000mm', 'Y:=', '4.000000mm', 'Z:=', '0.0mm'])
segs.append(['NAME:PLSegment', 'SegmentType:=', 'Line', 'StartIndex:=', 5, 'NoOfPoints:=', 2])
pts.append(['NAME:PLPoint', 'X:=', '2.495000mm', 'Y:=', '3.975000mm', 'Z:=', '0.0mm'])
segs.append(['NAME:PLSegment', 'SegmentType:=', 'Line', 'StartIndex:=', 6, 'NoOfPoints:=', 2])
pts.append(['NAME:PLPoint', 'X:=', '2.505000mm', 'Y:=', '3.975000mm', 'Z:=', '0.0mm'])
segs.append(['NAME:PLSegment', 'SegmentType:=', 'Line', 'StartIndex:=', 7, 'NoOfPoints:=', 2])
pts.append(['NAME:PLPoint', 'X:=', '2.505000mm', 'Y:=', '4.000000mm', 'Z:=', '0.0mm'])
oEditor.CreatePolyline(
    ['NAME:PolylineParameters', 'IsPolylineCovered:=', True, 'IsPolylineClosed:=', True, pts, segs],
    [
        'NAME:Attributes',
        'Name:=', 'launch_pad_LP_Q2_47',
        'Flags:=', '',
        'Color:=', '(200 220 255)',
        'Transparency:=', 0.0,
        'PartCoordinateSystem:=', 'Global',
        'UDMId:=', '',
        'MaterialName:=', 'vacuum',
        'SolveInside:=', True
    ]
)
# Element: pocket_LP_Q2_48
pts = ['NAME:PolylinePoints']
segs = ['NAME:PolylineSegments']
pts.append(['NAME:PLPoint', 'X:=', '2.511000mm', 'Y:=', '4.000000mm', 'Z:=', '0.0mm'])
segs.append(['NAME:PLSegment', 'SegmentType:=', 'Line', 'StartIndex:=', 0, 'NoOfPoints:=', 2])
pts.append(['NAME:PLPoint', 'X:=', '2.598000mm', 'Y:=', '4.122000mm', 'Z:=', '0.0mm'])
segs.append(['NAME:PLSegment', 'SegmentType:=', 'Line', 'StartIndex:=', 1, 'NoOfPoints:=', 2])
pts.append(['NAME:PLPoint', 'X:=', '2.598000mm', 'Y:=', '4.260000mm', 'Z:=', '0.0mm'])
segs.append(['NAME:PLSegment', 'SegmentType:=', 'Line', 'StartIndex:=', 2, 'NoOfPoints:=', 2])
pts.append(['NAME:PLPoint', 'X:=', '2.402000mm', 'Y:=', '4.260000mm', 'Z:=', '0.0mm'])
segs.append(['NAME:PLSegment', 'SegmentType:=', 'Line', 'StartIndex:=', 3, 'NoOfPoints:=', 2])
pts.append(['NAME:PLPoint', 'X:=', '2.402000mm', 'Y:=', '4.122000mm', 'Z:=', '0.0mm'])
segs.append(['NAME:PLSegment', 'SegmentType:=', 'Line', 'StartIndex:=', 4, 'NoOfPoints:=', 2])
pts.append(['NAME:PLPoint', 'X:=', '2.489000mm', 'Y:=', '4.000000mm', 'Z:=', '0.0mm'])
segs.append(['NAME:PLSegment', 'SegmentType:=', 'Line', 'StartIndex:=', 5, 'NoOfPoints:=', 2])
pts.append(['NAME:PLPoint', 'X:=', '2.489000mm', 'Y:=', '3.975000mm', 'Z:=', '0.0mm'])
segs.append(['NAME:PLSegment', 'SegmentType:=', 'Line', 'StartIndex:=', 6, 'NoOfPoints:=', 2])
pts.append(['NAME:PLPoint', 'X:=', '2.511000mm', 'Y:=', '3.975000mm', 'Z:=', '0.0mm'])
segs.append(['NAME:PLSegment', 'SegmentType:=', 'Line', 'StartIndex:=', 7, 'NoOfPoints:=', 2])
pts.append(['NAME:PLPoint', 'X:=', '2.511000mm', 'Y:=', '4.000000mm', 'Z:=', '0.0mm'])
oEditor.CreatePolyline(
    ['NAME:PolylineParameters', 'IsPolylineCovered:=', True, 'IsPolylineClosed:=', True, pts, segs],
    [
        'NAME:Attributes',
        'Name:=', 'pocket_LP_Q2_48',
        'Flags:=', '',
        'Color:=', '(255 100 100)',
        'Transparency:=', 0.0,
        'PartCoordinateSystem:=', 'Global',
        'UDMId:=', '',
        'MaterialName:=', 'vacuum',
        'SolveInside:=', True
    ]
)
# Element: launch_pad_LP_Q0_49
pts = ['NAME:PolylinePoints']
segs = ['NAME:PolylineSegments']
pts.append(['NAME:PLPoint', 'X:=', '-2.505000mm', 'Y:=', '-2.000000mm', 'Z:=', '0.0mm'])
segs.append(['NAME:PLSegment', 'SegmentType:=', 'Line', 'StartIndex:=', 0, 'NoOfPoints:=', 2])
pts.append(['NAME:PLPoint', 'X:=', '-2.540000mm', 'Y:=', '-2.122000mm', 'Z:=', '0.0mm'])
segs.append(['NAME:PLSegment', 'SegmentType:=', 'Line', 'StartIndex:=', 1, 'NoOfPoints:=', 2])
pts.append(['NAME:PLPoint', 'X:=', '-2.540000mm', 'Y:=', '-2.202000mm', 'Z:=', '0.0mm'])
segs.append(['NAME:PLSegment', 'SegmentType:=', 'Line', 'StartIndex:=', 2, 'NoOfPoints:=', 2])
pts.append(['NAME:PLPoint', 'X:=', '-2.460000mm', 'Y:=', '-2.202000mm', 'Z:=', '0.0mm'])
segs.append(['NAME:PLSegment', 'SegmentType:=', 'Line', 'StartIndex:=', 3, 'NoOfPoints:=', 2])
pts.append(['NAME:PLPoint', 'X:=', '-2.460000mm', 'Y:=', '-2.122000mm', 'Z:=', '0.0mm'])
segs.append(['NAME:PLSegment', 'SegmentType:=', 'Line', 'StartIndex:=', 4, 'NoOfPoints:=', 2])
pts.append(['NAME:PLPoint', 'X:=', '-2.495000mm', 'Y:=', '-2.000000mm', 'Z:=', '0.0mm'])
segs.append(['NAME:PLSegment', 'SegmentType:=', 'Line', 'StartIndex:=', 5, 'NoOfPoints:=', 2])
pts.append(['NAME:PLPoint', 'X:=', '-2.495000mm', 'Y:=', '-1.975000mm', 'Z:=', '0.0mm'])
segs.append(['NAME:PLSegment', 'SegmentType:=', 'Line', 'StartIndex:=', 6, 'NoOfPoints:=', 2])
pts.append(['NAME:PLPoint', 'X:=', '-2.505000mm', 'Y:=', '-1.975000mm', 'Z:=', '0.0mm'])
segs.append(['NAME:PLSegment', 'SegmentType:=', 'Line', 'StartIndex:=', 7, 'NoOfPoints:=', 2])
pts.append(['NAME:PLPoint', 'X:=', '-2.505000mm', 'Y:=', '-2.000000mm', 'Z:=', '0.0mm'])
oEditor.CreatePolyline(
    ['NAME:PolylineParameters', 'IsPolylineCovered:=', True, 'IsPolylineClosed:=', True, pts, segs],
    [
        'NAME:Attributes',
        'Name:=', 'launch_pad_LP_Q0_49',
        'Flags:=', '',
        'Color:=', '(200 220 255)',
        'Transparency:=', 0.0,
        'PartCoordinateSystem:=', 'Global',
        'UDMId:=', '',
        'MaterialName:=', 'vacuum',
        'SolveInside:=', True
    ]
)
# Element: pocket_LP_Q0_50
pts = ['NAME:PolylinePoints']
segs = ['NAME:PolylineSegments']
pts.append(['NAME:PLPoint', 'X:=', '-2.511000mm', 'Y:=', '-2.000000mm', 'Z:=', '0.0mm'])
segs.append(['NAME:PLSegment', 'SegmentType:=', 'Line', 'StartIndex:=', 0, 'NoOfPoints:=', 2])
pts.append(['NAME:PLPoint', 'X:=', '-2.598000mm', 'Y:=', '-2.122000mm', 'Z:=', '0.0mm'])
segs.append(['NAME:PLSegment', 'SegmentType:=', 'Line', 'StartIndex:=', 1, 'NoOfPoints:=', 2])
pts.append(['NAME:PLPoint', 'X:=', '-2.598000mm', 'Y:=', '-2.260000mm', 'Z:=', '0.0mm'])
segs.append(['NAME:PLSegment', 'SegmentType:=', 'Line', 'StartIndex:=', 2, 'NoOfPoints:=', 2])
pts.append(['NAME:PLPoint', 'X:=', '-2.402000mm', 'Y:=', '-2.260000mm', 'Z:=', '0.0mm'])
segs.append(['NAME:PLSegment', 'SegmentType:=', 'Line', 'StartIndex:=', 3, 'NoOfPoints:=', 2])
pts.append(['NAME:PLPoint', 'X:=', '-2.402000mm', 'Y:=', '-2.122000mm', 'Z:=', '0.0mm'])
segs.append(['NAME:PLSegment', 'SegmentType:=', 'Line', 'StartIndex:=', 4, 'NoOfPoints:=', 2])
pts.append(['NAME:PLPoint', 'X:=', '-2.489000mm', 'Y:=', '-2.000000mm', 'Z:=', '0.0mm'])
segs.append(['NAME:PLSegment', 'SegmentType:=', 'Line', 'StartIndex:=', 5, 'NoOfPoints:=', 2])
pts.append(['NAME:PLPoint', 'X:=', '-2.489000mm', 'Y:=', '-1.975000mm', 'Z:=', '0.0mm'])
segs.append(['NAME:PLSegment', 'SegmentType:=', 'Line', 'StartIndex:=', 6, 'NoOfPoints:=', 2])
pts.append(['NAME:PLPoint', 'X:=', '-2.511000mm', 'Y:=', '-1.975000mm', 'Z:=', '0.0mm'])
segs.append(['NAME:PLSegment', 'SegmentType:=', 'Line', 'StartIndex:=', 7, 'NoOfPoints:=', 2])
pts.append(['NAME:PLPoint', 'X:=', '-2.511000mm', 'Y:=', '-2.000000mm', 'Z:=', '0.0mm'])
oEditor.CreatePolyline(
    ['NAME:PolylineParameters', 'IsPolylineCovered:=', True, 'IsPolylineClosed:=', True, pts, segs],
    [
        'NAME:Attributes',
        'Name:=', 'pocket_LP_Q0_50',
        'Flags:=', '',
        'Color:=', '(255 100 100)',
        'Transparency:=', 0.0,
        'PartCoordinateSystem:=', 'Global',
        'UDMId:=', '',
        'MaterialName:=', 'vacuum',
        'SolveInside:=', True
    ]
)
# Element: launch_pad_LP_Q6_51
pts = ['NAME:PolylinePoints']
segs = ['NAME:PolylineSegments']
pts.append(['NAME:PLPoint', 'X:=', '2.495000mm', 'Y:=', '-2.000000mm', 'Z:=', '0.0mm'])
segs.append(['NAME:PLSegment', 'SegmentType:=', 'Line', 'StartIndex:=', 0, 'NoOfPoints:=', 2])
pts.append(['NAME:PLPoint', 'X:=', '2.460000mm', 'Y:=', '-2.122000mm', 'Z:=', '0.0mm'])
segs.append(['NAME:PLSegment', 'SegmentType:=', 'Line', 'StartIndex:=', 1, 'NoOfPoints:=', 2])
pts.append(['NAME:PLPoint', 'X:=', '2.460000mm', 'Y:=', '-2.202000mm', 'Z:=', '0.0mm'])
segs.append(['NAME:PLSegment', 'SegmentType:=', 'Line', 'StartIndex:=', 2, 'NoOfPoints:=', 2])
pts.append(['NAME:PLPoint', 'X:=', '2.540000mm', 'Y:=', '-2.202000mm', 'Z:=', '0.0mm'])
segs.append(['NAME:PLSegment', 'SegmentType:=', 'Line', 'StartIndex:=', 3, 'NoOfPoints:=', 2])
pts.append(['NAME:PLPoint', 'X:=', '2.540000mm', 'Y:=', '-2.122000mm', 'Z:=', '0.0mm'])
segs.append(['NAME:PLSegment', 'SegmentType:=', 'Line', 'StartIndex:=', 4, 'NoOfPoints:=', 2])
pts.append(['NAME:PLPoint', 'X:=', '2.505000mm', 'Y:=', '-2.000000mm', 'Z:=', '0.0mm'])
segs.append(['NAME:PLSegment', 'SegmentType:=', 'Line', 'StartIndex:=', 5, 'NoOfPoints:=', 2])
pts.append(['NAME:PLPoint', 'X:=', '2.505000mm', 'Y:=', '-1.975000mm', 'Z:=', '0.0mm'])
segs.append(['NAME:PLSegment', 'SegmentType:=', 'Line', 'StartIndex:=', 6, 'NoOfPoints:=', 2])
pts.append(['NAME:PLPoint', 'X:=', '2.495000mm', 'Y:=', '-1.975000mm', 'Z:=', '0.0mm'])
segs.append(['NAME:PLSegment', 'SegmentType:=', 'Line', 'StartIndex:=', 7, 'NoOfPoints:=', 2])
pts.append(['NAME:PLPoint', 'X:=', '2.495000mm', 'Y:=', '-2.000000mm', 'Z:=', '0.0mm'])
oEditor.CreatePolyline(
    ['NAME:PolylineParameters', 'IsPolylineCovered:=', True, 'IsPolylineClosed:=', True, pts, segs],
    [
        'NAME:Attributes',
        'Name:=', 'launch_pad_LP_Q6_51',
        'Flags:=', '',
        'Color:=', '(200 220 255)',
        'Transparency:=', 0.0,
        'PartCoordinateSystem:=', 'Global',
        'UDMId:=', '',
        'MaterialName:=', 'vacuum',
        'SolveInside:=', True
    ]
)
# Element: pocket_LP_Q6_52
pts = ['NAME:PolylinePoints']
segs = ['NAME:PolylineSegments']
pts.append(['NAME:PLPoint', 'X:=', '2.489000mm', 'Y:=', '-2.000000mm', 'Z:=', '0.0mm'])
segs.append(['NAME:PLSegment', 'SegmentType:=', 'Line', 'StartIndex:=', 0, 'NoOfPoints:=', 2])
pts.append(['NAME:PLPoint', 'X:=', '2.402000mm', 'Y:=', '-2.122000mm', 'Z:=', '0.0mm'])
segs.append(['NAME:PLSegment', 'SegmentType:=', 'Line', 'StartIndex:=', 1, 'NoOfPoints:=', 2])
pts.append(['NAME:PLPoint', 'X:=', '2.402000mm', 'Y:=', '-2.260000mm', 'Z:=', '0.0mm'])
segs.append(['NAME:PLSegment', 'SegmentType:=', 'Line', 'StartIndex:=', 2, 'NoOfPoints:=', 2])
pts.append(['NAME:PLPoint', 'X:=', '2.598000mm', 'Y:=', '-2.260000mm', 'Z:=', '0.0mm'])
segs.append(['NAME:PLSegment', 'SegmentType:=', 'Line', 'StartIndex:=', 3, 'NoOfPoints:=', 2])
pts.append(['NAME:PLPoint', 'X:=', '2.598000mm', 'Y:=', '-2.122000mm', 'Z:=', '0.0mm'])
segs.append(['NAME:PLSegment', 'SegmentType:=', 'Line', 'StartIndex:=', 4, 'NoOfPoints:=', 2])
pts.append(['NAME:PLPoint', 'X:=', '2.511000mm', 'Y:=', '-2.000000mm', 'Z:=', '0.0mm'])
segs.append(['NAME:PLSegment', 'SegmentType:=', 'Line', 'StartIndex:=', 5, 'NoOfPoints:=', 2])
pts.append(['NAME:PLPoint', 'X:=', '2.511000mm', 'Y:=', '-1.975000mm', 'Z:=', '0.0mm'])
segs.append(['NAME:PLSegment', 'SegmentType:=', 'Line', 'StartIndex:=', 6, 'NoOfPoints:=', 2])
pts.append(['NAME:PLPoint', 'X:=', '2.489000mm', 'Y:=', '-1.975000mm', 'Z:=', '0.0mm'])
segs.append(['NAME:PLSegment', 'SegmentType:=', 'Line', 'StartIndex:=', 7, 'NoOfPoints:=', 2])
pts.append(['NAME:PLPoint', 'X:=', '2.489000mm', 'Y:=', '-2.000000mm', 'Z:=', '0.0mm'])
oEditor.CreatePolyline(
    ['NAME:PolylineParameters', 'IsPolylineCovered:=', True, 'IsPolylineClosed:=', True, pts, segs],
    [
        'NAME:Attributes',
        'Name:=', 'pocket_LP_Q6_52',
        'Flags:=', '',
        'Color:=', '(255 100 100)',
        'Transparency:=', 0.0,
        'PartCoordinateSystem:=', 'Global',
        'UDMId:=', '',
        'MaterialName:=', 'vacuum',
        'SolveInside:=', True
    ]
)

# --- 4. Readout Resonators & Coupling Buses ---
# Element: bus_left_wire_Q4_0
pts = ['NAME:PolylinePoints']
segs = ['NAME:PolylineSegments']
pts.append(['NAME:PLPoint', 'X:=', '-0.250484mm', 'Y:=', '0.735000mm', 'Z:=', '0.0mm'])
segs.append(['NAME:PLSegment', 'SegmentType:=', 'Line', 'StartIndex:=', 0, 'NoOfPoints:=', 2])
pts.append(['NAME:PLPoint', 'X:=', '-0.317984mm', 'Y:=', '0.670000mm', 'Z:=', '0.0mm'])
segs.append(['NAME:PLSegment', 'SegmentType:=', 'Line', 'StartIndex:=', 1, 'NoOfPoints:=', 2])
pts.append(['NAME:PLPoint', 'X:=', '-0.425000mm', 'Y:=', '0.670000mm', 'Z:=', '0.0mm'])
segs.append(['NAME:PLSegment', 'SegmentType:=', 'Line', 'StartIndex:=', 2, 'NoOfPoints:=', 2])
pts.append(['NAME:PLPoint', 'X:=', '-0.425000mm', 'Y:=', '0.680000mm', 'Z:=', '0.0mm'])
segs.append(['NAME:PLSegment', 'SegmentType:=', 'Line', 'StartIndex:=', 3, 'NoOfPoints:=', 2])
pts.append(['NAME:PLPoint', 'X:=', '-0.322016mm', 'Y:=', '0.680000mm', 'Z:=', '0.0mm'])
segs.append(['NAME:PLSegment', 'SegmentType:=', 'Line', 'StartIndex:=', 4, 'NoOfPoints:=', 2])
pts.append(['NAME:PLPoint', 'X:=', '-0.254516mm', 'Y:=', '0.745000mm', 'Z:=', '0.0mm'])
segs.append(['NAME:PLSegment', 'SegmentType:=', 'Line', 'StartIndex:=', 5, 'NoOfPoints:=', 2])
pts.append(['NAME:PLPoint', 'X:=', '-0.227500mm', 'Y:=', '0.745000mm', 'Z:=', '0.0mm'])
segs.append(['NAME:PLSegment', 'SegmentType:=', 'Line', 'StartIndex:=', 6, 'NoOfPoints:=', 2])
pts.append(['NAME:PLPoint', 'X:=', '-0.227500mm', 'Y:=', '0.735000mm', 'Z:=', '0.0mm'])
segs.append(['NAME:PLSegment', 'SegmentType:=', 'Line', 'StartIndex:=', 7, 'NoOfPoints:=', 2])
pts.append(['NAME:PLPoint', 'X:=', '-0.250484mm', 'Y:=', '0.735000mm', 'Z:=', '0.0mm'])
oEditor.CreatePolyline(
    ['NAME:PolylineParameters', 'IsPolylineCovered:=', True, 'IsPolylineClosed:=', True, pts, segs],
    [
        'NAME:Attributes',
        'Name:=', 'bus_left_wire_Q4_0',
        'Flags:=', '',
        'Color:=', '(200 220 255)',
        'Transparency:=', 0.0,
        'PartCoordinateSystem:=', 'Global',
        'UDMId:=', '',
        'MaterialName:=', 'vacuum',
        'SolveInside:=', True
    ]
)
# Element: bus_left_wire_sub_Q4_1
pts = ['NAME:PolylinePoints']
segs = ['NAME:PolylineSegments']
pts.append(['NAME:PLPoint', 'X:=', '-0.248065mm', 'Y:=', '0.729000mm', 'Z:=', '0.0mm'])
segs.append(['NAME:PLSegment', 'SegmentType:=', 'Line', 'StartIndex:=', 0, 'NoOfPoints:=', 2])
pts.append(['NAME:PLPoint', 'X:=', '-0.315565mm', 'Y:=', '0.664000mm', 'Z:=', '0.0mm'])
segs.append(['NAME:PLSegment', 'SegmentType:=', 'Line', 'StartIndex:=', 1, 'NoOfPoints:=', 2])
pts.append(['NAME:PLPoint', 'X:=', '-0.425000mm', 'Y:=', '0.664000mm', 'Z:=', '0.0mm'])
segs.append(['NAME:PLSegment', 'SegmentType:=', 'Line', 'StartIndex:=', 2, 'NoOfPoints:=', 2])
pts.append(['NAME:PLPoint', 'X:=', '-0.425000mm', 'Y:=', '0.686000mm', 'Z:=', '0.0mm'])
segs.append(['NAME:PLSegment', 'SegmentType:=', 'Line', 'StartIndex:=', 3, 'NoOfPoints:=', 2])
pts.append(['NAME:PLPoint', 'X:=', '-0.324435mm', 'Y:=', '0.686000mm', 'Z:=', '0.0mm'])
segs.append(['NAME:PLSegment', 'SegmentType:=', 'Line', 'StartIndex:=', 4, 'NoOfPoints:=', 2])
pts.append(['NAME:PLPoint', 'X:=', '-0.256935mm', 'Y:=', '0.751000mm', 'Z:=', '0.0mm'])
segs.append(['NAME:PLSegment', 'SegmentType:=', 'Line', 'StartIndex:=', 5, 'NoOfPoints:=', 2])
pts.append(['NAME:PLPoint', 'X:=', '-0.227500mm', 'Y:=', '0.751000mm', 'Z:=', '0.0mm'])
segs.append(['NAME:PLSegment', 'SegmentType:=', 'Line', 'StartIndex:=', 6, 'NoOfPoints:=', 2])
pts.append(['NAME:PLPoint', 'X:=', '-0.227500mm', 'Y:=', '0.729000mm', 'Z:=', '0.0mm'])
segs.append(['NAME:PLSegment', 'SegmentType:=', 'Line', 'StartIndex:=', 7, 'NoOfPoints:=', 2])
pts.append(['NAME:PLPoint', 'X:=', '-0.248065mm', 'Y:=', '0.729000mm', 'Z:=', '0.0mm'])
oEditor.CreatePolyline(
    ['NAME:PolylineParameters', 'IsPolylineCovered:=', True, 'IsPolylineClosed:=', True, pts, segs],
    [
        'NAME:Attributes',
        'Name:=', 'bus_left_wire_sub_Q4_1',
        'Flags:=', '',
        'Color:=', '(255 100 100)',
        'Transparency:=', 0.0,
        'PartCoordinateSystem:=', 'Global',
        'UDMId:=', '',
        'MaterialName:=', 'vacuum',
        'SolveInside:=', True
    ]
)
# Element: bus_right_wire_Q4_2
pts = ['NAME:PolylinePoints']
segs = ['NAME:PolylineSegments']
pts.append(['NAME:PLPoint', 'X:=', '0.254516mm', 'Y:=', '0.745000mm', 'Z:=', '0.0mm'])
segs.append(['NAME:PLSegment', 'SegmentType:=', 'Line', 'StartIndex:=', 0, 'NoOfPoints:=', 2])
pts.append(['NAME:PLPoint', 'X:=', '0.322016mm', 'Y:=', '0.680000mm', 'Z:=', '0.0mm'])
segs.append(['NAME:PLSegment', 'SegmentType:=', 'Line', 'StartIndex:=', 1, 'NoOfPoints:=', 2])
pts.append(['NAME:PLPoint', 'X:=', '0.425000mm', 'Y:=', '0.680000mm', 'Z:=', '0.0mm'])
segs.append(['NAME:PLSegment', 'SegmentType:=', 'Line', 'StartIndex:=', 2, 'NoOfPoints:=', 2])
pts.append(['NAME:PLPoint', 'X:=', '0.425000mm', 'Y:=', '0.670000mm', 'Z:=', '0.0mm'])
segs.append(['NAME:PLSegment', 'SegmentType:=', 'Line', 'StartIndex:=', 3, 'NoOfPoints:=', 2])
pts.append(['NAME:PLPoint', 'X:=', '0.317984mm', 'Y:=', '0.670000mm', 'Z:=', '0.0mm'])
segs.append(['NAME:PLSegment', 'SegmentType:=', 'Line', 'StartIndex:=', 4, 'NoOfPoints:=', 2])
pts.append(['NAME:PLPoint', 'X:=', '0.250484mm', 'Y:=', '0.735000mm', 'Z:=', '0.0mm'])
segs.append(['NAME:PLSegment', 'SegmentType:=', 'Line', 'StartIndex:=', 5, 'NoOfPoints:=', 2])
pts.append(['NAME:PLPoint', 'X:=', '0.227500mm', 'Y:=', '0.735000mm', 'Z:=', '0.0mm'])
segs.append(['NAME:PLSegment', 'SegmentType:=', 'Line', 'StartIndex:=', 6, 'NoOfPoints:=', 2])
pts.append(['NAME:PLPoint', 'X:=', '0.227500mm', 'Y:=', '0.745000mm', 'Z:=', '0.0mm'])
segs.append(['NAME:PLSegment', 'SegmentType:=', 'Line', 'StartIndex:=', 7, 'NoOfPoints:=', 2])
pts.append(['NAME:PLPoint', 'X:=', '0.254516mm', 'Y:=', '0.745000mm', 'Z:=', '0.0mm'])
oEditor.CreatePolyline(
    ['NAME:PolylineParameters', 'IsPolylineCovered:=', True, 'IsPolylineClosed:=', True, pts, segs],
    [
        'NAME:Attributes',
        'Name:=', 'bus_right_wire_Q4_2',
        'Flags:=', '',
        'Color:=', '(200 220 255)',
        'Transparency:=', 0.0,
        'PartCoordinateSystem:=', 'Global',
        'UDMId:=', '',
        'MaterialName:=', 'vacuum',
        'SolveInside:=', True
    ]
)
# Element: bus_right_wire_sub_Q4_3
pts = ['NAME:PolylinePoints']
segs = ['NAME:PolylineSegments']
pts.append(['NAME:PLPoint', 'X:=', '0.256935mm', 'Y:=', '0.751000mm', 'Z:=', '0.0mm'])
segs.append(['NAME:PLSegment', 'SegmentType:=', 'Line', 'StartIndex:=', 0, 'NoOfPoints:=', 2])
pts.append(['NAME:PLPoint', 'X:=', '0.324435mm', 'Y:=', '0.686000mm', 'Z:=', '0.0mm'])
segs.append(['NAME:PLSegment', 'SegmentType:=', 'Line', 'StartIndex:=', 1, 'NoOfPoints:=', 2])
pts.append(['NAME:PLPoint', 'X:=', '0.425000mm', 'Y:=', '0.686000mm', 'Z:=', '0.0mm'])
segs.append(['NAME:PLSegment', 'SegmentType:=', 'Line', 'StartIndex:=', 2, 'NoOfPoints:=', 2])
pts.append(['NAME:PLPoint', 'X:=', '0.425000mm', 'Y:=', '0.664000mm', 'Z:=', '0.0mm'])
segs.append(['NAME:PLSegment', 'SegmentType:=', 'Line', 'StartIndex:=', 3, 'NoOfPoints:=', 2])
pts.append(['NAME:PLPoint', 'X:=', '0.315565mm', 'Y:=', '0.664000mm', 'Z:=', '0.0mm'])
segs.append(['NAME:PLSegment', 'SegmentType:=', 'Line', 'StartIndex:=', 4, 'NoOfPoints:=', 2])
pts.append(['NAME:PLPoint', 'X:=', '0.248065mm', 'Y:=', '0.729000mm', 'Z:=', '0.0mm'])
segs.append(['NAME:PLSegment', 'SegmentType:=', 'Line', 'StartIndex:=', 5, 'NoOfPoints:=', 2])
pts.append(['NAME:PLPoint', 'X:=', '0.227500mm', 'Y:=', '0.729000mm', 'Z:=', '0.0mm'])
segs.append(['NAME:PLSegment', 'SegmentType:=', 'Line', 'StartIndex:=', 6, 'NoOfPoints:=', 2])
pts.append(['NAME:PLPoint', 'X:=', '0.227500mm', 'Y:=', '0.751000mm', 'Z:=', '0.0mm'])
segs.append(['NAME:PLSegment', 'SegmentType:=', 'Line', 'StartIndex:=', 7, 'NoOfPoints:=', 2])
pts.append(['NAME:PLPoint', 'X:=', '0.256935mm', 'Y:=', '0.751000mm', 'Z:=', '0.0mm'])
oEditor.CreatePolyline(
    ['NAME:PolylineParameters', 'IsPolylineCovered:=', True, 'IsPolylineClosed:=', True, pts, segs],
    [
        'NAME:Attributes',
        'Name:=', 'bus_right_wire_sub_Q4_3',
        'Flags:=', '',
        'Color:=', '(255 100 100)',
        'Transparency:=', 0.0,
        'PartCoordinateSystem:=', 'Global',
        'UDMId:=', '',
        'MaterialName:=', 'vacuum',
        'SolveInside:=', True
    ]
)
# Element: bus_top_wire_Q0_4
pts = ['NAME:PolylinePoints']
segs = ['NAME:PolylineSegments']
pts.append(['NAME:PLPoint', 'X:=', '-2.630000mm', 'Y:=', '0.425000mm', 'Z:=', '0.0mm'])
segs.append(['NAME:PLSegment', 'SegmentType:=', 'Line', 'StartIndex:=', 0, 'NoOfPoints:=', 2])
pts.append(['NAME:PLPoint', 'X:=', '-2.620000mm', 'Y:=', '0.425000mm', 'Z:=', '0.0mm'])
segs.append(['NAME:PLSegment', 'SegmentType:=', 'Line', 'StartIndex:=', 1, 'NoOfPoints:=', 2])
pts.append(['NAME:PLPoint', 'X:=', '-2.620000mm', 'Y:=', '0.227500mm', 'Z:=', '0.0mm'])
segs.append(['NAME:PLSegment', 'SegmentType:=', 'Line', 'StartIndex:=', 2, 'NoOfPoints:=', 2])
pts.append(['NAME:PLPoint', 'X:=', '-2.630000mm', 'Y:=', '0.227500mm', 'Z:=', '0.0mm'])
segs.append(['NAME:PLSegment', 'SegmentType:=', 'Line', 'StartIndex:=', 3, 'NoOfPoints:=', 2])
pts.append(['NAME:PLPoint', 'X:=', '-2.630000mm', 'Y:=', '0.425000mm', 'Z:=', '0.0mm'])
oEditor.CreatePolyline(
    ['NAME:PolylineParameters', 'IsPolylineCovered:=', True, 'IsPolylineClosed:=', True, pts, segs],
    [
        'NAME:Attributes',
        'Name:=', 'bus_top_wire_Q0_4',
        'Flags:=', '',
        'Color:=', '(200 220 255)',
        'Transparency:=', 0.0,
        'PartCoordinateSystem:=', 'Global',
        'UDMId:=', '',
        'MaterialName:=', 'vacuum',
        'SolveInside:=', True
    ]
)
# Element: bus_top_wire_sub_Q0_5
pts = ['NAME:PolylinePoints']
segs = ['NAME:PolylineSegments']
pts.append(['NAME:PLPoint', 'X:=', '-2.636000mm', 'Y:=', '0.425000mm', 'Z:=', '0.0mm'])
segs.append(['NAME:PLSegment', 'SegmentType:=', 'Line', 'StartIndex:=', 0, 'NoOfPoints:=', 2])
pts.append(['NAME:PLPoint', 'X:=', '-2.614000mm', 'Y:=', '0.425000mm', 'Z:=', '0.0mm'])
segs.append(['NAME:PLSegment', 'SegmentType:=', 'Line', 'StartIndex:=', 1, 'NoOfPoints:=', 2])
pts.append(['NAME:PLPoint', 'X:=', '-2.614000mm', 'Y:=', '0.227500mm', 'Z:=', '0.0mm'])
segs.append(['NAME:PLSegment', 'SegmentType:=', 'Line', 'StartIndex:=', 2, 'NoOfPoints:=', 2])
pts.append(['NAME:PLPoint', 'X:=', '-2.636000mm', 'Y:=', '0.227500mm', 'Z:=', '0.0mm'])
segs.append(['NAME:PLSegment', 'SegmentType:=', 'Line', 'StartIndex:=', 3, 'NoOfPoints:=', 2])
pts.append(['NAME:PLPoint', 'X:=', '-2.636000mm', 'Y:=', '0.425000mm', 'Z:=', '0.0mm'])
oEditor.CreatePolyline(
    ['NAME:PolylineParameters', 'IsPolylineCovered:=', True, 'IsPolylineClosed:=', True, pts, segs],
    [
        'NAME:Attributes',
        'Name:=', 'bus_top_wire_sub_Q0_5',
        'Flags:=', '',
        'Color:=', '(255 100 100)',
        'Transparency:=', 0.0,
        'PartCoordinateSystem:=', 'Global',
        'UDMId:=', '',
        'MaterialName:=', 'vacuum',
        'SolveInside:=', True
    ]
)
# Element: readout_wire_Q0_6
pts = ['NAME:PolylinePoints']
segs = ['NAME:PolylineSegments']
pts.append(['NAME:PLPoint', 'X:=', '-2.370000mm', 'Y:=', '-0.425000mm', 'Z:=', '0.0mm'])
segs.append(['NAME:PLSegment', 'SegmentType:=', 'Line', 'StartIndex:=', 0, 'NoOfPoints:=', 2])
pts.append(['NAME:PLPoint', 'X:=', '-2.380000mm', 'Y:=', '-0.425000mm', 'Z:=', '0.0mm'])
segs.append(['NAME:PLSegment', 'SegmentType:=', 'Line', 'StartIndex:=', 1, 'NoOfPoints:=', 2])
pts.append(['NAME:PLPoint', 'X:=', '-2.380000mm', 'Y:=', '-0.227500mm', 'Z:=', '0.0mm'])
segs.append(['NAME:PLSegment', 'SegmentType:=', 'Line', 'StartIndex:=', 2, 'NoOfPoints:=', 2])
pts.append(['NAME:PLPoint', 'X:=', '-2.370000mm', 'Y:=', '-0.227500mm', 'Z:=', '0.0mm'])
segs.append(['NAME:PLSegment', 'SegmentType:=', 'Line', 'StartIndex:=', 3, 'NoOfPoints:=', 2])
pts.append(['NAME:PLPoint', 'X:=', '-2.370000mm', 'Y:=', '-0.425000mm', 'Z:=', '0.0mm'])
oEditor.CreatePolyline(
    ['NAME:PolylineParameters', 'IsPolylineCovered:=', True, 'IsPolylineClosed:=', True, pts, segs],
    [
        'NAME:Attributes',
        'Name:=', 'readout_wire_Q0_6',
        'Flags:=', '',
        'Color:=', '(200 220 255)',
        'Transparency:=', 0.0,
        'PartCoordinateSystem:=', 'Global',
        'UDMId:=', '',
        'MaterialName:=', 'vacuum',
        'SolveInside:=', True
    ]
)
# Element: readout_wire_sub_Q0_7
pts = ['NAME:PolylinePoints']
segs = ['NAME:PolylineSegments']
pts.append(['NAME:PLPoint', 'X:=', '-2.364000mm', 'Y:=', '-0.425000mm', 'Z:=', '0.0mm'])
segs.append(['NAME:PLSegment', 'SegmentType:=', 'Line', 'StartIndex:=', 0, 'NoOfPoints:=', 2])
pts.append(['NAME:PLPoint', 'X:=', '-2.386000mm', 'Y:=', '-0.425000mm', 'Z:=', '0.0mm'])
segs.append(['NAME:PLSegment', 'SegmentType:=', 'Line', 'StartIndex:=', 1, 'NoOfPoints:=', 2])
pts.append(['NAME:PLPoint', 'X:=', '-2.386000mm', 'Y:=', '-0.227500mm', 'Z:=', '0.0mm'])
segs.append(['NAME:PLSegment', 'SegmentType:=', 'Line', 'StartIndex:=', 2, 'NoOfPoints:=', 2])
pts.append(['NAME:PLPoint', 'X:=', '-2.364000mm', 'Y:=', '-0.227500mm', 'Z:=', '0.0mm'])
segs.append(['NAME:PLSegment', 'SegmentType:=', 'Line', 'StartIndex:=', 3, 'NoOfPoints:=', 2])
pts.append(['NAME:PLPoint', 'X:=', '-2.364000mm', 'Y:=', '-0.425000mm', 'Z:=', '0.0mm'])
oEditor.CreatePolyline(
    ['NAME:PolylineParameters', 'IsPolylineCovered:=', True, 'IsPolylineClosed:=', True, pts, segs],
    [
        'NAME:Attributes',
        'Name:=', 'readout_wire_sub_Q0_7',
        'Flags:=', '',
        'Color:=', '(255 100 100)',
        'Transparency:=', 0.0,
        'PartCoordinateSystem:=', 'Global',
        'UDMId:=', '',
        'MaterialName:=', 'vacuum',
        'SolveInside:=', True
    ]
)
# Element: bus_bot_wire_Q1_8
pts = ['NAME:PolylinePoints']
segs = ['NAME:PolylineSegments']
pts.append(['NAME:PLPoint', 'X:=', '-2.380000mm', 'Y:=', '2.225000mm', 'Z:=', '0.0mm'])
segs.append(['NAME:PLSegment', 'SegmentType:=', 'Line', 'StartIndex:=', 0, 'NoOfPoints:=', 2])
pts.append(['NAME:PLPoint', 'X:=', '-2.370000mm', 'Y:=', '2.225000mm', 'Z:=', '0.0mm'])
segs.append(['NAME:PLSegment', 'SegmentType:=', 'Line', 'StartIndex:=', 1, 'NoOfPoints:=', 2])
pts.append(['NAME:PLPoint', 'X:=', '-2.370000mm', 'Y:=', '2.027500mm', 'Z:=', '0.0mm'])
segs.append(['NAME:PLSegment', 'SegmentType:=', 'Line', 'StartIndex:=', 2, 'NoOfPoints:=', 2])
pts.append(['NAME:PLPoint', 'X:=', '-2.380000mm', 'Y:=', '2.027500mm', 'Z:=', '0.0mm'])
segs.append(['NAME:PLSegment', 'SegmentType:=', 'Line', 'StartIndex:=', 3, 'NoOfPoints:=', 2])
pts.append(['NAME:PLPoint', 'X:=', '-2.380000mm', 'Y:=', '2.225000mm', 'Z:=', '0.0mm'])
oEditor.CreatePolyline(
    ['NAME:PolylineParameters', 'IsPolylineCovered:=', True, 'IsPolylineClosed:=', True, pts, segs],
    [
        'NAME:Attributes',
        'Name:=', 'bus_bot_wire_Q1_8',
        'Flags:=', '',
        'Color:=', '(200 220 255)',
        'Transparency:=', 0.0,
        'PartCoordinateSystem:=', 'Global',
        'UDMId:=', '',
        'MaterialName:=', 'vacuum',
        'SolveInside:=', True
    ]
)
# Element: bus_bot_wire_sub_Q1_9
pts = ['NAME:PolylinePoints']
segs = ['NAME:PolylineSegments']
pts.append(['NAME:PLPoint', 'X:=', '-2.386000mm', 'Y:=', '2.225000mm', 'Z:=', '0.0mm'])
segs.append(['NAME:PLSegment', 'SegmentType:=', 'Line', 'StartIndex:=', 0, 'NoOfPoints:=', 2])
pts.append(['NAME:PLPoint', 'X:=', '-2.364000mm', 'Y:=', '2.225000mm', 'Z:=', '0.0mm'])
segs.append(['NAME:PLSegment', 'SegmentType:=', 'Line', 'StartIndex:=', 1, 'NoOfPoints:=', 2])
pts.append(['NAME:PLPoint', 'X:=', '-2.364000mm', 'Y:=', '2.027500mm', 'Z:=', '0.0mm'])
segs.append(['NAME:PLSegment', 'SegmentType:=', 'Line', 'StartIndex:=', 2, 'NoOfPoints:=', 2])
pts.append(['NAME:PLPoint', 'X:=', '-2.386000mm', 'Y:=', '2.027500mm', 'Z:=', '0.0mm'])
segs.append(['NAME:PLSegment', 'SegmentType:=', 'Line', 'StartIndex:=', 3, 'NoOfPoints:=', 2])
pts.append(['NAME:PLPoint', 'X:=', '-2.386000mm', 'Y:=', '2.225000mm', 'Z:=', '0.0mm'])
oEditor.CreatePolyline(
    ['NAME:PolylineParameters', 'IsPolylineCovered:=', True, 'IsPolylineClosed:=', True, pts, segs],
    [
        'NAME:Attributes',
        'Name:=', 'bus_bot_wire_sub_Q1_9',
        'Flags:=', '',
        'Color:=', '(255 100 100)',
        'Transparency:=', 0.0,
        'PartCoordinateSystem:=', 'Global',
        'UDMId:=', '',
        'MaterialName:=', 'vacuum',
        'SolveInside:=', True
    ]
)
# Element: bus_right_wire_Q1_10
pts = ['NAME:PolylinePoints']
segs = ['NAME:PolylineSegments']
pts.append(['NAME:PLPoint', 'X:=', '-2.370000mm', 'Y:=', '1.375000mm', 'Z:=', '0.0mm'])
segs.append(['NAME:PLSegment', 'SegmentType:=', 'Line', 'StartIndex:=', 0, 'NoOfPoints:=', 2])
pts.append(['NAME:PLPoint', 'X:=', '-2.380000mm', 'Y:=', '1.375000mm', 'Z:=', '0.0mm'])
segs.append(['NAME:PLSegment', 'SegmentType:=', 'Line', 'StartIndex:=', 1, 'NoOfPoints:=', 2])
pts.append(['NAME:PLPoint', 'X:=', '-2.380000mm', 'Y:=', '1.572500mm', 'Z:=', '0.0mm'])
segs.append(['NAME:PLSegment', 'SegmentType:=', 'Line', 'StartIndex:=', 2, 'NoOfPoints:=', 2])
pts.append(['NAME:PLPoint', 'X:=', '-2.370000mm', 'Y:=', '1.572500mm', 'Z:=', '0.0mm'])
segs.append(['NAME:PLSegment', 'SegmentType:=', 'Line', 'StartIndex:=', 3, 'NoOfPoints:=', 2])
pts.append(['NAME:PLPoint', 'X:=', '-2.370000mm', 'Y:=', '1.375000mm', 'Z:=', '0.0mm'])
oEditor.CreatePolyline(
    ['NAME:PolylineParameters', 'IsPolylineCovered:=', True, 'IsPolylineClosed:=', True, pts, segs],
    [
        'NAME:Attributes',
        'Name:=', 'bus_right_wire_Q1_10',
        'Flags:=', '',
        'Color:=', '(200 220 255)',
        'Transparency:=', 0.0,
        'PartCoordinateSystem:=', 'Global',
        'UDMId:=', '',
        'MaterialName:=', 'vacuum',
        'SolveInside:=', True
    ]
)
# Element: bus_right_wire_sub_Q1_11
pts = ['NAME:PolylinePoints']
segs = ['NAME:PolylineSegments']
pts.append(['NAME:PLPoint', 'X:=', '-2.364000mm', 'Y:=', '1.375000mm', 'Z:=', '0.0mm'])
segs.append(['NAME:PLSegment', 'SegmentType:=', 'Line', 'StartIndex:=', 0, 'NoOfPoints:=', 2])
pts.append(['NAME:PLPoint', 'X:=', '-2.386000mm', 'Y:=', '1.375000mm', 'Z:=', '0.0mm'])
segs.append(['NAME:PLSegment', 'SegmentType:=', 'Line', 'StartIndex:=', 1, 'NoOfPoints:=', 2])
pts.append(['NAME:PLPoint', 'X:=', '-2.386000mm', 'Y:=', '1.572500mm', 'Z:=', '0.0mm'])
segs.append(['NAME:PLSegment', 'SegmentType:=', 'Line', 'StartIndex:=', 2, 'NoOfPoints:=', 2])
pts.append(['NAME:PLPoint', 'X:=', '-2.364000mm', 'Y:=', '1.572500mm', 'Z:=', '0.0mm'])
segs.append(['NAME:PLSegment', 'SegmentType:=', 'Line', 'StartIndex:=', 3, 'NoOfPoints:=', 2])
pts.append(['NAME:PLPoint', 'X:=', '-2.364000mm', 'Y:=', '1.375000mm', 'Z:=', '0.0mm'])
oEditor.CreatePolyline(
    ['NAME:PolylineParameters', 'IsPolylineCovered:=', True, 'IsPolylineClosed:=', True, pts, segs],
    [
        'NAME:Attributes',
        'Name:=', 'bus_right_wire_sub_Q1_11',
        'Flags:=', '',
        'Color:=', '(255 100 100)',
        'Transparency:=', 0.0,
        'PartCoordinateSystem:=', 'Global',
        'UDMId:=', '',
        'MaterialName:=', 'vacuum',
        'SolveInside:=', True
    ]
)
# Element: readout_wire_Q1_12
pts = ['NAME:PolylinePoints']
segs = ['NAME:PolylineSegments']
pts.append(['NAME:PLPoint', 'X:=', '-2.630000mm', 'Y:=', '2.225000mm', 'Z:=', '0.0mm'])
segs.append(['NAME:PLSegment', 'SegmentType:=', 'Line', 'StartIndex:=', 0, 'NoOfPoints:=', 2])
pts.append(['NAME:PLPoint', 'X:=', '-2.620000mm', 'Y:=', '2.225000mm', 'Z:=', '0.0mm'])
segs.append(['NAME:PLSegment', 'SegmentType:=', 'Line', 'StartIndex:=', 1, 'NoOfPoints:=', 2])
pts.append(['NAME:PLPoint', 'X:=', '-2.620000mm', 'Y:=', '2.027500mm', 'Z:=', '0.0mm'])
segs.append(['NAME:PLSegment', 'SegmentType:=', 'Line', 'StartIndex:=', 2, 'NoOfPoints:=', 2])
pts.append(['NAME:PLPoint', 'X:=', '-2.630000mm', 'Y:=', '2.027500mm', 'Z:=', '0.0mm'])
segs.append(['NAME:PLSegment', 'SegmentType:=', 'Line', 'StartIndex:=', 3, 'NoOfPoints:=', 2])
pts.append(['NAME:PLPoint', 'X:=', '-2.630000mm', 'Y:=', '2.225000mm', 'Z:=', '0.0mm'])
oEditor.CreatePolyline(
    ['NAME:PolylineParameters', 'IsPolylineCovered:=', True, 'IsPolylineClosed:=', True, pts, segs],
    [
        'NAME:Attributes',
        'Name:=', 'readout_wire_Q1_12',
        'Flags:=', '',
        'Color:=', '(200 220 255)',
        'Transparency:=', 0.0,
        'PartCoordinateSystem:=', 'Global',
        'UDMId:=', '',
        'MaterialName:=', 'vacuum',
        'SolveInside:=', True
    ]
)
# Element: readout_wire_sub_Q1_13
pts = ['NAME:PolylinePoints']
segs = ['NAME:PolylineSegments']
pts.append(['NAME:PLPoint', 'X:=', '-2.636000mm', 'Y:=', '2.225000mm', 'Z:=', '0.0mm'])
segs.append(['NAME:PLSegment', 'SegmentType:=', 'Line', 'StartIndex:=', 0, 'NoOfPoints:=', 2])
pts.append(['NAME:PLPoint', 'X:=', '-2.614000mm', 'Y:=', '2.225000mm', 'Z:=', '0.0mm'])
segs.append(['NAME:PLSegment', 'SegmentType:=', 'Line', 'StartIndex:=', 1, 'NoOfPoints:=', 2])
pts.append(['NAME:PLPoint', 'X:=', '-2.614000mm', 'Y:=', '2.027500mm', 'Z:=', '0.0mm'])
segs.append(['NAME:PLSegment', 'SegmentType:=', 'Line', 'StartIndex:=', 2, 'NoOfPoints:=', 2])
pts.append(['NAME:PLPoint', 'X:=', '-2.636000mm', 'Y:=', '2.027500mm', 'Z:=', '0.0mm'])
segs.append(['NAME:PLSegment', 'SegmentType:=', 'Line', 'StartIndex:=', 3, 'NoOfPoints:=', 2])
pts.append(['NAME:PLPoint', 'X:=', '-2.636000mm', 'Y:=', '2.225000mm', 'Z:=', '0.0mm'])
oEditor.CreatePolyline(
    ['NAME:PolylineParameters', 'IsPolylineCovered:=', True, 'IsPolylineClosed:=', True, pts, segs],
    [
        'NAME:Attributes',
        'Name:=', 'readout_wire_sub_Q1_13',
        'Flags:=', '',
        'Color:=', '(255 100 100)',
        'Transparency:=', 0.0,
        'PartCoordinateSystem:=', 'Global',
        'UDMId:=', '',
        'MaterialName:=', 'vacuum',
        'SolveInside:=', True
    ]
)
# Element: bus_left_wire_Q3_14
pts = ['NAME:PolylinePoints']
segs = ['NAME:PolylineSegments']
pts.append(['NAME:PLPoint', 'X:=', '-1.775000mm', 'Y:=', '0.990000mm', 'Z:=', '0.0mm'])
segs.append(['NAME:PLSegment', 'SegmentType:=', 'Line', 'StartIndex:=', 0, 'NoOfPoints:=', 2])
pts.append(['NAME:PLPoint', 'X:=', '-1.775000mm', 'Y:=', '1.000000mm', 'Z:=', '0.0mm'])
segs.append(['NAME:PLSegment', 'SegmentType:=', 'Line', 'StartIndex:=', 1, 'NoOfPoints:=', 2])
pts.append(['NAME:PLPoint', 'X:=', '-1.577500mm', 'Y:=', '1.000000mm', 'Z:=', '0.0mm'])
segs.append(['NAME:PLSegment', 'SegmentType:=', 'Line', 'StartIndex:=', 2, 'NoOfPoints:=', 2])
pts.append(['NAME:PLPoint', 'X:=', '-1.577500mm', 'Y:=', '0.990000mm', 'Z:=', '0.0mm'])
segs.append(['NAME:PLSegment', 'SegmentType:=', 'Line', 'StartIndex:=', 3, 'NoOfPoints:=', 2])
pts.append(['NAME:PLPoint', 'X:=', '-1.775000mm', 'Y:=', '0.990000mm', 'Z:=', '0.0mm'])
oEditor.CreatePolyline(
    ['NAME:PolylineParameters', 'IsPolylineCovered:=', True, 'IsPolylineClosed:=', True, pts, segs],
    [
        'NAME:Attributes',
        'Name:=', 'bus_left_wire_Q3_14',
        'Flags:=', '',
        'Color:=', '(200 220 255)',
        'Transparency:=', 0.0,
        'PartCoordinateSystem:=', 'Global',
        'UDMId:=', '',
        'MaterialName:=', 'vacuum',
        'SolveInside:=', True
    ]
)
# Element: bus_left_wire_sub_Q3_15
pts = ['NAME:PolylinePoints']
segs = ['NAME:PolylineSegments']
pts.append(['NAME:PLPoint', 'X:=', '-1.775000mm', 'Y:=', '0.984000mm', 'Z:=', '0.0mm'])
segs.append(['NAME:PLSegment', 'SegmentType:=', 'Line', 'StartIndex:=', 0, 'NoOfPoints:=', 2])
pts.append(['NAME:PLPoint', 'X:=', '-1.775000mm', 'Y:=', '1.006000mm', 'Z:=', '0.0mm'])
segs.append(['NAME:PLSegment', 'SegmentType:=', 'Line', 'StartIndex:=', 1, 'NoOfPoints:=', 2])
pts.append(['NAME:PLPoint', 'X:=', '-1.577500mm', 'Y:=', '1.006000mm', 'Z:=', '0.0mm'])
segs.append(['NAME:PLSegment', 'SegmentType:=', 'Line', 'StartIndex:=', 2, 'NoOfPoints:=', 2])
pts.append(['NAME:PLPoint', 'X:=', '-1.577500mm', 'Y:=', '0.984000mm', 'Z:=', '0.0mm'])
segs.append(['NAME:PLSegment', 'SegmentType:=', 'Line', 'StartIndex:=', 3, 'NoOfPoints:=', 2])
pts.append(['NAME:PLPoint', 'X:=', '-1.775000mm', 'Y:=', '0.984000mm', 'Z:=', '0.0mm'])
oEditor.CreatePolyline(
    ['NAME:PolylineParameters', 'IsPolylineCovered:=', True, 'IsPolylineClosed:=', True, pts, segs],
    [
        'NAME:Attributes',
        'Name:=', 'bus_left_wire_sub_Q3_15',
        'Flags:=', '',
        'Color:=', '(255 100 100)',
        'Transparency:=', 0.0,
        'PartCoordinateSystem:=', 'Global',
        'UDMId:=', '',
        'MaterialName:=', 'vacuum',
        'SolveInside:=', True
    ]
)
# Element: bus_right_wire_Q3_16
pts = ['NAME:PolylinePoints']
segs = ['NAME:PolylineSegments']
pts.append(['NAME:PLPoint', 'X:=', '-0.925000mm', 'Y:=', '0.750000mm', 'Z:=', '0.0mm'])
segs.append(['NAME:PLSegment', 'SegmentType:=', 'Line', 'StartIndex:=', 0, 'NoOfPoints:=', 2])
pts.append(['NAME:PLPoint', 'X:=', '-0.925000mm', 'Y:=', '0.740000mm', 'Z:=', '0.0mm'])
segs.append(['NAME:PLSegment', 'SegmentType:=', 'Line', 'StartIndex:=', 1, 'NoOfPoints:=', 2])
pts.append(['NAME:PLPoint', 'X:=', '-1.122500mm', 'Y:=', '0.740000mm', 'Z:=', '0.0mm'])
segs.append(['NAME:PLSegment', 'SegmentType:=', 'Line', 'StartIndex:=', 2, 'NoOfPoints:=', 2])
pts.append(['NAME:PLPoint', 'X:=', '-1.122500mm', 'Y:=', '0.750000mm', 'Z:=', '0.0mm'])
segs.append(['NAME:PLSegment', 'SegmentType:=', 'Line', 'StartIndex:=', 3, 'NoOfPoints:=', 2])
pts.append(['NAME:PLPoint', 'X:=', '-0.925000mm', 'Y:=', '0.750000mm', 'Z:=', '0.0mm'])
oEditor.CreatePolyline(
    ['NAME:PolylineParameters', 'IsPolylineCovered:=', True, 'IsPolylineClosed:=', True, pts, segs],
    [
        'NAME:Attributes',
        'Name:=', 'bus_right_wire_Q3_16',
        'Flags:=', '',
        'Color:=', '(200 220 255)',
        'Transparency:=', 0.0,
        'PartCoordinateSystem:=', 'Global',
        'UDMId:=', '',
        'MaterialName:=', 'vacuum',
        'SolveInside:=', True
    ]
)
# Element: bus_right_wire_sub_Q3_17
pts = ['NAME:PolylinePoints']
segs = ['NAME:PolylineSegments']
pts.append(['NAME:PLPoint', 'X:=', '-0.925000mm', 'Y:=', '0.756000mm', 'Z:=', '0.0mm'])
segs.append(['NAME:PLSegment', 'SegmentType:=', 'Line', 'StartIndex:=', 0, 'NoOfPoints:=', 2])
pts.append(['NAME:PLPoint', 'X:=', '-0.925000mm', 'Y:=', '0.734000mm', 'Z:=', '0.0mm'])
segs.append(['NAME:PLSegment', 'SegmentType:=', 'Line', 'StartIndex:=', 1, 'NoOfPoints:=', 2])
pts.append(['NAME:PLPoint', 'X:=', '-1.122500mm', 'Y:=', '0.734000mm', 'Z:=', '0.0mm'])
segs.append(['NAME:PLSegment', 'SegmentType:=', 'Line', 'StartIndex:=', 2, 'NoOfPoints:=', 2])
pts.append(['NAME:PLPoint', 'X:=', '-1.122500mm', 'Y:=', '0.756000mm', 'Z:=', '0.0mm'])
segs.append(['NAME:PLSegment', 'SegmentType:=', 'Line', 'StartIndex:=', 3, 'NoOfPoints:=', 2])
pts.append(['NAME:PLPoint', 'X:=', '-0.925000mm', 'Y:=', '0.756000mm', 'Z:=', '0.0mm'])
oEditor.CreatePolyline(
    ['NAME:PolylineParameters', 'IsPolylineCovered:=', True, 'IsPolylineClosed:=', True, pts, segs],
    [
        'NAME:Attributes',
        'Name:=', 'bus_right_wire_sub_Q3_17',
        'Flags:=', '',
        'Color:=', '(255 100 100)',
        'Transparency:=', 0.0,
        'PartCoordinateSystem:=', 'Global',
        'UDMId:=', '',
        'MaterialName:=', 'vacuum',
        'SolveInside:=', True
    ]
)
# Element: readout_wire_Q3_18
pts = ['NAME:PolylinePoints']
segs = ['NAME:PolylineSegments']
pts.append(['NAME:PLPoint', 'X:=', '-0.925000mm', 'Y:=', '1.000000mm', 'Z:=', '0.0mm'])
segs.append(['NAME:PLSegment', 'SegmentType:=', 'Line', 'StartIndex:=', 0, 'NoOfPoints:=', 2])
pts.append(['NAME:PLPoint', 'X:=', '-0.925000mm', 'Y:=', '0.990000mm', 'Z:=', '0.0mm'])
segs.append(['NAME:PLSegment', 'SegmentType:=', 'Line', 'StartIndex:=', 1, 'NoOfPoints:=', 2])
pts.append(['NAME:PLPoint', 'X:=', '-1.122500mm', 'Y:=', '0.990000mm', 'Z:=', '0.0mm'])
segs.append(['NAME:PLSegment', 'SegmentType:=', 'Line', 'StartIndex:=', 2, 'NoOfPoints:=', 2])
pts.append(['NAME:PLPoint', 'X:=', '-1.122500mm', 'Y:=', '1.000000mm', 'Z:=', '0.0mm'])
segs.append(['NAME:PLSegment', 'SegmentType:=', 'Line', 'StartIndex:=', 3, 'NoOfPoints:=', 2])
pts.append(['NAME:PLPoint', 'X:=', '-0.925000mm', 'Y:=', '1.000000mm', 'Z:=', '0.0mm'])
oEditor.CreatePolyline(
    ['NAME:PolylineParameters', 'IsPolylineCovered:=', True, 'IsPolylineClosed:=', True, pts, segs],
    [
        'NAME:Attributes',
        'Name:=', 'readout_wire_Q3_18',
        'Flags:=', '',
        'Color:=', '(200 220 255)',
        'Transparency:=', 0.0,
        'PartCoordinateSystem:=', 'Global',
        'UDMId:=', '',
        'MaterialName:=', 'vacuum',
        'SolveInside:=', True
    ]
)
# Element: readout_wire_sub_Q3_19
pts = ['NAME:PolylinePoints']
segs = ['NAME:PolylineSegments']
pts.append(['NAME:PLPoint', 'X:=', '-0.925000mm', 'Y:=', '1.006000mm', 'Z:=', '0.0mm'])
segs.append(['NAME:PLSegment', 'SegmentType:=', 'Line', 'StartIndex:=', 0, 'NoOfPoints:=', 2])
pts.append(['NAME:PLPoint', 'X:=', '-0.925000mm', 'Y:=', '0.984000mm', 'Z:=', '0.0mm'])
segs.append(['NAME:PLSegment', 'SegmentType:=', 'Line', 'StartIndex:=', 1, 'NoOfPoints:=', 2])
pts.append(['NAME:PLPoint', 'X:=', '-1.122500mm', 'Y:=', '0.984000mm', 'Z:=', '0.0mm'])
segs.append(['NAME:PLSegment', 'SegmentType:=', 'Line', 'StartIndex:=', 2, 'NoOfPoints:=', 2])
pts.append(['NAME:PLPoint', 'X:=', '-1.122500mm', 'Y:=', '1.006000mm', 'Z:=', '0.0mm'])
segs.append(['NAME:PLSegment', 'SegmentType:=', 'Line', 'StartIndex:=', 3, 'NoOfPoints:=', 2])
pts.append(['NAME:PLPoint', 'X:=', '-0.925000mm', 'Y:=', '1.006000mm', 'Z:=', '0.0mm'])
oEditor.CreatePolyline(
    ['NAME:PolylineParameters', 'IsPolylineCovered:=', True, 'IsPolylineClosed:=', True, pts, segs],
    [
        'NAME:Attributes',
        'Name:=', 'readout_wire_sub_Q3_19',
        'Flags:=', '',
        'Color:=', '(255 100 100)',
        'Transparency:=', 0.0,
        'PartCoordinateSystem:=', 'Global',
        'UDMId:=', '',
        'MaterialName:=', 'vacuum',
        'SolveInside:=', True
    ]
)
# Element: bus_left_wire_Q5_20
pts = ['NAME:PolylinePoints']
segs = ['NAME:PolylineSegments']
pts.append(['NAME:PLPoint', 'X:=', '0.925000mm', 'Y:=', '0.740000mm', 'Z:=', '0.0mm'])
segs.append(['NAME:PLSegment', 'SegmentType:=', 'Line', 'StartIndex:=', 0, 'NoOfPoints:=', 2])
pts.append(['NAME:PLPoint', 'X:=', '0.925000mm', 'Y:=', '0.750000mm', 'Z:=', '0.0mm'])
segs.append(['NAME:PLSegment', 'SegmentType:=', 'Line', 'StartIndex:=', 1, 'NoOfPoints:=', 2])
pts.append(['NAME:PLPoint', 'X:=', '1.122500mm', 'Y:=', '0.750000mm', 'Z:=', '0.0mm'])
segs.append(['NAME:PLSegment', 'SegmentType:=', 'Line', 'StartIndex:=', 2, 'NoOfPoints:=', 2])
pts.append(['NAME:PLPoint', 'X:=', '1.122500mm', 'Y:=', '0.740000mm', 'Z:=', '0.0mm'])
segs.append(['NAME:PLSegment', 'SegmentType:=', 'Line', 'StartIndex:=', 3, 'NoOfPoints:=', 2])
pts.append(['NAME:PLPoint', 'X:=', '0.925000mm', 'Y:=', '0.740000mm', 'Z:=', '0.0mm'])
oEditor.CreatePolyline(
    ['NAME:PolylineParameters', 'IsPolylineCovered:=', True, 'IsPolylineClosed:=', True, pts, segs],
    [
        'NAME:Attributes',
        'Name:=', 'bus_left_wire_Q5_20',
        'Flags:=', '',
        'Color:=', '(200 220 255)',
        'Transparency:=', 0.0,
        'PartCoordinateSystem:=', 'Global',
        'UDMId:=', '',
        'MaterialName:=', 'vacuum',
        'SolveInside:=', True
    ]
)
# Element: bus_left_wire_sub_Q5_21
pts = ['NAME:PolylinePoints']
segs = ['NAME:PolylineSegments']
pts.append(['NAME:PLPoint', 'X:=', '0.925000mm', 'Y:=', '0.734000mm', 'Z:=', '0.0mm'])
segs.append(['NAME:PLSegment', 'SegmentType:=', 'Line', 'StartIndex:=', 0, 'NoOfPoints:=', 2])
pts.append(['NAME:PLPoint', 'X:=', '0.925000mm', 'Y:=', '0.756000mm', 'Z:=', '0.0mm'])
segs.append(['NAME:PLSegment', 'SegmentType:=', 'Line', 'StartIndex:=', 1, 'NoOfPoints:=', 2])
pts.append(['NAME:PLPoint', 'X:=', '1.122500mm', 'Y:=', '0.756000mm', 'Z:=', '0.0mm'])
segs.append(['NAME:PLSegment', 'SegmentType:=', 'Line', 'StartIndex:=', 2, 'NoOfPoints:=', 2])
pts.append(['NAME:PLPoint', 'X:=', '1.122500mm', 'Y:=', '0.734000mm', 'Z:=', '0.0mm'])
segs.append(['NAME:PLSegment', 'SegmentType:=', 'Line', 'StartIndex:=', 3, 'NoOfPoints:=', 2])
pts.append(['NAME:PLPoint', 'X:=', '0.925000mm', 'Y:=', '0.734000mm', 'Z:=', '0.0mm'])
oEditor.CreatePolyline(
    ['NAME:PolylineParameters', 'IsPolylineCovered:=', True, 'IsPolylineClosed:=', True, pts, segs],
    [
        'NAME:Attributes',
        'Name:=', 'bus_left_wire_sub_Q5_21',
        'Flags:=', '',
        'Color:=', '(255 100 100)',
        'Transparency:=', 0.0,
        'PartCoordinateSystem:=', 'Global',
        'UDMId:=', '',
        'MaterialName:=', 'vacuum',
        'SolveInside:=', True
    ]
)
# Element: bus_right_wire_Q5_22
pts = ['NAME:PolylinePoints']
segs = ['NAME:PolylineSegments']
pts.append(['NAME:PLPoint', 'X:=', '1.775000mm', 'Y:=', '1.000000mm', 'Z:=', '0.0mm'])
segs.append(['NAME:PLSegment', 'SegmentType:=', 'Line', 'StartIndex:=', 0, 'NoOfPoints:=', 2])
pts.append(['NAME:PLPoint', 'X:=', '1.775000mm', 'Y:=', '0.990000mm', 'Z:=', '0.0mm'])
segs.append(['NAME:PLSegment', 'SegmentType:=', 'Line', 'StartIndex:=', 1, 'NoOfPoints:=', 2])
pts.append(['NAME:PLPoint', 'X:=', '1.577500mm', 'Y:=', '0.990000mm', 'Z:=', '0.0mm'])
segs.append(['NAME:PLSegment', 'SegmentType:=', 'Line', 'StartIndex:=', 2, 'NoOfPoints:=', 2])
pts.append(['NAME:PLPoint', 'X:=', '1.577500mm', 'Y:=', '1.000000mm', 'Z:=', '0.0mm'])
segs.append(['NAME:PLSegment', 'SegmentType:=', 'Line', 'StartIndex:=', 3, 'NoOfPoints:=', 2])
pts.append(['NAME:PLPoint', 'X:=', '1.775000mm', 'Y:=', '1.000000mm', 'Z:=', '0.0mm'])
oEditor.CreatePolyline(
    ['NAME:PolylineParameters', 'IsPolylineCovered:=', True, 'IsPolylineClosed:=', True, pts, segs],
    [
        'NAME:Attributes',
        'Name:=', 'bus_right_wire_Q5_22',
        'Flags:=', '',
        'Color:=', '(200 220 255)',
        'Transparency:=', 0.0,
        'PartCoordinateSystem:=', 'Global',
        'UDMId:=', '',
        'MaterialName:=', 'vacuum',
        'SolveInside:=', True
    ]
)
# Element: bus_right_wire_sub_Q5_23
pts = ['NAME:PolylinePoints']
segs = ['NAME:PolylineSegments']
pts.append(['NAME:PLPoint', 'X:=', '1.775000mm', 'Y:=', '1.006000mm', 'Z:=', '0.0mm'])
segs.append(['NAME:PLSegment', 'SegmentType:=', 'Line', 'StartIndex:=', 0, 'NoOfPoints:=', 2])
pts.append(['NAME:PLPoint', 'X:=', '1.775000mm', 'Y:=', '0.984000mm', 'Z:=', '0.0mm'])
segs.append(['NAME:PLSegment', 'SegmentType:=', 'Line', 'StartIndex:=', 1, 'NoOfPoints:=', 2])
pts.append(['NAME:PLPoint', 'X:=', '1.577500mm', 'Y:=', '0.984000mm', 'Z:=', '0.0mm'])
segs.append(['NAME:PLSegment', 'SegmentType:=', 'Line', 'StartIndex:=', 2, 'NoOfPoints:=', 2])
pts.append(['NAME:PLPoint', 'X:=', '1.577500mm', 'Y:=', '1.006000mm', 'Z:=', '0.0mm'])
segs.append(['NAME:PLSegment', 'SegmentType:=', 'Line', 'StartIndex:=', 3, 'NoOfPoints:=', 2])
pts.append(['NAME:PLPoint', 'X:=', '1.775000mm', 'Y:=', '1.006000mm', 'Z:=', '0.0mm'])
oEditor.CreatePolyline(
    ['NAME:PolylineParameters', 'IsPolylineCovered:=', True, 'IsPolylineClosed:=', True, pts, segs],
    [
        'NAME:Attributes',
        'Name:=', 'bus_right_wire_sub_Q5_23',
        'Flags:=', '',
        'Color:=', '(255 100 100)',
        'Transparency:=', 0.0,
        'PartCoordinateSystem:=', 'Global',
        'UDMId:=', '',
        'MaterialName:=', 'vacuum',
        'SolveInside:=', True
    ]
)
# Element: readout_wire_Q5_24
pts = ['NAME:PolylinePoints']
segs = ['NAME:PolylineSegments']
pts.append(['NAME:PLPoint', 'X:=', '0.925000mm', 'Y:=', '0.990000mm', 'Z:=', '0.0mm'])
segs.append(['NAME:PLSegment', 'SegmentType:=', 'Line', 'StartIndex:=', 0, 'NoOfPoints:=', 2])
pts.append(['NAME:PLPoint', 'X:=', '0.925000mm', 'Y:=', '1.000000mm', 'Z:=', '0.0mm'])
segs.append(['NAME:PLSegment', 'SegmentType:=', 'Line', 'StartIndex:=', 1, 'NoOfPoints:=', 2])
pts.append(['NAME:PLPoint', 'X:=', '1.122500mm', 'Y:=', '1.000000mm', 'Z:=', '0.0mm'])
segs.append(['NAME:PLSegment', 'SegmentType:=', 'Line', 'StartIndex:=', 2, 'NoOfPoints:=', 2])
pts.append(['NAME:PLPoint', 'X:=', '1.122500mm', 'Y:=', '0.990000mm', 'Z:=', '0.0mm'])
segs.append(['NAME:PLSegment', 'SegmentType:=', 'Line', 'StartIndex:=', 3, 'NoOfPoints:=', 2])
pts.append(['NAME:PLPoint', 'X:=', '0.925000mm', 'Y:=', '0.990000mm', 'Z:=', '0.0mm'])
oEditor.CreatePolyline(
    ['NAME:PolylineParameters', 'IsPolylineCovered:=', True, 'IsPolylineClosed:=', True, pts, segs],
    [
        'NAME:Attributes',
        'Name:=', 'readout_wire_Q5_24',
        'Flags:=', '',
        'Color:=', '(200 220 255)',
        'Transparency:=', 0.0,
        'PartCoordinateSystem:=', 'Global',
        'UDMId:=', '',
        'MaterialName:=', 'vacuum',
        'SolveInside:=', True
    ]
)
# Element: readout_wire_sub_Q5_25
pts = ['NAME:PolylinePoints']
segs = ['NAME:PolylineSegments']
pts.append(['NAME:PLPoint', 'X:=', '0.925000mm', 'Y:=', '0.984000mm', 'Z:=', '0.0mm'])
segs.append(['NAME:PLSegment', 'SegmentType:=', 'Line', 'StartIndex:=', 0, 'NoOfPoints:=', 2])
pts.append(['NAME:PLPoint', 'X:=', '0.925000mm', 'Y:=', '1.006000mm', 'Z:=', '0.0mm'])
segs.append(['NAME:PLSegment', 'SegmentType:=', 'Line', 'StartIndex:=', 1, 'NoOfPoints:=', 2])
pts.append(['NAME:PLPoint', 'X:=', '1.122500mm', 'Y:=', '1.006000mm', 'Z:=', '0.0mm'])
segs.append(['NAME:PLSegment', 'SegmentType:=', 'Line', 'StartIndex:=', 2, 'NoOfPoints:=', 2])
pts.append(['NAME:PLPoint', 'X:=', '1.122500mm', 'Y:=', '0.984000mm', 'Z:=', '0.0mm'])
segs.append(['NAME:PLSegment', 'SegmentType:=', 'Line', 'StartIndex:=', 3, 'NoOfPoints:=', 2])
pts.append(['NAME:PLPoint', 'X:=', '0.925000mm', 'Y:=', '0.984000mm', 'Z:=', '0.0mm'])
oEditor.CreatePolyline(
    ['NAME:PolylineParameters', 'IsPolylineCovered:=', True, 'IsPolylineClosed:=', True, pts, segs],
    [
        'NAME:Attributes',
        'Name:=', 'readout_wire_sub_Q5_25',
        'Flags:=', '',
        'Color:=', '(255 100 100)',
        'Transparency:=', 0.0,
        'PartCoordinateSystem:=', 'Global',
        'UDMId:=', '',
        'MaterialName:=', 'vacuum',
        'SolveInside:=', True
    ]
)
# Element: bus_bot_wire_Q2_26
pts = ['NAME:PolylinePoints']
segs = ['NAME:PolylineSegments']
pts.append(['NAME:PLPoint', 'X:=', '2.620000mm', 'Y:=', '2.225000mm', 'Z:=', '0.0mm'])
segs.append(['NAME:PLSegment', 'SegmentType:=', 'Line', 'StartIndex:=', 0, 'NoOfPoints:=', 2])
pts.append(['NAME:PLPoint', 'X:=', '2.630000mm', 'Y:=', '2.225000mm', 'Z:=', '0.0mm'])
segs.append(['NAME:PLSegment', 'SegmentType:=', 'Line', 'StartIndex:=', 1, 'NoOfPoints:=', 2])
pts.append(['NAME:PLPoint', 'X:=', '2.630000mm', 'Y:=', '2.027500mm', 'Z:=', '0.0mm'])
segs.append(['NAME:PLSegment', 'SegmentType:=', 'Line', 'StartIndex:=', 2, 'NoOfPoints:=', 2])
pts.append(['NAME:PLPoint', 'X:=', '2.620000mm', 'Y:=', '2.027500mm', 'Z:=', '0.0mm'])
segs.append(['NAME:PLSegment', 'SegmentType:=', 'Line', 'StartIndex:=', 3, 'NoOfPoints:=', 2])
pts.append(['NAME:PLPoint', 'X:=', '2.620000mm', 'Y:=', '2.225000mm', 'Z:=', '0.0mm'])
oEditor.CreatePolyline(
    ['NAME:PolylineParameters', 'IsPolylineCovered:=', True, 'IsPolylineClosed:=', True, pts, segs],
    [
        'NAME:Attributes',
        'Name:=', 'bus_bot_wire_Q2_26',
        'Flags:=', '',
        'Color:=', '(200 220 255)',
        'Transparency:=', 0.0,
        'PartCoordinateSystem:=', 'Global',
        'UDMId:=', '',
        'MaterialName:=', 'vacuum',
        'SolveInside:=', True
    ]
)
# Element: bus_bot_wire_sub_Q2_27
pts = ['NAME:PolylinePoints']
segs = ['NAME:PolylineSegments']
pts.append(['NAME:PLPoint', 'X:=', '2.614000mm', 'Y:=', '2.225000mm', 'Z:=', '0.0mm'])
segs.append(['NAME:PLSegment', 'SegmentType:=', 'Line', 'StartIndex:=', 0, 'NoOfPoints:=', 2])
pts.append(['NAME:PLPoint', 'X:=', '2.636000mm', 'Y:=', '2.225000mm', 'Z:=', '0.0mm'])
segs.append(['NAME:PLSegment', 'SegmentType:=', 'Line', 'StartIndex:=', 1, 'NoOfPoints:=', 2])
pts.append(['NAME:PLPoint', 'X:=', '2.636000mm', 'Y:=', '2.027500mm', 'Z:=', '0.0mm'])
segs.append(['NAME:PLSegment', 'SegmentType:=', 'Line', 'StartIndex:=', 2, 'NoOfPoints:=', 2])
pts.append(['NAME:PLPoint', 'X:=', '2.614000mm', 'Y:=', '2.027500mm', 'Z:=', '0.0mm'])
segs.append(['NAME:PLSegment', 'SegmentType:=', 'Line', 'StartIndex:=', 3, 'NoOfPoints:=', 2])
pts.append(['NAME:PLPoint', 'X:=', '2.614000mm', 'Y:=', '2.225000mm', 'Z:=', '0.0mm'])
oEditor.CreatePolyline(
    ['NAME:PolylineParameters', 'IsPolylineCovered:=', True, 'IsPolylineClosed:=', True, pts, segs],
    [
        'NAME:Attributes',
        'Name:=', 'bus_bot_wire_sub_Q2_27',
        'Flags:=', '',
        'Color:=', '(255 100 100)',
        'Transparency:=', 0.0,
        'PartCoordinateSystem:=', 'Global',
        'UDMId:=', '',
        'MaterialName:=', 'vacuum',
        'SolveInside:=', True
    ]
)
# Element: bus_left_wire_Q2_28
pts = ['NAME:PolylinePoints']
segs = ['NAME:PolylineSegments']
pts.append(['NAME:PLPoint', 'X:=', '2.630000mm', 'Y:=', '1.375000mm', 'Z:=', '0.0mm'])
segs.append(['NAME:PLSegment', 'SegmentType:=', 'Line', 'StartIndex:=', 0, 'NoOfPoints:=', 2])
pts.append(['NAME:PLPoint', 'X:=', '2.620000mm', 'Y:=', '1.375000mm', 'Z:=', '0.0mm'])
segs.append(['NAME:PLSegment', 'SegmentType:=', 'Line', 'StartIndex:=', 1, 'NoOfPoints:=', 2])
pts.append(['NAME:PLPoint', 'X:=', '2.620000mm', 'Y:=', '1.572500mm', 'Z:=', '0.0mm'])
segs.append(['NAME:PLSegment', 'SegmentType:=', 'Line', 'StartIndex:=', 2, 'NoOfPoints:=', 2])
pts.append(['NAME:PLPoint', 'X:=', '2.630000mm', 'Y:=', '1.572500mm', 'Z:=', '0.0mm'])
segs.append(['NAME:PLSegment', 'SegmentType:=', 'Line', 'StartIndex:=', 3, 'NoOfPoints:=', 2])
pts.append(['NAME:PLPoint', 'X:=', '2.630000mm', 'Y:=', '1.375000mm', 'Z:=', '0.0mm'])
oEditor.CreatePolyline(
    ['NAME:PolylineParameters', 'IsPolylineCovered:=', True, 'IsPolylineClosed:=', True, pts, segs],
    [
        'NAME:Attributes',
        'Name:=', 'bus_left_wire_Q2_28',
        'Flags:=', '',
        'Color:=', '(200 220 255)',
        'Transparency:=', 0.0,
        'PartCoordinateSystem:=', 'Global',
        'UDMId:=', '',
        'MaterialName:=', 'vacuum',
        'SolveInside:=', True
    ]
)
# Element: bus_left_wire_sub_Q2_29
pts = ['NAME:PolylinePoints']
segs = ['NAME:PolylineSegments']
pts.append(['NAME:PLPoint', 'X:=', '2.636000mm', 'Y:=', '1.375000mm', 'Z:=', '0.0mm'])
segs.append(['NAME:PLSegment', 'SegmentType:=', 'Line', 'StartIndex:=', 0, 'NoOfPoints:=', 2])
pts.append(['NAME:PLPoint', 'X:=', '2.614000mm', 'Y:=', '1.375000mm', 'Z:=', '0.0mm'])
segs.append(['NAME:PLSegment', 'SegmentType:=', 'Line', 'StartIndex:=', 1, 'NoOfPoints:=', 2])
pts.append(['NAME:PLPoint', 'X:=', '2.614000mm', 'Y:=', '1.572500mm', 'Z:=', '0.0mm'])
segs.append(['NAME:PLSegment', 'SegmentType:=', 'Line', 'StartIndex:=', 2, 'NoOfPoints:=', 2])
pts.append(['NAME:PLPoint', 'X:=', '2.636000mm', 'Y:=', '1.572500mm', 'Z:=', '0.0mm'])
segs.append(['NAME:PLSegment', 'SegmentType:=', 'Line', 'StartIndex:=', 3, 'NoOfPoints:=', 2])
pts.append(['NAME:PLPoint', 'X:=', '2.636000mm', 'Y:=', '1.375000mm', 'Z:=', '0.0mm'])
oEditor.CreatePolyline(
    ['NAME:PolylineParameters', 'IsPolylineCovered:=', True, 'IsPolylineClosed:=', True, pts, segs],
    [
        'NAME:Attributes',
        'Name:=', 'bus_left_wire_sub_Q2_29',
        'Flags:=', '',
        'Color:=', '(255 100 100)',
        'Transparency:=', 0.0,
        'PartCoordinateSystem:=', 'Global',
        'UDMId:=', '',
        'MaterialName:=', 'vacuum',
        'SolveInside:=', True
    ]
)
# Element: readout_wire_Q2_30
pts = ['NAME:PolylinePoints']
segs = ['NAME:PolylineSegments']
pts.append(['NAME:PLPoint', 'X:=', '2.370000mm', 'Y:=', '2.225000mm', 'Z:=', '0.0mm'])
segs.append(['NAME:PLSegment', 'SegmentType:=', 'Line', 'StartIndex:=', 0, 'NoOfPoints:=', 2])
pts.append(['NAME:PLPoint', 'X:=', '2.380000mm', 'Y:=', '2.225000mm', 'Z:=', '0.0mm'])
segs.append(['NAME:PLSegment', 'SegmentType:=', 'Line', 'StartIndex:=', 1, 'NoOfPoints:=', 2])
pts.append(['NAME:PLPoint', 'X:=', '2.380000mm', 'Y:=', '2.027500mm', 'Z:=', '0.0mm'])
segs.append(['NAME:PLSegment', 'SegmentType:=', 'Line', 'StartIndex:=', 2, 'NoOfPoints:=', 2])
pts.append(['NAME:PLPoint', 'X:=', '2.370000mm', 'Y:=', '2.027500mm', 'Z:=', '0.0mm'])
segs.append(['NAME:PLSegment', 'SegmentType:=', 'Line', 'StartIndex:=', 3, 'NoOfPoints:=', 2])
pts.append(['NAME:PLPoint', 'X:=', '2.370000mm', 'Y:=', '2.225000mm', 'Z:=', '0.0mm'])
oEditor.CreatePolyline(
    ['NAME:PolylineParameters', 'IsPolylineCovered:=', True, 'IsPolylineClosed:=', True, pts, segs],
    [
        'NAME:Attributes',
        'Name:=', 'readout_wire_Q2_30',
        'Flags:=', '',
        'Color:=', '(200 220 255)',
        'Transparency:=', 0.0,
        'PartCoordinateSystem:=', 'Global',
        'UDMId:=', '',
        'MaterialName:=', 'vacuum',
        'SolveInside:=', True
    ]
)
# Element: readout_wire_sub_Q2_31
pts = ['NAME:PolylinePoints']
segs = ['NAME:PolylineSegments']
pts.append(['NAME:PLPoint', 'X:=', '2.364000mm', 'Y:=', '2.225000mm', 'Z:=', '0.0mm'])
segs.append(['NAME:PLSegment', 'SegmentType:=', 'Line', 'StartIndex:=', 0, 'NoOfPoints:=', 2])
pts.append(['NAME:PLPoint', 'X:=', '2.386000mm', 'Y:=', '2.225000mm', 'Z:=', '0.0mm'])
segs.append(['NAME:PLSegment', 'SegmentType:=', 'Line', 'StartIndex:=', 1, 'NoOfPoints:=', 2])
pts.append(['NAME:PLPoint', 'X:=', '2.386000mm', 'Y:=', '2.027500mm', 'Z:=', '0.0mm'])
segs.append(['NAME:PLSegment', 'SegmentType:=', 'Line', 'StartIndex:=', 2, 'NoOfPoints:=', 2])
pts.append(['NAME:PLPoint', 'X:=', '2.364000mm', 'Y:=', '2.027500mm', 'Z:=', '0.0mm'])
segs.append(['NAME:PLSegment', 'SegmentType:=', 'Line', 'StartIndex:=', 3, 'NoOfPoints:=', 2])
pts.append(['NAME:PLPoint', 'X:=', '2.364000mm', 'Y:=', '2.225000mm', 'Z:=', '0.0mm'])
oEditor.CreatePolyline(
    ['NAME:PolylineParameters', 'IsPolylineCovered:=', True, 'IsPolylineClosed:=', True, pts, segs],
    [
        'NAME:Attributes',
        'Name:=', 'readout_wire_sub_Q2_31',
        'Flags:=', '',
        'Color:=', '(255 100 100)',
        'Transparency:=', 0.0,
        'PartCoordinateSystem:=', 'Global',
        'UDMId:=', '',
        'MaterialName:=', 'vacuum',
        'SolveInside:=', True
    ]
)
# Element: bus_top_wire_Q6_32
pts = ['NAME:PolylinePoints']
segs = ['NAME:PolylineSegments']
pts.append(['NAME:PLPoint', 'X:=', '2.370000mm', 'Y:=', '0.425000mm', 'Z:=', '0.0mm'])
segs.append(['NAME:PLSegment', 'SegmentType:=', 'Line', 'StartIndex:=', 0, 'NoOfPoints:=', 2])
pts.append(['NAME:PLPoint', 'X:=', '2.380000mm', 'Y:=', '0.425000mm', 'Z:=', '0.0mm'])
segs.append(['NAME:PLSegment', 'SegmentType:=', 'Line', 'StartIndex:=', 1, 'NoOfPoints:=', 2])
pts.append(['NAME:PLPoint', 'X:=', '2.380000mm', 'Y:=', '0.227500mm', 'Z:=', '0.0mm'])
segs.append(['NAME:PLSegment', 'SegmentType:=', 'Line', 'StartIndex:=', 2, 'NoOfPoints:=', 2])
pts.append(['NAME:PLPoint', 'X:=', '2.370000mm', 'Y:=', '0.227500mm', 'Z:=', '0.0mm'])
segs.append(['NAME:PLSegment', 'SegmentType:=', 'Line', 'StartIndex:=', 3, 'NoOfPoints:=', 2])
pts.append(['NAME:PLPoint', 'X:=', '2.370000mm', 'Y:=', '0.425000mm', 'Z:=', '0.0mm'])
oEditor.CreatePolyline(
    ['NAME:PolylineParameters', 'IsPolylineCovered:=', True, 'IsPolylineClosed:=', True, pts, segs],
    [
        'NAME:Attributes',
        'Name:=', 'bus_top_wire_Q6_32',
        'Flags:=', '',
        'Color:=', '(200 220 255)',
        'Transparency:=', 0.0,
        'PartCoordinateSystem:=', 'Global',
        'UDMId:=', '',
        'MaterialName:=', 'vacuum',
        'SolveInside:=', True
    ]
)
# Element: bus_top_wire_sub_Q6_33
pts = ['NAME:PolylinePoints']
segs = ['NAME:PolylineSegments']
pts.append(['NAME:PLPoint', 'X:=', '2.364000mm', 'Y:=', '0.425000mm', 'Z:=', '0.0mm'])
segs.append(['NAME:PLSegment', 'SegmentType:=', 'Line', 'StartIndex:=', 0, 'NoOfPoints:=', 2])
pts.append(['NAME:PLPoint', 'X:=', '2.386000mm', 'Y:=', '0.425000mm', 'Z:=', '0.0mm'])
segs.append(['NAME:PLSegment', 'SegmentType:=', 'Line', 'StartIndex:=', 1, 'NoOfPoints:=', 2])
pts.append(['NAME:PLPoint', 'X:=', '2.386000mm', 'Y:=', '0.227500mm', 'Z:=', '0.0mm'])
segs.append(['NAME:PLSegment', 'SegmentType:=', 'Line', 'StartIndex:=', 2, 'NoOfPoints:=', 2])
pts.append(['NAME:PLPoint', 'X:=', '2.364000mm', 'Y:=', '0.227500mm', 'Z:=', '0.0mm'])
segs.append(['NAME:PLSegment', 'SegmentType:=', 'Line', 'StartIndex:=', 3, 'NoOfPoints:=', 2])
pts.append(['NAME:PLPoint', 'X:=', '2.364000mm', 'Y:=', '0.425000mm', 'Z:=', '0.0mm'])
oEditor.CreatePolyline(
    ['NAME:PolylineParameters', 'IsPolylineCovered:=', True, 'IsPolylineClosed:=', True, pts, segs],
    [
        'NAME:Attributes',
        'Name:=', 'bus_top_wire_sub_Q6_33',
        'Flags:=', '',
        'Color:=', '(255 100 100)',
        'Transparency:=', 0.0,
        'PartCoordinateSystem:=', 'Global',
        'UDMId:=', '',
        'MaterialName:=', 'vacuum',
        'SolveInside:=', True
    ]
)
# Element: readout_wire_Q6_34
pts = ['NAME:PolylinePoints']
segs = ['NAME:PolylineSegments']
pts.append(['NAME:PLPoint', 'X:=', '2.630000mm', 'Y:=', '-0.425000mm', 'Z:=', '0.0mm'])
segs.append(['NAME:PLSegment', 'SegmentType:=', 'Line', 'StartIndex:=', 0, 'NoOfPoints:=', 2])
pts.append(['NAME:PLPoint', 'X:=', '2.620000mm', 'Y:=', '-0.425000mm', 'Z:=', '0.0mm'])
segs.append(['NAME:PLSegment', 'SegmentType:=', 'Line', 'StartIndex:=', 1, 'NoOfPoints:=', 2])
pts.append(['NAME:PLPoint', 'X:=', '2.620000mm', 'Y:=', '-0.227500mm', 'Z:=', '0.0mm'])
segs.append(['NAME:PLSegment', 'SegmentType:=', 'Line', 'StartIndex:=', 2, 'NoOfPoints:=', 2])
pts.append(['NAME:PLPoint', 'X:=', '2.630000mm', 'Y:=', '-0.227500mm', 'Z:=', '0.0mm'])
segs.append(['NAME:PLSegment', 'SegmentType:=', 'Line', 'StartIndex:=', 3, 'NoOfPoints:=', 2])
pts.append(['NAME:PLPoint', 'X:=', '2.630000mm', 'Y:=', '-0.425000mm', 'Z:=', '0.0mm'])
oEditor.CreatePolyline(
    ['NAME:PolylineParameters', 'IsPolylineCovered:=', True, 'IsPolylineClosed:=', True, pts, segs],
    [
        'NAME:Attributes',
        'Name:=', 'readout_wire_Q6_34',
        'Flags:=', '',
        'Color:=', '(200 220 255)',
        'Transparency:=', 0.0,
        'PartCoordinateSystem:=', 'Global',
        'UDMId:=', '',
        'MaterialName:=', 'vacuum',
        'SolveInside:=', True
    ]
)
# Element: readout_wire_sub_Q6_35
pts = ['NAME:PolylinePoints']
segs = ['NAME:PolylineSegments']
pts.append(['NAME:PLPoint', 'X:=', '2.636000mm', 'Y:=', '-0.425000mm', 'Z:=', '0.0mm'])
segs.append(['NAME:PLSegment', 'SegmentType:=', 'Line', 'StartIndex:=', 0, 'NoOfPoints:=', 2])
pts.append(['NAME:PLPoint', 'X:=', '2.614000mm', 'Y:=', '-0.425000mm', 'Z:=', '0.0mm'])
segs.append(['NAME:PLSegment', 'SegmentType:=', 'Line', 'StartIndex:=', 1, 'NoOfPoints:=', 2])
pts.append(['NAME:PLPoint', 'X:=', '2.614000mm', 'Y:=', '-0.227500mm', 'Z:=', '0.0mm'])
segs.append(['NAME:PLSegment', 'SegmentType:=', 'Line', 'StartIndex:=', 2, 'NoOfPoints:=', 2])
pts.append(['NAME:PLPoint', 'X:=', '2.636000mm', 'Y:=', '-0.227500mm', 'Z:=', '0.0mm'])
segs.append(['NAME:PLSegment', 'SegmentType:=', 'Line', 'StartIndex:=', 3, 'NoOfPoints:=', 2])
pts.append(['NAME:PLPoint', 'X:=', '2.636000mm', 'Y:=', '-0.425000mm', 'Z:=', '0.0mm'])
oEditor.CreatePolyline(
    ['NAME:PolylineParameters', 'IsPolylineCovered:=', True, 'IsPolylineClosed:=', True, pts, segs],
    [
        'NAME:Attributes',
        'Name:=', 'readout_wire_sub_Q6_35',
        'Flags:=', '',
        'Color:=', '(255 100 100)',
        'Transparency:=', 0.0,
        'PartCoordinateSystem:=', 'Global',
        'UDMId:=', '',
        'MaterialName:=', 'vacuum',
        'SolveInside:=', True
    ]
)
# Element: trace_Bus_Q0_Q1_36
pts = ['NAME:PolylinePoints']
segs = ['NAME:PolylineSegments']
pts.append(['NAME:PLPoint', 'X:=', '-2.630000mm', 'Y:=', '0.425000mm', 'Z:=', '0.0mm'])
segs.append(['NAME:PLSegment', 'SegmentType:=', 'Line', 'StartIndex:=', 0, 'NoOfPoints:=', 2])
pts.append(['NAME:PLPoint', 'X:=', '-2.904444mm', 'Y:=', '0.425000mm', 'Z:=', '0.0mm'])
segs.append(['NAME:PLSegment', 'SegmentType:=', 'Line', 'StartIndex:=', 1, 'NoOfPoints:=', 2])
pts.append(['NAME:PLPoint', 'X:=', '-2.904444mm', 'Y:=', '0.635000mm', 'Z:=', '0.0mm'])
segs.append(['NAME:PLSegment', 'SegmentType:=', 'Line', 'StartIndex:=', 2, 'NoOfPoints:=', 2])
pts.append(['NAME:PLPoint', 'X:=', '-2.355556mm', 'Y:=', '0.635000mm', 'Z:=', '0.0mm'])
segs.append(['NAME:PLSegment', 'SegmentType:=', 'Line', 'StartIndex:=', 3, 'NoOfPoints:=', 2])
pts.append(['NAME:PLPoint', 'X:=', '-2.355556mm', 'Y:=', '0.825000mm', 'Z:=', '0.0mm'])
segs.append(['NAME:PLSegment', 'SegmentType:=', 'Line', 'StartIndex:=', 4, 'NoOfPoints:=', 2])
pts.append(['NAME:PLPoint', 'X:=', '-2.904444mm', 'Y:=', '0.825000mm', 'Z:=', '0.0mm'])
segs.append(['NAME:PLSegment', 'SegmentType:=', 'Line', 'StartIndex:=', 5, 'NoOfPoints:=', 2])
pts.append(['NAME:PLPoint', 'X:=', '-2.904444mm', 'Y:=', '1.035000mm', 'Z:=', '0.0mm'])
segs.append(['NAME:PLSegment', 'SegmentType:=', 'Line', 'StartIndex:=', 6, 'NoOfPoints:=', 2])
pts.append(['NAME:PLPoint', 'X:=', '-2.355556mm', 'Y:=', '1.035000mm', 'Z:=', '0.0mm'])
segs.append(['NAME:PLSegment', 'SegmentType:=', 'Line', 'StartIndex:=', 7, 'NoOfPoints:=', 2])
pts.append(['NAME:PLPoint', 'X:=', '-2.355556mm', 'Y:=', '1.225000mm', 'Z:=', '0.0mm'])
segs.append(['NAME:PLSegment', 'SegmentType:=', 'Line', 'StartIndex:=', 8, 'NoOfPoints:=', 2])
pts.append(['NAME:PLPoint', 'X:=', '-2.904444mm', 'Y:=', '1.225000mm', 'Z:=', '0.0mm'])
segs.append(['NAME:PLSegment', 'SegmentType:=', 'Line', 'StartIndex:=', 9, 'NoOfPoints:=', 2])
pts.append(['NAME:PLPoint', 'X:=', '-2.904444mm', 'Y:=', '1.435000mm', 'Z:=', '0.0mm'])
segs.append(['NAME:PLSegment', 'SegmentType:=', 'Line', 'StartIndex:=', 10, 'NoOfPoints:=', 2])
pts.append(['NAME:PLPoint', 'X:=', '-2.355556mm', 'Y:=', '1.435000mm', 'Z:=', '0.0mm'])
segs.append(['NAME:PLSegment', 'SegmentType:=', 'Line', 'StartIndex:=', 11, 'NoOfPoints:=', 2])
pts.append(['NAME:PLPoint', 'X:=', '-2.355556mm', 'Y:=', '1.625000mm', 'Z:=', '0.0mm'])
segs.append(['NAME:PLSegment', 'SegmentType:=', 'Line', 'StartIndex:=', 12, 'NoOfPoints:=', 2])
pts.append(['NAME:PLPoint', 'X:=', '-2.904444mm', 'Y:=', '1.625000mm', 'Z:=', '0.0mm'])
segs.append(['NAME:PLSegment', 'SegmentType:=', 'Line', 'StartIndex:=', 13, 'NoOfPoints:=', 2])
pts.append(['NAME:PLPoint', 'X:=', '-2.904444mm', 'Y:=', '1.835000mm', 'Z:=', '0.0mm'])
segs.append(['NAME:PLSegment', 'SegmentType:=', 'Line', 'StartIndex:=', 14, 'NoOfPoints:=', 2])
pts.append(['NAME:PLPoint', 'X:=', '-2.355556mm', 'Y:=', '1.835000mm', 'Z:=', '0.0mm'])
segs.append(['NAME:PLSegment', 'SegmentType:=', 'Line', 'StartIndex:=', 15, 'NoOfPoints:=', 2])
pts.append(['NAME:PLPoint', 'X:=', '-2.355556mm', 'Y:=', '2.025000mm', 'Z:=', '0.0mm'])
segs.append(['NAME:PLSegment', 'SegmentType:=', 'Line', 'StartIndex:=', 16, 'NoOfPoints:=', 2])
pts.append(['NAME:PLPoint', 'X:=', '-2.904444mm', 'Y:=', '2.025000mm', 'Z:=', '0.0mm'])
segs.append(['NAME:PLSegment', 'SegmentType:=', 'Line', 'StartIndex:=', 17, 'NoOfPoints:=', 2])
pts.append(['NAME:PLPoint', 'X:=', '-2.904444mm', 'Y:=', '2.235000mm', 'Z:=', '0.0mm'])
segs.append(['NAME:PLSegment', 'SegmentType:=', 'Line', 'StartIndex:=', 18, 'NoOfPoints:=', 2])
pts.append(['NAME:PLPoint', 'X:=', '-2.370000mm', 'Y:=', '2.235000mm', 'Z:=', '0.0mm'])
segs.append(['NAME:PLSegment', 'SegmentType:=', 'Line', 'StartIndex:=', 19, 'NoOfPoints:=', 2])
pts.append(['NAME:PLPoint', 'X:=', '-2.370000mm', 'Y:=', '2.225000mm', 'Z:=', '0.0mm'])
segs.append(['NAME:PLSegment', 'SegmentType:=', 'Line', 'StartIndex:=', 20, 'NoOfPoints:=', 2])
pts.append(['NAME:PLPoint', 'X:=', '-2.380000mm', 'Y:=', '2.225000mm', 'Z:=', '0.0mm'])
segs.append(['NAME:PLSegment', 'SegmentType:=', 'Line', 'StartIndex:=', 21, 'NoOfPoints:=', 2])
pts.append(['NAME:PLPoint', 'X:=', '-2.894444mm', 'Y:=', '2.225000mm', 'Z:=', '0.0mm'])
segs.append(['NAME:PLSegment', 'SegmentType:=', 'Line', 'StartIndex:=', 22, 'NoOfPoints:=', 2])
pts.append(['NAME:PLPoint', 'X:=', '-2.894444mm', 'Y:=', '2.035000mm', 'Z:=', '0.0mm'])
segs.append(['NAME:PLSegment', 'SegmentType:=', 'Line', 'StartIndex:=', 23, 'NoOfPoints:=', 2])
pts.append(['NAME:PLPoint', 'X:=', '-2.345556mm', 'Y:=', '2.035000mm', 'Z:=', '0.0mm'])
segs.append(['NAME:PLSegment', 'SegmentType:=', 'Line', 'StartIndex:=', 24, 'NoOfPoints:=', 2])
pts.append(['NAME:PLPoint', 'X:=', '-2.345556mm', 'Y:=', '1.825000mm', 'Z:=', '0.0mm'])
segs.append(['NAME:PLSegment', 'SegmentType:=', 'Line', 'StartIndex:=', 25, 'NoOfPoints:=', 2])
pts.append(['NAME:PLPoint', 'X:=', '-2.894444mm', 'Y:=', '1.825000mm', 'Z:=', '0.0mm'])
segs.append(['NAME:PLSegment', 'SegmentType:=', 'Line', 'StartIndex:=', 26, 'NoOfPoints:=', 2])
pts.append(['NAME:PLPoint', 'X:=', '-2.894444mm', 'Y:=', '1.635000mm', 'Z:=', '0.0mm'])
segs.append(['NAME:PLSegment', 'SegmentType:=', 'Line', 'StartIndex:=', 27, 'NoOfPoints:=', 2])
pts.append(['NAME:PLPoint', 'X:=', '-2.345556mm', 'Y:=', '1.635000mm', 'Z:=', '0.0mm'])
segs.append(['NAME:PLSegment', 'SegmentType:=', 'Line', 'StartIndex:=', 28, 'NoOfPoints:=', 2])
pts.append(['NAME:PLPoint', 'X:=', '-2.345556mm', 'Y:=', '1.425000mm', 'Z:=', '0.0mm'])
segs.append(['NAME:PLSegment', 'SegmentType:=', 'Line', 'StartIndex:=', 29, 'NoOfPoints:=', 2])
pts.append(['NAME:PLPoint', 'X:=', '-2.894444mm', 'Y:=', '1.425000mm', 'Z:=', '0.0mm'])
segs.append(['NAME:PLSegment', 'SegmentType:=', 'Line', 'StartIndex:=', 30, 'NoOfPoints:=', 2])
pts.append(['NAME:PLPoint', 'X:=', '-2.894444mm', 'Y:=', '1.235000mm', 'Z:=', '0.0mm'])
segs.append(['NAME:PLSegment', 'SegmentType:=', 'Line', 'StartIndex:=', 31, 'NoOfPoints:=', 2])
pts.append(['NAME:PLPoint', 'X:=', '-2.345556mm', 'Y:=', '1.235000mm', 'Z:=', '0.0mm'])
segs.append(['NAME:PLSegment', 'SegmentType:=', 'Line', 'StartIndex:=', 32, 'NoOfPoints:=', 2])
pts.append(['NAME:PLPoint', 'X:=', '-2.345556mm', 'Y:=', '1.025000mm', 'Z:=', '0.0mm'])
segs.append(['NAME:PLSegment', 'SegmentType:=', 'Line', 'StartIndex:=', 33, 'NoOfPoints:=', 2])
pts.append(['NAME:PLPoint', 'X:=', '-2.894444mm', 'Y:=', '1.025000mm', 'Z:=', '0.0mm'])
segs.append(['NAME:PLSegment', 'SegmentType:=', 'Line', 'StartIndex:=', 34, 'NoOfPoints:=', 2])
pts.append(['NAME:PLPoint', 'X:=', '-2.894444mm', 'Y:=', '0.835000mm', 'Z:=', '0.0mm'])
segs.append(['NAME:PLSegment', 'SegmentType:=', 'Line', 'StartIndex:=', 35, 'NoOfPoints:=', 2])
pts.append(['NAME:PLPoint', 'X:=', '-2.345556mm', 'Y:=', '0.835000mm', 'Z:=', '0.0mm'])
segs.append(['NAME:PLSegment', 'SegmentType:=', 'Line', 'StartIndex:=', 36, 'NoOfPoints:=', 2])
pts.append(['NAME:PLPoint', 'X:=', '-2.345556mm', 'Y:=', '0.625000mm', 'Z:=', '0.0mm'])
segs.append(['NAME:PLSegment', 'SegmentType:=', 'Line', 'StartIndex:=', 37, 'NoOfPoints:=', 2])
pts.append(['NAME:PLPoint', 'X:=', '-2.894444mm', 'Y:=', '0.625000mm', 'Z:=', '0.0mm'])
segs.append(['NAME:PLSegment', 'SegmentType:=', 'Line', 'StartIndex:=', 38, 'NoOfPoints:=', 2])
pts.append(['NAME:PLPoint', 'X:=', '-2.894444mm', 'Y:=', '0.435000mm', 'Z:=', '0.0mm'])
segs.append(['NAME:PLSegment', 'SegmentType:=', 'Line', 'StartIndex:=', 39, 'NoOfPoints:=', 2])
pts.append(['NAME:PLPoint', 'X:=', '-2.620000mm', 'Y:=', '0.435000mm', 'Z:=', '0.0mm'])
segs.append(['NAME:PLSegment', 'SegmentType:=', 'Line', 'StartIndex:=', 40, 'NoOfPoints:=', 2])
pts.append(['NAME:PLPoint', 'X:=', '-2.620000mm', 'Y:=', '0.425000mm', 'Z:=', '0.0mm'])
segs.append(['NAME:PLSegment', 'SegmentType:=', 'Line', 'StartIndex:=', 41, 'NoOfPoints:=', 2])
pts.append(['NAME:PLPoint', 'X:=', '-2.630000mm', 'Y:=', '0.425000mm', 'Z:=', '0.0mm'])
oEditor.CreatePolyline(
    ['NAME:PolylineParameters', 'IsPolylineCovered:=', True, 'IsPolylineClosed:=', True, pts, segs],
    [
        'NAME:Attributes',
        'Name:=', 'trace_Bus_Q0_Q1_36',
        'Flags:=', '',
        'Color:=', '(200 220 255)',
        'Transparency:=', 0.0,
        'PartCoordinateSystem:=', 'Global',
        'UDMId:=', '',
        'MaterialName:=', 'vacuum',
        'SolveInside:=', True
    ]
)
# Element: cut_Bus_Q0_Q1_37
pts = ['NAME:PolylinePoints']
segs = ['NAME:PolylineSegments']
pts.append(['NAME:PLPoint', 'X:=', '-2.625500mm', 'Y:=', '0.425000mm', 'Z:=', '0.0mm'])
segs.append(['NAME:PLSegment', 'SegmentType:=', 'Line', 'StartIndex:=', 0, 'NoOfPoints:=', 2])
pts.append(['NAME:PLPoint', 'X:=', '-2.625000mm', 'Y:=', '0.424500mm', 'Z:=', '0.0mm'])
segs.append(['NAME:PLSegment', 'SegmentType:=', 'Line', 'StartIndex:=', 1, 'NoOfPoints:=', 2])
pts.append(['NAME:PLPoint', 'X:=', '-2.625000mm', 'Y:=', '0.419000mm', 'Z:=', '0.0mm'])
segs.append(['NAME:PLSegment', 'SegmentType:=', 'Line', 'StartIndex:=', 2, 'NoOfPoints:=', 2])
pts.append(['NAME:PLPoint', 'X:=', '-2.910444mm', 'Y:=', '0.419000mm', 'Z:=', '0.0mm'])
segs.append(['NAME:PLSegment', 'SegmentType:=', 'Line', 'StartIndex:=', 3, 'NoOfPoints:=', 2])
pts.append(['NAME:PLPoint', 'X:=', '-2.910444mm', 'Y:=', '0.641000mm', 'Z:=', '0.0mm'])
segs.append(['NAME:PLSegment', 'SegmentType:=', 'Line', 'StartIndex:=', 4, 'NoOfPoints:=', 2])
pts.append(['NAME:PLPoint', 'X:=', '-2.361556mm', 'Y:=', '0.641000mm', 'Z:=', '0.0mm'])
segs.append(['NAME:PLSegment', 'SegmentType:=', 'Line', 'StartIndex:=', 5, 'NoOfPoints:=', 2])
pts.append(['NAME:PLPoint', 'X:=', '-2.361556mm', 'Y:=', '0.819000mm', 'Z:=', '0.0mm'])
segs.append(['NAME:PLSegment', 'SegmentType:=', 'Line', 'StartIndex:=', 6, 'NoOfPoints:=', 2])
pts.append(['NAME:PLPoint', 'X:=', '-2.910444mm', 'Y:=', '0.819000mm', 'Z:=', '0.0mm'])
segs.append(['NAME:PLSegment', 'SegmentType:=', 'Line', 'StartIndex:=', 7, 'NoOfPoints:=', 2])
pts.append(['NAME:PLPoint', 'X:=', '-2.910444mm', 'Y:=', '1.041000mm', 'Z:=', '0.0mm'])
segs.append(['NAME:PLSegment', 'SegmentType:=', 'Line', 'StartIndex:=', 8, 'NoOfPoints:=', 2])
pts.append(['NAME:PLPoint', 'X:=', '-2.361556mm', 'Y:=', '1.041000mm', 'Z:=', '0.0mm'])
segs.append(['NAME:PLSegment', 'SegmentType:=', 'Line', 'StartIndex:=', 9, 'NoOfPoints:=', 2])
pts.append(['NAME:PLPoint', 'X:=', '-2.361556mm', 'Y:=', '1.219000mm', 'Z:=', '0.0mm'])
segs.append(['NAME:PLSegment', 'SegmentType:=', 'Line', 'StartIndex:=', 10, 'NoOfPoints:=', 2])
pts.append(['NAME:PLPoint', 'X:=', '-2.910444mm', 'Y:=', '1.219000mm', 'Z:=', '0.0mm'])
segs.append(['NAME:PLSegment', 'SegmentType:=', 'Line', 'StartIndex:=', 11, 'NoOfPoints:=', 2])
pts.append(['NAME:PLPoint', 'X:=', '-2.910444mm', 'Y:=', '1.441000mm', 'Z:=', '0.0mm'])
segs.append(['NAME:PLSegment', 'SegmentType:=', 'Line', 'StartIndex:=', 12, 'NoOfPoints:=', 2])
pts.append(['NAME:PLPoint', 'X:=', '-2.361556mm', 'Y:=', '1.441000mm', 'Z:=', '0.0mm'])
segs.append(['NAME:PLSegment', 'SegmentType:=', 'Line', 'StartIndex:=', 13, 'NoOfPoints:=', 2])
pts.append(['NAME:PLPoint', 'X:=', '-2.361556mm', 'Y:=', '1.619000mm', 'Z:=', '0.0mm'])
segs.append(['NAME:PLSegment', 'SegmentType:=', 'Line', 'StartIndex:=', 14, 'NoOfPoints:=', 2])
pts.append(['NAME:PLPoint', 'X:=', '-2.910444mm', 'Y:=', '1.619000mm', 'Z:=', '0.0mm'])
segs.append(['NAME:PLSegment', 'SegmentType:=', 'Line', 'StartIndex:=', 15, 'NoOfPoints:=', 2])
pts.append(['NAME:PLPoint', 'X:=', '-2.910444mm', 'Y:=', '1.841000mm', 'Z:=', '0.0mm'])
segs.append(['NAME:PLSegment', 'SegmentType:=', 'Line', 'StartIndex:=', 16, 'NoOfPoints:=', 2])
pts.append(['NAME:PLPoint', 'X:=', '-2.361556mm', 'Y:=', '1.841000mm', 'Z:=', '0.0mm'])
segs.append(['NAME:PLSegment', 'SegmentType:=', 'Line', 'StartIndex:=', 17, 'NoOfPoints:=', 2])
pts.append(['NAME:PLPoint', 'X:=', '-2.361556mm', 'Y:=', '2.019000mm', 'Z:=', '0.0mm'])
segs.append(['NAME:PLSegment', 'SegmentType:=', 'Line', 'StartIndex:=', 18, 'NoOfPoints:=', 2])
pts.append(['NAME:PLPoint', 'X:=', '-2.910444mm', 'Y:=', '2.019000mm', 'Z:=', '0.0mm'])
segs.append(['NAME:PLSegment', 'SegmentType:=', 'Line', 'StartIndex:=', 19, 'NoOfPoints:=', 2])
pts.append(['NAME:PLPoint', 'X:=', '-2.910444mm', 'Y:=', '2.241000mm', 'Z:=', '0.0mm'])
segs.append(['NAME:PLSegment', 'SegmentType:=', 'Line', 'StartIndex:=', 20, 'NoOfPoints:=', 2])
pts.append(['NAME:PLPoint', 'X:=', '-2.364000mm', 'Y:=', '2.241000mm', 'Z:=', '0.0mm'])
segs.append(['NAME:PLSegment', 'SegmentType:=', 'Line', 'StartIndex:=', 21, 'NoOfPoints:=', 2])
pts.append(['NAME:PLPoint', 'X:=', '-2.364000mm', 'Y:=', '2.225000mm', 'Z:=', '0.0mm'])
segs.append(['NAME:PLSegment', 'SegmentType:=', 'Line', 'StartIndex:=', 22, 'NoOfPoints:=', 2])
pts.append(['NAME:PLPoint', 'X:=', '-2.375500mm', 'Y:=', '2.225000mm', 'Z:=', '0.0mm'])
segs.append(['NAME:PLSegment', 'SegmentType:=', 'Line', 'StartIndex:=', 23, 'NoOfPoints:=', 2])
pts.append(['NAME:PLPoint', 'X:=', '-2.375000mm', 'Y:=', '2.224500mm', 'Z:=', '0.0mm'])
segs.append(['NAME:PLSegment', 'SegmentType:=', 'Line', 'StartIndex:=', 24, 'NoOfPoints:=', 2])
pts.append(['NAME:PLPoint', 'X:=', '-2.375000mm', 'Y:=', '2.219000mm', 'Z:=', '0.0mm'])
segs.append(['NAME:PLSegment', 'SegmentType:=', 'Line', 'StartIndex:=', 25, 'NoOfPoints:=', 2])
pts.append(['NAME:PLPoint', 'X:=', '-2.888444mm', 'Y:=', '2.219000mm', 'Z:=', '0.0mm'])
segs.append(['NAME:PLSegment', 'SegmentType:=', 'Line', 'StartIndex:=', 26, 'NoOfPoints:=', 2])
pts.append(['NAME:PLPoint', 'X:=', '-2.888444mm', 'Y:=', '2.041000mm', 'Z:=', '0.0mm'])
segs.append(['NAME:PLSegment', 'SegmentType:=', 'Line', 'StartIndex:=', 27, 'NoOfPoints:=', 2])
pts.append(['NAME:PLPoint', 'X:=', '-2.339556mm', 'Y:=', '2.041000mm', 'Z:=', '0.0mm'])
segs.append(['NAME:PLSegment', 'SegmentType:=', 'Line', 'StartIndex:=', 28, 'NoOfPoints:=', 2])
pts.append(['NAME:PLPoint', 'X:=', '-2.339556mm', 'Y:=', '1.819000mm', 'Z:=', '0.0mm'])
segs.append(['NAME:PLSegment', 'SegmentType:=', 'Line', 'StartIndex:=', 29, 'NoOfPoints:=', 2])
pts.append(['NAME:PLPoint', 'X:=', '-2.888444mm', 'Y:=', '1.819000mm', 'Z:=', '0.0mm'])
segs.append(['NAME:PLSegment', 'SegmentType:=', 'Line', 'StartIndex:=', 30, 'NoOfPoints:=', 2])
pts.append(['NAME:PLPoint', 'X:=', '-2.888444mm', 'Y:=', '1.641000mm', 'Z:=', '0.0mm'])
segs.append(['NAME:PLSegment', 'SegmentType:=', 'Line', 'StartIndex:=', 31, 'NoOfPoints:=', 2])
pts.append(['NAME:PLPoint', 'X:=', '-2.339556mm', 'Y:=', '1.641000mm', 'Z:=', '0.0mm'])
segs.append(['NAME:PLSegment', 'SegmentType:=', 'Line', 'StartIndex:=', 32, 'NoOfPoints:=', 2])
pts.append(['NAME:PLPoint', 'X:=', '-2.339556mm', 'Y:=', '1.419000mm', 'Z:=', '0.0mm'])
segs.append(['NAME:PLSegment', 'SegmentType:=', 'Line', 'StartIndex:=', 33, 'NoOfPoints:=', 2])
pts.append(['NAME:PLPoint', 'X:=', '-2.888444mm', 'Y:=', '1.419000mm', 'Z:=', '0.0mm'])
segs.append(['NAME:PLSegment', 'SegmentType:=', 'Line', 'StartIndex:=', 34, 'NoOfPoints:=', 2])
pts.append(['NAME:PLPoint', 'X:=', '-2.888444mm', 'Y:=', '1.241000mm', 'Z:=', '0.0mm'])
segs.append(['NAME:PLSegment', 'SegmentType:=', 'Line', 'StartIndex:=', 35, 'NoOfPoints:=', 2])
pts.append(['NAME:PLPoint', 'X:=', '-2.339556mm', 'Y:=', '1.241000mm', 'Z:=', '0.0mm'])
segs.append(['NAME:PLSegment', 'SegmentType:=', 'Line', 'StartIndex:=', 36, 'NoOfPoints:=', 2])
pts.append(['NAME:PLPoint', 'X:=', '-2.339556mm', 'Y:=', '1.019000mm', 'Z:=', '0.0mm'])
segs.append(['NAME:PLSegment', 'SegmentType:=', 'Line', 'StartIndex:=', 37, 'NoOfPoints:=', 2])
pts.append(['NAME:PLPoint', 'X:=', '-2.888444mm', 'Y:=', '1.019000mm', 'Z:=', '0.0mm'])
segs.append(['NAME:PLSegment', 'SegmentType:=', 'Line', 'StartIndex:=', 38, 'NoOfPoints:=', 2])
pts.append(['NAME:PLPoint', 'X:=', '-2.888444mm', 'Y:=', '0.841000mm', 'Z:=', '0.0mm'])
segs.append(['NAME:PLSegment', 'SegmentType:=', 'Line', 'StartIndex:=', 39, 'NoOfPoints:=', 2])
pts.append(['NAME:PLPoint', 'X:=', '-2.339556mm', 'Y:=', '0.841000mm', 'Z:=', '0.0mm'])
segs.append(['NAME:PLSegment', 'SegmentType:=', 'Line', 'StartIndex:=', 40, 'NoOfPoints:=', 2])
pts.append(['NAME:PLPoint', 'X:=', '-2.339556mm', 'Y:=', '0.619000mm', 'Z:=', '0.0mm'])
segs.append(['NAME:PLSegment', 'SegmentType:=', 'Line', 'StartIndex:=', 41, 'NoOfPoints:=', 2])
pts.append(['NAME:PLPoint', 'X:=', '-2.888444mm', 'Y:=', '0.619000mm', 'Z:=', '0.0mm'])
segs.append(['NAME:PLSegment', 'SegmentType:=', 'Line', 'StartIndex:=', 42, 'NoOfPoints:=', 2])
pts.append(['NAME:PLPoint', 'X:=', '-2.888444mm', 'Y:=', '0.441000mm', 'Z:=', '0.0mm'])
segs.append(['NAME:PLSegment', 'SegmentType:=', 'Line', 'StartIndex:=', 43, 'NoOfPoints:=', 2])
pts.append(['NAME:PLPoint', 'X:=', '-2.614000mm', 'Y:=', '0.441000mm', 'Z:=', '0.0mm'])
segs.append(['NAME:PLSegment', 'SegmentType:=', 'Line', 'StartIndex:=', 44, 'NoOfPoints:=', 2])
pts.append(['NAME:PLPoint', 'X:=', '-2.614000mm', 'Y:=', '0.425000mm', 'Z:=', '0.0mm'])
segs.append(['NAME:PLSegment', 'SegmentType:=', 'Line', 'StartIndex:=', 45, 'NoOfPoints:=', 2])
pts.append(['NAME:PLPoint', 'X:=', '-2.625500mm', 'Y:=', '0.425000mm', 'Z:=', '0.0mm'])
oEditor.CreatePolyline(
    ['NAME:PolylineParameters', 'IsPolylineCovered:=', True, 'IsPolylineClosed:=', True, pts, segs],
    [
        'NAME:Attributes',
        'Name:=', 'cut_Bus_Q0_Q1_37',
        'Flags:=', '',
        'Color:=', '(255 100 100)',
        'Transparency:=', 0.0,
        'PartCoordinateSystem:=', 'Global',
        'UDMId:=', '',
        'MaterialName:=', 'vacuum',
        'SolveInside:=', True
    ]
)
# Element: trace_Bus_Q1_Q3_38
pts = ['NAME:PolylinePoints']
segs = ['NAME:PolylineSegments']
pts.append(['NAME:PLPoint', 'X:=', '-2.370000mm', 'Y:=', '-0.130000mm', 'Z:=', '0.0mm'])
segs.append(['NAME:PLSegment', 'SegmentType:=', 'Line', 'StartIndex:=', 0, 'NoOfPoints:=', 2])
pts.append(['NAME:PLPoint', 'X:=', '-2.180000mm', 'Y:=', '-0.130000mm', 'Z:=', '0.0mm'])
segs.append(['NAME:PLSegment', 'SegmentType:=', 'Line', 'StartIndex:=', 1, 'NoOfPoints:=', 2])
pts.append(['NAME:PLPoint', 'X:=', '-2.180000mm', 'Y:=', '2.880000mm', 'Z:=', '0.0mm'])
segs.append(['NAME:PLSegment', 'SegmentType:=', 'Line', 'StartIndex:=', 2, 'NoOfPoints:=', 2])
pts.append(['NAME:PLPoint', 'X:=', '-1.970000mm', 'Y:=', '2.880000mm', 'Z:=', '0.0mm'])
segs.append(['NAME:PLSegment', 'SegmentType:=', 'Line', 'StartIndex:=', 3, 'NoOfPoints:=', 2])
pts.append(['NAME:PLPoint', 'X:=', '-1.970000mm', 'Y:=', '1.000000mm', 'Z:=', '0.0mm'])
segs.append(['NAME:PLSegment', 'SegmentType:=', 'Line', 'StartIndex:=', 4, 'NoOfPoints:=', 2])
pts.append(['NAME:PLPoint', 'X:=', '-1.775000mm', 'Y:=', '1.000000mm', 'Z:=', '0.0mm'])
segs.append(['NAME:PLSegment', 'SegmentType:=', 'Line', 'StartIndex:=', 5, 'NoOfPoints:=', 2])
pts.append(['NAME:PLPoint', 'X:=', '-1.775000mm', 'Y:=', '0.990000mm', 'Z:=', '0.0mm'])
segs.append(['NAME:PLSegment', 'SegmentType:=', 'Line', 'StartIndex:=', 6, 'NoOfPoints:=', 2])
pts.append(['NAME:PLPoint', 'X:=', '-1.980000mm', 'Y:=', '0.990000mm', 'Z:=', '0.0mm'])
segs.append(['NAME:PLSegment', 'SegmentType:=', 'Line', 'StartIndex:=', 7, 'NoOfPoints:=', 2])
pts.append(['NAME:PLPoint', 'X:=', '-1.980000mm', 'Y:=', '2.870000mm', 'Z:=', '0.0mm'])
segs.append(['NAME:PLSegment', 'SegmentType:=', 'Line', 'StartIndex:=', 8, 'NoOfPoints:=', 2])
pts.append(['NAME:PLPoint', 'X:=', '-2.170000mm', 'Y:=', '2.870000mm', 'Z:=', '0.0mm'])
segs.append(['NAME:PLSegment', 'SegmentType:=', 'Line', 'StartIndex:=', 9, 'NoOfPoints:=', 2])
pts.append(['NAME:PLPoint', 'X:=', '-2.170000mm', 'Y:=', '-0.140000mm', 'Z:=', '0.0mm'])
segs.append(['NAME:PLSegment', 'SegmentType:=', 'Line', 'StartIndex:=', 10, 'NoOfPoints:=', 2])
pts.append(['NAME:PLPoint', 'X:=', '-2.380000mm', 'Y:=', '-0.140000mm', 'Z:=', '0.0mm'])
segs.append(['NAME:PLSegment', 'SegmentType:=', 'Line', 'StartIndex:=', 11, 'NoOfPoints:=', 2])
pts.append(['NAME:PLPoint', 'X:=', '-2.380000mm', 'Y:=', '1.375000mm', 'Z:=', '0.0mm'])
segs.append(['NAME:PLSegment', 'SegmentType:=', 'Line', 'StartIndex:=', 12, 'NoOfPoints:=', 2])
pts.append(['NAME:PLPoint', 'X:=', '-2.370000mm', 'Y:=', '1.375000mm', 'Z:=', '0.0mm'])
segs.append(['NAME:PLSegment', 'SegmentType:=', 'Line', 'StartIndex:=', 13, 'NoOfPoints:=', 2])
pts.append(['NAME:PLPoint', 'X:=', '-2.370000mm', 'Y:=', '-0.130000mm', 'Z:=', '0.0mm'])
oEditor.CreatePolyline(
    ['NAME:PolylineParameters', 'IsPolylineCovered:=', True, 'IsPolylineClosed:=', True, pts, segs],
    [
        'NAME:Attributes',
        'Name:=', 'trace_Bus_Q1_Q3_38',
        'Flags:=', '',
        'Color:=', '(200 220 255)',
        'Transparency:=', 0.0,
        'PartCoordinateSystem:=', 'Global',
        'UDMId:=', '',
        'MaterialName:=', 'vacuum',
        'SolveInside:=', True
    ]
)
# Element: cut_Bus_Q1_Q3_39
pts = ['NAME:PolylinePoints']
segs = ['NAME:PolylineSegments']
pts.append(['NAME:PLPoint', 'X:=', '-2.364000mm', 'Y:=', '-0.124000mm', 'Z:=', '0.0mm'])
segs.append(['NAME:PLSegment', 'SegmentType:=', 'Line', 'StartIndex:=', 0, 'NoOfPoints:=', 2])
pts.append(['NAME:PLPoint', 'X:=', '-2.186000mm', 'Y:=', '-0.124000mm', 'Z:=', '0.0mm'])
segs.append(['NAME:PLSegment', 'SegmentType:=', 'Line', 'StartIndex:=', 1, 'NoOfPoints:=', 2])
pts.append(['NAME:PLPoint', 'X:=', '-2.186000mm', 'Y:=', '2.886000mm', 'Z:=', '0.0mm'])
segs.append(['NAME:PLSegment', 'SegmentType:=', 'Line', 'StartIndex:=', 2, 'NoOfPoints:=', 2])
pts.append(['NAME:PLPoint', 'X:=', '-1.964000mm', 'Y:=', '2.886000mm', 'Z:=', '0.0mm'])
segs.append(['NAME:PLSegment', 'SegmentType:=', 'Line', 'StartIndex:=', 3, 'NoOfPoints:=', 2])
pts.append(['NAME:PLPoint', 'X:=', '-1.964000mm', 'Y:=', '1.006000mm', 'Z:=', '0.0mm'])
segs.append(['NAME:PLSegment', 'SegmentType:=', 'Line', 'StartIndex:=', 4, 'NoOfPoints:=', 2])
pts.append(['NAME:PLPoint', 'X:=', '-1.775000mm', 'Y:=', '1.006000mm', 'Z:=', '0.0mm'])
segs.append(['NAME:PLSegment', 'SegmentType:=', 'Line', 'StartIndex:=', 5, 'NoOfPoints:=', 2])
pts.append(['NAME:PLPoint', 'X:=', '-1.775000mm', 'Y:=', '0.984000mm', 'Z:=', '0.0mm'])
segs.append(['NAME:PLSegment', 'SegmentType:=', 'Line', 'StartIndex:=', 6, 'NoOfPoints:=', 2])
pts.append(['NAME:PLPoint', 'X:=', '-1.986000mm', 'Y:=', '0.984000mm', 'Z:=', '0.0mm'])
segs.append(['NAME:PLSegment', 'SegmentType:=', 'Line', 'StartIndex:=', 7, 'NoOfPoints:=', 2])
pts.append(['NAME:PLPoint', 'X:=', '-1.986000mm', 'Y:=', '2.864000mm', 'Z:=', '0.0mm'])
segs.append(['NAME:PLSegment', 'SegmentType:=', 'Line', 'StartIndex:=', 8, 'NoOfPoints:=', 2])
pts.append(['NAME:PLPoint', 'X:=', '-2.164000mm', 'Y:=', '2.864000mm', 'Z:=', '0.0mm'])
segs.append(['NAME:PLSegment', 'SegmentType:=', 'Line', 'StartIndex:=', 9, 'NoOfPoints:=', 2])
pts.append(['NAME:PLPoint', 'X:=', '-2.164000mm', 'Y:=', '-0.146000mm', 'Z:=', '0.0mm'])
segs.append(['NAME:PLSegment', 'SegmentType:=', 'Line', 'StartIndex:=', 10, 'NoOfPoints:=', 2])
pts.append(['NAME:PLPoint', 'X:=', '-2.386000mm', 'Y:=', '-0.146000mm', 'Z:=', '0.0mm'])
segs.append(['NAME:PLSegment', 'SegmentType:=', 'Line', 'StartIndex:=', 11, 'NoOfPoints:=', 2])
pts.append(['NAME:PLPoint', 'X:=', '-2.386000mm', 'Y:=', '1.375000mm', 'Z:=', '0.0mm'])
segs.append(['NAME:PLSegment', 'SegmentType:=', 'Line', 'StartIndex:=', 12, 'NoOfPoints:=', 2])
pts.append(['NAME:PLPoint', 'X:=', '-2.364000mm', 'Y:=', '1.375000mm', 'Z:=', '0.0mm'])
segs.append(['NAME:PLSegment', 'SegmentType:=', 'Line', 'StartIndex:=', 13, 'NoOfPoints:=', 2])
pts.append(['NAME:PLPoint', 'X:=', '-2.364000mm', 'Y:=', '-0.124000mm', 'Z:=', '0.0mm'])
oEditor.CreatePolyline(
    ['NAME:PolylineParameters', 'IsPolylineCovered:=', True, 'IsPolylineClosed:=', True, pts, segs],
    [
        'NAME:Attributes',
        'Name:=', 'cut_Bus_Q1_Q3_39',
        'Flags:=', '',
        'Color:=', '(255 100 100)',
        'Transparency:=', 0.0,
        'PartCoordinateSystem:=', 'Global',
        'UDMId:=', '',
        'MaterialName:=', 'vacuum',
        'SolveInside:=', True
    ]
)
# Element: trace_Bus_Q3_Q4_40
pts = ['NAME:PolylinePoints']
segs = ['NAME:PolylineSegments']
pts.append(['NAME:PLPoint', 'X:=', '-0.925000mm', 'Y:=', '0.750000mm', 'Z:=', '0.0mm'])
segs.append(['NAME:PLSegment', 'SegmentType:=', 'Line', 'StartIndex:=', 0, 'NoOfPoints:=', 2])
pts.append(['NAME:PLPoint', 'X:=', '-0.925000mm', 'Y:=', '2.392500mm', 'Z:=', '0.0mm'])
segs.append(['NAME:PLSegment', 'SegmentType:=', 'Line', 'StartIndex:=', 1, 'NoOfPoints:=', 2])
pts.append(['NAME:PLPoint', 'X:=', '-0.715000mm', 'Y:=', '2.392500mm', 'Z:=', '0.0mm'])
segs.append(['NAME:PLSegment', 'SegmentType:=', 'Line', 'StartIndex:=', 2, 'NoOfPoints:=', 2])
pts.append(['NAME:PLPoint', 'X:=', '-0.715000mm', 'Y:=', '-0.892500mm', 'Z:=', '0.0mm'])
segs.append(['NAME:PLSegment', 'SegmentType:=', 'Line', 'StartIndex:=', 3, 'NoOfPoints:=', 2])
pts.append(['NAME:PLPoint', 'X:=', '-0.525000mm', 'Y:=', '-0.892500mm', 'Z:=', '0.0mm'])
segs.append(['NAME:PLSegment', 'SegmentType:=', 'Line', 'StartIndex:=', 4, 'NoOfPoints:=', 2])
pts.append(['NAME:PLPoint', 'X:=', '-0.525000mm', 'Y:=', '0.680000mm', 'Z:=', '0.0mm'])
segs.append(['NAME:PLSegment', 'SegmentType:=', 'Line', 'StartIndex:=', 5, 'NoOfPoints:=', 2])
pts.append(['NAME:PLPoint', 'X:=', '-0.425000mm', 'Y:=', '0.680000mm', 'Z:=', '0.0mm'])
segs.append(['NAME:PLSegment', 'SegmentType:=', 'Line', 'StartIndex:=', 6, 'NoOfPoints:=', 2])
pts.append(['NAME:PLPoint', 'X:=', '-0.425000mm', 'Y:=', '0.670000mm', 'Z:=', '0.0mm'])
segs.append(['NAME:PLSegment', 'SegmentType:=', 'Line', 'StartIndex:=', 7, 'NoOfPoints:=', 2])
pts.append(['NAME:PLPoint', 'X:=', '-0.515000mm', 'Y:=', '0.670000mm', 'Z:=', '0.0mm'])
segs.append(['NAME:PLSegment', 'SegmentType:=', 'Line', 'StartIndex:=', 8, 'NoOfPoints:=', 2])
pts.append(['NAME:PLPoint', 'X:=', '-0.515000mm', 'Y:=', '-0.902500mm', 'Z:=', '0.0mm'])
segs.append(['NAME:PLSegment', 'SegmentType:=', 'Line', 'StartIndex:=', 9, 'NoOfPoints:=', 2])
pts.append(['NAME:PLPoint', 'X:=', '-0.725000mm', 'Y:=', '-0.902500mm', 'Z:=', '0.0mm'])
segs.append(['NAME:PLSegment', 'SegmentType:=', 'Line', 'StartIndex:=', 10, 'NoOfPoints:=', 2])
pts.append(['NAME:PLPoint', 'X:=', '-0.725000mm', 'Y:=', '2.382500mm', 'Z:=', '0.0mm'])
segs.append(['NAME:PLSegment', 'SegmentType:=', 'Line', 'StartIndex:=', 11, 'NoOfPoints:=', 2])
pts.append(['NAME:PLPoint', 'X:=', '-0.915000mm', 'Y:=', '2.382500mm', 'Z:=', '0.0mm'])
segs.append(['NAME:PLSegment', 'SegmentType:=', 'Line', 'StartIndex:=', 12, 'NoOfPoints:=', 2])
pts.append(['NAME:PLPoint', 'X:=', '-0.915000mm', 'Y:=', '0.740000mm', 'Z:=', '0.0mm'])
segs.append(['NAME:PLSegment', 'SegmentType:=', 'Line', 'StartIndex:=', 13, 'NoOfPoints:=', 2])
pts.append(['NAME:PLPoint', 'X:=', '-0.925000mm', 'Y:=', '0.740000mm', 'Z:=', '0.0mm'])
segs.append(['NAME:PLSegment', 'SegmentType:=', 'Line', 'StartIndex:=', 14, 'NoOfPoints:=', 2])
pts.append(['NAME:PLPoint', 'X:=', '-0.925000mm', 'Y:=', '0.750000mm', 'Z:=', '0.0mm'])
oEditor.CreatePolyline(
    ['NAME:PolylineParameters', 'IsPolylineCovered:=', True, 'IsPolylineClosed:=', True, pts, segs],
    [
        'NAME:Attributes',
        'Name:=', 'trace_Bus_Q3_Q4_40',
        'Flags:=', '',
        'Color:=', '(200 220 255)',
        'Transparency:=', 0.0,
        'PartCoordinateSystem:=', 'Global',
        'UDMId:=', '',
        'MaterialName:=', 'vacuum',
        'SolveInside:=', True
    ]
)
# Element: cut_Bus_Q3_Q4_41
pts = ['NAME:PolylinePoints']
segs = ['NAME:PolylineSegments']
pts.append(['NAME:PLPoint', 'X:=', '-0.925000mm', 'Y:=', '0.745500mm', 'Z:=', '0.0mm'])
segs.append(['NAME:PLSegment', 'SegmentType:=', 'Line', 'StartIndex:=', 0, 'NoOfPoints:=', 2])
pts.append(['NAME:PLPoint', 'X:=', '-0.925500mm', 'Y:=', '0.745000mm', 'Z:=', '0.0mm'])
segs.append(['NAME:PLSegment', 'SegmentType:=', 'Line', 'StartIndex:=', 1, 'NoOfPoints:=', 2])
pts.append(['NAME:PLPoint', 'X:=', '-0.931000mm', 'Y:=', '0.745000mm', 'Z:=', '0.0mm'])
segs.append(['NAME:PLSegment', 'SegmentType:=', 'Line', 'StartIndex:=', 2, 'NoOfPoints:=', 2])
pts.append(['NAME:PLPoint', 'X:=', '-0.931000mm', 'Y:=', '2.398500mm', 'Z:=', '0.0mm'])
segs.append(['NAME:PLSegment', 'SegmentType:=', 'Line', 'StartIndex:=', 3, 'NoOfPoints:=', 2])
pts.append(['NAME:PLPoint', 'X:=', '-0.709000mm', 'Y:=', '2.398500mm', 'Z:=', '0.0mm'])
segs.append(['NAME:PLSegment', 'SegmentType:=', 'Line', 'StartIndex:=', 4, 'NoOfPoints:=', 2])
pts.append(['NAME:PLPoint', 'X:=', '-0.709000mm', 'Y:=', '-0.886500mm', 'Z:=', '0.0mm'])
segs.append(['NAME:PLSegment', 'SegmentType:=', 'Line', 'StartIndex:=', 5, 'NoOfPoints:=', 2])
pts.append(['NAME:PLPoint', 'X:=', '-0.531000mm', 'Y:=', '-0.886500mm', 'Z:=', '0.0mm'])
segs.append(['NAME:PLSegment', 'SegmentType:=', 'Line', 'StartIndex:=', 6, 'NoOfPoints:=', 2])
pts.append(['NAME:PLPoint', 'X:=', '-0.531000mm', 'Y:=', '0.686000mm', 'Z:=', '0.0mm'])
segs.append(['NAME:PLSegment', 'SegmentType:=', 'Line', 'StartIndex:=', 7, 'NoOfPoints:=', 2])
pts.append(['NAME:PLPoint', 'X:=', '-0.425000mm', 'Y:=', '0.686000mm', 'Z:=', '0.0mm'])
segs.append(['NAME:PLSegment', 'SegmentType:=', 'Line', 'StartIndex:=', 8, 'NoOfPoints:=', 2])
pts.append(['NAME:PLPoint', 'X:=', '-0.425000mm', 'Y:=', '0.664000mm', 'Z:=', '0.0mm'])
segs.append(['NAME:PLSegment', 'SegmentType:=', 'Line', 'StartIndex:=', 9, 'NoOfPoints:=', 2])
pts.append(['NAME:PLPoint', 'X:=', '-0.509000mm', 'Y:=', '0.664000mm', 'Z:=', '0.0mm'])
segs.append(['NAME:PLSegment', 'SegmentType:=', 'Line', 'StartIndex:=', 10, 'NoOfPoints:=', 2])
pts.append(['NAME:PLPoint', 'X:=', '-0.509000mm', 'Y:=', '-0.908500mm', 'Z:=', '0.0mm'])
segs.append(['NAME:PLSegment', 'SegmentType:=', 'Line', 'StartIndex:=', 11, 'NoOfPoints:=', 2])
pts.append(['NAME:PLPoint', 'X:=', '-0.731000mm', 'Y:=', '-0.908500mm', 'Z:=', '0.0mm'])
segs.append(['NAME:PLSegment', 'SegmentType:=', 'Line', 'StartIndex:=', 12, 'NoOfPoints:=', 2])
pts.append(['NAME:PLPoint', 'X:=', '-0.731000mm', 'Y:=', '2.376500mm', 'Z:=', '0.0mm'])
segs.append(['NAME:PLSegment', 'SegmentType:=', 'Line', 'StartIndex:=', 13, 'NoOfPoints:=', 2])
pts.append(['NAME:PLPoint', 'X:=', '-0.909000mm', 'Y:=', '2.376500mm', 'Z:=', '0.0mm'])
segs.append(['NAME:PLSegment', 'SegmentType:=', 'Line', 'StartIndex:=', 14, 'NoOfPoints:=', 2])
pts.append(['NAME:PLPoint', 'X:=', '-0.909000mm', 'Y:=', '0.734000mm', 'Z:=', '0.0mm'])
segs.append(['NAME:PLSegment', 'SegmentType:=', 'Line', 'StartIndex:=', 15, 'NoOfPoints:=', 2])
pts.append(['NAME:PLPoint', 'X:=', '-0.925000mm', 'Y:=', '0.734000mm', 'Z:=', '0.0mm'])
segs.append(['NAME:PLSegment', 'SegmentType:=', 'Line', 'StartIndex:=', 16, 'NoOfPoints:=', 2])
pts.append(['NAME:PLPoint', 'X:=', '-0.925000mm', 'Y:=', '0.745500mm', 'Z:=', '0.0mm'])
oEditor.CreatePolyline(
    ['NAME:PolylineParameters', 'IsPolylineCovered:=', True, 'IsPolylineClosed:=', True, pts, segs],
    [
        'NAME:Attributes',
        'Name:=', 'cut_Bus_Q3_Q4_41',
        'Flags:=', '',
        'Color:=', '(255 100 100)',
        'Transparency:=', 0.0,
        'PartCoordinateSystem:=', 'Global',
        'UDMId:=', '',
        'MaterialName:=', 'vacuum',
        'SolveInside:=', True
    ]
)
# Element: trace_Bus_Q4_Q5_42
pts = ['NAME:PolylinePoints']
segs = ['NAME:PolylineSegments']
pts.append(['NAME:PLPoint', 'X:=', '0.425000mm', 'Y:=', '0.680000mm', 'Z:=', '0.0mm'])
segs.append(['NAME:PLSegment', 'SegmentType:=', 'Line', 'StartIndex:=', 0, 'NoOfPoints:=', 2])
pts.append(['NAME:PLPoint', 'X:=', '0.425000mm', 'Y:=', '2.287500mm', 'Z:=', '0.0mm'])
segs.append(['NAME:PLSegment', 'SegmentType:=', 'Line', 'StartIndex:=', 1, 'NoOfPoints:=', 2])
pts.append(['NAME:PLPoint', 'X:=', '0.635000mm', 'Y:=', '2.287500mm', 'Z:=', '0.0mm'])
segs.append(['NAME:PLSegment', 'SegmentType:=', 'Line', 'StartIndex:=', 2, 'NoOfPoints:=', 2])
pts.append(['NAME:PLPoint', 'X:=', '0.635000mm', 'Y:=', '-0.927500mm', 'Z:=', '0.0mm'])
segs.append(['NAME:PLSegment', 'SegmentType:=', 'Line', 'StartIndex:=', 3, 'NoOfPoints:=', 2])
pts.append(['NAME:PLPoint', 'X:=', '0.825000mm', 'Y:=', '-0.927500mm', 'Z:=', '0.0mm'])
segs.append(['NAME:PLSegment', 'SegmentType:=', 'Line', 'StartIndex:=', 4, 'NoOfPoints:=', 2])
pts.append(['NAME:PLPoint', 'X:=', '0.825000mm', 'Y:=', '0.750000mm', 'Z:=', '0.0mm'])
segs.append(['NAME:PLSegment', 'SegmentType:=', 'Line', 'StartIndex:=', 5, 'NoOfPoints:=', 2])
pts.append(['NAME:PLPoint', 'X:=', '0.925000mm', 'Y:=', '0.750000mm', 'Z:=', '0.0mm'])
segs.append(['NAME:PLSegment', 'SegmentType:=', 'Line', 'StartIndex:=', 6, 'NoOfPoints:=', 2])
pts.append(['NAME:PLPoint', 'X:=', '0.925000mm', 'Y:=', '0.740000mm', 'Z:=', '0.0mm'])
segs.append(['NAME:PLSegment', 'SegmentType:=', 'Line', 'StartIndex:=', 7, 'NoOfPoints:=', 2])
pts.append(['NAME:PLPoint', 'X:=', '0.835000mm', 'Y:=', '0.740000mm', 'Z:=', '0.0mm'])
segs.append(['NAME:PLSegment', 'SegmentType:=', 'Line', 'StartIndex:=', 8, 'NoOfPoints:=', 2])
pts.append(['NAME:PLPoint', 'X:=', '0.835000mm', 'Y:=', '-0.937500mm', 'Z:=', '0.0mm'])
segs.append(['NAME:PLSegment', 'SegmentType:=', 'Line', 'StartIndex:=', 9, 'NoOfPoints:=', 2])
pts.append(['NAME:PLPoint', 'X:=', '0.625000mm', 'Y:=', '-0.937500mm', 'Z:=', '0.0mm'])
segs.append(['NAME:PLSegment', 'SegmentType:=', 'Line', 'StartIndex:=', 10, 'NoOfPoints:=', 2])
pts.append(['NAME:PLPoint', 'X:=', '0.625000mm', 'Y:=', '2.277500mm', 'Z:=', '0.0mm'])
segs.append(['NAME:PLSegment', 'SegmentType:=', 'Line', 'StartIndex:=', 11, 'NoOfPoints:=', 2])
pts.append(['NAME:PLPoint', 'X:=', '0.435000mm', 'Y:=', '2.277500mm', 'Z:=', '0.0mm'])
segs.append(['NAME:PLSegment', 'SegmentType:=', 'Line', 'StartIndex:=', 12, 'NoOfPoints:=', 2])
pts.append(['NAME:PLPoint', 'X:=', '0.435000mm', 'Y:=', '0.670000mm', 'Z:=', '0.0mm'])
segs.append(['NAME:PLSegment', 'SegmentType:=', 'Line', 'StartIndex:=', 13, 'NoOfPoints:=', 2])
pts.append(['NAME:PLPoint', 'X:=', '0.425000mm', 'Y:=', '0.670000mm', 'Z:=', '0.0mm'])
segs.append(['NAME:PLSegment', 'SegmentType:=', 'Line', 'StartIndex:=', 14, 'NoOfPoints:=', 2])
pts.append(['NAME:PLPoint', 'X:=', '0.425000mm', 'Y:=', '0.680000mm', 'Z:=', '0.0mm'])
oEditor.CreatePolyline(
    ['NAME:PolylineParameters', 'IsPolylineCovered:=', True, 'IsPolylineClosed:=', True, pts, segs],
    [
        'NAME:Attributes',
        'Name:=', 'trace_Bus_Q4_Q5_42',
        'Flags:=', '',
        'Color:=', '(200 220 255)',
        'Transparency:=', 0.0,
        'PartCoordinateSystem:=', 'Global',
        'UDMId:=', '',
        'MaterialName:=', 'vacuum',
        'SolveInside:=', True
    ]
)
# Element: cut_Bus_Q4_Q5_43
pts = ['NAME:PolylinePoints']
segs = ['NAME:PolylineSegments']
pts.append(['NAME:PLPoint', 'X:=', '0.425000mm', 'Y:=', '0.675500mm', 'Z:=', '0.0mm'])
segs.append(['NAME:PLSegment', 'SegmentType:=', 'Line', 'StartIndex:=', 0, 'NoOfPoints:=', 2])
pts.append(['NAME:PLPoint', 'X:=', '0.424500mm', 'Y:=', '0.675000mm', 'Z:=', '0.0mm'])
segs.append(['NAME:PLSegment', 'SegmentType:=', 'Line', 'StartIndex:=', 1, 'NoOfPoints:=', 2])
pts.append(['NAME:PLPoint', 'X:=', '0.419000mm', 'Y:=', '0.675000mm', 'Z:=', '0.0mm'])
segs.append(['NAME:PLSegment', 'SegmentType:=', 'Line', 'StartIndex:=', 2, 'NoOfPoints:=', 2])
pts.append(['NAME:PLPoint', 'X:=', '0.419000mm', 'Y:=', '2.293500mm', 'Z:=', '0.0mm'])
segs.append(['NAME:PLSegment', 'SegmentType:=', 'Line', 'StartIndex:=', 3, 'NoOfPoints:=', 2])
pts.append(['NAME:PLPoint', 'X:=', '0.641000mm', 'Y:=', '2.293500mm', 'Z:=', '0.0mm'])
segs.append(['NAME:PLSegment', 'SegmentType:=', 'Line', 'StartIndex:=', 4, 'NoOfPoints:=', 2])
pts.append(['NAME:PLPoint', 'X:=', '0.641000mm', 'Y:=', '-0.921500mm', 'Z:=', '0.0mm'])
segs.append(['NAME:PLSegment', 'SegmentType:=', 'Line', 'StartIndex:=', 5, 'NoOfPoints:=', 2])
pts.append(['NAME:PLPoint', 'X:=', '0.819000mm', 'Y:=', '-0.921500mm', 'Z:=', '0.0mm'])
segs.append(['NAME:PLSegment', 'SegmentType:=', 'Line', 'StartIndex:=', 6, 'NoOfPoints:=', 2])
pts.append(['NAME:PLPoint', 'X:=', '0.819000mm', 'Y:=', '0.756000mm', 'Z:=', '0.0mm'])
segs.append(['NAME:PLSegment', 'SegmentType:=', 'Line', 'StartIndex:=', 7, 'NoOfPoints:=', 2])
pts.append(['NAME:PLPoint', 'X:=', '0.925000mm', 'Y:=', '0.756000mm', 'Z:=', '0.0mm'])
segs.append(['NAME:PLSegment', 'SegmentType:=', 'Line', 'StartIndex:=', 8, 'NoOfPoints:=', 2])
pts.append(['NAME:PLPoint', 'X:=', '0.925000mm', 'Y:=', '0.734000mm', 'Z:=', '0.0mm'])
segs.append(['NAME:PLSegment', 'SegmentType:=', 'Line', 'StartIndex:=', 9, 'NoOfPoints:=', 2])
pts.append(['NAME:PLPoint', 'X:=', '0.841000mm', 'Y:=', '0.734000mm', 'Z:=', '0.0mm'])
segs.append(['NAME:PLSegment', 'SegmentType:=', 'Line', 'StartIndex:=', 10, 'NoOfPoints:=', 2])
pts.append(['NAME:PLPoint', 'X:=', '0.841000mm', 'Y:=', '-0.943500mm', 'Z:=', '0.0mm'])
segs.append(['NAME:PLSegment', 'SegmentType:=', 'Line', 'StartIndex:=', 11, 'NoOfPoints:=', 2])
pts.append(['NAME:PLPoint', 'X:=', '0.619000mm', 'Y:=', '-0.943500mm', 'Z:=', '0.0mm'])
segs.append(['NAME:PLSegment', 'SegmentType:=', 'Line', 'StartIndex:=', 12, 'NoOfPoints:=', 2])
pts.append(['NAME:PLPoint', 'X:=', '0.619000mm', 'Y:=', '2.271500mm', 'Z:=', '0.0mm'])
segs.append(['NAME:PLSegment', 'SegmentType:=', 'Line', 'StartIndex:=', 13, 'NoOfPoints:=', 2])
pts.append(['NAME:PLPoint', 'X:=', '0.441000mm', 'Y:=', '2.271500mm', 'Z:=', '0.0mm'])
segs.append(['NAME:PLSegment', 'SegmentType:=', 'Line', 'StartIndex:=', 14, 'NoOfPoints:=', 2])
pts.append(['NAME:PLPoint', 'X:=', '0.441000mm', 'Y:=', '0.664000mm', 'Z:=', '0.0mm'])
segs.append(['NAME:PLSegment', 'SegmentType:=', 'Line', 'StartIndex:=', 15, 'NoOfPoints:=', 2])
pts.append(['NAME:PLPoint', 'X:=', '0.425000mm', 'Y:=', '0.664000mm', 'Z:=', '0.0mm'])
segs.append(['NAME:PLSegment', 'SegmentType:=', 'Line', 'StartIndex:=', 16, 'NoOfPoints:=', 2])
pts.append(['NAME:PLPoint', 'X:=', '0.425000mm', 'Y:=', '0.675500mm', 'Z:=', '0.0mm'])
oEditor.CreatePolyline(
    ['NAME:PolylineParameters', 'IsPolylineCovered:=', True, 'IsPolylineClosed:=', True, pts, segs],
    [
        'NAME:Attributes',
        'Name:=', 'cut_Bus_Q4_Q5_43',
        'Flags:=', '',
        'Color:=', '(255 100 100)',
        'Transparency:=', 0.0,
        'PartCoordinateSystem:=', 'Global',
        'UDMId:=', '',
        'MaterialName:=', 'vacuum',
        'SolveInside:=', True
    ]
)
# Element: trace_Bus_Q5_Q2_44
pts = ['NAME:PolylinePoints']
segs = ['NAME:PolylineSegments']
pts.append(['NAME:PLPoint', 'X:=', '1.775000mm', 'Y:=', '1.000000mm', 'Z:=', '0.0mm'])
segs.append(['NAME:PLSegment', 'SegmentType:=', 'Line', 'StartIndex:=', 0, 'NoOfPoints:=', 2])
pts.append(['NAME:PLPoint', 'X:=', '1.775000mm', 'Y:=', '1.721250mm', 'Z:=', '0.0mm'])
segs.append(['NAME:PLSegment', 'SegmentType:=', 'Line', 'StartIndex:=', 1, 'NoOfPoints:=', 2])
pts.append(['NAME:PLPoint', 'X:=', '1.985000mm', 'Y:=', '1.721250mm', 'Z:=', '0.0mm'])
segs.append(['NAME:PLSegment', 'SegmentType:=', 'Line', 'StartIndex:=', 2, 'NoOfPoints:=', 2])
pts.append(['NAME:PLPoint', 'X:=', '1.985000mm', 'Y:=', '0.278750mm', 'Z:=', '0.0mm'])
segs.append(['NAME:PLSegment', 'SegmentType:=', 'Line', 'StartIndex:=', 3, 'NoOfPoints:=', 2])
pts.append(['NAME:PLPoint', 'X:=', '2.175000mm', 'Y:=', '0.278750mm', 'Z:=', '0.0mm'])
segs.append(['NAME:PLSegment', 'SegmentType:=', 'Line', 'StartIndex:=', 4, 'NoOfPoints:=', 2])
pts.append(['NAME:PLPoint', 'X:=', '2.175000mm', 'Y:=', '1.721250mm', 'Z:=', '0.0mm'])
segs.append(['NAME:PLSegment', 'SegmentType:=', 'Line', 'StartIndex:=', 5, 'NoOfPoints:=', 2])
pts.append(['NAME:PLPoint', 'X:=', '2.385000mm', 'Y:=', '1.721250mm', 'Z:=', '0.0mm'])
segs.append(['NAME:PLSegment', 'SegmentType:=', 'Line', 'StartIndex:=', 6, 'NoOfPoints:=', 2])
pts.append(['NAME:PLPoint', 'X:=', '2.385000mm', 'Y:=', '0.278750mm', 'Z:=', '0.0mm'])
segs.append(['NAME:PLSegment', 'SegmentType:=', 'Line', 'StartIndex:=', 7, 'NoOfPoints:=', 2])
pts.append(['NAME:PLPoint', 'X:=', '2.575000mm', 'Y:=', '0.278750mm', 'Z:=', '0.0mm'])
segs.append(['NAME:PLSegment', 'SegmentType:=', 'Line', 'StartIndex:=', 8, 'NoOfPoints:=', 2])
pts.append(['NAME:PLPoint', 'X:=', '2.575000mm', 'Y:=', '1.375000mm', 'Z:=', '0.0mm'])
segs.append(['NAME:PLSegment', 'SegmentType:=', 'Line', 'StartIndex:=', 9, 'NoOfPoints:=', 2])
pts.append(['NAME:PLPoint', 'X:=', '2.620000mm', 'Y:=', '1.375000mm', 'Z:=', '0.0mm'])
segs.append(['NAME:PLSegment', 'SegmentType:=', 'Line', 'StartIndex:=', 10, 'NoOfPoints:=', 2])
pts.append(['NAME:PLPoint', 'X:=', '2.630000mm', 'Y:=', '1.375000mm', 'Z:=', '0.0mm'])
segs.append(['NAME:PLSegment', 'SegmentType:=', 'Line', 'StartIndex:=', 11, 'NoOfPoints:=', 2])
pts.append(['NAME:PLPoint', 'X:=', '2.630000mm', 'Y:=', '1.365000mm', 'Z:=', '0.0mm'])
segs.append(['NAME:PLSegment', 'SegmentType:=', 'Line', 'StartIndex:=', 12, 'NoOfPoints:=', 2])
pts.append(['NAME:PLPoint', 'X:=', '2.585000mm', 'Y:=', '1.365000mm', 'Z:=', '0.0mm'])
segs.append(['NAME:PLSegment', 'SegmentType:=', 'Line', 'StartIndex:=', 13, 'NoOfPoints:=', 2])
pts.append(['NAME:PLPoint', 'X:=', '2.585000mm', 'Y:=', '0.268750mm', 'Z:=', '0.0mm'])
segs.append(['NAME:PLSegment', 'SegmentType:=', 'Line', 'StartIndex:=', 14, 'NoOfPoints:=', 2])
pts.append(['NAME:PLPoint', 'X:=', '2.375000mm', 'Y:=', '0.268750mm', 'Z:=', '0.0mm'])
segs.append(['NAME:PLSegment', 'SegmentType:=', 'Line', 'StartIndex:=', 15, 'NoOfPoints:=', 2])
pts.append(['NAME:PLPoint', 'X:=', '2.375000mm', 'Y:=', '1.711250mm', 'Z:=', '0.0mm'])
segs.append(['NAME:PLSegment', 'SegmentType:=', 'Line', 'StartIndex:=', 16, 'NoOfPoints:=', 2])
pts.append(['NAME:PLPoint', 'X:=', '2.185000mm', 'Y:=', '1.711250mm', 'Z:=', '0.0mm'])
segs.append(['NAME:PLSegment', 'SegmentType:=', 'Line', 'StartIndex:=', 17, 'NoOfPoints:=', 2])
pts.append(['NAME:PLPoint', 'X:=', '2.185000mm', 'Y:=', '0.268750mm', 'Z:=', '0.0mm'])
segs.append(['NAME:PLSegment', 'SegmentType:=', 'Line', 'StartIndex:=', 18, 'NoOfPoints:=', 2])
pts.append(['NAME:PLPoint', 'X:=', '1.975000mm', 'Y:=', '0.268750mm', 'Z:=', '0.0mm'])
segs.append(['NAME:PLSegment', 'SegmentType:=', 'Line', 'StartIndex:=', 19, 'NoOfPoints:=', 2])
pts.append(['NAME:PLPoint', 'X:=', '1.975000mm', 'Y:=', '1.711250mm', 'Z:=', '0.0mm'])
segs.append(['NAME:PLSegment', 'SegmentType:=', 'Line', 'StartIndex:=', 20, 'NoOfPoints:=', 2])
pts.append(['NAME:PLPoint', 'X:=', '1.785000mm', 'Y:=', '1.711250mm', 'Z:=', '0.0mm'])
segs.append(['NAME:PLSegment', 'SegmentType:=', 'Line', 'StartIndex:=', 21, 'NoOfPoints:=', 2])
pts.append(['NAME:PLPoint', 'X:=', '1.785000mm', 'Y:=', '0.990000mm', 'Z:=', '0.0mm'])
segs.append(['NAME:PLSegment', 'SegmentType:=', 'Line', 'StartIndex:=', 22, 'NoOfPoints:=', 2])
pts.append(['NAME:PLPoint', 'X:=', '1.775000mm', 'Y:=', '0.990000mm', 'Z:=', '0.0mm'])
segs.append(['NAME:PLSegment', 'SegmentType:=', 'Line', 'StartIndex:=', 23, 'NoOfPoints:=', 2])
pts.append(['NAME:PLPoint', 'X:=', '1.775000mm', 'Y:=', '1.000000mm', 'Z:=', '0.0mm'])
segs.append(['NAME:PLSegment', 'SegmentType:=', 'Line', 'StartIndex:=', 24, 'NoOfPoints:=', 2])
pts.append(['NAME:PLPoint', 'X:=', '1.775000mm', 'Y:=', '1.000000mm', 'Z:=', '0.0mm'])
oEditor.CreatePolyline(
    ['NAME:PolylineParameters', 'IsPolylineCovered:=', True, 'IsPolylineClosed:=', True, pts, segs],
    [
        'NAME:Attributes',
        'Name:=', 'trace_Bus_Q5_Q2_44',
        'Flags:=', '',
        'Color:=', '(200 220 255)',
        'Transparency:=', 0.0,
        'PartCoordinateSystem:=', 'Global',
        'UDMId:=', '',
        'MaterialName:=', 'vacuum',
        'SolveInside:=', True
    ]
)
# Element: cut_Bus_Q5_Q2_45
pts = ['NAME:PolylinePoints']
segs = ['NAME:PolylineSegments']
pts.append(['NAME:PLPoint', 'X:=', '1.775000mm', 'Y:=', '0.995500mm', 'Z:=', '0.0mm'])
segs.append(['NAME:PLSegment', 'SegmentType:=', 'Line', 'StartIndex:=', 0, 'NoOfPoints:=', 2])
pts.append(['NAME:PLPoint', 'X:=', '1.774500mm', 'Y:=', '0.995000mm', 'Z:=', '0.0mm'])
segs.append(['NAME:PLSegment', 'SegmentType:=', 'Line', 'StartIndex:=', 1, 'NoOfPoints:=', 2])
pts.append(['NAME:PLPoint', 'X:=', '1.769000mm', 'Y:=', '0.995000mm', 'Z:=', '0.0mm'])
segs.append(['NAME:PLSegment', 'SegmentType:=', 'Line', 'StartIndex:=', 2, 'NoOfPoints:=', 2])
pts.append(['NAME:PLPoint', 'X:=', '1.769000mm', 'Y:=', '1.727250mm', 'Z:=', '0.0mm'])
segs.append(['NAME:PLSegment', 'SegmentType:=', 'Line', 'StartIndex:=', 3, 'NoOfPoints:=', 2])
pts.append(['NAME:PLPoint', 'X:=', '1.991000mm', 'Y:=', '1.727250mm', 'Z:=', '0.0mm'])
segs.append(['NAME:PLSegment', 'SegmentType:=', 'Line', 'StartIndex:=', 4, 'NoOfPoints:=', 2])
pts.append(['NAME:PLPoint', 'X:=', '1.991000mm', 'Y:=', '0.284750mm', 'Z:=', '0.0mm'])
segs.append(['NAME:PLSegment', 'SegmentType:=', 'Line', 'StartIndex:=', 5, 'NoOfPoints:=', 2])
pts.append(['NAME:PLPoint', 'X:=', '2.169000mm', 'Y:=', '0.284750mm', 'Z:=', '0.0mm'])
segs.append(['NAME:PLSegment', 'SegmentType:=', 'Line', 'StartIndex:=', 6, 'NoOfPoints:=', 2])
pts.append(['NAME:PLPoint', 'X:=', '2.169000mm', 'Y:=', '1.727250mm', 'Z:=', '0.0mm'])
segs.append(['NAME:PLSegment', 'SegmentType:=', 'Line', 'StartIndex:=', 7, 'NoOfPoints:=', 2])
pts.append(['NAME:PLPoint', 'X:=', '2.391000mm', 'Y:=', '1.727250mm', 'Z:=', '0.0mm'])
segs.append(['NAME:PLSegment', 'SegmentType:=', 'Line', 'StartIndex:=', 8, 'NoOfPoints:=', 2])
pts.append(['NAME:PLPoint', 'X:=', '2.391000mm', 'Y:=', '0.284750mm', 'Z:=', '0.0mm'])
segs.append(['NAME:PLSegment', 'SegmentType:=', 'Line', 'StartIndex:=', 9, 'NoOfPoints:=', 2])
pts.append(['NAME:PLPoint', 'X:=', '2.569000mm', 'Y:=', '0.284750mm', 'Z:=', '0.0mm'])
segs.append(['NAME:PLSegment', 'SegmentType:=', 'Line', 'StartIndex:=', 10, 'NoOfPoints:=', 2])
pts.append(['NAME:PLPoint', 'X:=', '2.569000mm', 'Y:=', '1.381000mm', 'Z:=', '0.0mm'])
segs.append(['NAME:PLSegment', 'SegmentType:=', 'Line', 'StartIndex:=', 11, 'NoOfPoints:=', 2])
pts.append(['NAME:PLPoint', 'X:=', '2.625000mm', 'Y:=', '1.381000mm', 'Z:=', '0.0mm'])
segs.append(['NAME:PLSegment', 'SegmentType:=', 'Line', 'StartIndex:=', 12, 'NoOfPoints:=', 2])
pts.append(['NAME:PLPoint', 'X:=', '2.625000mm', 'Y:=', '1.375500mm', 'Z:=', '0.0mm'])
segs.append(['NAME:PLSegment', 'SegmentType:=', 'Line', 'StartIndex:=', 13, 'NoOfPoints:=', 2])
pts.append(['NAME:PLPoint', 'X:=', '2.624500mm', 'Y:=', '1.375000mm', 'Z:=', '0.0mm'])
segs.append(['NAME:PLSegment', 'SegmentType:=', 'Line', 'StartIndex:=', 14, 'NoOfPoints:=', 2])
pts.append(['NAME:PLPoint', 'X:=', '2.636000mm', 'Y:=', '1.375000mm', 'Z:=', '0.0mm'])
segs.append(['NAME:PLSegment', 'SegmentType:=', 'Line', 'StartIndex:=', 15, 'NoOfPoints:=', 2])
pts.append(['NAME:PLPoint', 'X:=', '2.636000mm', 'Y:=', '1.359000mm', 'Z:=', '0.0mm'])
segs.append(['NAME:PLSegment', 'SegmentType:=', 'Line', 'StartIndex:=', 16, 'NoOfPoints:=', 2])
pts.append(['NAME:PLPoint', 'X:=', '2.591000mm', 'Y:=', '1.359000mm', 'Z:=', '0.0mm'])
segs.append(['NAME:PLSegment', 'SegmentType:=', 'Line', 'StartIndex:=', 17, 'NoOfPoints:=', 2])
pts.append(['NAME:PLPoint', 'X:=', '2.591000mm', 'Y:=', '0.262750mm', 'Z:=', '0.0mm'])
segs.append(['NAME:PLSegment', 'SegmentType:=', 'Line', 'StartIndex:=', 18, 'NoOfPoints:=', 2])
pts.append(['NAME:PLPoint', 'X:=', '2.369000mm', 'Y:=', '0.262750mm', 'Z:=', '0.0mm'])
segs.append(['NAME:PLSegment', 'SegmentType:=', 'Line', 'StartIndex:=', 19, 'NoOfPoints:=', 2])
pts.append(['NAME:PLPoint', 'X:=', '2.369000mm', 'Y:=', '1.705250mm', 'Z:=', '0.0mm'])
segs.append(['NAME:PLSegment', 'SegmentType:=', 'Line', 'StartIndex:=', 20, 'NoOfPoints:=', 2])
pts.append(['NAME:PLPoint', 'X:=', '2.191000mm', 'Y:=', '1.705250mm', 'Z:=', '0.0mm'])
segs.append(['NAME:PLSegment', 'SegmentType:=', 'Line', 'StartIndex:=', 21, 'NoOfPoints:=', 2])
pts.append(['NAME:PLPoint', 'X:=', '2.191000mm', 'Y:=', '0.262750mm', 'Z:=', '0.0mm'])
segs.append(['NAME:PLSegment', 'SegmentType:=', 'Line', 'StartIndex:=', 22, 'NoOfPoints:=', 2])
pts.append(['NAME:PLPoint', 'X:=', '1.969000mm', 'Y:=', '0.262750mm', 'Z:=', '0.0mm'])
segs.append(['NAME:PLSegment', 'SegmentType:=', 'Line', 'StartIndex:=', 23, 'NoOfPoints:=', 2])
pts.append(['NAME:PLPoint', 'X:=', '1.969000mm', 'Y:=', '1.705250mm', 'Z:=', '0.0mm'])
segs.append(['NAME:PLSegment', 'SegmentType:=', 'Line', 'StartIndex:=', 24, 'NoOfPoints:=', 2])
pts.append(['NAME:PLPoint', 'X:=', '1.791000mm', 'Y:=', '1.705250mm', 'Z:=', '0.0mm'])
segs.append(['NAME:PLSegment', 'SegmentType:=', 'Line', 'StartIndex:=', 25, 'NoOfPoints:=', 2])
pts.append(['NAME:PLPoint', 'X:=', '1.791000mm', 'Y:=', '0.984000mm', 'Z:=', '0.0mm'])
segs.append(['NAME:PLSegment', 'SegmentType:=', 'Line', 'StartIndex:=', 26, 'NoOfPoints:=', 2])
pts.append(['NAME:PLPoint', 'X:=', '1.775000mm', 'Y:=', '0.984000mm', 'Z:=', '0.0mm'])
segs.append(['NAME:PLSegment', 'SegmentType:=', 'Line', 'StartIndex:=', 27, 'NoOfPoints:=', 2])
pts.append(['NAME:PLPoint', 'X:=', '1.775000mm', 'Y:=', '0.995500mm', 'Z:=', '0.0mm'])
oEditor.CreatePolyline(
    ['NAME:PolylineParameters', 'IsPolylineCovered:=', True, 'IsPolylineClosed:=', True, pts, segs],
    [
        'NAME:Attributes',
        'Name:=', 'cut_Bus_Q5_Q2_45',
        'Flags:=', '',
        'Color:=', '(255 100 100)',
        'Transparency:=', 0.0,
        'PartCoordinateSystem:=', 'Global',
        'UDMId:=', '',
        'MaterialName:=', 'vacuum',
        'SolveInside:=', True
    ]
)
# Element: trace_Bus_Q2_Q6_46
pts = ['NAME:PolylinePoints']
segs = ['NAME:PolylineSegments']
pts.append(['NAME:PLPoint', 'X:=', '2.620000mm', 'Y:=', '2.235000mm', 'Z:=', '0.0mm'])
segs.append(['NAME:PLSegment', 'SegmentType:=', 'Line', 'StartIndex:=', 0, 'NoOfPoints:=', 2])
pts.append(['NAME:PLPoint', 'X:=', '2.904444mm', 'Y:=', '2.235000mm', 'Z:=', '0.0mm'])
segs.append(['NAME:PLSegment', 'SegmentType:=', 'Line', 'StartIndex:=', 1, 'NoOfPoints:=', 2])
pts.append(['NAME:PLPoint', 'X:=', '2.904444mm', 'Y:=', '2.025000mm', 'Z:=', '0.0mm'])
segs.append(['NAME:PLSegment', 'SegmentType:=', 'Line', 'StartIndex:=', 2, 'NoOfPoints:=', 2])
pts.append(['NAME:PLPoint', 'X:=', '2.355556mm', 'Y:=', '2.025000mm', 'Z:=', '0.0mm'])
segs.append(['NAME:PLSegment', 'SegmentType:=', 'Line', 'StartIndex:=', 3, 'NoOfPoints:=', 2])
pts.append(['NAME:PLPoint', 'X:=', '2.355556mm', 'Y:=', '1.835000mm', 'Z:=', '0.0mm'])
segs.append(['NAME:PLSegment', 'SegmentType:=', 'Line', 'StartIndex:=', 4, 'NoOfPoints:=', 2])
pts.append(['NAME:PLPoint', 'X:=', '2.904444mm', 'Y:=', '1.835000mm', 'Z:=', '0.0mm'])
segs.append(['NAME:PLSegment', 'SegmentType:=', 'Line', 'StartIndex:=', 5, 'NoOfPoints:=', 2])
pts.append(['NAME:PLPoint', 'X:=', '2.904444mm', 'Y:=', '1.625000mm', 'Z:=', '0.0mm'])
segs.append(['NAME:PLSegment', 'SegmentType:=', 'Line', 'StartIndex:=', 6, 'NoOfPoints:=', 2])
pts.append(['NAME:PLPoint', 'X:=', '2.355556mm', 'Y:=', '1.625000mm', 'Z:=', '0.0mm'])
segs.append(['NAME:PLSegment', 'SegmentType:=', 'Line', 'StartIndex:=', 7, 'NoOfPoints:=', 2])
pts.append(['NAME:PLPoint', 'X:=', '2.355556mm', 'Y:=', '1.435000mm', 'Z:=', '0.0mm'])
segs.append(['NAME:PLSegment', 'SegmentType:=', 'Line', 'StartIndex:=', 8, 'NoOfPoints:=', 2])
pts.append(['NAME:PLPoint', 'X:=', '2.904444mm', 'Y:=', '1.435000mm', 'Z:=', '0.0mm'])
segs.append(['NAME:PLSegment', 'SegmentType:=', 'Line', 'StartIndex:=', 9, 'NoOfPoints:=', 2])
pts.append(['NAME:PLPoint', 'X:=', '2.904444mm', 'Y:=', '1.225000mm', 'Z:=', '0.0mm'])
segs.append(['NAME:PLSegment', 'SegmentType:=', 'Line', 'StartIndex:=', 10, 'NoOfPoints:=', 2])
pts.append(['NAME:PLPoint', 'X:=', '2.355556mm', 'Y:=', '1.225000mm', 'Z:=', '0.0mm'])
segs.append(['NAME:PLSegment', 'SegmentType:=', 'Line', 'StartIndex:=', 11, 'NoOfPoints:=', 2])
pts.append(['NAME:PLPoint', 'X:=', '2.355556mm', 'Y:=', '1.035000mm', 'Z:=', '0.0mm'])
segs.append(['NAME:PLSegment', 'SegmentType:=', 'Line', 'StartIndex:=', 12, 'NoOfPoints:=', 2])
pts.append(['NAME:PLPoint', 'X:=', '2.904444mm', 'Y:=', '1.035000mm', 'Z:=', '0.0mm'])
segs.append(['NAME:PLSegment', 'SegmentType:=', 'Line', 'StartIndex:=', 13, 'NoOfPoints:=', 2])
pts.append(['NAME:PLPoint', 'X:=', '2.904444mm', 'Y:=', '0.825000mm', 'Z:=', '0.0mm'])
segs.append(['NAME:PLSegment', 'SegmentType:=', 'Line', 'StartIndex:=', 14, 'NoOfPoints:=', 2])
pts.append(['NAME:PLPoint', 'X:=', '2.355556mm', 'Y:=', '0.825000mm', 'Z:=', '0.0mm'])
segs.append(['NAME:PLSegment', 'SegmentType:=', 'Line', 'StartIndex:=', 15, 'NoOfPoints:=', 2])
pts.append(['NAME:PLPoint', 'X:=', '2.355556mm', 'Y:=', '0.635000mm', 'Z:=', '0.0mm'])
segs.append(['NAME:PLSegment', 'SegmentType:=', 'Line', 'StartIndex:=', 16, 'NoOfPoints:=', 2])
pts.append(['NAME:PLPoint', 'X:=', '2.904444mm', 'Y:=', '0.635000mm', 'Z:=', '0.0mm'])
segs.append(['NAME:PLSegment', 'SegmentType:=', 'Line', 'StartIndex:=', 17, 'NoOfPoints:=', 2])
pts.append(['NAME:PLPoint', 'X:=', '2.904444mm', 'Y:=', '0.425000mm', 'Z:=', '0.0mm'])
segs.append(['NAME:PLSegment', 'SegmentType:=', 'Line', 'StartIndex:=', 18, 'NoOfPoints:=', 2])
pts.append(['NAME:PLPoint', 'X:=', '2.380000mm', 'Y:=', '0.425000mm', 'Z:=', '0.0mm'])
segs.append(['NAME:PLSegment', 'SegmentType:=', 'Line', 'StartIndex:=', 19, 'NoOfPoints:=', 2])
pts.append(['NAME:PLPoint', 'X:=', '2.370000mm', 'Y:=', '0.425000mm', 'Z:=', '0.0mm'])
segs.append(['NAME:PLSegment', 'SegmentType:=', 'Line', 'StartIndex:=', 20, 'NoOfPoints:=', 2])
pts.append(['NAME:PLPoint', 'X:=', '2.370000mm', 'Y:=', '0.435000mm', 'Z:=', '0.0mm'])
segs.append(['NAME:PLSegment', 'SegmentType:=', 'Line', 'StartIndex:=', 21, 'NoOfPoints:=', 2])
pts.append(['NAME:PLPoint', 'X:=', '2.894444mm', 'Y:=', '0.435000mm', 'Z:=', '0.0mm'])
segs.append(['NAME:PLSegment', 'SegmentType:=', 'Line', 'StartIndex:=', 22, 'NoOfPoints:=', 2])
pts.append(['NAME:PLPoint', 'X:=', '2.894444mm', 'Y:=', '0.625000mm', 'Z:=', '0.0mm'])
segs.append(['NAME:PLSegment', 'SegmentType:=', 'Line', 'StartIndex:=', 23, 'NoOfPoints:=', 2])
pts.append(['NAME:PLPoint', 'X:=', '2.345556mm', 'Y:=', '0.625000mm', 'Z:=', '0.0mm'])
segs.append(['NAME:PLSegment', 'SegmentType:=', 'Line', 'StartIndex:=', 24, 'NoOfPoints:=', 2])
pts.append(['NAME:PLPoint', 'X:=', '2.345556mm', 'Y:=', '0.835000mm', 'Z:=', '0.0mm'])
segs.append(['NAME:PLSegment', 'SegmentType:=', 'Line', 'StartIndex:=', 25, 'NoOfPoints:=', 2])
pts.append(['NAME:PLPoint', 'X:=', '2.894444mm', 'Y:=', '0.835000mm', 'Z:=', '0.0mm'])
segs.append(['NAME:PLSegment', 'SegmentType:=', 'Line', 'StartIndex:=', 26, 'NoOfPoints:=', 2])
pts.append(['NAME:PLPoint', 'X:=', '2.894444mm', 'Y:=', '1.025000mm', 'Z:=', '0.0mm'])
segs.append(['NAME:PLSegment', 'SegmentType:=', 'Line', 'StartIndex:=', 27, 'NoOfPoints:=', 2])
pts.append(['NAME:PLPoint', 'X:=', '2.345556mm', 'Y:=', '1.025000mm', 'Z:=', '0.0mm'])
segs.append(['NAME:PLSegment', 'SegmentType:=', 'Line', 'StartIndex:=', 28, 'NoOfPoints:=', 2])
pts.append(['NAME:PLPoint', 'X:=', '2.345556mm', 'Y:=', '1.235000mm', 'Z:=', '0.0mm'])
segs.append(['NAME:PLSegment', 'SegmentType:=', 'Line', 'StartIndex:=', 29, 'NoOfPoints:=', 2])
pts.append(['NAME:PLPoint', 'X:=', '2.894444mm', 'Y:=', '1.235000mm', 'Z:=', '0.0mm'])
segs.append(['NAME:PLSegment', 'SegmentType:=', 'Line', 'StartIndex:=', 30, 'NoOfPoints:=', 2])
pts.append(['NAME:PLPoint', 'X:=', '2.894444mm', 'Y:=', '1.425000mm', 'Z:=', '0.0mm'])
segs.append(['NAME:PLSegment', 'SegmentType:=', 'Line', 'StartIndex:=', 31, 'NoOfPoints:=', 2])
pts.append(['NAME:PLPoint', 'X:=', '2.345556mm', 'Y:=', '1.425000mm', 'Z:=', '0.0mm'])
segs.append(['NAME:PLSegment', 'SegmentType:=', 'Line', 'StartIndex:=', 32, 'NoOfPoints:=', 2])
pts.append(['NAME:PLPoint', 'X:=', '2.345556mm', 'Y:=', '1.635000mm', 'Z:=', '0.0mm'])
segs.append(['NAME:PLSegment', 'SegmentType:=', 'Line', 'StartIndex:=', 33, 'NoOfPoints:=', 2])
pts.append(['NAME:PLPoint', 'X:=', '2.894444mm', 'Y:=', '1.635000mm', 'Z:=', '0.0mm'])
segs.append(['NAME:PLSegment', 'SegmentType:=', 'Line', 'StartIndex:=', 34, 'NoOfPoints:=', 2])
pts.append(['NAME:PLPoint', 'X:=', '2.894444mm', 'Y:=', '1.825000mm', 'Z:=', '0.0mm'])
segs.append(['NAME:PLSegment', 'SegmentType:=', 'Line', 'StartIndex:=', 35, 'NoOfPoints:=', 2])
pts.append(['NAME:PLPoint', 'X:=', '2.345556mm', 'Y:=', '1.825000mm', 'Z:=', '0.0mm'])
segs.append(['NAME:PLSegment', 'SegmentType:=', 'Line', 'StartIndex:=', 36, 'NoOfPoints:=', 2])
pts.append(['NAME:PLPoint', 'X:=', '2.345556mm', 'Y:=', '2.035000mm', 'Z:=', '0.0mm'])
segs.append(['NAME:PLSegment', 'SegmentType:=', 'Line', 'StartIndex:=', 37, 'NoOfPoints:=', 2])
pts.append(['NAME:PLPoint', 'X:=', '2.894444mm', 'Y:=', '2.035000mm', 'Z:=', '0.0mm'])
segs.append(['NAME:PLSegment', 'SegmentType:=', 'Line', 'StartIndex:=', 38, 'NoOfPoints:=', 2])
pts.append(['NAME:PLPoint', 'X:=', '2.894444mm', 'Y:=', '2.225000mm', 'Z:=', '0.0mm'])
segs.append(['NAME:PLSegment', 'SegmentType:=', 'Line', 'StartIndex:=', 39, 'NoOfPoints:=', 2])
pts.append(['NAME:PLPoint', 'X:=', '2.630000mm', 'Y:=', '2.225000mm', 'Z:=', '0.0mm'])
segs.append(['NAME:PLSegment', 'SegmentType:=', 'Line', 'StartIndex:=', 40, 'NoOfPoints:=', 2])
pts.append(['NAME:PLPoint', 'X:=', '2.620000mm', 'Y:=', '2.225000mm', 'Z:=', '0.0mm'])
segs.append(['NAME:PLSegment', 'SegmentType:=', 'Line', 'StartIndex:=', 41, 'NoOfPoints:=', 2])
pts.append(['NAME:PLPoint', 'X:=', '2.620000mm', 'Y:=', '2.235000mm', 'Z:=', '0.0mm'])
oEditor.CreatePolyline(
    ['NAME:PolylineParameters', 'IsPolylineCovered:=', True, 'IsPolylineClosed:=', True, pts, segs],
    [
        'NAME:Attributes',
        'Name:=', 'trace_Bus_Q2_Q6_46',
        'Flags:=', '',
        'Color:=', '(200 220 255)',
        'Transparency:=', 0.0,
        'PartCoordinateSystem:=', 'Global',
        'UDMId:=', '',
        'MaterialName:=', 'vacuum',
        'SolveInside:=', True
    ]
)
# Element: cut_Bus_Q2_Q6_47
pts = ['NAME:PolylinePoints']
segs = ['NAME:PolylineSegments']
pts.append(['NAME:PLPoint', 'X:=', '2.375500mm', 'Y:=', '0.425000mm', 'Z:=', '0.0mm'])
segs.append(['NAME:PLSegment', 'SegmentType:=', 'Line', 'StartIndex:=', 0, 'NoOfPoints:=', 2])
pts.append(['NAME:PLPoint', 'X:=', '2.364000mm', 'Y:=', '0.425000mm', 'Z:=', '0.0mm'])
segs.append(['NAME:PLSegment', 'SegmentType:=', 'Line', 'StartIndex:=', 1, 'NoOfPoints:=', 2])
pts.append(['NAME:PLPoint', 'X:=', '2.364000mm', 'Y:=', '0.441000mm', 'Z:=', '0.0mm'])
segs.append(['NAME:PLSegment', 'SegmentType:=', 'Line', 'StartIndex:=', 2, 'NoOfPoints:=', 2])
pts.append(['NAME:PLPoint', 'X:=', '2.888444mm', 'Y:=', '0.441000mm', 'Z:=', '0.0mm'])
segs.append(['NAME:PLSegment', 'SegmentType:=', 'Line', 'StartIndex:=', 3, 'NoOfPoints:=', 2])
pts.append(['NAME:PLPoint', 'X:=', '2.888444mm', 'Y:=', '0.619000mm', 'Z:=', '0.0mm'])
segs.append(['NAME:PLSegment', 'SegmentType:=', 'Line', 'StartIndex:=', 4, 'NoOfPoints:=', 2])
pts.append(['NAME:PLPoint', 'X:=', '2.339556mm', 'Y:=', '0.619000mm', 'Z:=', '0.0mm'])
segs.append(['NAME:PLSegment', 'SegmentType:=', 'Line', 'StartIndex:=', 5, 'NoOfPoints:=', 2])
pts.append(['NAME:PLPoint', 'X:=', '2.339556mm', 'Y:=', '0.841000mm', 'Z:=', '0.0mm'])
segs.append(['NAME:PLSegment', 'SegmentType:=', 'Line', 'StartIndex:=', 6, 'NoOfPoints:=', 2])
pts.append(['NAME:PLPoint', 'X:=', '2.888444mm', 'Y:=', '0.841000mm', 'Z:=', '0.0mm'])
segs.append(['NAME:PLSegment', 'SegmentType:=', 'Line', 'StartIndex:=', 7, 'NoOfPoints:=', 2])
pts.append(['NAME:PLPoint', 'X:=', '2.888444mm', 'Y:=', '1.019000mm', 'Z:=', '0.0mm'])
segs.append(['NAME:PLSegment', 'SegmentType:=', 'Line', 'StartIndex:=', 8, 'NoOfPoints:=', 2])
pts.append(['NAME:PLPoint', 'X:=', '2.339556mm', 'Y:=', '1.019000mm', 'Z:=', '0.0mm'])
segs.append(['NAME:PLSegment', 'SegmentType:=', 'Line', 'StartIndex:=', 9, 'NoOfPoints:=', 2])
pts.append(['NAME:PLPoint', 'X:=', '2.339556mm', 'Y:=', '1.241000mm', 'Z:=', '0.0mm'])
segs.append(['NAME:PLSegment', 'SegmentType:=', 'Line', 'StartIndex:=', 10, 'NoOfPoints:=', 2])
pts.append(['NAME:PLPoint', 'X:=', '2.888444mm', 'Y:=', '1.241000mm', 'Z:=', '0.0mm'])
segs.append(['NAME:PLSegment', 'SegmentType:=', 'Line', 'StartIndex:=', 11, 'NoOfPoints:=', 2])
pts.append(['NAME:PLPoint', 'X:=', '2.888444mm', 'Y:=', '1.419000mm', 'Z:=', '0.0mm'])
segs.append(['NAME:PLSegment', 'SegmentType:=', 'Line', 'StartIndex:=', 12, 'NoOfPoints:=', 2])
pts.append(['NAME:PLPoint', 'X:=', '2.339556mm', 'Y:=', '1.419000mm', 'Z:=', '0.0mm'])
segs.append(['NAME:PLSegment', 'SegmentType:=', 'Line', 'StartIndex:=', 13, 'NoOfPoints:=', 2])
pts.append(['NAME:PLPoint', 'X:=', '2.339556mm', 'Y:=', '1.641000mm', 'Z:=', '0.0mm'])
segs.append(['NAME:PLSegment', 'SegmentType:=', 'Line', 'StartIndex:=', 14, 'NoOfPoints:=', 2])
pts.append(['NAME:PLPoint', 'X:=', '2.888444mm', 'Y:=', '1.641000mm', 'Z:=', '0.0mm'])
segs.append(['NAME:PLSegment', 'SegmentType:=', 'Line', 'StartIndex:=', 15, 'NoOfPoints:=', 2])
pts.append(['NAME:PLPoint', 'X:=', '2.888444mm', 'Y:=', '1.819000mm', 'Z:=', '0.0mm'])
segs.append(['NAME:PLSegment', 'SegmentType:=', 'Line', 'StartIndex:=', 16, 'NoOfPoints:=', 2])
pts.append(['NAME:PLPoint', 'X:=', '2.339556mm', 'Y:=', '1.819000mm', 'Z:=', '0.0mm'])
segs.append(['NAME:PLSegment', 'SegmentType:=', 'Line', 'StartIndex:=', 17, 'NoOfPoints:=', 2])
pts.append(['NAME:PLPoint', 'X:=', '2.339556mm', 'Y:=', '2.041000mm', 'Z:=', '0.0mm'])
segs.append(['NAME:PLSegment', 'SegmentType:=', 'Line', 'StartIndex:=', 18, 'NoOfPoints:=', 2])
pts.append(['NAME:PLPoint', 'X:=', '2.888444mm', 'Y:=', '2.041000mm', 'Z:=', '0.0mm'])
segs.append(['NAME:PLSegment', 'SegmentType:=', 'Line', 'StartIndex:=', 19, 'NoOfPoints:=', 2])
pts.append(['NAME:PLPoint', 'X:=', '2.888444mm', 'Y:=', '2.219000mm', 'Z:=', '0.0mm'])
segs.append(['NAME:PLSegment', 'SegmentType:=', 'Line', 'StartIndex:=', 20, 'NoOfPoints:=', 2])
pts.append(['NAME:PLPoint', 'X:=', '2.625000mm', 'Y:=', '2.219000mm', 'Z:=', '0.0mm'])
segs.append(['NAME:PLSegment', 'SegmentType:=', 'Line', 'StartIndex:=', 21, 'NoOfPoints:=', 2])
pts.append(['NAME:PLPoint', 'X:=', '2.625000mm', 'Y:=', '2.224500mm', 'Z:=', '0.0mm'])
segs.append(['NAME:PLSegment', 'SegmentType:=', 'Line', 'StartIndex:=', 22, 'NoOfPoints:=', 2])
pts.append(['NAME:PLPoint', 'X:=', '2.625500mm', 'Y:=', '2.225000mm', 'Z:=', '0.0mm'])
segs.append(['NAME:PLSegment', 'SegmentType:=', 'Line', 'StartIndex:=', 23, 'NoOfPoints:=', 2])
pts.append(['NAME:PLPoint', 'X:=', '2.614000mm', 'Y:=', '2.225000mm', 'Z:=', '0.0mm'])
segs.append(['NAME:PLSegment', 'SegmentType:=', 'Line', 'StartIndex:=', 24, 'NoOfPoints:=', 2])
pts.append(['NAME:PLPoint', 'X:=', '2.614000mm', 'Y:=', '2.241000mm', 'Z:=', '0.0mm'])
segs.append(['NAME:PLSegment', 'SegmentType:=', 'Line', 'StartIndex:=', 25, 'NoOfPoints:=', 2])
pts.append(['NAME:PLPoint', 'X:=', '2.910444mm', 'Y:=', '2.241000mm', 'Z:=', '0.0mm'])
segs.append(['NAME:PLSegment', 'SegmentType:=', 'Line', 'StartIndex:=', 26, 'NoOfPoints:=', 2])
pts.append(['NAME:PLPoint', 'X:=', '2.910444mm', 'Y:=', '2.019000mm', 'Z:=', '0.0mm'])
segs.append(['NAME:PLSegment', 'SegmentType:=', 'Line', 'StartIndex:=', 27, 'NoOfPoints:=', 2])
pts.append(['NAME:PLPoint', 'X:=', '2.361556mm', 'Y:=', '2.019000mm', 'Z:=', '0.0mm'])
segs.append(['NAME:PLSegment', 'SegmentType:=', 'Line', 'StartIndex:=', 28, 'NoOfPoints:=', 2])
pts.append(['NAME:PLPoint', 'X:=', '2.361556mm', 'Y:=', '1.841000mm', 'Z:=', '0.0mm'])
segs.append(['NAME:PLSegment', 'SegmentType:=', 'Line', 'StartIndex:=', 29, 'NoOfPoints:=', 2])
pts.append(['NAME:PLPoint', 'X:=', '2.910444mm', 'Y:=', '1.841000mm', 'Z:=', '0.0mm'])
segs.append(['NAME:PLSegment', 'SegmentType:=', 'Line', 'StartIndex:=', 30, 'NoOfPoints:=', 2])
pts.append(['NAME:PLPoint', 'X:=', '2.910444mm', 'Y:=', '1.619000mm', 'Z:=', '0.0mm'])
segs.append(['NAME:PLSegment', 'SegmentType:=', 'Line', 'StartIndex:=', 31, 'NoOfPoints:=', 2])
pts.append(['NAME:PLPoint', 'X:=', '2.361556mm', 'Y:=', '1.619000mm', 'Z:=', '0.0mm'])
segs.append(['NAME:PLSegment', 'SegmentType:=', 'Line', 'StartIndex:=', 32, 'NoOfPoints:=', 2])
pts.append(['NAME:PLPoint', 'X:=', '2.361556mm', 'Y:=', '1.441000mm', 'Z:=', '0.0mm'])
segs.append(['NAME:PLSegment', 'SegmentType:=', 'Line', 'StartIndex:=', 33, 'NoOfPoints:=', 2])
pts.append(['NAME:PLPoint', 'X:=', '2.910444mm', 'Y:=', '1.441000mm', 'Z:=', '0.0mm'])
segs.append(['NAME:PLSegment', 'SegmentType:=', 'Line', 'StartIndex:=', 34, 'NoOfPoints:=', 2])
pts.append(['NAME:PLPoint', 'X:=', '2.910444mm', 'Y:=', '1.219000mm', 'Z:=', '0.0mm'])
segs.append(['NAME:PLSegment', 'SegmentType:=', 'Line', 'StartIndex:=', 35, 'NoOfPoints:=', 2])
pts.append(['NAME:PLPoint', 'X:=', '2.361556mm', 'Y:=', '1.219000mm', 'Z:=', '0.0mm'])
segs.append(['NAME:PLSegment', 'SegmentType:=', 'Line', 'StartIndex:=', 36, 'NoOfPoints:=', 2])
pts.append(['NAME:PLPoint', 'X:=', '2.361556mm', 'Y:=', '1.041000mm', 'Z:=', '0.0mm'])
segs.append(['NAME:PLSegment', 'SegmentType:=', 'Line', 'StartIndex:=', 37, 'NoOfPoints:=', 2])
pts.append(['NAME:PLPoint', 'X:=', '2.910444mm', 'Y:=', '1.041000mm', 'Z:=', '0.0mm'])
segs.append(['NAME:PLSegment', 'SegmentType:=', 'Line', 'StartIndex:=', 38, 'NoOfPoints:=', 2])
pts.append(['NAME:PLPoint', 'X:=', '2.910444mm', 'Y:=', '0.819000mm', 'Z:=', '0.0mm'])
segs.append(['NAME:PLSegment', 'SegmentType:=', 'Line', 'StartIndex:=', 39, 'NoOfPoints:=', 2])
pts.append(['NAME:PLPoint', 'X:=', '2.361556mm', 'Y:=', '0.819000mm', 'Z:=', '0.0mm'])
segs.append(['NAME:PLSegment', 'SegmentType:=', 'Line', 'StartIndex:=', 40, 'NoOfPoints:=', 2])
pts.append(['NAME:PLPoint', 'X:=', '2.361556mm', 'Y:=', '0.641000mm', 'Z:=', '0.0mm'])
segs.append(['NAME:PLSegment', 'SegmentType:=', 'Line', 'StartIndex:=', 41, 'NoOfPoints:=', 2])
pts.append(['NAME:PLPoint', 'X:=', '2.910444mm', 'Y:=', '0.641000mm', 'Z:=', '0.0mm'])
segs.append(['NAME:PLSegment', 'SegmentType:=', 'Line', 'StartIndex:=', 42, 'NoOfPoints:=', 2])
pts.append(['NAME:PLPoint', 'X:=', '2.910444mm', 'Y:=', '0.419000mm', 'Z:=', '0.0mm'])
segs.append(['NAME:PLSegment', 'SegmentType:=', 'Line', 'StartIndex:=', 43, 'NoOfPoints:=', 2])
pts.append(['NAME:PLPoint', 'X:=', '2.375000mm', 'Y:=', '0.419000mm', 'Z:=', '0.0mm'])
segs.append(['NAME:PLSegment', 'SegmentType:=', 'Line', 'StartIndex:=', 44, 'NoOfPoints:=', 2])
pts.append(['NAME:PLPoint', 'X:=', '2.375000mm', 'Y:=', '0.424500mm', 'Z:=', '0.0mm'])
segs.append(['NAME:PLSegment', 'SegmentType:=', 'Line', 'StartIndex:=', 45, 'NoOfPoints:=', 2])
pts.append(['NAME:PLPoint', 'X:=', '2.375500mm', 'Y:=', '0.425000mm', 'Z:=', '0.0mm'])
oEditor.CreatePolyline(
    ['NAME:PolylineParameters', 'IsPolylineCovered:=', True, 'IsPolylineClosed:=', True, pts, segs],
    [
        'NAME:Attributes',
        'Name:=', 'cut_Bus_Q2_Q6_47',
        'Flags:=', '',
        'Color:=', '(255 100 100)',
        'Transparency:=', 0.0,
        'PartCoordinateSystem:=', 'Global',
        'UDMId:=', '',
        'MaterialName:=', 'vacuum',
        'SolveInside:=', True
    ]
)
# Element: trace_Readout_Q0_48
pts = ['NAME:PolylinePoints']
segs = ['NAME:PolylineSegments']
pts.append(['NAME:PLPoint', 'X:=', '-2.370000mm', 'Y:=', '-0.425000mm', 'Z:=', '0.0mm'])
segs.append(['NAME:PLSegment', 'SegmentType:=', 'Line', 'StartIndex:=', 0, 'NoOfPoints:=', 2])
pts.append(['NAME:PLPoint', 'X:=', '-1.989643mm', 'Y:=', '-0.425000mm', 'Z:=', '0.0mm'])
segs.append(['NAME:PLSegment', 'SegmentType:=', 'Line', 'StartIndex:=', 1, 'NoOfPoints:=', 2])
pts.append(['NAME:PLPoint', 'X:=', '-1.989643mm', 'Y:=', '-0.635000mm', 'Z:=', '0.0mm'])
segs.append(['NAME:PLSegment', 'SegmentType:=', 'Line', 'StartIndex:=', 2, 'NoOfPoints:=', 2])
pts.append(['NAME:PLPoint', 'X:=', '-2.750357mm', 'Y:=', '-0.635000mm', 'Z:=', '0.0mm'])
segs.append(['NAME:PLSegment', 'SegmentType:=', 'Line', 'StartIndex:=', 3, 'NoOfPoints:=', 2])
pts.append(['NAME:PLPoint', 'X:=', '-2.750357mm', 'Y:=', '-0.825000mm', 'Z:=', '0.0mm'])
segs.append(['NAME:PLSegment', 'SegmentType:=', 'Line', 'StartIndex:=', 4, 'NoOfPoints:=', 2])
pts.append(['NAME:PLPoint', 'X:=', '-1.989643mm', 'Y:=', '-0.825000mm', 'Z:=', '0.0mm'])
segs.append(['NAME:PLSegment', 'SegmentType:=', 'Line', 'StartIndex:=', 5, 'NoOfPoints:=', 2])
pts.append(['NAME:PLPoint', 'X:=', '-1.989643mm', 'Y:=', '-1.035000mm', 'Z:=', '0.0mm'])
segs.append(['NAME:PLSegment', 'SegmentType:=', 'Line', 'StartIndex:=', 6, 'NoOfPoints:=', 2])
pts.append(['NAME:PLPoint', 'X:=', '-2.750357mm', 'Y:=', '-1.035000mm', 'Z:=', '0.0mm'])
segs.append(['NAME:PLSegment', 'SegmentType:=', 'Line', 'StartIndex:=', 7, 'NoOfPoints:=', 2])
pts.append(['NAME:PLPoint', 'X:=', '-2.750357mm', 'Y:=', '-1.225000mm', 'Z:=', '0.0mm'])
segs.append(['NAME:PLSegment', 'SegmentType:=', 'Line', 'StartIndex:=', 8, 'NoOfPoints:=', 2])
pts.append(['NAME:PLPoint', 'X:=', '-1.989643mm', 'Y:=', '-1.225000mm', 'Z:=', '0.0mm'])
segs.append(['NAME:PLSegment', 'SegmentType:=', 'Line', 'StartIndex:=', 9, 'NoOfPoints:=', 2])
pts.append(['NAME:PLPoint', 'X:=', '-1.989643mm', 'Y:=', '-1.435000mm', 'Z:=', '0.0mm'])
segs.append(['NAME:PLSegment', 'SegmentType:=', 'Line', 'StartIndex:=', 10, 'NoOfPoints:=', 2])
pts.append(['NAME:PLPoint', 'X:=', '-2.750357mm', 'Y:=', '-1.435000mm', 'Z:=', '0.0mm'])
segs.append(['NAME:PLSegment', 'SegmentType:=', 'Line', 'StartIndex:=', 11, 'NoOfPoints:=', 2])
pts.append(['NAME:PLPoint', 'X:=', '-2.750357mm', 'Y:=', '-1.625000mm', 'Z:=', '0.0mm'])
segs.append(['NAME:PLSegment', 'SegmentType:=', 'Line', 'StartIndex:=', 12, 'NoOfPoints:=', 2])
pts.append(['NAME:PLPoint', 'X:=', '-1.989643mm', 'Y:=', '-1.625000mm', 'Z:=', '0.0mm'])
segs.append(['NAME:PLSegment', 'SegmentType:=', 'Line', 'StartIndex:=', 13, 'NoOfPoints:=', 2])
pts.append(['NAME:PLPoint', 'X:=', '-1.989643mm', 'Y:=', '-1.835000mm', 'Z:=', '0.0mm'])
segs.append(['NAME:PLSegment', 'SegmentType:=', 'Line', 'StartIndex:=', 14, 'NoOfPoints:=', 2])
pts.append(['NAME:PLPoint', 'X:=', '-2.495000mm', 'Y:=', '-1.835000mm', 'Z:=', '0.0mm'])
segs.append(['NAME:PLSegment', 'SegmentType:=', 'Line', 'StartIndex:=', 15, 'NoOfPoints:=', 2])
pts.append(['NAME:PLPoint', 'X:=', '-2.495000mm', 'Y:=', '-1.975000mm', 'Z:=', '0.0mm'])
segs.append(['NAME:PLSegment', 'SegmentType:=', 'Line', 'StartIndex:=', 16, 'NoOfPoints:=', 2])
pts.append(['NAME:PLPoint', 'X:=', '-2.505000mm', 'Y:=', '-1.975000mm', 'Z:=', '0.0mm'])
segs.append(['NAME:PLSegment', 'SegmentType:=', 'Line', 'StartIndex:=', 17, 'NoOfPoints:=', 2])
pts.append(['NAME:PLPoint', 'X:=', '-2.505000mm', 'Y:=', '-1.825000mm', 'Z:=', '0.0mm'])
segs.append(['NAME:PLSegment', 'SegmentType:=', 'Line', 'StartIndex:=', 18, 'NoOfPoints:=', 2])
pts.append(['NAME:PLPoint', 'X:=', '-1.999643mm', 'Y:=', '-1.825000mm', 'Z:=', '0.0mm'])
segs.append(['NAME:PLSegment', 'SegmentType:=', 'Line', 'StartIndex:=', 19, 'NoOfPoints:=', 2])
pts.append(['NAME:PLPoint', 'X:=', '-1.999643mm', 'Y:=', '-1.635000mm', 'Z:=', '0.0mm'])
segs.append(['NAME:PLSegment', 'SegmentType:=', 'Line', 'StartIndex:=', 20, 'NoOfPoints:=', 2])
pts.append(['NAME:PLPoint', 'X:=', '-2.760357mm', 'Y:=', '-1.635000mm', 'Z:=', '0.0mm'])
segs.append(['NAME:PLSegment', 'SegmentType:=', 'Line', 'StartIndex:=', 21, 'NoOfPoints:=', 2])
pts.append(['NAME:PLPoint', 'X:=', '-2.760357mm', 'Y:=', '-1.425000mm', 'Z:=', '0.0mm'])
segs.append(['NAME:PLSegment', 'SegmentType:=', 'Line', 'StartIndex:=', 22, 'NoOfPoints:=', 2])
pts.append(['NAME:PLPoint', 'X:=', '-1.999643mm', 'Y:=', '-1.425000mm', 'Z:=', '0.0mm'])
segs.append(['NAME:PLSegment', 'SegmentType:=', 'Line', 'StartIndex:=', 23, 'NoOfPoints:=', 2])
pts.append(['NAME:PLPoint', 'X:=', '-1.999643mm', 'Y:=', '-1.235000mm', 'Z:=', '0.0mm'])
segs.append(['NAME:PLSegment', 'SegmentType:=', 'Line', 'StartIndex:=', 24, 'NoOfPoints:=', 2])
pts.append(['NAME:PLPoint', 'X:=', '-2.760357mm', 'Y:=', '-1.235000mm', 'Z:=', '0.0mm'])
segs.append(['NAME:PLSegment', 'SegmentType:=', 'Line', 'StartIndex:=', 25, 'NoOfPoints:=', 2])
pts.append(['NAME:PLPoint', 'X:=', '-2.760357mm', 'Y:=', '-1.025000mm', 'Z:=', '0.0mm'])
segs.append(['NAME:PLSegment', 'SegmentType:=', 'Line', 'StartIndex:=', 26, 'NoOfPoints:=', 2])
pts.append(['NAME:PLPoint', 'X:=', '-1.999643mm', 'Y:=', '-1.025000mm', 'Z:=', '0.0mm'])
segs.append(['NAME:PLSegment', 'SegmentType:=', 'Line', 'StartIndex:=', 27, 'NoOfPoints:=', 2])
pts.append(['NAME:PLPoint', 'X:=', '-1.999643mm', 'Y:=', '-0.835000mm', 'Z:=', '0.0mm'])
segs.append(['NAME:PLSegment', 'SegmentType:=', 'Line', 'StartIndex:=', 28, 'NoOfPoints:=', 2])
pts.append(['NAME:PLPoint', 'X:=', '-2.760357mm', 'Y:=', '-0.835000mm', 'Z:=', '0.0mm'])
segs.append(['NAME:PLSegment', 'SegmentType:=', 'Line', 'StartIndex:=', 29, 'NoOfPoints:=', 2])
pts.append(['NAME:PLPoint', 'X:=', '-2.760357mm', 'Y:=', '-0.625000mm', 'Z:=', '0.0mm'])
segs.append(['NAME:PLSegment', 'SegmentType:=', 'Line', 'StartIndex:=', 30, 'NoOfPoints:=', 2])
pts.append(['NAME:PLPoint', 'X:=', '-1.999643mm', 'Y:=', '-0.625000mm', 'Z:=', '0.0mm'])
segs.append(['NAME:PLSegment', 'SegmentType:=', 'Line', 'StartIndex:=', 31, 'NoOfPoints:=', 2])
pts.append(['NAME:PLPoint', 'X:=', '-1.999643mm', 'Y:=', '-0.435000mm', 'Z:=', '0.0mm'])
segs.append(['NAME:PLSegment', 'SegmentType:=', 'Line', 'StartIndex:=', 32, 'NoOfPoints:=', 2])
pts.append(['NAME:PLPoint', 'X:=', '-2.380000mm', 'Y:=', '-0.435000mm', 'Z:=', '0.0mm'])
segs.append(['NAME:PLSegment', 'SegmentType:=', 'Line', 'StartIndex:=', 33, 'NoOfPoints:=', 2])
pts.append(['NAME:PLPoint', 'X:=', '-2.380000mm', 'Y:=', '-0.425000mm', 'Z:=', '0.0mm'])
segs.append(['NAME:PLSegment', 'SegmentType:=', 'Line', 'StartIndex:=', 34, 'NoOfPoints:=', 2])
pts.append(['NAME:PLPoint', 'X:=', '-2.370000mm', 'Y:=', '-0.425000mm', 'Z:=', '0.0mm'])
oEditor.CreatePolyline(
    ['NAME:PolylineParameters', 'IsPolylineCovered:=', True, 'IsPolylineClosed:=', True, pts, segs],
    [
        'NAME:Attributes',
        'Name:=', 'trace_Readout_Q0_48',
        'Flags:=', '',
        'Color:=', '(200 220 255)',
        'Transparency:=', 0.0,
        'PartCoordinateSystem:=', 'Global',
        'UDMId:=', '',
        'MaterialName:=', 'vacuum',
        'SolveInside:=', True
    ]
)
# Element: cut_Readout_Q0_49
pts = ['NAME:PolylinePoints']
segs = ['NAME:PolylineSegments']
pts.append(['NAME:PLPoint', 'X:=', '-2.374500mm', 'Y:=', '-0.425000mm', 'Z:=', '0.0mm'])
segs.append(['NAME:PLSegment', 'SegmentType:=', 'Line', 'StartIndex:=', 0, 'NoOfPoints:=', 2])
pts.append(['NAME:PLPoint', 'X:=', '-2.375000mm', 'Y:=', '-0.424500mm', 'Z:=', '0.0mm'])
segs.append(['NAME:PLSegment', 'SegmentType:=', 'Line', 'StartIndex:=', 1, 'NoOfPoints:=', 2])
pts.append(['NAME:PLPoint', 'X:=', '-2.375000mm', 'Y:=', '-0.419000mm', 'Z:=', '0.0mm'])
segs.append(['NAME:PLSegment', 'SegmentType:=', 'Line', 'StartIndex:=', 2, 'NoOfPoints:=', 2])
pts.append(['NAME:PLPoint', 'X:=', '-1.983643mm', 'Y:=', '-0.419000mm', 'Z:=', '0.0mm'])
segs.append(['NAME:PLSegment', 'SegmentType:=', 'Line', 'StartIndex:=', 3, 'NoOfPoints:=', 2])
pts.append(['NAME:PLPoint', 'X:=', '-1.983643mm', 'Y:=', '-0.641000mm', 'Z:=', '0.0mm'])
segs.append(['NAME:PLSegment', 'SegmentType:=', 'Line', 'StartIndex:=', 4, 'NoOfPoints:=', 2])
pts.append(['NAME:PLPoint', 'X:=', '-2.744357mm', 'Y:=', '-0.641000mm', 'Z:=', '0.0mm'])
segs.append(['NAME:PLSegment', 'SegmentType:=', 'Line', 'StartIndex:=', 5, 'NoOfPoints:=', 2])
pts.append(['NAME:PLPoint', 'X:=', '-2.744357mm', 'Y:=', '-0.819000mm', 'Z:=', '0.0mm'])
segs.append(['NAME:PLSegment', 'SegmentType:=', 'Line', 'StartIndex:=', 6, 'NoOfPoints:=', 2])
pts.append(['NAME:PLPoint', 'X:=', '-1.983643mm', 'Y:=', '-0.819000mm', 'Z:=', '0.0mm'])
segs.append(['NAME:PLSegment', 'SegmentType:=', 'Line', 'StartIndex:=', 7, 'NoOfPoints:=', 2])
pts.append(['NAME:PLPoint', 'X:=', '-1.983643mm', 'Y:=', '-1.041000mm', 'Z:=', '0.0mm'])
segs.append(['NAME:PLSegment', 'SegmentType:=', 'Line', 'StartIndex:=', 8, 'NoOfPoints:=', 2])
pts.append(['NAME:PLPoint', 'X:=', '-2.744357mm', 'Y:=', '-1.041000mm', 'Z:=', '0.0mm'])
segs.append(['NAME:PLSegment', 'SegmentType:=', 'Line', 'StartIndex:=', 9, 'NoOfPoints:=', 2])
pts.append(['NAME:PLPoint', 'X:=', '-2.744357mm', 'Y:=', '-1.219000mm', 'Z:=', '0.0mm'])
segs.append(['NAME:PLSegment', 'SegmentType:=', 'Line', 'StartIndex:=', 10, 'NoOfPoints:=', 2])
pts.append(['NAME:PLPoint', 'X:=', '-1.983643mm', 'Y:=', '-1.219000mm', 'Z:=', '0.0mm'])
segs.append(['NAME:PLSegment', 'SegmentType:=', 'Line', 'StartIndex:=', 11, 'NoOfPoints:=', 2])
pts.append(['NAME:PLPoint', 'X:=', '-1.983643mm', 'Y:=', '-1.441000mm', 'Z:=', '0.0mm'])
segs.append(['NAME:PLSegment', 'SegmentType:=', 'Line', 'StartIndex:=', 12, 'NoOfPoints:=', 2])
pts.append(['NAME:PLPoint', 'X:=', '-2.744357mm', 'Y:=', '-1.441000mm', 'Z:=', '0.0mm'])
segs.append(['NAME:PLSegment', 'SegmentType:=', 'Line', 'StartIndex:=', 13, 'NoOfPoints:=', 2])
pts.append(['NAME:PLPoint', 'X:=', '-2.744357mm', 'Y:=', '-1.619000mm', 'Z:=', '0.0mm'])
segs.append(['NAME:PLSegment', 'SegmentType:=', 'Line', 'StartIndex:=', 14, 'NoOfPoints:=', 2])
pts.append(['NAME:PLPoint', 'X:=', '-1.983643mm', 'Y:=', '-1.619000mm', 'Z:=', '0.0mm'])
segs.append(['NAME:PLSegment', 'SegmentType:=', 'Line', 'StartIndex:=', 15, 'NoOfPoints:=', 2])
pts.append(['NAME:PLPoint', 'X:=', '-1.983643mm', 'Y:=', '-1.841000mm', 'Z:=', '0.0mm'])
segs.append(['NAME:PLSegment', 'SegmentType:=', 'Line', 'StartIndex:=', 16, 'NoOfPoints:=', 2])
pts.append(['NAME:PLPoint', 'X:=', '-2.489000mm', 'Y:=', '-1.841000mm', 'Z:=', '0.0mm'])
segs.append(['NAME:PLSegment', 'SegmentType:=', 'Line', 'StartIndex:=', 17, 'NoOfPoints:=', 2])
pts.append(['NAME:PLPoint', 'X:=', '-2.489000mm', 'Y:=', '-1.975000mm', 'Z:=', '0.0mm'])
segs.append(['NAME:PLSegment', 'SegmentType:=', 'Line', 'StartIndex:=', 18, 'NoOfPoints:=', 2])
pts.append(['NAME:PLPoint', 'X:=', '-2.511000mm', 'Y:=', '-1.975000mm', 'Z:=', '0.0mm'])
segs.append(['NAME:PLSegment', 'SegmentType:=', 'Line', 'StartIndex:=', 19, 'NoOfPoints:=', 2])
pts.append(['NAME:PLPoint', 'X:=', '-2.511000mm', 'Y:=', '-1.819000mm', 'Z:=', '0.0mm'])
segs.append(['NAME:PLSegment', 'SegmentType:=', 'Line', 'StartIndex:=', 20, 'NoOfPoints:=', 2])
pts.append(['NAME:PLPoint', 'X:=', '-2.005643mm', 'Y:=', '-1.819000mm', 'Z:=', '0.0mm'])
segs.append(['NAME:PLSegment', 'SegmentType:=', 'Line', 'StartIndex:=', 21, 'NoOfPoints:=', 2])
pts.append(['NAME:PLPoint', 'X:=', '-2.005643mm', 'Y:=', '-1.641000mm', 'Z:=', '0.0mm'])
segs.append(['NAME:PLSegment', 'SegmentType:=', 'Line', 'StartIndex:=', 22, 'NoOfPoints:=', 2])
pts.append(['NAME:PLPoint', 'X:=', '-2.766357mm', 'Y:=', '-1.641000mm', 'Z:=', '0.0mm'])
segs.append(['NAME:PLSegment', 'SegmentType:=', 'Line', 'StartIndex:=', 23, 'NoOfPoints:=', 2])
pts.append(['NAME:PLPoint', 'X:=', '-2.766357mm', 'Y:=', '-1.419000mm', 'Z:=', '0.0mm'])
segs.append(['NAME:PLSegment', 'SegmentType:=', 'Line', 'StartIndex:=', 24, 'NoOfPoints:=', 2])
pts.append(['NAME:PLPoint', 'X:=', '-2.005643mm', 'Y:=', '-1.419000mm', 'Z:=', '0.0mm'])
segs.append(['NAME:PLSegment', 'SegmentType:=', 'Line', 'StartIndex:=', 25, 'NoOfPoints:=', 2])
pts.append(['NAME:PLPoint', 'X:=', '-2.005643mm', 'Y:=', '-1.241000mm', 'Z:=', '0.0mm'])
segs.append(['NAME:PLSegment', 'SegmentType:=', 'Line', 'StartIndex:=', 26, 'NoOfPoints:=', 2])
pts.append(['NAME:PLPoint', 'X:=', '-2.766357mm', 'Y:=', '-1.241000mm', 'Z:=', '0.0mm'])
segs.append(['NAME:PLSegment', 'SegmentType:=', 'Line', 'StartIndex:=', 27, 'NoOfPoints:=', 2])
pts.append(['NAME:PLPoint', 'X:=', '-2.766357mm', 'Y:=', '-1.019000mm', 'Z:=', '0.0mm'])
segs.append(['NAME:PLSegment', 'SegmentType:=', 'Line', 'StartIndex:=', 28, 'NoOfPoints:=', 2])
pts.append(['NAME:PLPoint', 'X:=', '-2.005643mm', 'Y:=', '-1.019000mm', 'Z:=', '0.0mm'])
segs.append(['NAME:PLSegment', 'SegmentType:=', 'Line', 'StartIndex:=', 29, 'NoOfPoints:=', 2])
pts.append(['NAME:PLPoint', 'X:=', '-2.005643mm', 'Y:=', '-0.841000mm', 'Z:=', '0.0mm'])
segs.append(['NAME:PLSegment', 'SegmentType:=', 'Line', 'StartIndex:=', 30, 'NoOfPoints:=', 2])
pts.append(['NAME:PLPoint', 'X:=', '-2.766357mm', 'Y:=', '-0.841000mm', 'Z:=', '0.0mm'])
segs.append(['NAME:PLSegment', 'SegmentType:=', 'Line', 'StartIndex:=', 31, 'NoOfPoints:=', 2])
pts.append(['NAME:PLPoint', 'X:=', '-2.766357mm', 'Y:=', '-0.619000mm', 'Z:=', '0.0mm'])
segs.append(['NAME:PLSegment', 'SegmentType:=', 'Line', 'StartIndex:=', 32, 'NoOfPoints:=', 2])
pts.append(['NAME:PLPoint', 'X:=', '-2.005643mm', 'Y:=', '-0.619000mm', 'Z:=', '0.0mm'])
segs.append(['NAME:PLSegment', 'SegmentType:=', 'Line', 'StartIndex:=', 33, 'NoOfPoints:=', 2])
pts.append(['NAME:PLPoint', 'X:=', '-2.005643mm', 'Y:=', '-0.441000mm', 'Z:=', '0.0mm'])
segs.append(['NAME:PLSegment', 'SegmentType:=', 'Line', 'StartIndex:=', 34, 'NoOfPoints:=', 2])
pts.append(['NAME:PLPoint', 'X:=', '-2.386000mm', 'Y:=', '-0.441000mm', 'Z:=', '0.0mm'])
segs.append(['NAME:PLSegment', 'SegmentType:=', 'Line', 'StartIndex:=', 35, 'NoOfPoints:=', 2])
pts.append(['NAME:PLPoint', 'X:=', '-2.386000mm', 'Y:=', '-0.425000mm', 'Z:=', '0.0mm'])
segs.append(['NAME:PLSegment', 'SegmentType:=', 'Line', 'StartIndex:=', 36, 'NoOfPoints:=', 2])
pts.append(['NAME:PLPoint', 'X:=', '-2.374500mm', 'Y:=', '-0.425000mm', 'Z:=', '0.0mm'])
oEditor.CreatePolyline(
    ['NAME:PolylineParameters', 'IsPolylineCovered:=', True, 'IsPolylineClosed:=', True, pts, segs],
    [
        'NAME:Attributes',
        'Name:=', 'cut_Readout_Q0_49',
        'Flags:=', '',
        'Color:=', '(255 100 100)',
        'Transparency:=', 0.0,
        'PartCoordinateSystem:=', 'Global',
        'UDMId:=', '',
        'MaterialName:=', 'vacuum',
        'SolveInside:=', True
    ]
)
# Element: trace_Readout_Q1_50
pts = ['NAME:PolylinePoints']
segs = ['NAME:PolylineSegments']
pts.append(['NAME:PLPoint', 'X:=', '-2.630000mm', 'Y:=', '2.225000mm', 'Z:=', '0.0mm'])
segs.append(['NAME:PLSegment', 'SegmentType:=', 'Line', 'StartIndex:=', 0, 'NoOfPoints:=', 2])
pts.append(['NAME:PLPoint', 'X:=', '-2.965937mm', 'Y:=', '2.225000mm', 'Z:=', '0.0mm'])
segs.append(['NAME:PLSegment', 'SegmentType:=', 'Line', 'StartIndex:=', 1, 'NoOfPoints:=', 2])
pts.append(['NAME:PLPoint', 'X:=', '-2.965937mm', 'Y:=', '2.435000mm', 'Z:=', '0.0mm'])
segs.append(['NAME:PLSegment', 'SegmentType:=', 'Line', 'StartIndex:=', 2, 'NoOfPoints:=', 2])
pts.append(['NAME:PLPoint', 'X:=', '-2.294062mm', 'Y:=', '2.435000mm', 'Z:=', '0.0mm'])
segs.append(['NAME:PLSegment', 'SegmentType:=', 'Line', 'StartIndex:=', 3, 'NoOfPoints:=', 2])
pts.append(['NAME:PLPoint', 'X:=', '-2.294062mm', 'Y:=', '2.625000mm', 'Z:=', '0.0mm'])
segs.append(['NAME:PLSegment', 'SegmentType:=', 'Line', 'StartIndex:=', 4, 'NoOfPoints:=', 2])
pts.append(['NAME:PLPoint', 'X:=', '-2.965937mm', 'Y:=', '2.625000mm', 'Z:=', '0.0mm'])
segs.append(['NAME:PLSegment', 'SegmentType:=', 'Line', 'StartIndex:=', 5, 'NoOfPoints:=', 2])
pts.append(['NAME:PLPoint', 'X:=', '-2.965937mm', 'Y:=', '2.835000mm', 'Z:=', '0.0mm'])
segs.append(['NAME:PLSegment', 'SegmentType:=', 'Line', 'StartIndex:=', 6, 'NoOfPoints:=', 2])
pts.append(['NAME:PLPoint', 'X:=', '-2.294062mm', 'Y:=', '2.835000mm', 'Z:=', '0.0mm'])
segs.append(['NAME:PLSegment', 'SegmentType:=', 'Line', 'StartIndex:=', 7, 'NoOfPoints:=', 2])
pts.append(['NAME:PLPoint', 'X:=', '-2.294062mm', 'Y:=', '3.025000mm', 'Z:=', '0.0mm'])
segs.append(['NAME:PLSegment', 'SegmentType:=', 'Line', 'StartIndex:=', 8, 'NoOfPoints:=', 2])
pts.append(['NAME:PLPoint', 'X:=', '-2.965937mm', 'Y:=', '3.025000mm', 'Z:=', '0.0mm'])
segs.append(['NAME:PLSegment', 'SegmentType:=', 'Line', 'StartIndex:=', 9, 'NoOfPoints:=', 2])
pts.append(['NAME:PLPoint', 'X:=', '-2.965937mm', 'Y:=', '3.235000mm', 'Z:=', '0.0mm'])
segs.append(['NAME:PLSegment', 'SegmentType:=', 'Line', 'StartIndex:=', 10, 'NoOfPoints:=', 2])
pts.append(['NAME:PLPoint', 'X:=', '-2.294062mm', 'Y:=', '3.235000mm', 'Z:=', '0.0mm'])
segs.append(['NAME:PLSegment', 'SegmentType:=', 'Line', 'StartIndex:=', 11, 'NoOfPoints:=', 2])
pts.append(['NAME:PLPoint', 'X:=', '-2.294062mm', 'Y:=', '3.425000mm', 'Z:=', '0.0mm'])
segs.append(['NAME:PLSegment', 'SegmentType:=', 'Line', 'StartIndex:=', 12, 'NoOfPoints:=', 2])
pts.append(['NAME:PLPoint', 'X:=', '-2.965937mm', 'Y:=', '3.425000mm', 'Z:=', '0.0mm'])
segs.append(['NAME:PLSegment', 'SegmentType:=', 'Line', 'StartIndex:=', 13, 'NoOfPoints:=', 2])
pts.append(['NAME:PLPoint', 'X:=', '-2.965937mm', 'Y:=', '3.635000mm', 'Z:=', '0.0mm'])
segs.append(['NAME:PLSegment', 'SegmentType:=', 'Line', 'StartIndex:=', 14, 'NoOfPoints:=', 2])
pts.append(['NAME:PLPoint', 'X:=', '-2.294062mm', 'Y:=', '3.635000mm', 'Z:=', '0.0mm'])
segs.append(['NAME:PLSegment', 'SegmentType:=', 'Line', 'StartIndex:=', 15, 'NoOfPoints:=', 2])
pts.append(['NAME:PLPoint', 'X:=', '-2.294062mm', 'Y:=', '3.825000mm', 'Z:=', '0.0mm'])
segs.append(['NAME:PLSegment', 'SegmentType:=', 'Line', 'StartIndex:=', 16, 'NoOfPoints:=', 2])
pts.append(['NAME:PLPoint', 'X:=', '-2.505000mm', 'Y:=', '3.825000mm', 'Z:=', '0.0mm'])
segs.append(['NAME:PLSegment', 'SegmentType:=', 'Line', 'StartIndex:=', 17, 'NoOfPoints:=', 2])
pts.append(['NAME:PLPoint', 'X:=', '-2.505000mm', 'Y:=', '3.975000mm', 'Z:=', '0.0mm'])
segs.append(['NAME:PLSegment', 'SegmentType:=', 'Line', 'StartIndex:=', 18, 'NoOfPoints:=', 2])
pts.append(['NAME:PLPoint', 'X:=', '-2.495000mm', 'Y:=', '3.975000mm', 'Z:=', '0.0mm'])
segs.append(['NAME:PLSegment', 'SegmentType:=', 'Line', 'StartIndex:=', 19, 'NoOfPoints:=', 2])
pts.append(['NAME:PLPoint', 'X:=', '-2.495000mm', 'Y:=', '3.835000mm', 'Z:=', '0.0mm'])
segs.append(['NAME:PLSegment', 'SegmentType:=', 'Line', 'StartIndex:=', 20, 'NoOfPoints:=', 2])
pts.append(['NAME:PLPoint', 'X:=', '-2.284063mm', 'Y:=', '3.835000mm', 'Z:=', '0.0mm'])
segs.append(['NAME:PLSegment', 'SegmentType:=', 'Line', 'StartIndex:=', 21, 'NoOfPoints:=', 2])
pts.append(['NAME:PLPoint', 'X:=', '-2.284063mm', 'Y:=', '3.625000mm', 'Z:=', '0.0mm'])
segs.append(['NAME:PLSegment', 'SegmentType:=', 'Line', 'StartIndex:=', 22, 'NoOfPoints:=', 2])
pts.append(['NAME:PLPoint', 'X:=', '-2.955938mm', 'Y:=', '3.625000mm', 'Z:=', '0.0mm'])
segs.append(['NAME:PLSegment', 'SegmentType:=', 'Line', 'StartIndex:=', 23, 'NoOfPoints:=', 2])
pts.append(['NAME:PLPoint', 'X:=', '-2.955938mm', 'Y:=', '3.435000mm', 'Z:=', '0.0mm'])
segs.append(['NAME:PLSegment', 'SegmentType:=', 'Line', 'StartIndex:=', 24, 'NoOfPoints:=', 2])
pts.append(['NAME:PLPoint', 'X:=', '-2.284063mm', 'Y:=', '3.435000mm', 'Z:=', '0.0mm'])
segs.append(['NAME:PLSegment', 'SegmentType:=', 'Line', 'StartIndex:=', 25, 'NoOfPoints:=', 2])
pts.append(['NAME:PLPoint', 'X:=', '-2.284063mm', 'Y:=', '3.225000mm', 'Z:=', '0.0mm'])
segs.append(['NAME:PLSegment', 'SegmentType:=', 'Line', 'StartIndex:=', 26, 'NoOfPoints:=', 2])
pts.append(['NAME:PLPoint', 'X:=', '-2.955938mm', 'Y:=', '3.225000mm', 'Z:=', '0.0mm'])
segs.append(['NAME:PLSegment', 'SegmentType:=', 'Line', 'StartIndex:=', 27, 'NoOfPoints:=', 2])
pts.append(['NAME:PLPoint', 'X:=', '-2.955938mm', 'Y:=', '3.035000mm', 'Z:=', '0.0mm'])
segs.append(['NAME:PLSegment', 'SegmentType:=', 'Line', 'StartIndex:=', 28, 'NoOfPoints:=', 2])
pts.append(['NAME:PLPoint', 'X:=', '-2.284063mm', 'Y:=', '3.035000mm', 'Z:=', '0.0mm'])
segs.append(['NAME:PLSegment', 'SegmentType:=', 'Line', 'StartIndex:=', 29, 'NoOfPoints:=', 2])
pts.append(['NAME:PLPoint', 'X:=', '-2.284063mm', 'Y:=', '2.825000mm', 'Z:=', '0.0mm'])
segs.append(['NAME:PLSegment', 'SegmentType:=', 'Line', 'StartIndex:=', 30, 'NoOfPoints:=', 2])
pts.append(['NAME:PLPoint', 'X:=', '-2.955938mm', 'Y:=', '2.825000mm', 'Z:=', '0.0mm'])
segs.append(['NAME:PLSegment', 'SegmentType:=', 'Line', 'StartIndex:=', 31, 'NoOfPoints:=', 2])
pts.append(['NAME:PLPoint', 'X:=', '-2.955938mm', 'Y:=', '2.635000mm', 'Z:=', '0.0mm'])
segs.append(['NAME:PLSegment', 'SegmentType:=', 'Line', 'StartIndex:=', 32, 'NoOfPoints:=', 2])
pts.append(['NAME:PLPoint', 'X:=', '-2.284063mm', 'Y:=', '2.635000mm', 'Z:=', '0.0mm'])
segs.append(['NAME:PLSegment', 'SegmentType:=', 'Line', 'StartIndex:=', 33, 'NoOfPoints:=', 2])
pts.append(['NAME:PLPoint', 'X:=', '-2.284063mm', 'Y:=', '2.425000mm', 'Z:=', '0.0mm'])
segs.append(['NAME:PLSegment', 'SegmentType:=', 'Line', 'StartIndex:=', 34, 'NoOfPoints:=', 2])
pts.append(['NAME:PLPoint', 'X:=', '-2.955938mm', 'Y:=', '2.425000mm', 'Z:=', '0.0mm'])
segs.append(['NAME:PLSegment', 'SegmentType:=', 'Line', 'StartIndex:=', 35, 'NoOfPoints:=', 2])
pts.append(['NAME:PLPoint', 'X:=', '-2.955938mm', 'Y:=', '2.235000mm', 'Z:=', '0.0mm'])
segs.append(['NAME:PLSegment', 'SegmentType:=', 'Line', 'StartIndex:=', 36, 'NoOfPoints:=', 2])
pts.append(['NAME:PLPoint', 'X:=', '-2.620000mm', 'Y:=', '2.235000mm', 'Z:=', '0.0mm'])
segs.append(['NAME:PLSegment', 'SegmentType:=', 'Line', 'StartIndex:=', 37, 'NoOfPoints:=', 2])
pts.append(['NAME:PLPoint', 'X:=', '-2.620000mm', 'Y:=', '2.225000mm', 'Z:=', '0.0mm'])
segs.append(['NAME:PLSegment', 'SegmentType:=', 'Line', 'StartIndex:=', 38, 'NoOfPoints:=', 2])
pts.append(['NAME:PLPoint', 'X:=', '-2.630000mm', 'Y:=', '2.225000mm', 'Z:=', '0.0mm'])
oEditor.CreatePolyline(
    ['NAME:PolylineParameters', 'IsPolylineCovered:=', True, 'IsPolylineClosed:=', True, pts, segs],
    [
        'NAME:Attributes',
        'Name:=', 'trace_Readout_Q1_50',
        'Flags:=', '',
        'Color:=', '(200 220 255)',
        'Transparency:=', 0.0,
        'PartCoordinateSystem:=', 'Global',
        'UDMId:=', '',
        'MaterialName:=', 'vacuum',
        'SolveInside:=', True
    ]
)
# Element: cut_Readout_Q1_51
pts = ['NAME:PolylinePoints']
segs = ['NAME:PolylineSegments']
pts.append(['NAME:PLPoint', 'X:=', '-2.625500mm', 'Y:=', '2.225000mm', 'Z:=', '0.0mm'])
segs.append(['NAME:PLSegment', 'SegmentType:=', 'Line', 'StartIndex:=', 0, 'NoOfPoints:=', 2])
pts.append(['NAME:PLPoint', 'X:=', '-2.625000mm', 'Y:=', '2.224500mm', 'Z:=', '0.0mm'])
segs.append(['NAME:PLSegment', 'SegmentType:=', 'Line', 'StartIndex:=', 1, 'NoOfPoints:=', 2])
pts.append(['NAME:PLPoint', 'X:=', '-2.625000mm', 'Y:=', '2.219000mm', 'Z:=', '0.0mm'])
segs.append(['NAME:PLSegment', 'SegmentType:=', 'Line', 'StartIndex:=', 2, 'NoOfPoints:=', 2])
pts.append(['NAME:PLPoint', 'X:=', '-2.971938mm', 'Y:=', '2.219000mm', 'Z:=', '0.0mm'])
segs.append(['NAME:PLSegment', 'SegmentType:=', 'Line', 'StartIndex:=', 3, 'NoOfPoints:=', 2])
pts.append(['NAME:PLPoint', 'X:=', '-2.971938mm', 'Y:=', '2.441000mm', 'Z:=', '0.0mm'])
segs.append(['NAME:PLSegment', 'SegmentType:=', 'Line', 'StartIndex:=', 4, 'NoOfPoints:=', 2])
pts.append(['NAME:PLPoint', 'X:=', '-2.300063mm', 'Y:=', '2.441000mm', 'Z:=', '0.0mm'])
segs.append(['NAME:PLSegment', 'SegmentType:=', 'Line', 'StartIndex:=', 5, 'NoOfPoints:=', 2])
pts.append(['NAME:PLPoint', 'X:=', '-2.300063mm', 'Y:=', '2.619000mm', 'Z:=', '0.0mm'])
segs.append(['NAME:PLSegment', 'SegmentType:=', 'Line', 'StartIndex:=', 6, 'NoOfPoints:=', 2])
pts.append(['NAME:PLPoint', 'X:=', '-2.971938mm', 'Y:=', '2.619000mm', 'Z:=', '0.0mm'])
segs.append(['NAME:PLSegment', 'SegmentType:=', 'Line', 'StartIndex:=', 7, 'NoOfPoints:=', 2])
pts.append(['NAME:PLPoint', 'X:=', '-2.971938mm', 'Y:=', '2.841000mm', 'Z:=', '0.0mm'])
segs.append(['NAME:PLSegment', 'SegmentType:=', 'Line', 'StartIndex:=', 8, 'NoOfPoints:=', 2])
pts.append(['NAME:PLPoint', 'X:=', '-2.300063mm', 'Y:=', '2.841000mm', 'Z:=', '0.0mm'])
segs.append(['NAME:PLSegment', 'SegmentType:=', 'Line', 'StartIndex:=', 9, 'NoOfPoints:=', 2])
pts.append(['NAME:PLPoint', 'X:=', '-2.300063mm', 'Y:=', '3.019000mm', 'Z:=', '0.0mm'])
segs.append(['NAME:PLSegment', 'SegmentType:=', 'Line', 'StartIndex:=', 10, 'NoOfPoints:=', 2])
pts.append(['NAME:PLPoint', 'X:=', '-2.971938mm', 'Y:=', '3.019000mm', 'Z:=', '0.0mm'])
segs.append(['NAME:PLSegment', 'SegmentType:=', 'Line', 'StartIndex:=', 11, 'NoOfPoints:=', 2])
pts.append(['NAME:PLPoint', 'X:=', '-2.971938mm', 'Y:=', '3.241000mm', 'Z:=', '0.0mm'])
segs.append(['NAME:PLSegment', 'SegmentType:=', 'Line', 'StartIndex:=', 12, 'NoOfPoints:=', 2])
pts.append(['NAME:PLPoint', 'X:=', '-2.300063mm', 'Y:=', '3.241000mm', 'Z:=', '0.0mm'])
segs.append(['NAME:PLSegment', 'SegmentType:=', 'Line', 'StartIndex:=', 13, 'NoOfPoints:=', 2])
pts.append(['NAME:PLPoint', 'X:=', '-2.300063mm', 'Y:=', '3.419000mm', 'Z:=', '0.0mm'])
segs.append(['NAME:PLSegment', 'SegmentType:=', 'Line', 'StartIndex:=', 14, 'NoOfPoints:=', 2])
pts.append(['NAME:PLPoint', 'X:=', '-2.971938mm', 'Y:=', '3.419000mm', 'Z:=', '0.0mm'])
segs.append(['NAME:PLSegment', 'SegmentType:=', 'Line', 'StartIndex:=', 15, 'NoOfPoints:=', 2])
pts.append(['NAME:PLPoint', 'X:=', '-2.971938mm', 'Y:=', '3.641000mm', 'Z:=', '0.0mm'])
segs.append(['NAME:PLSegment', 'SegmentType:=', 'Line', 'StartIndex:=', 16, 'NoOfPoints:=', 2])
pts.append(['NAME:PLPoint', 'X:=', '-2.300063mm', 'Y:=', '3.641000mm', 'Z:=', '0.0mm'])
segs.append(['NAME:PLSegment', 'SegmentType:=', 'Line', 'StartIndex:=', 17, 'NoOfPoints:=', 2])
pts.append(['NAME:PLPoint', 'X:=', '-2.300063mm', 'Y:=', '3.819000mm', 'Z:=', '0.0mm'])
segs.append(['NAME:PLSegment', 'SegmentType:=', 'Line', 'StartIndex:=', 18, 'NoOfPoints:=', 2])
pts.append(['NAME:PLPoint', 'X:=', '-2.511000mm', 'Y:=', '3.819000mm', 'Z:=', '0.0mm'])
segs.append(['NAME:PLSegment', 'SegmentType:=', 'Line', 'StartIndex:=', 19, 'NoOfPoints:=', 2])
pts.append(['NAME:PLPoint', 'X:=', '-2.511000mm', 'Y:=', '3.975000mm', 'Z:=', '0.0mm'])
segs.append(['NAME:PLSegment', 'SegmentType:=', 'Line', 'StartIndex:=', 20, 'NoOfPoints:=', 2])
pts.append(['NAME:PLPoint', 'X:=', '-2.489000mm', 'Y:=', '3.975000mm', 'Z:=', '0.0mm'])
segs.append(['NAME:PLSegment', 'SegmentType:=', 'Line', 'StartIndex:=', 21, 'NoOfPoints:=', 2])
pts.append(['NAME:PLPoint', 'X:=', '-2.489000mm', 'Y:=', '3.841000mm', 'Z:=', '0.0mm'])
segs.append(['NAME:PLSegment', 'SegmentType:=', 'Line', 'StartIndex:=', 22, 'NoOfPoints:=', 2])
pts.append(['NAME:PLPoint', 'X:=', '-2.278062mm', 'Y:=', '3.841000mm', 'Z:=', '0.0mm'])
segs.append(['NAME:PLSegment', 'SegmentType:=', 'Line', 'StartIndex:=', 23, 'NoOfPoints:=', 2])
pts.append(['NAME:PLPoint', 'X:=', '-2.278062mm', 'Y:=', '3.619000mm', 'Z:=', '0.0mm'])
segs.append(['NAME:PLSegment', 'SegmentType:=', 'Line', 'StartIndex:=', 24, 'NoOfPoints:=', 2])
pts.append(['NAME:PLPoint', 'X:=', '-2.949937mm', 'Y:=', '3.619000mm', 'Z:=', '0.0mm'])
segs.append(['NAME:PLSegment', 'SegmentType:=', 'Line', 'StartIndex:=', 25, 'NoOfPoints:=', 2])
pts.append(['NAME:PLPoint', 'X:=', '-2.949937mm', 'Y:=', '3.441000mm', 'Z:=', '0.0mm'])
segs.append(['NAME:PLSegment', 'SegmentType:=', 'Line', 'StartIndex:=', 26, 'NoOfPoints:=', 2])
pts.append(['NAME:PLPoint', 'X:=', '-2.278062mm', 'Y:=', '3.441000mm', 'Z:=', '0.0mm'])
segs.append(['NAME:PLSegment', 'SegmentType:=', 'Line', 'StartIndex:=', 27, 'NoOfPoints:=', 2])
pts.append(['NAME:PLPoint', 'X:=', '-2.278062mm', 'Y:=', '3.219000mm', 'Z:=', '0.0mm'])
segs.append(['NAME:PLSegment', 'SegmentType:=', 'Line', 'StartIndex:=', 28, 'NoOfPoints:=', 2])
pts.append(['NAME:PLPoint', 'X:=', '-2.949937mm', 'Y:=', '3.219000mm', 'Z:=', '0.0mm'])
segs.append(['NAME:PLSegment', 'SegmentType:=', 'Line', 'StartIndex:=', 29, 'NoOfPoints:=', 2])
pts.append(['NAME:PLPoint', 'X:=', '-2.949937mm', 'Y:=', '3.041000mm', 'Z:=', '0.0mm'])
segs.append(['NAME:PLSegment', 'SegmentType:=', 'Line', 'StartIndex:=', 30, 'NoOfPoints:=', 2])
pts.append(['NAME:PLPoint', 'X:=', '-2.278062mm', 'Y:=', '3.041000mm', 'Z:=', '0.0mm'])
segs.append(['NAME:PLSegment', 'SegmentType:=', 'Line', 'StartIndex:=', 31, 'NoOfPoints:=', 2])
pts.append(['NAME:PLPoint', 'X:=', '-2.278062mm', 'Y:=', '2.819000mm', 'Z:=', '0.0mm'])
segs.append(['NAME:PLSegment', 'SegmentType:=', 'Line', 'StartIndex:=', 32, 'NoOfPoints:=', 2])
pts.append(['NAME:PLPoint', 'X:=', '-2.949937mm', 'Y:=', '2.819000mm', 'Z:=', '0.0mm'])
segs.append(['NAME:PLSegment', 'SegmentType:=', 'Line', 'StartIndex:=', 33, 'NoOfPoints:=', 2])
pts.append(['NAME:PLPoint', 'X:=', '-2.949937mm', 'Y:=', '2.641000mm', 'Z:=', '0.0mm'])
segs.append(['NAME:PLSegment', 'SegmentType:=', 'Line', 'StartIndex:=', 34, 'NoOfPoints:=', 2])
pts.append(['NAME:PLPoint', 'X:=', '-2.278062mm', 'Y:=', '2.641000mm', 'Z:=', '0.0mm'])
segs.append(['NAME:PLSegment', 'SegmentType:=', 'Line', 'StartIndex:=', 35, 'NoOfPoints:=', 2])
pts.append(['NAME:PLPoint', 'X:=', '-2.278062mm', 'Y:=', '2.419000mm', 'Z:=', '0.0mm'])
segs.append(['NAME:PLSegment', 'SegmentType:=', 'Line', 'StartIndex:=', 36, 'NoOfPoints:=', 2])
pts.append(['NAME:PLPoint', 'X:=', '-2.949937mm', 'Y:=', '2.419000mm', 'Z:=', '0.0mm'])
segs.append(['NAME:PLSegment', 'SegmentType:=', 'Line', 'StartIndex:=', 37, 'NoOfPoints:=', 2])
pts.append(['NAME:PLPoint', 'X:=', '-2.949937mm', 'Y:=', '2.241000mm', 'Z:=', '0.0mm'])
segs.append(['NAME:PLSegment', 'SegmentType:=', 'Line', 'StartIndex:=', 38, 'NoOfPoints:=', 2])
pts.append(['NAME:PLPoint', 'X:=', '-2.614000mm', 'Y:=', '2.241000mm', 'Z:=', '0.0mm'])
segs.append(['NAME:PLSegment', 'SegmentType:=', 'Line', 'StartIndex:=', 39, 'NoOfPoints:=', 2])
pts.append(['NAME:PLPoint', 'X:=', '-2.614000mm', 'Y:=', '2.225000mm', 'Z:=', '0.0mm'])
segs.append(['NAME:PLSegment', 'SegmentType:=', 'Line', 'StartIndex:=', 40, 'NoOfPoints:=', 2])
pts.append(['NAME:PLPoint', 'X:=', '-2.625500mm', 'Y:=', '2.225000mm', 'Z:=', '0.0mm'])
oEditor.CreatePolyline(
    ['NAME:PolylineParameters', 'IsPolylineCovered:=', True, 'IsPolylineClosed:=', True, pts, segs],
    [
        'NAME:Attributes',
        'Name:=', 'cut_Readout_Q1_51',
        'Flags:=', '',
        'Color:=', '(255 100 100)',
        'Transparency:=', 0.0,
        'PartCoordinateSystem:=', 'Global',
        'UDMId:=', '',
        'MaterialName:=', 'vacuum',
        'SolveInside:=', True
    ]
)
# Element: trace_Readout_Q3_52
pts = ['NAME:PolylinePoints']
segs = ['NAME:PolylineSegments']
pts.append(['NAME:PLPoint', 'X:=', '-0.800500mm', 'Y:=', '1.000000mm', 'Z:=', '0.0mm'])
segs.append(['NAME:PLSegment', 'SegmentType:=', 'Line', 'StartIndex:=', 0, 'NoOfPoints:=', 2])
pts.append(['NAME:PLPoint', 'X:=', '-0.800500mm', 'Y:=', '1.190000mm', 'Z:=', '0.0mm'])
segs.append(['NAME:PLSegment', 'SegmentType:=', 'Line', 'StartIndex:=', 1, 'NoOfPoints:=', 2])
pts.append(['NAME:PLPoint', 'X:=', '-1.049500mm', 'Y:=', '1.190000mm', 'Z:=', '0.0mm'])
segs.append(['NAME:PLSegment', 'SegmentType:=', 'Line', 'StartIndex:=', 2, 'NoOfPoints:=', 2])
pts.append(['NAME:PLPoint', 'X:=', '-1.049500mm', 'Y:=', '1.400000mm', 'Z:=', '0.0mm'])
segs.append(['NAME:PLSegment', 'SegmentType:=', 'Line', 'StartIndex:=', 3, 'NoOfPoints:=', 2])
pts.append(['NAME:PLPoint', 'X:=', '-0.800500mm', 'Y:=', '1.400000mm', 'Z:=', '0.0mm'])
segs.append(['NAME:PLSegment', 'SegmentType:=', 'Line', 'StartIndex:=', 4, 'NoOfPoints:=', 2])
pts.append(['NAME:PLPoint', 'X:=', '-0.800500mm', 'Y:=', '1.590000mm', 'Z:=', '0.0mm'])
segs.append(['NAME:PLSegment', 'SegmentType:=', 'Line', 'StartIndex:=', 5, 'NoOfPoints:=', 2])
pts.append(['NAME:PLPoint', 'X:=', '-1.049500mm', 'Y:=', '1.590000mm', 'Z:=', '0.0mm'])
segs.append(['NAME:PLSegment', 'SegmentType:=', 'Line', 'StartIndex:=', 6, 'NoOfPoints:=', 2])
pts.append(['NAME:PLPoint', 'X:=', '-1.049500mm', 'Y:=', '1.800000mm', 'Z:=', '0.0mm'])
segs.append(['NAME:PLSegment', 'SegmentType:=', 'Line', 'StartIndex:=', 7, 'NoOfPoints:=', 2])
pts.append(['NAME:PLPoint', 'X:=', '-0.800500mm', 'Y:=', '1.800000mm', 'Z:=', '0.0mm'])
segs.append(['NAME:PLSegment', 'SegmentType:=', 'Line', 'StartIndex:=', 8, 'NoOfPoints:=', 2])
pts.append(['NAME:PLPoint', 'X:=', '-0.800500mm', 'Y:=', '1.990000mm', 'Z:=', '0.0mm'])
segs.append(['NAME:PLSegment', 'SegmentType:=', 'Line', 'StartIndex:=', 9, 'NoOfPoints:=', 2])
pts.append(['NAME:PLPoint', 'X:=', '-1.049500mm', 'Y:=', '1.990000mm', 'Z:=', '0.0mm'])
segs.append(['NAME:PLSegment', 'SegmentType:=', 'Line', 'StartIndex:=', 10, 'NoOfPoints:=', 2])
pts.append(['NAME:PLPoint', 'X:=', '-1.049500mm', 'Y:=', '2.200000mm', 'Z:=', '0.0mm'])
segs.append(['NAME:PLSegment', 'SegmentType:=', 'Line', 'StartIndex:=', 11, 'NoOfPoints:=', 2])
pts.append(['NAME:PLPoint', 'X:=', '-0.800500mm', 'Y:=', '2.200000mm', 'Z:=', '0.0mm'])
segs.append(['NAME:PLSegment', 'SegmentType:=', 'Line', 'StartIndex:=', 12, 'NoOfPoints:=', 2])
pts.append(['NAME:PLPoint', 'X:=', '-0.800500mm', 'Y:=', '2.390000mm', 'Z:=', '0.0mm'])
segs.append(['NAME:PLSegment', 'SegmentType:=', 'Line', 'StartIndex:=', 13, 'NoOfPoints:=', 2])
pts.append(['NAME:PLPoint', 'X:=', '-1.049500mm', 'Y:=', '2.390000mm', 'Z:=', '0.0mm'])
segs.append(['NAME:PLSegment', 'SegmentType:=', 'Line', 'StartIndex:=', 14, 'NoOfPoints:=', 2])
pts.append(['NAME:PLPoint', 'X:=', '-1.049500mm', 'Y:=', '2.600000mm', 'Z:=', '0.0mm'])
segs.append(['NAME:PLSegment', 'SegmentType:=', 'Line', 'StartIndex:=', 15, 'NoOfPoints:=', 2])
pts.append(['NAME:PLPoint', 'X:=', '-0.800500mm', 'Y:=', '2.600000mm', 'Z:=', '0.0mm'])
segs.append(['NAME:PLSegment', 'SegmentType:=', 'Line', 'StartIndex:=', 16, 'NoOfPoints:=', 2])
pts.append(['NAME:PLPoint', 'X:=', '-0.800500mm', 'Y:=', '2.790000mm', 'Z:=', '0.0mm'])
segs.append(['NAME:PLSegment', 'SegmentType:=', 'Line', 'StartIndex:=', 17, 'NoOfPoints:=', 2])
pts.append(['NAME:PLPoint', 'X:=', '-1.049500mm', 'Y:=', '2.790000mm', 'Z:=', '0.0mm'])
segs.append(['NAME:PLSegment', 'SegmentType:=', 'Line', 'StartIndex:=', 18, 'NoOfPoints:=', 2])
pts.append(['NAME:PLPoint', 'X:=', '-1.049500mm', 'Y:=', '3.000000mm', 'Z:=', '0.0mm'])
segs.append(['NAME:PLSegment', 'SegmentType:=', 'Line', 'StartIndex:=', 19, 'NoOfPoints:=', 2])
pts.append(['NAME:PLPoint', 'X:=', '-0.800500mm', 'Y:=', '3.000000mm', 'Z:=', '0.0mm'])
segs.append(['NAME:PLSegment', 'SegmentType:=', 'Line', 'StartIndex:=', 20, 'NoOfPoints:=', 2])
pts.append(['NAME:PLPoint', 'X:=', '-0.800500mm', 'Y:=', '3.190000mm', 'Z:=', '0.0mm'])
segs.append(['NAME:PLSegment', 'SegmentType:=', 'Line', 'StartIndex:=', 21, 'NoOfPoints:=', 2])
pts.append(['NAME:PLPoint', 'X:=', '-1.049500mm', 'Y:=', '3.190000mm', 'Z:=', '0.0mm'])
segs.append(['NAME:PLSegment', 'SegmentType:=', 'Line', 'StartIndex:=', 22, 'NoOfPoints:=', 2])
pts.append(['NAME:PLPoint', 'X:=', '-1.049500mm', 'Y:=', '3.400000mm', 'Z:=', '0.0mm'])
segs.append(['NAME:PLSegment', 'SegmentType:=', 'Line', 'StartIndex:=', 23, 'NoOfPoints:=', 2])
pts.append(['NAME:PLPoint', 'X:=', '-0.800500mm', 'Y:=', '3.400000mm', 'Z:=', '0.0mm'])
segs.append(['NAME:PLSegment', 'SegmentType:=', 'Line', 'StartIndex:=', 24, 'NoOfPoints:=', 2])
pts.append(['NAME:PLPoint', 'X:=', '-0.800500mm', 'Y:=', '3.590000mm', 'Z:=', '0.0mm'])
segs.append(['NAME:PLSegment', 'SegmentType:=', 'Line', 'StartIndex:=', 25, 'NoOfPoints:=', 2])
pts.append(['NAME:PLPoint', 'X:=', '-1.049500mm', 'Y:=', '3.590000mm', 'Z:=', '0.0mm'])
segs.append(['NAME:PLSegment', 'SegmentType:=', 'Line', 'StartIndex:=', 26, 'NoOfPoints:=', 2])
pts.append(['NAME:PLPoint', 'X:=', '-1.049500mm', 'Y:=', '3.800000mm', 'Z:=', '0.0mm'])
segs.append(['NAME:PLSegment', 'SegmentType:=', 'Line', 'StartIndex:=', 27, 'NoOfPoints:=', 2])
pts.append(['NAME:PLPoint', 'X:=', '-0.800500mm', 'Y:=', '3.800000mm', 'Z:=', '0.0mm'])
segs.append(['NAME:PLSegment', 'SegmentType:=', 'Line', 'StartIndex:=', 28, 'NoOfPoints:=', 2])
pts.append(['NAME:PLPoint', 'X:=', '-0.800500mm', 'Y:=', '3.990000mm', 'Z:=', '0.0mm'])
segs.append(['NAME:PLSegment', 'SegmentType:=', 'Line', 'StartIndex:=', 29, 'NoOfPoints:=', 2])
pts.append(['NAME:PLPoint', 'X:=', '-1.005000mm', 'Y:=', '3.990000mm', 'Z:=', '0.0mm'])
segs.append(['NAME:PLSegment', 'SegmentType:=', 'Line', 'StartIndex:=', 30, 'NoOfPoints:=', 2])
pts.append(['NAME:PLPoint', 'X:=', '-1.005000mm', 'Y:=', '4.175000mm', 'Z:=', '0.0mm'])
segs.append(['NAME:PLSegment', 'SegmentType:=', 'Line', 'StartIndex:=', 31, 'NoOfPoints:=', 2])
pts.append(['NAME:PLPoint', 'X:=', '-0.995000mm', 'Y:=', '4.175000mm', 'Z:=', '0.0mm'])
segs.append(['NAME:PLSegment', 'SegmentType:=', 'Line', 'StartIndex:=', 32, 'NoOfPoints:=', 2])
pts.append(['NAME:PLPoint', 'X:=', '-0.995000mm', 'Y:=', '4.000000mm', 'Z:=', '0.0mm'])
segs.append(['NAME:PLSegment', 'SegmentType:=', 'Line', 'StartIndex:=', 33, 'NoOfPoints:=', 2])
pts.append(['NAME:PLPoint', 'X:=', '-0.790500mm', 'Y:=', '4.000000mm', 'Z:=', '0.0mm'])
segs.append(['NAME:PLSegment', 'SegmentType:=', 'Line', 'StartIndex:=', 34, 'NoOfPoints:=', 2])
pts.append(['NAME:PLPoint', 'X:=', '-0.790500mm', 'Y:=', '3.790000mm', 'Z:=', '0.0mm'])
segs.append(['NAME:PLSegment', 'SegmentType:=', 'Line', 'StartIndex:=', 35, 'NoOfPoints:=', 2])
pts.append(['NAME:PLPoint', 'X:=', '-1.039500mm', 'Y:=', '3.790000mm', 'Z:=', '0.0mm'])
segs.append(['NAME:PLSegment', 'SegmentType:=', 'Line', 'StartIndex:=', 36, 'NoOfPoints:=', 2])
pts.append(['NAME:PLPoint', 'X:=', '-1.039500mm', 'Y:=', '3.600000mm', 'Z:=', '0.0mm'])
segs.append(['NAME:PLSegment', 'SegmentType:=', 'Line', 'StartIndex:=', 37, 'NoOfPoints:=', 2])
pts.append(['NAME:PLPoint', 'X:=', '-0.790500mm', 'Y:=', '3.600000mm', 'Z:=', '0.0mm'])
segs.append(['NAME:PLSegment', 'SegmentType:=', 'Line', 'StartIndex:=', 38, 'NoOfPoints:=', 2])
pts.append(['NAME:PLPoint', 'X:=', '-0.790500mm', 'Y:=', '3.390000mm', 'Z:=', '0.0mm'])
segs.append(['NAME:PLSegment', 'SegmentType:=', 'Line', 'StartIndex:=', 39, 'NoOfPoints:=', 2])
pts.append(['NAME:PLPoint', 'X:=', '-1.039500mm', 'Y:=', '3.390000mm', 'Z:=', '0.0mm'])
segs.append(['NAME:PLSegment', 'SegmentType:=', 'Line', 'StartIndex:=', 40, 'NoOfPoints:=', 2])
pts.append(['NAME:PLPoint', 'X:=', '-1.039500mm', 'Y:=', '3.200000mm', 'Z:=', '0.0mm'])
segs.append(['NAME:PLSegment', 'SegmentType:=', 'Line', 'StartIndex:=', 41, 'NoOfPoints:=', 2])
pts.append(['NAME:PLPoint', 'X:=', '-0.790500mm', 'Y:=', '3.200000mm', 'Z:=', '0.0mm'])
segs.append(['NAME:PLSegment', 'SegmentType:=', 'Line', 'StartIndex:=', 42, 'NoOfPoints:=', 2])
pts.append(['NAME:PLPoint', 'X:=', '-0.790500mm', 'Y:=', '2.990000mm', 'Z:=', '0.0mm'])
segs.append(['NAME:PLSegment', 'SegmentType:=', 'Line', 'StartIndex:=', 43, 'NoOfPoints:=', 2])
pts.append(['NAME:PLPoint', 'X:=', '-1.039500mm', 'Y:=', '2.990000mm', 'Z:=', '0.0mm'])
segs.append(['NAME:PLSegment', 'SegmentType:=', 'Line', 'StartIndex:=', 44, 'NoOfPoints:=', 2])
pts.append(['NAME:PLPoint', 'X:=', '-1.039500mm', 'Y:=', '2.800000mm', 'Z:=', '0.0mm'])
segs.append(['NAME:PLSegment', 'SegmentType:=', 'Line', 'StartIndex:=', 45, 'NoOfPoints:=', 2])
pts.append(['NAME:PLPoint', 'X:=', '-0.790500mm', 'Y:=', '2.800000mm', 'Z:=', '0.0mm'])
segs.append(['NAME:PLSegment', 'SegmentType:=', 'Line', 'StartIndex:=', 46, 'NoOfPoints:=', 2])
pts.append(['NAME:PLPoint', 'X:=', '-0.790500mm', 'Y:=', '2.590000mm', 'Z:=', '0.0mm'])
segs.append(['NAME:PLSegment', 'SegmentType:=', 'Line', 'StartIndex:=', 47, 'NoOfPoints:=', 2])
pts.append(['NAME:PLPoint', 'X:=', '-1.039500mm', 'Y:=', '2.590000mm', 'Z:=', '0.0mm'])
segs.append(['NAME:PLSegment', 'SegmentType:=', 'Line', 'StartIndex:=', 48, 'NoOfPoints:=', 2])
pts.append(['NAME:PLPoint', 'X:=', '-1.039500mm', 'Y:=', '2.400000mm', 'Z:=', '0.0mm'])
segs.append(['NAME:PLSegment', 'SegmentType:=', 'Line', 'StartIndex:=', 49, 'NoOfPoints:=', 2])
pts.append(['NAME:PLPoint', 'X:=', '-0.790500mm', 'Y:=', '2.400000mm', 'Z:=', '0.0mm'])
segs.append(['NAME:PLSegment', 'SegmentType:=', 'Line', 'StartIndex:=', 50, 'NoOfPoints:=', 2])
pts.append(['NAME:PLPoint', 'X:=', '-0.790500mm', 'Y:=', '2.190000mm', 'Z:=', '0.0mm'])
segs.append(['NAME:PLSegment', 'SegmentType:=', 'Line', 'StartIndex:=', 51, 'NoOfPoints:=', 2])
pts.append(['NAME:PLPoint', 'X:=', '-1.039500mm', 'Y:=', '2.190000mm', 'Z:=', '0.0mm'])
segs.append(['NAME:PLSegment', 'SegmentType:=', 'Line', 'StartIndex:=', 52, 'NoOfPoints:=', 2])
pts.append(['NAME:PLPoint', 'X:=', '-1.039500mm', 'Y:=', '2.000000mm', 'Z:=', '0.0mm'])
segs.append(['NAME:PLSegment', 'SegmentType:=', 'Line', 'StartIndex:=', 53, 'NoOfPoints:=', 2])
pts.append(['NAME:PLPoint', 'X:=', '-0.790500mm', 'Y:=', '2.000000mm', 'Z:=', '0.0mm'])
segs.append(['NAME:PLSegment', 'SegmentType:=', 'Line', 'StartIndex:=', 54, 'NoOfPoints:=', 2])
pts.append(['NAME:PLPoint', 'X:=', '-0.790500mm', 'Y:=', '1.790000mm', 'Z:=', '0.0mm'])
segs.append(['NAME:PLSegment', 'SegmentType:=', 'Line', 'StartIndex:=', 55, 'NoOfPoints:=', 2])
pts.append(['NAME:PLPoint', 'X:=', '-1.039500mm', 'Y:=', '1.790000mm', 'Z:=', '0.0mm'])
segs.append(['NAME:PLSegment', 'SegmentType:=', 'Line', 'StartIndex:=', 56, 'NoOfPoints:=', 2])
pts.append(['NAME:PLPoint', 'X:=', '-1.039500mm', 'Y:=', '1.600000mm', 'Z:=', '0.0mm'])
segs.append(['NAME:PLSegment', 'SegmentType:=', 'Line', 'StartIndex:=', 57, 'NoOfPoints:=', 2])
pts.append(['NAME:PLPoint', 'X:=', '-0.790500mm', 'Y:=', '1.600000mm', 'Z:=', '0.0mm'])
segs.append(['NAME:PLSegment', 'SegmentType:=', 'Line', 'StartIndex:=', 58, 'NoOfPoints:=', 2])
pts.append(['NAME:PLPoint', 'X:=', '-0.790500mm', 'Y:=', '1.390000mm', 'Z:=', '0.0mm'])
segs.append(['NAME:PLSegment', 'SegmentType:=', 'Line', 'StartIndex:=', 59, 'NoOfPoints:=', 2])
pts.append(['NAME:PLPoint', 'X:=', '-1.039500mm', 'Y:=', '1.390000mm', 'Z:=', '0.0mm'])
segs.append(['NAME:PLSegment', 'SegmentType:=', 'Line', 'StartIndex:=', 60, 'NoOfPoints:=', 2])
pts.append(['NAME:PLPoint', 'X:=', '-1.039500mm', 'Y:=', '1.200000mm', 'Z:=', '0.0mm'])
segs.append(['NAME:PLSegment', 'SegmentType:=', 'Line', 'StartIndex:=', 61, 'NoOfPoints:=', 2])
pts.append(['NAME:PLPoint', 'X:=', '-0.790500mm', 'Y:=', '1.200000mm', 'Z:=', '0.0mm'])
segs.append(['NAME:PLSegment', 'SegmentType:=', 'Line', 'StartIndex:=', 62, 'NoOfPoints:=', 2])
pts.append(['NAME:PLPoint', 'X:=', '-0.790500mm', 'Y:=', '0.990000mm', 'Z:=', '0.0mm'])
segs.append(['NAME:PLSegment', 'SegmentType:=', 'Line', 'StartIndex:=', 63, 'NoOfPoints:=', 2])
pts.append(['NAME:PLPoint', 'X:=', '-0.925000mm', 'Y:=', '0.990000mm', 'Z:=', '0.0mm'])
segs.append(['NAME:PLSegment', 'SegmentType:=', 'Line', 'StartIndex:=', 64, 'NoOfPoints:=', 2])
pts.append(['NAME:PLPoint', 'X:=', '-0.925000mm', 'Y:=', '1.000000mm', 'Z:=', '0.0mm'])
segs.append(['NAME:PLSegment', 'SegmentType:=', 'Line', 'StartIndex:=', 65, 'NoOfPoints:=', 2])
pts.append(['NAME:PLPoint', 'X:=', '-0.800500mm', 'Y:=', '1.000000mm', 'Z:=', '0.0mm'])
oEditor.CreatePolyline(
    ['NAME:PolylineParameters', 'IsPolylineCovered:=', True, 'IsPolylineClosed:=', True, pts, segs],
    [
        'NAME:Attributes',
        'Name:=', 'trace_Readout_Q3_52',
        'Flags:=', '',
        'Color:=', '(200 220 255)',
        'Transparency:=', 0.0,
        'PartCoordinateSystem:=', 'Global',
        'UDMId:=', '',
        'MaterialName:=', 'vacuum',
        'SolveInside:=', True
    ]
)
# Element: cut_Readout_Q3_53
pts = ['NAME:PolylinePoints']
segs = ['NAME:PolylineSegments']
pts.append(['NAME:PLPoint', 'X:=', '-0.806500mm', 'Y:=', '1.006000mm', 'Z:=', '0.0mm'])
segs.append(['NAME:PLSegment', 'SegmentType:=', 'Line', 'StartIndex:=', 0, 'NoOfPoints:=', 2])
pts.append(['NAME:PLPoint', 'X:=', '-0.806500mm', 'Y:=', '1.184000mm', 'Z:=', '0.0mm'])
segs.append(['NAME:PLSegment', 'SegmentType:=', 'Line', 'StartIndex:=', 1, 'NoOfPoints:=', 2])
pts.append(['NAME:PLPoint', 'X:=', '-1.055500mm', 'Y:=', '1.184000mm', 'Z:=', '0.0mm'])
segs.append(['NAME:PLSegment', 'SegmentType:=', 'Line', 'StartIndex:=', 2, 'NoOfPoints:=', 2])
pts.append(['NAME:PLPoint', 'X:=', '-1.055500mm', 'Y:=', '1.406000mm', 'Z:=', '0.0mm'])
segs.append(['NAME:PLSegment', 'SegmentType:=', 'Line', 'StartIndex:=', 3, 'NoOfPoints:=', 2])
pts.append(['NAME:PLPoint', 'X:=', '-0.806500mm', 'Y:=', '1.406000mm', 'Z:=', '0.0mm'])
segs.append(['NAME:PLSegment', 'SegmentType:=', 'Line', 'StartIndex:=', 4, 'NoOfPoints:=', 2])
pts.append(['NAME:PLPoint', 'X:=', '-0.806500mm', 'Y:=', '1.584000mm', 'Z:=', '0.0mm'])
segs.append(['NAME:PLSegment', 'SegmentType:=', 'Line', 'StartIndex:=', 5, 'NoOfPoints:=', 2])
pts.append(['NAME:PLPoint', 'X:=', '-1.055500mm', 'Y:=', '1.584000mm', 'Z:=', '0.0mm'])
segs.append(['NAME:PLSegment', 'SegmentType:=', 'Line', 'StartIndex:=', 6, 'NoOfPoints:=', 2])
pts.append(['NAME:PLPoint', 'X:=', '-1.055500mm', 'Y:=', '1.806000mm', 'Z:=', '0.0mm'])
segs.append(['NAME:PLSegment', 'SegmentType:=', 'Line', 'StartIndex:=', 7, 'NoOfPoints:=', 2])
pts.append(['NAME:PLPoint', 'X:=', '-0.806500mm', 'Y:=', '1.806000mm', 'Z:=', '0.0mm'])
segs.append(['NAME:PLSegment', 'SegmentType:=', 'Line', 'StartIndex:=', 8, 'NoOfPoints:=', 2])
pts.append(['NAME:PLPoint', 'X:=', '-0.806500mm', 'Y:=', '1.984000mm', 'Z:=', '0.0mm'])
segs.append(['NAME:PLSegment', 'SegmentType:=', 'Line', 'StartIndex:=', 9, 'NoOfPoints:=', 2])
pts.append(['NAME:PLPoint', 'X:=', '-1.055500mm', 'Y:=', '1.984000mm', 'Z:=', '0.0mm'])
segs.append(['NAME:PLSegment', 'SegmentType:=', 'Line', 'StartIndex:=', 10, 'NoOfPoints:=', 2])
pts.append(['NAME:PLPoint', 'X:=', '-1.055500mm', 'Y:=', '2.206000mm', 'Z:=', '0.0mm'])
segs.append(['NAME:PLSegment', 'SegmentType:=', 'Line', 'StartIndex:=', 11, 'NoOfPoints:=', 2])
pts.append(['NAME:PLPoint', 'X:=', '-0.806500mm', 'Y:=', '2.206000mm', 'Z:=', '0.0mm'])
segs.append(['NAME:PLSegment', 'SegmentType:=', 'Line', 'StartIndex:=', 12, 'NoOfPoints:=', 2])
pts.append(['NAME:PLPoint', 'X:=', '-0.806500mm', 'Y:=', '2.384000mm', 'Z:=', '0.0mm'])
segs.append(['NAME:PLSegment', 'SegmentType:=', 'Line', 'StartIndex:=', 13, 'NoOfPoints:=', 2])
pts.append(['NAME:PLPoint', 'X:=', '-1.055500mm', 'Y:=', '2.384000mm', 'Z:=', '0.0mm'])
segs.append(['NAME:PLSegment', 'SegmentType:=', 'Line', 'StartIndex:=', 14, 'NoOfPoints:=', 2])
pts.append(['NAME:PLPoint', 'X:=', '-1.055500mm', 'Y:=', '2.606000mm', 'Z:=', '0.0mm'])
segs.append(['NAME:PLSegment', 'SegmentType:=', 'Line', 'StartIndex:=', 15, 'NoOfPoints:=', 2])
pts.append(['NAME:PLPoint', 'X:=', '-0.806500mm', 'Y:=', '2.606000mm', 'Z:=', '0.0mm'])
segs.append(['NAME:PLSegment', 'SegmentType:=', 'Line', 'StartIndex:=', 16, 'NoOfPoints:=', 2])
pts.append(['NAME:PLPoint', 'X:=', '-0.806500mm', 'Y:=', '2.784000mm', 'Z:=', '0.0mm'])
segs.append(['NAME:PLSegment', 'SegmentType:=', 'Line', 'StartIndex:=', 17, 'NoOfPoints:=', 2])
pts.append(['NAME:PLPoint', 'X:=', '-1.055500mm', 'Y:=', '2.784000mm', 'Z:=', '0.0mm'])
segs.append(['NAME:PLSegment', 'SegmentType:=', 'Line', 'StartIndex:=', 18, 'NoOfPoints:=', 2])
pts.append(['NAME:PLPoint', 'X:=', '-1.055500mm', 'Y:=', '3.006000mm', 'Z:=', '0.0mm'])
segs.append(['NAME:PLSegment', 'SegmentType:=', 'Line', 'StartIndex:=', 19, 'NoOfPoints:=', 2])
pts.append(['NAME:PLPoint', 'X:=', '-0.806500mm', 'Y:=', '3.006000mm', 'Z:=', '0.0mm'])
segs.append(['NAME:PLSegment', 'SegmentType:=', 'Line', 'StartIndex:=', 20, 'NoOfPoints:=', 2])
pts.append(['NAME:PLPoint', 'X:=', '-0.806500mm', 'Y:=', '3.184000mm', 'Z:=', '0.0mm'])
segs.append(['NAME:PLSegment', 'SegmentType:=', 'Line', 'StartIndex:=', 21, 'NoOfPoints:=', 2])
pts.append(['NAME:PLPoint', 'X:=', '-1.055500mm', 'Y:=', '3.184000mm', 'Z:=', '0.0mm'])
segs.append(['NAME:PLSegment', 'SegmentType:=', 'Line', 'StartIndex:=', 22, 'NoOfPoints:=', 2])
pts.append(['NAME:PLPoint', 'X:=', '-1.055500mm', 'Y:=', '3.406000mm', 'Z:=', '0.0mm'])
segs.append(['NAME:PLSegment', 'SegmentType:=', 'Line', 'StartIndex:=', 23, 'NoOfPoints:=', 2])
pts.append(['NAME:PLPoint', 'X:=', '-0.806500mm', 'Y:=', '3.406000mm', 'Z:=', '0.0mm'])
segs.append(['NAME:PLSegment', 'SegmentType:=', 'Line', 'StartIndex:=', 24, 'NoOfPoints:=', 2])
pts.append(['NAME:PLPoint', 'X:=', '-0.806500mm', 'Y:=', '3.584000mm', 'Z:=', '0.0mm'])
segs.append(['NAME:PLSegment', 'SegmentType:=', 'Line', 'StartIndex:=', 25, 'NoOfPoints:=', 2])
pts.append(['NAME:PLPoint', 'X:=', '-1.055500mm', 'Y:=', '3.584000mm', 'Z:=', '0.0mm'])
segs.append(['NAME:PLSegment', 'SegmentType:=', 'Line', 'StartIndex:=', 26, 'NoOfPoints:=', 2])
pts.append(['NAME:PLPoint', 'X:=', '-1.055500mm', 'Y:=', '3.806000mm', 'Z:=', '0.0mm'])
segs.append(['NAME:PLSegment', 'SegmentType:=', 'Line', 'StartIndex:=', 27, 'NoOfPoints:=', 2])
pts.append(['NAME:PLPoint', 'X:=', '-0.806500mm', 'Y:=', '3.806000mm', 'Z:=', '0.0mm'])
segs.append(['NAME:PLSegment', 'SegmentType:=', 'Line', 'StartIndex:=', 28, 'NoOfPoints:=', 2])
pts.append(['NAME:PLPoint', 'X:=', '-0.806500mm', 'Y:=', '3.984000mm', 'Z:=', '0.0mm'])
segs.append(['NAME:PLSegment', 'SegmentType:=', 'Line', 'StartIndex:=', 29, 'NoOfPoints:=', 2])
pts.append(['NAME:PLPoint', 'X:=', '-1.011000mm', 'Y:=', '3.984000mm', 'Z:=', '0.0mm'])
segs.append(['NAME:PLSegment', 'SegmentType:=', 'Line', 'StartIndex:=', 30, 'NoOfPoints:=', 2])
pts.append(['NAME:PLPoint', 'X:=', '-1.011000mm', 'Y:=', '4.175000mm', 'Z:=', '0.0mm'])
segs.append(['NAME:PLSegment', 'SegmentType:=', 'Line', 'StartIndex:=', 31, 'NoOfPoints:=', 2])
pts.append(['NAME:PLPoint', 'X:=', '-0.989000mm', 'Y:=', '4.175000mm', 'Z:=', '0.0mm'])
segs.append(['NAME:PLSegment', 'SegmentType:=', 'Line', 'StartIndex:=', 32, 'NoOfPoints:=', 2])
pts.append(['NAME:PLPoint', 'X:=', '-0.989000mm', 'Y:=', '4.006000mm', 'Z:=', '0.0mm'])
segs.append(['NAME:PLSegment', 'SegmentType:=', 'Line', 'StartIndex:=', 33, 'NoOfPoints:=', 2])
pts.append(['NAME:PLPoint', 'X:=', '-0.784500mm', 'Y:=', '4.006000mm', 'Z:=', '0.0mm'])
segs.append(['NAME:PLSegment', 'SegmentType:=', 'Line', 'StartIndex:=', 34, 'NoOfPoints:=', 2])
pts.append(['NAME:PLPoint', 'X:=', '-0.784500mm', 'Y:=', '3.784000mm', 'Z:=', '0.0mm'])
segs.append(['NAME:PLSegment', 'SegmentType:=', 'Line', 'StartIndex:=', 35, 'NoOfPoints:=', 2])
pts.append(['NAME:PLPoint', 'X:=', '-1.033500mm', 'Y:=', '3.784000mm', 'Z:=', '0.0mm'])
segs.append(['NAME:PLSegment', 'SegmentType:=', 'Line', 'StartIndex:=', 36, 'NoOfPoints:=', 2])
pts.append(['NAME:PLPoint', 'X:=', '-1.033500mm', 'Y:=', '3.606000mm', 'Z:=', '0.0mm'])
segs.append(['NAME:PLSegment', 'SegmentType:=', 'Line', 'StartIndex:=', 37, 'NoOfPoints:=', 2])
pts.append(['NAME:PLPoint', 'X:=', '-0.784500mm', 'Y:=', '3.606000mm', 'Z:=', '0.0mm'])
segs.append(['NAME:PLSegment', 'SegmentType:=', 'Line', 'StartIndex:=', 38, 'NoOfPoints:=', 2])
pts.append(['NAME:PLPoint', 'X:=', '-0.784500mm', 'Y:=', '3.384000mm', 'Z:=', '0.0mm'])
segs.append(['NAME:PLSegment', 'SegmentType:=', 'Line', 'StartIndex:=', 39, 'NoOfPoints:=', 2])
pts.append(['NAME:PLPoint', 'X:=', '-1.033500mm', 'Y:=', '3.384000mm', 'Z:=', '0.0mm'])
segs.append(['NAME:PLSegment', 'SegmentType:=', 'Line', 'StartIndex:=', 40, 'NoOfPoints:=', 2])
pts.append(['NAME:PLPoint', 'X:=', '-1.033500mm', 'Y:=', '3.206000mm', 'Z:=', '0.0mm'])
segs.append(['NAME:PLSegment', 'SegmentType:=', 'Line', 'StartIndex:=', 41, 'NoOfPoints:=', 2])
pts.append(['NAME:PLPoint', 'X:=', '-0.784500mm', 'Y:=', '3.206000mm', 'Z:=', '0.0mm'])
segs.append(['NAME:PLSegment', 'SegmentType:=', 'Line', 'StartIndex:=', 42, 'NoOfPoints:=', 2])
pts.append(['NAME:PLPoint', 'X:=', '-0.784500mm', 'Y:=', '2.984000mm', 'Z:=', '0.0mm'])
segs.append(['NAME:PLSegment', 'SegmentType:=', 'Line', 'StartIndex:=', 43, 'NoOfPoints:=', 2])
pts.append(['NAME:PLPoint', 'X:=', '-1.033500mm', 'Y:=', '2.984000mm', 'Z:=', '0.0mm'])
segs.append(['NAME:PLSegment', 'SegmentType:=', 'Line', 'StartIndex:=', 44, 'NoOfPoints:=', 2])
pts.append(['NAME:PLPoint', 'X:=', '-1.033500mm', 'Y:=', '2.806000mm', 'Z:=', '0.0mm'])
segs.append(['NAME:PLSegment', 'SegmentType:=', 'Line', 'StartIndex:=', 45, 'NoOfPoints:=', 2])
pts.append(['NAME:PLPoint', 'X:=', '-0.784500mm', 'Y:=', '2.806000mm', 'Z:=', '0.0mm'])
segs.append(['NAME:PLSegment', 'SegmentType:=', 'Line', 'StartIndex:=', 46, 'NoOfPoints:=', 2])
pts.append(['NAME:PLPoint', 'X:=', '-0.784500mm', 'Y:=', '2.584000mm', 'Z:=', '0.0mm'])
segs.append(['NAME:PLSegment', 'SegmentType:=', 'Line', 'StartIndex:=', 47, 'NoOfPoints:=', 2])
pts.append(['NAME:PLPoint', 'X:=', '-1.033500mm', 'Y:=', '2.584000mm', 'Z:=', '0.0mm'])
segs.append(['NAME:PLSegment', 'SegmentType:=', 'Line', 'StartIndex:=', 48, 'NoOfPoints:=', 2])
pts.append(['NAME:PLPoint', 'X:=', '-1.033500mm', 'Y:=', '2.406000mm', 'Z:=', '0.0mm'])
segs.append(['NAME:PLSegment', 'SegmentType:=', 'Line', 'StartIndex:=', 49, 'NoOfPoints:=', 2])
pts.append(['NAME:PLPoint', 'X:=', '-0.784500mm', 'Y:=', '2.406000mm', 'Z:=', '0.0mm'])
segs.append(['NAME:PLSegment', 'SegmentType:=', 'Line', 'StartIndex:=', 50, 'NoOfPoints:=', 2])
pts.append(['NAME:PLPoint', 'X:=', '-0.784500mm', 'Y:=', '2.184000mm', 'Z:=', '0.0mm'])
segs.append(['NAME:PLSegment', 'SegmentType:=', 'Line', 'StartIndex:=', 51, 'NoOfPoints:=', 2])
pts.append(['NAME:PLPoint', 'X:=', '-1.033500mm', 'Y:=', '2.184000mm', 'Z:=', '0.0mm'])
segs.append(['NAME:PLSegment', 'SegmentType:=', 'Line', 'StartIndex:=', 52, 'NoOfPoints:=', 2])
pts.append(['NAME:PLPoint', 'X:=', '-1.033500mm', 'Y:=', '2.006000mm', 'Z:=', '0.0mm'])
segs.append(['NAME:PLSegment', 'SegmentType:=', 'Line', 'StartIndex:=', 53, 'NoOfPoints:=', 2])
pts.append(['NAME:PLPoint', 'X:=', '-0.784500mm', 'Y:=', '2.006000mm', 'Z:=', '0.0mm'])
segs.append(['NAME:PLSegment', 'SegmentType:=', 'Line', 'StartIndex:=', 54, 'NoOfPoints:=', 2])
pts.append(['NAME:PLPoint', 'X:=', '-0.784500mm', 'Y:=', '1.784000mm', 'Z:=', '0.0mm'])
segs.append(['NAME:PLSegment', 'SegmentType:=', 'Line', 'StartIndex:=', 55, 'NoOfPoints:=', 2])
pts.append(['NAME:PLPoint', 'X:=', '-1.033500mm', 'Y:=', '1.784000mm', 'Z:=', '0.0mm'])
segs.append(['NAME:PLSegment', 'SegmentType:=', 'Line', 'StartIndex:=', 56, 'NoOfPoints:=', 2])
pts.append(['NAME:PLPoint', 'X:=', '-1.033500mm', 'Y:=', '1.606000mm', 'Z:=', '0.0mm'])
segs.append(['NAME:PLSegment', 'SegmentType:=', 'Line', 'StartIndex:=', 57, 'NoOfPoints:=', 2])
pts.append(['NAME:PLPoint', 'X:=', '-0.784500mm', 'Y:=', '1.606000mm', 'Z:=', '0.0mm'])
segs.append(['NAME:PLSegment', 'SegmentType:=', 'Line', 'StartIndex:=', 58, 'NoOfPoints:=', 2])
pts.append(['NAME:PLPoint', 'X:=', '-0.784500mm', 'Y:=', '1.384000mm', 'Z:=', '0.0mm'])
segs.append(['NAME:PLSegment', 'SegmentType:=', 'Line', 'StartIndex:=', 59, 'NoOfPoints:=', 2])
pts.append(['NAME:PLPoint', 'X:=', '-1.033500mm', 'Y:=', '1.384000mm', 'Z:=', '0.0mm'])
segs.append(['NAME:PLSegment', 'SegmentType:=', 'Line', 'StartIndex:=', 60, 'NoOfPoints:=', 2])
pts.append(['NAME:PLPoint', 'X:=', '-1.033500mm', 'Y:=', '1.206000mm', 'Z:=', '0.0mm'])
segs.append(['NAME:PLSegment', 'SegmentType:=', 'Line', 'StartIndex:=', 61, 'NoOfPoints:=', 2])
pts.append(['NAME:PLPoint', 'X:=', '-0.784500mm', 'Y:=', '1.206000mm', 'Z:=', '0.0mm'])
segs.append(['NAME:PLSegment', 'SegmentType:=', 'Line', 'StartIndex:=', 62, 'NoOfPoints:=', 2])
pts.append(['NAME:PLPoint', 'X:=', '-0.784500mm', 'Y:=', '0.984000mm', 'Z:=', '0.0mm'])
segs.append(['NAME:PLSegment', 'SegmentType:=', 'Line', 'StartIndex:=', 63, 'NoOfPoints:=', 2])
pts.append(['NAME:PLPoint', 'X:=', '-0.925000mm', 'Y:=', '0.984000mm', 'Z:=', '0.0mm'])
segs.append(['NAME:PLSegment', 'SegmentType:=', 'Line', 'StartIndex:=', 64, 'NoOfPoints:=', 2])
pts.append(['NAME:PLPoint', 'X:=', '-0.925000mm', 'Y:=', '1.006000mm', 'Z:=', '0.0mm'])
segs.append(['NAME:PLSegment', 'SegmentType:=', 'Line', 'StartIndex:=', 65, 'NoOfPoints:=', 2])
pts.append(['NAME:PLPoint', 'X:=', '-0.806500mm', 'Y:=', '1.006000mm', 'Z:=', '0.0mm'])
oEditor.CreatePolyline(
    ['NAME:PolylineParameters', 'IsPolylineCovered:=', True, 'IsPolylineClosed:=', True, pts, segs],
    [
        'NAME:Attributes',
        'Name:=', 'cut_Readout_Q3_53',
        'Flags:=', '',
        'Color:=', '(255 100 100)',
        'Transparency:=', 0.0,
        'PartCoordinateSystem:=', 'Global',
        'UDMId:=', '',
        'MaterialName:=', 'vacuum',
        'SolveInside:=', True
    ]
)
# Element: trace_Readout_Q5_54
pts = ['NAME:PolylinePoints']
segs = ['NAME:PolylineSegments']
pts.append(['NAME:PLPoint', 'X:=', '0.790500mm', 'Y:=', '0.990000mm', 'Z:=', '0.0mm'])
segs.append(['NAME:PLSegment', 'SegmentType:=', 'Line', 'StartIndex:=', 0, 'NoOfPoints:=', 2])
pts.append(['NAME:PLPoint', 'X:=', '0.790500mm', 'Y:=', '1.200000mm', 'Z:=', '0.0mm'])
segs.append(['NAME:PLSegment', 'SegmentType:=', 'Line', 'StartIndex:=', 1, 'NoOfPoints:=', 2])
pts.append(['NAME:PLPoint', 'X:=', '1.039500mm', 'Y:=', '1.200000mm', 'Z:=', '0.0mm'])
segs.append(['NAME:PLSegment', 'SegmentType:=', 'Line', 'StartIndex:=', 2, 'NoOfPoints:=', 2])
pts.append(['NAME:PLPoint', 'X:=', '1.039500mm', 'Y:=', '1.390000mm', 'Z:=', '0.0mm'])
segs.append(['NAME:PLSegment', 'SegmentType:=', 'Line', 'StartIndex:=', 3, 'NoOfPoints:=', 2])
pts.append(['NAME:PLPoint', 'X:=', '0.790500mm', 'Y:=', '1.390000mm', 'Z:=', '0.0mm'])
segs.append(['NAME:PLSegment', 'SegmentType:=', 'Line', 'StartIndex:=', 4, 'NoOfPoints:=', 2])
pts.append(['NAME:PLPoint', 'X:=', '0.790500mm', 'Y:=', '1.600000mm', 'Z:=', '0.0mm'])
segs.append(['NAME:PLSegment', 'SegmentType:=', 'Line', 'StartIndex:=', 5, 'NoOfPoints:=', 2])
pts.append(['NAME:PLPoint', 'X:=', '1.039500mm', 'Y:=', '1.600000mm', 'Z:=', '0.0mm'])
segs.append(['NAME:PLSegment', 'SegmentType:=', 'Line', 'StartIndex:=', 6, 'NoOfPoints:=', 2])
pts.append(['NAME:PLPoint', 'X:=', '1.039500mm', 'Y:=', '1.790000mm', 'Z:=', '0.0mm'])
segs.append(['NAME:PLSegment', 'SegmentType:=', 'Line', 'StartIndex:=', 7, 'NoOfPoints:=', 2])
pts.append(['NAME:PLPoint', 'X:=', '0.790500mm', 'Y:=', '1.790000mm', 'Z:=', '0.0mm'])
segs.append(['NAME:PLSegment', 'SegmentType:=', 'Line', 'StartIndex:=', 8, 'NoOfPoints:=', 2])
pts.append(['NAME:PLPoint', 'X:=', '0.790500mm', 'Y:=', '2.000000mm', 'Z:=', '0.0mm'])
segs.append(['NAME:PLSegment', 'SegmentType:=', 'Line', 'StartIndex:=', 9, 'NoOfPoints:=', 2])
pts.append(['NAME:PLPoint', 'X:=', '1.039500mm', 'Y:=', '2.000000mm', 'Z:=', '0.0mm'])
segs.append(['NAME:PLSegment', 'SegmentType:=', 'Line', 'StartIndex:=', 10, 'NoOfPoints:=', 2])
pts.append(['NAME:PLPoint', 'X:=', '1.039500mm', 'Y:=', '2.190000mm', 'Z:=', '0.0mm'])
segs.append(['NAME:PLSegment', 'SegmentType:=', 'Line', 'StartIndex:=', 11, 'NoOfPoints:=', 2])
pts.append(['NAME:PLPoint', 'X:=', '0.790500mm', 'Y:=', '2.190000mm', 'Z:=', '0.0mm'])
segs.append(['NAME:PLSegment', 'SegmentType:=', 'Line', 'StartIndex:=', 12, 'NoOfPoints:=', 2])
pts.append(['NAME:PLPoint', 'X:=', '0.790500mm', 'Y:=', '2.400000mm', 'Z:=', '0.0mm'])
segs.append(['NAME:PLSegment', 'SegmentType:=', 'Line', 'StartIndex:=', 13, 'NoOfPoints:=', 2])
pts.append(['NAME:PLPoint', 'X:=', '1.039500mm', 'Y:=', '2.400000mm', 'Z:=', '0.0mm'])
segs.append(['NAME:PLSegment', 'SegmentType:=', 'Line', 'StartIndex:=', 14, 'NoOfPoints:=', 2])
pts.append(['NAME:PLPoint', 'X:=', '1.039500mm', 'Y:=', '2.590000mm', 'Z:=', '0.0mm'])
segs.append(['NAME:PLSegment', 'SegmentType:=', 'Line', 'StartIndex:=', 15, 'NoOfPoints:=', 2])
pts.append(['NAME:PLPoint', 'X:=', '0.790500mm', 'Y:=', '2.590000mm', 'Z:=', '0.0mm'])
segs.append(['NAME:PLSegment', 'SegmentType:=', 'Line', 'StartIndex:=', 16, 'NoOfPoints:=', 2])
pts.append(['NAME:PLPoint', 'X:=', '0.790500mm', 'Y:=', '2.800000mm', 'Z:=', '0.0mm'])
segs.append(['NAME:PLSegment', 'SegmentType:=', 'Line', 'StartIndex:=', 17, 'NoOfPoints:=', 2])
pts.append(['NAME:PLPoint', 'X:=', '1.039500mm', 'Y:=', '2.800000mm', 'Z:=', '0.0mm'])
segs.append(['NAME:PLSegment', 'SegmentType:=', 'Line', 'StartIndex:=', 18, 'NoOfPoints:=', 2])
pts.append(['NAME:PLPoint', 'X:=', '1.039500mm', 'Y:=', '2.990000mm', 'Z:=', '0.0mm'])
segs.append(['NAME:PLSegment', 'SegmentType:=', 'Line', 'StartIndex:=', 19, 'NoOfPoints:=', 2])
pts.append(['NAME:PLPoint', 'X:=', '0.790500mm', 'Y:=', '2.990000mm', 'Z:=', '0.0mm'])
segs.append(['NAME:PLSegment', 'SegmentType:=', 'Line', 'StartIndex:=', 20, 'NoOfPoints:=', 2])
pts.append(['NAME:PLPoint', 'X:=', '0.790500mm', 'Y:=', '3.200000mm', 'Z:=', '0.0mm'])
segs.append(['NAME:PLSegment', 'SegmentType:=', 'Line', 'StartIndex:=', 21, 'NoOfPoints:=', 2])
pts.append(['NAME:PLPoint', 'X:=', '1.039500mm', 'Y:=', '3.200000mm', 'Z:=', '0.0mm'])
segs.append(['NAME:PLSegment', 'SegmentType:=', 'Line', 'StartIndex:=', 22, 'NoOfPoints:=', 2])
pts.append(['NAME:PLPoint', 'X:=', '1.039500mm', 'Y:=', '3.390000mm', 'Z:=', '0.0mm'])
segs.append(['NAME:PLSegment', 'SegmentType:=', 'Line', 'StartIndex:=', 23, 'NoOfPoints:=', 2])
pts.append(['NAME:PLPoint', 'X:=', '0.790500mm', 'Y:=', '3.390000mm', 'Z:=', '0.0mm'])
segs.append(['NAME:PLSegment', 'SegmentType:=', 'Line', 'StartIndex:=', 24, 'NoOfPoints:=', 2])
pts.append(['NAME:PLPoint', 'X:=', '0.790500mm', 'Y:=', '3.600000mm', 'Z:=', '0.0mm'])
segs.append(['NAME:PLSegment', 'SegmentType:=', 'Line', 'StartIndex:=', 25, 'NoOfPoints:=', 2])
pts.append(['NAME:PLPoint', 'X:=', '1.039500mm', 'Y:=', '3.600000mm', 'Z:=', '0.0mm'])
segs.append(['NAME:PLSegment', 'SegmentType:=', 'Line', 'StartIndex:=', 26, 'NoOfPoints:=', 2])
pts.append(['NAME:PLPoint', 'X:=', '1.039500mm', 'Y:=', '3.790000mm', 'Z:=', '0.0mm'])
segs.append(['NAME:PLSegment', 'SegmentType:=', 'Line', 'StartIndex:=', 27, 'NoOfPoints:=', 2])
pts.append(['NAME:PLPoint', 'X:=', '0.790500mm', 'Y:=', '3.790000mm', 'Z:=', '0.0mm'])
segs.append(['NAME:PLSegment', 'SegmentType:=', 'Line', 'StartIndex:=', 28, 'NoOfPoints:=', 2])
pts.append(['NAME:PLPoint', 'X:=', '0.790500mm', 'Y:=', '4.000000mm', 'Z:=', '0.0mm'])
segs.append(['NAME:PLSegment', 'SegmentType:=', 'Line', 'StartIndex:=', 29, 'NoOfPoints:=', 2])
pts.append(['NAME:PLPoint', 'X:=', '0.995000mm', 'Y:=', '4.000000mm', 'Z:=', '0.0mm'])
segs.append(['NAME:PLSegment', 'SegmentType:=', 'Line', 'StartIndex:=', 30, 'NoOfPoints:=', 2])
pts.append(['NAME:PLPoint', 'X:=', '0.995000mm', 'Y:=', '4.175000mm', 'Z:=', '0.0mm'])
segs.append(['NAME:PLSegment', 'SegmentType:=', 'Line', 'StartIndex:=', 31, 'NoOfPoints:=', 2])
pts.append(['NAME:PLPoint', 'X:=', '1.005000mm', 'Y:=', '4.175000mm', 'Z:=', '0.0mm'])
segs.append(['NAME:PLSegment', 'SegmentType:=', 'Line', 'StartIndex:=', 32, 'NoOfPoints:=', 2])
pts.append(['NAME:PLPoint', 'X:=', '1.005000mm', 'Y:=', '3.990000mm', 'Z:=', '0.0mm'])
segs.append(['NAME:PLSegment', 'SegmentType:=', 'Line', 'StartIndex:=', 33, 'NoOfPoints:=', 2])
pts.append(['NAME:PLPoint', 'X:=', '0.800500mm', 'Y:=', '3.990000mm', 'Z:=', '0.0mm'])
segs.append(['NAME:PLSegment', 'SegmentType:=', 'Line', 'StartIndex:=', 34, 'NoOfPoints:=', 2])
pts.append(['NAME:PLPoint', 'X:=', '0.800500mm', 'Y:=', '3.800000mm', 'Z:=', '0.0mm'])
segs.append(['NAME:PLSegment', 'SegmentType:=', 'Line', 'StartIndex:=', 35, 'NoOfPoints:=', 2])
pts.append(['NAME:PLPoint', 'X:=', '1.049500mm', 'Y:=', '3.800000mm', 'Z:=', '0.0mm'])
segs.append(['NAME:PLSegment', 'SegmentType:=', 'Line', 'StartIndex:=', 36, 'NoOfPoints:=', 2])
pts.append(['NAME:PLPoint', 'X:=', '1.049500mm', 'Y:=', '3.590000mm', 'Z:=', '0.0mm'])
segs.append(['NAME:PLSegment', 'SegmentType:=', 'Line', 'StartIndex:=', 37, 'NoOfPoints:=', 2])
pts.append(['NAME:PLPoint', 'X:=', '0.800500mm', 'Y:=', '3.590000mm', 'Z:=', '0.0mm'])
segs.append(['NAME:PLSegment', 'SegmentType:=', 'Line', 'StartIndex:=', 38, 'NoOfPoints:=', 2])
pts.append(['NAME:PLPoint', 'X:=', '0.800500mm', 'Y:=', '3.400000mm', 'Z:=', '0.0mm'])
segs.append(['NAME:PLSegment', 'SegmentType:=', 'Line', 'StartIndex:=', 39, 'NoOfPoints:=', 2])
pts.append(['NAME:PLPoint', 'X:=', '1.049500mm', 'Y:=', '3.400000mm', 'Z:=', '0.0mm'])
segs.append(['NAME:PLSegment', 'SegmentType:=', 'Line', 'StartIndex:=', 40, 'NoOfPoints:=', 2])
pts.append(['NAME:PLPoint', 'X:=', '1.049500mm', 'Y:=', '3.190000mm', 'Z:=', '0.0mm'])
segs.append(['NAME:PLSegment', 'SegmentType:=', 'Line', 'StartIndex:=', 41, 'NoOfPoints:=', 2])
pts.append(['NAME:PLPoint', 'X:=', '0.800500mm', 'Y:=', '3.190000mm', 'Z:=', '0.0mm'])
segs.append(['NAME:PLSegment', 'SegmentType:=', 'Line', 'StartIndex:=', 42, 'NoOfPoints:=', 2])
pts.append(['NAME:PLPoint', 'X:=', '0.800500mm', 'Y:=', '3.000000mm', 'Z:=', '0.0mm'])
segs.append(['NAME:PLSegment', 'SegmentType:=', 'Line', 'StartIndex:=', 43, 'NoOfPoints:=', 2])
pts.append(['NAME:PLPoint', 'X:=', '1.049500mm', 'Y:=', '3.000000mm', 'Z:=', '0.0mm'])
segs.append(['NAME:PLSegment', 'SegmentType:=', 'Line', 'StartIndex:=', 44, 'NoOfPoints:=', 2])
pts.append(['NAME:PLPoint', 'X:=', '1.049500mm', 'Y:=', '2.790000mm', 'Z:=', '0.0mm'])
segs.append(['NAME:PLSegment', 'SegmentType:=', 'Line', 'StartIndex:=', 45, 'NoOfPoints:=', 2])
pts.append(['NAME:PLPoint', 'X:=', '0.800500mm', 'Y:=', '2.790000mm', 'Z:=', '0.0mm'])
segs.append(['NAME:PLSegment', 'SegmentType:=', 'Line', 'StartIndex:=', 46, 'NoOfPoints:=', 2])
pts.append(['NAME:PLPoint', 'X:=', '0.800500mm', 'Y:=', '2.600000mm', 'Z:=', '0.0mm'])
segs.append(['NAME:PLSegment', 'SegmentType:=', 'Line', 'StartIndex:=', 47, 'NoOfPoints:=', 2])
pts.append(['NAME:PLPoint', 'X:=', '1.049500mm', 'Y:=', '2.600000mm', 'Z:=', '0.0mm'])
segs.append(['NAME:PLSegment', 'SegmentType:=', 'Line', 'StartIndex:=', 48, 'NoOfPoints:=', 2])
pts.append(['NAME:PLPoint', 'X:=', '1.049500mm', 'Y:=', '2.390000mm', 'Z:=', '0.0mm'])
segs.append(['NAME:PLSegment', 'SegmentType:=', 'Line', 'StartIndex:=', 49, 'NoOfPoints:=', 2])
pts.append(['NAME:PLPoint', 'X:=', '0.800500mm', 'Y:=', '2.390000mm', 'Z:=', '0.0mm'])
segs.append(['NAME:PLSegment', 'SegmentType:=', 'Line', 'StartIndex:=', 50, 'NoOfPoints:=', 2])
pts.append(['NAME:PLPoint', 'X:=', '0.800500mm', 'Y:=', '2.200000mm', 'Z:=', '0.0mm'])
segs.append(['NAME:PLSegment', 'SegmentType:=', 'Line', 'StartIndex:=', 51, 'NoOfPoints:=', 2])
pts.append(['NAME:PLPoint', 'X:=', '1.049500mm', 'Y:=', '2.200000mm', 'Z:=', '0.0mm'])
segs.append(['NAME:PLSegment', 'SegmentType:=', 'Line', 'StartIndex:=', 52, 'NoOfPoints:=', 2])
pts.append(['NAME:PLPoint', 'X:=', '1.049500mm', 'Y:=', '1.990000mm', 'Z:=', '0.0mm'])
segs.append(['NAME:PLSegment', 'SegmentType:=', 'Line', 'StartIndex:=', 53, 'NoOfPoints:=', 2])
pts.append(['NAME:PLPoint', 'X:=', '0.800500mm', 'Y:=', '1.990000mm', 'Z:=', '0.0mm'])
segs.append(['NAME:PLSegment', 'SegmentType:=', 'Line', 'StartIndex:=', 54, 'NoOfPoints:=', 2])
pts.append(['NAME:PLPoint', 'X:=', '0.800500mm', 'Y:=', '1.800000mm', 'Z:=', '0.0mm'])
segs.append(['NAME:PLSegment', 'SegmentType:=', 'Line', 'StartIndex:=', 55, 'NoOfPoints:=', 2])
pts.append(['NAME:PLPoint', 'X:=', '1.049500mm', 'Y:=', '1.800000mm', 'Z:=', '0.0mm'])
segs.append(['NAME:PLSegment', 'SegmentType:=', 'Line', 'StartIndex:=', 56, 'NoOfPoints:=', 2])
pts.append(['NAME:PLPoint', 'X:=', '1.049500mm', 'Y:=', '1.590000mm', 'Z:=', '0.0mm'])
segs.append(['NAME:PLSegment', 'SegmentType:=', 'Line', 'StartIndex:=', 57, 'NoOfPoints:=', 2])
pts.append(['NAME:PLPoint', 'X:=', '0.800500mm', 'Y:=', '1.590000mm', 'Z:=', '0.0mm'])
segs.append(['NAME:PLSegment', 'SegmentType:=', 'Line', 'StartIndex:=', 58, 'NoOfPoints:=', 2])
pts.append(['NAME:PLPoint', 'X:=', '0.800500mm', 'Y:=', '1.400000mm', 'Z:=', '0.0mm'])
segs.append(['NAME:PLSegment', 'SegmentType:=', 'Line', 'StartIndex:=', 59, 'NoOfPoints:=', 2])
pts.append(['NAME:PLPoint', 'X:=', '1.049500mm', 'Y:=', '1.400000mm', 'Z:=', '0.0mm'])
segs.append(['NAME:PLSegment', 'SegmentType:=', 'Line', 'StartIndex:=', 60, 'NoOfPoints:=', 2])
pts.append(['NAME:PLPoint', 'X:=', '1.049500mm', 'Y:=', '1.190000mm', 'Z:=', '0.0mm'])
segs.append(['NAME:PLSegment', 'SegmentType:=', 'Line', 'StartIndex:=', 61, 'NoOfPoints:=', 2])
pts.append(['NAME:PLPoint', 'X:=', '0.800500mm', 'Y:=', '1.190000mm', 'Z:=', '0.0mm'])
segs.append(['NAME:PLSegment', 'SegmentType:=', 'Line', 'StartIndex:=', 62, 'NoOfPoints:=', 2])
pts.append(['NAME:PLPoint', 'X:=', '0.800500mm', 'Y:=', '1.000000mm', 'Z:=', '0.0mm'])
segs.append(['NAME:PLSegment', 'SegmentType:=', 'Line', 'StartIndex:=', 63, 'NoOfPoints:=', 2])
pts.append(['NAME:PLPoint', 'X:=', '0.925000mm', 'Y:=', '1.000000mm', 'Z:=', '0.0mm'])
segs.append(['NAME:PLSegment', 'SegmentType:=', 'Line', 'StartIndex:=', 64, 'NoOfPoints:=', 2])
pts.append(['NAME:PLPoint', 'X:=', '0.925000mm', 'Y:=', '0.990000mm', 'Z:=', '0.0mm'])
segs.append(['NAME:PLSegment', 'SegmentType:=', 'Line', 'StartIndex:=', 65, 'NoOfPoints:=', 2])
pts.append(['NAME:PLPoint', 'X:=', '0.790500mm', 'Y:=', '0.990000mm', 'Z:=', '0.0mm'])
oEditor.CreatePolyline(
    ['NAME:PolylineParameters', 'IsPolylineCovered:=', True, 'IsPolylineClosed:=', True, pts, segs],
    [
        'NAME:Attributes',
        'Name:=', 'trace_Readout_Q5_54',
        'Flags:=', '',
        'Color:=', '(200 220 255)',
        'Transparency:=', 0.0,
        'PartCoordinateSystem:=', 'Global',
        'UDMId:=', '',
        'MaterialName:=', 'vacuum',
        'SolveInside:=', True
    ]
)
# Element: cut_Readout_Q5_55
pts = ['NAME:PolylinePoints']
segs = ['NAME:PolylineSegments']
pts.append(['NAME:PLPoint', 'X:=', '0.784500mm', 'Y:=', '0.984000mm', 'Z:=', '0.0mm'])
segs.append(['NAME:PLSegment', 'SegmentType:=', 'Line', 'StartIndex:=', 0, 'NoOfPoints:=', 2])
pts.append(['NAME:PLPoint', 'X:=', '0.784500mm', 'Y:=', '1.206000mm', 'Z:=', '0.0mm'])
segs.append(['NAME:PLSegment', 'SegmentType:=', 'Line', 'StartIndex:=', 1, 'NoOfPoints:=', 2])
pts.append(['NAME:PLPoint', 'X:=', '1.033500mm', 'Y:=', '1.206000mm', 'Z:=', '0.0mm'])
segs.append(['NAME:PLSegment', 'SegmentType:=', 'Line', 'StartIndex:=', 2, 'NoOfPoints:=', 2])
pts.append(['NAME:PLPoint', 'X:=', '1.033500mm', 'Y:=', '1.384000mm', 'Z:=', '0.0mm'])
segs.append(['NAME:PLSegment', 'SegmentType:=', 'Line', 'StartIndex:=', 3, 'NoOfPoints:=', 2])
pts.append(['NAME:PLPoint', 'X:=', '0.784500mm', 'Y:=', '1.384000mm', 'Z:=', '0.0mm'])
segs.append(['NAME:PLSegment', 'SegmentType:=', 'Line', 'StartIndex:=', 4, 'NoOfPoints:=', 2])
pts.append(['NAME:PLPoint', 'X:=', '0.784500mm', 'Y:=', '1.606000mm', 'Z:=', '0.0mm'])
segs.append(['NAME:PLSegment', 'SegmentType:=', 'Line', 'StartIndex:=', 5, 'NoOfPoints:=', 2])
pts.append(['NAME:PLPoint', 'X:=', '1.033500mm', 'Y:=', '1.606000mm', 'Z:=', '0.0mm'])
segs.append(['NAME:PLSegment', 'SegmentType:=', 'Line', 'StartIndex:=', 6, 'NoOfPoints:=', 2])
pts.append(['NAME:PLPoint', 'X:=', '1.033500mm', 'Y:=', '1.784000mm', 'Z:=', '0.0mm'])
segs.append(['NAME:PLSegment', 'SegmentType:=', 'Line', 'StartIndex:=', 7, 'NoOfPoints:=', 2])
pts.append(['NAME:PLPoint', 'X:=', '0.784500mm', 'Y:=', '1.784000mm', 'Z:=', '0.0mm'])
segs.append(['NAME:PLSegment', 'SegmentType:=', 'Line', 'StartIndex:=', 8, 'NoOfPoints:=', 2])
pts.append(['NAME:PLPoint', 'X:=', '0.784500mm', 'Y:=', '2.006000mm', 'Z:=', '0.0mm'])
segs.append(['NAME:PLSegment', 'SegmentType:=', 'Line', 'StartIndex:=', 9, 'NoOfPoints:=', 2])
pts.append(['NAME:PLPoint', 'X:=', '1.033500mm', 'Y:=', '2.006000mm', 'Z:=', '0.0mm'])
segs.append(['NAME:PLSegment', 'SegmentType:=', 'Line', 'StartIndex:=', 10, 'NoOfPoints:=', 2])
pts.append(['NAME:PLPoint', 'X:=', '1.033500mm', 'Y:=', '2.184000mm', 'Z:=', '0.0mm'])
segs.append(['NAME:PLSegment', 'SegmentType:=', 'Line', 'StartIndex:=', 11, 'NoOfPoints:=', 2])
pts.append(['NAME:PLPoint', 'X:=', '0.784500mm', 'Y:=', '2.184000mm', 'Z:=', '0.0mm'])
segs.append(['NAME:PLSegment', 'SegmentType:=', 'Line', 'StartIndex:=', 12, 'NoOfPoints:=', 2])
pts.append(['NAME:PLPoint', 'X:=', '0.784500mm', 'Y:=', '2.406000mm', 'Z:=', '0.0mm'])
segs.append(['NAME:PLSegment', 'SegmentType:=', 'Line', 'StartIndex:=', 13, 'NoOfPoints:=', 2])
pts.append(['NAME:PLPoint', 'X:=', '1.033500mm', 'Y:=', '2.406000mm', 'Z:=', '0.0mm'])
segs.append(['NAME:PLSegment', 'SegmentType:=', 'Line', 'StartIndex:=', 14, 'NoOfPoints:=', 2])
pts.append(['NAME:PLPoint', 'X:=', '1.033500mm', 'Y:=', '2.584000mm', 'Z:=', '0.0mm'])
segs.append(['NAME:PLSegment', 'SegmentType:=', 'Line', 'StartIndex:=', 15, 'NoOfPoints:=', 2])
pts.append(['NAME:PLPoint', 'X:=', '0.784500mm', 'Y:=', '2.584000mm', 'Z:=', '0.0mm'])
segs.append(['NAME:PLSegment', 'SegmentType:=', 'Line', 'StartIndex:=', 16, 'NoOfPoints:=', 2])
pts.append(['NAME:PLPoint', 'X:=', '0.784500mm', 'Y:=', '2.806000mm', 'Z:=', '0.0mm'])
segs.append(['NAME:PLSegment', 'SegmentType:=', 'Line', 'StartIndex:=', 17, 'NoOfPoints:=', 2])
pts.append(['NAME:PLPoint', 'X:=', '1.033500mm', 'Y:=', '2.806000mm', 'Z:=', '0.0mm'])
segs.append(['NAME:PLSegment', 'SegmentType:=', 'Line', 'StartIndex:=', 18, 'NoOfPoints:=', 2])
pts.append(['NAME:PLPoint', 'X:=', '1.033500mm', 'Y:=', '2.984000mm', 'Z:=', '0.0mm'])
segs.append(['NAME:PLSegment', 'SegmentType:=', 'Line', 'StartIndex:=', 19, 'NoOfPoints:=', 2])
pts.append(['NAME:PLPoint', 'X:=', '0.784500mm', 'Y:=', '2.984000mm', 'Z:=', '0.0mm'])
segs.append(['NAME:PLSegment', 'SegmentType:=', 'Line', 'StartIndex:=', 20, 'NoOfPoints:=', 2])
pts.append(['NAME:PLPoint', 'X:=', '0.784500mm', 'Y:=', '3.206000mm', 'Z:=', '0.0mm'])
segs.append(['NAME:PLSegment', 'SegmentType:=', 'Line', 'StartIndex:=', 21, 'NoOfPoints:=', 2])
pts.append(['NAME:PLPoint', 'X:=', '1.033500mm', 'Y:=', '3.206000mm', 'Z:=', '0.0mm'])
segs.append(['NAME:PLSegment', 'SegmentType:=', 'Line', 'StartIndex:=', 22, 'NoOfPoints:=', 2])
pts.append(['NAME:PLPoint', 'X:=', '1.033500mm', 'Y:=', '3.384000mm', 'Z:=', '0.0mm'])
segs.append(['NAME:PLSegment', 'SegmentType:=', 'Line', 'StartIndex:=', 23, 'NoOfPoints:=', 2])
pts.append(['NAME:PLPoint', 'X:=', '0.784500mm', 'Y:=', '3.384000mm', 'Z:=', '0.0mm'])
segs.append(['NAME:PLSegment', 'SegmentType:=', 'Line', 'StartIndex:=', 24, 'NoOfPoints:=', 2])
pts.append(['NAME:PLPoint', 'X:=', '0.784500mm', 'Y:=', '3.606000mm', 'Z:=', '0.0mm'])
segs.append(['NAME:PLSegment', 'SegmentType:=', 'Line', 'StartIndex:=', 25, 'NoOfPoints:=', 2])
pts.append(['NAME:PLPoint', 'X:=', '1.033500mm', 'Y:=', '3.606000mm', 'Z:=', '0.0mm'])
segs.append(['NAME:PLSegment', 'SegmentType:=', 'Line', 'StartIndex:=', 26, 'NoOfPoints:=', 2])
pts.append(['NAME:PLPoint', 'X:=', '1.033500mm', 'Y:=', '3.784000mm', 'Z:=', '0.0mm'])
segs.append(['NAME:PLSegment', 'SegmentType:=', 'Line', 'StartIndex:=', 27, 'NoOfPoints:=', 2])
pts.append(['NAME:PLPoint', 'X:=', '0.784500mm', 'Y:=', '3.784000mm', 'Z:=', '0.0mm'])
segs.append(['NAME:PLSegment', 'SegmentType:=', 'Line', 'StartIndex:=', 28, 'NoOfPoints:=', 2])
pts.append(['NAME:PLPoint', 'X:=', '0.784500mm', 'Y:=', '4.006000mm', 'Z:=', '0.0mm'])
segs.append(['NAME:PLSegment', 'SegmentType:=', 'Line', 'StartIndex:=', 29, 'NoOfPoints:=', 2])
pts.append(['NAME:PLPoint', 'X:=', '0.989000mm', 'Y:=', '4.006000mm', 'Z:=', '0.0mm'])
segs.append(['NAME:PLSegment', 'SegmentType:=', 'Line', 'StartIndex:=', 30, 'NoOfPoints:=', 2])
pts.append(['NAME:PLPoint', 'X:=', '0.989000mm', 'Y:=', '4.175000mm', 'Z:=', '0.0mm'])
segs.append(['NAME:PLSegment', 'SegmentType:=', 'Line', 'StartIndex:=', 31, 'NoOfPoints:=', 2])
pts.append(['NAME:PLPoint', 'X:=', '1.011000mm', 'Y:=', '4.175000mm', 'Z:=', '0.0mm'])
segs.append(['NAME:PLSegment', 'SegmentType:=', 'Line', 'StartIndex:=', 32, 'NoOfPoints:=', 2])
pts.append(['NAME:PLPoint', 'X:=', '1.011000mm', 'Y:=', '3.984000mm', 'Z:=', '0.0mm'])
segs.append(['NAME:PLSegment', 'SegmentType:=', 'Line', 'StartIndex:=', 33, 'NoOfPoints:=', 2])
pts.append(['NAME:PLPoint', 'X:=', '0.806500mm', 'Y:=', '3.984000mm', 'Z:=', '0.0mm'])
segs.append(['NAME:PLSegment', 'SegmentType:=', 'Line', 'StartIndex:=', 34, 'NoOfPoints:=', 2])
pts.append(['NAME:PLPoint', 'X:=', '0.806500mm', 'Y:=', '3.806000mm', 'Z:=', '0.0mm'])
segs.append(['NAME:PLSegment', 'SegmentType:=', 'Line', 'StartIndex:=', 35, 'NoOfPoints:=', 2])
pts.append(['NAME:PLPoint', 'X:=', '1.055500mm', 'Y:=', '3.806000mm', 'Z:=', '0.0mm'])
segs.append(['NAME:PLSegment', 'SegmentType:=', 'Line', 'StartIndex:=', 36, 'NoOfPoints:=', 2])
pts.append(['NAME:PLPoint', 'X:=', '1.055500mm', 'Y:=', '3.584000mm', 'Z:=', '0.0mm'])
segs.append(['NAME:PLSegment', 'SegmentType:=', 'Line', 'StartIndex:=', 37, 'NoOfPoints:=', 2])
pts.append(['NAME:PLPoint', 'X:=', '0.806500mm', 'Y:=', '3.584000mm', 'Z:=', '0.0mm'])
segs.append(['NAME:PLSegment', 'SegmentType:=', 'Line', 'StartIndex:=', 38, 'NoOfPoints:=', 2])
pts.append(['NAME:PLPoint', 'X:=', '0.806500mm', 'Y:=', '3.406000mm', 'Z:=', '0.0mm'])
segs.append(['NAME:PLSegment', 'SegmentType:=', 'Line', 'StartIndex:=', 39, 'NoOfPoints:=', 2])
pts.append(['NAME:PLPoint', 'X:=', '1.055500mm', 'Y:=', '3.406000mm', 'Z:=', '0.0mm'])
segs.append(['NAME:PLSegment', 'SegmentType:=', 'Line', 'StartIndex:=', 40, 'NoOfPoints:=', 2])
pts.append(['NAME:PLPoint', 'X:=', '1.055500mm', 'Y:=', '3.184000mm', 'Z:=', '0.0mm'])
segs.append(['NAME:PLSegment', 'SegmentType:=', 'Line', 'StartIndex:=', 41, 'NoOfPoints:=', 2])
pts.append(['NAME:PLPoint', 'X:=', '0.806500mm', 'Y:=', '3.184000mm', 'Z:=', '0.0mm'])
segs.append(['NAME:PLSegment', 'SegmentType:=', 'Line', 'StartIndex:=', 42, 'NoOfPoints:=', 2])
pts.append(['NAME:PLPoint', 'X:=', '0.806500mm', 'Y:=', '3.006000mm', 'Z:=', '0.0mm'])
segs.append(['NAME:PLSegment', 'SegmentType:=', 'Line', 'StartIndex:=', 43, 'NoOfPoints:=', 2])
pts.append(['NAME:PLPoint', 'X:=', '1.055500mm', 'Y:=', '3.006000mm', 'Z:=', '0.0mm'])
segs.append(['NAME:PLSegment', 'SegmentType:=', 'Line', 'StartIndex:=', 44, 'NoOfPoints:=', 2])
pts.append(['NAME:PLPoint', 'X:=', '1.055500mm', 'Y:=', '2.784000mm', 'Z:=', '0.0mm'])
segs.append(['NAME:PLSegment', 'SegmentType:=', 'Line', 'StartIndex:=', 45, 'NoOfPoints:=', 2])
pts.append(['NAME:PLPoint', 'X:=', '0.806500mm', 'Y:=', '2.784000mm', 'Z:=', '0.0mm'])
segs.append(['NAME:PLSegment', 'SegmentType:=', 'Line', 'StartIndex:=', 46, 'NoOfPoints:=', 2])
pts.append(['NAME:PLPoint', 'X:=', '0.806500mm', 'Y:=', '2.606000mm', 'Z:=', '0.0mm'])
segs.append(['NAME:PLSegment', 'SegmentType:=', 'Line', 'StartIndex:=', 47, 'NoOfPoints:=', 2])
pts.append(['NAME:PLPoint', 'X:=', '1.055500mm', 'Y:=', '2.606000mm', 'Z:=', '0.0mm'])
segs.append(['NAME:PLSegment', 'SegmentType:=', 'Line', 'StartIndex:=', 48, 'NoOfPoints:=', 2])
pts.append(['NAME:PLPoint', 'X:=', '1.055500mm', 'Y:=', '2.384000mm', 'Z:=', '0.0mm'])
segs.append(['NAME:PLSegment', 'SegmentType:=', 'Line', 'StartIndex:=', 49, 'NoOfPoints:=', 2])
pts.append(['NAME:PLPoint', 'X:=', '0.806500mm', 'Y:=', '2.384000mm', 'Z:=', '0.0mm'])
segs.append(['NAME:PLSegment', 'SegmentType:=', 'Line', 'StartIndex:=', 50, 'NoOfPoints:=', 2])
pts.append(['NAME:PLPoint', 'X:=', '0.806500mm', 'Y:=', '2.206000mm', 'Z:=', '0.0mm'])
segs.append(['NAME:PLSegment', 'SegmentType:=', 'Line', 'StartIndex:=', 51, 'NoOfPoints:=', 2])
pts.append(['NAME:PLPoint', 'X:=', '1.055500mm', 'Y:=', '2.206000mm', 'Z:=', '0.0mm'])
segs.append(['NAME:PLSegment', 'SegmentType:=', 'Line', 'StartIndex:=', 52, 'NoOfPoints:=', 2])
pts.append(['NAME:PLPoint', 'X:=', '1.055500mm', 'Y:=', '1.984000mm', 'Z:=', '0.0mm'])
segs.append(['NAME:PLSegment', 'SegmentType:=', 'Line', 'StartIndex:=', 53, 'NoOfPoints:=', 2])
pts.append(['NAME:PLPoint', 'X:=', '0.806500mm', 'Y:=', '1.984000mm', 'Z:=', '0.0mm'])
segs.append(['NAME:PLSegment', 'SegmentType:=', 'Line', 'StartIndex:=', 54, 'NoOfPoints:=', 2])
pts.append(['NAME:PLPoint', 'X:=', '0.806500mm', 'Y:=', '1.806000mm', 'Z:=', '0.0mm'])
segs.append(['NAME:PLSegment', 'SegmentType:=', 'Line', 'StartIndex:=', 55, 'NoOfPoints:=', 2])
pts.append(['NAME:PLPoint', 'X:=', '1.055500mm', 'Y:=', '1.806000mm', 'Z:=', '0.0mm'])
segs.append(['NAME:PLSegment', 'SegmentType:=', 'Line', 'StartIndex:=', 56, 'NoOfPoints:=', 2])
pts.append(['NAME:PLPoint', 'X:=', '1.055500mm', 'Y:=', '1.584000mm', 'Z:=', '0.0mm'])
segs.append(['NAME:PLSegment', 'SegmentType:=', 'Line', 'StartIndex:=', 57, 'NoOfPoints:=', 2])
pts.append(['NAME:PLPoint', 'X:=', '0.806500mm', 'Y:=', '1.584000mm', 'Z:=', '0.0mm'])
segs.append(['NAME:PLSegment', 'SegmentType:=', 'Line', 'StartIndex:=', 58, 'NoOfPoints:=', 2])
pts.append(['NAME:PLPoint', 'X:=', '0.806500mm', 'Y:=', '1.406000mm', 'Z:=', '0.0mm'])
segs.append(['NAME:PLSegment', 'SegmentType:=', 'Line', 'StartIndex:=', 59, 'NoOfPoints:=', 2])
pts.append(['NAME:PLPoint', 'X:=', '1.055500mm', 'Y:=', '1.406000mm', 'Z:=', '0.0mm'])
segs.append(['NAME:PLSegment', 'SegmentType:=', 'Line', 'StartIndex:=', 60, 'NoOfPoints:=', 2])
pts.append(['NAME:PLPoint', 'X:=', '1.055500mm', 'Y:=', '1.184000mm', 'Z:=', '0.0mm'])
segs.append(['NAME:PLSegment', 'SegmentType:=', 'Line', 'StartIndex:=', 61, 'NoOfPoints:=', 2])
pts.append(['NAME:PLPoint', 'X:=', '0.806500mm', 'Y:=', '1.184000mm', 'Z:=', '0.0mm'])
segs.append(['NAME:PLSegment', 'SegmentType:=', 'Line', 'StartIndex:=', 62, 'NoOfPoints:=', 2])
pts.append(['NAME:PLPoint', 'X:=', '0.806500mm', 'Y:=', '1.006000mm', 'Z:=', '0.0mm'])
segs.append(['NAME:PLSegment', 'SegmentType:=', 'Line', 'StartIndex:=', 63, 'NoOfPoints:=', 2])
pts.append(['NAME:PLPoint', 'X:=', '0.925000mm', 'Y:=', '1.006000mm', 'Z:=', '0.0mm'])
segs.append(['NAME:PLSegment', 'SegmentType:=', 'Line', 'StartIndex:=', 64, 'NoOfPoints:=', 2])
pts.append(['NAME:PLPoint', 'X:=', '0.925000mm', 'Y:=', '0.984000mm', 'Z:=', '0.0mm'])
segs.append(['NAME:PLSegment', 'SegmentType:=', 'Line', 'StartIndex:=', 65, 'NoOfPoints:=', 2])
pts.append(['NAME:PLPoint', 'X:=', '0.784500mm', 'Y:=', '0.984000mm', 'Z:=', '0.0mm'])
oEditor.CreatePolyline(
    ['NAME:PolylineParameters', 'IsPolylineCovered:=', True, 'IsPolylineClosed:=', True, pts, segs],
    [
        'NAME:Attributes',
        'Name:=', 'cut_Readout_Q5_55',
        'Flags:=', '',
        'Color:=', '(255 100 100)',
        'Transparency:=', 0.0,
        'PartCoordinateSystem:=', 'Global',
        'UDMId:=', '',
        'MaterialName:=', 'vacuum',
        'SolveInside:=', True
    ]
)
# Element: trace_Readout_Q2_56
pts = ['NAME:PolylinePoints']
segs = ['NAME:PolylineSegments']
pts.append(['NAME:PLPoint', 'X:=', '2.370000mm', 'Y:=', '2.225000mm', 'Z:=', '0.0mm'])
segs.append(['NAME:PLSegment', 'SegmentType:=', 'Line', 'StartIndex:=', 0, 'NoOfPoints:=', 2])
pts.append(['NAME:PLPoint', 'X:=', '2.034063mm', 'Y:=', '2.225000mm', 'Z:=', '0.0mm'])
segs.append(['NAME:PLSegment', 'SegmentType:=', 'Line', 'StartIndex:=', 1, 'NoOfPoints:=', 2])
pts.append(['NAME:PLPoint', 'X:=', '2.034063mm', 'Y:=', '2.435000mm', 'Z:=', '0.0mm'])
segs.append(['NAME:PLSegment', 'SegmentType:=', 'Line', 'StartIndex:=', 2, 'NoOfPoints:=', 2])
pts.append(['NAME:PLPoint', 'X:=', '2.705938mm', 'Y:=', '2.435000mm', 'Z:=', '0.0mm'])
segs.append(['NAME:PLSegment', 'SegmentType:=', 'Line', 'StartIndex:=', 3, 'NoOfPoints:=', 2])
pts.append(['NAME:PLPoint', 'X:=', '2.705938mm', 'Y:=', '2.625000mm', 'Z:=', '0.0mm'])
segs.append(['NAME:PLSegment', 'SegmentType:=', 'Line', 'StartIndex:=', 4, 'NoOfPoints:=', 2])
pts.append(['NAME:PLPoint', 'X:=', '2.034063mm', 'Y:=', '2.625000mm', 'Z:=', '0.0mm'])
segs.append(['NAME:PLSegment', 'SegmentType:=', 'Line', 'StartIndex:=', 5, 'NoOfPoints:=', 2])
pts.append(['NAME:PLPoint', 'X:=', '2.034063mm', 'Y:=', '2.835000mm', 'Z:=', '0.0mm'])
segs.append(['NAME:PLSegment', 'SegmentType:=', 'Line', 'StartIndex:=', 6, 'NoOfPoints:=', 2])
pts.append(['NAME:PLPoint', 'X:=', '2.705938mm', 'Y:=', '2.835000mm', 'Z:=', '0.0mm'])
segs.append(['NAME:PLSegment', 'SegmentType:=', 'Line', 'StartIndex:=', 7, 'NoOfPoints:=', 2])
pts.append(['NAME:PLPoint', 'X:=', '2.705938mm', 'Y:=', '3.025000mm', 'Z:=', '0.0mm'])
segs.append(['NAME:PLSegment', 'SegmentType:=', 'Line', 'StartIndex:=', 8, 'NoOfPoints:=', 2])
pts.append(['NAME:PLPoint', 'X:=', '2.034063mm', 'Y:=', '3.025000mm', 'Z:=', '0.0mm'])
segs.append(['NAME:PLSegment', 'SegmentType:=', 'Line', 'StartIndex:=', 9, 'NoOfPoints:=', 2])
pts.append(['NAME:PLPoint', 'X:=', '2.034063mm', 'Y:=', '3.235000mm', 'Z:=', '0.0mm'])
segs.append(['NAME:PLSegment', 'SegmentType:=', 'Line', 'StartIndex:=', 10, 'NoOfPoints:=', 2])
pts.append(['NAME:PLPoint', 'X:=', '2.705938mm', 'Y:=', '3.235000mm', 'Z:=', '0.0mm'])
segs.append(['NAME:PLSegment', 'SegmentType:=', 'Line', 'StartIndex:=', 11, 'NoOfPoints:=', 2])
pts.append(['NAME:PLPoint', 'X:=', '2.705938mm', 'Y:=', '3.425000mm', 'Z:=', '0.0mm'])
segs.append(['NAME:PLSegment', 'SegmentType:=', 'Line', 'StartIndex:=', 12, 'NoOfPoints:=', 2])
pts.append(['NAME:PLPoint', 'X:=', '2.034063mm', 'Y:=', '3.425000mm', 'Z:=', '0.0mm'])
segs.append(['NAME:PLSegment', 'SegmentType:=', 'Line', 'StartIndex:=', 13, 'NoOfPoints:=', 2])
pts.append(['NAME:PLPoint', 'X:=', '2.034063mm', 'Y:=', '3.635000mm', 'Z:=', '0.0mm'])
segs.append(['NAME:PLSegment', 'SegmentType:=', 'Line', 'StartIndex:=', 14, 'NoOfPoints:=', 2])
pts.append(['NAME:PLPoint', 'X:=', '2.705938mm', 'Y:=', '3.635000mm', 'Z:=', '0.0mm'])
segs.append(['NAME:PLSegment', 'SegmentType:=', 'Line', 'StartIndex:=', 15, 'NoOfPoints:=', 2])
pts.append(['NAME:PLPoint', 'X:=', '2.705938mm', 'Y:=', '3.825000mm', 'Z:=', '0.0mm'])
segs.append(['NAME:PLSegment', 'SegmentType:=', 'Line', 'StartIndex:=', 16, 'NoOfPoints:=', 2])
pts.append(['NAME:PLPoint', 'X:=', '2.495000mm', 'Y:=', '3.825000mm', 'Z:=', '0.0mm'])
segs.append(['NAME:PLSegment', 'SegmentType:=', 'Line', 'StartIndex:=', 17, 'NoOfPoints:=', 2])
pts.append(['NAME:PLPoint', 'X:=', '2.495000mm', 'Y:=', '3.975000mm', 'Z:=', '0.0mm'])
segs.append(['NAME:PLSegment', 'SegmentType:=', 'Line', 'StartIndex:=', 18, 'NoOfPoints:=', 2])
pts.append(['NAME:PLPoint', 'X:=', '2.505000mm', 'Y:=', '3.975000mm', 'Z:=', '0.0mm'])
segs.append(['NAME:PLSegment', 'SegmentType:=', 'Line', 'StartIndex:=', 19, 'NoOfPoints:=', 2])
pts.append(['NAME:PLPoint', 'X:=', '2.505000mm', 'Y:=', '3.835000mm', 'Z:=', '0.0mm'])
segs.append(['NAME:PLSegment', 'SegmentType:=', 'Line', 'StartIndex:=', 20, 'NoOfPoints:=', 2])
pts.append(['NAME:PLPoint', 'X:=', '2.715937mm', 'Y:=', '3.835000mm', 'Z:=', '0.0mm'])
segs.append(['NAME:PLSegment', 'SegmentType:=', 'Line', 'StartIndex:=', 21, 'NoOfPoints:=', 2])
pts.append(['NAME:PLPoint', 'X:=', '2.715937mm', 'Y:=', '3.625000mm', 'Z:=', '0.0mm'])
segs.append(['NAME:PLSegment', 'SegmentType:=', 'Line', 'StartIndex:=', 22, 'NoOfPoints:=', 2])
pts.append(['NAME:PLPoint', 'X:=', '2.044062mm', 'Y:=', '3.625000mm', 'Z:=', '0.0mm'])
segs.append(['NAME:PLSegment', 'SegmentType:=', 'Line', 'StartIndex:=', 23, 'NoOfPoints:=', 2])
pts.append(['NAME:PLPoint', 'X:=', '2.044062mm', 'Y:=', '3.435000mm', 'Z:=', '0.0mm'])
segs.append(['NAME:PLSegment', 'SegmentType:=', 'Line', 'StartIndex:=', 24, 'NoOfPoints:=', 2])
pts.append(['NAME:PLPoint', 'X:=', '2.715937mm', 'Y:=', '3.435000mm', 'Z:=', '0.0mm'])
segs.append(['NAME:PLSegment', 'SegmentType:=', 'Line', 'StartIndex:=', 25, 'NoOfPoints:=', 2])
pts.append(['NAME:PLPoint', 'X:=', '2.715937mm', 'Y:=', '3.225000mm', 'Z:=', '0.0mm'])
segs.append(['NAME:PLSegment', 'SegmentType:=', 'Line', 'StartIndex:=', 26, 'NoOfPoints:=', 2])
pts.append(['NAME:PLPoint', 'X:=', '2.044062mm', 'Y:=', '3.225000mm', 'Z:=', '0.0mm'])
segs.append(['NAME:PLSegment', 'SegmentType:=', 'Line', 'StartIndex:=', 27, 'NoOfPoints:=', 2])
pts.append(['NAME:PLPoint', 'X:=', '2.044062mm', 'Y:=', '3.035000mm', 'Z:=', '0.0mm'])
segs.append(['NAME:PLSegment', 'SegmentType:=', 'Line', 'StartIndex:=', 28, 'NoOfPoints:=', 2])
pts.append(['NAME:PLPoint', 'X:=', '2.715937mm', 'Y:=', '3.035000mm', 'Z:=', '0.0mm'])
segs.append(['NAME:PLSegment', 'SegmentType:=', 'Line', 'StartIndex:=', 29, 'NoOfPoints:=', 2])
pts.append(['NAME:PLPoint', 'X:=', '2.715937mm', 'Y:=', '2.825000mm', 'Z:=', '0.0mm'])
segs.append(['NAME:PLSegment', 'SegmentType:=', 'Line', 'StartIndex:=', 30, 'NoOfPoints:=', 2])
pts.append(['NAME:PLPoint', 'X:=', '2.044062mm', 'Y:=', '2.825000mm', 'Z:=', '0.0mm'])
segs.append(['NAME:PLSegment', 'SegmentType:=', 'Line', 'StartIndex:=', 31, 'NoOfPoints:=', 2])
pts.append(['NAME:PLPoint', 'X:=', '2.044062mm', 'Y:=', '2.635000mm', 'Z:=', '0.0mm'])
segs.append(['NAME:PLSegment', 'SegmentType:=', 'Line', 'StartIndex:=', 32, 'NoOfPoints:=', 2])
pts.append(['NAME:PLPoint', 'X:=', '2.715937mm', 'Y:=', '2.635000mm', 'Z:=', '0.0mm'])
segs.append(['NAME:PLSegment', 'SegmentType:=', 'Line', 'StartIndex:=', 33, 'NoOfPoints:=', 2])
pts.append(['NAME:PLPoint', 'X:=', '2.715937mm', 'Y:=', '2.425000mm', 'Z:=', '0.0mm'])
segs.append(['NAME:PLSegment', 'SegmentType:=', 'Line', 'StartIndex:=', 34, 'NoOfPoints:=', 2])
pts.append(['NAME:PLPoint', 'X:=', '2.044062mm', 'Y:=', '2.425000mm', 'Z:=', '0.0mm'])
segs.append(['NAME:PLSegment', 'SegmentType:=', 'Line', 'StartIndex:=', 35, 'NoOfPoints:=', 2])
pts.append(['NAME:PLPoint', 'X:=', '2.044062mm', 'Y:=', '2.235000mm', 'Z:=', '0.0mm'])
segs.append(['NAME:PLSegment', 'SegmentType:=', 'Line', 'StartIndex:=', 36, 'NoOfPoints:=', 2])
pts.append(['NAME:PLPoint', 'X:=', '2.380000mm', 'Y:=', '2.235000mm', 'Z:=', '0.0mm'])
segs.append(['NAME:PLSegment', 'SegmentType:=', 'Line', 'StartIndex:=', 37, 'NoOfPoints:=', 2])
pts.append(['NAME:PLPoint', 'X:=', '2.380000mm', 'Y:=', '2.225000mm', 'Z:=', '0.0mm'])
segs.append(['NAME:PLSegment', 'SegmentType:=', 'Line', 'StartIndex:=', 38, 'NoOfPoints:=', 2])
pts.append(['NAME:PLPoint', 'X:=', '2.370000mm', 'Y:=', '2.225000mm', 'Z:=', '0.0mm'])
oEditor.CreatePolyline(
    ['NAME:PolylineParameters', 'IsPolylineCovered:=', True, 'IsPolylineClosed:=', True, pts, segs],
    [
        'NAME:Attributes',
        'Name:=', 'trace_Readout_Q2_56',
        'Flags:=', '',
        'Color:=', '(200 220 255)',
        'Transparency:=', 0.0,
        'PartCoordinateSystem:=', 'Global',
        'UDMId:=', '',
        'MaterialName:=', 'vacuum',
        'SolveInside:=', True
    ]
)
# Element: cut_Readout_Q2_57
pts = ['NAME:PolylinePoints']
segs = ['NAME:PolylineSegments']
pts.append(['NAME:PLPoint', 'X:=', '2.374500mm', 'Y:=', '2.225000mm', 'Z:=', '0.0mm'])
segs.append(['NAME:PLSegment', 'SegmentType:=', 'Line', 'StartIndex:=', 0, 'NoOfPoints:=', 2])
pts.append(['NAME:PLPoint', 'X:=', '2.375000mm', 'Y:=', '2.224500mm', 'Z:=', '0.0mm'])
segs.append(['NAME:PLSegment', 'SegmentType:=', 'Line', 'StartIndex:=', 1, 'NoOfPoints:=', 2])
pts.append(['NAME:PLPoint', 'X:=', '2.375000mm', 'Y:=', '2.219000mm', 'Z:=', '0.0mm'])
segs.append(['NAME:PLSegment', 'SegmentType:=', 'Line', 'StartIndex:=', 2, 'NoOfPoints:=', 2])
pts.append(['NAME:PLPoint', 'X:=', '2.028062mm', 'Y:=', '2.219000mm', 'Z:=', '0.0mm'])
segs.append(['NAME:PLSegment', 'SegmentType:=', 'Line', 'StartIndex:=', 3, 'NoOfPoints:=', 2])
pts.append(['NAME:PLPoint', 'X:=', '2.028062mm', 'Y:=', '2.441000mm', 'Z:=', '0.0mm'])
segs.append(['NAME:PLSegment', 'SegmentType:=', 'Line', 'StartIndex:=', 4, 'NoOfPoints:=', 2])
pts.append(['NAME:PLPoint', 'X:=', '2.699937mm', 'Y:=', '2.441000mm', 'Z:=', '0.0mm'])
segs.append(['NAME:PLSegment', 'SegmentType:=', 'Line', 'StartIndex:=', 5, 'NoOfPoints:=', 2])
pts.append(['NAME:PLPoint', 'X:=', '2.699937mm', 'Y:=', '2.619000mm', 'Z:=', '0.0mm'])
segs.append(['NAME:PLSegment', 'SegmentType:=', 'Line', 'StartIndex:=', 6, 'NoOfPoints:=', 2])
pts.append(['NAME:PLPoint', 'X:=', '2.028062mm', 'Y:=', '2.619000mm', 'Z:=', '0.0mm'])
segs.append(['NAME:PLSegment', 'SegmentType:=', 'Line', 'StartIndex:=', 7, 'NoOfPoints:=', 2])
pts.append(['NAME:PLPoint', 'X:=', '2.028062mm', 'Y:=', '2.841000mm', 'Z:=', '0.0mm'])
segs.append(['NAME:PLSegment', 'SegmentType:=', 'Line', 'StartIndex:=', 8, 'NoOfPoints:=', 2])
pts.append(['NAME:PLPoint', 'X:=', '2.699937mm', 'Y:=', '2.841000mm', 'Z:=', '0.0mm'])
segs.append(['NAME:PLSegment', 'SegmentType:=', 'Line', 'StartIndex:=', 9, 'NoOfPoints:=', 2])
pts.append(['NAME:PLPoint', 'X:=', '2.699937mm', 'Y:=', '3.019000mm', 'Z:=', '0.0mm'])
segs.append(['NAME:PLSegment', 'SegmentType:=', 'Line', 'StartIndex:=', 10, 'NoOfPoints:=', 2])
pts.append(['NAME:PLPoint', 'X:=', '2.028062mm', 'Y:=', '3.019000mm', 'Z:=', '0.0mm'])
segs.append(['NAME:PLSegment', 'SegmentType:=', 'Line', 'StartIndex:=', 11, 'NoOfPoints:=', 2])
pts.append(['NAME:PLPoint', 'X:=', '2.028062mm', 'Y:=', '3.241000mm', 'Z:=', '0.0mm'])
segs.append(['NAME:PLSegment', 'SegmentType:=', 'Line', 'StartIndex:=', 12, 'NoOfPoints:=', 2])
pts.append(['NAME:PLPoint', 'X:=', '2.699937mm', 'Y:=', '3.241000mm', 'Z:=', '0.0mm'])
segs.append(['NAME:PLSegment', 'SegmentType:=', 'Line', 'StartIndex:=', 13, 'NoOfPoints:=', 2])
pts.append(['NAME:PLPoint', 'X:=', '2.699937mm', 'Y:=', '3.419000mm', 'Z:=', '0.0mm'])
segs.append(['NAME:PLSegment', 'SegmentType:=', 'Line', 'StartIndex:=', 14, 'NoOfPoints:=', 2])
pts.append(['NAME:PLPoint', 'X:=', '2.028062mm', 'Y:=', '3.419000mm', 'Z:=', '0.0mm'])
segs.append(['NAME:PLSegment', 'SegmentType:=', 'Line', 'StartIndex:=', 15, 'NoOfPoints:=', 2])
pts.append(['NAME:PLPoint', 'X:=', '2.028062mm', 'Y:=', '3.641000mm', 'Z:=', '0.0mm'])
segs.append(['NAME:PLSegment', 'SegmentType:=', 'Line', 'StartIndex:=', 16, 'NoOfPoints:=', 2])
pts.append(['NAME:PLPoint', 'X:=', '2.699937mm', 'Y:=', '3.641000mm', 'Z:=', '0.0mm'])
segs.append(['NAME:PLSegment', 'SegmentType:=', 'Line', 'StartIndex:=', 17, 'NoOfPoints:=', 2])
pts.append(['NAME:PLPoint', 'X:=', '2.699937mm', 'Y:=', '3.819000mm', 'Z:=', '0.0mm'])
segs.append(['NAME:PLSegment', 'SegmentType:=', 'Line', 'StartIndex:=', 18, 'NoOfPoints:=', 2])
pts.append(['NAME:PLPoint', 'X:=', '2.489000mm', 'Y:=', '3.819000mm', 'Z:=', '0.0mm'])
segs.append(['NAME:PLSegment', 'SegmentType:=', 'Line', 'StartIndex:=', 19, 'NoOfPoints:=', 2])
pts.append(['NAME:PLPoint', 'X:=', '2.489000mm', 'Y:=', '3.975000mm', 'Z:=', '0.0mm'])
segs.append(['NAME:PLSegment', 'SegmentType:=', 'Line', 'StartIndex:=', 20, 'NoOfPoints:=', 2])
pts.append(['NAME:PLPoint', 'X:=', '2.511000mm', 'Y:=', '3.975000mm', 'Z:=', '0.0mm'])
segs.append(['NAME:PLSegment', 'SegmentType:=', 'Line', 'StartIndex:=', 21, 'NoOfPoints:=', 2])
pts.append(['NAME:PLPoint', 'X:=', '2.511000mm', 'Y:=', '3.841000mm', 'Z:=', '0.0mm'])
segs.append(['NAME:PLSegment', 'SegmentType:=', 'Line', 'StartIndex:=', 22, 'NoOfPoints:=', 2])
pts.append(['NAME:PLPoint', 'X:=', '2.721938mm', 'Y:=', '3.841000mm', 'Z:=', '0.0mm'])
segs.append(['NAME:PLSegment', 'SegmentType:=', 'Line', 'StartIndex:=', 23, 'NoOfPoints:=', 2])
pts.append(['NAME:PLPoint', 'X:=', '2.721938mm', 'Y:=', '3.619000mm', 'Z:=', '0.0mm'])
segs.append(['NAME:PLSegment', 'SegmentType:=', 'Line', 'StartIndex:=', 24, 'NoOfPoints:=', 2])
pts.append(['NAME:PLPoint', 'X:=', '2.050063mm', 'Y:=', '3.619000mm', 'Z:=', '0.0mm'])
segs.append(['NAME:PLSegment', 'SegmentType:=', 'Line', 'StartIndex:=', 25, 'NoOfPoints:=', 2])
pts.append(['NAME:PLPoint', 'X:=', '2.050063mm', 'Y:=', '3.441000mm', 'Z:=', '0.0mm'])
segs.append(['NAME:PLSegment', 'SegmentType:=', 'Line', 'StartIndex:=', 26, 'NoOfPoints:=', 2])
pts.append(['NAME:PLPoint', 'X:=', '2.721938mm', 'Y:=', '3.441000mm', 'Z:=', '0.0mm'])
segs.append(['NAME:PLSegment', 'SegmentType:=', 'Line', 'StartIndex:=', 27, 'NoOfPoints:=', 2])
pts.append(['NAME:PLPoint', 'X:=', '2.721938mm', 'Y:=', '3.219000mm', 'Z:=', '0.0mm'])
segs.append(['NAME:PLSegment', 'SegmentType:=', 'Line', 'StartIndex:=', 28, 'NoOfPoints:=', 2])
pts.append(['NAME:PLPoint', 'X:=', '2.050063mm', 'Y:=', '3.219000mm', 'Z:=', '0.0mm'])
segs.append(['NAME:PLSegment', 'SegmentType:=', 'Line', 'StartIndex:=', 29, 'NoOfPoints:=', 2])
pts.append(['NAME:PLPoint', 'X:=', '2.050063mm', 'Y:=', '3.041000mm', 'Z:=', '0.0mm'])
segs.append(['NAME:PLSegment', 'SegmentType:=', 'Line', 'StartIndex:=', 30, 'NoOfPoints:=', 2])
pts.append(['NAME:PLPoint', 'X:=', '2.721938mm', 'Y:=', '3.041000mm', 'Z:=', '0.0mm'])
segs.append(['NAME:PLSegment', 'SegmentType:=', 'Line', 'StartIndex:=', 31, 'NoOfPoints:=', 2])
pts.append(['NAME:PLPoint', 'X:=', '2.721938mm', 'Y:=', '2.819000mm', 'Z:=', '0.0mm'])
segs.append(['NAME:PLSegment', 'SegmentType:=', 'Line', 'StartIndex:=', 32, 'NoOfPoints:=', 2])
pts.append(['NAME:PLPoint', 'X:=', '2.050063mm', 'Y:=', '2.819000mm', 'Z:=', '0.0mm'])
segs.append(['NAME:PLSegment', 'SegmentType:=', 'Line', 'StartIndex:=', 33, 'NoOfPoints:=', 2])
pts.append(['NAME:PLPoint', 'X:=', '2.050063mm', 'Y:=', '2.641000mm', 'Z:=', '0.0mm'])
segs.append(['NAME:PLSegment', 'SegmentType:=', 'Line', 'StartIndex:=', 34, 'NoOfPoints:=', 2])
pts.append(['NAME:PLPoint', 'X:=', '2.721938mm', 'Y:=', '2.641000mm', 'Z:=', '0.0mm'])
segs.append(['NAME:PLSegment', 'SegmentType:=', 'Line', 'StartIndex:=', 35, 'NoOfPoints:=', 2])
pts.append(['NAME:PLPoint', 'X:=', '2.721938mm', 'Y:=', '2.419000mm', 'Z:=', '0.0mm'])
segs.append(['NAME:PLSegment', 'SegmentType:=', 'Line', 'StartIndex:=', 36, 'NoOfPoints:=', 2])
pts.append(['NAME:PLPoint', 'X:=', '2.050063mm', 'Y:=', '2.419000mm', 'Z:=', '0.0mm'])
segs.append(['NAME:PLSegment', 'SegmentType:=', 'Line', 'StartIndex:=', 37, 'NoOfPoints:=', 2])
pts.append(['NAME:PLPoint', 'X:=', '2.050063mm', 'Y:=', '2.241000mm', 'Z:=', '0.0mm'])
segs.append(['NAME:PLSegment', 'SegmentType:=', 'Line', 'StartIndex:=', 38, 'NoOfPoints:=', 2])
pts.append(['NAME:PLPoint', 'X:=', '2.386000mm', 'Y:=', '2.241000mm', 'Z:=', '0.0mm'])
segs.append(['NAME:PLSegment', 'SegmentType:=', 'Line', 'StartIndex:=', 39, 'NoOfPoints:=', 2])
pts.append(['NAME:PLPoint', 'X:=', '2.386000mm', 'Y:=', '2.225000mm', 'Z:=', '0.0mm'])
segs.append(['NAME:PLSegment', 'SegmentType:=', 'Line', 'StartIndex:=', 40, 'NoOfPoints:=', 2])
pts.append(['NAME:PLPoint', 'X:=', '2.374500mm', 'Y:=', '2.225000mm', 'Z:=', '0.0mm'])
oEditor.CreatePolyline(
    ['NAME:PolylineParameters', 'IsPolylineCovered:=', True, 'IsPolylineClosed:=', True, pts, segs],
    [
        'NAME:Attributes',
        'Name:=', 'cut_Readout_Q2_57',
        'Flags:=', '',
        'Color:=', '(255 100 100)',
        'Transparency:=', 0.0,
        'PartCoordinateSystem:=', 'Global',
        'UDMId:=', '',
        'MaterialName:=', 'vacuum',
        'SolveInside:=', True
    ]
)
# Element: trace_Readout_Q6_58
pts = ['NAME:PolylinePoints']
segs = ['NAME:PolylineSegments']
pts.append(['NAME:PLPoint', 'X:=', '2.630000mm', 'Y:=', '-0.425000mm', 'Z:=', '0.0mm'])
segs.append(['NAME:PLSegment', 'SegmentType:=', 'Line', 'StartIndex:=', 0, 'NoOfPoints:=', 2])
pts.append(['NAME:PLPoint', 'X:=', '3.010357mm', 'Y:=', '-0.425000mm', 'Z:=', '0.0mm'])
segs.append(['NAME:PLSegment', 'SegmentType:=', 'Line', 'StartIndex:=', 1, 'NoOfPoints:=', 2])
pts.append(['NAME:PLPoint', 'X:=', '3.010357mm', 'Y:=', '-0.635000mm', 'Z:=', '0.0mm'])
segs.append(['NAME:PLSegment', 'SegmentType:=', 'Line', 'StartIndex:=', 2, 'NoOfPoints:=', 2])
pts.append(['NAME:PLPoint', 'X:=', '2.249643mm', 'Y:=', '-0.635000mm', 'Z:=', '0.0mm'])
segs.append(['NAME:PLSegment', 'SegmentType:=', 'Line', 'StartIndex:=', 3, 'NoOfPoints:=', 2])
pts.append(['NAME:PLPoint', 'X:=', '2.249643mm', 'Y:=', '-0.825000mm', 'Z:=', '0.0mm'])
segs.append(['NAME:PLSegment', 'SegmentType:=', 'Line', 'StartIndex:=', 4, 'NoOfPoints:=', 2])
pts.append(['NAME:PLPoint', 'X:=', '3.010357mm', 'Y:=', '-0.825000mm', 'Z:=', '0.0mm'])
segs.append(['NAME:PLSegment', 'SegmentType:=', 'Line', 'StartIndex:=', 5, 'NoOfPoints:=', 2])
pts.append(['NAME:PLPoint', 'X:=', '3.010357mm', 'Y:=', '-1.035000mm', 'Z:=', '0.0mm'])
segs.append(['NAME:PLSegment', 'SegmentType:=', 'Line', 'StartIndex:=', 6, 'NoOfPoints:=', 2])
pts.append(['NAME:PLPoint', 'X:=', '2.249643mm', 'Y:=', '-1.035000mm', 'Z:=', '0.0mm'])
segs.append(['NAME:PLSegment', 'SegmentType:=', 'Line', 'StartIndex:=', 7, 'NoOfPoints:=', 2])
pts.append(['NAME:PLPoint', 'X:=', '2.249643mm', 'Y:=', '-1.225000mm', 'Z:=', '0.0mm'])
segs.append(['NAME:PLSegment', 'SegmentType:=', 'Line', 'StartIndex:=', 8, 'NoOfPoints:=', 2])
pts.append(['NAME:PLPoint', 'X:=', '3.010357mm', 'Y:=', '-1.225000mm', 'Z:=', '0.0mm'])
segs.append(['NAME:PLSegment', 'SegmentType:=', 'Line', 'StartIndex:=', 9, 'NoOfPoints:=', 2])
pts.append(['NAME:PLPoint', 'X:=', '3.010357mm', 'Y:=', '-1.435000mm', 'Z:=', '0.0mm'])
segs.append(['NAME:PLSegment', 'SegmentType:=', 'Line', 'StartIndex:=', 10, 'NoOfPoints:=', 2])
pts.append(['NAME:PLPoint', 'X:=', '2.249643mm', 'Y:=', '-1.435000mm', 'Z:=', '0.0mm'])
segs.append(['NAME:PLSegment', 'SegmentType:=', 'Line', 'StartIndex:=', 11, 'NoOfPoints:=', 2])
pts.append(['NAME:PLPoint', 'X:=', '2.249643mm', 'Y:=', '-1.625000mm', 'Z:=', '0.0mm'])
segs.append(['NAME:PLSegment', 'SegmentType:=', 'Line', 'StartIndex:=', 12, 'NoOfPoints:=', 2])
pts.append(['NAME:PLPoint', 'X:=', '3.010357mm', 'Y:=', '-1.625000mm', 'Z:=', '0.0mm'])
segs.append(['NAME:PLSegment', 'SegmentType:=', 'Line', 'StartIndex:=', 13, 'NoOfPoints:=', 2])
pts.append(['NAME:PLPoint', 'X:=', '3.010357mm', 'Y:=', '-1.835000mm', 'Z:=', '0.0mm'])
segs.append(['NAME:PLSegment', 'SegmentType:=', 'Line', 'StartIndex:=', 14, 'NoOfPoints:=', 2])
pts.append(['NAME:PLPoint', 'X:=', '2.505000mm', 'Y:=', '-1.835000mm', 'Z:=', '0.0mm'])
segs.append(['NAME:PLSegment', 'SegmentType:=', 'Line', 'StartIndex:=', 15, 'NoOfPoints:=', 2])
pts.append(['NAME:PLPoint', 'X:=', '2.505000mm', 'Y:=', '-1.975000mm', 'Z:=', '0.0mm'])
segs.append(['NAME:PLSegment', 'SegmentType:=', 'Line', 'StartIndex:=', 16, 'NoOfPoints:=', 2])
pts.append(['NAME:PLPoint', 'X:=', '2.495000mm', 'Y:=', '-1.975000mm', 'Z:=', '0.0mm'])
segs.append(['NAME:PLSegment', 'SegmentType:=', 'Line', 'StartIndex:=', 17, 'NoOfPoints:=', 2])
pts.append(['NAME:PLPoint', 'X:=', '2.495000mm', 'Y:=', '-1.825000mm', 'Z:=', '0.0mm'])
segs.append(['NAME:PLSegment', 'SegmentType:=', 'Line', 'StartIndex:=', 18, 'NoOfPoints:=', 2])
pts.append(['NAME:PLPoint', 'X:=', '3.000357mm', 'Y:=', '-1.825000mm', 'Z:=', '0.0mm'])
segs.append(['NAME:PLSegment', 'SegmentType:=', 'Line', 'StartIndex:=', 19, 'NoOfPoints:=', 2])
pts.append(['NAME:PLPoint', 'X:=', '3.000357mm', 'Y:=', '-1.635000mm', 'Z:=', '0.0mm'])
segs.append(['NAME:PLSegment', 'SegmentType:=', 'Line', 'StartIndex:=', 20, 'NoOfPoints:=', 2])
pts.append(['NAME:PLPoint', 'X:=', '2.239643mm', 'Y:=', '-1.635000mm', 'Z:=', '0.0mm'])
segs.append(['NAME:PLSegment', 'SegmentType:=', 'Line', 'StartIndex:=', 21, 'NoOfPoints:=', 2])
pts.append(['NAME:PLPoint', 'X:=', '2.239643mm', 'Y:=', '-1.425000mm', 'Z:=', '0.0mm'])
segs.append(['NAME:PLSegment', 'SegmentType:=', 'Line', 'StartIndex:=', 22, 'NoOfPoints:=', 2])
pts.append(['NAME:PLPoint', 'X:=', '3.000357mm', 'Y:=', '-1.425000mm', 'Z:=', '0.0mm'])
segs.append(['NAME:PLSegment', 'SegmentType:=', 'Line', 'StartIndex:=', 23, 'NoOfPoints:=', 2])
pts.append(['NAME:PLPoint', 'X:=', '3.000357mm', 'Y:=', '-1.235000mm', 'Z:=', '0.0mm'])
segs.append(['NAME:PLSegment', 'SegmentType:=', 'Line', 'StartIndex:=', 24, 'NoOfPoints:=', 2])
pts.append(['NAME:PLPoint', 'X:=', '2.239643mm', 'Y:=', '-1.235000mm', 'Z:=', '0.0mm'])
segs.append(['NAME:PLSegment', 'SegmentType:=', 'Line', 'StartIndex:=', 25, 'NoOfPoints:=', 2])
pts.append(['NAME:PLPoint', 'X:=', '2.239643mm', 'Y:=', '-1.025000mm', 'Z:=', '0.0mm'])
segs.append(['NAME:PLSegment', 'SegmentType:=', 'Line', 'StartIndex:=', 26, 'NoOfPoints:=', 2])
pts.append(['NAME:PLPoint', 'X:=', '3.000357mm', 'Y:=', '-1.025000mm', 'Z:=', '0.0mm'])
segs.append(['NAME:PLSegment', 'SegmentType:=', 'Line', 'StartIndex:=', 27, 'NoOfPoints:=', 2])
pts.append(['NAME:PLPoint', 'X:=', '3.000357mm', 'Y:=', '-0.835000mm', 'Z:=', '0.0mm'])
segs.append(['NAME:PLSegment', 'SegmentType:=', 'Line', 'StartIndex:=', 28, 'NoOfPoints:=', 2])
pts.append(['NAME:PLPoint', 'X:=', '2.239643mm', 'Y:=', '-0.835000mm', 'Z:=', '0.0mm'])
segs.append(['NAME:PLSegment', 'SegmentType:=', 'Line', 'StartIndex:=', 29, 'NoOfPoints:=', 2])
pts.append(['NAME:PLPoint', 'X:=', '2.239643mm', 'Y:=', '-0.625000mm', 'Z:=', '0.0mm'])
segs.append(['NAME:PLSegment', 'SegmentType:=', 'Line', 'StartIndex:=', 30, 'NoOfPoints:=', 2])
pts.append(['NAME:PLPoint', 'X:=', '3.000357mm', 'Y:=', '-0.625000mm', 'Z:=', '0.0mm'])
segs.append(['NAME:PLSegment', 'SegmentType:=', 'Line', 'StartIndex:=', 31, 'NoOfPoints:=', 2])
pts.append(['NAME:PLPoint', 'X:=', '3.000357mm', 'Y:=', '-0.435000mm', 'Z:=', '0.0mm'])
segs.append(['NAME:PLSegment', 'SegmentType:=', 'Line', 'StartIndex:=', 32, 'NoOfPoints:=', 2])
pts.append(['NAME:PLPoint', 'X:=', '2.620000mm', 'Y:=', '-0.435000mm', 'Z:=', '0.0mm'])
segs.append(['NAME:PLSegment', 'SegmentType:=', 'Line', 'StartIndex:=', 33, 'NoOfPoints:=', 2])
pts.append(['NAME:PLPoint', 'X:=', '2.620000mm', 'Y:=', '-0.425000mm', 'Z:=', '0.0mm'])
segs.append(['NAME:PLSegment', 'SegmentType:=', 'Line', 'StartIndex:=', 34, 'NoOfPoints:=', 2])
pts.append(['NAME:PLPoint', 'X:=', '2.630000mm', 'Y:=', '-0.425000mm', 'Z:=', '0.0mm'])
oEditor.CreatePolyline(
    ['NAME:PolylineParameters', 'IsPolylineCovered:=', True, 'IsPolylineClosed:=', True, pts, segs],
    [
        'NAME:Attributes',
        'Name:=', 'trace_Readout_Q6_58',
        'Flags:=', '',
        'Color:=', '(200 220 255)',
        'Transparency:=', 0.0,
        'PartCoordinateSystem:=', 'Global',
        'UDMId:=', '',
        'MaterialName:=', 'vacuum',
        'SolveInside:=', True
    ]
)
# Element: cut_Readout_Q6_59
pts = ['NAME:PolylinePoints']
segs = ['NAME:PolylineSegments']
pts.append(['NAME:PLPoint', 'X:=', '2.625500mm', 'Y:=', '-0.425000mm', 'Z:=', '0.0mm'])
segs.append(['NAME:PLSegment', 'SegmentType:=', 'Line', 'StartIndex:=', 0, 'NoOfPoints:=', 2])
pts.append(['NAME:PLPoint', 'X:=', '2.625000mm', 'Y:=', '-0.424500mm', 'Z:=', '0.0mm'])
segs.append(['NAME:PLSegment', 'SegmentType:=', 'Line', 'StartIndex:=', 1, 'NoOfPoints:=', 2])
pts.append(['NAME:PLPoint', 'X:=', '2.625000mm', 'Y:=', '-0.419000mm', 'Z:=', '0.0mm'])
segs.append(['NAME:PLSegment', 'SegmentType:=', 'Line', 'StartIndex:=', 2, 'NoOfPoints:=', 2])
pts.append(['NAME:PLPoint', 'X:=', '3.016357mm', 'Y:=', '-0.419000mm', 'Z:=', '0.0mm'])
segs.append(['NAME:PLSegment', 'SegmentType:=', 'Line', 'StartIndex:=', 3, 'NoOfPoints:=', 2])
pts.append(['NAME:PLPoint', 'X:=', '3.016357mm', 'Y:=', '-0.641000mm', 'Z:=', '0.0mm'])
segs.append(['NAME:PLSegment', 'SegmentType:=', 'Line', 'StartIndex:=', 4, 'NoOfPoints:=', 2])
pts.append(['NAME:PLPoint', 'X:=', '2.255643mm', 'Y:=', '-0.641000mm', 'Z:=', '0.0mm'])
segs.append(['NAME:PLSegment', 'SegmentType:=', 'Line', 'StartIndex:=', 5, 'NoOfPoints:=', 2])
pts.append(['NAME:PLPoint', 'X:=', '2.255643mm', 'Y:=', '-0.819000mm', 'Z:=', '0.0mm'])
segs.append(['NAME:PLSegment', 'SegmentType:=', 'Line', 'StartIndex:=', 6, 'NoOfPoints:=', 2])
pts.append(['NAME:PLPoint', 'X:=', '3.016357mm', 'Y:=', '-0.819000mm', 'Z:=', '0.0mm'])
segs.append(['NAME:PLSegment', 'SegmentType:=', 'Line', 'StartIndex:=', 7, 'NoOfPoints:=', 2])
pts.append(['NAME:PLPoint', 'X:=', '3.016357mm', 'Y:=', '-1.041000mm', 'Z:=', '0.0mm'])
segs.append(['NAME:PLSegment', 'SegmentType:=', 'Line', 'StartIndex:=', 8, 'NoOfPoints:=', 2])
pts.append(['NAME:PLPoint', 'X:=', '2.255643mm', 'Y:=', '-1.041000mm', 'Z:=', '0.0mm'])
segs.append(['NAME:PLSegment', 'SegmentType:=', 'Line', 'StartIndex:=', 9, 'NoOfPoints:=', 2])
pts.append(['NAME:PLPoint', 'X:=', '2.255643mm', 'Y:=', '-1.219000mm', 'Z:=', '0.0mm'])
segs.append(['NAME:PLSegment', 'SegmentType:=', 'Line', 'StartIndex:=', 10, 'NoOfPoints:=', 2])
pts.append(['NAME:PLPoint', 'X:=', '3.016357mm', 'Y:=', '-1.219000mm', 'Z:=', '0.0mm'])
segs.append(['NAME:PLSegment', 'SegmentType:=', 'Line', 'StartIndex:=', 11, 'NoOfPoints:=', 2])
pts.append(['NAME:PLPoint', 'X:=', '3.016357mm', 'Y:=', '-1.441000mm', 'Z:=', '0.0mm'])
segs.append(['NAME:PLSegment', 'SegmentType:=', 'Line', 'StartIndex:=', 12, 'NoOfPoints:=', 2])
pts.append(['NAME:PLPoint', 'X:=', '2.255643mm', 'Y:=', '-1.441000mm', 'Z:=', '0.0mm'])
segs.append(['NAME:PLSegment', 'SegmentType:=', 'Line', 'StartIndex:=', 13, 'NoOfPoints:=', 2])
pts.append(['NAME:PLPoint', 'X:=', '2.255643mm', 'Y:=', '-1.619000mm', 'Z:=', '0.0mm'])
segs.append(['NAME:PLSegment', 'SegmentType:=', 'Line', 'StartIndex:=', 14, 'NoOfPoints:=', 2])
pts.append(['NAME:PLPoint', 'X:=', '3.016357mm', 'Y:=', '-1.619000mm', 'Z:=', '0.0mm'])
segs.append(['NAME:PLSegment', 'SegmentType:=', 'Line', 'StartIndex:=', 15, 'NoOfPoints:=', 2])
pts.append(['NAME:PLPoint', 'X:=', '3.016357mm', 'Y:=', '-1.841000mm', 'Z:=', '0.0mm'])
segs.append(['NAME:PLSegment', 'SegmentType:=', 'Line', 'StartIndex:=', 16, 'NoOfPoints:=', 2])
pts.append(['NAME:PLPoint', 'X:=', '2.511000mm', 'Y:=', '-1.841000mm', 'Z:=', '0.0mm'])
segs.append(['NAME:PLSegment', 'SegmentType:=', 'Line', 'StartIndex:=', 17, 'NoOfPoints:=', 2])
pts.append(['NAME:PLPoint', 'X:=', '2.511000mm', 'Y:=', '-1.975000mm', 'Z:=', '0.0mm'])
segs.append(['NAME:PLSegment', 'SegmentType:=', 'Line', 'StartIndex:=', 18, 'NoOfPoints:=', 2])
pts.append(['NAME:PLPoint', 'X:=', '2.489000mm', 'Y:=', '-1.975000mm', 'Z:=', '0.0mm'])
segs.append(['NAME:PLSegment', 'SegmentType:=', 'Line', 'StartIndex:=', 19, 'NoOfPoints:=', 2])
pts.append(['NAME:PLPoint', 'X:=', '2.489000mm', 'Y:=', '-1.819000mm', 'Z:=', '0.0mm'])
segs.append(['NAME:PLSegment', 'SegmentType:=', 'Line', 'StartIndex:=', 20, 'NoOfPoints:=', 2])
pts.append(['NAME:PLPoint', 'X:=', '2.994357mm', 'Y:=', '-1.819000mm', 'Z:=', '0.0mm'])
segs.append(['NAME:PLSegment', 'SegmentType:=', 'Line', 'StartIndex:=', 21, 'NoOfPoints:=', 2])
pts.append(['NAME:PLPoint', 'X:=', '2.994357mm', 'Y:=', '-1.641000mm', 'Z:=', '0.0mm'])
segs.append(['NAME:PLSegment', 'SegmentType:=', 'Line', 'StartIndex:=', 22, 'NoOfPoints:=', 2])
pts.append(['NAME:PLPoint', 'X:=', '2.233643mm', 'Y:=', '-1.641000mm', 'Z:=', '0.0mm'])
segs.append(['NAME:PLSegment', 'SegmentType:=', 'Line', 'StartIndex:=', 23, 'NoOfPoints:=', 2])
pts.append(['NAME:PLPoint', 'X:=', '2.233643mm', 'Y:=', '-1.419000mm', 'Z:=', '0.0mm'])
segs.append(['NAME:PLSegment', 'SegmentType:=', 'Line', 'StartIndex:=', 24, 'NoOfPoints:=', 2])
pts.append(['NAME:PLPoint', 'X:=', '2.994357mm', 'Y:=', '-1.419000mm', 'Z:=', '0.0mm'])
segs.append(['NAME:PLSegment', 'SegmentType:=', 'Line', 'StartIndex:=', 25, 'NoOfPoints:=', 2])
pts.append(['NAME:PLPoint', 'X:=', '2.994357mm', 'Y:=', '-1.241000mm', 'Z:=', '0.0mm'])
segs.append(['NAME:PLSegment', 'SegmentType:=', 'Line', 'StartIndex:=', 26, 'NoOfPoints:=', 2])
pts.append(['NAME:PLPoint', 'X:=', '2.233643mm', 'Y:=', '-1.241000mm', 'Z:=', '0.0mm'])
segs.append(['NAME:PLSegment', 'SegmentType:=', 'Line', 'StartIndex:=', 27, 'NoOfPoints:=', 2])
pts.append(['NAME:PLPoint', 'X:=', '2.233643mm', 'Y:=', '-1.019000mm', 'Z:=', '0.0mm'])
segs.append(['NAME:PLSegment', 'SegmentType:=', 'Line', 'StartIndex:=', 28, 'NoOfPoints:=', 2])
pts.append(['NAME:PLPoint', 'X:=', '2.994357mm', 'Y:=', '-1.019000mm', 'Z:=', '0.0mm'])
segs.append(['NAME:PLSegment', 'SegmentType:=', 'Line', 'StartIndex:=', 29, 'NoOfPoints:=', 2])
pts.append(['NAME:PLPoint', 'X:=', '2.994357mm', 'Y:=', '-0.841000mm', 'Z:=', '0.0mm'])
segs.append(['NAME:PLSegment', 'SegmentType:=', 'Line', 'StartIndex:=', 30, 'NoOfPoints:=', 2])
pts.append(['NAME:PLPoint', 'X:=', '2.233643mm', 'Y:=', '-0.841000mm', 'Z:=', '0.0mm'])
segs.append(['NAME:PLSegment', 'SegmentType:=', 'Line', 'StartIndex:=', 31, 'NoOfPoints:=', 2])
pts.append(['NAME:PLPoint', 'X:=', '2.233643mm', 'Y:=', '-0.619000mm', 'Z:=', '0.0mm'])
segs.append(['NAME:PLSegment', 'SegmentType:=', 'Line', 'StartIndex:=', 32, 'NoOfPoints:=', 2])
pts.append(['NAME:PLPoint', 'X:=', '2.994357mm', 'Y:=', '-0.619000mm', 'Z:=', '0.0mm'])
segs.append(['NAME:PLSegment', 'SegmentType:=', 'Line', 'StartIndex:=', 33, 'NoOfPoints:=', 2])
pts.append(['NAME:PLPoint', 'X:=', '2.994357mm', 'Y:=', '-0.441000mm', 'Z:=', '0.0mm'])
segs.append(['NAME:PLSegment', 'SegmentType:=', 'Line', 'StartIndex:=', 34, 'NoOfPoints:=', 2])
pts.append(['NAME:PLPoint', 'X:=', '2.614000mm', 'Y:=', '-0.441000mm', 'Z:=', '0.0mm'])
segs.append(['NAME:PLSegment', 'SegmentType:=', 'Line', 'StartIndex:=', 35, 'NoOfPoints:=', 2])
pts.append(['NAME:PLPoint', 'X:=', '2.614000mm', 'Y:=', '-0.425000mm', 'Z:=', '0.0mm'])
segs.append(['NAME:PLSegment', 'SegmentType:=', 'Line', 'StartIndex:=', 36, 'NoOfPoints:=', 2])
pts.append(['NAME:PLPoint', 'X:=', '2.625500mm', 'Y:=', '-0.425000mm', 'Z:=', '0.0mm'])
oEditor.CreatePolyline(
    ['NAME:PolylineParameters', 'IsPolylineCovered:=', True, 'IsPolylineClosed:=', True, pts, segs],
    [
        'NAME:Attributes',
        'Name:=', 'cut_Readout_Q6_59',
        'Flags:=', '',
        'Color:=', '(255 100 100)',
        'Transparency:=', 0.0,
        'PartCoordinateSystem:=', 'Global',
        'UDMId:=', '',
        'MaterialName:=', 'vacuum',
        'SolveInside:=', True
    ]
)

# --- 5. Subtract All Pockets & CPW Slots from Ground Plane ---
cut_list = ['rect_pk_Q4_2', 'cl_etcher_Q4_6', 'rect_pk_Q0_9', 'rect_pk_Q1_14', 'rect_pk_Q3_20', 'rect_pk_Q5_26', 'rect_pk_Q2_32', 'rect_pk_Q6_38', 'pocket_LP_Q1_42', 'pocket_LP_Q3_44', 'pocket_LP_Q5_46', 'pocket_LP_Q2_48', 'pocket_LP_Q0_50', 'pocket_LP_Q6_52', 'bus_left_wire_sub_Q4_1', 'bus_right_wire_sub_Q4_3', 'bus_top_wire_sub_Q0_5', 'readout_wire_sub_Q0_7', 'bus_bot_wire_sub_Q1_9', 'bus_right_wire_sub_Q1_11', 'readout_wire_sub_Q1_13', 'bus_left_wire_sub_Q3_15', 'bus_right_wire_sub_Q3_17', 'readout_wire_sub_Q3_19', 'bus_left_wire_sub_Q5_21', 'bus_right_wire_sub_Q5_23', 'readout_wire_sub_Q5_25', 'bus_bot_wire_sub_Q2_27', 'bus_left_wire_sub_Q2_29', 'readout_wire_sub_Q2_31', 'bus_top_wire_sub_Q6_33', 'readout_wire_sub_Q6_35', 'cut_Bus_Q0_Q1_37', 'cut_Bus_Q1_Q3_39', 'cut_Bus_Q3_Q4_41', 'cut_Bus_Q4_Q5_43', 'cut_Bus_Q5_Q2_45', 'cut_Bus_Q2_Q6_47', 'cut_Readout_Q0_49', 'cut_Readout_Q1_51', 'cut_Readout_Q3_53', 'cut_Readout_Q5_55', 'cut_Readout_Q2_57', 'cut_Readout_Q6_59']
oEditor.Subtract(
    [
        'NAME:Selections',
        'Blank Parts:=', 'ground_main_plane',
        'Tool Parts:=', ','.join(cut_list)
    ],
    [
        'NAME:SubtractParameters',
        'KeepOriginals:=', False
    ]
)

# --- 6. Assign Perfect E to Ground Plane & Metal Traces/Pads ---
metal_list = ['ground_main_plane'] + ['pad_top_Q4_0', 'pad_bot_Q4_1', 'bus_left_connector_pad_Q4_3', 'bus_right_connector_pad_Q4_4', 'cl_metal_Q4_5', 'pad_top_Q0_7', 'pad_bot_Q0_8', 'bus_top_connector_pad_Q0_10', 'readout_connector_pad_Q0_11', 'pad_top_Q1_12', 'pad_bot_Q1_13', 'bus_bot_connector_pad_Q1_15', 'bus_right_connector_pad_Q1_16', 'readout_connector_pad_Q1_17', 'pad_top_Q3_18', 'pad_bot_Q3_19', 'bus_left_connector_pad_Q3_21', 'bus_right_connector_pad_Q3_22', 'readout_connector_pad_Q3_23', 'pad_top_Q5_24', 'pad_bot_Q5_25', 'bus_left_connector_pad_Q5_27', 'bus_right_connector_pad_Q5_28', 'readout_connector_pad_Q5_29', 'pad_top_Q2_30', 'pad_bot_Q2_31', 'bus_bot_connector_pad_Q2_33', 'bus_left_connector_pad_Q2_34', 'readout_connector_pad_Q2_35', 'pad_top_Q6_36', 'pad_bot_Q6_37', 'bus_top_connector_pad_Q6_39', 'readout_connector_pad_Q6_40', 'launch_pad_LP_Q1_41', 'launch_pad_LP_Q3_43', 'launch_pad_LP_Q5_45', 'launch_pad_LP_Q2_47', 'launch_pad_LP_Q0_49', 'launch_pad_LP_Q6_51', 'bus_left_wire_Q4_0', 'bus_right_wire_Q4_2', 'bus_top_wire_Q0_4', 'readout_wire_Q0_6', 'bus_bot_wire_Q1_8', 'bus_right_wire_Q1_10', 'readout_wire_Q1_12', 'bus_left_wire_Q3_14', 'bus_right_wire_Q3_16', 'readout_wire_Q3_18', 'bus_left_wire_Q5_20', 'bus_right_wire_Q5_22', 'readout_wire_Q5_24', 'bus_bot_wire_Q2_26', 'bus_left_wire_Q2_28', 'readout_wire_Q2_30', 'bus_top_wire_Q6_32', 'readout_wire_Q6_34', 'trace_Bus_Q0_Q1_36', 'trace_Bus_Q1_Q3_38', 'trace_Bus_Q3_Q4_40', 'trace_Bus_Q4_Q5_42', 'trace_Bus_Q5_Q2_44', 'trace_Bus_Q2_Q6_46', 'trace_Readout_Q0_48', 'trace_Readout_Q1_50', 'trace_Readout_Q3_52', 'trace_Readout_Q5_54', 'trace_Readout_Q2_56', 'trace_Readout_Q6_58']
oBoundarySetup.AssignPerfectE(
    [
        'NAME:PerfE_Superconductors',
        'Objects:=', metal_list,
        'InfGroundPlane:=', False
    ]
)

# --- 7. Josephson Junction Sheet & Lumped RLC Boundary (Simon's exact 57:45 setup) ---
oEditor.CreateRectangle(
    [
        'NAME:RectangleParameters',
        'IsCovered:=', True,
        'XStart:=', '-0.015mm',
        'YStart:=', '0.855mm',
        'ZStart:=', '0.0mm',
        'Width:=', '0.03mm',
        'Height:=', '0.03mm',
        'WhichAxis:=', 'Z'
    ],
    [
        'NAME:Attributes',
        'Name:=', 'JJ_Q4_sheet',
        'Flags:=', '',
        'Color:=', '(255 0 0)',
        'Transparency:=', 0.2,
        'PartCoordinateSystem:=', 'Global',
        'UDMId:=', '',
        'MaterialName:=', 'vacuum',
        'SolveInside:=', True
    ]
)
try:
    oBoundarySetup.AssignLumpedRLC(
        [
            'NAME:Q4_Josephson_Junction',
            'Objects:=', ['JJ_Q4_sheet'],
            'CurrentLine:=', [
                'NAME:CurrentLine',
                'Start:=', ['0.0mm', '0.855mm', '0.0mm'],
                'End:=', ['0.0mm', '0.885mm', '0.0mm']
            ],
            'UseResist:=', False,
            'UseInduct:=', True,
            'Inductance:=', '12.31nH',
            'UseCap:=', True,
            'Capacitance:=', '2.0fF'
        ]
    )
    print('[+] Assigned Q4 Lumped RLC boundary!')
except Exception as rlc_err:
    print('[*] Note on Lumped RLC assignment: ' + str(rlc_err))

# --- 8. Fit All Geometry in 3D Modeler View ---
oEditor.FitAll()
print('[SUCCESS] Simon 7-Qubit Quantum Processor fully generated in Ansys HFSS!')