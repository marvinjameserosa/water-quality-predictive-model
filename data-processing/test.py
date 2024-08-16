import data_processing

input_file = 'data-processing/water_qua.csv'
output_file = 'data-processing/output.html'

#num_rows is defaulted to 100  
data_processing.csv_to_html(input_file, output_file)