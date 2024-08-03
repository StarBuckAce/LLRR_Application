from PIL import Image
from pytesseract import pytesseract
import tkinter as tk
import enum
import re

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

# Print button to print the stored result
btn_print_result = tk.Button(frame, text="Print Numeric Values", command=lambda: printNumericValues(result_variable.get()))
btn_print_result.pack()

def printNumericValues(text):
    # Use regular expression to extract only numeric values
    numeric_values = re.findall(r'\b\d+\b', text)
    numeric_text = ' '.join(numeric_values)
    print("Extracted Numeric Values:", numeric_text)

frame.mainloop()
