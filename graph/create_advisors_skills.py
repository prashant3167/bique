import csv
import pandas as pd

advisors = pd.read_csv('graph/final_advisors.csv')
skills = pd.read_csv('graph/skills.csv')

file = open('graph/skill_mappings.csv', 'w+', newline='')

writer = csv.writer(file)
writer.writerow(['advisor_id','skill_id'])

advisors_list =  list(advisors.id)

for i in advisors_list:
    advisor =  advisors[advisors["id"] == i]
    advisor_skill = advisor["skills"].iloc[0]
    all_skills = advisor_skill.split('|')
    for x in all_skills:
        myId = skills['id'][skills['skill'] == x.lower()]
        writer.writerow([i, myId.to_string(index=False)])