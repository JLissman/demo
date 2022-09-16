import glob
import os
import fitz
from PIL import Image
import numpy as np
import matplotlib
import pytesseract
from cvReader.image_extraction import extractProfilePictureFromPDF as saveImage


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


def getDescription(pdf):
    fullImg_path = "C:\\Users\\Jonathan\\PycharmProjects\\demo\\venv\\cvReader\\png\\" + pdf.replace(".pdf", ".png")
    output = "C:\\Users\\Jonathan\\PycharmProjects\\demo\\venv\\cvReader\\png\\" + pdf.replace(".pdf", "DESC.png")

    im = Image.open(fullImg_path)

    fullX, fullY = im.size
    skillStartList = getProfileCardCoords(fullImg_path)
    startX, startY = getHighestXandLowestY(skillStartList)

    toolsStartList = getSkillsStartCoords(fullImg_path)
    endX,endY = getHighestXandLowestY(toolsStartList)

    crop_rectangle = (startX, startY, endX, endY)
    print(crop_rectangle)
    cropped_im = im.crop(crop_rectangle)
    cropped_im.show()
    cropped_im.save(output)


def getSkillsStartCoords(image):
    pim = Image.open(image).convert('RGB')
    print("getting coords for "+image)
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
    print("ZIPPED")
    print(zipped)
    return zipped



def extractTextFromImage(pdf):
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
    print(text)
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

if __name__ == '__main__':
    files = getFileNames()
    for file in files:
        convertToPng(file)
        getSkillsAndTools(file)
        skills = extractTextFromImage(file.replace(".pdf", "TOOLS.png"))
        getDescription(file)
        description = extractTextFromImage(file.replace(".pdf", "DESC.png"))
        


        saveImage(file, name)
        image_url = "{{ url_for('static', filename='profilePictures/" + name + ".jpg') }}"
