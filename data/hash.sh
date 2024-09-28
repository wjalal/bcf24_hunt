#!/bin/bash

# Create the 'hashed' folder if it doesn't exist
mkdir -p hashed
rm hashed/*

cp puzzles.tsv hashed/puzzles_h.tsv

# Loop over all PNG files in the current directory
cd puzzles

for file in *.png; do
    if [ -f "$file" ]; then
        # Generate a random UUID
        uuid=$(uuidgen)
        fullname="$uuid-$file"

        # Rename the file to the UUID and move it to the 'hashed' folder
        cp "$file" "../hashed/$fullname"
        # Replace every occurrence of $file with the full URL in puzzles_h.txt
        sed -i "s|$file|https://csefest2024-storage.sgp1.cdn.digitaloceanspaces.com/hunt/$fullname|g" "../hashed/puzzles_h.tsv"

        
    fi
done

cd ..
python3 gen_quiz.py