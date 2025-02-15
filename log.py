import os
import glob


def log():
    log_directory = 'data/logs/'
    output_file = 'data/logs-recent.txt'
    log_files = glob.glob(os.path.join(log_directory, '*.log'))

    log_files.sort(key=os.path.getmtime, reverse=True)
    lines_to_write = []
    for log_file in log_files[:10]:  # Limit to the 10 most recent files
        with open(log_file, 'r') as file:
            first_line = file.readline().strip()  # Read the first line
            lines_to_write.append(first_line)

    # Write the collected lines to the output file
    with open(output_file, 'w') as output:
        for line in lines_to_write:
            output.write(line + '\n')

