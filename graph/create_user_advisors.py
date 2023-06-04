import csv
import pandas as pd
import random
from datetime import datetime, timedelta

# Define the start and end dates
start_date = datetime(2023, 1, 1)
end_date = datetime(2023, 12, 31)

# Calculate the number of days between the start and end dates
days_diff = (end_date - start_date).days

users = pd.read_csv('users.csv')
advisors = pd.read_csv('final_advisors.csv')

file = open('mapping.csv', 'w+', newline='')
writer = csv.writer(file)
user_list = list(users.id)
advisors_list =  list(advisors.id)
for i in user_list:
    for j in range(random.randint(5,8)):
        advisor =  advisors[advisors["id"]==random.choice(advisors_list)]
        advisor_skill = advisor["skills"].iloc[0]
        random_days = random.randint(0, days_diff)

        # Create the random date by adding the random number of days to the start date
        random_date = start_date + timedelta(days=random_days)

        x = random.choice(advisor_skill.split('|'))
        # print(x)
        writer.writerow([i,advisor["id"].to_string(index=False),x,random.randint(4,10),random_date.date()])