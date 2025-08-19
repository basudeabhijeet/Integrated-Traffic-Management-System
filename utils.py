import easyocr
import os
import cv2
import re
import ssl
import smtplib
import numpy as np
import pandas as pd
from datetime import datetime
from difflib import get_close_matches
from email.message import EmailMessage
from dotenv import load_dotenv
from document import make_doc  # ✅ Import make_doc from document.py
import glob

ROOT_DIR = "./"

# ✅ Load environment variables at the start
load_dotenv()

folders_to_clean = ["./challan", "./images", "./person"]

def clean_folders():
    """Deletes all files in the specified directories before processing new data."""
    for folder in folders_to_clean:
        if os.path.exists(folder):
            files = glob.glob(os.path.join(folder, "*"))  # Get all files
            for file in files:
                try:
                    os.remove(file)
                    print(f"🗑️ Deleted: {file}")
                except Exception as e:
                    print(f"⚠️ Error deleting {file}: {e}")
        else:
            print(f"🚫 Directory not found: {folder}")

# ✅ Call this at the start of the script
clean_folders()

def closeMatches(patterns, word):
    """Find the closest match for a given word from a list of patterns."""
    matc = get_close_matches(word, patterns, n=1)
    return matc[0] if matc else None

def correct_ocr_misread(text):
    """Fix common OCR misinterpretations."""
    corrections = {
        "J": "1", "O": "0", "B": "8", "S": "5", "Z": "2", "G": "6", "T": "1",
        "I": "1", "L": "1", "D": "0", "€": "E", "=": "8", "E8": "P8", 
        "PB00E": "PB10E", "PBIOE": "PB10E", "8443": "8143",
        "P8H00": "PB100", "PP8100": "PB10", '"': "", "'": "", "P8100": "PB10E", "P814P3": "P8143"
    }
    for wrong, right in corrections.items():
        text = text.replace(wrong, right)

    # Ensure the corrected text matches a vehicle number pattern
    pattern = r'P[B8]\d{2}[A-Z]{1,2}\d{4}'  # Matches PB10DE8143 format
    match = re.search(pattern, text)
    
    return match.group(0) if match else text

def preprocess_image(image_path):
    """Enhance the image for better OCR recognition."""
    img = cv2.imread(image_path)
    if img is None:
        print(f"⚠️ Error: Could not read {image_path}")
        return None

    scale_percent = 300  # Resize to 300% of original
    width = int(img.shape[1] * scale_percent / 100)
    height = int(img.shape[0] * scale_percent / 100)
    resized_img = cv2.resize(img, (width, height), interpolation=cv2.INTER_CUBIC)

    lab = cv2.cvtColor(resized_img, cv2.COLOR_BGR2LAB)
    l, a, b = cv2.split(lab)
    clahe = cv2.createCLAHE(clipLimit=2.5, tileGridSize=(8,8))
    cl = clahe.apply(l)
    limg = cv2.merge((cl, a, b))
    enhanced_img = cv2.cvtColor(limg, cv2.COLOR_LAB2BGR)

    blurred_img = cv2.GaussianBlur(enhanced_img, (3,3), 0)
    kernel = np.array([[0, -1, 0], [-1, 5,-1], [0, -1, 0]])
    sharp_img = cv2.filter2D(blurred_img, -1, kernel)

    cv2.imwrite(image_path, sharp_img)
    print(f"✅ Enhanced and saved over: {image_path}")
    return image_path

def perform_ocr():
    """Process images for OCR after enhancement."""
    im_dir = ROOT_DIR + 'images/'
    reader = easyocr.Reader(['en'])
    fnames = os.listdir(im_dir)
    result_set = []

    for name in fnames:
        if name.startswith("crop_"):
            image_path = os.path.join(im_dir, name)
            preprocess_image(image_path)

    for name in fnames:
        if name.startswith("crop_"):
            image_path = os.path.join(im_dir, name)
            im = cv2.imread(image_path)
            result = reader.readtext(im, detail=0)
            try:
                if result:
                    raw_text = "".join(result).replace(" ", "").upper()
                    corrected_text = correct_ocr_misread(raw_text)
                    result_set.append([name, corrected_text])
                else:
                    result_set.append([name, "NO TEXT DETECTED"])
            except:
                result_set.append([name, "ERROR"])

    print(result_set)

    # ✅ Call `make_doc` from `document.py`
    make_doc(result_set)

    return result_set

def send_email(cont_path, mail_receiver):
    """Send an email with the generated document as an attachment."""
    mail_sender = os.getenv('EMAIL_SENDER')
    mail_password = os.getenv('EMAIL_PASSWORD')
    
    print("EMAIL_SENDER:", mail_sender if mail_sender else "❌ NOT SET")
    print("EMAIL_PASSWORD:", "*****" if mail_password else "❌ NOT SET")

    if not mail_sender or not mail_password:
        print("❌ EMAIL_SENDER and EMAIL_PASSWORD environment variables are missing!")
        return

    subject = 'Violation Detection'
    body = "A ticket has been issued for your violation of traffic rules."

    em = EmailMessage()
    em['From'] = mail_sender
    em['To'] = mail_receiver
    em['Subject'] = subject
    em.set_content(body)

    with open(cont_path, 'rb') as content_file:
        content = content_file.read()
        em.add_attachment(content, maintype='application', subtype='docx', filename='ticket.docx')

    try:
        context = ssl.create_default_context()
        with smtplib.SMTP_SSL('smtp.gmail.com', 465, context=context) as smtp:
            smtp.login(mail_sender, mail_password)
            smtp.send_message(em)
        print("✅ Email sent successfully!")
    except Exception as e:
        print(f"❌ Error sending email: {e}")
