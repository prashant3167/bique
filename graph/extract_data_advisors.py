import csv
import json
import random
import datetime

with open('accounts.json', 'r') as file:
    json_data = json.load(file)

file = open('users.csv', 'w', newline='')
writer = csv.writer(file)

for data in json_data:
    all_data = []

    id = data["id"]
    all_data.append(id)

    name = data["name"]
    all_data.append(name)

    # # any rating between 1 to 10
    # rating = random.randint(1,10)
    # all_data.append(rating)

    # start_date = datetime.date(2018, 1, 1)
    # end_date = datetime.date(2022, 12, 31)
    # random_days = random.randint(0, (end_date - start_date).days)
    # random_date = start_date + datetime.timedelta(days=random_days)
    # all_data.append(random_date)

    writer.writerow(all_data)

