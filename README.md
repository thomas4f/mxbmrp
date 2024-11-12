# MX Bikes Memory Reader Project (MXBMRP)

![mxbmrp](https://github.com/user-attachments/assets/09dd7100-9938-471a-8c98-09d32ea1aad9)

The program reads specific memory addresses in MX Bikes to retrieve real-time game data. It then writes this data to a ReShade shader file, creating an in-game overlay that displays the information live, similar to [MaxHUD](http://forum.mx-bikes.com/index.php?topic=180.0)).

## Features
 - Real-Time Data: Reads game memory data such as bike, track, and server information.
 - Shader Integration: Outputs formatted data to a ReShade shader for in-game display.
 - Customizable: Change displayed content, background layer and update intervals.

## Prerequisites
 - [ReShade](https://reshade.me/) configured for MX Bikes, with Add-on support installed and with the AutoReload add-on enabled.

## Installation
Download the latest .zip from [releases](https://github.com/thomas4f/mxbmrp/releases), and decompress the archive to your desktop (or anywhere you like).

## Configuration
Edit `config.yaml` for customizable settings, such as:

 - Text Display: Customize the text format with {Bike}, {Track}, {Server}, and {Password} placeholders.
 - Shader Path: Path to save the shader file (ensure it points to the ReShade shader directory).
 - Layer Image: Path to the image overlay for the shader.
 - Memory Addresses: Preconfigured for MX Bikes beta19; these can be adjusted if the game is updated.

The position of the HUD, text size and text colors can be adjusted from within ReShade.

## Usage
 - Edit config.yaml according to the comments within the file.
 - Run mxbmrp.exe.
 - Enable the mxbmrp shader within ReShade.
 - Press CTRL + C to exit.
 
*You only need to restart the program if you change its configuration. Restarting MX Bikes alone does not require a program restart.*

## Installation help
A short video on how to set things up:
<video src="https://github.com/user-attachments/assets/bace9bc2-277e-4054-8b6d-c1d9cca8dcfe" width="1280" height="718"></video>

## Caveats
This project uses specific memory addresses for reading game data. Due to variations, memory reading may not always be 100% accurate. Some values might be incorrect or unavailable during gameplay.

The provided memory addresses are configured for MX Bikes beta19b. If the game updates or if you use a different version, these addresses may need adjustment, as the data locations could shift with game updates.

## Running and building the project from source
Note that **this is optional**, and that it assumes that you have Git, Python and Pip installed.

### Running
```code
git clone https://github.com/thomas4f/mxbmrp
cd mxbmrp
pip install psutil pyyaml
python src\main.py
```

### Building
```code
pip install pyinstaller
pyinstaller --onefile src\main.py --name mxbmrp.exe --distpath=.
```

## Final notes
I created this project primarily out of an interest in exploring memory reading and integrating game data into a visual format.

It’s worth noting that this is hacky and not very elegant. If MaxHUD or similar tools implement equivalent functionality, they may provide a more seamless, stable, and fully integrated solution.

Turns out 🥑🥕🥦🥬 are very useful for testing, thanks!

