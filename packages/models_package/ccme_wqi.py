import pandas as pd

class CCMEWQICalculator:
  def __init__(self, csv_file):
      self.data = pd.read_csv(csv_file, parse_dates=['Timestamp'])
      self.data['Date'] = self.data['Timestamp'].dt.date  # Extract the date from the timestamp
      self.data = self.data.dropna(subset=['Dissolved Oxygen', 'pH', 'Temperature', 'Turbidity'])  
      self.total_parameters = 4  

  # Group by 'Date' and calculate WQI for each day
  def compute_daily_wqi(self):
      daily_wqi = self.data.groupby('Date').apply(self.calculate_wqi).reset_index(name='WQI')
      return daily_wqi

  def calculate_wqi(self, group):
      f1 = self.calculate_f1(group)
      f2 = self.calculate_f2(group)
      f3 = self.calculate_f3(group)

      print(f"F1: {f1}, F2: {f2}, F3: {f3}")  # Debugging print
      
      # Simplified WQI formula for debugging
      wqi = 100 - (f1 + f2 + f3) / 3  # Average the components for a simpler check
      
      return round(wqi, 2)


  def calculate_f1(self, group):
      # F1: Percentage of failed parameters
      num_failed_parameters = group.apply(self.count_failed_parameters, axis=1).sum()
      total_tests = group.shape[0] * self.total_parameters
      return (num_failed_parameters / total_tests) * 100

  def calculate_f2(self, group):
      # F2: Percentage of failed tests
      num_failed_tests = group.apply(self.is_any_parameter_failed, axis=1).sum()
      total_tests = group.shape[0]  # Total number of tests in a day
      return (num_failed_tests / total_tests) * 100

  def calculate_f3(self, group):
      deviations = group.apply(self.deviation_from_standard, axis=1).sum()
      num_failed_tests = group.apply(self.is_any_parameter_failed, axis=1).sum()
      return deviations / num_failed_tests if num_failed_tests != 0 else 0

  def count_failed_parameters(self, row)->int:
      # Count how many parameters fail in a given row
      failed_count = 0
      if row['Dissolved Oxygen'] < 5:
          failed_count += 1
      if row['pH'] < 6.5 or row['pH'] > 9.0:
          failed_count += 1
      if row['Temperature'] < 25 or row['Temperature'] > 31:
          failed_count += 1
      if row['Turbidity'] >= 5:
          failed_count += 1
      return failed_count

  def is_any_parameter_failed(self, row):
      # Check if any parameter fails in a given row (test)
      return (row['Dissolved Oxygen'] < 5 or
              row['pH'] < 6.5 or row['pH'] > 9.0 or
              row['Temperature'] < 25 or row['Temperature'] > 31 or
              row['Turbidity'] >= 5)

  def deviation_from_standard(self, row):
      deviation = 0
      if row['Dissolved Oxygen'] < 5:
          deviation += (5 - row['Dissolved Oxygen']) / 5 * 100
      if row['pH'] < 6.5 or row['pH'] > 9.0:
          deviation += abs(row['pH'] - 7.75) / 7.75 * 100
      if row['Temperature'] < 25 or row['Temperature'] > 31:
          if row['Temperature'] < 25:
              deviation += (25 - row['Temperature']) / 25 * 100
          else:
              deviation += (row['Temperature'] - 31) / 31 * 100
      if row['Turbidity'] >= 5:
          deviation += (row['Turbidity'] - 5) / 5 * 100
      return deviation

  def save_to_csv(self, output_file):
      daily_wqi = self.calculate_wqi_per_day()
      daily_wqi.to_csv(output_file, index=False)
      print(f"Daily WQI values saved to {output_file}")


