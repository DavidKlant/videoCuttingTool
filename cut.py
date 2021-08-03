import os
import pandas

# converts relPath like this:
#   "['08.08', 'GH020015.MP4']" --> "08.08/GH020015.MP4"
def resolveRelPath(str):
    # removes unneeded chars
    str = str.replace("[", "")
    str = str.replace("]", "")
    str = str.replace("\'", "")
    # create list
    str = str.split(", ")
    # create fielPath
    str = str[0] + "/" + str[1]
    return str

def convertCsvToListOfDicts(csv):
    csvList = csv.values.tolist()

    resultList = []
    for line in csvList:
        dict = {
            "username": line[0],
            "dateTimeAdded": line[2],
            "relPath": resolveRelPath(line[3]),
            "timestamp": line[4],
            "situation": line[5],
            "comment": line[6]
        }
        resultList.append(dict)

    return resultList

######## MAIN #########
print("Please make sure the Folder with the base Videos & the csv are in the UserInput Folder.")
print("All files in the folders UserInput & output will be ignored by git.\n")
# get user input (csv name & seconds to cut)
csvFileName = "UserInput/" + input("How is your csv called? (incl. \".csv\") ")
secondsToCut = input("How many seconds per Video? ")

# read csv & convert to List<Dict>
csv = pandas.read_csv(csvFileName)
csvMapList = convertCsvToListOfDicts(csv)

# cut all entrys (starting at timestamp for x seconds (x = secondsToCut from user input))
for map in csvMapList:
    fileName = map["username"] + "-" + map["relPath"].replace("/", "-").replace(".mp4", "") + "-" + map["timestamp"] + "-" + map["situation"] + "-" + map["comment"]
    
    startStamp = "00:" + map["timestamp"] + ".0"

    if (len(secondsToCut) == 1):
        secondsToCut = "0" + secondsToCut
    length = "00:00:" + secondsToCut + ".0"

    relPath = "UserInput/" + map["relPath"]

    os.system(f"ffmpeg -ss {startStamp} -i {relPath} -c copy -t {length} output/{fileName}.mp4")
