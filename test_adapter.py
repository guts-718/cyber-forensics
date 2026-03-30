from adapters.csv_adapter import read_csv_logs

file_path = "data/sample-main-mon-plus.csv"

for i, log in enumerate(read_csv_logs(file_path)):
    print(log["raw"])
    if i == 5:
        break