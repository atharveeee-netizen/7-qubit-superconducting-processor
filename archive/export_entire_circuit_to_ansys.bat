@echo off
title Render Simon's Exact Circuit into Ansys HFSS
echo ======================================================================
echo   Rendering SIMON'S EXACT CIRCUITS INTO ANSYS HFSS
echo   1. Simon_Q4_Single_Qubit (Single-Qubit FEM / LOM Model)
echo   2. Simon_7Qubit_Complete_Processor (Full 7-Qubit Processor)
echo   Reference: Simon Quantum Hardware Masterclass (56:27 / 57:45)
echo ======================================================================
echo.
echo [1/3] Activating 'qmetal' Conda Environment...
call "C:\Users\noobg\Miniconda3\condabin\conda.bat" activate qmetal
set OPENBLAS_NUM_THREADS=1
set OMP_NUM_THREADS=1
set KMP_DUPLICATE_LIB_OK=TRUE

echo.
echo [2/3] Generating Standalone Ansys HFSS Scripts...
python "%~dp0export_entire_circuit_to_ansys.py"

echo.
echo ======================================================================
echo [3/3] Done! Ready to render in Ansys HFSS.
echo.
echo TO VIEW IN ANSYS HFSS:
echo 1. Switch to your open Ansys Electronics Desktop window.
echo 2. Go to menu: Tools -> Run Script...
echo 3. Select 'render_in_ansys_direct.py'
echo 4. Within seconds, Ansys creates BOTH designs in your Project Tree:
echo.
echo    [DESIGN 1] Simon_Q4_Single_Qubit
echo    - 5 mm x 5 mm Silicon Substrate + Ground Plane with Q4 pocket cutout
echo    - Two capacitor pads (455 um x 90 um), charge line, 30 um gap
echo    - Josephson Junction Sheet & Line with Lumped RLC (Lj = 12.31 nH)
echo    - Exactly what Simon zoomed into and created lines on in the video!
echo.
echo    [DESIGN 2] Simon_7Qubit_Complete_Processor
echo    - 10 mm x 10 mm Silicon Substrate + Ground Plane
echo    - 7 Transmons (Q0-Q6 with Q4 center), 6 Launchpads, 6 Readouts, 6 Buses
echo.
echo 5. Click either design in the Project Tree to switch between them!
echo ======================================================================
pause
