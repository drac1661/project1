from datetime import datetime

def whichday():
    input_file_path = 'data/dates.txt'
    output_file_path = 'data/dates-wednesdays.txt'

    wednesday_count = 0

    date_formats = [
        "%b %d, %Y",  # Oct 31, 2005
        "%d-%b-%Y",    # 30-Mar-2010
        "%Y-%m-%d",    # 2018-03-03
        "%b %d, %Y",   # Dec 23, 2024
        "%b %d, %Y",   # Mar 19, 2009
        "%Y/%m/%d %H:%M:%S"  # 2008/07/27 19:12:56
    ]

    # Read the dates from the input file
    with open(input_file_path, 'r') as file:
        for line in file:
            date_str = line.strip()
            for date_format in date_formats:
                try:
                    # Try to parse the date
                    date_obj = datetime.strptime(date_str, date_format)
                    # Check if the date is a Wednesday (0 = Monday, ..., 2 = Wednesday)
                    if date_obj.weekday() == 2:
                        wednesday_count += 1
                    break  # Exit the loop if parsing was successful
                except ValueError:
                    continue  # Try the next format if parsing fails

    with open(output_file_path, 'w') as output_file:
        output_file.write(str(wednesday_count))