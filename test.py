from packages.data_package.dict_to_csv import dict_to_csv


data_dict = {
  'exception':'1',
  'pH':'1',
  'temperature':'asd',
  'do':'None',
  'turbidity':'None',
}

dict_to_csv(data_dict, "sensor_data.csv")