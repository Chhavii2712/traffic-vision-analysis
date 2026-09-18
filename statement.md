# Traffic Vision Analysis

## Problem Statement
The exponential increase in urban traffic has necessitated automated systems for traffic monitoring and management. Manual monitoring of traffic surveillance footage is highly inefficient and error-prone. This project aims to build an automated, command-line executable Computer Vision tool that can analyze traffic video streams or images to detect road lanes and count vehicles passing through a defined zone.

## Scope of the project
- Implement robust line detection using Canny edge detection and Hough Line Transforms.
- Implement vehicle detection and counting using Background Subtraction (MOG2) and Contour Analysis.
- Provide a modular, extendable command-line interface (CLI) for users to process custom media files.
- Support both image and video I/O.
- The project focuses on traditional Computer Vision techniques without relying on deep learning models, ensuring high performance on standard CPU hardware.

## Target users
- Traffic Management Authorities looking for lightweight surveillance analysis tools.
- City Planners analyzing road utilization rates.
- Computer Vision students and researchers aiming to understand foundational CV algorithms.

## High-level features
1. **Lane Detection Module**: Highlights driving lanes to analyze traffic flow boundaries.
2. **Vehicle Counting Module**: Detects and tracks vehicles across a designated counting line, maintaining a real-time tally.
3. **Flexible CLI**: A robust terminal interface to chain tasks together (e.g. run lane detection and counting simultaneously).
4. **Performance Optimized**: Uses efficient OpenCV matrix operations to achieve high FPS processing.
