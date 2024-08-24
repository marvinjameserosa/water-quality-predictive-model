import pandas as pd

class CCMEWQICalculator:
    def __init__(self, csv_file):
        self.data = pd.read_csv(csv_file, parse_dates=['Timestamp'])
        self.data['Date'] = self.data['Timestamp'].dt.date  # Extract the date from the timestamp
        self.data = self.data.dropna(subset=['Dissolved Oxygen', 'pH', 'Temperature', 'Turbidity'])  # Drop rows with null values
        self.data = self.data[self.data['Timestamp'].dt.minute.isin([0, 30])]  # Filtering timestamp with 30 Mins Intervals

    def calculate_wqi_per_day(self):
        # Group by 'Date' and calculate WQI for each day
        daily_wqi = self.data.groupby('Date').apply(self.calculate_wqi).reset_index(name='WQI')
        return daily_wqi

    def calculate_wqi(self, group):
        f1 = self.calculate_f1(group)
        f2 = self.calculate_f2(group)
        f3 = self.calculate_f3(group)

        wqi = 100 - ((f1**2 + f2**2 + f3**2)**0.5) / 1.732
        return round(wqi, 2)

    def calculate_f1(self, group):
        num_failed_tests = group.apply(self.is_failed, axis=1).sum()
        total_tests = group.shape[0] * 4  # 4 tests per sample 
        return (num_failed_tests / total_tests) * 100

    def calculate_f2(self, group):
        failed_tests = group.apply(self.is_failed, axis=1)
        total_tests = group.shape[0] * 4  # 4 tests per sample
        num_failed_values = group[failed_tests].count().sum()
        return (num_failed_values / total_tests) * 100

    def calculate_f3(self, group):
        deviations = group.apply(self.deviation_from_standard, axis=1).sum()
        num_failed_tests = group.apply(self.is_failed, axis=1).sum()
        return deviations / num_failed_tests if num_failed_tests != 0 else 0

    def is_failed(self, row):
        # Check against the updated thresholds
        return (row['Dissolved Oxygen'] < 6 or  # Corrected DO threshold
                row['pH'] < 6.5 or row['pH'] > 8.5 or 
                row['Temperature'] < 15 or row['Temperature'] > 25 or
                row['Turbidity'] >= 10)

    def deviation_from_standard(self, row):
        deviation = 0
        max_deviation_per_parameter = 100  # Cap the maximum deviation for each parameter

        if row['Dissolved Oxygen'] < 6:  # Updated DO threshold
            deviation += min((6 - row['Dissolved Oxygen']) / 6 * 100, max_deviation_per_parameter)
        if row['pH'] < 6.5 or row['pH'] > 8.5:  # Updated pH threshold
            deviation += min(abs(row['pH'] - 7.5) / 7.5 * 100, max_deviation_per_parameter)  # Updated ideal pH
        if row['Temperature'] < 15 or row['Temperature'] > 25:
            if row['Temperature'] < 15:
                deviation += min((15 - row['Temperature']) / 15 * 100, max_deviation_per_parameter)
            else:
                deviation += min((row['Temperature'] - 25) / 25 * 100, max_deviation_per_parameter)
        if row['Turbidity'] >= 10:
            deviation += min((row['Turbidity'] - 10) / 10 * 100, max_deviation_per_parameter)
        return deviation

    def save_wqi_to_csv(self, output_file):
        daily_wqi = self.calculate_wqi_per_day()
        daily_wqi.to_csv(output_file, index=False)
        print(f"Daily WQI values saved to {output_file}")

if __name__ == "__main__":
    calculator = CCMEWQICalculator(r"D:\Downloads\water_qua.csv")
    calculator.save_wqi_to_csv(r"D:\Downloads\daily_wqi.csv")