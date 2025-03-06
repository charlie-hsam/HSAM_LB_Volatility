import json
import xlwings as xw
from datetime import datetime
from update_and_upload_data import TIME_PERIOD, WEIGHT_END, WEIGHT_STEP

WB_PATH = (r"C:\Users\cdela\High Street Asset Management\High Street - AA) High Street Asset Management\Marketing\LB "
           r"Risk-Adjusted Metrics\Local Balanced & Top 4 Peers Risk Metrics.xlsx")


def extract_chart_data(sheet):
    # Ensure the correct sheet is active
    sheet.activate()
    # Debug: Print sheet name to confirm correct sheet is being accessed
    print(f"Accessing sheet: {sheet.name}")

    # Count the number of rows with data
    start_row = 4  # Adjusted start row based on provided image
    end_row = start_row
    while sheet.range(f'B{end_row}').value is not None:
        end_row += 1

    # Debug: Print the detected range
    print(f"Detected data range: B{start_row} to B{end_row - 1}")

    if end_row == start_row:
        print("No data found in the specified range.")
        return {}

    # Columns to extract data from
    columns = ['B', 'C', 'D', 'E', 'F']
    headers = ['dates', 'HSAM LB Fund', 'Benchmark', 'Largest 4 Funds (Equally Weighted)',
               'Largest 4 Funds (EW) + x% HSAM']

    # Extract line chart data
    chart_data = {}
    for col, header in zip(columns, headers):
        data = [sheet.range(f'{col}{i}').value for i in range(start_row, end_row)]
        # Convert datetime objects to strings
        if header == 'dates':
            data = [dt.strftime('%Y-%m-%d') if isinstance(dt, datetime) else dt for dt in data]
        chart_data[header] = data
        # Debug: Print extracted data for each header
        print(f"Extracted {header} data: {data}")

    return chart_data


def cycle_and_store_chart_data():
    data = {'last_updated': str(datetime.strftime(datetime.now(), '%Y-%m-%d %H:%M:%S'))}

    with xw.App(visible=False) as app:
        wb = app.books.open(WB_PATH)
        input_sheet = wb.sheets['SUMMARY TAB']
        chart_sheet = wb.sheets['CHART DATA']

        for years in range(1, TIME_PERIOD + 1):
            for weight in range(0, WEIGHT_END + WEIGHT_STEP, WEIGHT_STEP):
                # Update values in the workbook
                input_sheet.range('B5').value = years
                input_sheet.range('C5').value = weight / 100

                # Debug: Confirm values are updated
                print(f"Setting time period to {years} and weight to {weight / 100}")

                # Force recalculation in Excel
                app.api.CalculateFull()

                # Extract recalculated values
                key = f"{years}_{weight}"
                chart_data = extract_chart_data(chart_sheet)
                data[key] = chart_data

                # Debug information
                print(f"Time Period: {years}, Weight: {weight}")
                print("Chart Data:", chart_data)

        wb.close()

    with open('chart_and_table_data/volatility_chart_data.json', 'w') as f:
        json.dump(data, f, indent=4)


if __name__ == '__main__':
    cycle_and_store_chart_data()
