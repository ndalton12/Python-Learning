import csv

MY_FILE = "sample_sfpd_incident_all.csv"

def parse(raw_file, delimiter):
	"""Parses a raw CSV file to a JSON-line object"""
	
	# Open CSV file
	opened_file = open(raw_file)

	# Read CSV file
	csv_data = csv.reader(opened_file, delimiter=delimiter)
	
	# Init data
	parsed_data = []
	
	# Header data
	fields = next(csv_data)

	# Append CSV info into data
	for row in csv_data:
	        parsed_data.append(dict(zip(fields, row)))

	# Close CSV file	
	opened_file.close()

	# Build data

	return parsed_data

def main():
	# Call parse function
	new_data = parse(MY_FILE, ',')

	# Output
	print(new_data)

if __name__ == '__main__':
	main()
