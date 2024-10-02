 
#!/bin/bash

# Create the 'annot' folder if it doesn't exist
mkdir -p annot

# Loop over all JPG files in the current directory
for img in *.jpg; do
    if [ -f "$img" ]; then
        # Overlay 'annot.png' on top of the image and save it in the 'annot' folder
        ffmpeg -i "$img" -i annot.png -filter_complex "[0][1]overlay=0:0" "annot/annot_${img%.jpg}.png"
    fi
done
