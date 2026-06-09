#!/usr/bin/env python3

# =============================================================================
# DASHBOARD CONFIGURATION
# Modify these values to change the layout or add/remove cameras
# =============================================================================

MIN_VIDEO_WIDTH = 600   # Minimum width of each video in pixels (e.g., 800)
MAX_COLS_PER_ROW = 4    # Maximum number of videos allowed in a single row
OUTPUT_FILE = "index.html" # Name of the generated file

# List of webcams. 
# Best results come from direct embed URLs (like YouTube /embed/ links).
WEBCAMS = [
    {
        "label": "Lyall Bay",
        "url": "https://www.youtube.com/embed/r7qzi_d758w"
    },
    {
        "label": "Lyall Bay Surf",
        "url": "https://www.youtube.com/embed/f8BC5jHXZMA"
    },
    {
        "label": "Wellington Harbour",
        "url": "https://www.youtube.com/embed/QmAEV9sFDtY"
    },
    {
        "label": "Worser Bay - South",
        "url": "https://www.youtube.com/embed/J1BJE4lhXHw"
    },
    {
        "label": "Worser Bay - Ramp",
        "url": "https://www.youtube.com/embed/_nGsameml7g"
    },
    {
        "label": "Worser Bay - North",
        "url": "https://www.youtube.com/embed/9iH0NG30slE"
    },
    {
        "label": "Eastbourne",
        "url": "https://www.youtube.com/embed/fLBBFepYh3o"
    },
    {
        "label": "Castlepoint",
        "url": "https://www.youtube.com/embed/t0nYqriNf-w?autoplay=1&mute=1"
    },
    {
        "label": "Cape Palliser",
        "url": "https://g3.ipcamlive.com/player/player.php?alias=64c0d6f04f46b"
    },
    {
        "label": "Tora Beach",
        "url": "https://mynetwork.co.nz/Sites/Tora-martinborough.jpg"
    }
]

# =============================================================================
# SCRIPT LOGIC (Do not edit below unless changing core functionality)
# =============================================================================

def generate_html():
    # Generate the individual camera blocks
    camera_html_blocks = ""
    
    for i, cam in enumerate(WEBCAMS):
        pane_id = f"pane{i+1}"
        label = cam["label"]
        url = cam["url"]
        
        block = f"""
        <div class="cam-container" id="{pane_id}">
            <a href="{url}" target="_blank" class="label">{label}</a>
            <div class="fullscreen-btn" onclick="toggleFullScreen('{pane_id}')" title="Fullscreen">
                <svg viewBox="0 0 16 16"><path fill-rule="evenodd" d="M1.5 1a.5.5 0 0 0-.5.5v4a.5.5 0 0 1-1 0v-4A1.5 1.5 0 0 1 1.5 0h4a.5.5 0 0 1 0 1h-4zM10 .5a.5.5 0 0 1 .5-.5h4A1.5 1.5 0 0 1 16 1.5v4a.5.5 0 0 1-1 0v-4a.5.5 0 0 0-.5-.5h-4a.5.5 0 0 1-.5-.5zM.5 10a.5.5 0 0 1 .5.5v4a.5.5 0 0 0 .5.5h4a.5.5 0 0 1 0 1h-4A1.5 1.5 0 0 1 0 14.5v-4a.5.5 0 0 1 .5-.5zm15 0a.5.5 0 0 1 .5.5v4a1.5 1.5 0 0 1-1.5 1.5h-4a.5.5 0 0 1 0-1h4a.5.5 0 0 0 .5-.5v-4a.5.5 0 0 1 .5-.5z"/></svg>
            </div>
            <iframe class="direct-feed" src="{url}" referrerpolicy="strict-origin-when-cross-origin" allowfullscreen></iframe>
        </div>
        """
        camera_html_blocks += block

    # Base HTML and CSS template
    html_template = f"""<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Wellington region webcams</title>
    <style>
        body, html {{
            margin: 0; 
            padding: 0; 
            width: 100%; 
            min-height: 100%;
            background-color: #000; 
            font-family: sans-serif;
            overflow-x: hidden; /* Prevent horizontal scrolling */
        }}

        /* 
           Responsive Grid Math:
           Uses auto-fill so orphaned bottom rows align to the left grid.
           min(100%, {MIN_VIDEO_WIDTH}px) ensures the minimum size is respected on desktop, 
           but shrinks to fit 100% of the screen on mobile devices.
        */
        .grid-container {{
            display: grid;
            grid-template-columns: repeat(auto-fill, minmax(min(100%, {MIN_VIDEO_WIDTH}px), 1fr));
            gap: 4px;
            padding: 4px;
            width: 100vw;
            box-sizing: border-box;
        }}

        /* Force maximum columns on ultra-wide screens */
        @media (min-width: {MIN_VIDEO_WIDTH * MAX_COLS_PER_ROW}px) {{
            .grid-container {{
                grid-template-columns: repeat({MAX_COLS_PER_ROW}, 1fr);
            }}
        }}

        .cam-container {{
            position: relative; 
            width: 100%; 
            aspect-ratio: 16 / 9; /* Perfect ratio for standard HD video */
            background-color: #111; 
            overflow: hidden; 
        }}

        .direct-feed {{
            width: 100%; 
            height: 100%; 
            border: none;
        }}

        /* UI Elements */
        .label {{
            position: absolute; top: 10px; left: 10px;
            background-color: rgba(0, 0, 0, 0.8); color: white;
            padding: 6px 12px; font-size: 14px; font-weight: bold; 
            border-radius: 4px; z-index: 10; text-decoration: none;
            border: 1px solid transparent;
            transition: all 0.2s ease;
        }}

        .label:hover {{
            background-color: rgba(0, 0, 0, 0.95);
            border: 1px solid rgba(255, 255, 255, 0.5);
            color: #4da6ff;
        }}

        .fullscreen-btn {{
            position: absolute; top: 10px; right: 10px;
            background-color: rgba(0, 0, 0, 0.8); color: white;
            width: 32px; height: 32px; border-radius: 4px;
            display: flex; align-items: center; justify-content: center;
            cursor: pointer; z-index: 10;
            transition: background-color 0.2s ease;
            border: 1px solid transparent;
        }}

        .fullscreen-btn:hover {{
            background-color: rgba(0, 0, 0, 0.95);
            border: 1px solid rgba(255, 255, 255, 0.5);
        }}

        .fullscreen-btn svg {{
            width: 16px; height: 16px; fill: currentColor;
        }}
    </style>
</head>
<body>

    <div class="grid-container">
{camera_html_blocks}
    </div>

    <script>
        // Handles expanding a specific pane to full screen
        function toggleFullScreen(paneId) {{
            const pane = document.getElementById(paneId);
            
            if (!document.fullscreenElement) {{
                if (pane.requestFullscreen) {{
                    pane.requestFullscreen();
                }} else if (pane.webkitRequestFullscreen) {{ /* Safari */
                    pane.webkitRequestFullscreen();
                }} else if (pane.msRequestFullscreen) {{ /* IE11 */
                    pane.msRequestFullscreen();
                }}
            }} else {{
                if (document.exitFullscreen) {{
                    document.exitFullscreen();
                }} else if (document.webkitExitFullscreen) {{ /* Safari */
                    document.webkitExitFullscreen();
                }} else if (document.msExitFullscreen) {{ /* IE11 */
                    document.msExitFullscreen();
                }}
            }}
        }}
    </script>
</body>
</html>
"""

    # Write the output file
    try:
        with open(OUTPUT_FILE, "w", encoding="utf-8") as file:
            file.write(html_template)
        print(f"Success! Generated '{OUTPUT_FILE}' with {len(WEBCAMS)} webcams.")
        print(f"Layout rules applied: Minimum Width = {MIN_VIDEO_WIDTH}px | Maximum Columns = {MAX_COLS_PER_ROW}")
    except Exception as e:
        print(f"Error writing file: {e}")

if __name__ == "__main__":
    generate_html()
