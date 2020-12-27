from fpdf import FPDF
from PIL import Image
import os
import re

def sorted_alphanumeric(data):
    convert = lambda text: int(text) if text.isdigit() else text.lower()
    alphanum_key = lambda key: [ convert(c) for c in re.split('([0-9]+)', key) ] 
    return sorted(data, key=alphanum_key)

def makePdf(pdfFileName, dir = ''):
    if (dir):
        dir += "/"

    cover = Image.open("1.png")
    width, height = cover.size
    pdf = FPDF(unit = "pt", format = [width, height])

    for filename in sorted_alphanumeric(os.listdir(dir)):
        if filename.endswith(".png"): 
            pdf.add_page()
            pdf.image(filename, 0, 0)
            continue
        else:
            continue

    pdf.output(dir + pdfFileName + ".pdf", "F")