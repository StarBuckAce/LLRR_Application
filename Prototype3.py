from PIL import Image
from pytesseract import pytesseract
import tkinter as tk
import enum
import re
import mysql.connector

class OS(enum.Enum):
    Windows = 1

class Language(enum.Enum):
    ENG = 'eng'
    RUS = 'rus'
    ITA = 'ita'

class ImageReader:
    def __init__(self, os: OS):
        if os == OS.Windows:
            windows_path = r'C:\Program Files\Tesseract-OCR\tesseract.exe'
            pytesseract.tesseract_cmd = windows_path

    def extract_text(self, image: str, lang: str) -> str:
        img = Image.open(image)
        extracted_text = pytesseract.image_to_string(img, lang=lang.value)
        return extracted_text

def printInput():
    file_path = inputtxt.get("1.0", "end-1c")
    ir = ImageReader(OS.Windows)
    extracted_text = ir.extract_text(file_path, lang=Language.ENG)
    result_variable.set(extracted_text)
    print("Extracted Text:", extracted_text)
    insert_into_database(extracted_text)

def insert_into_database(text2):

    text2 = text2.split(" ")
    text = []
    for i in text2:
        if "\n" in i:
            i = i.split("\n")
            for j in i:
                text.append(j)
        else:
            text.append(i)
    print(text)

    s = text.index("Hemoglobin(gm%)")
    data1 = [text[s+1], text[s+2], text[s+3], text[s+4]]
    data2 = [text[s+6], text[s+7], text[s+8], text[s+9]]
    data3 = [text[s+11], text[s+12], text[s+13], text[s+14]]
    data4 = [text[s+16], text[s+17], text[s+18], text[s+19]]
    print(data1)
    print(data2)
    print(data3)
    print(data4)

    host = "localhost"
    user = "root"
    password = "madhaesh2004"
    database = "astra"

    connection = mysql.connector.connect(
        host=host,
        user=user,
        password=password,
        database=database
    )

    cursor = connection.cursor()

    cursor.execute('''
        CREATE TABLE IF NOT EXISTS PATIENTDATA (
            HEMOPAST DOUBLE,
            HEMOPRESENT DOUBLE,
            HEMOLOWER DOUBLE,
            HEMOUPPER DOUBLE,
            RBCPAST DOUBLE,
            RBCPRESENT DOUBLE,
            RBCLOWER DOUBLE,
            RBCUPPER DOUBLE,
            WBCPAST DOUBLE,
            WBCPRESENT DOUBLE,
            WBCLOWER DOUBLE,
            WBCUPPER DOUBLE,
            PLATELETPAST DOUBLE,
            PLATELETPRESENT DOUBLE,
            PLATELETLOWER DOUBLE,
            PLATELETUPPER DOUBLE
        );
    ''')

    command = "INSERT INTO PATIENTDATA (HEMOPAST, HEMOPRESENT, HEMOLOWER, HEMOUPPER, RBCPAST, RBCPRESENT, RBCLOWER, RBCUPPER, WBCPAST, WBCPRESENT, WBCLOWER, WBCUPPER, PLATELETPAST, PLATELETPRESENT, PLATELETLOWER, PLATELETUPPER) VALUES (" + str(data1[0]) + ","  + str(data1[1]) + ","  + str(data1[2]) + ","  + str(data1[3]) + "," + str(data2[0]) + ","  + str(data2[1]) + ","  + str(data2[2]) + ","  + str(data2[3]) + "," + str(data3[0]) + ","  + str(data3[1]) + ","  + str(data3[2]) + ","  + str(data3[3]) + "," + str(data4[0]) + ","  + str(data4[1]) + ","  + str(data4[2]) + ","  + str(data4[3]) + ");"
    cursor.execute(command)

    connection.commit()
    connection.close()

# Creating a frame
frame = tk.Tk()
frame.title("Image Text Extractor")
frame.geometry('400x250')

# Text Entry Field
lbl_file_path = tk.Label(frame, text="Enter File Path:")
lbl_file_path.pack()
inputtxt = tk.Text(frame, height=1, width=30)
inputtxt.pack()

# Button
btn_extract_text = tk.Button(frame, text="Extract Text", command=printInput)
btn_extract_text.pack()

# Variable to store the extracted text
result_variable = tk.StringVar()

# Label to display the extracted text
lbl = tk.Label(frame, textvariable=result_variable)
lbl.pack()

frame.mainloop()
