import re

def cleanData(text: str):
    # develop the pattern
    pattern = r"[^a-zA-Z0-9]"  # ^ ye ye bata raha hai k inka ilawa baki sab remove krdo
    # clean the data

    cleanedData = re.sub(pattern, "",text)    # re.sub clean and special charactors remove krna main help krta hai
    # "" this represents empty strings
    cleanedData = cleanedData.strip()        # .strip is used to remove space in the strings bcz in database it's an error         
    
    # return the data
    return cleanedData

print(cleanData("noumanejaz64@gmail.com"))