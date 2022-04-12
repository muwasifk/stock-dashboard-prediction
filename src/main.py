import json

# https://betterprogramming.pub/how-to-work-with-json-files-in-python-bedb5b37cbc9
with open("config.json") as jsonFile:
    jsonObject = json.load(jsonFile)
    jsonFile.close()

firstName = jsonObject["firstName"]
lastName = jsonObject["lastName"]

if firstName == "" and lastName == "": 
    print("It seems like you're a new user. What is your name?")
    firstName = input("First Name: ")
    lastName = input("Last Name: ")

    jsonData = {
        "firstName": firstName,
        "lastName": lastName
    }

    with open('config.json', 'w') as jsonFile:
        json.dump(jsonData, jsonFile)
        jsonFile.close()