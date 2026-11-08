@echo off
title 3D FEM & Quantum Transmon LOM Simulation Lab
echo ======================================================================
echo   Running 3D Electrostatic FEM & Quantum Hamiltonian Simulation
echo   Reference: Simon Quantum Hardware & IEEE Quantum Processor Design
echo ======================================================================
echo.
echo Activating 'qmetal' Conda Environment...
call "C:\Users\noobg\Miniconda3\condabin\conda.bat" activate qmetal
set OPENBLAS_NUM_THREADS=1
set OMP_NUM_THREADS=1
set KMP_DUPLICATE_LIB_OK=TRUE

echo.
echo Executing Interactive Quantum FEM & Hamiltonian Extraction Lab...
python "%~dp0interactive_fem_quantum_lab.py"

echo.
echo Opening Simulation Wavefunction and Charge Noise Plot...
start "" "%~dp0live_fem_quantum_simulation.png"

echo.
echo ======================================================================
echo [SUCCESS] Simulation completed!
echo To launch interactive JupyterLab notebooks, run: launch_jupyter_lab.bat
echo ======================================================================
pause

