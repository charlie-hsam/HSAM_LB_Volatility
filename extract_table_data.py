import json
from datetime import datetime
import xlwings as xw
from update_and_upload_data import TIME_PERIOD, WEIGHT_END, WEIGHT_STEP

WB_PATH = (r"C:\Users\cdela\High Street Asset Management\High Street - AA) High Street Asset Management\Marketing\LB "
           r"Risk-Adjusted Metrics\Local Balanced & Top 4 Peers Risk Metrics.xlsx")
TIME_PERIOD = TIME_PERIOD
WEIGHT_END = WEIGHT_END
WEIGHT_STEP = WEIGHT_STEP


def extract_data(sheet):
    # Extract relevant data for the volatility metrics into a Pandas dataframe
    top_metrics = {
        'Annual Return': [sheet['G4'].value, sheet['H4'].value, sheet['I4'].value,
                          sheet['J4'].value],
        'Standard Deviation': [sheet['G5'].value, sheet['H5'].value, sheet['I5'].value, sheet['J5'].value],
        'Downside Deviation': [sheet['G6'].value, sheet['H6'].value, sheet['I6'].value,
                               sheet['J6'].value],
        'Sharpe Ratio': [sheet['G7'].value, sheet['H7'].value, sheet['I7'].value,
                         sheet['J7'].value],
        'Sortino Ratio': [sheet['G8'].value, sheet['H8'].value, sheet['I8'].value,
                          sheet['J8'].value],
        'Correlation to Benchmark': [sheet['G9'].value, sheet['H9'].value, sheet['I9'].value,
                                     sheet['J9'].value]
    }

    advanced_metrics = {
        'Beta (to benchmark)': [sheet['G13'].value, sheet['H13'].value, sheet['I13'].value,
                                sheet['J13'].value],
        'Treynor Ratio': [sheet['G14'].value, sheet['H14'].value, sheet['I14'].value,
                          sheet['J14'].value],
        'Jensen\'s Alpha': [sheet['G15'].value, sheet['H15'].value, sheet['I15'].value,
                            sheet['J15'].value],
        'Upside Capture': [sheet['G16'].value, sheet['H16'].value, sheet['I16'].value,
                           sheet['J16'].value],
        'Downside Capture': [sheet['G17'].value, sheet['H17'].value, sheet['I17'].value,
                             sheet['J17'].value],
        'Capture Ratio': [sheet['G18'].value, sheet['H18'].value, sheet['I18'].value,
                          sheet['J18'].value]
    }

    return {
        'top_metrics': top_metrics,
        'advanced_metrics': advanced_metrics
    }


def cycle_and_store_table_data():
    data = {'last_updated': str(datetime.strftime(datetime.now(), '%Y-%m-%d %H:%M:%S'))}

    with xw.App(visible=False) as app:
        wb = app.books.open(WB_PATH)
        sheet = wb.sheets['SUMMARY TAB']

        for years in range(1, TIME_PERIOD + 1):
            for weight in range(0, WEIGHT_END + WEIGHT_STEP, WEIGHT_STEP):
                # Update values in the workbook using openpyxl
                sheet.range('B5').value = years
                sheet.range('C5').value = weight / 100

                # Force recalculation in Excel
                app.api.CalculateFull()

                # Extract recalculated values
                key = f"{years}_{weight}"
                tables = extract_data(sheet)
                data[key] = tables

                # Debug information
                print(f"Time Period: {years}, Weight: {weight}")
                print("Top Metrics:", tables['top_metrics'])
                print("Advanced Metrics:", tables['advanced_metrics'])

        wb.close()

    with open('chart_and_table_data/volatility_table_data.json', 'w') as f:
        json.dump(data, f, indent=4)


if __name__ == '__main__':
    cycle_and_store_table_data()
