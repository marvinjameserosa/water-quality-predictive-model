import serial

def read_data(PORT : str, BAUDRATE : int ) -> dict:
 
  error: str =  "An error has occured."
  data_dict = {
    'exception':'',
    'pH':'None',
    'temperature':'None',
    'do':'None',
    'turbidity':'None',
  }

  try:
    ser = serial.Serial(port=PORT, baudrate=BAUDRATE)
    data_dict['exception'] = ''

    for _ in range(7):
      raw_data = ser.readline().decode('utf-8').strip()
      data = raw_data.split(':')
      data_dict[data[0]]=data[1]

  except serial.SerialException as error:
    error = error + str(error)
    data_dict['exception'] = error

  return data_dict    
 