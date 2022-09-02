import fitz
import io
from PIL import Image, ImageChops


def extractProfilePictureFromPDF(file, fullName):
    pdf_file = fitz.open(file)
    x = 4
    for page_index in range(len(pdf_file)):
        page = pdf_file[page_index]
        image_list = page.get_images()
        #if image_list:
        #    print(f"[+] Found a total of {len(image_list)} images in page {page_index}")
        #else:
        #    print("[!] No images found on page", page_index)

        for image_index, img in enumerate(page.get_images(), start=1):
            xref = img[0]
            base_image = pdf_file.extract_image(xref)
            image_bytes = base_image["image"]
            image = Image.open(io.BytesIO(image_bytes)).convert('RGB')

            for x in range(1,3):
                adesso_image = Image.open('adesso_'+str(x)+".png").convert('RGB')
                diff_adesso = ImageChops.difference(image, adesso_image).getbbox()

                scout_image = Image.open('scout_' + str(x) + ".png").convert('RGB')
                diff_scout = ImageChops.difference(image, scout_image).getbbox()
                if(diff_scout and diff_adesso):
                    image.save("../static/profilePictures/"+fullName+".jpg")



            image_ext = base_image["ext"]




#if __name__ == "__main__":
#    extractProfilePictureFromPDF("./cvs/adesso-Consulting profile_Jonah Carneskog_22 June 2022.pdf",'Jonah Carneskog')