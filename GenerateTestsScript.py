import os
import sys
import csv
import time
"""
	ARGUMENTS ORDER [5]: folder path, nr of iterations, Altwalker model, Altwalker algorithm, Altwalker coverage criteria (with/without nr) 

	[1] Folder path example: 
		"LoginModelTests/test1/test2/...."

	[2] Nr of iteration example: 100

	[3] Altwalker model example:
		"LoginModel_Simple"

	[4] Altwalker algorithm example:
		"random"

	[5] Altwalker coverage example:
		"edge_coverage(100)"
		"reached_edge(edge_name)"
"""

# Create directory from path parameter
parent_dir = "C:/altwalker/DISERTATIE/dissertation-hrapp/offlineTests2/"
# to be received as parameter   
directory = sys.argv[1]
full_path = os.path.join(parent_dir, directory)
try: 
    if not os.path.exists(full_path):
    	os.makedirs(full_path)
except OSError as error: 
    print(error)  

# Initialize CSV file from path parameter with metrics columns: id, time, steps
# open the file in the write mode
with open(full_path + 'metrics.csv', 'w', newline='') as f:
    # create the csv writer
    writer = csv.writer(f)
    # write a row to the csv file
    header = ['Id', 'Generation time','Nr of test steps']
    writer.writerow(header)

def append_to_csv_file(it_id, time, steps):
	with open(full_path + 'metrics.csv', 'a', newline='') as f:
		writer = csv.writer(f)
		data = [it_id, time, steps]
		writer.writerow(data)

# time in milliseconds from seconds
def get_current_time():
	return time.time() * 1000

def countStepsInFile(path):
	file = open(path, "r")
	data = file.read()
	occurrences = data.count('"id": "e')
	return occurrences


# Begin FOR cycle (starts from 0)
iterations = int(sys.argv[2])
for i in range(iterations):

	# Initialize startTime
	start_time = get_current_time()

	# Execute altwalker command given as parameter + save JSON output concatenated to current iteration number in the new directory
	os.system('altwalker offline -m models/'+sys.argv[3]+'.json "'+sys.argv[4]+'('+sys.argv[5]+')" -f ' + full_path + '/test' + str(i+1) + '.json')

	# Calculate end time and total time
	total_time = get_current_time() - start_time

	# Extract total edges from the JSON output of Altwalker -> lines that start with ->  "id": "e
	steps = str(countStepsInFile(full_path + '/test' + str(i+1) + '.json'))

	# Append new CSV line to metrics file: iteration id, total time, total edges (steps)
	append_to_csv_file(str(i+1), total_time, steps)

