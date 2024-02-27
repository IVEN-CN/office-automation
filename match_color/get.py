import csv

data_pass = []
with open('已通过.csv','r') as f:
    reader = csv.reader(f)
    for row in reader:
        data_pass.append(row[0])

data_used = []
with open('已使用.csv','r') as f:
    reader = csv.reader(f)
    for row in reader:
        data_used.append(row[0])

data_unused = list(set(data_pass) - set(data_used))
for i in data_unused:
    print(f'未使用的款号有{i}')
print('结果可能不准确，通过款号的识别可能存在误差，结果仅供参考')
