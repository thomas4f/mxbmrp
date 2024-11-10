# MXB Memory Reader Project (MXBMRP)

![mxbmrp](https://github.com/user-attachments/assets/09dd7100-9938-471a-8c98-09d32ea1aad9)

A memory reader project that retrieves and displays game data from MX Bikes. The program reads memory data, and creates a ReShade shader that displays the info (similar to [MaxHUD](https://mxb-mods.com/maxhud/)).

## Features
 - Real-Time Data: Reads game memory data such as bike, track, and server information.
 - Shader Integration: Outputs formatted data to a ReShade shader for in-game display.
 - Customizable: Change displayed content, background layer and update intervals.

## Prerequisites
 - [ReShade](https://reshade.me/) configured for MX Bikes, with Add-on support installed and with the AutoReload add-on enabled.

## Installation
Download the latest release from the releases tab, and decompress the archive to your desktop (or anywhere you like).

## Configuration
Edit config.yaml for customizable settings:

 - Text Display: Customize the text format with {Bike}, {Track}, {Server}, and {Password} placeholders.
 - Shader Path: Path to save the shader file (ensure it points to the ReShade shader directory).
 - Layer Image: Path to the image overlay for the shader.
 - Memory Addresses: Preconfigured for MX Bikes beta19; these can be adjusted if the game is updated.

The position of the HUD, text size and text colors can be adjusted from within ReShade.

## Usage
    Edit config.yaml according to the description above.
    Run memreader.exe.
	Enable the mxbmrp shader within ReShade.
    Press CTRL + C to exit.
	
## Caveats
This project uses specific memory addresses for reading game data. Due to variations, memory reading may not always be 100% accurate. Some values might be incorrect or unavailable during gameplay.

The provided memory addresses are configured for MX Bikes beta19. If the game updates or if you use a different version, these addresses may need adjustment, as the data locations could shift with game updates.

## Running and building the project from source
Note that this is optional, and that it assumes that you have Python and pip installed.

### Running
```code
git clone https://github.com/thomas4f/mxbmrp
cd mxbmrp
pip install psutil pyyaml jinja2
python src\main.py
```

### Building
```code
pip install pyinstaller
pyinstaller --onefile src\main.py --name mxbmrp.exe
copy dist\mxbmrp.exe .
```

## Final notes
I created this project primarily out of an interest in exploring memory reading and integrating game data into a visual format.

It’s worth noting that this is hacky and not very elegant. If MaxHUD or similar tools implement equivalent functionality, they may provide a more seamless, stable, and fully integrated solution.

Turns out 🥑🥕🥦🥬 are very useful for testing, thanks!

