# Smart Greenhouse System Documentation

## Overview
The Smart Greenhouse System is a Python application that simulates and manages a greenhouse with multiple sections, each dedicated to a different crop. It monitors temperature and moisture levels, provides a user interface for control, and alerts users when conditions fall outside optimal ranges.

## Features
- Multiple greenhouse sections with different crops
- Real-time monitoring of temperature and moisture levels
- User interface for adjusting environmental conditions
- Automated alerts for out-of-range conditions
- Configurable settings for different crop types

## System Requirements
- Python 3.7+
- Tkinter (usually comes with Python)
- Pillow library for image processing

## Installation
1. Ensure Python 3.7+ is installed on your system.
2. Install the Pillow library: `pip install Pillow`
3. Place the `greenhouse_system.py` and `config.json` files in the same directory.
4. Create an `images` subdirectory and place the required image files there.

## Configuration
The `config.json` file contains all the configurable settings for the application:
- Crop thresholds for temperature and moisture
- UI settings (colors, sizes)
- Image file names
- Initial sensor data

Modify this file to adjust the system's behavior and appearance.

## Usage
1. Run the script: `python greenhouse_system.py`
2. The main window will display three greenhouse sections.
3. Use the control buttons to adjust temperature and moisture in each section.
4. Alert popups will appear if conditions fall outside the optimal range for each crop.

## Classes
- `CropSettings`: Manages threshold settings for a crop
- `GreenhouseSection`: Represents a section of the greenhouse
- `GreenhouseUI`: Main application window and user interface

## Customization
To add new crop types or modify existing ones, update the `crop_thresholds` section in the `config.json` file.

## Troubleshooting
- If images don't appear, ensure they are present in the `images` directory and correctly named in the `config.json` file.
- For any other issues, check the console for error messages.
