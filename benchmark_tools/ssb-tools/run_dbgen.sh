#!/bin/bash

# Check if the correct number of arguments is provided
if [ "$#" -ne 2 ]; then
    echo "Usage: $0 <scale_factor> <destination_path>"
    exit 1
fi

# Assign arguments to variables
scale_factor="$1"
destination_path="$2"

# Run the dbgen command
./dbgen -s "$scale_factor" -T c
./dbgen -s "$scale_factor" -T l
./dbgen -s "$scale_factor" -T p
./dbgen -s "$scale_factor" -T s
./dbgen -s "$scale_factor" -T d

# Move the generated CSV files to the specified destination path
mv *.csv "$destination_path"

echo "CSV files generated and moved to $destination_path"

