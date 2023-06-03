<<<<<<< HEAD
import csv
import json

with open('advisors.json', 'r') as file:
    json_data = json.load(file)

file = open('final_advisors.csv', 'w', newline='')
writer = csv.writer(file)

for data in json_data:
    all_data = []

    uid = data["recno"]
    all_data.append(uid)

    name = data["shortName"]
    all_data.append(name)

    skills = []
    if data.get("attrSkills",None):
        for group in data["attrSkills"]:
            skills = skills + [i["skill"]["name"] for i in group["skills"]]
    else:
        skills = ['groceries','shopping']
    all_data.append("|".join(skills))

    jobs = data["totalJobs"]
    all_data.append(jobs)

    charge = data["serviceProfiles"][0]["aggregates"]["totalCharge"]
    all_data.append(charge)

    writer.writerow(all_data)



=======
import csv
import json

with open('advisors.json', 'r') as file:
    json_data = json.load(file)

file = open('final_advisors.csv', 'w', newline='')
writer = csv.writer(file)

for data in json_data:
    all_data = []

    uid = data["recno"]
    all_data.append(uid)

    name = data["shortName"]
    all_data.append(name)

    skills = []
    if data.get("attrSkills",None):
        for group in data["attrSkills"]:
            skills = skills + [i["skill"]["name"] for i in group["skills"]]
    else:
        skills = ['groceries','shopping']
    all_data.append("|".join(skills))

    jobs = data["totalJobs"]
    all_data.append(jobs)

    charge = data["serviceProfiles"][0]["aggregates"]["totalCharge"]
    all_data.append(charge)

    writer.writerow(all_data)



>>>>>>> deaad08941bc82050c10cfbf6a73da6cc1b107c2
