from PIL import Image
import os
from collections import defaultdict

def create_pixel_html(image_path, output_path, pixel_size=10, 
                      row_interval=1, col_interval=1):
    """
    Convert an image into pixel-style HTML with background color optimization to reduce element count
    
    Parameters:
    image_path: Input image path
    output_path: Output HTML path
    pixel_size: Display size of each pixel in HTML (in pixels)
    row_interval: Row sampling interval (take every nth row)
    col_interval: Column sampling interval (take every nth column)
    """
    # Open image and convert to RGB mode
    img = Image.open(image_path).convert('RGB')
    width, height = img.size
    
    # Store all color classes
    color_classes = {}
    # Store HTML structure
    html_rows = []
    
    # Calculate actual dimensions after sampling
    sampled_width = (width + col_interval - 1) // col_interval
    sampled_height = (height + row_interval - 1) // row_interval
    
    # Step 1: Count frequency of all pixel colors
    color_frequency = defaultdict(int)
    for y in range(0, height, row_interval):
        for x in range(0, width, col_interval):
            r, g, b = img.getpixel((x, y))
            hex_color = f'#{r:02x}{g:02x}{b:02x}'
            color_frequency[hex_color] += 1
    
    # Find most frequent color as background
    if color_frequency:
        bg_color = max(color_frequency, key=color_frequency.get)
        bg_r, bg_g, bg_b = tuple(int(bg_color[i:i+2], 16) for i in (1, 3, 5))
        print(f"Background color: {bg_color} (frequency: {color_frequency[bg_color]}/{sampled_width*sampled_height})")
    else:
        bg_color = "#000000"
        bg_r, bg_g, bg_b = 0, 0, 0
    
    # Create class name for background color
    bg_class = f'color_{bg_r:03d}_{bg_g:03d}_{bg_b:03d}'
    color_classes[bg_color] = bg_class
    
    # Process each pixel row (with row interval sampling)
    for y in range(0, height, row_interval):
        row_divs = []
        # Process each pixel in current row (with column interval sampling)
        for x in range(0, width, col_interval):
            # Get RGB color values
            r, g, b = img.getpixel((x, y))
            # Generate hex color code
            hex_color = f'#{r:02x}{g:02x}{b:02x}'
            
            # Skip div creation for background color
            if hex_color == bg_color:
                continue
            
            # Create or get color class name
            if hex_color not in color_classes:
                class_name = f'color_{r:03d}_{bg_g:03d}_{b:03d}'
                color_classes[hex_color] = class_name
            else:
                class_name = color_classes[hex_color]
            
            # Calculate grid position
            grid_x = x // col_interval + 1
            grid_y = y // row_interval + 1
            
            # Create pixel div with CSS grid positioning
            row_divs.append(
                f'<div class="pixel {class_name}" '
                f'style="grid-row: {grid_y}; grid-column: {grid_x};"></div>'
            )
        
        # Add row content
        html_rows.append(''.join(row_divs))
    
    # Create CSS styles
    css_styles = [
        '* { margin: 0; padding: 0; box-sizing: border-box; }',
        '.image-container {',
        f'  display: grid;',
        f'  width: {pixel_size*sampled_width}px;',
        f'  height: {pixel_size*sampled_height}px;',
        f'  grid-template-columns: repeat({sampled_width}, {pixel_size}px);',
        f'  grid-template-rows: repeat({sampled_height}, {pixel_size}px);',
        f'  background-color: {bg_color};',
        '}',
        '.pixel {',
        f'  width: {pixel_size}px;',
        f'  height: {pixel_size}px;',
        '  transition: transform 0.2s ease, opacity 0.3s ease;',
        '}',
        '.pixel:hover {',
        '  transform: scale(1.5);',
        '  z-index: 10;',
        '  opacity: 0.9 !important;',
        '  box-shadow: 0 0 5px rgba(255,255,255,0.5);',
        '}'
    ]
    
    # Add color class styles
    for hex_color, class_name in color_classes.items():
        css_styles.append(f'.{class_name} {{ background-color: {hex_color}; }}')
    
    # Create complete HTML content
    html_content = [
        '<style>',
        ''.join(css_styles),
        '</style>',
        f'<div class="image-container">{"".join(html_rows)}</div>',
    ]
    
    # Write to file
    with open(output_path, 'w') as f:
        f.write('\n'.join(html_content))

if __name__ == "__main__":
    # Configuration parameters
    input_image = "mountain-477832_1280.jpg"  # Input image path
    output_html = "pixel_art.html"  # Output HTML path
    pixel_size = 5                 # Display size per pixel (pixels)
    row_interval = 15              # Row sampling interval
    col_interval = 15              # Column sampling interval
    
    create_pixel_html(
        input_image, 
        output_html, 
        pixel_size=pixel_size,
        row_interval=row_interval,
        col_interval=col_interval
    )