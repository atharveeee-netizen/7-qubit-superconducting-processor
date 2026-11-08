# =====================================================================
# Ansys HFSS Standalone Python Script - Simon's Exact Video Chip (Part 1, 57:45)
# Canvas: 9mm x 7mm (center [0, 1mm])
# Components: Q1-Q7 (3-1-3 grid), Lt1-Lt4, RM1, RS1-RS3, LP1-LP7
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

design_name = 'Simon_Exact_Video_Chip'
design_names = []
try:
    for d in oProject.GetDesigns():
        try:
            design_names.append(d.GetName())
        except Exception:
            pass
except Exception:
    pass

if design_name in design_names:
    try:
        oProject.SetActiveDesign(design_name)
    except Exception:
        pass
    try:
        oDesign = oProject.GetDesign(design_name)
    except Exception:
        oDesign = oProject.GetActiveDesign()
else:
    oDesign = oProject.InsertDesign('HFSS', design_name, 'DrivenModal', '')

if oDesign is None:
    oDesign = oProject.GetActiveDesign()

oEditor = oDesign.SetActiveEditor('3D Modeler')
oBoundarySetup = oDesign.GetModule('BoundarySetup')

# --- Clean Any Old Boundaries (Clean Slate) ---
try:
    old_bounds = list(oBoundarySetup.GetBoundaries())
    for b in old_bounds:
        try:
            oBoundarySetup.DeleteBoundaries([b])
        except Exception:
            pass
except Exception:
    pass

# --- Clean Any Old Objects for 100% Fresh Rebuild ---
try:
    objs_to_del = []
    try:
        objs_to_del = list(oEditor.GetMatchedObjectName('*'))
    except Exception:
        pass
    if not objs_to_del:
        try:
            objs_to_del = list(oEditor.GetObjectsInGroup('All Objects'))
        except Exception:
            pass
    if objs_to_del:
        oEditor.Delete(['NAME:Selections', 'Selections:=', ','.join(objs_to_del)])
except Exception:
    pass

# --- 1. Silicon Substrate Box (9mm x 7mm, center [0, 1mm]) ---
oEditor.CreateBox(
    [
        'NAME:BoxParameters',
        'XPosition:=', '-4.5mm',
        'YPosition:=', '-2.5mm',
        'ZPosition:=', '-0.5mm',
        'XSize:=', '9.0mm',
        'YSize:=', '7.0mm',
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
        'XStart:=', '-4.5mm',
        'YStart:=', '-2.5mm',
        'ZStart:=', '0.0mm',
        'Width:=', '9.0mm',
        'Height:=', '7.0mm',
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
# Element: pad_top_Q1_0
pts = ['NAME:PolylinePoints']
segs = ['NAME:PolylineSegments']
pts.append(['NAME:PLPoint', 'X:=', '-2.515000mm', 'Y:=', '1.772500mm', 'Z:=', '0.0mm'])
segs.append(['NAME:PLSegment', 'SegmentType:=', 'Line', 'StartIndex:=', 0, 'NoOfPoints:=', 2])
pts.append(['NAME:PLPoint', 'X:=', '-2.515000mm', 'Y:=', '2.227500mm', 'Z:=', '0.0mm'])
segs.append(['NAME:PLSegment', 'SegmentType:=', 'Line', 'StartIndex:=', 1, 'NoOfPoints:=', 2])
pts.append(['NAME:PLPoint', 'X:=', '-2.605000mm', 'Y:=', '2.227500mm', 'Z:=', '0.0mm'])
segs.append(['NAME:PLSegment', 'SegmentType:=', 'Line', 'StartIndex:=', 2, 'NoOfPoints:=', 2])
pts.append(['NAME:PLPoint', 'X:=', '-2.605000mm', 'Y:=', '1.772500mm', 'Z:=', '0.0mm'])
segs.append(['NAME:PLSegment', 'SegmentType:=', 'Line', 'StartIndex:=', 3, 'NoOfPoints:=', 2])
pts.append(['NAME:PLPoint', 'X:=', '-2.515000mm', 'Y:=', '1.772500mm', 'Z:=', '0.0mm'])
oEditor.CreatePolyline(
    ['NAME:PolylineParameters', 'IsPolylineCovered:=', True, 'IsPolylineClosed:=', True, pts, segs],
    [
        'NAME:Attributes',
        'Name:=', 'pad_top_Q1_0',
        'Flags:=', '',
        'Color:=', '(200 220 255)',
        'Transparency:=', 0.0,
        'PartCoordinateSystem:=', 'Global',
        'UDMId:=', '',
        'MaterialName:=', 'vacuum',
        'SolveInside:=', True
    ]
)
# Element: pad_bot_Q1_1
pts = ['NAME:PolylinePoints']
segs = ['NAME:PolylineSegments']
pts.append(['NAME:PLPoint', 'X:=', '-2.395000mm', 'Y:=', '1.772500mm', 'Z:=', '0.0mm'])
segs.append(['NAME:PLSegment', 'SegmentType:=', 'Line', 'StartIndex:=', 0, 'NoOfPoints:=', 2])
pts.append(['NAME:PLPoint', 'X:=', '-2.395000mm', 'Y:=', '2.227500mm', 'Z:=', '0.0mm'])
segs.append(['NAME:PLSegment', 'SegmentType:=', 'Line', 'StartIndex:=', 1, 'NoOfPoints:=', 2])
pts.append(['NAME:PLPoint', 'X:=', '-2.485000mm', 'Y:=', '2.227500mm', 'Z:=', '0.0mm'])
segs.append(['NAME:PLSegment', 'SegmentType:=', 'Line', 'StartIndex:=', 2, 'NoOfPoints:=', 2])
pts.append(['NAME:PLPoint', 'X:=', '-2.485000mm', 'Y:=', '1.772500mm', 'Z:=', '0.0mm'])
segs.append(['NAME:PLSegment', 'SegmentType:=', 'Line', 'StartIndex:=', 3, 'NoOfPoints:=', 2])
pts.append(['NAME:PLPoint', 'X:=', '-2.395000mm', 'Y:=', '1.772500mm', 'Z:=', '0.0mm'])
oEditor.CreatePolyline(
    ['NAME:PolylineParameters', 'IsPolylineCovered:=', True, 'IsPolylineClosed:=', True, pts, segs],
    [
        'NAME:Attributes',
        'Name:=', 'pad_bot_Q1_1',
        'Flags:=', '',
        'Color:=', '(200 220 255)',
        'Transparency:=', 0.0,
        'PartCoordinateSystem:=', 'Global',
        'UDMId:=', '',
        'MaterialName:=', 'vacuum',
        'SolveInside:=', True
    ]
)
# Element: rect_pk_Q1_2
pts = ['NAME:PolylinePoints']
segs = ['NAME:PolylineSegments']
pts.append(['NAME:PLPoint', 'X:=', '-2.175000mm', 'Y:=', '1.675000mm', 'Z:=', '0.0mm'])
segs.append(['NAME:PLSegment', 'SegmentType:=', 'Line', 'StartIndex:=', 0, 'NoOfPoints:=', 2])
pts.append(['NAME:PLPoint', 'X:=', '-2.175000mm', 'Y:=', '2.325000mm', 'Z:=', '0.0mm'])
segs.append(['NAME:PLSegment', 'SegmentType:=', 'Line', 'StartIndex:=', 1, 'NoOfPoints:=', 2])
pts.append(['NAME:PLPoint', 'X:=', '-2.825000mm', 'Y:=', '2.325000mm', 'Z:=', '0.0mm'])
segs.append(['NAME:PLSegment', 'SegmentType:=', 'Line', 'StartIndex:=', 2, 'NoOfPoints:=', 2])
pts.append(['NAME:PLPoint', 'X:=', '-2.825000mm', 'Y:=', '1.675000mm', 'Z:=', '0.0mm'])
segs.append(['NAME:PLSegment', 'SegmentType:=', 'Line', 'StartIndex:=', 3, 'NoOfPoints:=', 2])
pts.append(['NAME:PLPoint', 'X:=', '-2.175000mm', 'Y:=', '1.675000mm', 'Z:=', '0.0mm'])
oEditor.CreatePolyline(
    ['NAME:PolylineParameters', 'IsPolylineCovered:=', True, 'IsPolylineClosed:=', True, pts, segs],
    [
        'NAME:Attributes',
        'Name:=', 'rect_pk_Q1_2',
        'Flags:=', '',
        'Color:=', '(255 100 100)',
        'Transparency:=', 0.0,
        'PartCoordinateSystem:=', 'Global',
        'UDMId:=', '',
        'MaterialName:=', 'vacuum',
        'SolveInside:=', True
    ]
)
# Element: a_connector_pad_Q1_3
pts = ['NAME:PolylinePoints']
segs = ['NAME:PolylineSegments']
pts.append(['NAME:PLPoint', 'X:=', '-2.620000mm', 'Y:=', '1.975000mm', 'Z:=', '0.0mm'])
segs.append(['NAME:PLSegment', 'SegmentType:=', 'Line', 'StartIndex:=', 0, 'NoOfPoints:=', 2])
pts.append(['NAME:PLPoint', 'X:=', '-2.620000mm', 'Y:=', '2.025000mm', 'Z:=', '0.0mm'])
segs.append(['NAME:PLSegment', 'SegmentType:=', 'Line', 'StartIndex:=', 1, 'NoOfPoints:=', 2])
pts.append(['NAME:PLPoint', 'X:=', '-2.650000mm', 'Y:=', '2.025000mm', 'Z:=', '0.0mm'])
segs.append(['NAME:PLSegment', 'SegmentType:=', 'Line', 'StartIndex:=', 2, 'NoOfPoints:=', 2])
pts.append(['NAME:PLPoint', 'X:=', '-2.650000mm', 'Y:=', '1.975000mm', 'Z:=', '0.0mm'])
segs.append(['NAME:PLSegment', 'SegmentType:=', 'Line', 'StartIndex:=', 3, 'NoOfPoints:=', 2])
pts.append(['NAME:PLPoint', 'X:=', '-2.620000mm', 'Y:=', '1.975000mm', 'Z:=', '0.0mm'])
oEditor.CreatePolyline(
    ['NAME:PolylineParameters', 'IsPolylineCovered:=', True, 'IsPolylineClosed:=', True, pts, segs],
    [
        'NAME:Attributes',
        'Name:=', 'a_connector_pad_Q1_3',
        'Flags:=', '',
        'Color:=', '(200 220 255)',
        'Transparency:=', 0.0,
        'PartCoordinateSystem:=', 'Global',
        'UDMId:=', '',
        'MaterialName:=', 'vacuum',
        'SolveInside:=', True
    ]
)
# Element: b_connector_pad_Q1_4
pts = ['NAME:PolylinePoints']
segs = ['NAME:PolylineSegments']
pts.append(['NAME:PLPoint', 'X:=', '-2.380000mm', 'Y:=', '1.975000mm', 'Z:=', '0.0mm'])
segs.append(['NAME:PLSegment', 'SegmentType:=', 'Line', 'StartIndex:=', 0, 'NoOfPoints:=', 2])
pts.append(['NAME:PLPoint', 'X:=', '-2.380000mm', 'Y:=', '2.025000mm', 'Z:=', '0.0mm'])
segs.append(['NAME:PLSegment', 'SegmentType:=', 'Line', 'StartIndex:=', 1, 'NoOfPoints:=', 2])
pts.append(['NAME:PLPoint', 'X:=', '-2.350000mm', 'Y:=', '2.025000mm', 'Z:=', '0.0mm'])
segs.append(['NAME:PLSegment', 'SegmentType:=', 'Line', 'StartIndex:=', 2, 'NoOfPoints:=', 2])
pts.append(['NAME:PLPoint', 'X:=', '-2.350000mm', 'Y:=', '1.975000mm', 'Z:=', '0.0mm'])
segs.append(['NAME:PLSegment', 'SegmentType:=', 'Line', 'StartIndex:=', 3, 'NoOfPoints:=', 2])
pts.append(['NAME:PLPoint', 'X:=', '-2.380000mm', 'Y:=', '1.975000mm', 'Z:=', '0.0mm'])
oEditor.CreatePolyline(
    ['NAME:PolylineParameters', 'IsPolylineCovered:=', True, 'IsPolylineClosed:=', True, pts, segs],
    [
        'NAME:Attributes',
        'Name:=', 'b_connector_pad_Q1_4',
        'Flags:=', '',
        'Color:=', '(200 220 255)',
        'Transparency:=', 0.0,
        'PartCoordinateSystem:=', 'Global',
        'UDMId:=', '',
        'MaterialName:=', 'vacuum',
        'SolveInside:=', True
    ]
)
# Element: pad_top_Q2_5
pts = ['NAME:PolylinePoints']
segs = ['NAME:PolylineSegments']
pts.append(['NAME:PLPoint', 'X:=', '-0.015000mm', 'Y:=', '1.772500mm', 'Z:=', '0.0mm'])
segs.append(['NAME:PLSegment', 'SegmentType:=', 'Line', 'StartIndex:=', 0, 'NoOfPoints:=', 2])
pts.append(['NAME:PLPoint', 'X:=', '-0.015000mm', 'Y:=', '2.227500mm', 'Z:=', '0.0mm'])
segs.append(['NAME:PLSegment', 'SegmentType:=', 'Line', 'StartIndex:=', 1, 'NoOfPoints:=', 2])
pts.append(['NAME:PLPoint', 'X:=', '-0.105000mm', 'Y:=', '2.227500mm', 'Z:=', '0.0mm'])
segs.append(['NAME:PLSegment', 'SegmentType:=', 'Line', 'StartIndex:=', 2, 'NoOfPoints:=', 2])
pts.append(['NAME:PLPoint', 'X:=', '-0.105000mm', 'Y:=', '1.772500mm', 'Z:=', '0.0mm'])
segs.append(['NAME:PLSegment', 'SegmentType:=', 'Line', 'StartIndex:=', 3, 'NoOfPoints:=', 2])
pts.append(['NAME:PLPoint', 'X:=', '-0.015000mm', 'Y:=', '1.772500mm', 'Z:=', '0.0mm'])
oEditor.CreatePolyline(
    ['NAME:PolylineParameters', 'IsPolylineCovered:=', True, 'IsPolylineClosed:=', True, pts, segs],
    [
        'NAME:Attributes',
        'Name:=', 'pad_top_Q2_5',
        'Flags:=', '',
        'Color:=', '(200 220 255)',
        'Transparency:=', 0.0,
        'PartCoordinateSystem:=', 'Global',
        'UDMId:=', '',
        'MaterialName:=', 'vacuum',
        'SolveInside:=', True
    ]
)
# Element: pad_bot_Q2_6
pts = ['NAME:PolylinePoints']
segs = ['NAME:PolylineSegments']
pts.append(['NAME:PLPoint', 'X:=', '0.105000mm', 'Y:=', '1.772500mm', 'Z:=', '0.0mm'])
segs.append(['NAME:PLSegment', 'SegmentType:=', 'Line', 'StartIndex:=', 0, 'NoOfPoints:=', 2])
pts.append(['NAME:PLPoint', 'X:=', '0.105000mm', 'Y:=', '2.227500mm', 'Z:=', '0.0mm'])
segs.append(['NAME:PLSegment', 'SegmentType:=', 'Line', 'StartIndex:=', 1, 'NoOfPoints:=', 2])
pts.append(['NAME:PLPoint', 'X:=', '0.015000mm', 'Y:=', '2.227500mm', 'Z:=', '0.0mm'])
segs.append(['NAME:PLSegment', 'SegmentType:=', 'Line', 'StartIndex:=', 2, 'NoOfPoints:=', 2])
pts.append(['NAME:PLPoint', 'X:=', '0.015000mm', 'Y:=', '1.772500mm', 'Z:=', '0.0mm'])
segs.append(['NAME:PLSegment', 'SegmentType:=', 'Line', 'StartIndex:=', 3, 'NoOfPoints:=', 2])
pts.append(['NAME:PLPoint', 'X:=', '0.105000mm', 'Y:=', '1.772500mm', 'Z:=', '0.0mm'])
oEditor.CreatePolyline(
    ['NAME:PolylineParameters', 'IsPolylineCovered:=', True, 'IsPolylineClosed:=', True, pts, segs],
    [
        'NAME:Attributes',
        'Name:=', 'pad_bot_Q2_6',
        'Flags:=', '',
        'Color:=', '(200 220 255)',
        'Transparency:=', 0.0,
        'PartCoordinateSystem:=', 'Global',
        'UDMId:=', '',
        'MaterialName:=', 'vacuum',
        'SolveInside:=', True
    ]
)
# Element: rect_pk_Q2_7
pts = ['NAME:PolylinePoints']
segs = ['NAME:PolylineSegments']
pts.append(['NAME:PLPoint', 'X:=', '0.325000mm', 'Y:=', '1.675000mm', 'Z:=', '0.0mm'])
segs.append(['NAME:PLSegment', 'SegmentType:=', 'Line', 'StartIndex:=', 0, 'NoOfPoints:=', 2])
pts.append(['NAME:PLPoint', 'X:=', '0.325000mm', 'Y:=', '2.325000mm', 'Z:=', '0.0mm'])
segs.append(['NAME:PLSegment', 'SegmentType:=', 'Line', 'StartIndex:=', 1, 'NoOfPoints:=', 2])
pts.append(['NAME:PLPoint', 'X:=', '-0.325000mm', 'Y:=', '2.325000mm', 'Z:=', '0.0mm'])
segs.append(['NAME:PLSegment', 'SegmentType:=', 'Line', 'StartIndex:=', 2, 'NoOfPoints:=', 2])
pts.append(['NAME:PLPoint', 'X:=', '-0.325000mm', 'Y:=', '1.675000mm', 'Z:=', '0.0mm'])
segs.append(['NAME:PLSegment', 'SegmentType:=', 'Line', 'StartIndex:=', 3, 'NoOfPoints:=', 2])
pts.append(['NAME:PLPoint', 'X:=', '0.325000mm', 'Y:=', '1.675000mm', 'Z:=', '0.0mm'])
oEditor.CreatePolyline(
    ['NAME:PolylineParameters', 'IsPolylineCovered:=', True, 'IsPolylineClosed:=', True, pts, segs],
    [
        'NAME:Attributes',
        'Name:=', 'rect_pk_Q2_7',
        'Flags:=', '',
        'Color:=', '(255 100 100)',
        'Transparency:=', 0.0,
        'PartCoordinateSystem:=', 'Global',
        'UDMId:=', '',
        'MaterialName:=', 'vacuum',
        'SolveInside:=', True
    ]
)
# Element: a_connector_pad_Q2_8
pts = ['NAME:PolylinePoints']
segs = ['NAME:PolylineSegments']
pts.append(['NAME:PLPoint', 'X:=', '-0.120000mm', 'Y:=', '1.975000mm', 'Z:=', '0.0mm'])
segs.append(['NAME:PLSegment', 'SegmentType:=', 'Line', 'StartIndex:=', 0, 'NoOfPoints:=', 2])
pts.append(['NAME:PLPoint', 'X:=', '-0.120000mm', 'Y:=', '2.025000mm', 'Z:=', '0.0mm'])
segs.append(['NAME:PLSegment', 'SegmentType:=', 'Line', 'StartIndex:=', 1, 'NoOfPoints:=', 2])
pts.append(['NAME:PLPoint', 'X:=', '-0.150000mm', 'Y:=', '2.025000mm', 'Z:=', '0.0mm'])
segs.append(['NAME:PLSegment', 'SegmentType:=', 'Line', 'StartIndex:=', 2, 'NoOfPoints:=', 2])
pts.append(['NAME:PLPoint', 'X:=', '-0.150000mm', 'Y:=', '1.975000mm', 'Z:=', '0.0mm'])
segs.append(['NAME:PLSegment', 'SegmentType:=', 'Line', 'StartIndex:=', 3, 'NoOfPoints:=', 2])
pts.append(['NAME:PLPoint', 'X:=', '-0.120000mm', 'Y:=', '1.975000mm', 'Z:=', '0.0mm'])
oEditor.CreatePolyline(
    ['NAME:PolylineParameters', 'IsPolylineCovered:=', True, 'IsPolylineClosed:=', True, pts, segs],
    [
        'NAME:Attributes',
        'Name:=', 'a_connector_pad_Q2_8',
        'Flags:=', '',
        'Color:=', '(200 220 255)',
        'Transparency:=', 0.0,
        'PartCoordinateSystem:=', 'Global',
        'UDMId:=', '',
        'MaterialName:=', 'vacuum',
        'SolveInside:=', True
    ]
)
# Element: b_connector_pad_Q2_9
pts = ['NAME:PolylinePoints']
segs = ['NAME:PolylineSegments']
pts.append(['NAME:PLPoint', 'X:=', '0.120000mm', 'Y:=', '1.975000mm', 'Z:=', '0.0mm'])
segs.append(['NAME:PLSegment', 'SegmentType:=', 'Line', 'StartIndex:=', 0, 'NoOfPoints:=', 2])
pts.append(['NAME:PLPoint', 'X:=', '0.120000mm', 'Y:=', '2.025000mm', 'Z:=', '0.0mm'])
segs.append(['NAME:PLSegment', 'SegmentType:=', 'Line', 'StartIndex:=', 1, 'NoOfPoints:=', 2])
pts.append(['NAME:PLPoint', 'X:=', '0.150000mm', 'Y:=', '2.025000mm', 'Z:=', '0.0mm'])
segs.append(['NAME:PLSegment', 'SegmentType:=', 'Line', 'StartIndex:=', 2, 'NoOfPoints:=', 2])
pts.append(['NAME:PLPoint', 'X:=', '0.150000mm', 'Y:=', '1.975000mm', 'Z:=', '0.0mm'])
segs.append(['NAME:PLSegment', 'SegmentType:=', 'Line', 'StartIndex:=', 3, 'NoOfPoints:=', 2])
pts.append(['NAME:PLPoint', 'X:=', '0.120000mm', 'Y:=', '1.975000mm', 'Z:=', '0.0mm'])
oEditor.CreatePolyline(
    ['NAME:PolylineParameters', 'IsPolylineCovered:=', True, 'IsPolylineClosed:=', True, pts, segs],
    [
        'NAME:Attributes',
        'Name:=', 'b_connector_pad_Q2_9',
        'Flags:=', '',
        'Color:=', '(200 220 255)',
        'Transparency:=', 0.0,
        'PartCoordinateSystem:=', 'Global',
        'UDMId:=', '',
        'MaterialName:=', 'vacuum',
        'SolveInside:=', True
    ]
)
# Element: pad_top_Q3_10
pts = ['NAME:PolylinePoints']
segs = ['NAME:PolylineSegments']
pts.append(['NAME:PLPoint', 'X:=', '2.485000mm', 'Y:=', '1.772500mm', 'Z:=', '0.0mm'])
segs.append(['NAME:PLSegment', 'SegmentType:=', 'Line', 'StartIndex:=', 0, 'NoOfPoints:=', 2])
pts.append(['NAME:PLPoint', 'X:=', '2.485000mm', 'Y:=', '2.227500mm', 'Z:=', '0.0mm'])
segs.append(['NAME:PLSegment', 'SegmentType:=', 'Line', 'StartIndex:=', 1, 'NoOfPoints:=', 2])
pts.append(['NAME:PLPoint', 'X:=', '2.395000mm', 'Y:=', '2.227500mm', 'Z:=', '0.0mm'])
segs.append(['NAME:PLSegment', 'SegmentType:=', 'Line', 'StartIndex:=', 2, 'NoOfPoints:=', 2])
pts.append(['NAME:PLPoint', 'X:=', '2.395000mm', 'Y:=', '1.772500mm', 'Z:=', '0.0mm'])
segs.append(['NAME:PLSegment', 'SegmentType:=', 'Line', 'StartIndex:=', 3, 'NoOfPoints:=', 2])
pts.append(['NAME:PLPoint', 'X:=', '2.485000mm', 'Y:=', '1.772500mm', 'Z:=', '0.0mm'])
oEditor.CreatePolyline(
    ['NAME:PolylineParameters', 'IsPolylineCovered:=', True, 'IsPolylineClosed:=', True, pts, segs],
    [
        'NAME:Attributes',
        'Name:=', 'pad_top_Q3_10',
        'Flags:=', '',
        'Color:=', '(200 220 255)',
        'Transparency:=', 0.0,
        'PartCoordinateSystem:=', 'Global',
        'UDMId:=', '',
        'MaterialName:=', 'vacuum',
        'SolveInside:=', True
    ]
)
# Element: pad_bot_Q3_11
pts = ['NAME:PolylinePoints']
segs = ['NAME:PolylineSegments']
pts.append(['NAME:PLPoint', 'X:=', '2.605000mm', 'Y:=', '1.772500mm', 'Z:=', '0.0mm'])
segs.append(['NAME:PLSegment', 'SegmentType:=', 'Line', 'StartIndex:=', 0, 'NoOfPoints:=', 2])
pts.append(['NAME:PLPoint', 'X:=', '2.605000mm', 'Y:=', '2.227500mm', 'Z:=', '0.0mm'])
segs.append(['NAME:PLSegment', 'SegmentType:=', 'Line', 'StartIndex:=', 1, 'NoOfPoints:=', 2])
pts.append(['NAME:PLPoint', 'X:=', '2.515000mm', 'Y:=', '2.227500mm', 'Z:=', '0.0mm'])
segs.append(['NAME:PLSegment', 'SegmentType:=', 'Line', 'StartIndex:=', 2, 'NoOfPoints:=', 2])
pts.append(['NAME:PLPoint', 'X:=', '2.515000mm', 'Y:=', '1.772500mm', 'Z:=', '0.0mm'])
segs.append(['NAME:PLSegment', 'SegmentType:=', 'Line', 'StartIndex:=', 3, 'NoOfPoints:=', 2])
pts.append(['NAME:PLPoint', 'X:=', '2.605000mm', 'Y:=', '1.772500mm', 'Z:=', '0.0mm'])
oEditor.CreatePolyline(
    ['NAME:PolylineParameters', 'IsPolylineCovered:=', True, 'IsPolylineClosed:=', True, pts, segs],
    [
        'NAME:Attributes',
        'Name:=', 'pad_bot_Q3_11',
        'Flags:=', '',
        'Color:=', '(200 220 255)',
        'Transparency:=', 0.0,
        'PartCoordinateSystem:=', 'Global',
        'UDMId:=', '',
        'MaterialName:=', 'vacuum',
        'SolveInside:=', True
    ]
)
# Element: rect_pk_Q3_12
pts = ['NAME:PolylinePoints']
segs = ['NAME:PolylineSegments']
pts.append(['NAME:PLPoint', 'X:=', '2.825000mm', 'Y:=', '1.675000mm', 'Z:=', '0.0mm'])
segs.append(['NAME:PLSegment', 'SegmentType:=', 'Line', 'StartIndex:=', 0, 'NoOfPoints:=', 2])
pts.append(['NAME:PLPoint', 'X:=', '2.825000mm', 'Y:=', '2.325000mm', 'Z:=', '0.0mm'])
segs.append(['NAME:PLSegment', 'SegmentType:=', 'Line', 'StartIndex:=', 1, 'NoOfPoints:=', 2])
pts.append(['NAME:PLPoint', 'X:=', '2.175000mm', 'Y:=', '2.325000mm', 'Z:=', '0.0mm'])
segs.append(['NAME:PLSegment', 'SegmentType:=', 'Line', 'StartIndex:=', 2, 'NoOfPoints:=', 2])
pts.append(['NAME:PLPoint', 'X:=', '2.175000mm', 'Y:=', '1.675000mm', 'Z:=', '0.0mm'])
segs.append(['NAME:PLSegment', 'SegmentType:=', 'Line', 'StartIndex:=', 3, 'NoOfPoints:=', 2])
pts.append(['NAME:PLPoint', 'X:=', '2.825000mm', 'Y:=', '1.675000mm', 'Z:=', '0.0mm'])
oEditor.CreatePolyline(
    ['NAME:PolylineParameters', 'IsPolylineCovered:=', True, 'IsPolylineClosed:=', True, pts, segs],
    [
        'NAME:Attributes',
        'Name:=', 'rect_pk_Q3_12',
        'Flags:=', '',
        'Color:=', '(255 100 100)',
        'Transparency:=', 0.0,
        'PartCoordinateSystem:=', 'Global',
        'UDMId:=', '',
        'MaterialName:=', 'vacuum',
        'SolveInside:=', True
    ]
)
# Element: a_connector_pad_Q3_13
pts = ['NAME:PolylinePoints']
segs = ['NAME:PolylineSegments']
pts.append(['NAME:PLPoint', 'X:=', '2.380000mm', 'Y:=', '1.975000mm', 'Z:=', '0.0mm'])
segs.append(['NAME:PLSegment', 'SegmentType:=', 'Line', 'StartIndex:=', 0, 'NoOfPoints:=', 2])
pts.append(['NAME:PLPoint', 'X:=', '2.380000mm', 'Y:=', '2.025000mm', 'Z:=', '0.0mm'])
segs.append(['NAME:PLSegment', 'SegmentType:=', 'Line', 'StartIndex:=', 1, 'NoOfPoints:=', 2])
pts.append(['NAME:PLPoint', 'X:=', '2.350000mm', 'Y:=', '2.025000mm', 'Z:=', '0.0mm'])
segs.append(['NAME:PLSegment', 'SegmentType:=', 'Line', 'StartIndex:=', 2, 'NoOfPoints:=', 2])
pts.append(['NAME:PLPoint', 'X:=', '2.350000mm', 'Y:=', '1.975000mm', 'Z:=', '0.0mm'])
segs.append(['NAME:PLSegment', 'SegmentType:=', 'Line', 'StartIndex:=', 3, 'NoOfPoints:=', 2])
pts.append(['NAME:PLPoint', 'X:=', '2.380000mm', 'Y:=', '1.975000mm', 'Z:=', '0.0mm'])
oEditor.CreatePolyline(
    ['NAME:PolylineParameters', 'IsPolylineCovered:=', True, 'IsPolylineClosed:=', True, pts, segs],
    [
        'NAME:Attributes',
        'Name:=', 'a_connector_pad_Q3_13',
        'Flags:=', '',
        'Color:=', '(200 220 255)',
        'Transparency:=', 0.0,
        'PartCoordinateSystem:=', 'Global',
        'UDMId:=', '',
        'MaterialName:=', 'vacuum',
        'SolveInside:=', True
    ]
)
# Element: b_connector_pad_Q3_14
pts = ['NAME:PolylinePoints']
segs = ['NAME:PolylineSegments']
pts.append(['NAME:PLPoint', 'X:=', '2.620000mm', 'Y:=', '1.975000mm', 'Z:=', '0.0mm'])
segs.append(['NAME:PLSegment', 'SegmentType:=', 'Line', 'StartIndex:=', 0, 'NoOfPoints:=', 2])
pts.append(['NAME:PLPoint', 'X:=', '2.620000mm', 'Y:=', '2.025000mm', 'Z:=', '0.0mm'])
segs.append(['NAME:PLSegment', 'SegmentType:=', 'Line', 'StartIndex:=', 1, 'NoOfPoints:=', 2])
pts.append(['NAME:PLPoint', 'X:=', '2.650000mm', 'Y:=', '2.025000mm', 'Z:=', '0.0mm'])
segs.append(['NAME:PLSegment', 'SegmentType:=', 'Line', 'StartIndex:=', 2, 'NoOfPoints:=', 2])
pts.append(['NAME:PLPoint', 'X:=', '2.650000mm', 'Y:=', '1.975000mm', 'Z:=', '0.0mm'])
segs.append(['NAME:PLSegment', 'SegmentType:=', 'Line', 'StartIndex:=', 3, 'NoOfPoints:=', 2])
pts.append(['NAME:PLPoint', 'X:=', '2.620000mm', 'Y:=', '1.975000mm', 'Z:=', '0.0mm'])
oEditor.CreatePolyline(
    ['NAME:PolylineParameters', 'IsPolylineCovered:=', True, 'IsPolylineClosed:=', True, pts, segs],
    [
        'NAME:Attributes',
        'Name:=', 'b_connector_pad_Q3_14',
        'Flags:=', '',
        'Color:=', '(200 220 255)',
        'Transparency:=', 0.0,
        'PartCoordinateSystem:=', 'Global',
        'UDMId:=', '',
        'MaterialName:=', 'vacuum',
        'SolveInside:=', True
    ]
)
# Element: pad_top_Q5_15
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
        'Name:=', 'pad_top_Q5_15',
        'Flags:=', '',
        'Color:=', '(200 220 255)',
        'Transparency:=', 0.0,
        'PartCoordinateSystem:=', 'Global',
        'UDMId:=', '',
        'MaterialName:=', 'vacuum',
        'SolveInside:=', True
    ]
)
# Element: pad_bot_Q5_16
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
        'Name:=', 'pad_bot_Q5_16',
        'Flags:=', '',
        'Color:=', '(200 220 255)',
        'Transparency:=', 0.0,
        'PartCoordinateSystem:=', 'Global',
        'UDMId:=', '',
        'MaterialName:=', 'vacuum',
        'SolveInside:=', True
    ]
)
# Element: rect_pk_Q5_17
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
        'Name:=', 'rect_pk_Q5_17',
        'Flags:=', '',
        'Color:=', '(255 100 100)',
        'Transparency:=', 0.0,
        'PartCoordinateSystem:=', 'Global',
        'UDMId:=', '',
        'MaterialName:=', 'vacuum',
        'SolveInside:=', True
    ]
)
# Element: a_connector_pad_Q5_18
pts = ['NAME:PolylinePoints']
segs = ['NAME:PolylineSegments']
pts.append(['NAME:PLPoint', 'X:=', '-2.620000mm', 'Y:=', '-0.025000mm', 'Z:=', '0.0mm'])
segs.append(['NAME:PLSegment', 'SegmentType:=', 'Line', 'StartIndex:=', 0, 'NoOfPoints:=', 2])
pts.append(['NAME:PLPoint', 'X:=', '-2.620000mm', 'Y:=', '0.025000mm', 'Z:=', '0.0mm'])
segs.append(['NAME:PLSegment', 'SegmentType:=', 'Line', 'StartIndex:=', 1, 'NoOfPoints:=', 2])
pts.append(['NAME:PLPoint', 'X:=', '-2.650000mm', 'Y:=', '0.025000mm', 'Z:=', '0.0mm'])
segs.append(['NAME:PLSegment', 'SegmentType:=', 'Line', 'StartIndex:=', 2, 'NoOfPoints:=', 2])
pts.append(['NAME:PLPoint', 'X:=', '-2.650000mm', 'Y:=', '-0.025000mm', 'Z:=', '0.0mm'])
segs.append(['NAME:PLSegment', 'SegmentType:=', 'Line', 'StartIndex:=', 3, 'NoOfPoints:=', 2])
pts.append(['NAME:PLPoint', 'X:=', '-2.620000mm', 'Y:=', '-0.025000mm', 'Z:=', '0.0mm'])
oEditor.CreatePolyline(
    ['NAME:PolylineParameters', 'IsPolylineCovered:=', True, 'IsPolylineClosed:=', True, pts, segs],
    [
        'NAME:Attributes',
        'Name:=', 'a_connector_pad_Q5_18',
        'Flags:=', '',
        'Color:=', '(200 220 255)',
        'Transparency:=', 0.0,
        'PartCoordinateSystem:=', 'Global',
        'UDMId:=', '',
        'MaterialName:=', 'vacuum',
        'SolveInside:=', True
    ]
)
# Element: b_connector_pad_Q5_19
pts = ['NAME:PolylinePoints']
segs = ['NAME:PolylineSegments']
pts.append(['NAME:PLPoint', 'X:=', '-2.380000mm', 'Y:=', '-0.025000mm', 'Z:=', '0.0mm'])
segs.append(['NAME:PLSegment', 'SegmentType:=', 'Line', 'StartIndex:=', 0, 'NoOfPoints:=', 2])
pts.append(['NAME:PLPoint', 'X:=', '-2.380000mm', 'Y:=', '0.025000mm', 'Z:=', '0.0mm'])
segs.append(['NAME:PLSegment', 'SegmentType:=', 'Line', 'StartIndex:=', 1, 'NoOfPoints:=', 2])
pts.append(['NAME:PLPoint', 'X:=', '-2.350000mm', 'Y:=', '0.025000mm', 'Z:=', '0.0mm'])
segs.append(['NAME:PLSegment', 'SegmentType:=', 'Line', 'StartIndex:=', 2, 'NoOfPoints:=', 2])
pts.append(['NAME:PLPoint', 'X:=', '-2.350000mm', 'Y:=', '-0.025000mm', 'Z:=', '0.0mm'])
segs.append(['NAME:PLSegment', 'SegmentType:=', 'Line', 'StartIndex:=', 3, 'NoOfPoints:=', 2])
pts.append(['NAME:PLPoint', 'X:=', '-2.380000mm', 'Y:=', '-0.025000mm', 'Z:=', '0.0mm'])
oEditor.CreatePolyline(
    ['NAME:PolylineParameters', 'IsPolylineCovered:=', True, 'IsPolylineClosed:=', True, pts, segs],
    [
        'NAME:Attributes',
        'Name:=', 'b_connector_pad_Q5_19',
        'Flags:=', '',
        'Color:=', '(200 220 255)',
        'Transparency:=', 0.0,
        'PartCoordinateSystem:=', 'Global',
        'UDMId:=', '',
        'MaterialName:=', 'vacuum',
        'SolveInside:=', True
    ]
)
# Element: pad_top_Q6_20
pts = ['NAME:PolylinePoints']
segs = ['NAME:PolylineSegments']
pts.append(['NAME:PLPoint', 'X:=', '-0.015000mm', 'Y:=', '-0.227500mm', 'Z:=', '0.0mm'])
segs.append(['NAME:PLSegment', 'SegmentType:=', 'Line', 'StartIndex:=', 0, 'NoOfPoints:=', 2])
pts.append(['NAME:PLPoint', 'X:=', '-0.015000mm', 'Y:=', '0.227500mm', 'Z:=', '0.0mm'])
segs.append(['NAME:PLSegment', 'SegmentType:=', 'Line', 'StartIndex:=', 1, 'NoOfPoints:=', 2])
pts.append(['NAME:PLPoint', 'X:=', '-0.105000mm', 'Y:=', '0.227500mm', 'Z:=', '0.0mm'])
segs.append(['NAME:PLSegment', 'SegmentType:=', 'Line', 'StartIndex:=', 2, 'NoOfPoints:=', 2])
pts.append(['NAME:PLPoint', 'X:=', '-0.105000mm', 'Y:=', '-0.227500mm', 'Z:=', '0.0mm'])
segs.append(['NAME:PLSegment', 'SegmentType:=', 'Line', 'StartIndex:=', 3, 'NoOfPoints:=', 2])
pts.append(['NAME:PLPoint', 'X:=', '-0.015000mm', 'Y:=', '-0.227500mm', 'Z:=', '0.0mm'])
oEditor.CreatePolyline(
    ['NAME:PolylineParameters', 'IsPolylineCovered:=', True, 'IsPolylineClosed:=', True, pts, segs],
    [
        'NAME:Attributes',
        'Name:=', 'pad_top_Q6_20',
        'Flags:=', '',
        'Color:=', '(200 220 255)',
        'Transparency:=', 0.0,
        'PartCoordinateSystem:=', 'Global',
        'UDMId:=', '',
        'MaterialName:=', 'vacuum',
        'SolveInside:=', True
    ]
)
# Element: pad_bot_Q6_21
pts = ['NAME:PolylinePoints']
segs = ['NAME:PolylineSegments']
pts.append(['NAME:PLPoint', 'X:=', '0.105000mm', 'Y:=', '-0.227500mm', 'Z:=', '0.0mm'])
segs.append(['NAME:PLSegment', 'SegmentType:=', 'Line', 'StartIndex:=', 0, 'NoOfPoints:=', 2])
pts.append(['NAME:PLPoint', 'X:=', '0.105000mm', 'Y:=', '0.227500mm', 'Z:=', '0.0mm'])
segs.append(['NAME:PLSegment', 'SegmentType:=', 'Line', 'StartIndex:=', 1, 'NoOfPoints:=', 2])
pts.append(['NAME:PLPoint', 'X:=', '0.015000mm', 'Y:=', '0.227500mm', 'Z:=', '0.0mm'])
segs.append(['NAME:PLSegment', 'SegmentType:=', 'Line', 'StartIndex:=', 2, 'NoOfPoints:=', 2])
pts.append(['NAME:PLPoint', 'X:=', '0.015000mm', 'Y:=', '-0.227500mm', 'Z:=', '0.0mm'])
segs.append(['NAME:PLSegment', 'SegmentType:=', 'Line', 'StartIndex:=', 3, 'NoOfPoints:=', 2])
pts.append(['NAME:PLPoint', 'X:=', '0.105000mm', 'Y:=', '-0.227500mm', 'Z:=', '0.0mm'])
oEditor.CreatePolyline(
    ['NAME:PolylineParameters', 'IsPolylineCovered:=', True, 'IsPolylineClosed:=', True, pts, segs],
    [
        'NAME:Attributes',
        'Name:=', 'pad_bot_Q6_21',
        'Flags:=', '',
        'Color:=', '(200 220 255)',
        'Transparency:=', 0.0,
        'PartCoordinateSystem:=', 'Global',
        'UDMId:=', '',
        'MaterialName:=', 'vacuum',
        'SolveInside:=', True
    ]
)
# Element: rect_pk_Q6_22
pts = ['NAME:PolylinePoints']
segs = ['NAME:PolylineSegments']
pts.append(['NAME:PLPoint', 'X:=', '0.325000mm', 'Y:=', '-0.325000mm', 'Z:=', '0.0mm'])
segs.append(['NAME:PLSegment', 'SegmentType:=', 'Line', 'StartIndex:=', 0, 'NoOfPoints:=', 2])
pts.append(['NAME:PLPoint', 'X:=', '0.325000mm', 'Y:=', '0.325000mm', 'Z:=', '0.0mm'])
segs.append(['NAME:PLSegment', 'SegmentType:=', 'Line', 'StartIndex:=', 1, 'NoOfPoints:=', 2])
pts.append(['NAME:PLPoint', 'X:=', '-0.325000mm', 'Y:=', '0.325000mm', 'Z:=', '0.0mm'])
segs.append(['NAME:PLSegment', 'SegmentType:=', 'Line', 'StartIndex:=', 2, 'NoOfPoints:=', 2])
pts.append(['NAME:PLPoint', 'X:=', '-0.325000mm', 'Y:=', '-0.325000mm', 'Z:=', '0.0mm'])
segs.append(['NAME:PLSegment', 'SegmentType:=', 'Line', 'StartIndex:=', 3, 'NoOfPoints:=', 2])
pts.append(['NAME:PLPoint', 'X:=', '0.325000mm', 'Y:=', '-0.325000mm', 'Z:=', '0.0mm'])
oEditor.CreatePolyline(
    ['NAME:PolylineParameters', 'IsPolylineCovered:=', True, 'IsPolylineClosed:=', True, pts, segs],
    [
        'NAME:Attributes',
        'Name:=', 'rect_pk_Q6_22',
        'Flags:=', '',
        'Color:=', '(255 100 100)',
        'Transparency:=', 0.0,
        'PartCoordinateSystem:=', 'Global',
        'UDMId:=', '',
        'MaterialName:=', 'vacuum',
        'SolveInside:=', True
    ]
)
# Element: a_connector_pad_Q6_23
pts = ['NAME:PolylinePoints']
segs = ['NAME:PolylineSegments']
pts.append(['NAME:PLPoint', 'X:=', '-0.120000mm', 'Y:=', '-0.025000mm', 'Z:=', '0.0mm'])
segs.append(['NAME:PLSegment', 'SegmentType:=', 'Line', 'StartIndex:=', 0, 'NoOfPoints:=', 2])
pts.append(['NAME:PLPoint', 'X:=', '-0.120000mm', 'Y:=', '0.025000mm', 'Z:=', '0.0mm'])
segs.append(['NAME:PLSegment', 'SegmentType:=', 'Line', 'StartIndex:=', 1, 'NoOfPoints:=', 2])
pts.append(['NAME:PLPoint', 'X:=', '-0.150000mm', 'Y:=', '0.025000mm', 'Z:=', '0.0mm'])
segs.append(['NAME:PLSegment', 'SegmentType:=', 'Line', 'StartIndex:=', 2, 'NoOfPoints:=', 2])
pts.append(['NAME:PLPoint', 'X:=', '-0.150000mm', 'Y:=', '-0.025000mm', 'Z:=', '0.0mm'])
segs.append(['NAME:PLSegment', 'SegmentType:=', 'Line', 'StartIndex:=', 3, 'NoOfPoints:=', 2])
pts.append(['NAME:PLPoint', 'X:=', '-0.120000mm', 'Y:=', '-0.025000mm', 'Z:=', '0.0mm'])
oEditor.CreatePolyline(
    ['NAME:PolylineParameters', 'IsPolylineCovered:=', True, 'IsPolylineClosed:=', True, pts, segs],
    [
        'NAME:Attributes',
        'Name:=', 'a_connector_pad_Q6_23',
        'Flags:=', '',
        'Color:=', '(200 220 255)',
        'Transparency:=', 0.0,
        'PartCoordinateSystem:=', 'Global',
        'UDMId:=', '',
        'MaterialName:=', 'vacuum',
        'SolveInside:=', True
    ]
)
# Element: b_connector_pad_Q6_24
pts = ['NAME:PolylinePoints']
segs = ['NAME:PolylineSegments']
pts.append(['NAME:PLPoint', 'X:=', '0.120000mm', 'Y:=', '-0.025000mm', 'Z:=', '0.0mm'])
segs.append(['NAME:PLSegment', 'SegmentType:=', 'Line', 'StartIndex:=', 0, 'NoOfPoints:=', 2])
pts.append(['NAME:PLPoint', 'X:=', '0.120000mm', 'Y:=', '0.025000mm', 'Z:=', '0.0mm'])
segs.append(['NAME:PLSegment', 'SegmentType:=', 'Line', 'StartIndex:=', 1, 'NoOfPoints:=', 2])
pts.append(['NAME:PLPoint', 'X:=', '0.150000mm', 'Y:=', '0.025000mm', 'Z:=', '0.0mm'])
segs.append(['NAME:PLSegment', 'SegmentType:=', 'Line', 'StartIndex:=', 2, 'NoOfPoints:=', 2])
pts.append(['NAME:PLPoint', 'X:=', '0.150000mm', 'Y:=', '-0.025000mm', 'Z:=', '0.0mm'])
segs.append(['NAME:PLSegment', 'SegmentType:=', 'Line', 'StartIndex:=', 3, 'NoOfPoints:=', 2])
pts.append(['NAME:PLPoint', 'X:=', '0.120000mm', 'Y:=', '-0.025000mm', 'Z:=', '0.0mm'])
oEditor.CreatePolyline(
    ['NAME:PolylineParameters', 'IsPolylineCovered:=', True, 'IsPolylineClosed:=', True, pts, segs],
    [
        'NAME:Attributes',
        'Name:=', 'b_connector_pad_Q6_24',
        'Flags:=', '',
        'Color:=', '(200 220 255)',
        'Transparency:=', 0.0,
        'PartCoordinateSystem:=', 'Global',
        'UDMId:=', '',
        'MaterialName:=', 'vacuum',
        'SolveInside:=', True
    ]
)
# Element: pad_top_Q7_25
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
        'Name:=', 'pad_top_Q7_25',
        'Flags:=', '',
        'Color:=', '(200 220 255)',
        'Transparency:=', 0.0,
        'PartCoordinateSystem:=', 'Global',
        'UDMId:=', '',
        'MaterialName:=', 'vacuum',
        'SolveInside:=', True
    ]
)
# Element: pad_bot_Q7_26
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
        'Name:=', 'pad_bot_Q7_26',
        'Flags:=', '',
        'Color:=', '(200 220 255)',
        'Transparency:=', 0.0,
        'PartCoordinateSystem:=', 'Global',
        'UDMId:=', '',
        'MaterialName:=', 'vacuum',
        'SolveInside:=', True
    ]
)
# Element: rect_pk_Q7_27
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
        'Name:=', 'rect_pk_Q7_27',
        'Flags:=', '',
        'Color:=', '(255 100 100)',
        'Transparency:=', 0.0,
        'PartCoordinateSystem:=', 'Global',
        'UDMId:=', '',
        'MaterialName:=', 'vacuum',
        'SolveInside:=', True
    ]
)
# Element: a_connector_pad_Q7_28
pts = ['NAME:PolylinePoints']
segs = ['NAME:PolylineSegments']
pts.append(['NAME:PLPoint', 'X:=', '2.380000mm', 'Y:=', '-0.025000mm', 'Z:=', '0.0mm'])
segs.append(['NAME:PLSegment', 'SegmentType:=', 'Line', 'StartIndex:=', 0, 'NoOfPoints:=', 2])
pts.append(['NAME:PLPoint', 'X:=', '2.380000mm', 'Y:=', '0.025000mm', 'Z:=', '0.0mm'])
segs.append(['NAME:PLSegment', 'SegmentType:=', 'Line', 'StartIndex:=', 1, 'NoOfPoints:=', 2])
pts.append(['NAME:PLPoint', 'X:=', '2.350000mm', 'Y:=', '0.025000mm', 'Z:=', '0.0mm'])
segs.append(['NAME:PLSegment', 'SegmentType:=', 'Line', 'StartIndex:=', 2, 'NoOfPoints:=', 2])
pts.append(['NAME:PLPoint', 'X:=', '2.350000mm', 'Y:=', '-0.025000mm', 'Z:=', '0.0mm'])
segs.append(['NAME:PLSegment', 'SegmentType:=', 'Line', 'StartIndex:=', 3, 'NoOfPoints:=', 2])
pts.append(['NAME:PLPoint', 'X:=', '2.380000mm', 'Y:=', '-0.025000mm', 'Z:=', '0.0mm'])
oEditor.CreatePolyline(
    ['NAME:PolylineParameters', 'IsPolylineCovered:=', True, 'IsPolylineClosed:=', True, pts, segs],
    [
        'NAME:Attributes',
        'Name:=', 'a_connector_pad_Q7_28',
        'Flags:=', '',
        'Color:=', '(200 220 255)',
        'Transparency:=', 0.0,
        'PartCoordinateSystem:=', 'Global',
        'UDMId:=', '',
        'MaterialName:=', 'vacuum',
        'SolveInside:=', True
    ]
)
# Element: b_connector_pad_Q7_29
pts = ['NAME:PolylinePoints']
segs = ['NAME:PolylineSegments']
pts.append(['NAME:PLPoint', 'X:=', '2.620000mm', 'Y:=', '-0.025000mm', 'Z:=', '0.0mm'])
segs.append(['NAME:PLSegment', 'SegmentType:=', 'Line', 'StartIndex:=', 0, 'NoOfPoints:=', 2])
pts.append(['NAME:PLPoint', 'X:=', '2.620000mm', 'Y:=', '0.025000mm', 'Z:=', '0.0mm'])
segs.append(['NAME:PLSegment', 'SegmentType:=', 'Line', 'StartIndex:=', 1, 'NoOfPoints:=', 2])
pts.append(['NAME:PLPoint', 'X:=', '2.650000mm', 'Y:=', '0.025000mm', 'Z:=', '0.0mm'])
segs.append(['NAME:PLSegment', 'SegmentType:=', 'Line', 'StartIndex:=', 2, 'NoOfPoints:=', 2])
pts.append(['NAME:PLPoint', 'X:=', '2.650000mm', 'Y:=', '-0.025000mm', 'Z:=', '0.0mm'])
segs.append(['NAME:PLSegment', 'SegmentType:=', 'Line', 'StartIndex:=', 3, 'NoOfPoints:=', 2])
pts.append(['NAME:PLPoint', 'X:=', '2.620000mm', 'Y:=', '-0.025000mm', 'Z:=', '0.0mm'])
oEditor.CreatePolyline(
    ['NAME:PolylineParameters', 'IsPolylineCovered:=', True, 'IsPolylineClosed:=', True, pts, segs],
    [
        'NAME:Attributes',
        'Name:=', 'b_connector_pad_Q7_29',
        'Flags:=', '',
        'Color:=', '(200 220 255)',
        'Transparency:=', 0.0,
        'PartCoordinateSystem:=', 'Global',
        'UDMId:=', '',
        'MaterialName:=', 'vacuum',
        'SolveInside:=', True
    ]
)
# Element: pad_top_Q4_30
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
        'Name:=', 'pad_top_Q4_30',
        'Flags:=', '',
        'Color:=', '(200 220 255)',
        'Transparency:=', 0.0,
        'PartCoordinateSystem:=', 'Global',
        'UDMId:=', '',
        'MaterialName:=', 'vacuum',
        'SolveInside:=', True
    ]
)
# Element: pad_bot_Q4_31
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
        'Name:=', 'pad_bot_Q4_31',
        'Flags:=', '',
        'Color:=', '(200 220 255)',
        'Transparency:=', 0.0,
        'PartCoordinateSystem:=', 'Global',
        'UDMId:=', '',
        'MaterialName:=', 'vacuum',
        'SolveInside:=', True
    ]
)
# Element: rect_pk_Q4_32
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
        'Name:=', 'rect_pk_Q4_32',
        'Flags:=', '',
        'Color:=', '(255 100 100)',
        'Transparency:=', 0.0,
        'PartCoordinateSystem:=', 'Global',
        'UDMId:=', '',
        'MaterialName:=', 'vacuum',
        'SolveInside:=', True
    ]
)
# Element: a_connector_pad_Q4_33
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
        'Name:=', 'a_connector_pad_Q4_33',
        'Flags:=', '',
        'Color:=', '(200 220 255)',
        'Transparency:=', 0.0,
        'PartCoordinateSystem:=', 'Global',
        'UDMId:=', '',
        'MaterialName:=', 'vacuum',
        'SolveInside:=', True
    ]
)
# Element: b_connector_pad_Q4_34
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
        'Name:=', 'b_connector_pad_Q4_34',
        'Flags:=', '',
        'Color:=', '(200 220 255)',
        'Transparency:=', 0.0,
        'PartCoordinateSystem:=', 'Global',
        'UDMId:=', '',
        'MaterialName:=', 'vacuum',
        'SolveInside:=', True
    ]
)
# Element: cl_metal_Q4_35
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
        'Name:=', 'cl_metal_Q4_35',
        'Flags:=', '',
        'Color:=', '(200 220 255)',
        'Transparency:=', 0.0,
        'PartCoordinateSystem:=', 'Global',
        'UDMId:=', '',
        'MaterialName:=', 'vacuum',
        'SolveInside:=', True
    ]
)
# Element: cl_etcher_Q4_36
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
        'Name:=', 'cl_etcher_Q4_36',
        'Flags:=', '',
        'Color:=', '(255 100 100)',
        'Transparency:=', 0.0,
        'PartCoordinateSystem:=', 'Global',
        'UDMId:=', '',
        'MaterialName:=', 'vacuum',
        'SolveInside:=', True
    ]
)
# Element: launch_pad_LP1_37
pts = ['NAME:PolylinePoints']
segs = ['NAME:PolylineSegments']
pts.append(['NAME:PLPoint', 'X:=', '-3.495000mm', 'Y:=', '4.000000mm', 'Z:=', '0.0mm'])
segs.append(['NAME:PLSegment', 'SegmentType:=', 'Line', 'StartIndex:=', 0, 'NoOfPoints:=', 2])
pts.append(['NAME:PLPoint', 'X:=', '-3.460000mm', 'Y:=', '4.122000mm', 'Z:=', '0.0mm'])
segs.append(['NAME:PLSegment', 'SegmentType:=', 'Line', 'StartIndex:=', 1, 'NoOfPoints:=', 2])
pts.append(['NAME:PLPoint', 'X:=', '-3.460000mm', 'Y:=', '4.202000mm', 'Z:=', '0.0mm'])
segs.append(['NAME:PLSegment', 'SegmentType:=', 'Line', 'StartIndex:=', 2, 'NoOfPoints:=', 2])
pts.append(['NAME:PLPoint', 'X:=', '-3.540000mm', 'Y:=', '4.202000mm', 'Z:=', '0.0mm'])
segs.append(['NAME:PLSegment', 'SegmentType:=', 'Line', 'StartIndex:=', 3, 'NoOfPoints:=', 2])
pts.append(['NAME:PLPoint', 'X:=', '-3.540000mm', 'Y:=', '4.122000mm', 'Z:=', '0.0mm'])
segs.append(['NAME:PLSegment', 'SegmentType:=', 'Line', 'StartIndex:=', 4, 'NoOfPoints:=', 2])
pts.append(['NAME:PLPoint', 'X:=', '-3.505000mm', 'Y:=', '4.000000mm', 'Z:=', '0.0mm'])
segs.append(['NAME:PLSegment', 'SegmentType:=', 'Line', 'StartIndex:=', 5, 'NoOfPoints:=', 2])
pts.append(['NAME:PLPoint', 'X:=', '-3.505000mm', 'Y:=', '3.975000mm', 'Z:=', '0.0mm'])
segs.append(['NAME:PLSegment', 'SegmentType:=', 'Line', 'StartIndex:=', 6, 'NoOfPoints:=', 2])
pts.append(['NAME:PLPoint', 'X:=', '-3.495000mm', 'Y:=', '3.975000mm', 'Z:=', '0.0mm'])
segs.append(['NAME:PLSegment', 'SegmentType:=', 'Line', 'StartIndex:=', 7, 'NoOfPoints:=', 2])
pts.append(['NAME:PLPoint', 'X:=', '-3.495000mm', 'Y:=', '4.000000mm', 'Z:=', '0.0mm'])
oEditor.CreatePolyline(
    ['NAME:PolylineParameters', 'IsPolylineCovered:=', True, 'IsPolylineClosed:=', True, pts, segs],
    [
        'NAME:Attributes',
        'Name:=', 'launch_pad_LP1_37',
        'Flags:=', '',
        'Color:=', '(200 220 255)',
        'Transparency:=', 0.0,
        'PartCoordinateSystem:=', 'Global',
        'UDMId:=', '',
        'MaterialName:=', 'vacuum',
        'SolveInside:=', True
    ]
)
# Element: pocket_LP1_38
pts = ['NAME:PolylinePoints']
segs = ['NAME:PolylineSegments']
pts.append(['NAME:PLPoint', 'X:=', '-3.489000mm', 'Y:=', '4.000000mm', 'Z:=', '0.0mm'])
segs.append(['NAME:PLSegment', 'SegmentType:=', 'Line', 'StartIndex:=', 0, 'NoOfPoints:=', 2])
pts.append(['NAME:PLPoint', 'X:=', '-3.402000mm', 'Y:=', '4.122000mm', 'Z:=', '0.0mm'])
segs.append(['NAME:PLSegment', 'SegmentType:=', 'Line', 'StartIndex:=', 1, 'NoOfPoints:=', 2])
pts.append(['NAME:PLPoint', 'X:=', '-3.402000mm', 'Y:=', '4.260000mm', 'Z:=', '0.0mm'])
segs.append(['NAME:PLSegment', 'SegmentType:=', 'Line', 'StartIndex:=', 2, 'NoOfPoints:=', 2])
pts.append(['NAME:PLPoint', 'X:=', '-3.598000mm', 'Y:=', '4.260000mm', 'Z:=', '0.0mm'])
segs.append(['NAME:PLSegment', 'SegmentType:=', 'Line', 'StartIndex:=', 3, 'NoOfPoints:=', 2])
pts.append(['NAME:PLPoint', 'X:=', '-3.598000mm', 'Y:=', '4.122000mm', 'Z:=', '0.0mm'])
segs.append(['NAME:PLSegment', 'SegmentType:=', 'Line', 'StartIndex:=', 4, 'NoOfPoints:=', 2])
pts.append(['NAME:PLPoint', 'X:=', '-3.511000mm', 'Y:=', '4.000000mm', 'Z:=', '0.0mm'])
segs.append(['NAME:PLSegment', 'SegmentType:=', 'Line', 'StartIndex:=', 5, 'NoOfPoints:=', 2])
pts.append(['NAME:PLPoint', 'X:=', '-3.511000mm', 'Y:=', '3.975000mm', 'Z:=', '0.0mm'])
segs.append(['NAME:PLSegment', 'SegmentType:=', 'Line', 'StartIndex:=', 6, 'NoOfPoints:=', 2])
pts.append(['NAME:PLPoint', 'X:=', '-3.489000mm', 'Y:=', '3.975000mm', 'Z:=', '0.0mm'])
segs.append(['NAME:PLSegment', 'SegmentType:=', 'Line', 'StartIndex:=', 7, 'NoOfPoints:=', 2])
pts.append(['NAME:PLPoint', 'X:=', '-3.489000mm', 'Y:=', '4.000000mm', 'Z:=', '0.0mm'])
oEditor.CreatePolyline(
    ['NAME:PolylineParameters', 'IsPolylineCovered:=', True, 'IsPolylineClosed:=', True, pts, segs],
    [
        'NAME:Attributes',
        'Name:=', 'pocket_LP1_38',
        'Flags:=', '',
        'Color:=', '(255 100 100)',
        'Transparency:=', 0.0,
        'PartCoordinateSystem:=', 'Global',
        'UDMId:=', '',
        'MaterialName:=', 'vacuum',
        'SolveInside:=', True
    ]
)
# Element: launch_pad_LP2_39
pts = ['NAME:PolylinePoints']
segs = ['NAME:PolylineSegments']
pts.append(['NAME:PLPoint', 'X:=', '-1.195000mm', 'Y:=', '4.000000mm', 'Z:=', '0.0mm'])
segs.append(['NAME:PLSegment', 'SegmentType:=', 'Line', 'StartIndex:=', 0, 'NoOfPoints:=', 2])
pts.append(['NAME:PLPoint', 'X:=', '-1.160000mm', 'Y:=', '4.122000mm', 'Z:=', '0.0mm'])
segs.append(['NAME:PLSegment', 'SegmentType:=', 'Line', 'StartIndex:=', 1, 'NoOfPoints:=', 2])
pts.append(['NAME:PLPoint', 'X:=', '-1.160000mm', 'Y:=', '4.202000mm', 'Z:=', '0.0mm'])
segs.append(['NAME:PLSegment', 'SegmentType:=', 'Line', 'StartIndex:=', 2, 'NoOfPoints:=', 2])
pts.append(['NAME:PLPoint', 'X:=', '-1.240000mm', 'Y:=', '4.202000mm', 'Z:=', '0.0mm'])
segs.append(['NAME:PLSegment', 'SegmentType:=', 'Line', 'StartIndex:=', 3, 'NoOfPoints:=', 2])
pts.append(['NAME:PLPoint', 'X:=', '-1.240000mm', 'Y:=', '4.122000mm', 'Z:=', '0.0mm'])
segs.append(['NAME:PLSegment', 'SegmentType:=', 'Line', 'StartIndex:=', 4, 'NoOfPoints:=', 2])
pts.append(['NAME:PLPoint', 'X:=', '-1.205000mm', 'Y:=', '4.000000mm', 'Z:=', '0.0mm'])
segs.append(['NAME:PLSegment', 'SegmentType:=', 'Line', 'StartIndex:=', 5, 'NoOfPoints:=', 2])
pts.append(['NAME:PLPoint', 'X:=', '-1.205000mm', 'Y:=', '3.975000mm', 'Z:=', '0.0mm'])
segs.append(['NAME:PLSegment', 'SegmentType:=', 'Line', 'StartIndex:=', 6, 'NoOfPoints:=', 2])
pts.append(['NAME:PLPoint', 'X:=', '-1.195000mm', 'Y:=', '3.975000mm', 'Z:=', '0.0mm'])
segs.append(['NAME:PLSegment', 'SegmentType:=', 'Line', 'StartIndex:=', 7, 'NoOfPoints:=', 2])
pts.append(['NAME:PLPoint', 'X:=', '-1.195000mm', 'Y:=', '4.000000mm', 'Z:=', '0.0mm'])
oEditor.CreatePolyline(
    ['NAME:PolylineParameters', 'IsPolylineCovered:=', True, 'IsPolylineClosed:=', True, pts, segs],
    [
        'NAME:Attributes',
        'Name:=', 'launch_pad_LP2_39',
        'Flags:=', '',
        'Color:=', '(200 220 255)',
        'Transparency:=', 0.0,
        'PartCoordinateSystem:=', 'Global',
        'UDMId:=', '',
        'MaterialName:=', 'vacuum',
        'SolveInside:=', True
    ]
)
# Element: pocket_LP2_40
pts = ['NAME:PolylinePoints']
segs = ['NAME:PolylineSegments']
pts.append(['NAME:PLPoint', 'X:=', '-1.189000mm', 'Y:=', '4.000000mm', 'Z:=', '0.0mm'])
segs.append(['NAME:PLSegment', 'SegmentType:=', 'Line', 'StartIndex:=', 0, 'NoOfPoints:=', 2])
pts.append(['NAME:PLPoint', 'X:=', '-1.102000mm', 'Y:=', '4.122000mm', 'Z:=', '0.0mm'])
segs.append(['NAME:PLSegment', 'SegmentType:=', 'Line', 'StartIndex:=', 1, 'NoOfPoints:=', 2])
pts.append(['NAME:PLPoint', 'X:=', '-1.102000mm', 'Y:=', '4.260000mm', 'Z:=', '0.0mm'])
segs.append(['NAME:PLSegment', 'SegmentType:=', 'Line', 'StartIndex:=', 2, 'NoOfPoints:=', 2])
pts.append(['NAME:PLPoint', 'X:=', '-1.298000mm', 'Y:=', '4.260000mm', 'Z:=', '0.0mm'])
segs.append(['NAME:PLSegment', 'SegmentType:=', 'Line', 'StartIndex:=', 3, 'NoOfPoints:=', 2])
pts.append(['NAME:PLPoint', 'X:=', '-1.298000mm', 'Y:=', '4.122000mm', 'Z:=', '0.0mm'])
segs.append(['NAME:PLSegment', 'SegmentType:=', 'Line', 'StartIndex:=', 4, 'NoOfPoints:=', 2])
pts.append(['NAME:PLPoint', 'X:=', '-1.211000mm', 'Y:=', '4.000000mm', 'Z:=', '0.0mm'])
segs.append(['NAME:PLSegment', 'SegmentType:=', 'Line', 'StartIndex:=', 5, 'NoOfPoints:=', 2])
pts.append(['NAME:PLPoint', 'X:=', '-1.211000mm', 'Y:=', '3.975000mm', 'Z:=', '0.0mm'])
segs.append(['NAME:PLSegment', 'SegmentType:=', 'Line', 'StartIndex:=', 6, 'NoOfPoints:=', 2])
pts.append(['NAME:PLPoint', 'X:=', '-1.189000mm', 'Y:=', '3.975000mm', 'Z:=', '0.0mm'])
segs.append(['NAME:PLSegment', 'SegmentType:=', 'Line', 'StartIndex:=', 7, 'NoOfPoints:=', 2])
pts.append(['NAME:PLPoint', 'X:=', '-1.189000mm', 'Y:=', '4.000000mm', 'Z:=', '0.0mm'])
oEditor.CreatePolyline(
    ['NAME:PolylineParameters', 'IsPolylineCovered:=', True, 'IsPolylineClosed:=', True, pts, segs],
    [
        'NAME:Attributes',
        'Name:=', 'pocket_LP2_40',
        'Flags:=', '',
        'Color:=', '(255 100 100)',
        'Transparency:=', 0.0,
        'PartCoordinateSystem:=', 'Global',
        'UDMId:=', '',
        'MaterialName:=', 'vacuum',
        'SolveInside:=', True
    ]
)
# Element: launch_pad_LP3_41
pts = ['NAME:PolylinePoints']
segs = ['NAME:PolylineSegments']
pts.append(['NAME:PLPoint', 'X:=', '1.205000mm', 'Y:=', '4.000000mm', 'Z:=', '0.0mm'])
segs.append(['NAME:PLSegment', 'SegmentType:=', 'Line', 'StartIndex:=', 0, 'NoOfPoints:=', 2])
pts.append(['NAME:PLPoint', 'X:=', '1.240000mm', 'Y:=', '4.122000mm', 'Z:=', '0.0mm'])
segs.append(['NAME:PLSegment', 'SegmentType:=', 'Line', 'StartIndex:=', 1, 'NoOfPoints:=', 2])
pts.append(['NAME:PLPoint', 'X:=', '1.240000mm', 'Y:=', '4.202000mm', 'Z:=', '0.0mm'])
segs.append(['NAME:PLSegment', 'SegmentType:=', 'Line', 'StartIndex:=', 2, 'NoOfPoints:=', 2])
pts.append(['NAME:PLPoint', 'X:=', '1.160000mm', 'Y:=', '4.202000mm', 'Z:=', '0.0mm'])
segs.append(['NAME:PLSegment', 'SegmentType:=', 'Line', 'StartIndex:=', 3, 'NoOfPoints:=', 2])
pts.append(['NAME:PLPoint', 'X:=', '1.160000mm', 'Y:=', '4.122000mm', 'Z:=', '0.0mm'])
segs.append(['NAME:PLSegment', 'SegmentType:=', 'Line', 'StartIndex:=', 4, 'NoOfPoints:=', 2])
pts.append(['NAME:PLPoint', 'X:=', '1.195000mm', 'Y:=', '4.000000mm', 'Z:=', '0.0mm'])
segs.append(['NAME:PLSegment', 'SegmentType:=', 'Line', 'StartIndex:=', 5, 'NoOfPoints:=', 2])
pts.append(['NAME:PLPoint', 'X:=', '1.195000mm', 'Y:=', '3.975000mm', 'Z:=', '0.0mm'])
segs.append(['NAME:PLSegment', 'SegmentType:=', 'Line', 'StartIndex:=', 6, 'NoOfPoints:=', 2])
pts.append(['NAME:PLPoint', 'X:=', '1.205000mm', 'Y:=', '3.975000mm', 'Z:=', '0.0mm'])
segs.append(['NAME:PLSegment', 'SegmentType:=', 'Line', 'StartIndex:=', 7, 'NoOfPoints:=', 2])
pts.append(['NAME:PLPoint', 'X:=', '1.205000mm', 'Y:=', '4.000000mm', 'Z:=', '0.0mm'])
oEditor.CreatePolyline(
    ['NAME:PolylineParameters', 'IsPolylineCovered:=', True, 'IsPolylineClosed:=', True, pts, segs],
    [
        'NAME:Attributes',
        'Name:=', 'launch_pad_LP3_41',
        'Flags:=', '',
        'Color:=', '(200 220 255)',
        'Transparency:=', 0.0,
        'PartCoordinateSystem:=', 'Global',
        'UDMId:=', '',
        'MaterialName:=', 'vacuum',
        'SolveInside:=', True
    ]
)
# Element: pocket_LP3_42
pts = ['NAME:PolylinePoints']
segs = ['NAME:PolylineSegments']
pts.append(['NAME:PLPoint', 'X:=', '1.211000mm', 'Y:=', '4.000000mm', 'Z:=', '0.0mm'])
segs.append(['NAME:PLSegment', 'SegmentType:=', 'Line', 'StartIndex:=', 0, 'NoOfPoints:=', 2])
pts.append(['NAME:PLPoint', 'X:=', '1.298000mm', 'Y:=', '4.122000mm', 'Z:=', '0.0mm'])
segs.append(['NAME:PLSegment', 'SegmentType:=', 'Line', 'StartIndex:=', 1, 'NoOfPoints:=', 2])
pts.append(['NAME:PLPoint', 'X:=', '1.298000mm', 'Y:=', '4.260000mm', 'Z:=', '0.0mm'])
segs.append(['NAME:PLSegment', 'SegmentType:=', 'Line', 'StartIndex:=', 2, 'NoOfPoints:=', 2])
pts.append(['NAME:PLPoint', 'X:=', '1.102000mm', 'Y:=', '4.260000mm', 'Z:=', '0.0mm'])
segs.append(['NAME:PLSegment', 'SegmentType:=', 'Line', 'StartIndex:=', 3, 'NoOfPoints:=', 2])
pts.append(['NAME:PLPoint', 'X:=', '1.102000mm', 'Y:=', '4.122000mm', 'Z:=', '0.0mm'])
segs.append(['NAME:PLSegment', 'SegmentType:=', 'Line', 'StartIndex:=', 4, 'NoOfPoints:=', 2])
pts.append(['NAME:PLPoint', 'X:=', '1.189000mm', 'Y:=', '4.000000mm', 'Z:=', '0.0mm'])
segs.append(['NAME:PLSegment', 'SegmentType:=', 'Line', 'StartIndex:=', 5, 'NoOfPoints:=', 2])
pts.append(['NAME:PLPoint', 'X:=', '1.189000mm', 'Y:=', '3.975000mm', 'Z:=', '0.0mm'])
segs.append(['NAME:PLSegment', 'SegmentType:=', 'Line', 'StartIndex:=', 6, 'NoOfPoints:=', 2])
pts.append(['NAME:PLPoint', 'X:=', '1.211000mm', 'Y:=', '3.975000mm', 'Z:=', '0.0mm'])
segs.append(['NAME:PLSegment', 'SegmentType:=', 'Line', 'StartIndex:=', 7, 'NoOfPoints:=', 2])
pts.append(['NAME:PLPoint', 'X:=', '1.211000mm', 'Y:=', '4.000000mm', 'Z:=', '0.0mm'])
oEditor.CreatePolyline(
    ['NAME:PolylineParameters', 'IsPolylineCovered:=', True, 'IsPolylineClosed:=', True, pts, segs],
    [
        'NAME:Attributes',
        'Name:=', 'pocket_LP3_42',
        'Flags:=', '',
        'Color:=', '(255 100 100)',
        'Transparency:=', 0.0,
        'PartCoordinateSystem:=', 'Global',
        'UDMId:=', '',
        'MaterialName:=', 'vacuum',
        'SolveInside:=', True
    ]
)
# Element: launch_pad_LP4_43
pts = ['NAME:PolylinePoints']
segs = ['NAME:PolylineSegments']
pts.append(['NAME:PLPoint', 'X:=', '3.505000mm', 'Y:=', '4.000000mm', 'Z:=', '0.0mm'])
segs.append(['NAME:PLSegment', 'SegmentType:=', 'Line', 'StartIndex:=', 0, 'NoOfPoints:=', 2])
pts.append(['NAME:PLPoint', 'X:=', '3.540000mm', 'Y:=', '4.122000mm', 'Z:=', '0.0mm'])
segs.append(['NAME:PLSegment', 'SegmentType:=', 'Line', 'StartIndex:=', 1, 'NoOfPoints:=', 2])
pts.append(['NAME:PLPoint', 'X:=', '3.540000mm', 'Y:=', '4.202000mm', 'Z:=', '0.0mm'])
segs.append(['NAME:PLSegment', 'SegmentType:=', 'Line', 'StartIndex:=', 2, 'NoOfPoints:=', 2])
pts.append(['NAME:PLPoint', 'X:=', '3.460000mm', 'Y:=', '4.202000mm', 'Z:=', '0.0mm'])
segs.append(['NAME:PLSegment', 'SegmentType:=', 'Line', 'StartIndex:=', 3, 'NoOfPoints:=', 2])
pts.append(['NAME:PLPoint', 'X:=', '3.460000mm', 'Y:=', '4.122000mm', 'Z:=', '0.0mm'])
segs.append(['NAME:PLSegment', 'SegmentType:=', 'Line', 'StartIndex:=', 4, 'NoOfPoints:=', 2])
pts.append(['NAME:PLPoint', 'X:=', '3.495000mm', 'Y:=', '4.000000mm', 'Z:=', '0.0mm'])
segs.append(['NAME:PLSegment', 'SegmentType:=', 'Line', 'StartIndex:=', 5, 'NoOfPoints:=', 2])
pts.append(['NAME:PLPoint', 'X:=', '3.495000mm', 'Y:=', '3.975000mm', 'Z:=', '0.0mm'])
segs.append(['NAME:PLSegment', 'SegmentType:=', 'Line', 'StartIndex:=', 6, 'NoOfPoints:=', 2])
pts.append(['NAME:PLPoint', 'X:=', '3.505000mm', 'Y:=', '3.975000mm', 'Z:=', '0.0mm'])
segs.append(['NAME:PLSegment', 'SegmentType:=', 'Line', 'StartIndex:=', 7, 'NoOfPoints:=', 2])
pts.append(['NAME:PLPoint', 'X:=', '3.505000mm', 'Y:=', '4.000000mm', 'Z:=', '0.0mm'])
oEditor.CreatePolyline(
    ['NAME:PolylineParameters', 'IsPolylineCovered:=', True, 'IsPolylineClosed:=', True, pts, segs],
    [
        'NAME:Attributes',
        'Name:=', 'launch_pad_LP4_43',
        'Flags:=', '',
        'Color:=', '(200 220 255)',
        'Transparency:=', 0.0,
        'PartCoordinateSystem:=', 'Global',
        'UDMId:=', '',
        'MaterialName:=', 'vacuum',
        'SolveInside:=', True
    ]
)
# Element: pocket_LP4_44
pts = ['NAME:PolylinePoints']
segs = ['NAME:PolylineSegments']
pts.append(['NAME:PLPoint', 'X:=', '3.511000mm', 'Y:=', '4.000000mm', 'Z:=', '0.0mm'])
segs.append(['NAME:PLSegment', 'SegmentType:=', 'Line', 'StartIndex:=', 0, 'NoOfPoints:=', 2])
pts.append(['NAME:PLPoint', 'X:=', '3.598000mm', 'Y:=', '4.122000mm', 'Z:=', '0.0mm'])
segs.append(['NAME:PLSegment', 'SegmentType:=', 'Line', 'StartIndex:=', 1, 'NoOfPoints:=', 2])
pts.append(['NAME:PLPoint', 'X:=', '3.598000mm', 'Y:=', '4.260000mm', 'Z:=', '0.0mm'])
segs.append(['NAME:PLSegment', 'SegmentType:=', 'Line', 'StartIndex:=', 2, 'NoOfPoints:=', 2])
pts.append(['NAME:PLPoint', 'X:=', '3.402000mm', 'Y:=', '4.260000mm', 'Z:=', '0.0mm'])
segs.append(['NAME:PLSegment', 'SegmentType:=', 'Line', 'StartIndex:=', 3, 'NoOfPoints:=', 2])
pts.append(['NAME:PLPoint', 'X:=', '3.402000mm', 'Y:=', '4.122000mm', 'Z:=', '0.0mm'])
segs.append(['NAME:PLSegment', 'SegmentType:=', 'Line', 'StartIndex:=', 4, 'NoOfPoints:=', 2])
pts.append(['NAME:PLPoint', 'X:=', '3.489000mm', 'Y:=', '4.000000mm', 'Z:=', '0.0mm'])
segs.append(['NAME:PLSegment', 'SegmentType:=', 'Line', 'StartIndex:=', 5, 'NoOfPoints:=', 2])
pts.append(['NAME:PLPoint', 'X:=', '3.489000mm', 'Y:=', '3.975000mm', 'Z:=', '0.0mm'])
segs.append(['NAME:PLSegment', 'SegmentType:=', 'Line', 'StartIndex:=', 6, 'NoOfPoints:=', 2])
pts.append(['NAME:PLPoint', 'X:=', '3.511000mm', 'Y:=', '3.975000mm', 'Z:=', '0.0mm'])
segs.append(['NAME:PLSegment', 'SegmentType:=', 'Line', 'StartIndex:=', 7, 'NoOfPoints:=', 2])
pts.append(['NAME:PLPoint', 'X:=', '3.511000mm', 'Y:=', '4.000000mm', 'Z:=', '0.0mm'])
oEditor.CreatePolyline(
    ['NAME:PolylineParameters', 'IsPolylineCovered:=', True, 'IsPolylineClosed:=', True, pts, segs],
    [
        'NAME:Attributes',
        'Name:=', 'pocket_LP4_44',
        'Flags:=', '',
        'Color:=', '(255 100 100)',
        'Transparency:=', 0.0,
        'PartCoordinateSystem:=', 'Global',
        'UDMId:=', '',
        'MaterialName:=', 'vacuum',
        'SolveInside:=', True
    ]
)
# Element: launch_pad_LP5_45
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
        'Name:=', 'launch_pad_LP5_45',
        'Flags:=', '',
        'Color:=', '(200 220 255)',
        'Transparency:=', 0.0,
        'PartCoordinateSystem:=', 'Global',
        'UDMId:=', '',
        'MaterialName:=', 'vacuum',
        'SolveInside:=', True
    ]
)
# Element: pocket_LP5_46
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
        'Name:=', 'pocket_LP5_46',
        'Flags:=', '',
        'Color:=', '(255 100 100)',
        'Transparency:=', 0.0,
        'PartCoordinateSystem:=', 'Global',
        'UDMId:=', '',
        'MaterialName:=', 'vacuum',
        'SolveInside:=', True
    ]
)
# Element: launch_pad_LP6_47
pts = ['NAME:PolylinePoints']
segs = ['NAME:PolylineSegments']
pts.append(['NAME:PLPoint', 'X:=', '-0.005000mm', 'Y:=', '-2.000000mm', 'Z:=', '0.0mm'])
segs.append(['NAME:PLSegment', 'SegmentType:=', 'Line', 'StartIndex:=', 0, 'NoOfPoints:=', 2])
pts.append(['NAME:PLPoint', 'X:=', '-0.040000mm', 'Y:=', '-2.122000mm', 'Z:=', '0.0mm'])
segs.append(['NAME:PLSegment', 'SegmentType:=', 'Line', 'StartIndex:=', 1, 'NoOfPoints:=', 2])
pts.append(['NAME:PLPoint', 'X:=', '-0.040000mm', 'Y:=', '-2.202000mm', 'Z:=', '0.0mm'])
segs.append(['NAME:PLSegment', 'SegmentType:=', 'Line', 'StartIndex:=', 2, 'NoOfPoints:=', 2])
pts.append(['NAME:PLPoint', 'X:=', '0.040000mm', 'Y:=', '-2.202000mm', 'Z:=', '0.0mm'])
segs.append(['NAME:PLSegment', 'SegmentType:=', 'Line', 'StartIndex:=', 3, 'NoOfPoints:=', 2])
pts.append(['NAME:PLPoint', 'X:=', '0.040000mm', 'Y:=', '-2.122000mm', 'Z:=', '0.0mm'])
segs.append(['NAME:PLSegment', 'SegmentType:=', 'Line', 'StartIndex:=', 4, 'NoOfPoints:=', 2])
pts.append(['NAME:PLPoint', 'X:=', '0.005000mm', 'Y:=', '-2.000000mm', 'Z:=', '0.0mm'])
segs.append(['NAME:PLSegment', 'SegmentType:=', 'Line', 'StartIndex:=', 5, 'NoOfPoints:=', 2])
pts.append(['NAME:PLPoint', 'X:=', '0.005000mm', 'Y:=', '-1.975000mm', 'Z:=', '0.0mm'])
segs.append(['NAME:PLSegment', 'SegmentType:=', 'Line', 'StartIndex:=', 6, 'NoOfPoints:=', 2])
pts.append(['NAME:PLPoint', 'X:=', '-0.005000mm', 'Y:=', '-1.975000mm', 'Z:=', '0.0mm'])
segs.append(['NAME:PLSegment', 'SegmentType:=', 'Line', 'StartIndex:=', 7, 'NoOfPoints:=', 2])
pts.append(['NAME:PLPoint', 'X:=', '-0.005000mm', 'Y:=', '-2.000000mm', 'Z:=', '0.0mm'])
oEditor.CreatePolyline(
    ['NAME:PolylineParameters', 'IsPolylineCovered:=', True, 'IsPolylineClosed:=', True, pts, segs],
    [
        'NAME:Attributes',
        'Name:=', 'launch_pad_LP6_47',
        'Flags:=', '',
        'Color:=', '(200 220 255)',
        'Transparency:=', 0.0,
        'PartCoordinateSystem:=', 'Global',
        'UDMId:=', '',
        'MaterialName:=', 'vacuum',
        'SolveInside:=', True
    ]
)
# Element: pocket_LP6_48
pts = ['NAME:PolylinePoints']
segs = ['NAME:PolylineSegments']
pts.append(['NAME:PLPoint', 'X:=', '-0.011000mm', 'Y:=', '-2.000000mm', 'Z:=', '0.0mm'])
segs.append(['NAME:PLSegment', 'SegmentType:=', 'Line', 'StartIndex:=', 0, 'NoOfPoints:=', 2])
pts.append(['NAME:PLPoint', 'X:=', '-0.098000mm', 'Y:=', '-2.122000mm', 'Z:=', '0.0mm'])
segs.append(['NAME:PLSegment', 'SegmentType:=', 'Line', 'StartIndex:=', 1, 'NoOfPoints:=', 2])
pts.append(['NAME:PLPoint', 'X:=', '-0.098000mm', 'Y:=', '-2.260000mm', 'Z:=', '0.0mm'])
segs.append(['NAME:PLSegment', 'SegmentType:=', 'Line', 'StartIndex:=', 2, 'NoOfPoints:=', 2])
pts.append(['NAME:PLPoint', 'X:=', '0.098000mm', 'Y:=', '-2.260000mm', 'Z:=', '0.0mm'])
segs.append(['NAME:PLSegment', 'SegmentType:=', 'Line', 'StartIndex:=', 3, 'NoOfPoints:=', 2])
pts.append(['NAME:PLPoint', 'X:=', '0.098000mm', 'Y:=', '-2.122000mm', 'Z:=', '0.0mm'])
segs.append(['NAME:PLSegment', 'SegmentType:=', 'Line', 'StartIndex:=', 4, 'NoOfPoints:=', 2])
pts.append(['NAME:PLPoint', 'X:=', '0.011000mm', 'Y:=', '-2.000000mm', 'Z:=', '0.0mm'])
segs.append(['NAME:PLSegment', 'SegmentType:=', 'Line', 'StartIndex:=', 5, 'NoOfPoints:=', 2])
pts.append(['NAME:PLPoint', 'X:=', '0.011000mm', 'Y:=', '-1.975000mm', 'Z:=', '0.0mm'])
segs.append(['NAME:PLSegment', 'SegmentType:=', 'Line', 'StartIndex:=', 6, 'NoOfPoints:=', 2])
pts.append(['NAME:PLPoint', 'X:=', '-0.011000mm', 'Y:=', '-1.975000mm', 'Z:=', '0.0mm'])
segs.append(['NAME:PLSegment', 'SegmentType:=', 'Line', 'StartIndex:=', 7, 'NoOfPoints:=', 2])
pts.append(['NAME:PLPoint', 'X:=', '-0.011000mm', 'Y:=', '-2.000000mm', 'Z:=', '0.0mm'])
oEditor.CreatePolyline(
    ['NAME:PolylineParameters', 'IsPolylineCovered:=', True, 'IsPolylineClosed:=', True, pts, segs],
    [
        'NAME:Attributes',
        'Name:=', 'pocket_LP6_48',
        'Flags:=', '',
        'Color:=', '(255 100 100)',
        'Transparency:=', 0.0,
        'PartCoordinateSystem:=', 'Global',
        'UDMId:=', '',
        'MaterialName:=', 'vacuum',
        'SolveInside:=', True
    ]
)
# Element: launch_pad_LP7_49
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
        'Name:=', 'launch_pad_LP7_49',
        'Flags:=', '',
        'Color:=', '(200 220 255)',
        'Transparency:=', 0.0,
        'PartCoordinateSystem:=', 'Global',
        'UDMId:=', '',
        'MaterialName:=', 'vacuum',
        'SolveInside:=', True
    ]
)
# Element: pocket_LP7_50
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
        'Name:=', 'pocket_LP7_50',
        'Flags:=', '',
        'Color:=', '(255 100 100)',
        'Transparency:=', 0.0,
        'PartCoordinateSystem:=', 'Global',
        'UDMId:=', '',
        'MaterialName:=', 'vacuum',
        'SolveInside:=', True
    ]
)

# --- 4. Readout Resonators & Couplers ---
# Element: a_wire_Q1_0
pts = ['NAME:PolylinePoints']
segs = ['NAME:PolylineSegments']
pts.append(['NAME:PLPoint', 'X:=', '-2.925000mm', 'Y:=', '1.995000mm', 'Z:=', '0.0mm'])
segs.append(['NAME:PLSegment', 'SegmentType:=', 'Line', 'StartIndex:=', 0, 'NoOfPoints:=', 2])
pts.append(['NAME:PLPoint', 'X:=', '-2.925000mm', 'Y:=', '2.005000mm', 'Z:=', '0.0mm'])
segs.append(['NAME:PLSegment', 'SegmentType:=', 'Line', 'StartIndex:=', 1, 'NoOfPoints:=', 2])
pts.append(['NAME:PLPoint', 'X:=', '-2.650000mm', 'Y:=', '2.005000mm', 'Z:=', '0.0mm'])
segs.append(['NAME:PLSegment', 'SegmentType:=', 'Line', 'StartIndex:=', 2, 'NoOfPoints:=', 2])
pts.append(['NAME:PLPoint', 'X:=', '-2.650000mm', 'Y:=', '1.995000mm', 'Z:=', '0.0mm'])
segs.append(['NAME:PLSegment', 'SegmentType:=', 'Line', 'StartIndex:=', 3, 'NoOfPoints:=', 2])
pts.append(['NAME:PLPoint', 'X:=', '-2.925000mm', 'Y:=', '1.995000mm', 'Z:=', '0.0mm'])
oEditor.CreatePolyline(
    ['NAME:PolylineParameters', 'IsPolylineCovered:=', True, 'IsPolylineClosed:=', True, pts, segs],
    [
        'NAME:Attributes',
        'Name:=', 'a_wire_Q1_0',
        'Flags:=', '',
        'Color:=', '(200 220 255)',
        'Transparency:=', 0.0,
        'PartCoordinateSystem:=', 'Global',
        'UDMId:=', '',
        'MaterialName:=', 'vacuum',
        'SolveInside:=', True
    ]
)
# Element: a_wire_sub_Q1_1
pts = ['NAME:PolylinePoints']
segs = ['NAME:PolylineSegments']
pts.append(['NAME:PLPoint', 'X:=', '-2.925000mm', 'Y:=', '1.989000mm', 'Z:=', '0.0mm'])
segs.append(['NAME:PLSegment', 'SegmentType:=', 'Line', 'StartIndex:=', 0, 'NoOfPoints:=', 2])
pts.append(['NAME:PLPoint', 'X:=', '-2.925000mm', 'Y:=', '2.011000mm', 'Z:=', '0.0mm'])
segs.append(['NAME:PLSegment', 'SegmentType:=', 'Line', 'StartIndex:=', 1, 'NoOfPoints:=', 2])
pts.append(['NAME:PLPoint', 'X:=', '-2.650000mm', 'Y:=', '2.011000mm', 'Z:=', '0.0mm'])
segs.append(['NAME:PLSegment', 'SegmentType:=', 'Line', 'StartIndex:=', 2, 'NoOfPoints:=', 2])
pts.append(['NAME:PLPoint', 'X:=', '-2.650000mm', 'Y:=', '1.989000mm', 'Z:=', '0.0mm'])
segs.append(['NAME:PLSegment', 'SegmentType:=', 'Line', 'StartIndex:=', 3, 'NoOfPoints:=', 2])
pts.append(['NAME:PLPoint', 'X:=', '-2.925000mm', 'Y:=', '1.989000mm', 'Z:=', '0.0mm'])
oEditor.CreatePolyline(
    ['NAME:PolylineParameters', 'IsPolylineCovered:=', True, 'IsPolylineClosed:=', True, pts, segs],
    [
        'NAME:Attributes',
        'Name:=', 'a_wire_sub_Q1_1',
        'Flags:=', '',
        'Color:=', '(255 100 100)',
        'Transparency:=', 0.0,
        'PartCoordinateSystem:=', 'Global',
        'UDMId:=', '',
        'MaterialName:=', 'vacuum',
        'SolveInside:=', True
    ]
)
# Element: b_wire_Q1_2
pts = ['NAME:PolylinePoints']
segs = ['NAME:PolylineSegments']
pts.append(['NAME:PLPoint', 'X:=', '-2.075000mm', 'Y:=', '2.005000mm', 'Z:=', '0.0mm'])
segs.append(['NAME:PLSegment', 'SegmentType:=', 'Line', 'StartIndex:=', 0, 'NoOfPoints:=', 2])
pts.append(['NAME:PLPoint', 'X:=', '-2.075000mm', 'Y:=', '1.995000mm', 'Z:=', '0.0mm'])
segs.append(['NAME:PLSegment', 'SegmentType:=', 'Line', 'StartIndex:=', 1, 'NoOfPoints:=', 2])
pts.append(['NAME:PLPoint', 'X:=', '-2.350000mm', 'Y:=', '1.995000mm', 'Z:=', '0.0mm'])
segs.append(['NAME:PLSegment', 'SegmentType:=', 'Line', 'StartIndex:=', 2, 'NoOfPoints:=', 2])
pts.append(['NAME:PLPoint', 'X:=', '-2.350000mm', 'Y:=', '2.005000mm', 'Z:=', '0.0mm'])
segs.append(['NAME:PLSegment', 'SegmentType:=', 'Line', 'StartIndex:=', 3, 'NoOfPoints:=', 2])
pts.append(['NAME:PLPoint', 'X:=', '-2.075000mm', 'Y:=', '2.005000mm', 'Z:=', '0.0mm'])
oEditor.CreatePolyline(
    ['NAME:PolylineParameters', 'IsPolylineCovered:=', True, 'IsPolylineClosed:=', True, pts, segs],
    [
        'NAME:Attributes',
        'Name:=', 'b_wire_Q1_2',
        'Flags:=', '',
        'Color:=', '(200 220 255)',
        'Transparency:=', 0.0,
        'PartCoordinateSystem:=', 'Global',
        'UDMId:=', '',
        'MaterialName:=', 'vacuum',
        'SolveInside:=', True
    ]
)
# Element: b_wire_sub_Q1_3
pts = ['NAME:PolylinePoints']
segs = ['NAME:PolylineSegments']
pts.append(['NAME:PLPoint', 'X:=', '-2.075000mm', 'Y:=', '2.011000mm', 'Z:=', '0.0mm'])
segs.append(['NAME:PLSegment', 'SegmentType:=', 'Line', 'StartIndex:=', 0, 'NoOfPoints:=', 2])
pts.append(['NAME:PLPoint', 'X:=', '-2.075000mm', 'Y:=', '1.989000mm', 'Z:=', '0.0mm'])
segs.append(['NAME:PLSegment', 'SegmentType:=', 'Line', 'StartIndex:=', 1, 'NoOfPoints:=', 2])
pts.append(['NAME:PLPoint', 'X:=', '-2.350000mm', 'Y:=', '1.989000mm', 'Z:=', '0.0mm'])
segs.append(['NAME:PLSegment', 'SegmentType:=', 'Line', 'StartIndex:=', 2, 'NoOfPoints:=', 2])
pts.append(['NAME:PLPoint', 'X:=', '-2.350000mm', 'Y:=', '2.011000mm', 'Z:=', '0.0mm'])
segs.append(['NAME:PLSegment', 'SegmentType:=', 'Line', 'StartIndex:=', 3, 'NoOfPoints:=', 2])
pts.append(['NAME:PLPoint', 'X:=', '-2.075000mm', 'Y:=', '2.011000mm', 'Z:=', '0.0mm'])
oEditor.CreatePolyline(
    ['NAME:PolylineParameters', 'IsPolylineCovered:=', True, 'IsPolylineClosed:=', True, pts, segs],
    [
        'NAME:Attributes',
        'Name:=', 'b_wire_sub_Q1_3',
        'Flags:=', '',
        'Color:=', '(255 100 100)',
        'Transparency:=', 0.0,
        'PartCoordinateSystem:=', 'Global',
        'UDMId:=', '',
        'MaterialName:=', 'vacuum',
        'SolveInside:=', True
    ]
)
# Element: a_wire_Q2_4
pts = ['NAME:PolylinePoints']
segs = ['NAME:PolylineSegments']
pts.append(['NAME:PLPoint', 'X:=', '-0.425000mm', 'Y:=', '1.995000mm', 'Z:=', '0.0mm'])
segs.append(['NAME:PLSegment', 'SegmentType:=', 'Line', 'StartIndex:=', 0, 'NoOfPoints:=', 2])
pts.append(['NAME:PLPoint', 'X:=', '-0.425000mm', 'Y:=', '2.005000mm', 'Z:=', '0.0mm'])
segs.append(['NAME:PLSegment', 'SegmentType:=', 'Line', 'StartIndex:=', 1, 'NoOfPoints:=', 2])
pts.append(['NAME:PLPoint', 'X:=', '-0.150000mm', 'Y:=', '2.005000mm', 'Z:=', '0.0mm'])
segs.append(['NAME:PLSegment', 'SegmentType:=', 'Line', 'StartIndex:=', 2, 'NoOfPoints:=', 2])
pts.append(['NAME:PLPoint', 'X:=', '-0.150000mm', 'Y:=', '1.995000mm', 'Z:=', '0.0mm'])
segs.append(['NAME:PLSegment', 'SegmentType:=', 'Line', 'StartIndex:=', 3, 'NoOfPoints:=', 2])
pts.append(['NAME:PLPoint', 'X:=', '-0.425000mm', 'Y:=', '1.995000mm', 'Z:=', '0.0mm'])
oEditor.CreatePolyline(
    ['NAME:PolylineParameters', 'IsPolylineCovered:=', True, 'IsPolylineClosed:=', True, pts, segs],
    [
        'NAME:Attributes',
        'Name:=', 'a_wire_Q2_4',
        'Flags:=', '',
        'Color:=', '(200 220 255)',
        'Transparency:=', 0.0,
        'PartCoordinateSystem:=', 'Global',
        'UDMId:=', '',
        'MaterialName:=', 'vacuum',
        'SolveInside:=', True
    ]
)
# Element: a_wire_sub_Q2_5
pts = ['NAME:PolylinePoints']
segs = ['NAME:PolylineSegments']
pts.append(['NAME:PLPoint', 'X:=', '-0.425000mm', 'Y:=', '1.989000mm', 'Z:=', '0.0mm'])
segs.append(['NAME:PLSegment', 'SegmentType:=', 'Line', 'StartIndex:=', 0, 'NoOfPoints:=', 2])
pts.append(['NAME:PLPoint', 'X:=', '-0.425000mm', 'Y:=', '2.011000mm', 'Z:=', '0.0mm'])
segs.append(['NAME:PLSegment', 'SegmentType:=', 'Line', 'StartIndex:=', 1, 'NoOfPoints:=', 2])
pts.append(['NAME:PLPoint', 'X:=', '-0.150000mm', 'Y:=', '2.011000mm', 'Z:=', '0.0mm'])
segs.append(['NAME:PLSegment', 'SegmentType:=', 'Line', 'StartIndex:=', 2, 'NoOfPoints:=', 2])
pts.append(['NAME:PLPoint', 'X:=', '-0.150000mm', 'Y:=', '1.989000mm', 'Z:=', '0.0mm'])
segs.append(['NAME:PLSegment', 'SegmentType:=', 'Line', 'StartIndex:=', 3, 'NoOfPoints:=', 2])
pts.append(['NAME:PLPoint', 'X:=', '-0.425000mm', 'Y:=', '1.989000mm', 'Z:=', '0.0mm'])
oEditor.CreatePolyline(
    ['NAME:PolylineParameters', 'IsPolylineCovered:=', True, 'IsPolylineClosed:=', True, pts, segs],
    [
        'NAME:Attributes',
        'Name:=', 'a_wire_sub_Q2_5',
        'Flags:=', '',
        'Color:=', '(255 100 100)',
        'Transparency:=', 0.0,
        'PartCoordinateSystem:=', 'Global',
        'UDMId:=', '',
        'MaterialName:=', 'vacuum',
        'SolveInside:=', True
    ]
)
# Element: b_wire_Q2_6
pts = ['NAME:PolylinePoints']
segs = ['NAME:PolylineSegments']
pts.append(['NAME:PLPoint', 'X:=', '0.425000mm', 'Y:=', '2.005000mm', 'Z:=', '0.0mm'])
segs.append(['NAME:PLSegment', 'SegmentType:=', 'Line', 'StartIndex:=', 0, 'NoOfPoints:=', 2])
pts.append(['NAME:PLPoint', 'X:=', '0.425000mm', 'Y:=', '1.995000mm', 'Z:=', '0.0mm'])
segs.append(['NAME:PLSegment', 'SegmentType:=', 'Line', 'StartIndex:=', 1, 'NoOfPoints:=', 2])
pts.append(['NAME:PLPoint', 'X:=', '0.150000mm', 'Y:=', '1.995000mm', 'Z:=', '0.0mm'])
segs.append(['NAME:PLSegment', 'SegmentType:=', 'Line', 'StartIndex:=', 2, 'NoOfPoints:=', 2])
pts.append(['NAME:PLPoint', 'X:=', '0.150000mm', 'Y:=', '2.005000mm', 'Z:=', '0.0mm'])
segs.append(['NAME:PLSegment', 'SegmentType:=', 'Line', 'StartIndex:=', 3, 'NoOfPoints:=', 2])
pts.append(['NAME:PLPoint', 'X:=', '0.425000mm', 'Y:=', '2.005000mm', 'Z:=', '0.0mm'])
oEditor.CreatePolyline(
    ['NAME:PolylineParameters', 'IsPolylineCovered:=', True, 'IsPolylineClosed:=', True, pts, segs],
    [
        'NAME:Attributes',
        'Name:=', 'b_wire_Q2_6',
        'Flags:=', '',
        'Color:=', '(200 220 255)',
        'Transparency:=', 0.0,
        'PartCoordinateSystem:=', 'Global',
        'UDMId:=', '',
        'MaterialName:=', 'vacuum',
        'SolveInside:=', True
    ]
)
# Element: b_wire_sub_Q2_7
pts = ['NAME:PolylinePoints']
segs = ['NAME:PolylineSegments']
pts.append(['NAME:PLPoint', 'X:=', '0.425000mm', 'Y:=', '2.011000mm', 'Z:=', '0.0mm'])
segs.append(['NAME:PLSegment', 'SegmentType:=', 'Line', 'StartIndex:=', 0, 'NoOfPoints:=', 2])
pts.append(['NAME:PLPoint', 'X:=', '0.425000mm', 'Y:=', '1.989000mm', 'Z:=', '0.0mm'])
segs.append(['NAME:PLSegment', 'SegmentType:=', 'Line', 'StartIndex:=', 1, 'NoOfPoints:=', 2])
pts.append(['NAME:PLPoint', 'X:=', '0.150000mm', 'Y:=', '1.989000mm', 'Z:=', '0.0mm'])
segs.append(['NAME:PLSegment', 'SegmentType:=', 'Line', 'StartIndex:=', 2, 'NoOfPoints:=', 2])
pts.append(['NAME:PLPoint', 'X:=', '0.150000mm', 'Y:=', '2.011000mm', 'Z:=', '0.0mm'])
segs.append(['NAME:PLSegment', 'SegmentType:=', 'Line', 'StartIndex:=', 3, 'NoOfPoints:=', 2])
pts.append(['NAME:PLPoint', 'X:=', '0.425000mm', 'Y:=', '2.011000mm', 'Z:=', '0.0mm'])
oEditor.CreatePolyline(
    ['NAME:PolylineParameters', 'IsPolylineCovered:=', True, 'IsPolylineClosed:=', True, pts, segs],
    [
        'NAME:Attributes',
        'Name:=', 'b_wire_sub_Q2_7',
        'Flags:=', '',
        'Color:=', '(255 100 100)',
        'Transparency:=', 0.0,
        'PartCoordinateSystem:=', 'Global',
        'UDMId:=', '',
        'MaterialName:=', 'vacuum',
        'SolveInside:=', True
    ]
)
# Element: a_wire_Q3_8
pts = ['NAME:PolylinePoints']
segs = ['NAME:PolylineSegments']
pts.append(['NAME:PLPoint', 'X:=', '2.075000mm', 'Y:=', '1.995000mm', 'Z:=', '0.0mm'])
segs.append(['NAME:PLSegment', 'SegmentType:=', 'Line', 'StartIndex:=', 0, 'NoOfPoints:=', 2])
pts.append(['NAME:PLPoint', 'X:=', '2.075000mm', 'Y:=', '2.005000mm', 'Z:=', '0.0mm'])
segs.append(['NAME:PLSegment', 'SegmentType:=', 'Line', 'StartIndex:=', 1, 'NoOfPoints:=', 2])
pts.append(['NAME:PLPoint', 'X:=', '2.350000mm', 'Y:=', '2.005000mm', 'Z:=', '0.0mm'])
segs.append(['NAME:PLSegment', 'SegmentType:=', 'Line', 'StartIndex:=', 2, 'NoOfPoints:=', 2])
pts.append(['NAME:PLPoint', 'X:=', '2.350000mm', 'Y:=', '1.995000mm', 'Z:=', '0.0mm'])
segs.append(['NAME:PLSegment', 'SegmentType:=', 'Line', 'StartIndex:=', 3, 'NoOfPoints:=', 2])
pts.append(['NAME:PLPoint', 'X:=', '2.075000mm', 'Y:=', '1.995000mm', 'Z:=', '0.0mm'])
oEditor.CreatePolyline(
    ['NAME:PolylineParameters', 'IsPolylineCovered:=', True, 'IsPolylineClosed:=', True, pts, segs],
    [
        'NAME:Attributes',
        'Name:=', 'a_wire_Q3_8',
        'Flags:=', '',
        'Color:=', '(200 220 255)',
        'Transparency:=', 0.0,
        'PartCoordinateSystem:=', 'Global',
        'UDMId:=', '',
        'MaterialName:=', 'vacuum',
        'SolveInside:=', True
    ]
)
# Element: a_wire_sub_Q3_9
pts = ['NAME:PolylinePoints']
segs = ['NAME:PolylineSegments']
pts.append(['NAME:PLPoint', 'X:=', '2.075000mm', 'Y:=', '1.989000mm', 'Z:=', '0.0mm'])
segs.append(['NAME:PLSegment', 'SegmentType:=', 'Line', 'StartIndex:=', 0, 'NoOfPoints:=', 2])
pts.append(['NAME:PLPoint', 'X:=', '2.075000mm', 'Y:=', '2.011000mm', 'Z:=', '0.0mm'])
segs.append(['NAME:PLSegment', 'SegmentType:=', 'Line', 'StartIndex:=', 1, 'NoOfPoints:=', 2])
pts.append(['NAME:PLPoint', 'X:=', '2.350000mm', 'Y:=', '2.011000mm', 'Z:=', '0.0mm'])
segs.append(['NAME:PLSegment', 'SegmentType:=', 'Line', 'StartIndex:=', 2, 'NoOfPoints:=', 2])
pts.append(['NAME:PLPoint', 'X:=', '2.350000mm', 'Y:=', '1.989000mm', 'Z:=', '0.0mm'])
segs.append(['NAME:PLSegment', 'SegmentType:=', 'Line', 'StartIndex:=', 3, 'NoOfPoints:=', 2])
pts.append(['NAME:PLPoint', 'X:=', '2.075000mm', 'Y:=', '1.989000mm', 'Z:=', '0.0mm'])
oEditor.CreatePolyline(
    ['NAME:PolylineParameters', 'IsPolylineCovered:=', True, 'IsPolylineClosed:=', True, pts, segs],
    [
        'NAME:Attributes',
        'Name:=', 'a_wire_sub_Q3_9',
        'Flags:=', '',
        'Color:=', '(255 100 100)',
        'Transparency:=', 0.0,
        'PartCoordinateSystem:=', 'Global',
        'UDMId:=', '',
        'MaterialName:=', 'vacuum',
        'SolveInside:=', True
    ]
)
# Element: b_wire_Q3_10
pts = ['NAME:PolylinePoints']
segs = ['NAME:PolylineSegments']
pts.append(['NAME:PLPoint', 'X:=', '2.925000mm', 'Y:=', '2.005000mm', 'Z:=', '0.0mm'])
segs.append(['NAME:PLSegment', 'SegmentType:=', 'Line', 'StartIndex:=', 0, 'NoOfPoints:=', 2])
pts.append(['NAME:PLPoint', 'X:=', '2.925000mm', 'Y:=', '1.995000mm', 'Z:=', '0.0mm'])
segs.append(['NAME:PLSegment', 'SegmentType:=', 'Line', 'StartIndex:=', 1, 'NoOfPoints:=', 2])
pts.append(['NAME:PLPoint', 'X:=', '2.650000mm', 'Y:=', '1.995000mm', 'Z:=', '0.0mm'])
segs.append(['NAME:PLSegment', 'SegmentType:=', 'Line', 'StartIndex:=', 2, 'NoOfPoints:=', 2])
pts.append(['NAME:PLPoint', 'X:=', '2.650000mm', 'Y:=', '2.005000mm', 'Z:=', '0.0mm'])
segs.append(['NAME:PLSegment', 'SegmentType:=', 'Line', 'StartIndex:=', 3, 'NoOfPoints:=', 2])
pts.append(['NAME:PLPoint', 'X:=', '2.925000mm', 'Y:=', '2.005000mm', 'Z:=', '0.0mm'])
oEditor.CreatePolyline(
    ['NAME:PolylineParameters', 'IsPolylineCovered:=', True, 'IsPolylineClosed:=', True, pts, segs],
    [
        'NAME:Attributes',
        'Name:=', 'b_wire_Q3_10',
        'Flags:=', '',
        'Color:=', '(200 220 255)',
        'Transparency:=', 0.0,
        'PartCoordinateSystem:=', 'Global',
        'UDMId:=', '',
        'MaterialName:=', 'vacuum',
        'SolveInside:=', True
    ]
)
# Element: b_wire_sub_Q3_11
pts = ['NAME:PolylinePoints']
segs = ['NAME:PolylineSegments']
pts.append(['NAME:PLPoint', 'X:=', '2.925000mm', 'Y:=', '2.011000mm', 'Z:=', '0.0mm'])
segs.append(['NAME:PLSegment', 'SegmentType:=', 'Line', 'StartIndex:=', 0, 'NoOfPoints:=', 2])
pts.append(['NAME:PLPoint', 'X:=', '2.925000mm', 'Y:=', '1.989000mm', 'Z:=', '0.0mm'])
segs.append(['NAME:PLSegment', 'SegmentType:=', 'Line', 'StartIndex:=', 1, 'NoOfPoints:=', 2])
pts.append(['NAME:PLPoint', 'X:=', '2.650000mm', 'Y:=', '1.989000mm', 'Z:=', '0.0mm'])
segs.append(['NAME:PLSegment', 'SegmentType:=', 'Line', 'StartIndex:=', 2, 'NoOfPoints:=', 2])
pts.append(['NAME:PLPoint', 'X:=', '2.650000mm', 'Y:=', '2.011000mm', 'Z:=', '0.0mm'])
segs.append(['NAME:PLSegment', 'SegmentType:=', 'Line', 'StartIndex:=', 3, 'NoOfPoints:=', 2])
pts.append(['NAME:PLPoint', 'X:=', '2.925000mm', 'Y:=', '2.011000mm', 'Z:=', '0.0mm'])
oEditor.CreatePolyline(
    ['NAME:PolylineParameters', 'IsPolylineCovered:=', True, 'IsPolylineClosed:=', True, pts, segs],
    [
        'NAME:Attributes',
        'Name:=', 'b_wire_sub_Q3_11',
        'Flags:=', '',
        'Color:=', '(255 100 100)',
        'Transparency:=', 0.0,
        'PartCoordinateSystem:=', 'Global',
        'UDMId:=', '',
        'MaterialName:=', 'vacuum',
        'SolveInside:=', True
    ]
)
# Element: a_wire_Q5_12
pts = ['NAME:PolylinePoints']
segs = ['NAME:PolylineSegments']
pts.append(['NAME:PLPoint', 'X:=', '-2.925000mm', 'Y:=', '-0.005000mm', 'Z:=', '0.0mm'])
segs.append(['NAME:PLSegment', 'SegmentType:=', 'Line', 'StartIndex:=', 0, 'NoOfPoints:=', 2])
pts.append(['NAME:PLPoint', 'X:=', '-2.925000mm', 'Y:=', '0.005000mm', 'Z:=', '0.0mm'])
segs.append(['NAME:PLSegment', 'SegmentType:=', 'Line', 'StartIndex:=', 1, 'NoOfPoints:=', 2])
pts.append(['NAME:PLPoint', 'X:=', '-2.650000mm', 'Y:=', '0.005000mm', 'Z:=', '0.0mm'])
segs.append(['NAME:PLSegment', 'SegmentType:=', 'Line', 'StartIndex:=', 2, 'NoOfPoints:=', 2])
pts.append(['NAME:PLPoint', 'X:=', '-2.650000mm', 'Y:=', '-0.005000mm', 'Z:=', '0.0mm'])
segs.append(['NAME:PLSegment', 'SegmentType:=', 'Line', 'StartIndex:=', 3, 'NoOfPoints:=', 2])
pts.append(['NAME:PLPoint', 'X:=', '-2.925000mm', 'Y:=', '-0.005000mm', 'Z:=', '0.0mm'])
oEditor.CreatePolyline(
    ['NAME:PolylineParameters', 'IsPolylineCovered:=', True, 'IsPolylineClosed:=', True, pts, segs],
    [
        'NAME:Attributes',
        'Name:=', 'a_wire_Q5_12',
        'Flags:=', '',
        'Color:=', '(200 220 255)',
        'Transparency:=', 0.0,
        'PartCoordinateSystem:=', 'Global',
        'UDMId:=', '',
        'MaterialName:=', 'vacuum',
        'SolveInside:=', True
    ]
)
# Element: a_wire_sub_Q5_13
pts = ['NAME:PolylinePoints']
segs = ['NAME:PolylineSegments']
pts.append(['NAME:PLPoint', 'X:=', '-2.925000mm', 'Y:=', '-0.011000mm', 'Z:=', '0.0mm'])
segs.append(['NAME:PLSegment', 'SegmentType:=', 'Line', 'StartIndex:=', 0, 'NoOfPoints:=', 2])
pts.append(['NAME:PLPoint', 'X:=', '-2.925000mm', 'Y:=', '0.011000mm', 'Z:=', '0.0mm'])
segs.append(['NAME:PLSegment', 'SegmentType:=', 'Line', 'StartIndex:=', 1, 'NoOfPoints:=', 2])
pts.append(['NAME:PLPoint', 'X:=', '-2.650000mm', 'Y:=', '0.011000mm', 'Z:=', '0.0mm'])
segs.append(['NAME:PLSegment', 'SegmentType:=', 'Line', 'StartIndex:=', 2, 'NoOfPoints:=', 2])
pts.append(['NAME:PLPoint', 'X:=', '-2.650000mm', 'Y:=', '-0.011000mm', 'Z:=', '0.0mm'])
segs.append(['NAME:PLSegment', 'SegmentType:=', 'Line', 'StartIndex:=', 3, 'NoOfPoints:=', 2])
pts.append(['NAME:PLPoint', 'X:=', '-2.925000mm', 'Y:=', '-0.011000mm', 'Z:=', '0.0mm'])
oEditor.CreatePolyline(
    ['NAME:PolylineParameters', 'IsPolylineCovered:=', True, 'IsPolylineClosed:=', True, pts, segs],
    [
        'NAME:Attributes',
        'Name:=', 'a_wire_sub_Q5_13',
        'Flags:=', '',
        'Color:=', '(255 100 100)',
        'Transparency:=', 0.0,
        'PartCoordinateSystem:=', 'Global',
        'UDMId:=', '',
        'MaterialName:=', 'vacuum',
        'SolveInside:=', True
    ]
)
# Element: b_wire_Q5_14
pts = ['NAME:PolylinePoints']
segs = ['NAME:PolylineSegments']
pts.append(['NAME:PLPoint', 'X:=', '-2.075000mm', 'Y:=', '0.005000mm', 'Z:=', '0.0mm'])
segs.append(['NAME:PLSegment', 'SegmentType:=', 'Line', 'StartIndex:=', 0, 'NoOfPoints:=', 2])
pts.append(['NAME:PLPoint', 'X:=', '-2.075000mm', 'Y:=', '-0.005000mm', 'Z:=', '0.0mm'])
segs.append(['NAME:PLSegment', 'SegmentType:=', 'Line', 'StartIndex:=', 1, 'NoOfPoints:=', 2])
pts.append(['NAME:PLPoint', 'X:=', '-2.350000mm', 'Y:=', '-0.005000mm', 'Z:=', '0.0mm'])
segs.append(['NAME:PLSegment', 'SegmentType:=', 'Line', 'StartIndex:=', 2, 'NoOfPoints:=', 2])
pts.append(['NAME:PLPoint', 'X:=', '-2.350000mm', 'Y:=', '0.005000mm', 'Z:=', '0.0mm'])
segs.append(['NAME:PLSegment', 'SegmentType:=', 'Line', 'StartIndex:=', 3, 'NoOfPoints:=', 2])
pts.append(['NAME:PLPoint', 'X:=', '-2.075000mm', 'Y:=', '0.005000mm', 'Z:=', '0.0mm'])
oEditor.CreatePolyline(
    ['NAME:PolylineParameters', 'IsPolylineCovered:=', True, 'IsPolylineClosed:=', True, pts, segs],
    [
        'NAME:Attributes',
        'Name:=', 'b_wire_Q5_14',
        'Flags:=', '',
        'Color:=', '(200 220 255)',
        'Transparency:=', 0.0,
        'PartCoordinateSystem:=', 'Global',
        'UDMId:=', '',
        'MaterialName:=', 'vacuum',
        'SolveInside:=', True
    ]
)
# Element: b_wire_sub_Q5_15
pts = ['NAME:PolylinePoints']
segs = ['NAME:PolylineSegments']
pts.append(['NAME:PLPoint', 'X:=', '-2.075000mm', 'Y:=', '0.011000mm', 'Z:=', '0.0mm'])
segs.append(['NAME:PLSegment', 'SegmentType:=', 'Line', 'StartIndex:=', 0, 'NoOfPoints:=', 2])
pts.append(['NAME:PLPoint', 'X:=', '-2.075000mm', 'Y:=', '-0.011000mm', 'Z:=', '0.0mm'])
segs.append(['NAME:PLSegment', 'SegmentType:=', 'Line', 'StartIndex:=', 1, 'NoOfPoints:=', 2])
pts.append(['NAME:PLPoint', 'X:=', '-2.350000mm', 'Y:=', '-0.011000mm', 'Z:=', '0.0mm'])
segs.append(['NAME:PLSegment', 'SegmentType:=', 'Line', 'StartIndex:=', 2, 'NoOfPoints:=', 2])
pts.append(['NAME:PLPoint', 'X:=', '-2.350000mm', 'Y:=', '0.011000mm', 'Z:=', '0.0mm'])
segs.append(['NAME:PLSegment', 'SegmentType:=', 'Line', 'StartIndex:=', 3, 'NoOfPoints:=', 2])
pts.append(['NAME:PLPoint', 'X:=', '-2.075000mm', 'Y:=', '0.011000mm', 'Z:=', '0.0mm'])
oEditor.CreatePolyline(
    ['NAME:PolylineParameters', 'IsPolylineCovered:=', True, 'IsPolylineClosed:=', True, pts, segs],
    [
        'NAME:Attributes',
        'Name:=', 'b_wire_sub_Q5_15',
        'Flags:=', '',
        'Color:=', '(255 100 100)',
        'Transparency:=', 0.0,
        'PartCoordinateSystem:=', 'Global',
        'UDMId:=', '',
        'MaterialName:=', 'vacuum',
        'SolveInside:=', True
    ]
)
# Element: a_wire_Q6_16
pts = ['NAME:PolylinePoints']
segs = ['NAME:PolylineSegments']
pts.append(['NAME:PLPoint', 'X:=', '-0.425000mm', 'Y:=', '-0.005000mm', 'Z:=', '0.0mm'])
segs.append(['NAME:PLSegment', 'SegmentType:=', 'Line', 'StartIndex:=', 0, 'NoOfPoints:=', 2])
pts.append(['NAME:PLPoint', 'X:=', '-0.425000mm', 'Y:=', '0.005000mm', 'Z:=', '0.0mm'])
segs.append(['NAME:PLSegment', 'SegmentType:=', 'Line', 'StartIndex:=', 1, 'NoOfPoints:=', 2])
pts.append(['NAME:PLPoint', 'X:=', '-0.150000mm', 'Y:=', '0.005000mm', 'Z:=', '0.0mm'])
segs.append(['NAME:PLSegment', 'SegmentType:=', 'Line', 'StartIndex:=', 2, 'NoOfPoints:=', 2])
pts.append(['NAME:PLPoint', 'X:=', '-0.150000mm', 'Y:=', '-0.005000mm', 'Z:=', '0.0mm'])
segs.append(['NAME:PLSegment', 'SegmentType:=', 'Line', 'StartIndex:=', 3, 'NoOfPoints:=', 2])
pts.append(['NAME:PLPoint', 'X:=', '-0.425000mm', 'Y:=', '-0.005000mm', 'Z:=', '0.0mm'])
oEditor.CreatePolyline(
    ['NAME:PolylineParameters', 'IsPolylineCovered:=', True, 'IsPolylineClosed:=', True, pts, segs],
    [
        'NAME:Attributes',
        'Name:=', 'a_wire_Q6_16',
        'Flags:=', '',
        'Color:=', '(200 220 255)',
        'Transparency:=', 0.0,
        'PartCoordinateSystem:=', 'Global',
        'UDMId:=', '',
        'MaterialName:=', 'vacuum',
        'SolveInside:=', True
    ]
)
# Element: a_wire_sub_Q6_17
pts = ['NAME:PolylinePoints']
segs = ['NAME:PolylineSegments']
pts.append(['NAME:PLPoint', 'X:=', '-0.425000mm', 'Y:=', '-0.011000mm', 'Z:=', '0.0mm'])
segs.append(['NAME:PLSegment', 'SegmentType:=', 'Line', 'StartIndex:=', 0, 'NoOfPoints:=', 2])
pts.append(['NAME:PLPoint', 'X:=', '-0.425000mm', 'Y:=', '0.011000mm', 'Z:=', '0.0mm'])
segs.append(['NAME:PLSegment', 'SegmentType:=', 'Line', 'StartIndex:=', 1, 'NoOfPoints:=', 2])
pts.append(['NAME:PLPoint', 'X:=', '-0.150000mm', 'Y:=', '0.011000mm', 'Z:=', '0.0mm'])
segs.append(['NAME:PLSegment', 'SegmentType:=', 'Line', 'StartIndex:=', 2, 'NoOfPoints:=', 2])
pts.append(['NAME:PLPoint', 'X:=', '-0.150000mm', 'Y:=', '-0.011000mm', 'Z:=', '0.0mm'])
segs.append(['NAME:PLSegment', 'SegmentType:=', 'Line', 'StartIndex:=', 3, 'NoOfPoints:=', 2])
pts.append(['NAME:PLPoint', 'X:=', '-0.425000mm', 'Y:=', '-0.011000mm', 'Z:=', '0.0mm'])
oEditor.CreatePolyline(
    ['NAME:PolylineParameters', 'IsPolylineCovered:=', True, 'IsPolylineClosed:=', True, pts, segs],
    [
        'NAME:Attributes',
        'Name:=', 'a_wire_sub_Q6_17',
        'Flags:=', '',
        'Color:=', '(255 100 100)',
        'Transparency:=', 0.0,
        'PartCoordinateSystem:=', 'Global',
        'UDMId:=', '',
        'MaterialName:=', 'vacuum',
        'SolveInside:=', True
    ]
)
# Element: b_wire_Q6_18
pts = ['NAME:PolylinePoints']
segs = ['NAME:PolylineSegments']
pts.append(['NAME:PLPoint', 'X:=', '0.425000mm', 'Y:=', '0.005000mm', 'Z:=', '0.0mm'])
segs.append(['NAME:PLSegment', 'SegmentType:=', 'Line', 'StartIndex:=', 0, 'NoOfPoints:=', 2])
pts.append(['NAME:PLPoint', 'X:=', '0.425000mm', 'Y:=', '-0.005000mm', 'Z:=', '0.0mm'])
segs.append(['NAME:PLSegment', 'SegmentType:=', 'Line', 'StartIndex:=', 1, 'NoOfPoints:=', 2])
pts.append(['NAME:PLPoint', 'X:=', '0.150000mm', 'Y:=', '-0.005000mm', 'Z:=', '0.0mm'])
segs.append(['NAME:PLSegment', 'SegmentType:=', 'Line', 'StartIndex:=', 2, 'NoOfPoints:=', 2])
pts.append(['NAME:PLPoint', 'X:=', '0.150000mm', 'Y:=', '0.005000mm', 'Z:=', '0.0mm'])
segs.append(['NAME:PLSegment', 'SegmentType:=', 'Line', 'StartIndex:=', 3, 'NoOfPoints:=', 2])
pts.append(['NAME:PLPoint', 'X:=', '0.425000mm', 'Y:=', '0.005000mm', 'Z:=', '0.0mm'])
oEditor.CreatePolyline(
    ['NAME:PolylineParameters', 'IsPolylineCovered:=', True, 'IsPolylineClosed:=', True, pts, segs],
    [
        'NAME:Attributes',
        'Name:=', 'b_wire_Q6_18',
        'Flags:=', '',
        'Color:=', '(200 220 255)',
        'Transparency:=', 0.0,
        'PartCoordinateSystem:=', 'Global',
        'UDMId:=', '',
        'MaterialName:=', 'vacuum',
        'SolveInside:=', True
    ]
)
# Element: b_wire_sub_Q6_19
pts = ['NAME:PolylinePoints']
segs = ['NAME:PolylineSegments']
pts.append(['NAME:PLPoint', 'X:=', '0.425000mm', 'Y:=', '0.011000mm', 'Z:=', '0.0mm'])
segs.append(['NAME:PLSegment', 'SegmentType:=', 'Line', 'StartIndex:=', 0, 'NoOfPoints:=', 2])
pts.append(['NAME:PLPoint', 'X:=', '0.425000mm', 'Y:=', '-0.011000mm', 'Z:=', '0.0mm'])
segs.append(['NAME:PLSegment', 'SegmentType:=', 'Line', 'StartIndex:=', 1, 'NoOfPoints:=', 2])
pts.append(['NAME:PLPoint', 'X:=', '0.150000mm', 'Y:=', '-0.011000mm', 'Z:=', '0.0mm'])
segs.append(['NAME:PLSegment', 'SegmentType:=', 'Line', 'StartIndex:=', 2, 'NoOfPoints:=', 2])
pts.append(['NAME:PLPoint', 'X:=', '0.150000mm', 'Y:=', '0.011000mm', 'Z:=', '0.0mm'])
segs.append(['NAME:PLSegment', 'SegmentType:=', 'Line', 'StartIndex:=', 3, 'NoOfPoints:=', 2])
pts.append(['NAME:PLPoint', 'X:=', '0.425000mm', 'Y:=', '0.011000mm', 'Z:=', '0.0mm'])
oEditor.CreatePolyline(
    ['NAME:PolylineParameters', 'IsPolylineCovered:=', True, 'IsPolylineClosed:=', True, pts, segs],
    [
        'NAME:Attributes',
        'Name:=', 'b_wire_sub_Q6_19',
        'Flags:=', '',
        'Color:=', '(255 100 100)',
        'Transparency:=', 0.0,
        'PartCoordinateSystem:=', 'Global',
        'UDMId:=', '',
        'MaterialName:=', 'vacuum',
        'SolveInside:=', True
    ]
)
# Element: a_wire_Q7_20
pts = ['NAME:PolylinePoints']
segs = ['NAME:PolylineSegments']
pts.append(['NAME:PLPoint', 'X:=', '2.075000mm', 'Y:=', '-0.005000mm', 'Z:=', '0.0mm'])
segs.append(['NAME:PLSegment', 'SegmentType:=', 'Line', 'StartIndex:=', 0, 'NoOfPoints:=', 2])
pts.append(['NAME:PLPoint', 'X:=', '2.075000mm', 'Y:=', '0.005000mm', 'Z:=', '0.0mm'])
segs.append(['NAME:PLSegment', 'SegmentType:=', 'Line', 'StartIndex:=', 1, 'NoOfPoints:=', 2])
pts.append(['NAME:PLPoint', 'X:=', '2.350000mm', 'Y:=', '0.005000mm', 'Z:=', '0.0mm'])
segs.append(['NAME:PLSegment', 'SegmentType:=', 'Line', 'StartIndex:=', 2, 'NoOfPoints:=', 2])
pts.append(['NAME:PLPoint', 'X:=', '2.350000mm', 'Y:=', '-0.005000mm', 'Z:=', '0.0mm'])
segs.append(['NAME:PLSegment', 'SegmentType:=', 'Line', 'StartIndex:=', 3, 'NoOfPoints:=', 2])
pts.append(['NAME:PLPoint', 'X:=', '2.075000mm', 'Y:=', '-0.005000mm', 'Z:=', '0.0mm'])
oEditor.CreatePolyline(
    ['NAME:PolylineParameters', 'IsPolylineCovered:=', True, 'IsPolylineClosed:=', True, pts, segs],
    [
        'NAME:Attributes',
        'Name:=', 'a_wire_Q7_20',
        'Flags:=', '',
        'Color:=', '(200 220 255)',
        'Transparency:=', 0.0,
        'PartCoordinateSystem:=', 'Global',
        'UDMId:=', '',
        'MaterialName:=', 'vacuum',
        'SolveInside:=', True
    ]
)
# Element: a_wire_sub_Q7_21
pts = ['NAME:PolylinePoints']
segs = ['NAME:PolylineSegments']
pts.append(['NAME:PLPoint', 'X:=', '2.075000mm', 'Y:=', '-0.011000mm', 'Z:=', '0.0mm'])
segs.append(['NAME:PLSegment', 'SegmentType:=', 'Line', 'StartIndex:=', 0, 'NoOfPoints:=', 2])
pts.append(['NAME:PLPoint', 'X:=', '2.075000mm', 'Y:=', '0.011000mm', 'Z:=', '0.0mm'])
segs.append(['NAME:PLSegment', 'SegmentType:=', 'Line', 'StartIndex:=', 1, 'NoOfPoints:=', 2])
pts.append(['NAME:PLPoint', 'X:=', '2.350000mm', 'Y:=', '0.011000mm', 'Z:=', '0.0mm'])
segs.append(['NAME:PLSegment', 'SegmentType:=', 'Line', 'StartIndex:=', 2, 'NoOfPoints:=', 2])
pts.append(['NAME:PLPoint', 'X:=', '2.350000mm', 'Y:=', '-0.011000mm', 'Z:=', '0.0mm'])
segs.append(['NAME:PLSegment', 'SegmentType:=', 'Line', 'StartIndex:=', 3, 'NoOfPoints:=', 2])
pts.append(['NAME:PLPoint', 'X:=', '2.075000mm', 'Y:=', '-0.011000mm', 'Z:=', '0.0mm'])
oEditor.CreatePolyline(
    ['NAME:PolylineParameters', 'IsPolylineCovered:=', True, 'IsPolylineClosed:=', True, pts, segs],
    [
        'NAME:Attributes',
        'Name:=', 'a_wire_sub_Q7_21',
        'Flags:=', '',
        'Color:=', '(255 100 100)',
        'Transparency:=', 0.0,
        'PartCoordinateSystem:=', 'Global',
        'UDMId:=', '',
        'MaterialName:=', 'vacuum',
        'SolveInside:=', True
    ]
)
# Element: b_wire_Q7_22
pts = ['NAME:PolylinePoints']
segs = ['NAME:PolylineSegments']
pts.append(['NAME:PLPoint', 'X:=', '2.925000mm', 'Y:=', '0.005000mm', 'Z:=', '0.0mm'])
segs.append(['NAME:PLSegment', 'SegmentType:=', 'Line', 'StartIndex:=', 0, 'NoOfPoints:=', 2])
pts.append(['NAME:PLPoint', 'X:=', '2.925000mm', 'Y:=', '-0.005000mm', 'Z:=', '0.0mm'])
segs.append(['NAME:PLSegment', 'SegmentType:=', 'Line', 'StartIndex:=', 1, 'NoOfPoints:=', 2])
pts.append(['NAME:PLPoint', 'X:=', '2.650000mm', 'Y:=', '-0.005000mm', 'Z:=', '0.0mm'])
segs.append(['NAME:PLSegment', 'SegmentType:=', 'Line', 'StartIndex:=', 2, 'NoOfPoints:=', 2])
pts.append(['NAME:PLPoint', 'X:=', '2.650000mm', 'Y:=', '0.005000mm', 'Z:=', '0.0mm'])
segs.append(['NAME:PLSegment', 'SegmentType:=', 'Line', 'StartIndex:=', 3, 'NoOfPoints:=', 2])
pts.append(['NAME:PLPoint', 'X:=', '2.925000mm', 'Y:=', '0.005000mm', 'Z:=', '0.0mm'])
oEditor.CreatePolyline(
    ['NAME:PolylineParameters', 'IsPolylineCovered:=', True, 'IsPolylineClosed:=', True, pts, segs],
    [
        'NAME:Attributes',
        'Name:=', 'b_wire_Q7_22',
        'Flags:=', '',
        'Color:=', '(200 220 255)',
        'Transparency:=', 0.0,
        'PartCoordinateSystem:=', 'Global',
        'UDMId:=', '',
        'MaterialName:=', 'vacuum',
        'SolveInside:=', True
    ]
)
# Element: b_wire_sub_Q7_23
pts = ['NAME:PolylinePoints']
segs = ['NAME:PolylineSegments']
pts.append(['NAME:PLPoint', 'X:=', '2.925000mm', 'Y:=', '0.011000mm', 'Z:=', '0.0mm'])
segs.append(['NAME:PLSegment', 'SegmentType:=', 'Line', 'StartIndex:=', 0, 'NoOfPoints:=', 2])
pts.append(['NAME:PLPoint', 'X:=', '2.925000mm', 'Y:=', '-0.011000mm', 'Z:=', '0.0mm'])
segs.append(['NAME:PLSegment', 'SegmentType:=', 'Line', 'StartIndex:=', 1, 'NoOfPoints:=', 2])
pts.append(['NAME:PLPoint', 'X:=', '2.650000mm', 'Y:=', '-0.011000mm', 'Z:=', '0.0mm'])
segs.append(['NAME:PLSegment', 'SegmentType:=', 'Line', 'StartIndex:=', 2, 'NoOfPoints:=', 2])
pts.append(['NAME:PLPoint', 'X:=', '2.650000mm', 'Y:=', '0.011000mm', 'Z:=', '0.0mm'])
segs.append(['NAME:PLSegment', 'SegmentType:=', 'Line', 'StartIndex:=', 3, 'NoOfPoints:=', 2])
pts.append(['NAME:PLPoint', 'X:=', '2.925000mm', 'Y:=', '0.011000mm', 'Z:=', '0.0mm'])
oEditor.CreatePolyline(
    ['NAME:PolylineParameters', 'IsPolylineCovered:=', True, 'IsPolylineClosed:=', True, pts, segs],
    [
        'NAME:Attributes',
        'Name:=', 'b_wire_sub_Q7_23',
        'Flags:=', '',
        'Color:=', '(255 100 100)',
        'Transparency:=', 0.0,
        'PartCoordinateSystem:=', 'Global',
        'UDMId:=', '',
        'MaterialName:=', 'vacuum',
        'SolveInside:=', True
    ]
)
# Element: a_wire_Q4_24
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
        'Name:=', 'a_wire_Q4_24',
        'Flags:=', '',
        'Color:=', '(200 220 255)',
        'Transparency:=', 0.0,
        'PartCoordinateSystem:=', 'Global',
        'UDMId:=', '',
        'MaterialName:=', 'vacuum',
        'SolveInside:=', True
    ]
)
# Element: a_wire_sub_Q4_25
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
        'Name:=', 'a_wire_sub_Q4_25',
        'Flags:=', '',
        'Color:=', '(255 100 100)',
        'Transparency:=', 0.0,
        'PartCoordinateSystem:=', 'Global',
        'UDMId:=', '',
        'MaterialName:=', 'vacuum',
        'SolveInside:=', True
    ]
)
# Element: b_wire_Q4_26
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
        'Name:=', 'b_wire_Q4_26',
        'Flags:=', '',
        'Color:=', '(200 220 255)',
        'Transparency:=', 0.0,
        'PartCoordinateSystem:=', 'Global',
        'UDMId:=', '',
        'MaterialName:=', 'vacuum',
        'SolveInside:=', True
    ]
)
# Element: b_wire_sub_Q4_27
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
        'Name:=', 'b_wire_sub_Q4_27',
        'Flags:=', '',
        'Color:=', '(255 100 100)',
        'Transparency:=', 0.0,
        'PartCoordinateSystem:=', 'Global',
        'UDMId:=', '',
        'MaterialName:=', 'vacuum',
        'SolveInside:=', True
    ]
)
# Element: prime_cpw_Lt1_28
pts = ['NAME:PolylinePoints']
segs = ['NAME:PolylineSegments']
pts.append(['NAME:PLPoint', 'X:=', '0.550000mm', 'Y:=', '1.005000mm', 'Z:=', '0.0mm'])
segs.append(['NAME:PLSegment', 'SegmentType:=', 'Line', 'StartIndex:=', 0, 'NoOfPoints:=', 2])
pts.append(['NAME:PLPoint', 'X:=', '0.550000mm', 'Y:=', '0.995000mm', 'Z:=', '0.0mm'])
segs.append(['NAME:PLSegment', 'SegmentType:=', 'Line', 'StartIndex:=', 1, 'NoOfPoints:=', 2])
pts.append(['NAME:PLPoint', 'X:=', '0.450000mm', 'Y:=', '0.995000mm', 'Z:=', '0.0mm'])
segs.append(['NAME:PLSegment', 'SegmentType:=', 'Line', 'StartIndex:=', 2, 'NoOfPoints:=', 2])
pts.append(['NAME:PLPoint', 'X:=', '0.450000mm', 'Y:=', '1.005000mm', 'Z:=', '0.0mm'])
segs.append(['NAME:PLSegment', 'SegmentType:=', 'Line', 'StartIndex:=', 3, 'NoOfPoints:=', 2])
pts.append(['NAME:PLPoint', 'X:=', '0.550000mm', 'Y:=', '1.005000mm', 'Z:=', '0.0mm'])
oEditor.CreatePolyline(
    ['NAME:PolylineParameters', 'IsPolylineCovered:=', True, 'IsPolylineClosed:=', True, pts, segs],
    [
        'NAME:Attributes',
        'Name:=', 'prime_cpw_Lt1_28',
        'Flags:=', '',
        'Color:=', '(200 220 255)',
        'Transparency:=', 0.0,
        'PartCoordinateSystem:=', 'Global',
        'UDMId:=', '',
        'MaterialName:=', 'vacuum',
        'SolveInside:=', True
    ]
)
# Element: prime_cpw_sub_Lt1_29
pts = ['NAME:PolylinePoints']
segs = ['NAME:PolylineSegments']
pts.append(['NAME:PLPoint', 'X:=', '0.550000mm', 'Y:=', '1.011000mm', 'Z:=', '0.0mm'])
segs.append(['NAME:PLSegment', 'SegmentType:=', 'Line', 'StartIndex:=', 0, 'NoOfPoints:=', 2])
pts.append(['NAME:PLPoint', 'X:=', '0.550000mm', 'Y:=', '0.989000mm', 'Z:=', '0.0mm'])
segs.append(['NAME:PLSegment', 'SegmentType:=', 'Line', 'StartIndex:=', 1, 'NoOfPoints:=', 2])
pts.append(['NAME:PLPoint', 'X:=', '0.450000mm', 'Y:=', '0.989000mm', 'Z:=', '0.0mm'])
segs.append(['NAME:PLSegment', 'SegmentType:=', 'Line', 'StartIndex:=', 2, 'NoOfPoints:=', 2])
pts.append(['NAME:PLPoint', 'X:=', '0.450000mm', 'Y:=', '1.011000mm', 'Z:=', '0.0mm'])
segs.append(['NAME:PLSegment', 'SegmentType:=', 'Line', 'StartIndex:=', 3, 'NoOfPoints:=', 2])
pts.append(['NAME:PLPoint', 'X:=', '0.550000mm', 'Y:=', '1.011000mm', 'Z:=', '0.0mm'])
oEditor.CreatePolyline(
    ['NAME:PolylineParameters', 'IsPolylineCovered:=', True, 'IsPolylineClosed:=', True, pts, segs],
    [
        'NAME:Attributes',
        'Name:=', 'prime_cpw_sub_Lt1_29',
        'Flags:=', '',
        'Color:=', '(255 100 100)',
        'Transparency:=', 0.0,
        'PartCoordinateSystem:=', 'Global',
        'UDMId:=', '',
        'MaterialName:=', 'vacuum',
        'SolveInside:=', True
    ]
)
# Element: second_cpw_Lt1_30
pts = ['NAME:PolylinePoints']
segs = ['NAME:PolylineSegments']
pts.append(['NAME:PLPoint', 'X:=', '0.505000mm', 'Y:=', '0.950000mm', 'Z:=', '0.0mm'])
segs.append(['NAME:PLSegment', 'SegmentType:=', 'Line', 'StartIndex:=', 0, 'NoOfPoints:=', 2])
pts.append(['NAME:PLPoint', 'X:=', '0.495000mm', 'Y:=', '0.950000mm', 'Z:=', '0.0mm'])
segs.append(['NAME:PLSegment', 'SegmentType:=', 'Line', 'StartIndex:=', 1, 'NoOfPoints:=', 2])
pts.append(['NAME:PLPoint', 'X:=', '0.495000mm', 'Y:=', '0.995000mm', 'Z:=', '0.0mm'])
segs.append(['NAME:PLSegment', 'SegmentType:=', 'Line', 'StartIndex:=', 2, 'NoOfPoints:=', 2])
pts.append(['NAME:PLPoint', 'X:=', '0.505000mm', 'Y:=', '0.995000mm', 'Z:=', '0.0mm'])
segs.append(['NAME:PLSegment', 'SegmentType:=', 'Line', 'StartIndex:=', 3, 'NoOfPoints:=', 2])
pts.append(['NAME:PLPoint', 'X:=', '0.505000mm', 'Y:=', '0.950000mm', 'Z:=', '0.0mm'])
oEditor.CreatePolyline(
    ['NAME:PolylineParameters', 'IsPolylineCovered:=', True, 'IsPolylineClosed:=', True, pts, segs],
    [
        'NAME:Attributes',
        'Name:=', 'second_cpw_Lt1_30',
        'Flags:=', '',
        'Color:=', '(200 220 255)',
        'Transparency:=', 0.0,
        'PartCoordinateSystem:=', 'Global',
        'UDMId:=', '',
        'MaterialName:=', 'vacuum',
        'SolveInside:=', True
    ]
)
# Element: second_cpw_sub_Lt1_31
pts = ['NAME:PolylinePoints']
segs = ['NAME:PolylineSegments']
pts.append(['NAME:PLPoint', 'X:=', '0.511000mm', 'Y:=', '0.950000mm', 'Z:=', '0.0mm'])
segs.append(['NAME:PLSegment', 'SegmentType:=', 'Line', 'StartIndex:=', 0, 'NoOfPoints:=', 2])
pts.append(['NAME:PLPoint', 'X:=', '0.489000mm', 'Y:=', '0.950000mm', 'Z:=', '0.0mm'])
segs.append(['NAME:PLSegment', 'SegmentType:=', 'Line', 'StartIndex:=', 1, 'NoOfPoints:=', 2])
pts.append(['NAME:PLPoint', 'X:=', '0.489000mm', 'Y:=', '0.995000mm', 'Z:=', '0.0mm'])
segs.append(['NAME:PLSegment', 'SegmentType:=', 'Line', 'StartIndex:=', 2, 'NoOfPoints:=', 2])
pts.append(['NAME:PLPoint', 'X:=', '0.511000mm', 'Y:=', '0.995000mm', 'Z:=', '0.0mm'])
segs.append(['NAME:PLSegment', 'SegmentType:=', 'Line', 'StartIndex:=', 3, 'NoOfPoints:=', 2])
pts.append(['NAME:PLPoint', 'X:=', '0.511000mm', 'Y:=', '0.950000mm', 'Z:=', '0.0mm'])
oEditor.CreatePolyline(
    ['NAME:PolylineParameters', 'IsPolylineCovered:=', True, 'IsPolylineClosed:=', True, pts, segs],
    [
        'NAME:Attributes',
        'Name:=', 'second_cpw_sub_Lt1_31',
        'Flags:=', '',
        'Color:=', '(255 100 100)',
        'Transparency:=', 0.0,
        'PartCoordinateSystem:=', 'Global',
        'UDMId:=', '',
        'MaterialName:=', 'vacuum',
        'SolveInside:=', True
    ]
)
# Element: prime_cpw_Lt2_32
pts = ['NAME:PolylinePoints']
segs = ['NAME:PolylineSegments']
pts.append(['NAME:PLPoint', 'X:=', '-0.550000mm', 'Y:=', '0.995000mm', 'Z:=', '0.0mm'])
segs.append(['NAME:PLSegment', 'SegmentType:=', 'Line', 'StartIndex:=', 0, 'NoOfPoints:=', 2])
pts.append(['NAME:PLPoint', 'X:=', '-0.550000mm', 'Y:=', '1.005000mm', 'Z:=', '0.0mm'])
segs.append(['NAME:PLSegment', 'SegmentType:=', 'Line', 'StartIndex:=', 1, 'NoOfPoints:=', 2])
pts.append(['NAME:PLPoint', 'X:=', '-0.450000mm', 'Y:=', '1.005000mm', 'Z:=', '0.0mm'])
segs.append(['NAME:PLSegment', 'SegmentType:=', 'Line', 'StartIndex:=', 2, 'NoOfPoints:=', 2])
pts.append(['NAME:PLPoint', 'X:=', '-0.450000mm', 'Y:=', '0.995000mm', 'Z:=', '0.0mm'])
segs.append(['NAME:PLSegment', 'SegmentType:=', 'Line', 'StartIndex:=', 3, 'NoOfPoints:=', 2])
pts.append(['NAME:PLPoint', 'X:=', '-0.550000mm', 'Y:=', '0.995000mm', 'Z:=', '0.0mm'])
oEditor.CreatePolyline(
    ['NAME:PolylineParameters', 'IsPolylineCovered:=', True, 'IsPolylineClosed:=', True, pts, segs],
    [
        'NAME:Attributes',
        'Name:=', 'prime_cpw_Lt2_32',
        'Flags:=', '',
        'Color:=', '(200 220 255)',
        'Transparency:=', 0.0,
        'PartCoordinateSystem:=', 'Global',
        'UDMId:=', '',
        'MaterialName:=', 'vacuum',
        'SolveInside:=', True
    ]
)
# Element: prime_cpw_sub_Lt2_33
pts = ['NAME:PolylinePoints']
segs = ['NAME:PolylineSegments']
pts.append(['NAME:PLPoint', 'X:=', '-0.550000mm', 'Y:=', '0.989000mm', 'Z:=', '0.0mm'])
segs.append(['NAME:PLSegment', 'SegmentType:=', 'Line', 'StartIndex:=', 0, 'NoOfPoints:=', 2])
pts.append(['NAME:PLPoint', 'X:=', '-0.550000mm', 'Y:=', '1.011000mm', 'Z:=', '0.0mm'])
segs.append(['NAME:PLSegment', 'SegmentType:=', 'Line', 'StartIndex:=', 1, 'NoOfPoints:=', 2])
pts.append(['NAME:PLPoint', 'X:=', '-0.450000mm', 'Y:=', '1.011000mm', 'Z:=', '0.0mm'])
segs.append(['NAME:PLSegment', 'SegmentType:=', 'Line', 'StartIndex:=', 2, 'NoOfPoints:=', 2])
pts.append(['NAME:PLPoint', 'X:=', '-0.450000mm', 'Y:=', '0.989000mm', 'Z:=', '0.0mm'])
segs.append(['NAME:PLSegment', 'SegmentType:=', 'Line', 'StartIndex:=', 3, 'NoOfPoints:=', 2])
pts.append(['NAME:PLPoint', 'X:=', '-0.550000mm', 'Y:=', '0.989000mm', 'Z:=', '0.0mm'])
oEditor.CreatePolyline(
    ['NAME:PolylineParameters', 'IsPolylineCovered:=', True, 'IsPolylineClosed:=', True, pts, segs],
    [
        'NAME:Attributes',
        'Name:=', 'prime_cpw_sub_Lt2_33',
        'Flags:=', '',
        'Color:=', '(255 100 100)',
        'Transparency:=', 0.0,
        'PartCoordinateSystem:=', 'Global',
        'UDMId:=', '',
        'MaterialName:=', 'vacuum',
        'SolveInside:=', True
    ]
)
# Element: second_cpw_Lt2_34
pts = ['NAME:PolylinePoints']
segs = ['NAME:PolylineSegments']
pts.append(['NAME:PLPoint', 'X:=', '-0.505000mm', 'Y:=', '1.050000mm', 'Z:=', '0.0mm'])
segs.append(['NAME:PLSegment', 'SegmentType:=', 'Line', 'StartIndex:=', 0, 'NoOfPoints:=', 2])
pts.append(['NAME:PLPoint', 'X:=', '-0.495000mm', 'Y:=', '1.050000mm', 'Z:=', '0.0mm'])
segs.append(['NAME:PLSegment', 'SegmentType:=', 'Line', 'StartIndex:=', 1, 'NoOfPoints:=', 2])
pts.append(['NAME:PLPoint', 'X:=', '-0.495000mm', 'Y:=', '1.005000mm', 'Z:=', '0.0mm'])
segs.append(['NAME:PLSegment', 'SegmentType:=', 'Line', 'StartIndex:=', 2, 'NoOfPoints:=', 2])
pts.append(['NAME:PLPoint', 'X:=', '-0.505000mm', 'Y:=', '1.005000mm', 'Z:=', '0.0mm'])
segs.append(['NAME:PLSegment', 'SegmentType:=', 'Line', 'StartIndex:=', 3, 'NoOfPoints:=', 2])
pts.append(['NAME:PLPoint', 'X:=', '-0.505000mm', 'Y:=', '1.050000mm', 'Z:=', '0.0mm'])
oEditor.CreatePolyline(
    ['NAME:PolylineParameters', 'IsPolylineCovered:=', True, 'IsPolylineClosed:=', True, pts, segs],
    [
        'NAME:Attributes',
        'Name:=', 'second_cpw_Lt2_34',
        'Flags:=', '',
        'Color:=', '(200 220 255)',
        'Transparency:=', 0.0,
        'PartCoordinateSystem:=', 'Global',
        'UDMId:=', '',
        'MaterialName:=', 'vacuum',
        'SolveInside:=', True
    ]
)
# Element: second_cpw_sub_Lt2_35
pts = ['NAME:PolylinePoints']
segs = ['NAME:PolylineSegments']
pts.append(['NAME:PLPoint', 'X:=', '-0.511000mm', 'Y:=', '1.050000mm', 'Z:=', '0.0mm'])
segs.append(['NAME:PLSegment', 'SegmentType:=', 'Line', 'StartIndex:=', 0, 'NoOfPoints:=', 2])
pts.append(['NAME:PLPoint', 'X:=', '-0.489000mm', 'Y:=', '1.050000mm', 'Z:=', '0.0mm'])
segs.append(['NAME:PLSegment', 'SegmentType:=', 'Line', 'StartIndex:=', 1, 'NoOfPoints:=', 2])
pts.append(['NAME:PLPoint', 'X:=', '-0.489000mm', 'Y:=', '1.005000mm', 'Z:=', '0.0mm'])
segs.append(['NAME:PLSegment', 'SegmentType:=', 'Line', 'StartIndex:=', 2, 'NoOfPoints:=', 2])
pts.append(['NAME:PLPoint', 'X:=', '-0.511000mm', 'Y:=', '1.005000mm', 'Z:=', '0.0mm'])
segs.append(['NAME:PLSegment', 'SegmentType:=', 'Line', 'StartIndex:=', 3, 'NoOfPoints:=', 2])
pts.append(['NAME:PLPoint', 'X:=', '-0.511000mm', 'Y:=', '1.050000mm', 'Z:=', '0.0mm'])
oEditor.CreatePolyline(
    ['NAME:PolylineParameters', 'IsPolylineCovered:=', True, 'IsPolylineClosed:=', True, pts, segs],
    [
        'NAME:Attributes',
        'Name:=', 'second_cpw_sub_Lt2_35',
        'Flags:=', '',
        'Color:=', '(255 100 100)',
        'Transparency:=', 0.0,
        'PartCoordinateSystem:=', 'Global',
        'UDMId:=', '',
        'MaterialName:=', 'vacuum',
        'SolveInside:=', True
    ]
)
# Element: prime_cpw_Lt3_36
pts = ['NAME:PolylinePoints']
segs = ['NAME:PolylineSegments']
pts.append(['NAME:PLPoint', 'X:=', '1.550000mm', 'Y:=', '1.005000mm', 'Z:=', '0.0mm'])
segs.append(['NAME:PLSegment', 'SegmentType:=', 'Line', 'StartIndex:=', 0, 'NoOfPoints:=', 2])
pts.append(['NAME:PLPoint', 'X:=', '1.550000mm', 'Y:=', '0.995000mm', 'Z:=', '0.0mm'])
segs.append(['NAME:PLSegment', 'SegmentType:=', 'Line', 'StartIndex:=', 1, 'NoOfPoints:=', 2])
pts.append(['NAME:PLPoint', 'X:=', '1.450000mm', 'Y:=', '0.995000mm', 'Z:=', '0.0mm'])
segs.append(['NAME:PLSegment', 'SegmentType:=', 'Line', 'StartIndex:=', 2, 'NoOfPoints:=', 2])
pts.append(['NAME:PLPoint', 'X:=', '1.450000mm', 'Y:=', '1.005000mm', 'Z:=', '0.0mm'])
segs.append(['NAME:PLSegment', 'SegmentType:=', 'Line', 'StartIndex:=', 3, 'NoOfPoints:=', 2])
pts.append(['NAME:PLPoint', 'X:=', '1.550000mm', 'Y:=', '1.005000mm', 'Z:=', '0.0mm'])
oEditor.CreatePolyline(
    ['NAME:PolylineParameters', 'IsPolylineCovered:=', True, 'IsPolylineClosed:=', True, pts, segs],
    [
        'NAME:Attributes',
        'Name:=', 'prime_cpw_Lt3_36',
        'Flags:=', '',
        'Color:=', '(200 220 255)',
        'Transparency:=', 0.0,
        'PartCoordinateSystem:=', 'Global',
        'UDMId:=', '',
        'MaterialName:=', 'vacuum',
        'SolveInside:=', True
    ]
)
# Element: prime_cpw_sub_Lt3_37
pts = ['NAME:PolylinePoints']
segs = ['NAME:PolylineSegments']
pts.append(['NAME:PLPoint', 'X:=', '1.550000mm', 'Y:=', '1.011000mm', 'Z:=', '0.0mm'])
segs.append(['NAME:PLSegment', 'SegmentType:=', 'Line', 'StartIndex:=', 0, 'NoOfPoints:=', 2])
pts.append(['NAME:PLPoint', 'X:=', '1.550000mm', 'Y:=', '0.989000mm', 'Z:=', '0.0mm'])
segs.append(['NAME:PLSegment', 'SegmentType:=', 'Line', 'StartIndex:=', 1, 'NoOfPoints:=', 2])
pts.append(['NAME:PLPoint', 'X:=', '1.450000mm', 'Y:=', '0.989000mm', 'Z:=', '0.0mm'])
segs.append(['NAME:PLSegment', 'SegmentType:=', 'Line', 'StartIndex:=', 2, 'NoOfPoints:=', 2])
pts.append(['NAME:PLPoint', 'X:=', '1.450000mm', 'Y:=', '1.011000mm', 'Z:=', '0.0mm'])
segs.append(['NAME:PLSegment', 'SegmentType:=', 'Line', 'StartIndex:=', 3, 'NoOfPoints:=', 2])
pts.append(['NAME:PLPoint', 'X:=', '1.550000mm', 'Y:=', '1.011000mm', 'Z:=', '0.0mm'])
oEditor.CreatePolyline(
    ['NAME:PolylineParameters', 'IsPolylineCovered:=', True, 'IsPolylineClosed:=', True, pts, segs],
    [
        'NAME:Attributes',
        'Name:=', 'prime_cpw_sub_Lt3_37',
        'Flags:=', '',
        'Color:=', '(255 100 100)',
        'Transparency:=', 0.0,
        'PartCoordinateSystem:=', 'Global',
        'UDMId:=', '',
        'MaterialName:=', 'vacuum',
        'SolveInside:=', True
    ]
)
# Element: second_cpw_Lt3_38
pts = ['NAME:PolylinePoints']
segs = ['NAME:PolylineSegments']
pts.append(['NAME:PLPoint', 'X:=', '1.505000mm', 'Y:=', '0.950000mm', 'Z:=', '0.0mm'])
segs.append(['NAME:PLSegment', 'SegmentType:=', 'Line', 'StartIndex:=', 0, 'NoOfPoints:=', 2])
pts.append(['NAME:PLPoint', 'X:=', '1.495000mm', 'Y:=', '0.950000mm', 'Z:=', '0.0mm'])
segs.append(['NAME:PLSegment', 'SegmentType:=', 'Line', 'StartIndex:=', 1, 'NoOfPoints:=', 2])
pts.append(['NAME:PLPoint', 'X:=', '1.495000mm', 'Y:=', '0.995000mm', 'Z:=', '0.0mm'])
segs.append(['NAME:PLSegment', 'SegmentType:=', 'Line', 'StartIndex:=', 2, 'NoOfPoints:=', 2])
pts.append(['NAME:PLPoint', 'X:=', '1.505000mm', 'Y:=', '0.995000mm', 'Z:=', '0.0mm'])
segs.append(['NAME:PLSegment', 'SegmentType:=', 'Line', 'StartIndex:=', 3, 'NoOfPoints:=', 2])
pts.append(['NAME:PLPoint', 'X:=', '1.505000mm', 'Y:=', '0.950000mm', 'Z:=', '0.0mm'])
oEditor.CreatePolyline(
    ['NAME:PolylineParameters', 'IsPolylineCovered:=', True, 'IsPolylineClosed:=', True, pts, segs],
    [
        'NAME:Attributes',
        'Name:=', 'second_cpw_Lt3_38',
        'Flags:=', '',
        'Color:=', '(200 220 255)',
        'Transparency:=', 0.0,
        'PartCoordinateSystem:=', 'Global',
        'UDMId:=', '',
        'MaterialName:=', 'vacuum',
        'SolveInside:=', True
    ]
)
# Element: second_cpw_sub_Lt3_39
pts = ['NAME:PolylinePoints']
segs = ['NAME:PolylineSegments']
pts.append(['NAME:PLPoint', 'X:=', '1.511000mm', 'Y:=', '0.950000mm', 'Z:=', '0.0mm'])
segs.append(['NAME:PLSegment', 'SegmentType:=', 'Line', 'StartIndex:=', 0, 'NoOfPoints:=', 2])
pts.append(['NAME:PLPoint', 'X:=', '1.489000mm', 'Y:=', '0.950000mm', 'Z:=', '0.0mm'])
segs.append(['NAME:PLSegment', 'SegmentType:=', 'Line', 'StartIndex:=', 1, 'NoOfPoints:=', 2])
pts.append(['NAME:PLPoint', 'X:=', '1.489000mm', 'Y:=', '0.995000mm', 'Z:=', '0.0mm'])
segs.append(['NAME:PLSegment', 'SegmentType:=', 'Line', 'StartIndex:=', 2, 'NoOfPoints:=', 2])
pts.append(['NAME:PLPoint', 'X:=', '1.511000mm', 'Y:=', '0.995000mm', 'Z:=', '0.0mm'])
segs.append(['NAME:PLSegment', 'SegmentType:=', 'Line', 'StartIndex:=', 3, 'NoOfPoints:=', 2])
pts.append(['NAME:PLPoint', 'X:=', '1.511000mm', 'Y:=', '0.950000mm', 'Z:=', '0.0mm'])
oEditor.CreatePolyline(
    ['NAME:PolylineParameters', 'IsPolylineCovered:=', True, 'IsPolylineClosed:=', True, pts, segs],
    [
        'NAME:Attributes',
        'Name:=', 'second_cpw_sub_Lt3_39',
        'Flags:=', '',
        'Color:=', '(255 100 100)',
        'Transparency:=', 0.0,
        'PartCoordinateSystem:=', 'Global',
        'UDMId:=', '',
        'MaterialName:=', 'vacuum',
        'SolveInside:=', True
    ]
)
# Element: prime_cpw_Lt4_40
pts = ['NAME:PolylinePoints']
segs = ['NAME:PolylineSegments']
pts.append(['NAME:PLPoint', 'X:=', '-1.550000mm', 'Y:=', '0.995000mm', 'Z:=', '0.0mm'])
segs.append(['NAME:PLSegment', 'SegmentType:=', 'Line', 'StartIndex:=', 0, 'NoOfPoints:=', 2])
pts.append(['NAME:PLPoint', 'X:=', '-1.550000mm', 'Y:=', '1.005000mm', 'Z:=', '0.0mm'])
segs.append(['NAME:PLSegment', 'SegmentType:=', 'Line', 'StartIndex:=', 1, 'NoOfPoints:=', 2])
pts.append(['NAME:PLPoint', 'X:=', '-1.450000mm', 'Y:=', '1.005000mm', 'Z:=', '0.0mm'])
segs.append(['NAME:PLSegment', 'SegmentType:=', 'Line', 'StartIndex:=', 2, 'NoOfPoints:=', 2])
pts.append(['NAME:PLPoint', 'X:=', '-1.450000mm', 'Y:=', '0.995000mm', 'Z:=', '0.0mm'])
segs.append(['NAME:PLSegment', 'SegmentType:=', 'Line', 'StartIndex:=', 3, 'NoOfPoints:=', 2])
pts.append(['NAME:PLPoint', 'X:=', '-1.550000mm', 'Y:=', '0.995000mm', 'Z:=', '0.0mm'])
oEditor.CreatePolyline(
    ['NAME:PolylineParameters', 'IsPolylineCovered:=', True, 'IsPolylineClosed:=', True, pts, segs],
    [
        'NAME:Attributes',
        'Name:=', 'prime_cpw_Lt4_40',
        'Flags:=', '',
        'Color:=', '(200 220 255)',
        'Transparency:=', 0.0,
        'PartCoordinateSystem:=', 'Global',
        'UDMId:=', '',
        'MaterialName:=', 'vacuum',
        'SolveInside:=', True
    ]
)
# Element: prime_cpw_sub_Lt4_41
pts = ['NAME:PolylinePoints']
segs = ['NAME:PolylineSegments']
pts.append(['NAME:PLPoint', 'X:=', '-1.550000mm', 'Y:=', '0.989000mm', 'Z:=', '0.0mm'])
segs.append(['NAME:PLSegment', 'SegmentType:=', 'Line', 'StartIndex:=', 0, 'NoOfPoints:=', 2])
pts.append(['NAME:PLPoint', 'X:=', '-1.550000mm', 'Y:=', '1.011000mm', 'Z:=', '0.0mm'])
segs.append(['NAME:PLSegment', 'SegmentType:=', 'Line', 'StartIndex:=', 1, 'NoOfPoints:=', 2])
pts.append(['NAME:PLPoint', 'X:=', '-1.450000mm', 'Y:=', '1.011000mm', 'Z:=', '0.0mm'])
segs.append(['NAME:PLSegment', 'SegmentType:=', 'Line', 'StartIndex:=', 2, 'NoOfPoints:=', 2])
pts.append(['NAME:PLPoint', 'X:=', '-1.450000mm', 'Y:=', '0.989000mm', 'Z:=', '0.0mm'])
segs.append(['NAME:PLSegment', 'SegmentType:=', 'Line', 'StartIndex:=', 3, 'NoOfPoints:=', 2])
pts.append(['NAME:PLPoint', 'X:=', '-1.550000mm', 'Y:=', '0.989000mm', 'Z:=', '0.0mm'])
oEditor.CreatePolyline(
    ['NAME:PolylineParameters', 'IsPolylineCovered:=', True, 'IsPolylineClosed:=', True, pts, segs],
    [
        'NAME:Attributes',
        'Name:=', 'prime_cpw_sub_Lt4_41',
        'Flags:=', '',
        'Color:=', '(255 100 100)',
        'Transparency:=', 0.0,
        'PartCoordinateSystem:=', 'Global',
        'UDMId:=', '',
        'MaterialName:=', 'vacuum',
        'SolveInside:=', True
    ]
)
# Element: second_cpw_Lt4_42
pts = ['NAME:PolylinePoints']
segs = ['NAME:PolylineSegments']
pts.append(['NAME:PLPoint', 'X:=', '-1.505000mm', 'Y:=', '1.050000mm', 'Z:=', '0.0mm'])
segs.append(['NAME:PLSegment', 'SegmentType:=', 'Line', 'StartIndex:=', 0, 'NoOfPoints:=', 2])
pts.append(['NAME:PLPoint', 'X:=', '-1.495000mm', 'Y:=', '1.050000mm', 'Z:=', '0.0mm'])
segs.append(['NAME:PLSegment', 'SegmentType:=', 'Line', 'StartIndex:=', 1, 'NoOfPoints:=', 2])
pts.append(['NAME:PLPoint', 'X:=', '-1.495000mm', 'Y:=', '1.005000mm', 'Z:=', '0.0mm'])
segs.append(['NAME:PLSegment', 'SegmentType:=', 'Line', 'StartIndex:=', 2, 'NoOfPoints:=', 2])
pts.append(['NAME:PLPoint', 'X:=', '-1.505000mm', 'Y:=', '1.005000mm', 'Z:=', '0.0mm'])
segs.append(['NAME:PLSegment', 'SegmentType:=', 'Line', 'StartIndex:=', 3, 'NoOfPoints:=', 2])
pts.append(['NAME:PLPoint', 'X:=', '-1.505000mm', 'Y:=', '1.050000mm', 'Z:=', '0.0mm'])
oEditor.CreatePolyline(
    ['NAME:PolylineParameters', 'IsPolylineCovered:=', True, 'IsPolylineClosed:=', True, pts, segs],
    [
        'NAME:Attributes',
        'Name:=', 'second_cpw_Lt4_42',
        'Flags:=', '',
        'Color:=', '(200 220 255)',
        'Transparency:=', 0.0,
        'PartCoordinateSystem:=', 'Global',
        'UDMId:=', '',
        'MaterialName:=', 'vacuum',
        'SolveInside:=', True
    ]
)
# Element: second_cpw_sub_Lt4_43
pts = ['NAME:PolylinePoints']
segs = ['NAME:PolylineSegments']
pts.append(['NAME:PLPoint', 'X:=', '-1.511000mm', 'Y:=', '1.050000mm', 'Z:=', '0.0mm'])
segs.append(['NAME:PLSegment', 'SegmentType:=', 'Line', 'StartIndex:=', 0, 'NoOfPoints:=', 2])
pts.append(['NAME:PLPoint', 'X:=', '-1.489000mm', 'Y:=', '1.050000mm', 'Z:=', '0.0mm'])
segs.append(['NAME:PLSegment', 'SegmentType:=', 'Line', 'StartIndex:=', 1, 'NoOfPoints:=', 2])
pts.append(['NAME:PLPoint', 'X:=', '-1.489000mm', 'Y:=', '1.005000mm', 'Z:=', '0.0mm'])
segs.append(['NAME:PLSegment', 'SegmentType:=', 'Line', 'StartIndex:=', 2, 'NoOfPoints:=', 2])
pts.append(['NAME:PLPoint', 'X:=', '-1.511000mm', 'Y:=', '1.005000mm', 'Z:=', '0.0mm'])
segs.append(['NAME:PLSegment', 'SegmentType:=', 'Line', 'StartIndex:=', 3, 'NoOfPoints:=', 2])
pts.append(['NAME:PLPoint', 'X:=', '-1.511000mm', 'Y:=', '1.050000mm', 'Z:=', '0.0mm'])
oEditor.CreatePolyline(
    ['NAME:PolylineParameters', 'IsPolylineCovered:=', True, 'IsPolylineClosed:=', True, pts, segs],
    [
        'NAME:Attributes',
        'Name:=', 'second_cpw_sub_Lt4_43',
        'Flags:=', '',
        'Color:=', '(255 100 100)',
        'Transparency:=', 0.0,
        'PartCoordinateSystem:=', 'Global',
        'UDMId:=', '',
        'MaterialName:=', 'vacuum',
        'SolveInside:=', True
    ]
)
# Element: trace_RM1_44
pts = ['NAME:PolylinePoints']
segs = ['NAME:PolylineSegments']
pts.append(['NAME:PLPoint', 'X:=', '0.505000mm', 'Y:=', '0.585000mm', 'Z:=', '0.0mm'])
segs.append(['NAME:PLSegment', 'SegmentType:=', 'Line', 'StartIndex:=', 0, 'NoOfPoints:=', 2])
pts.append(['NAME:PLPoint', 'X:=', '0.295000mm', 'Y:=', '0.585000mm', 'Z:=', '0.0mm'])
segs.append(['NAME:PLSegment', 'SegmentType:=', 'Line', 'StartIndex:=', 1, 'NoOfPoints:=', 2])
pts.append(['NAME:PLPoint', 'X:=', '0.295000mm', 'Y:=', '1.295000mm', 'Z:=', '0.0mm'])
segs.append(['NAME:PLSegment', 'SegmentType:=', 'Line', 'StartIndex:=', 2, 'NoOfPoints:=', 2])
pts.append(['NAME:PLPoint', 'X:=', '0.105000mm', 'Y:=', '1.295000mm', 'Z:=', '0.0mm'])
segs.append(['NAME:PLSegment', 'SegmentType:=', 'Line', 'StartIndex:=', 3, 'NoOfPoints:=', 2])
pts.append(['NAME:PLPoint', 'X:=', '0.105000mm', 'Y:=', '0.585000mm', 'Z:=', '0.0mm'])
segs.append(['NAME:PLSegment', 'SegmentType:=', 'Line', 'StartIndex:=', 4, 'NoOfPoints:=', 2])
pts.append(['NAME:PLPoint', 'X:=', '-0.105000mm', 'Y:=', '0.585000mm', 'Z:=', '0.0mm'])
segs.append(['NAME:PLSegment', 'SegmentType:=', 'Line', 'StartIndex:=', 5, 'NoOfPoints:=', 2])
pts.append(['NAME:PLPoint', 'X:=', '-0.105000mm', 'Y:=', '1.295000mm', 'Z:=', '0.0mm'])
segs.append(['NAME:PLSegment', 'SegmentType:=', 'Line', 'StartIndex:=', 6, 'NoOfPoints:=', 2])
pts.append(['NAME:PLPoint', 'X:=', '-0.295000mm', 'Y:=', '1.295000mm', 'Z:=', '0.0mm'])
segs.append(['NAME:PLSegment', 'SegmentType:=', 'Line', 'StartIndex:=', 7, 'NoOfPoints:=', 2])
pts.append(['NAME:PLPoint', 'X:=', '-0.295000mm', 'Y:=', '0.585000mm', 'Z:=', '0.0mm'])
segs.append(['NAME:PLSegment', 'SegmentType:=', 'Line', 'StartIndex:=', 8, 'NoOfPoints:=', 2])
pts.append(['NAME:PLPoint', 'X:=', '-0.505000mm', 'Y:=', '0.585000mm', 'Z:=', '0.0mm'])
segs.append(['NAME:PLSegment', 'SegmentType:=', 'Line', 'StartIndex:=', 9, 'NoOfPoints:=', 2])
pts.append(['NAME:PLPoint', 'X:=', '-0.505000mm', 'Y:=', '1.295000mm', 'Z:=', '0.0mm'])
segs.append(['NAME:PLSegment', 'SegmentType:=', 'Line', 'StartIndex:=', 10, 'NoOfPoints:=', 2])
pts.append(['NAME:PLPoint', 'X:=', '-0.695000mm', 'Y:=', '1.295000mm', 'Z:=', '0.0mm'])
segs.append(['NAME:PLSegment', 'SegmentType:=', 'Line', 'StartIndex:=', 11, 'NoOfPoints:=', 2])
pts.append(['NAME:PLPoint', 'X:=', '-0.695000mm', 'Y:=', '0.585000mm', 'Z:=', '0.0mm'])
segs.append(['NAME:PLSegment', 'SegmentType:=', 'Line', 'StartIndex:=', 12, 'NoOfPoints:=', 2])
pts.append(['NAME:PLPoint', 'X:=', '-0.905000mm', 'Y:=', '0.585000mm', 'Z:=', '0.0mm'])
segs.append(['NAME:PLSegment', 'SegmentType:=', 'Line', 'StartIndex:=', 13, 'NoOfPoints:=', 2])
pts.append(['NAME:PLPoint', 'X:=', '-0.905000mm', 'Y:=', '1.295000mm', 'Z:=', '0.0mm'])
segs.append(['NAME:PLSegment', 'SegmentType:=', 'Line', 'StartIndex:=', 14, 'NoOfPoints:=', 2])
pts.append(['NAME:PLPoint', 'X:=', '-1.095000mm', 'Y:=', '1.295000mm', 'Z:=', '0.0mm'])
segs.append(['NAME:PLSegment', 'SegmentType:=', 'Line', 'StartIndex:=', 15, 'NoOfPoints:=', 2])
pts.append(['NAME:PLPoint', 'X:=', '-1.095000mm', 'Y:=', '0.585000mm', 'Z:=', '0.0mm'])
segs.append(['NAME:PLSegment', 'SegmentType:=', 'Line', 'StartIndex:=', 16, 'NoOfPoints:=', 2])
pts.append(['NAME:PLPoint', 'X:=', '-1.305000mm', 'Y:=', '0.585000mm', 'Z:=', '0.0mm'])
segs.append(['NAME:PLSegment', 'SegmentType:=', 'Line', 'StartIndex:=', 17, 'NoOfPoints:=', 2])
pts.append(['NAME:PLPoint', 'X:=', '-1.305000mm', 'Y:=', '1.295000mm', 'Z:=', '0.0mm'])
segs.append(['NAME:PLSegment', 'SegmentType:=', 'Line', 'StartIndex:=', 18, 'NoOfPoints:=', 2])
pts.append(['NAME:PLPoint', 'X:=', '-1.495000mm', 'Y:=', '1.295000mm', 'Z:=', '0.0mm'])
segs.append(['NAME:PLSegment', 'SegmentType:=', 'Line', 'StartIndex:=', 19, 'NoOfPoints:=', 2])
pts.append(['NAME:PLPoint', 'X:=', '-1.495000mm', 'Y:=', '1.050000mm', 'Z:=', '0.0mm'])
segs.append(['NAME:PLSegment', 'SegmentType:=', 'Line', 'StartIndex:=', 20, 'NoOfPoints:=', 2])
pts.append(['NAME:PLPoint', 'X:=', '-1.505000mm', 'Y:=', '1.050000mm', 'Z:=', '0.0mm'])
segs.append(['NAME:PLSegment', 'SegmentType:=', 'Line', 'StartIndex:=', 21, 'NoOfPoints:=', 2])
pts.append(['NAME:PLPoint', 'X:=', '-1.505000mm', 'Y:=', '1.305000mm', 'Z:=', '0.0mm'])
segs.append(['NAME:PLSegment', 'SegmentType:=', 'Line', 'StartIndex:=', 22, 'NoOfPoints:=', 2])
pts.append(['NAME:PLPoint', 'X:=', '-1.295000mm', 'Y:=', '1.305000mm', 'Z:=', '0.0mm'])
segs.append(['NAME:PLSegment', 'SegmentType:=', 'Line', 'StartIndex:=', 23, 'NoOfPoints:=', 2])
pts.append(['NAME:PLPoint', 'X:=', '-1.295000mm', 'Y:=', '0.595000mm', 'Z:=', '0.0mm'])
segs.append(['NAME:PLSegment', 'SegmentType:=', 'Line', 'StartIndex:=', 24, 'NoOfPoints:=', 2])
pts.append(['NAME:PLPoint', 'X:=', '-1.105000mm', 'Y:=', '0.595000mm', 'Z:=', '0.0mm'])
segs.append(['NAME:PLSegment', 'SegmentType:=', 'Line', 'StartIndex:=', 25, 'NoOfPoints:=', 2])
pts.append(['NAME:PLPoint', 'X:=', '-1.105000mm', 'Y:=', '1.305000mm', 'Z:=', '0.0mm'])
segs.append(['NAME:PLSegment', 'SegmentType:=', 'Line', 'StartIndex:=', 26, 'NoOfPoints:=', 2])
pts.append(['NAME:PLPoint', 'X:=', '-0.895000mm', 'Y:=', '1.305000mm', 'Z:=', '0.0mm'])
segs.append(['NAME:PLSegment', 'SegmentType:=', 'Line', 'StartIndex:=', 27, 'NoOfPoints:=', 2])
pts.append(['NAME:PLPoint', 'X:=', '-0.895000mm', 'Y:=', '0.595000mm', 'Z:=', '0.0mm'])
segs.append(['NAME:PLSegment', 'SegmentType:=', 'Line', 'StartIndex:=', 28, 'NoOfPoints:=', 2])
pts.append(['NAME:PLPoint', 'X:=', '-0.705000mm', 'Y:=', '0.595000mm', 'Z:=', '0.0mm'])
segs.append(['NAME:PLSegment', 'SegmentType:=', 'Line', 'StartIndex:=', 29, 'NoOfPoints:=', 2])
pts.append(['NAME:PLPoint', 'X:=', '-0.705000mm', 'Y:=', '1.305000mm', 'Z:=', '0.0mm'])
segs.append(['NAME:PLSegment', 'SegmentType:=', 'Line', 'StartIndex:=', 30, 'NoOfPoints:=', 2])
pts.append(['NAME:PLPoint', 'X:=', '-0.495000mm', 'Y:=', '1.305000mm', 'Z:=', '0.0mm'])
segs.append(['NAME:PLSegment', 'SegmentType:=', 'Line', 'StartIndex:=', 31, 'NoOfPoints:=', 2])
pts.append(['NAME:PLPoint', 'X:=', '-0.495000mm', 'Y:=', '0.595000mm', 'Z:=', '0.0mm'])
segs.append(['NAME:PLSegment', 'SegmentType:=', 'Line', 'StartIndex:=', 32, 'NoOfPoints:=', 2])
pts.append(['NAME:PLPoint', 'X:=', '-0.305000mm', 'Y:=', '0.595000mm', 'Z:=', '0.0mm'])
segs.append(['NAME:PLSegment', 'SegmentType:=', 'Line', 'StartIndex:=', 33, 'NoOfPoints:=', 2])
pts.append(['NAME:PLPoint', 'X:=', '-0.305000mm', 'Y:=', '1.305000mm', 'Z:=', '0.0mm'])
segs.append(['NAME:PLSegment', 'SegmentType:=', 'Line', 'StartIndex:=', 34, 'NoOfPoints:=', 2])
pts.append(['NAME:PLPoint', 'X:=', '-0.095000mm', 'Y:=', '1.305000mm', 'Z:=', '0.0mm'])
segs.append(['NAME:PLSegment', 'SegmentType:=', 'Line', 'StartIndex:=', 35, 'NoOfPoints:=', 2])
pts.append(['NAME:PLPoint', 'X:=', '-0.095000mm', 'Y:=', '0.595000mm', 'Z:=', '0.0mm'])
segs.append(['NAME:PLSegment', 'SegmentType:=', 'Line', 'StartIndex:=', 36, 'NoOfPoints:=', 2])
pts.append(['NAME:PLPoint', 'X:=', '0.095000mm', 'Y:=', '0.595000mm', 'Z:=', '0.0mm'])
segs.append(['NAME:PLSegment', 'SegmentType:=', 'Line', 'StartIndex:=', 37, 'NoOfPoints:=', 2])
pts.append(['NAME:PLPoint', 'X:=', '0.095000mm', 'Y:=', '1.305000mm', 'Z:=', '0.0mm'])
segs.append(['NAME:PLSegment', 'SegmentType:=', 'Line', 'StartIndex:=', 38, 'NoOfPoints:=', 2])
pts.append(['NAME:PLPoint', 'X:=', '0.305000mm', 'Y:=', '1.305000mm', 'Z:=', '0.0mm'])
segs.append(['NAME:PLSegment', 'SegmentType:=', 'Line', 'StartIndex:=', 39, 'NoOfPoints:=', 2])
pts.append(['NAME:PLPoint', 'X:=', '0.305000mm', 'Y:=', '0.595000mm', 'Z:=', '0.0mm'])
segs.append(['NAME:PLSegment', 'SegmentType:=', 'Line', 'StartIndex:=', 40, 'NoOfPoints:=', 2])
pts.append(['NAME:PLPoint', 'X:=', '0.495000mm', 'Y:=', '0.595000mm', 'Z:=', '0.0mm'])
segs.append(['NAME:PLSegment', 'SegmentType:=', 'Line', 'StartIndex:=', 41, 'NoOfPoints:=', 2])
pts.append(['NAME:PLPoint', 'X:=', '0.495000mm', 'Y:=', '0.950000mm', 'Z:=', '0.0mm'])
segs.append(['NAME:PLSegment', 'SegmentType:=', 'Line', 'StartIndex:=', 42, 'NoOfPoints:=', 2])
pts.append(['NAME:PLPoint', 'X:=', '0.505000mm', 'Y:=', '0.950000mm', 'Z:=', '0.0mm'])
segs.append(['NAME:PLSegment', 'SegmentType:=', 'Line', 'StartIndex:=', 43, 'NoOfPoints:=', 2])
pts.append(['NAME:PLPoint', 'X:=', '0.505000mm', 'Y:=', '0.585000mm', 'Z:=', '0.0mm'])
oEditor.CreatePolyline(
    ['NAME:PolylineParameters', 'IsPolylineCovered:=', True, 'IsPolylineClosed:=', True, pts, segs],
    [
        'NAME:Attributes',
        'Name:=', 'trace_RM1_44',
        'Flags:=', '',
        'Color:=', '(200 220 255)',
        'Transparency:=', 0.0,
        'PartCoordinateSystem:=', 'Global',
        'UDMId:=', '',
        'MaterialName:=', 'vacuum',
        'SolveInside:=', True
    ]
)
# Element: cut_RM1_45
pts = ['NAME:PolylinePoints']
segs = ['NAME:PolylineSegments']
pts.append(['NAME:PLPoint', 'X:=', '0.511000mm', 'Y:=', '0.579000mm', 'Z:=', '0.0mm'])
segs.append(['NAME:PLSegment', 'SegmentType:=', 'Line', 'StartIndex:=', 0, 'NoOfPoints:=', 2])
pts.append(['NAME:PLPoint', 'X:=', '0.289000mm', 'Y:=', '0.579000mm', 'Z:=', '0.0mm'])
segs.append(['NAME:PLSegment', 'SegmentType:=', 'Line', 'StartIndex:=', 1, 'NoOfPoints:=', 2])
pts.append(['NAME:PLPoint', 'X:=', '0.289000mm', 'Y:=', '1.289000mm', 'Z:=', '0.0mm'])
segs.append(['NAME:PLSegment', 'SegmentType:=', 'Line', 'StartIndex:=', 2, 'NoOfPoints:=', 2])
pts.append(['NAME:PLPoint', 'X:=', '0.111000mm', 'Y:=', '1.289000mm', 'Z:=', '0.0mm'])
segs.append(['NAME:PLSegment', 'SegmentType:=', 'Line', 'StartIndex:=', 3, 'NoOfPoints:=', 2])
pts.append(['NAME:PLPoint', 'X:=', '0.111000mm', 'Y:=', '0.579000mm', 'Z:=', '0.0mm'])
segs.append(['NAME:PLSegment', 'SegmentType:=', 'Line', 'StartIndex:=', 4, 'NoOfPoints:=', 2])
pts.append(['NAME:PLPoint', 'X:=', '-0.111000mm', 'Y:=', '0.579000mm', 'Z:=', '0.0mm'])
segs.append(['NAME:PLSegment', 'SegmentType:=', 'Line', 'StartIndex:=', 5, 'NoOfPoints:=', 2])
pts.append(['NAME:PLPoint', 'X:=', '-0.111000mm', 'Y:=', '1.289000mm', 'Z:=', '0.0mm'])
segs.append(['NAME:PLSegment', 'SegmentType:=', 'Line', 'StartIndex:=', 6, 'NoOfPoints:=', 2])
pts.append(['NAME:PLPoint', 'X:=', '-0.289000mm', 'Y:=', '1.289000mm', 'Z:=', '0.0mm'])
segs.append(['NAME:PLSegment', 'SegmentType:=', 'Line', 'StartIndex:=', 7, 'NoOfPoints:=', 2])
pts.append(['NAME:PLPoint', 'X:=', '-0.289000mm', 'Y:=', '0.579000mm', 'Z:=', '0.0mm'])
segs.append(['NAME:PLSegment', 'SegmentType:=', 'Line', 'StartIndex:=', 8, 'NoOfPoints:=', 2])
pts.append(['NAME:PLPoint', 'X:=', '-0.511000mm', 'Y:=', '0.579000mm', 'Z:=', '0.0mm'])
segs.append(['NAME:PLSegment', 'SegmentType:=', 'Line', 'StartIndex:=', 9, 'NoOfPoints:=', 2])
pts.append(['NAME:PLPoint', 'X:=', '-0.511000mm', 'Y:=', '1.289000mm', 'Z:=', '0.0mm'])
segs.append(['NAME:PLSegment', 'SegmentType:=', 'Line', 'StartIndex:=', 10, 'NoOfPoints:=', 2])
pts.append(['NAME:PLPoint', 'X:=', '-0.689000mm', 'Y:=', '1.289000mm', 'Z:=', '0.0mm'])
segs.append(['NAME:PLSegment', 'SegmentType:=', 'Line', 'StartIndex:=', 11, 'NoOfPoints:=', 2])
pts.append(['NAME:PLPoint', 'X:=', '-0.689000mm', 'Y:=', '0.579000mm', 'Z:=', '0.0mm'])
segs.append(['NAME:PLSegment', 'SegmentType:=', 'Line', 'StartIndex:=', 12, 'NoOfPoints:=', 2])
pts.append(['NAME:PLPoint', 'X:=', '-0.911000mm', 'Y:=', '0.579000mm', 'Z:=', '0.0mm'])
segs.append(['NAME:PLSegment', 'SegmentType:=', 'Line', 'StartIndex:=', 13, 'NoOfPoints:=', 2])
pts.append(['NAME:PLPoint', 'X:=', '-0.911000mm', 'Y:=', '1.289000mm', 'Z:=', '0.0mm'])
segs.append(['NAME:PLSegment', 'SegmentType:=', 'Line', 'StartIndex:=', 14, 'NoOfPoints:=', 2])
pts.append(['NAME:PLPoint', 'X:=', '-1.089000mm', 'Y:=', '1.289000mm', 'Z:=', '0.0mm'])
segs.append(['NAME:PLSegment', 'SegmentType:=', 'Line', 'StartIndex:=', 15, 'NoOfPoints:=', 2])
pts.append(['NAME:PLPoint', 'X:=', '-1.089000mm', 'Y:=', '0.579000mm', 'Z:=', '0.0mm'])
segs.append(['NAME:PLSegment', 'SegmentType:=', 'Line', 'StartIndex:=', 16, 'NoOfPoints:=', 2])
pts.append(['NAME:PLPoint', 'X:=', '-1.311000mm', 'Y:=', '0.579000mm', 'Z:=', '0.0mm'])
segs.append(['NAME:PLSegment', 'SegmentType:=', 'Line', 'StartIndex:=', 17, 'NoOfPoints:=', 2])
pts.append(['NAME:PLPoint', 'X:=', '-1.311000mm', 'Y:=', '1.289000mm', 'Z:=', '0.0mm'])
segs.append(['NAME:PLSegment', 'SegmentType:=', 'Line', 'StartIndex:=', 18, 'NoOfPoints:=', 2])
pts.append(['NAME:PLPoint', 'X:=', '-1.489000mm', 'Y:=', '1.289000mm', 'Z:=', '0.0mm'])
segs.append(['NAME:PLSegment', 'SegmentType:=', 'Line', 'StartIndex:=', 19, 'NoOfPoints:=', 2])
pts.append(['NAME:PLPoint', 'X:=', '-1.489000mm', 'Y:=', '1.050000mm', 'Z:=', '0.0mm'])
segs.append(['NAME:PLSegment', 'SegmentType:=', 'Line', 'StartIndex:=', 20, 'NoOfPoints:=', 2])
pts.append(['NAME:PLPoint', 'X:=', '-1.511000mm', 'Y:=', '1.050000mm', 'Z:=', '0.0mm'])
segs.append(['NAME:PLSegment', 'SegmentType:=', 'Line', 'StartIndex:=', 21, 'NoOfPoints:=', 2])
pts.append(['NAME:PLPoint', 'X:=', '-1.511000mm', 'Y:=', '1.311000mm', 'Z:=', '0.0mm'])
segs.append(['NAME:PLSegment', 'SegmentType:=', 'Line', 'StartIndex:=', 22, 'NoOfPoints:=', 2])
pts.append(['NAME:PLPoint', 'X:=', '-1.289000mm', 'Y:=', '1.311000mm', 'Z:=', '0.0mm'])
segs.append(['NAME:PLSegment', 'SegmentType:=', 'Line', 'StartIndex:=', 23, 'NoOfPoints:=', 2])
pts.append(['NAME:PLPoint', 'X:=', '-1.289000mm', 'Y:=', '0.601000mm', 'Z:=', '0.0mm'])
segs.append(['NAME:PLSegment', 'SegmentType:=', 'Line', 'StartIndex:=', 24, 'NoOfPoints:=', 2])
pts.append(['NAME:PLPoint', 'X:=', '-1.111000mm', 'Y:=', '0.601000mm', 'Z:=', '0.0mm'])
segs.append(['NAME:PLSegment', 'SegmentType:=', 'Line', 'StartIndex:=', 25, 'NoOfPoints:=', 2])
pts.append(['NAME:PLPoint', 'X:=', '-1.111000mm', 'Y:=', '1.311000mm', 'Z:=', '0.0mm'])
segs.append(['NAME:PLSegment', 'SegmentType:=', 'Line', 'StartIndex:=', 26, 'NoOfPoints:=', 2])
pts.append(['NAME:PLPoint', 'X:=', '-0.889000mm', 'Y:=', '1.311000mm', 'Z:=', '0.0mm'])
segs.append(['NAME:PLSegment', 'SegmentType:=', 'Line', 'StartIndex:=', 27, 'NoOfPoints:=', 2])
pts.append(['NAME:PLPoint', 'X:=', '-0.889000mm', 'Y:=', '0.601000mm', 'Z:=', '0.0mm'])
segs.append(['NAME:PLSegment', 'SegmentType:=', 'Line', 'StartIndex:=', 28, 'NoOfPoints:=', 2])
pts.append(['NAME:PLPoint', 'X:=', '-0.711000mm', 'Y:=', '0.601000mm', 'Z:=', '0.0mm'])
segs.append(['NAME:PLSegment', 'SegmentType:=', 'Line', 'StartIndex:=', 29, 'NoOfPoints:=', 2])
pts.append(['NAME:PLPoint', 'X:=', '-0.711000mm', 'Y:=', '1.311000mm', 'Z:=', '0.0mm'])
segs.append(['NAME:PLSegment', 'SegmentType:=', 'Line', 'StartIndex:=', 30, 'NoOfPoints:=', 2])
pts.append(['NAME:PLPoint', 'X:=', '-0.489000mm', 'Y:=', '1.311000mm', 'Z:=', '0.0mm'])
segs.append(['NAME:PLSegment', 'SegmentType:=', 'Line', 'StartIndex:=', 31, 'NoOfPoints:=', 2])
pts.append(['NAME:PLPoint', 'X:=', '-0.489000mm', 'Y:=', '0.601000mm', 'Z:=', '0.0mm'])
segs.append(['NAME:PLSegment', 'SegmentType:=', 'Line', 'StartIndex:=', 32, 'NoOfPoints:=', 2])
pts.append(['NAME:PLPoint', 'X:=', '-0.311000mm', 'Y:=', '0.601000mm', 'Z:=', '0.0mm'])
segs.append(['NAME:PLSegment', 'SegmentType:=', 'Line', 'StartIndex:=', 33, 'NoOfPoints:=', 2])
pts.append(['NAME:PLPoint', 'X:=', '-0.311000mm', 'Y:=', '1.311000mm', 'Z:=', '0.0mm'])
segs.append(['NAME:PLSegment', 'SegmentType:=', 'Line', 'StartIndex:=', 34, 'NoOfPoints:=', 2])
pts.append(['NAME:PLPoint', 'X:=', '-0.089000mm', 'Y:=', '1.311000mm', 'Z:=', '0.0mm'])
segs.append(['NAME:PLSegment', 'SegmentType:=', 'Line', 'StartIndex:=', 35, 'NoOfPoints:=', 2])
pts.append(['NAME:PLPoint', 'X:=', '-0.089000mm', 'Y:=', '0.601000mm', 'Z:=', '0.0mm'])
segs.append(['NAME:PLSegment', 'SegmentType:=', 'Line', 'StartIndex:=', 36, 'NoOfPoints:=', 2])
pts.append(['NAME:PLPoint', 'X:=', '0.089000mm', 'Y:=', '0.601000mm', 'Z:=', '0.0mm'])
segs.append(['NAME:PLSegment', 'SegmentType:=', 'Line', 'StartIndex:=', 37, 'NoOfPoints:=', 2])
pts.append(['NAME:PLPoint', 'X:=', '0.089000mm', 'Y:=', '1.311000mm', 'Z:=', '0.0mm'])
segs.append(['NAME:PLSegment', 'SegmentType:=', 'Line', 'StartIndex:=', 38, 'NoOfPoints:=', 2])
pts.append(['NAME:PLPoint', 'X:=', '0.311000mm', 'Y:=', '1.311000mm', 'Z:=', '0.0mm'])
segs.append(['NAME:PLSegment', 'SegmentType:=', 'Line', 'StartIndex:=', 39, 'NoOfPoints:=', 2])
pts.append(['NAME:PLPoint', 'X:=', '0.311000mm', 'Y:=', '0.601000mm', 'Z:=', '0.0mm'])
segs.append(['NAME:PLSegment', 'SegmentType:=', 'Line', 'StartIndex:=', 40, 'NoOfPoints:=', 2])
pts.append(['NAME:PLPoint', 'X:=', '0.489000mm', 'Y:=', '0.601000mm', 'Z:=', '0.0mm'])
segs.append(['NAME:PLSegment', 'SegmentType:=', 'Line', 'StartIndex:=', 41, 'NoOfPoints:=', 2])
pts.append(['NAME:PLPoint', 'X:=', '0.489000mm', 'Y:=', '0.950000mm', 'Z:=', '0.0mm'])
segs.append(['NAME:PLSegment', 'SegmentType:=', 'Line', 'StartIndex:=', 42, 'NoOfPoints:=', 2])
pts.append(['NAME:PLPoint', 'X:=', '0.511000mm', 'Y:=', '0.950000mm', 'Z:=', '0.0mm'])
segs.append(['NAME:PLSegment', 'SegmentType:=', 'Line', 'StartIndex:=', 43, 'NoOfPoints:=', 2])
pts.append(['NAME:PLPoint', 'X:=', '0.511000mm', 'Y:=', '0.579000mm', 'Z:=', '0.0mm'])
oEditor.CreatePolyline(
    ['NAME:PolylineParameters', 'IsPolylineCovered:=', True, 'IsPolylineClosed:=', True, pts, segs],
    [
        'NAME:Attributes',
        'Name:=', 'cut_RM1_45',
        'Flags:=', '',
        'Color:=', '(255 100 100)',
        'Transparency:=', 0.0,
        'PartCoordinateSystem:=', 'Global',
        'UDMId:=', '',
        'MaterialName:=', 'vacuum',
        'SolveInside:=', True
    ]
)
# Element: trace_RS1_46
pts = ['NAME:PolylinePoints']
segs = ['NAME:PolylineSegments']
pts.append(['NAME:PLPoint', 'X:=', '-2.925000mm', 'Y:=', '2.003767mm', 'Z:=', '0.0mm'])
segs.append(['NAME:PLSegment', 'SegmentType:=', 'Line', 'StartIndex:=', 0, 'NoOfPoints:=', 2])
pts.append(['NAME:PLPoint', 'X:=', '0.579970mm', 'Y:=', '0.998037mm', 'Z:=', '0.0mm'])
segs.append(['NAME:PLSegment', 'SegmentType:=', 'Line', 'StartIndex:=', 1, 'NoOfPoints:=', 2])
pts.append(['NAME:PLPoint', 'X:=', '0.579543mm', 'Y:=', '0.995000mm', 'Z:=', '0.0mm'])
segs.append(['NAME:PLSegment', 'SegmentType:=', 'Line', 'StartIndex:=', 2, 'NoOfPoints:=', 2])
pts.append(['NAME:PLPoint', 'X:=', '0.550000mm', 'Y:=', '0.995000mm', 'Z:=', '0.0mm'])
segs.append(['NAME:PLSegment', 'SegmentType:=', 'Line', 'StartIndex:=', 3, 'NoOfPoints:=', 2])
pts.append(['NAME:PLPoint', 'X:=', '0.550000mm', 'Y:=', '0.996233mm', 'Z:=', '0.0mm'])
segs.append(['NAME:PLSegment', 'SegmentType:=', 'Line', 'StartIndex:=', 4, 'NoOfPoints:=', 2])
pts.append(['NAME:PLPoint', 'X:=', '-2.954970mm', 'Y:=', '2.001963mm', 'Z:=', '0.0mm'])
segs.append(['NAME:PLSegment', 'SegmentType:=', 'Line', 'StartIndex:=', 5, 'NoOfPoints:=', 2])
pts.append(['NAME:PLPoint', 'X:=', '-2.954543mm', 'Y:=', '2.005000mm', 'Z:=', '0.0mm'])
segs.append(['NAME:PLSegment', 'SegmentType:=', 'Line', 'StartIndex:=', 6, 'NoOfPoints:=', 2])
pts.append(['NAME:PLPoint', 'X:=', '-2.925000mm', 'Y:=', '2.005000mm', 'Z:=', '0.0mm'])
segs.append(['NAME:PLSegment', 'SegmentType:=', 'Line', 'StartIndex:=', 7, 'NoOfPoints:=', 2])
pts.append(['NAME:PLPoint', 'X:=', '-2.925000mm', 'Y:=', '2.003767mm', 'Z:=', '0.0mm'])
oEditor.CreatePolyline(
    ['NAME:PolylineParameters', 'IsPolylineCovered:=', True, 'IsPolylineClosed:=', True, pts, segs],
    [
        'NAME:Attributes',
        'Name:=', 'trace_RS1_46',
        'Flags:=', '',
        'Color:=', '(200 220 255)',
        'Transparency:=', 0.0,
        'PartCoordinateSystem:=', 'Global',
        'UDMId:=', '',
        'MaterialName:=', 'vacuum',
        'SolveInside:=', True
    ]
)
# Element: cut_RS1_47
pts = ['NAME:PolylinePoints']
segs = ['NAME:PolylineSegments']
pts.append(['NAME:PLPoint', 'X:=', '-2.925000mm', 'Y:=', '2.010009mm', 'Z:=', '0.0mm'])
segs.append(['NAME:PLSegment', 'SegmentType:=', 'Line', 'StartIndex:=', 0, 'NoOfPoints:=', 2])
pts.append(['NAME:PLPoint', 'X:=', '0.609934mm', 'Y:=', '0.995681mm', 'Z:=', '0.0mm'])
segs.append(['NAME:PLSegment', 'SegmentType:=', 'Line', 'StartIndex:=', 1, 'NoOfPoints:=', 2])
pts.append(['NAME:PLPoint', 'X:=', '0.608994mm', 'Y:=', '0.989000mm', 'Z:=', '0.0mm'])
segs.append(['NAME:PLSegment', 'SegmentType:=', 'Line', 'StartIndex:=', 2, 'NoOfPoints:=', 2])
pts.append(['NAME:PLPoint', 'X:=', '0.550000mm', 'Y:=', '0.989000mm', 'Z:=', '0.0mm'])
segs.append(['NAME:PLSegment', 'SegmentType:=', 'Line', 'StartIndex:=', 3, 'NoOfPoints:=', 2])
pts.append(['NAME:PLPoint', 'X:=', '0.550000mm', 'Y:=', '0.989991mm', 'Z:=', '0.0mm'])
segs.append(['NAME:PLSegment', 'SegmentType:=', 'Line', 'StartIndex:=', 4, 'NoOfPoints:=', 2])
pts.append(['NAME:PLPoint', 'X:=', '-2.984934mm', 'Y:=', '2.004319mm', 'Z:=', '0.0mm'])
segs.append(['NAME:PLSegment', 'SegmentType:=', 'Line', 'StartIndex:=', 5, 'NoOfPoints:=', 2])
pts.append(['NAME:PLPoint', 'X:=', '-2.983994mm', 'Y:=', '2.011000mm', 'Z:=', '0.0mm'])
segs.append(['NAME:PLSegment', 'SegmentType:=', 'Line', 'StartIndex:=', 6, 'NoOfPoints:=', 2])
pts.append(['NAME:PLPoint', 'X:=', '-2.925000mm', 'Y:=', '2.011000mm', 'Z:=', '0.0mm'])
segs.append(['NAME:PLSegment', 'SegmentType:=', 'Line', 'StartIndex:=', 7, 'NoOfPoints:=', 2])
pts.append(['NAME:PLPoint', 'X:=', '-2.925000mm', 'Y:=', '2.010009mm', 'Z:=', '0.0mm'])
oEditor.CreatePolyline(
    ['NAME:PolylineParameters', 'IsPolylineCovered:=', True, 'IsPolylineClosed:=', True, pts, segs],
    [
        'NAME:Attributes',
        'Name:=', 'cut_RS1_47',
        'Flags:=', '',
        'Color:=', '(255 100 100)',
        'Transparency:=', 0.0,
        'PartCoordinateSystem:=', 'Global',
        'UDMId:=', '',
        'MaterialName:=', 'vacuum',
        'SolveInside:=', True
    ]
)
# Element: trace_RS2_48
pts = ['NAME:PolylinePoints']
segs = ['NAME:PolylineSegments']
pts.append(['NAME:PLPoint', 'X:=', '-0.425000mm', 'Y:=', '0.671523mm', 'Z:=', '0.0mm'])
segs.append(['NAME:PLSegment', 'SegmentType:=', 'Line', 'StartIndex:=', 0, 'NoOfPoints:=', 2])
pts.append(['NAME:PLPoint', 'X:=', '-0.425000mm', 'Y:=', '0.670000mm', 'Z:=', '0.0mm'])
segs.append(['NAME:PLSegment', 'SegmentType:=', 'Line', 'StartIndex:=', 1, 'NoOfPoints:=', 2])
pts.append(['NAME:PLPoint', 'X:=', '-0.454502mm', 'Y:=', '0.670000mm', 'Z:=', '0.0mm'])
segs.append(['NAME:PLSegment', 'SegmentType:=', 'Line', 'StartIndex:=', 2, 'NoOfPoints:=', 2])
pts.append(['NAME:PLPoint', 'X:=', '-0.454710mm', 'Y:=', '0.671156mm', 'Z:=', '0.0mm'])
segs.append(['NAME:PLSegment', 'SegmentType:=', 'Line', 'StartIndex:=', 3, 'NoOfPoints:=', 2])
pts.append(['NAME:PLPoint', 'X:=', '0.444101mm', 'Y:=', '1.005000mm', 'Z:=', '0.0mm'])
segs.append(['NAME:PLSegment', 'SegmentType:=', 'Line', 'StartIndex:=', 4, 'NoOfPoints:=', 2])
pts.append(['NAME:PLPoint', 'X:=', '0.450000mm', 'Y:=', '1.005000mm', 'Z:=', '0.0mm'])
segs.append(['NAME:PLSegment', 'SegmentType:=', 'Line', 'StartIndex:=', 5, 'NoOfPoints:=', 2])
pts.append(['NAME:PLPoint', 'X:=', '0.450000mm', 'Y:=', '0.995000mm', 'Z:=', '0.0mm'])
segs.append(['NAME:PLSegment', 'SegmentType:=', 'Line', 'StartIndex:=', 6, 'NoOfPoints:=', 2])
pts.append(['NAME:PLPoint', 'X:=', '0.445899mm', 'Y:=', '0.995000mm', 'Z:=', '0.0mm'])
segs.append(['NAME:PLSegment', 'SegmentType:=', 'Line', 'StartIndex:=', 7, 'NoOfPoints:=', 2])
pts.append(['NAME:PLPoint', 'X:=', '-0.425000mm', 'Y:=', '0.671523mm', 'Z:=', '0.0mm'])
oEditor.CreatePolyline(
    ['NAME:PolylineParameters', 'IsPolylineCovered:=', True, 'IsPolylineClosed:=', True, pts, segs],
    [
        'NAME:Attributes',
        'Name:=', 'trace_RS2_48',
        'Flags:=', '',
        'Color:=', '(200 220 255)',
        'Transparency:=', 0.0,
        'PartCoordinateSystem:=', 'Global',
        'UDMId:=', '',
        'MaterialName:=', 'vacuum',
        'SolveInside:=', True
    ]
)
# Element: cut_RS2_49
pts = ['NAME:PolylinePoints']
segs = ['NAME:PolylineSegments']
pts.append(['NAME:PLPoint', 'X:=', '-0.425000mm', 'Y:=', '0.665123mm', 'Z:=', '0.0mm'])
segs.append(['NAME:PLSegment', 'SegmentType:=', 'Line', 'StartIndex:=', 0, 'NoOfPoints:=', 2])
pts.append(['NAME:PLPoint', 'X:=', '-0.425000mm', 'Y:=', '0.664000mm', 'Z:=', '0.0mm'])
segs.append(['NAME:PLSegment', 'SegmentType:=', 'Line', 'StartIndex:=', 1, 'NoOfPoints:=', 2])
pts.append(['NAME:PLPoint', 'X:=', '-0.483904mm', 'Y:=', '0.664000mm', 'Z:=', '0.0mm'])
segs.append(['NAME:PLSegment', 'SegmentType:=', 'Line', 'StartIndex:=', 2, 'NoOfPoints:=', 2])
pts.append(['NAME:PLPoint', 'X:=', '-0.484361mm', 'Y:=', '0.666543mm', 'Z:=', '0.0mm'])
segs.append(['NAME:PLSegment', 'SegmentType:=', 'Line', 'StartIndex:=', 3, 'NoOfPoints:=', 2])
pts.append(['NAME:PLPoint', 'X:=', '0.443023mm', 'Y:=', '1.011000mm', 'Z:=', '0.0mm'])
segs.append(['NAME:PLSegment', 'SegmentType:=', 'Line', 'StartIndex:=', 4, 'NoOfPoints:=', 2])
pts.append(['NAME:PLPoint', 'X:=', '0.450000mm', 'Y:=', '1.011000mm', 'Z:=', '0.0mm'])
segs.append(['NAME:PLSegment', 'SegmentType:=', 'Line', 'StartIndex:=', 5, 'NoOfPoints:=', 2])
pts.append(['NAME:PLPoint', 'X:=', '0.450000mm', 'Y:=', '0.989000mm', 'Z:=', '0.0mm'])
segs.append(['NAME:PLSegment', 'SegmentType:=', 'Line', 'StartIndex:=', 6, 'NoOfPoints:=', 2])
pts.append(['NAME:PLPoint', 'X:=', '0.446977mm', 'Y:=', '0.989000mm', 'Z:=', '0.0mm'])
segs.append(['NAME:PLSegment', 'SegmentType:=', 'Line', 'StartIndex:=', 7, 'NoOfPoints:=', 2])
pts.append(['NAME:PLPoint', 'X:=', '-0.425000mm', 'Y:=', '0.665123mm', 'Z:=', '0.0mm'])
oEditor.CreatePolyline(
    ['NAME:PolylineParameters', 'IsPolylineCovered:=', True, 'IsPolylineClosed:=', True, pts, segs],
    [
        'NAME:Attributes',
        'Name:=', 'cut_RS2_49',
        'Flags:=', '',
        'Color:=', '(255 100 100)',
        'Transparency:=', 0.0,
        'PartCoordinateSystem:=', 'Global',
        'UDMId:=', '',
        'MaterialName:=', 'vacuum',
        'SolveInside:=', True
    ]
)
# Element: trace_RS3_50
pts = ['NAME:PolylinePoints']
segs = ['NAME:PolylineSegments']
pts.append(['NAME:PLPoint', 'X:=', '-0.550000mm', 'Y:=', '1.003615mm', 'Z:=', '0.0mm'])
segs.append(['NAME:PLSegment', 'SegmentType:=', 'Line', 'StartIndex:=', 0, 'NoOfPoints:=', 2])
pts.append(['NAME:PLPoint', 'X:=', '0.454849mm', 'Y:=', '0.672066mm', 'Z:=', '0.0mm'])
segs.append(['NAME:PLSegment', 'SegmentType:=', 'Line', 'StartIndex:=', 1, 'NoOfPoints:=', 2])
pts.append(['NAME:PLPoint', 'X:=', '0.454517mm', 'Y:=', '0.670000mm', 'Z:=', '0.0mm'])
segs.append(['NAME:PLSegment', 'SegmentType:=', 'Line', 'StartIndex:=', 2, 'NoOfPoints:=', 2])
pts.append(['NAME:PLPoint', 'X:=', '0.425000mm', 'Y:=', '0.670000mm', 'Z:=', '0.0mm'])
segs.append(['NAME:PLSegment', 'SegmentType:=', 'Line', 'StartIndex:=', 3, 'NoOfPoints:=', 2])
pts.append(['NAME:PLPoint', 'X:=', '0.425000mm', 'Y:=', '0.671385mm', 'Z:=', '0.0mm'])
segs.append(['NAME:PLSegment', 'SegmentType:=', 'Line', 'StartIndex:=', 4, 'NoOfPoints:=', 2])
pts.append(['NAME:PLPoint', 'X:=', '-0.579849mm', 'Y:=', '1.002934mm', 'Z:=', '0.0mm'])
segs.append(['NAME:PLSegment', 'SegmentType:=', 'Line', 'StartIndex:=', 5, 'NoOfPoints:=', 2])
pts.append(['NAME:PLPoint', 'X:=', '-0.579517mm', 'Y:=', '1.005000mm', 'Z:=', '0.0mm'])
segs.append(['NAME:PLSegment', 'SegmentType:=', 'Line', 'StartIndex:=', 6, 'NoOfPoints:=', 2])
pts.append(['NAME:PLPoint', 'X:=', '-0.550000mm', 'Y:=', '1.005000mm', 'Z:=', '0.0mm'])
segs.append(['NAME:PLSegment', 'SegmentType:=', 'Line', 'StartIndex:=', 7, 'NoOfPoints:=', 2])
pts.append(['NAME:PLPoint', 'X:=', '-0.550000mm', 'Y:=', '1.003615mm', 'Z:=', '0.0mm'])
oEditor.CreatePolyline(
    ['NAME:PolylineParameters', 'IsPolylineCovered:=', True, 'IsPolylineClosed:=', True, pts, segs],
    [
        'NAME:Attributes',
        'Name:=', 'trace_RS3_50',
        'Flags:=', '',
        'Color:=', '(200 220 255)',
        'Transparency:=', 0.0,
        'PartCoordinateSystem:=', 'Global',
        'UDMId:=', '',
        'MaterialName:=', 'vacuum',
        'SolveInside:=', True
    ]
)
# Element: cut_RS3_51
pts = ['NAME:PolylinePoints']
segs = ['NAME:PolylineSegments']
pts.append(['NAME:PLPoint', 'X:=', '-0.550000mm', 'Y:=', '1.009934mm', 'Z:=', '0.0mm'])
segs.append(['NAME:PLSegment', 'SegmentType:=', 'Line', 'StartIndex:=', 0, 'NoOfPoints:=', 2])
pts.append(['NAME:PLPoint', 'X:=', '0.484668mm', 'Y:=', '0.668545mm', 'Z:=', '0.0mm'])
segs.append(['NAME:PLSegment', 'SegmentType:=', 'Line', 'StartIndex:=', 1, 'NoOfPoints:=', 2])
pts.append(['NAME:PLPoint', 'X:=', '0.483938mm', 'Y:=', '0.664000mm', 'Z:=', '0.0mm'])
segs.append(['NAME:PLSegment', 'SegmentType:=', 'Line', 'StartIndex:=', 2, 'NoOfPoints:=', 2])
pts.append(['NAME:PLPoint', 'X:=', '0.425000mm', 'Y:=', '0.664000mm', 'Z:=', '0.0mm'])
segs.append(['NAME:PLSegment', 'SegmentType:=', 'Line', 'StartIndex:=', 3, 'NoOfPoints:=', 2])
pts.append(['NAME:PLPoint', 'X:=', '0.425000mm', 'Y:=', '0.665066mm', 'Z:=', '0.0mm'])
segs.append(['NAME:PLSegment', 'SegmentType:=', 'Line', 'StartIndex:=', 4, 'NoOfPoints:=', 2])
pts.append(['NAME:PLPoint', 'X:=', '-0.609668mm', 'Y:=', '1.006455mm', 'Z:=', '0.0mm'])
segs.append(['NAME:PLSegment', 'SegmentType:=', 'Line', 'StartIndex:=', 5, 'NoOfPoints:=', 2])
pts.append(['NAME:PLPoint', 'X:=', '-0.608938mm', 'Y:=', '1.011000mm', 'Z:=', '0.0mm'])
segs.append(['NAME:PLSegment', 'SegmentType:=', 'Line', 'StartIndex:=', 6, 'NoOfPoints:=', 2])
pts.append(['NAME:PLPoint', 'X:=', '-0.550000mm', 'Y:=', '1.011000mm', 'Z:=', '0.0mm'])
segs.append(['NAME:PLSegment', 'SegmentType:=', 'Line', 'StartIndex:=', 7, 'NoOfPoints:=', 2])
pts.append(['NAME:PLPoint', 'X:=', '-0.550000mm', 'Y:=', '1.009934mm', 'Z:=', '0.0mm'])
oEditor.CreatePolyline(
    ['NAME:PolylineParameters', 'IsPolylineCovered:=', True, 'IsPolylineClosed:=', True, pts, segs],
    [
        'NAME:Attributes',
        'Name:=', 'cut_RS3_51',
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
cut_list = ['rect_pk_Q1_2', 'rect_pk_Q2_7', 'rect_pk_Q3_12', 'rect_pk_Q5_17', 'rect_pk_Q6_22', 'rect_pk_Q7_27', 'rect_pk_Q4_32', 'cl_etcher_Q4_36', 'pocket_LP1_38', 'pocket_LP2_40', 'pocket_LP3_42', 'pocket_LP4_44', 'pocket_LP5_46', 'pocket_LP6_48', 'pocket_LP7_50', 'a_wire_sub_Q1_1', 'b_wire_sub_Q1_3', 'a_wire_sub_Q2_5', 'b_wire_sub_Q2_7', 'a_wire_sub_Q3_9', 'b_wire_sub_Q3_11', 'a_wire_sub_Q5_13', 'b_wire_sub_Q5_15', 'a_wire_sub_Q6_17', 'b_wire_sub_Q6_19', 'a_wire_sub_Q7_21', 'b_wire_sub_Q7_23', 'a_wire_sub_Q4_25', 'b_wire_sub_Q4_27', 'prime_cpw_sub_Lt1_29', 'second_cpw_sub_Lt1_31', 'prime_cpw_sub_Lt2_33', 'second_cpw_sub_Lt2_35', 'prime_cpw_sub_Lt3_37', 'second_cpw_sub_Lt3_39', 'prime_cpw_sub_Lt4_41', 'second_cpw_sub_Lt4_43', 'cut_RM1_45', 'cut_RS1_47', 'cut_RS2_49', 'cut_RS3_51']
try:
    existing = set(oEditor.GetMatchedObjectName('*')) if hasattr(oEditor, 'GetMatchedObjectName') else set(cut_list)
    valid_cuts = [c for c in cut_list if c in existing] if existing else cut_list
    if valid_cuts:
        oEditor.Subtract(
            [
                'NAME:Selections',
                'Blank Parts:=', 'ground_main_plane',
                'Tool Parts:=', ','.join(valid_cuts)
            ],
            [
                'NAME:SubtractParameters',
                'KeepOriginals:=', False
            ]
        )
        print('[+] Successfully subtracted CPW slots and pockets from Ground Plane.')
except Exception as sub_err:
    print('[!] Subtract notice: ' + str(sub_err))

# --- 6. Assign Perfect E to Ground Plane & Metal Traces/Pads ---
metal_list = ['ground_main_plane'] + ['pad_top_Q1_0', 'pad_bot_Q1_1', 'a_connector_pad_Q1_3', 'b_connector_pad_Q1_4', 'pad_top_Q2_5', 'pad_bot_Q2_6', 'a_connector_pad_Q2_8', 'b_connector_pad_Q2_9', 'pad_top_Q3_10', 'pad_bot_Q3_11', 'a_connector_pad_Q3_13', 'b_connector_pad_Q3_14', 'pad_top_Q5_15', 'pad_bot_Q5_16', 'a_connector_pad_Q5_18', 'b_connector_pad_Q5_19', 'pad_top_Q6_20', 'pad_bot_Q6_21', 'a_connector_pad_Q6_23', 'b_connector_pad_Q6_24', 'pad_top_Q7_25', 'pad_bot_Q7_26', 'a_connector_pad_Q7_28', 'b_connector_pad_Q7_29', 'pad_top_Q4_30', 'pad_bot_Q4_31', 'a_connector_pad_Q4_33', 'b_connector_pad_Q4_34', 'cl_metal_Q4_35', 'launch_pad_LP1_37', 'launch_pad_LP2_39', 'launch_pad_LP3_41', 'launch_pad_LP4_43', 'launch_pad_LP5_45', 'launch_pad_LP6_47', 'launch_pad_LP7_49', 'a_wire_Q1_0', 'b_wire_Q1_2', 'a_wire_Q2_4', 'b_wire_Q2_6', 'a_wire_Q3_8', 'b_wire_Q3_10', 'a_wire_Q5_12', 'b_wire_Q5_14', 'a_wire_Q6_16', 'b_wire_Q6_18', 'a_wire_Q7_20', 'b_wire_Q7_22', 'a_wire_Q4_24', 'b_wire_Q4_26', 'prime_cpw_Lt1_28', 'second_cpw_Lt1_30', 'prime_cpw_Lt2_32', 'second_cpw_Lt2_34', 'prime_cpw_Lt3_36', 'second_cpw_Lt3_38', 'prime_cpw_Lt4_40', 'second_cpw_Lt4_42', 'trace_RM1_44', 'trace_RS1_46', 'trace_RS2_48', 'trace_RS3_50']
try:
    existing = set(oEditor.GetMatchedObjectName('*')) if hasattr(oEditor, 'GetMatchedObjectName') else set(metal_list)
    valid_metals = [m for m in metal_list if m in existing] if existing else metal_list
    if valid_metals:
        oBoundarySetup.AssignPerfectE(
            [
                'NAME:PerfE_Superconductors',
                'Objects:=', valid_metals,
                'InfGroundPlane:=', False
            ]
        )
        print('[+] Assigned Perfect E Boundary to Superconducting metallization.')
except Exception as pe_err:
    print('[!] Perfect E notice: ' + str(pe_err))

# --- 7. Josephson Junction Sheet on Q4 (Simon's exact 57:45 setup) ---
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
    pts_jj = ['NAME:PolylinePoints']
    pts_jj.append(['NAME:PLPoint', 'X:=', '0.0mm', 'Y:=', '0.855mm', 'Z:=', '0.0mm'])
    pts_jj.append(['NAME:PLPoint', 'X:=', '0.0mm', 'Y:=', '0.885mm', 'Z:=', '0.0mm'])
    segs_jj = ['NAME:PolylineSegments']
    segs_jj.append(['NAME:PLSegment', 'SegmentType:=', 'Line', 'StartIndex:=', 0, 'NoOfPoints:=', 2])
    oEditor.CreatePolyline(
        ['NAME:PolylineParameters', 'IsPolylineCovered:=', False, 'IsPolylineClosed:=', False, pts_jj, segs_jj],
        [
            'NAME:Attributes',
            'Name:=', 'JJ_Q4_line',
            'Flags:=', '',
            'Color:=', '(255 0 0)',
            'Transparency:=', 0.0,
            'PartCoordinateSystem:=', 'Global',
            'UDMId:=', '',
            'MaterialName:=', 'vacuum',
            'SolveInside:=', True
        ]
    )
except Exception:
    pass

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
    print('[+] Assigned Q4 Lumped RLC boundary (Lj=12.31nH, Cj=2.0fF) successfully!')
except Exception as rlc_err:
    print('[*] Note on Lumped RLC assignment: ' + str(rlc_err))

# --- 8. Fit All Geometry in 3D Modeler View ---
oEditor.FitAll()
print('[SUCCESS] Simon Exact Video Chip fully generated in Ansys HFSS!')