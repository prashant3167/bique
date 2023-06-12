import csv
import pandas as pd
import os

print(os.getcwd())
advisors = pd.read_csv('graph/final_advisors.csv')

file = open('graph/skills.csv', 'w+', newline='')
writer = csv.writer(file)

advisors_list =  list(advisors.id)

uniqueSkills = []

for i in advisors_list:
    advisor =  advisors[advisors["id"] == i]
    advisor_skill = advisor["skills"].iloc[0]

    for x in advisor_skill.split('|'):
        if x.lower() not in uniqueSkills:
            uniqueSkills.append(x.lower())

writer.writerow(['id','skill'])

for i in range(len(uniqueSkills)):   
    writer.writerow([f'skill_{str(i)}',uniqueSkills[i]])
