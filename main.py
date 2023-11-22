from google.oauth2 import service_account
from google.cloud import vision
from google.cloud.vision_v1 import types
import argparse
import cv2 as cv
import io
import os
from collections import namedtuple
from PIL import Image, ImageDraw, ImageFont


os.environ["GOOGLE_APPLICATION_CREDENTIALS"] = "document-classifier-404406-bc4b6ee5348e.json"
client = vision.ImageAnnotatorClient()


def extract_text(image_paths):
    result = []
    for image_path in image_paths:
        if image_path.startswith(("http", "https")):
            image = vision.Image()
            image.source.image_uri = image_path
        else:
            with open(image_path, "rb") as image_file:
                content = image_file.read()
            image = vision.Image(content=content)

        response = client.text_detection(image=image)
        text_annotations = response.text_annotations
        extracted_text = text_annotations[0].description if text_annotations else "No text found in the image."

        result.append(extracted_text.split())
    return result

def classify_aadhar(aadhar_data):
    eadhar_text_list = ['सत्यमेव', 'जयते', 'भारत', 'सरकार', 'भारतीय', 'विशिष्ट', 'पहचान', 'प्राधिकरण', 'Unique', 'Identification', 'Authority', 'of', 'India', 'नामांकन', 'क्रमांक/Enrolment', 'No.:', 'XXXX/XXXXX/XXXXX', 'Government', 'of', 'India', 'आपका', 'आधार', 'क्रमांक', '/', 'Your', 'Aadhaar', 'No.:', 'मेरा', 'आधार,', 'मेरी', 'पहचान', 'आधार', 'Government', 'of', 'India', 'अनिकेत', 'वर्मा', 'Aniket', 'Verma', 'जन्म', 'तिथि', '/', 'DOB:', '11/03/2000', 'पुरुष', '/', 'MALE', 'मेरा', 'आधार,', 'मेरी', 'पहचान', 'Issue', 'Date:', '03/10/2014', 'सत्यमेव', 'जयते', 'Government', 'of', 'India.', 'सूचना', 'आधार', 'पहचान', 'का', 'प्रमाण', 'है,', 'नागरिकता', 'का', 'नहीं।', 'सुरक्षित', 'QR', 'कोड', '/', 'ऑफलाइन', 'XML', '/', 'ऑनलाइन', 'ऑथेंटिकेशन', 'से', 'पहचान', 'प्रमाणित', 'करें।', 'यह', 'एक', 'इलेक्ट्रॉनिक', 'प्रक्रिया', 'द्वारा', 'बना', 'हुआ', 'पत्र', 'है।', 'INFORMATION', 'Aadhaar', 'is', 'a', 'proof', 'of', 'identity,', 'not', 'of', 'citizenship.', 'Verify', 'identity', 'using', 'Secure', 'QR', 'Code/', 'Offline', 'XML/', 'Online', 'Authentication.', 'This', 'is', 'electronically', 'generated', 'letter.', 'AADHAAR', 'आधार', 'देश', 'भर', 'में', 'मान्य', 'है।', 'आधार', 'कई', 'सरकारी', 'और', 'गैर', 'सरकारी', 'सेवाओं', 'को', 'पाना', 'आसान', 'बनाता', 'है।', 'आधार', 'में', 'मोबाइल', 'नंबर', 'और', 'ईमेल', 'ID', 'अपडेट', 'रखें।', 'आधार', 'को', 'अपने', 'स्मार्ट', 'फोन', 'पर', 'रखें,', 'mAadhaar', 'App', 'के', 'साथ।', 'Aadhaar', 'is', 'valid', 'throughout', 'the', 'country.', 'Aadhaar', 'helps', 'you', 'avail', 'various', 'Government', 'and', 'non-Government', 'services', 'easily.', 'Keep', 'your', 'mobile', 'number', '&', 'email', 'ID', 'updated', 'in', 'Aadhaar.', 'Carry', 'Aadhaar', 'in', 'your', 'smart', 'phone', '-', 'use', 'mAadhaar', 'App.', 'भारतीय', 'विशिष्ट', 'पहचान', 'प्राधिकरण', 'Unique', 'Identification', 'Authority', 'of', 'India', '।', '~', 'help@uidai.gov.in', '|', 'www.uidai.gov.in']    
    verify_list_front = ['Issue', 'Date:', 'सत्यमेव', 'जयते', 'भारत', 'सरकार', 'Government', 'of', 'India', 'मेरा', 'आधार', 'मेरी', 'पहचान', 'आधार']
    verify_list_back = ['Print', 'Date:', 'भारतीय', 'विशिष्ट', 'पहचान', 'प्राधिकरण', 'Unique', 'Identification', 'Authority','of', 'India', 'Address:', 'C/O:', '1947', 'help@uidai.gov.in', 'AADHAAR', 'www.uidai.gov.in']

    if len(aadhar_data) == 1:
        # Assume it's an e-Aadhar
        words = ' '.join(aadhar_data[0]).split()
        is_e_aadhar_card = all(word_or_sentence in words for word_or_sentence in eadhar_text_list)
        return "Valid E-Aadhar" if is_e_aadhar_card else "Invalid E-Aadhar"

    # Assume it's two sides of a physical Aadhar card
    
    # Convert the front and back sides into a list of words
    
    front_words = ' '.join(aadhar_data[0]).split()
    
    back_words = ' '.join(aadhar_data[1]).split()

    # Check if any word or sentence from the verify list matches the front side
    front_classification = "Valid Front Side" if all(word_or_sentence in front_words for word_or_sentence in verify_list_front) else "Invalid Front Side" 

    # Check if any word or sentence from the verify list matches the back side
    back_classification = "Valid Back Side" if all(word_or_sentence in back_words for word_or_sentence in verify_list_back) else "Invalid Back Side" 

    # Return both classifications
    return front_classification, back_classification
