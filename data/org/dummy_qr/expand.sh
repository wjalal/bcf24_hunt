 
#!/bin/bash

# Loop over all JPG files in the current directory
for img in *.jpg; do
    if [ -f "$img" ]; then
        # Use ffmpeg to expand the canvas to 1240x1754 with a white background while centering the image
        ffmpeg -i "$img" -vf "pad=1240:1754:(1240-iw)/2:(1754-ih)/2:color=white" "expanded_$img"
    fi
done
