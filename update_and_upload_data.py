import os
from extract_table_data import cycle_and_store_table_data
from extract_chart_data import cycle_and_store_chart_data

if __name__ == '__main__':
    # cycle_and_store_table_data()
    # cycle_and_store_chart_data()
    os.system("git add "
              "chart_and_table_data/volatility_chart_data.json "
              "chart_and_table_data/volatility_table_data.json")
    os.system('git commit -m "Updated JSON data from python script"')
    os.system("git push origin main")
