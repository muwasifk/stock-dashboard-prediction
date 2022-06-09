"""
ICS3U 
Muhammad Wasif Kamran & Eric Sui 
This file contains the code that runs in terminal at the start of the programming if the user is new. 
"""

# Import json library to access JSON files
import json

# Open the JSON file and add the contents to a dictionary
with open("config.json") as jsonFile:
    jsonObject = json.load(jsonFile)
    jsonFile.close()

# Access the first name and last name of the user from the dictionary (will be empty string if they have not added their names yet)
firstName = jsonObject["firstName"]
lastName = jsonObject["lastName"]

# Run the following lines if and only if the first name and last name have not been saved yet
if firstName == "" and lastName == "": 
    # Tell the user what is happening at the intial running of the program
    print("It seems like you're a new user. What is your name?")
    # Get inputs for first and last name
    firstName = input("First Name: ")
    lastName = input("Last Name: ")

    # Store their names in a dictionary
    jsonData = {
        "firstName": firstName,
        "lastName": lastName
    }

    # Add their inputted information to the dictionary
    with open('config.json', 'w') as jsonFile:
        json.dump(jsonData, jsonFile)
        jsonFile.close()