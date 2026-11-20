# Electric Motor Bearing Fault Analysis & Detection — Python FFT, SNR & Tkinter GUI

[![Portfolio](https://img.shields.io/badge/Portfolio-scidelo--andriasahy.github.io-0284c7?style=for-the-badge)](https://scidelo-andriasahy.github.io/?project=16)
[![Python](https://img.shields.io/badge/Signal_Processing-Python_NumPy_FFT-3776AB?style=for-the-badge)](https://www.python.org/)

## Overview
Interactive Python desktop application (`src/interface.py`) for predictive maintenance of rotating electric machinery:
- Synthetic healthy vs. faulty stator current / vibration signal generation with configurable Signal-to-Noise Ratio (`SNR`).
- Characteristic bearing defect sideband frequency computation (`f0 ± k * 0.4 * Nb * fr`) and automated spectral FFT fault detection.
