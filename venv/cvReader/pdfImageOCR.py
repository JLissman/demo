import csv
import glob
import os
import fitz
from PIL import Image
import numpy as np
import matplotlib
import pytesseract
from cvReader.image_extraction import extractProfilePictureFromPDF as saveImage
import language_tool_python
from database import add_consult

def getFileNames():
    folderPath = ("C:/Users/Jonathan/PycharmProjects/demo/venv/cvReader/cvs/*")#../cvReader/cvs/*.pdf
    fileNames = [os.path.relpath(x) for x in glob.glob(folderPath)]
    return fileNames



def convertToPng(pdf):
    basepath = "C:\\Users\\Jonathan\\PycharmProjects\\demo\\venv\\cvReader\\"
    pdffile = basepath+pdf
    doc = fitz.open(pdffile)
    page = doc.load_page(0)  # number of page
    pix = page.get_pixmap()
    output = "C:\\Users\\Jonathan\\PycharmProjects\\demo\\venv\\cvReader\\png\\"+pdf.replace(".pdf", ".png")
    pix.save(output)


def getSkillsAndTools(pdf):
    fullImg_path = "C:\\Users\\Jonathan\\PycharmProjects\\demo\\venv\\cvReader\\png\\"+pdf.replace(".pdf",".png")
    output = "C:\\Users\\Jonathan\\PycharmProjects\\demo\\venv\\cvReader\\png\\" + pdf.replace(".pdf", "TOOLS.png")

    im = Image.open(fullImg_path)

    fullX, fullY = im.size
    Y,X = getSkillsStartCoords(fullImg_path)[0]
    crop_rectangle = (Y, X, fullX, fullY-100)
    cropped_im = im.crop(crop_rectangle)
    cropped_im.save(output)


    #im = Image.open(output)
    #stopY, stopX = getSkillsEndCoords(output)
    #crop_rectangle2 = (0,0, stopY+10, stopX+5)
    #cropped_im2 = im.crop(crop_rectangle2)
    #cropped_im2.show()
    #cropped_im2.save(output)


def getDescriptionImg(pdf):
    fullImg_path = "C:\\Users\\Jonathan\\PycharmProjects\\demo\\venv\\cvReader\\png\\" + pdf.replace(".pdf", ".png")
    output = "C:\\Users\\Jonathan\\PycharmProjects\\demo\\venv\\cvReader\\png\\" + pdf.replace(".pdf", "DESC.png")

    im = Image.open(fullImg_path)

    fullX, fullY = im.size
    skillStartList = getProfileCardCoords(fullImg_path)
    startX, startY = getHighestXandLowestY(skillStartList)

    toolsStartList = getSkillsStartCoords(fullImg_path)
    endX,endY = getHighestXandLowestY(toolsStartList)

    crop_rectangle = (startX, startY, endX, endY)
    cropped_im = im.crop(crop_rectangle)
    #cropped_im.show()
    cropped_im.save(output)


def getSkillsStartCoords(image):
    pim = Image.open(image).convert('RGB')
    im = np.array(pim)
    #PIL uses RGB ordering
    blue = [5,44,70]
    # Get X and Y coordinates of all blue pixels
    Y, X = np.where(np.all(im == blue, axis=2))

    if Y.size == 0 and X.size == 0:
        blue = [5, 45, 71]
        Y,X = np.where(np.all(im== blue, axis=2))
        if Y.size == 0 and X.size == 0:
            blue = [5, 43, 69]
            Y,X = np.where(np.all(im==blue, axis=2))


    #make it into an array
    zipped = np.column_stack((X, Y))
    #return first occurance of pixel
    return zipped

def getProfileCardCoords(image):
    pim = Image.open(image).convert('RGB')
    im = np.array(pim)
    lightBlue = [220,230,241]

    Y, X = np.where(np.all(im==lightBlue, axis=2))

    if(Y.size == 0 and X.size == 0):
        lightBlue = [218, 229, 241]
        Y, X = np.where(np.all(im == lightBlue, axis=2))

    zipped = np.column_stack((X, Y))
    return zipped



def extractTextFromImage(pdf):
    #change this to relative path - current issue is that celery cant read relative path
    fullImg_path = "C:\\Users\\Jonathan\\PycharmProjects\\demo\\venv\\cvReader\\png\\" + pdf
    # Define path to tessaract.exe
    path_to_tesseract = r'C:\Program Files\Tesseract-OCR\tesseract.exe'
    # Define path to image

    # Point tessaract_cmd to tessaract.exe
    pytesseract.tesseract_cmd = path_to_tesseract
    # Open image with PIL
    img = Image.open(fullImg_path)
    size = 7016, 4961
    im_resized = img.resize(size)
    # Extract text from image
    text = pytesseract.image_to_string(im_resized)
    #print(text)
    return text

def getHighestXandLowestY(coords):
    placeholderX = 0
    placeholderY = 9000
    for x,y in coords:
        if x > placeholderX:
            placeholderX = x
        if y < placeholderY:
            placeholderY = y
    return (placeholderX, placeholderY)

def getHighestXandHighestY(coords):
    placeholderX = 0
    placeholderY = 0
    for x,y in coords:
        if x > placeholderX:
            placeholderX = x
        if y > placeholderY:
            placeholderY = y
    return (placeholderX, placeholderY)


def getLowestXandHighestY(coords):
    placeholderX = 9000
    placeholderY = 0
    for x,y in coords:
        if x < placeholderX:
            placeholderX = x
        if y > placeholderY:
            placeholderY = y
    return (placeholderX, placeholderY)


def checkPngs():
    #check folder if png exist
    pass


def getTitle(pdf):
    fullImg_path = "C:\\Users\\Jonathan\\PycharmProjects\\demo\\venv\\cvReader\\png\\" + pdf.replace(".pdf", ".png")
    output = "C:\\Users\\Jonathan\\PycharmProjects\\demo\\venv\\cvReader\\png\\" + pdf.replace(".pdf", "CARD.png")

    im = Image.open(fullImg_path)

    fullX, fullY = im.size
    profileCardCoords = getProfileCardCoords(fullImg_path)
    startX, startY = profileCardCoords[0]
    endX, endY = profileCardCoords[-1]

    crop_rectangle = (startX-10, startY+130, endX, fullY/2)
    #print(crop_rectangle)
    cropped_im = im.crop(crop_rectangle)
    #cropped_im.show()
    cropped_im.save(output)


def checkSpellingAndGrammar(text):
    my_tool = language_tool_python.LanguageTool('en-US')

    correct_text = my_tool.correct(text)

    # printing some texts
    print("Original Text:", text)
    print("Text after correction:", correct_text)


def loadCSV():
    result = []
    with open('C:/Users/Jonathan/PycharmProjects/demo/venv/cvReader/checkedPeople.csv', 'r') as csvFile:
        reader = csv.reader(csvFile)
        for row in reader:
            result.append(row)
        return result


def writeCSV(data):
    with open('C:/Users/Jonathan/PycharmProjects/demo/venv/cvReader/checkedPeople.csv', 'a', newline='') as file:
        writer = csv.writer(file, delimiter='\n', quotechar='|', quoting=csv.QUOTE_MINIMAL)
        writer.writerow(data)


if __name__ == '__main__':
    files = getFileNames()
    checkedFiles = loadCSV()
    profiles = []
    for file in files:
        if file not in (item for sublist in checkedFiles for item in sublist):
            print("working on "+file)
            convertToPng(file)

            getSkillsAndTools(file)
            skills = extractTextFromImage(file.replace(".pdf", "TOOLS.png")).split("\n")
            #extract skills
            tags = []
            for skill in skills:
                if skill != skill.upper() and skill != "y of Aspose. Words. To discover the full versions of our APIs" and skill != "yose.com/words/":
                    tags.append(skill)

            getDescriptionImg(file)
            description = extractTextFromImage(file.replace(".pdf", "DESC.png")).replace("'","")
            #getLocationImg(file)
            getTitle(file)
            nameAndtitle = extractTextFromImage(file.replace(".pdf", "CARD.png")).split("\n")
            title = nameAndtitle[1]
            name = nameAndtitle[0]
            print(name)
            firstname = name.split(" ")[0]
            lastname_split = name.split(" ")[1:]
            lastname = ""
            for n in lastname_split:
                lastname += " " + n

            saveImage(file, name)
            image_url = 'profilePictures/' + name + '.jpg'
            profiles.append({"firstname":firstname,"lastname":lastname.strip(), "title":title,"location":"Malmö", "description":str(description), "image_url":image_url, "tags":tags})
            writeCSV(file)
    print("adding consultants to db")
    for p in profiles:
        add_consult(p)