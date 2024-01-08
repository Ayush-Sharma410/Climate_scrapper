# Open the input and output files
with open('output.csv', 'r') as infile, open('output2.csv', 'w') as outfile:
    # Read each line in the input file
    for line in infile:
        # Split the line into fields
        fields = line.strip().split(',')
        
        # Check if there is more than one entry in the line
        if len(fields) > 2:
            # Write the line to the output file
            outfile.write(line)
