import json
import sys
import argparse
import requests
import random

parser = argparse.ArgumentParser()
parser.add_argument('-nc', '--no-color', '--no-colour', dest="color", help="disable colors", action="store_false", default=True)
parser.add_argument('-u', '--user', dest="username",help="select user", required=True)
args = parser.parse_args()

if args.color:
    color = random.choice([
            "\033[1;91m",
            "\033[1;92m",
            "\033[1;93m",
            "\033[1;94m",
            "\033[1;95m", 
            "\033[1;96m"
    ])
    reset = "\033[0m"
else:
    color = ""
    reset = ""

repos = requests.get(f"https://api.github.com/users/{args.username}/repos").json()

try:
    print(f"Error : {repos['message']}")
    exit()
except:
    pass

privateRepoNumber = 0
repoNumber = len(repos)
moreStared = ["unkown", 0]
totalStars = 0
moreForked = ["unkown", 0]
totalForks = 0
licenses = {}
moreUsedLicense = ["unkown", 0]
languages = {}
moreUsedLanguage = ["unkown", 0]

for currentRepo in repos:
    if currentRepo["private"]:
        privateRepoNumber += 1
    if currentRepo["stargazers_count"] > moreStared[1]:
        moreStared[0] = currentRepo["name"]
        moreStared[1] = currentRepo["stargazers_count"]
    if currentRepo["forks"] > moreForked[1]:
        moreForked[0] = currentRepo["name"]
        moreForked[1] = currentRepo["forks"]
    if currentRepo["license"] != None:
        try:
            licenses[currentRepo["license"]["key"]]["score"] += 1
        except KeyError:
            licenses[currentRepo["license"]["key"]] = {}
            licenses[currentRepo["license"]["key"]]["score"] = 1
            licenses[currentRepo["license"]["key"]]["name"] = currentRepo["license"]["name"]
    if currentRepo["language"] != None:
        try:
            languages[currentRepo["language"]]["score"] += 1
        except KeyError:
            languages[currentRepo["language"]] = {}
            languages[currentRepo["language"]]["score"] = 1
            languages[currentRepo["language"]]["name"] = currentRepo["language"]
    totalStars += currentRepo["stargazers_count"]
    totalForks += currentRepo["forks"]

for currentLicense in licenses:
    if licenses[currentLicense]["score"] > moreUsedLicense[1]:
        moreUsedLicense[0] = licenses[currentLicense]["name"]
        moreUsedLicense[1] = licenses[currentLicense]["score"]

for currentLanguage in languages:
    if languages[currentLanguage]["score"] > moreUsedLanguage[1]:
        moreUsedLanguage[0] = languages[currentLanguage]["name"]
        moreUsedLanguage[1] = languages[currentLanguage]["score"]
    
print(f"Private repositories : {color}{privateRepoNumber}{reset} ( {color}{round(privateRepoNumber*100/repoNumber,2)}%{reset} )")
print(f"More stared repositories : {color}{moreStared[0]}{reset} with {color}{moreStared[1]}{reset} stars")
print(f"Total stars : {color}{totalStars}{reset} ( {color}{round(totalStars/repoNumber, 2)}{reset} av )")
print(f"More forked repositories : {color}{moreForked[0]}{reset} with {color}{moreForked[1]}{reset} forks")
print(f"Total forked : {color}{totalForks}{reset} ( {color}{round(totalForks/repoNumber, 2)}{reset} av )")
print(f"License prefer : {color}{moreUsedLicense[0]}{reset} with {color}{moreUsedLicense[1]}{reset} repos ( {color}{round(moreUsedLicense[1]*100/repoNumber, 2)}%{reset} )")
print(f"Language prefer : {color}{moreUsedLanguage[0]}{reset} with {color}{moreUsedLanguage[1]}{reset} repos ( {color}{round(moreUsedLanguage[1]*100/repoNumber, 2)}%{reset} )")