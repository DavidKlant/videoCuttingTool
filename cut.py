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
            "situation": line[5].replace(" ", "_"),
            "comment": line[6].replace(" ", "_"),
        }
        resultList.append(dict)

    return resultList

######## MAIN #########
# load basePath
baseVideoPath = open("basePath.txt", "r").read()

# create folder
os.system(f"mkdir {baseVideoPath}/output")  
os.system("mkdir UserInput") 

print("\n\nPlease make sure the csv is in the UserInput Folder.")
print("\nPlease replace the text in basePath.txt with the path of your videos.")
print("\nAll files in the folders UserInput & output will be ignored by git.\n\n")

# get user input (csv name & seconds to cut)
csvFileName = "UserInput/" + input("How is your csv called? (incl. \".csv\") ")
secondsToCut = input("How many seconds per Video? ")

# read csv & convert to List<Dict>
csv = pandas.read_csv(csvFileName)
csvMapList = convertCsvToListOfDicts(csv)

# cut all entrys (starting at timestamp for x seconds (x = secondsToCut from user input))
for map in csvMapList:
    fileName = map["username"] + "-" + map["relPath"].replace("/", "-").replace(".mp4", "") + "-" + map["timestamp"].replace(":", "-") + "-" + map["situation"] + "-" + map["comment"]

    startStamp = "00:" + map["timestamp"] + ".0"

    if (len(secondsToCut) == 1):
        secondsToCut = "0" + secondsToCut
    length = "00:00:" + secondsToCut + ".0"

    relPath = baseVideoPath + "/" + map["relPath"]

    # if timestamp == alles -> copy entire video (with new name)
    if map["timestamp"] == "alles":
        cmd = f"cp {relPath} {baseVideoPath}/output/{fileName}.mp4"
        os.system(cmd)
        continue

    # cmd works even if clip is shorter than startStamp + secondsToCut. In that case the clip stops in the end
    cmd = f"ffmpeg -ss {startStamp} -i {relPath} -c copy -t {length} {baseVideoPath}/output/{fileName}.mp4"
    os.system(cmd)
