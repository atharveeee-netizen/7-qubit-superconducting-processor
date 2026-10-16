@echo off
title JupyterLab - 7-Qubit Quantum Design Suite
echo =====================================================================
echo  Launching JupyterLab in 'qmetal' Conda Environment...
echo  Workspace: %~dp0
echo =====================================================================
call "C:\Users\noobg\Miniconda3\condabin\conda.bat" activate qmetal
start "" http://localhost:8888/lab
jupyter-lab --notebook-dir="%~dp0"
pause
