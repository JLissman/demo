# importing required modules
import PyPDF2
import re
import glob
import os
import csv
from image_extraction import extractProfilePictureFromPDF as saveImage
import aspose.words as aw



def convertDocxToPDF(filename):
    doc = aw.Document(filename)
    pdfName = filename.replace(".docx", ".pdf")
    doc.save(pdfName)
    os.remove(filename)

def getContent(filename):
    print(filename)
    pdfFileObj = open('./'+filename, 'rb')
    pdfReader = PyPDF2.PdfFileReader(pdfFileObj)

    content = ""
    numberOfPages = pdfReader.numPages
    iterator = 0
    for iterator in range(0, numberOfPages):
        content += pdfReader.getPage(iterator).extractText() + "\n"
    content = content.split("\n")
    pdfFileObj.close()
    return content


def getTags(content):
    x = 0
    for line in content:
        if ("SKILLS & TOOLS" in line):
            tagRow = x
        if ("Contact Person" in line or "Contact P erson" in line):
            endTagRow = x
        x += 1
    tags = content[tagRow:endTagRow]
    # clean it up
    cleanTags = []
    for tag in tags:
        cleanTags.append(tag.strip(" "))
    return cleanTags


def getName(content):
    nameRegexPattern = "[–-]+ *([a-zA-Z].*)"
    nameLine = content[0]
    nameNoClean = re.search(nameRegexPattern, nameLine).group()
    nameClean = nameNoClean.replace("–","").replace("-","").strip()
    return nameClean

def getRole(content):
    x = 0
    for line in content:
        if("Roles" in line or "ROLES" in line):
            role = content[x+1]
        x+=1
    return role

def getDescription(content):
    descEndRow = 0
    x = 0
    while descEndRow == 0:
        line = content[x]
        if line == '  ':
            descEndRow = x
        x+=1
    description = content[4:descEndRow]
    return description

def getLocation(content):
    pass




def checkFolder():
    folderPath = ("../cvReader/cvs/*")#../cvReader/cvs/*.pdf
    fileNames = [os.path.relpath(x) for x in glob.glob(folderPath)]
    return fileNames



def loadCSV():
    result = []
    with open('../cvReader/checkedPeople.csv', 'r') as csvFile:
        reader = csv.reader(csvFile)
        for row in reader:
            result.append(row)
        return result


def writeCSV(data):
    with open('../cvReader/checkedPeople.csv', 'a', newline='') as file:
        writer = csv.writer(file, delimiter='\n', quotechar='|', quoting=csv.QUOTE_MINIMAL)
        writer.writerow(data)


def purpleScoutCV(cv):
    content = getContent(cv)
    tags = getTags(content)
    name = getName(content)
    role = getRole(content)
    description = getDescription(content)
    cvDict = {"name":name, "role":role, "description":description, "tags":tags}
    return cvDict

def adessoCV(cv):
    pass

if __name__ == '__main__':
    fileNames = checkFolder()
    checkedFiles = loadCSV()

    for file in fileNames:
        if '.docx' in file and file.replace(".docx", ".pdf") not in fileNames:
            print("found docx")
            convertDocxToPDF(file)
            fileNames = checkFolder()

    for file in fileNames:
        if file not in (item for sublist in checkedFiles for item in sublist):
            if('adesso' in file):
                adessoCV(file)
            else:
                content = getContent(file)
                tags = getTags(content)
                name = getName(content)
                split_name = name.split(" ", 1)
                first_name = split_name[0]  #0
                last_name = split_name[1:]  #1
                role = getRole(content)
                description = getDescription(content)
                saveImage(file, name)
                image_url = "{{ url_for('static', filename='profilePictures/"+name+".jpg') }}"
                writeCSV([file])
                print(name)
                print(role)
                profile_list.append((first_name, last_name, role, image_url, location, description, tags))
        else:
            print("already added this CV")