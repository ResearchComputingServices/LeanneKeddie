import csv

unique_data = []

with open('../docs/4000_test_cases.csv', 'r') as file:
    reader = csv.reader(file)
    csv_file = list(reader)
    
    for i, i_row in enumerate(csv_file):
        
        insert = True
        for j, j_row in enumerate(csv_file):
        
            if i == j:
                continue
            
            if i_row[1] == j_row[1] and i_row[2] < j_row[2]:
                insert = False
        
        
        if insert:
            unique_data.append(i_row)
            

output_file = open('../docs/4000_test_cases_cleaned.csv', 'w+')

for item in unique_data:
    
    sentence = item[1]
    label = item[0]
    
    if float(item[2]) < 0.9:
        label = 'Irrelevant'
        
    
    output_file.write(f'{label},\"{sentence}\",{float(item[2])}'+'\n')
    
output_file.close()
        
            
      