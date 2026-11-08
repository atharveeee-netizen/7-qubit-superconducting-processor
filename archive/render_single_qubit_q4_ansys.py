# =====================================================================
# Ansys HFSS Standalone Python Script - Simon Quantum Hardware
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

# =====================================================================
# DESIGN: Simon_Q4_Single_Qubit
# =====================================================================
design_name = 'Simon_Q4_Single_Qubit'
try:
    d_names = [d.GetName() for d in oProject.GetDesigns()]
except Exception:
    d_names = []
if design_name in d_names:
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

try:
    for b in list(oBoundarySetup.GetBoundaries()):
        try:
            oBoundarySetup.DeleteBoundaries([b])
        except Exception:
            pass
except Exception:
    pass

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

# Substrate Box (5.0mm x 5.0mm x 0.5mm)
oEditor.CreateBox(
    [
        'NAME:BoxParameters',
        'XPosition:=', '-2.5mm',
        'YPosition:=', '-2.5mm',
        'ZPosition:=', '-0.5mm',
        'XSize:=', '5.0mm',
        'YSize:=', '5.0mm',
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

# Ground Plane Sheet (5.0mm x 5.0mm)
oEditor.CreateRectangle(
    [
        'NAME:RectangleParameters',
        'IsCovered:=', True,
        'XStart:=', '-2.5mm',
        'YStart:=', '-2.5mm',
        'ZStart:=', '0.0mm',
        'Width:=', '5.0mm',
        'Height:=', '5.0mm',
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

# Element: pad_top_Q4_0
pts = ['NAME:PolylinePoints']
segs = ['NAME:PolylineSegments']
pts.append(['NAME:PLPoint', 'X:=', '-0.227500mm', 'Y:=', '0.015000mm', 'Z:=', '0.0mm'])
segs.append(['NAME:PLSegment', 'SegmentType:=', 'Line', 'StartIndex:=', 0, 'NoOfPoints:=', 2])
pts.append(['NAME:PLPoint', 'X:=', '0.227500mm', 'Y:=', '0.015000mm', 'Z:=', '0.0mm'])
segs.append(['NAME:PLSegment', 'SegmentType:=', 'Line', 'StartIndex:=', 1, 'NoOfPoints:=', 2])
pts.append(['NAME:PLPoint', 'X:=', '0.227500mm', 'Y:=', '0.105000mm', 'Z:=', '0.0mm'])
segs.append(['NAME:PLSegment', 'SegmentType:=', 'Line', 'StartIndex:=', 2, 'NoOfPoints:=', 2])
pts.append(['NAME:PLPoint', 'X:=', '-0.227500mm', 'Y:=', '0.105000mm', 'Z:=', '0.0mm'])
segs.append(['NAME:PLSegment', 'SegmentType:=', 'Line', 'StartIndex:=', 3, 'NoOfPoints:=', 2])
pts.append(['NAME:PLPoint', 'X:=', '-0.227500mm', 'Y:=', '0.015000mm', 'Z:=', '0.0mm'])
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
pts.append(['NAME:PLPoint', 'X:=', '-0.227500mm', 'Y:=', '-0.105000mm', 'Z:=', '0.0mm'])
segs.append(['NAME:PLSegment', 'SegmentType:=', 'Line', 'StartIndex:=', 0, 'NoOfPoints:=', 2])
pts.append(['NAME:PLPoint', 'X:=', '0.227500mm', 'Y:=', '-0.105000mm', 'Z:=', '0.0mm'])
segs.append(['NAME:PLSegment', 'SegmentType:=', 'Line', 'StartIndex:=', 1, 'NoOfPoints:=', 2])
pts.append(['NAME:PLPoint', 'X:=', '0.227500mm', 'Y:=', '-0.015000mm', 'Z:=', '0.0mm'])
segs.append(['NAME:PLSegment', 'SegmentType:=', 'Line', 'StartIndex:=', 2, 'NoOfPoints:=', 2])
pts.append(['NAME:PLPoint', 'X:=', '-0.227500mm', 'Y:=', '-0.015000mm', 'Z:=', '0.0mm'])
segs.append(['NAME:PLSegment', 'SegmentType:=', 'Line', 'StartIndex:=', 3, 'NoOfPoints:=', 2])
pts.append(['NAME:PLPoint', 'X:=', '-0.227500mm', 'Y:=', '-0.105000mm', 'Z:=', '0.0mm'])
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
pts.append(['NAME:PLPoint', 'X:=', '-0.325000mm', 'Y:=', '-0.325000mm', 'Z:=', '0.0mm'])
segs.append(['NAME:PLSegment', 'SegmentType:=', 'Line', 'StartIndex:=', 0, 'NoOfPoints:=', 2])
pts.append(['NAME:PLPoint', 'X:=', '0.325000mm', 'Y:=', '-0.325000mm', 'Z:=', '0.0mm'])
segs.append(['NAME:PLSegment', 'SegmentType:=', 'Line', 'StartIndex:=', 1, 'NoOfPoints:=', 2])
pts.append(['NAME:PLPoint', 'X:=', '0.325000mm', 'Y:=', '0.325000mm', 'Z:=', '0.0mm'])
segs.append(['NAME:PLSegment', 'SegmentType:=', 'Line', 'StartIndex:=', 2, 'NoOfPoints:=', 2])
pts.append(['NAME:PLPoint', 'X:=', '-0.325000mm', 'Y:=', '0.325000mm', 'Z:=', '0.0mm'])
segs.append(['NAME:PLSegment', 'SegmentType:=', 'Line', 'StartIndex:=', 3, 'NoOfPoints:=', 2])
pts.append(['NAME:PLPoint', 'X:=', '-0.325000mm', 'Y:=', '-0.325000mm', 'Z:=', '0.0mm'])
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
# Element: a_connector_pad_Q4_3
pts = ['NAME:PolylinePoints']
segs = ['NAME:PolylineSegments']
pts.append(['NAME:PLPoint', 'X:=', '-0.177500mm', 'Y:=', '-0.120000mm', 'Z:=', '0.0mm'])
segs.append(['NAME:PLSegment', 'SegmentType:=', 'Line', 'StartIndex:=', 0, 'NoOfPoints:=', 2])
pts.append(['NAME:PLPoint', 'X:=', '-0.227500mm', 'Y:=', '-0.120000mm', 'Z:=', '0.0mm'])
segs.append(['NAME:PLSegment', 'SegmentType:=', 'Line', 'StartIndex:=', 1, 'NoOfPoints:=', 2])
pts.append(['NAME:PLPoint', 'X:=', '-0.227500mm', 'Y:=', '-0.150000mm', 'Z:=', '0.0mm'])
segs.append(['NAME:PLSegment', 'SegmentType:=', 'Line', 'StartIndex:=', 2, 'NoOfPoints:=', 2])
pts.append(['NAME:PLPoint', 'X:=', '-0.177500mm', 'Y:=', '-0.150000mm', 'Z:=', '0.0mm'])
segs.append(['NAME:PLSegment', 'SegmentType:=', 'Line', 'StartIndex:=', 3, 'NoOfPoints:=', 2])
pts.append(['NAME:PLPoint', 'X:=', '-0.177500mm', 'Y:=', '-0.120000mm', 'Z:=', '0.0mm'])
oEditor.CreatePolyline(
    ['NAME:PolylineParameters', 'IsPolylineCovered:=', True, 'IsPolylineClosed:=', True, pts, segs],
    [
        'NAME:Attributes',
        'Name:=', 'a_connector_pad_Q4_3',
        'Flags:=', '',
        'Color:=', '(200 220 255)',
        'Transparency:=', 0.0,
        'PartCoordinateSystem:=', 'Global',
        'UDMId:=', '',
        'MaterialName:=', 'vacuum',
        'SolveInside:=', True
    ]
)
# Element: b_connector_pad_Q4_4
pts = ['NAME:PolylinePoints']
segs = ['NAME:PolylineSegments']
pts.append(['NAME:PLPoint', 'X:=', '0.177500mm', 'Y:=', '-0.120000mm', 'Z:=', '0.0mm'])
segs.append(['NAME:PLSegment', 'SegmentType:=', 'Line', 'StartIndex:=', 0, 'NoOfPoints:=', 2])
pts.append(['NAME:PLPoint', 'X:=', '0.227500mm', 'Y:=', '-0.120000mm', 'Z:=', '0.0mm'])
segs.append(['NAME:PLSegment', 'SegmentType:=', 'Line', 'StartIndex:=', 1, 'NoOfPoints:=', 2])
pts.append(['NAME:PLPoint', 'X:=', '0.227500mm', 'Y:=', '-0.150000mm', 'Z:=', '0.0mm'])
segs.append(['NAME:PLSegment', 'SegmentType:=', 'Line', 'StartIndex:=', 2, 'NoOfPoints:=', 2])
pts.append(['NAME:PLPoint', 'X:=', '0.177500mm', 'Y:=', '-0.150000mm', 'Z:=', '0.0mm'])
segs.append(['NAME:PLSegment', 'SegmentType:=', 'Line', 'StartIndex:=', 3, 'NoOfPoints:=', 2])
pts.append(['NAME:PLPoint', 'X:=', '0.177500mm', 'Y:=', '-0.120000mm', 'Z:=', '0.0mm'])
oEditor.CreatePolyline(
    ['NAME:PolylineParameters', 'IsPolylineCovered:=', True, 'IsPolylineClosed:=', True, pts, segs],
    [
        'NAME:Attributes',
        'Name:=', 'b_connector_pad_Q4_4',
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
pts.append(['NAME:PLPoint', 'X:=', '-0.010000mm', 'Y:=', '-0.417000mm', 'Z:=', '0.0mm'])
segs.append(['NAME:PLSegment', 'SegmentType:=', 'Line', 'StartIndex:=', 0, 'NoOfPoints:=', 2])
pts.append(['NAME:PLPoint', 'X:=', '-0.010000mm', 'Y:=', '-0.347000mm', 'Z:=', '0.0mm'])
segs.append(['NAME:PLSegment', 'SegmentType:=', 'Line', 'StartIndex:=', 1, 'NoOfPoints:=', 2])
pts.append(['NAME:PLPoint', 'X:=', '-0.020000mm', 'Y:=', '-0.347000mm', 'Z:=', '0.0mm'])
segs.append(['NAME:PLSegment', 'SegmentType:=', 'Line', 'StartIndex:=', 2, 'NoOfPoints:=', 2])
pts.append(['NAME:PLPoint', 'X:=', '-0.020000mm', 'Y:=', '-0.337000mm', 'Z:=', '0.0mm'])
segs.append(['NAME:PLSegment', 'SegmentType:=', 'Line', 'StartIndex:=', 3, 'NoOfPoints:=', 2])
pts.append(['NAME:PLPoint', 'X:=', '-0.010000mm', 'Y:=', '-0.337000mm', 'Z:=', '0.0mm'])
segs.append(['NAME:PLSegment', 'SegmentType:=', 'Line', 'StartIndex:=', 4, 'NoOfPoints:=', 2])
pts.append(['NAME:PLPoint', 'X:=', '0.000000mm', 'Y:=', '-0.337000mm', 'Z:=', '0.0mm'])
segs.append(['NAME:PLSegment', 'SegmentType:=', 'Line', 'StartIndex:=', 5, 'NoOfPoints:=', 2])
pts.append(['NAME:PLPoint', 'X:=', '0.000000mm', 'Y:=', '-0.347000mm', 'Z:=', '0.0mm'])
segs.append(['NAME:PLSegment', 'SegmentType:=', 'Line', 'StartIndex:=', 6, 'NoOfPoints:=', 2])
pts.append(['NAME:PLPoint', 'X:=', '0.000000mm', 'Y:=', '-0.417000mm', 'Z:=', '0.0mm'])
segs.append(['NAME:PLSegment', 'SegmentType:=', 'Line', 'StartIndex:=', 7, 'NoOfPoints:=', 2])
pts.append(['NAME:PLPoint', 'X:=', '-0.010000mm', 'Y:=', '-0.417000mm', 'Z:=', '0.0mm'])
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
pts.append(['NAME:PLPoint', 'X:=', '-0.016000mm', 'Y:=', '-0.423000mm', 'Z:=', '0.0mm'])
segs.append(['NAME:PLSegment', 'SegmentType:=', 'Line', 'StartIndex:=', 0, 'NoOfPoints:=', 2])
pts.append(['NAME:PLPoint', 'X:=', '-0.016000mm', 'Y:=', '-0.353000mm', 'Z:=', '0.0mm'])
segs.append(['NAME:PLSegment', 'SegmentType:=', 'Line', 'StartIndex:=', 1, 'NoOfPoints:=', 2])
pts.append(['NAME:PLPoint', 'X:=', '-0.026000mm', 'Y:=', '-0.353000mm', 'Z:=', '0.0mm'])
segs.append(['NAME:PLSegment', 'SegmentType:=', 'Line', 'StartIndex:=', 2, 'NoOfPoints:=', 2])
pts.append(['NAME:PLPoint', 'X:=', '-0.026000mm', 'Y:=', '-0.331000mm', 'Z:=', '0.0mm'])
segs.append(['NAME:PLSegment', 'SegmentType:=', 'Line', 'StartIndex:=', 3, 'NoOfPoints:=', 2])
pts.append(['NAME:PLPoint', 'X:=', '0.006000mm', 'Y:=', '-0.331000mm', 'Z:=', '0.0mm'])
segs.append(['NAME:PLSegment', 'SegmentType:=', 'Line', 'StartIndex:=', 4, 'NoOfPoints:=', 2])
pts.append(['NAME:PLPoint', 'X:=', '0.006000mm', 'Y:=', '-0.423000mm', 'Z:=', '0.0mm'])
segs.append(['NAME:PLSegment', 'SegmentType:=', 'Line', 'StartIndex:=', 5, 'NoOfPoints:=', 2])
pts.append(['NAME:PLPoint', 'X:=', '-0.016000mm', 'Y:=', '-0.423000mm', 'Z:=', '0.0mm'])
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
# Element: a_wire_Q4_0
pts = ['NAME:PolylinePoints']
segs = ['NAME:PolylineSegments']
pts.append(['NAME:PLPoint', 'X:=', '-0.250484mm', 'Y:=', '-0.135000mm', 'Z:=', '0.0mm'])
segs.append(['NAME:PLSegment', 'SegmentType:=', 'Line', 'StartIndex:=', 0, 'NoOfPoints:=', 2])
pts.append(['NAME:PLPoint', 'X:=', '-0.317984mm', 'Y:=', '-0.200000mm', 'Z:=', '0.0mm'])
segs.append(['NAME:PLSegment', 'SegmentType:=', 'Line', 'StartIndex:=', 1, 'NoOfPoints:=', 2])
pts.append(['NAME:PLPoint', 'X:=', '-0.425000mm', 'Y:=', '-0.200000mm', 'Z:=', '0.0mm'])
segs.append(['NAME:PLSegment', 'SegmentType:=', 'Line', 'StartIndex:=', 2, 'NoOfPoints:=', 2])
pts.append(['NAME:PLPoint', 'X:=', '-0.425000mm', 'Y:=', '-0.190000mm', 'Z:=', '0.0mm'])
segs.append(['NAME:PLSegment', 'SegmentType:=', 'Line', 'StartIndex:=', 3, 'NoOfPoints:=', 2])
pts.append(['NAME:PLPoint', 'X:=', '-0.322016mm', 'Y:=', '-0.190000mm', 'Z:=', '0.0mm'])
segs.append(['NAME:PLSegment', 'SegmentType:=', 'Line', 'StartIndex:=', 4, 'NoOfPoints:=', 2])
pts.append(['NAME:PLPoint', 'X:=', '-0.254516mm', 'Y:=', '-0.125000mm', 'Z:=', '0.0mm'])
segs.append(['NAME:PLSegment', 'SegmentType:=', 'Line', 'StartIndex:=', 5, 'NoOfPoints:=', 2])
pts.append(['NAME:PLPoint', 'X:=', '-0.227500mm', 'Y:=', '-0.125000mm', 'Z:=', '0.0mm'])
segs.append(['NAME:PLSegment', 'SegmentType:=', 'Line', 'StartIndex:=', 6, 'NoOfPoints:=', 2])
pts.append(['NAME:PLPoint', 'X:=', '-0.227500mm', 'Y:=', '-0.135000mm', 'Z:=', '0.0mm'])
segs.append(['NAME:PLSegment', 'SegmentType:=', 'Line', 'StartIndex:=', 7, 'NoOfPoints:=', 2])
pts.append(['NAME:PLPoint', 'X:=', '-0.250484mm', 'Y:=', '-0.135000mm', 'Z:=', '0.0mm'])
oEditor.CreatePolyline(
    ['NAME:PolylineParameters', 'IsPolylineCovered:=', True, 'IsPolylineClosed:=', True, pts, segs],
    [
        'NAME:Attributes',
        'Name:=', 'a_wire_Q4_0',
        'Flags:=', '',
        'Color:=', '(200 220 255)',
        'Transparency:=', 0.0,
        'PartCoordinateSystem:=', 'Global',
        'UDMId:=', '',
        'MaterialName:=', 'vacuum',
        'SolveInside:=', True
    ]
)
# Element: a_wire_sub_Q4_1
pts = ['NAME:PolylinePoints']
segs = ['NAME:PolylineSegments']
pts.append(['NAME:PLPoint', 'X:=', '-0.248065mm', 'Y:=', '-0.141000mm', 'Z:=', '0.0mm'])
segs.append(['NAME:PLSegment', 'SegmentType:=', 'Line', 'StartIndex:=', 0, 'NoOfPoints:=', 2])
pts.append(['NAME:PLPoint', 'X:=', '-0.315565mm', 'Y:=', '-0.206000mm', 'Z:=', '0.0mm'])
segs.append(['NAME:PLSegment', 'SegmentType:=', 'Line', 'StartIndex:=', 1, 'NoOfPoints:=', 2])
pts.append(['NAME:PLPoint', 'X:=', '-0.425000mm', 'Y:=', '-0.206000mm', 'Z:=', '0.0mm'])
segs.append(['NAME:PLSegment', 'SegmentType:=', 'Line', 'StartIndex:=', 2, 'NoOfPoints:=', 2])
pts.append(['NAME:PLPoint', 'X:=', '-0.425000mm', 'Y:=', '-0.184000mm', 'Z:=', '0.0mm'])
segs.append(['NAME:PLSegment', 'SegmentType:=', 'Line', 'StartIndex:=', 3, 'NoOfPoints:=', 2])
pts.append(['NAME:PLPoint', 'X:=', '-0.324435mm', 'Y:=', '-0.184000mm', 'Z:=', '0.0mm'])
segs.append(['NAME:PLSegment', 'SegmentType:=', 'Line', 'StartIndex:=', 4, 'NoOfPoints:=', 2])
pts.append(['NAME:PLPoint', 'X:=', '-0.256935mm', 'Y:=', '-0.119000mm', 'Z:=', '0.0mm'])
segs.append(['NAME:PLSegment', 'SegmentType:=', 'Line', 'StartIndex:=', 5, 'NoOfPoints:=', 2])
pts.append(['NAME:PLPoint', 'X:=', '-0.227500mm', 'Y:=', '-0.119000mm', 'Z:=', '0.0mm'])
segs.append(['NAME:PLSegment', 'SegmentType:=', 'Line', 'StartIndex:=', 6, 'NoOfPoints:=', 2])
pts.append(['NAME:PLPoint', 'X:=', '-0.227500mm', 'Y:=', '-0.141000mm', 'Z:=', '0.0mm'])
segs.append(['NAME:PLSegment', 'SegmentType:=', 'Line', 'StartIndex:=', 7, 'NoOfPoints:=', 2])
pts.append(['NAME:PLPoint', 'X:=', '-0.248065mm', 'Y:=', '-0.141000mm', 'Z:=', '0.0mm'])
oEditor.CreatePolyline(
    ['NAME:PolylineParameters', 'IsPolylineCovered:=', True, 'IsPolylineClosed:=', True, pts, segs],
    [
        'NAME:Attributes',
        'Name:=', 'a_wire_sub_Q4_1',
        'Flags:=', '',
        'Color:=', '(255 100 100)',
        'Transparency:=', 0.0,
        'PartCoordinateSystem:=', 'Global',
        'UDMId:=', '',
        'MaterialName:=', 'vacuum',
        'SolveInside:=', True
    ]
)
# Element: b_wire_Q4_2
pts = ['NAME:PolylinePoints']
segs = ['NAME:PolylineSegments']
pts.append(['NAME:PLPoint', 'X:=', '0.254516mm', 'Y:=', '-0.125000mm', 'Z:=', '0.0mm'])
segs.append(['NAME:PLSegment', 'SegmentType:=', 'Line', 'StartIndex:=', 0, 'NoOfPoints:=', 2])
pts.append(['NAME:PLPoint', 'X:=', '0.322016mm', 'Y:=', '-0.190000mm', 'Z:=', '0.0mm'])
segs.append(['NAME:PLSegment', 'SegmentType:=', 'Line', 'StartIndex:=', 1, 'NoOfPoints:=', 2])
pts.append(['NAME:PLPoint', 'X:=', '0.425000mm', 'Y:=', '-0.190000mm', 'Z:=', '0.0mm'])
segs.append(['NAME:PLSegment', 'SegmentType:=', 'Line', 'StartIndex:=', 2, 'NoOfPoints:=', 2])
pts.append(['NAME:PLPoint', 'X:=', '0.425000mm', 'Y:=', '-0.200000mm', 'Z:=', '0.0mm'])
segs.append(['NAME:PLSegment', 'SegmentType:=', 'Line', 'StartIndex:=', 3, 'NoOfPoints:=', 2])
pts.append(['NAME:PLPoint', 'X:=', '0.317984mm', 'Y:=', '-0.200000mm', 'Z:=', '0.0mm'])
segs.append(['NAME:PLSegment', 'SegmentType:=', 'Line', 'StartIndex:=', 4, 'NoOfPoints:=', 2])
pts.append(['NAME:PLPoint', 'X:=', '0.250484mm', 'Y:=', '-0.135000mm', 'Z:=', '0.0mm'])
segs.append(['NAME:PLSegment', 'SegmentType:=', 'Line', 'StartIndex:=', 5, 'NoOfPoints:=', 2])
pts.append(['NAME:PLPoint', 'X:=', '0.227500mm', 'Y:=', '-0.135000mm', 'Z:=', '0.0mm'])
segs.append(['NAME:PLSegment', 'SegmentType:=', 'Line', 'StartIndex:=', 6, 'NoOfPoints:=', 2])
pts.append(['NAME:PLPoint', 'X:=', '0.227500mm', 'Y:=', '-0.125000mm', 'Z:=', '0.0mm'])
segs.append(['NAME:PLSegment', 'SegmentType:=', 'Line', 'StartIndex:=', 7, 'NoOfPoints:=', 2])
pts.append(['NAME:PLPoint', 'X:=', '0.254516mm', 'Y:=', '-0.125000mm', 'Z:=', '0.0mm'])
oEditor.CreatePolyline(
    ['NAME:PolylineParameters', 'IsPolylineCovered:=', True, 'IsPolylineClosed:=', True, pts, segs],
    [
        'NAME:Attributes',
        'Name:=', 'b_wire_Q4_2',
        'Flags:=', '',
        'Color:=', '(200 220 255)',
        'Transparency:=', 0.0,
        'PartCoordinateSystem:=', 'Global',
        'UDMId:=', '',
        'MaterialName:=', 'vacuum',
        'SolveInside:=', True
    ]
)
# Element: b_wire_sub_Q4_3
pts = ['NAME:PolylinePoints']
segs = ['NAME:PolylineSegments']
pts.append(['NAME:PLPoint', 'X:=', '0.256935mm', 'Y:=', '-0.119000mm', 'Z:=', '0.0mm'])
segs.append(['NAME:PLSegment', 'SegmentType:=', 'Line', 'StartIndex:=', 0, 'NoOfPoints:=', 2])
pts.append(['NAME:PLPoint', 'X:=', '0.324435mm', 'Y:=', '-0.184000mm', 'Z:=', '0.0mm'])
segs.append(['NAME:PLSegment', 'SegmentType:=', 'Line', 'StartIndex:=', 1, 'NoOfPoints:=', 2])
pts.append(['NAME:PLPoint', 'X:=', '0.425000mm', 'Y:=', '-0.184000mm', 'Z:=', '0.0mm'])
segs.append(['NAME:PLSegment', 'SegmentType:=', 'Line', 'StartIndex:=', 2, 'NoOfPoints:=', 2])
pts.append(['NAME:PLPoint', 'X:=', '0.425000mm', 'Y:=', '-0.206000mm', 'Z:=', '0.0mm'])
segs.append(['NAME:PLSegment', 'SegmentType:=', 'Line', 'StartIndex:=', 3, 'NoOfPoints:=', 2])
pts.append(['NAME:PLPoint', 'X:=', '0.315565mm', 'Y:=', '-0.206000mm', 'Z:=', '0.0mm'])
segs.append(['NAME:PLSegment', 'SegmentType:=', 'Line', 'StartIndex:=', 4, 'NoOfPoints:=', 2])
pts.append(['NAME:PLPoint', 'X:=', '0.248065mm', 'Y:=', '-0.141000mm', 'Z:=', '0.0mm'])
segs.append(['NAME:PLSegment', 'SegmentType:=', 'Line', 'StartIndex:=', 5, 'NoOfPoints:=', 2])
pts.append(['NAME:PLPoint', 'X:=', '0.227500mm', 'Y:=', '-0.141000mm', 'Z:=', '0.0mm'])
segs.append(['NAME:PLSegment', 'SegmentType:=', 'Line', 'StartIndex:=', 6, 'NoOfPoints:=', 2])
pts.append(['NAME:PLPoint', 'X:=', '0.227500mm', 'Y:=', '-0.119000mm', 'Z:=', '0.0mm'])
segs.append(['NAME:PLSegment', 'SegmentType:=', 'Line', 'StartIndex:=', 7, 'NoOfPoints:=', 2])
pts.append(['NAME:PLPoint', 'X:=', '0.256935mm', 'Y:=', '-0.119000mm', 'Z:=', '0.0mm'])
oEditor.CreatePolyline(
    ['NAME:PolylineParameters', 'IsPolylineCovered:=', True, 'IsPolylineClosed:=', True, pts, segs],
    [
        'NAME:Attributes',
        'Name:=', 'b_wire_sub_Q4_3',
        'Flags:=', '',
        'Color:=', '(255 100 100)',
        'Transparency:=', 0.0,
        'PartCoordinateSystem:=', 'Global',
        'UDMId:=', '',
        'MaterialName:=', 'vacuum',
        'SolveInside:=', True
    ]
)

# Subtract All Pockets & CPW Slots from Ground Plane
cut_list = ['rect_pk_Q4_2', 'cl_etcher_Q4_6', 'a_wire_sub_Q4_1', 'b_wire_sub_Q4_3']
try:
    existing = set(oEditor.GetMatchedObjectName('*')) if hasattr(oEditor, 'GetMatchedObjectName') else set(cut_list)
    valid_cuts = [c for c in cut_list if c in existing] if existing else cut_list
    if valid_cuts:
        oEditor.Subtract(
            ['NAME:Selections', 'Blank Parts:=', 'ground_main_plane', 'Tool Parts:=', ','.join(valid_cuts)],
            ['NAME:SubtractParameters', 'KeepOriginals:=', False]
        )
except Exception as sub_err:
    print('[!] Subtract notice: ' + str(sub_err))

# Assign Perfect E to Ground Plane & Metal Traces/Pads
metal_list = ['ground_main_plane'] + ['pad_top_Q4_0', 'pad_bot_Q4_1', 'a_connector_pad_Q4_3', 'b_connector_pad_Q4_4', 'cl_metal_Q4_5', 'a_wire_Q4_0', 'b_wire_Q4_2']
try:
    existing = set(oEditor.GetMatchedObjectName('*')) if hasattr(oEditor, 'GetMatchedObjectName') else set(metal_list)
    valid_metals = [m for m in metal_list if m in existing] if existing else metal_list
    if valid_metals:
        oBoundarySetup.AssignPerfectE(
            ['NAME:PerfE_Superconductors', 'Objects:=', valid_metals, 'InfGroundPlane:=', False]
        )
except Exception as pe_err:
    print('[!] Perfect E notice: ' + str(pe_err))

# Josephson Junction 2D Sheet across 30um gap (center y=0.0mm)
oEditor.CreateRectangle(
    [
        'NAME:RectangleParameters',
        'IsCovered:=', True,
        'XStart:=', '-0.015mm',
        'YStart:=', '-0.015000mm',
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
# Visual Red Polyline across junction
try:
    pts_jj = ['NAME:PolylinePoints']
    pts_jj.append(['NAME:PLPoint', 'X:=', '0.0mm', 'Y:=', '-0.015000mm', 'Z:=', '0.0mm'])
    pts_jj.append(['NAME:PLPoint', 'X:=', '0.0mm', 'Y:=', '0.015000mm', 'Z:=', '0.0mm'])
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
                'Start:=', ['0.0mm', '-0.015000mm', '0.0mm'],
                'End:=', ['0.0mm', '0.015000mm', '0.0mm']
            ],
            'UseResist:=', False,
            'UseInduct:=', True,
            'Inductance:=', '12.31nH',
            'UseCap:=', True,
            'Capacitance:=', '2.0fF'
        ]
    )
    print('[+] Assigned Q4 Lumped RLC boundary for Simon_Q4_Single_Qubit!')
except Exception as rlc_err:
    print('[*] Note on Lumped RLC assignment: ' + str(rlc_err))

oEditor.FitAll()

print('[SUCCESS] Simon Single Qubit Q4 fully generated in Ansys HFSS!')
