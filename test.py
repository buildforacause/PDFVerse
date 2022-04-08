# import cv2
# import pytesseract
# import numpy as np
#
# def threshold_image(img_src):
#     """Grayscale image and apply Otsu's threshold"""
#     # Grayscale
#     img_gray = cv2.cvtColor(img_src, cv2.COLOR_BGR2GRAY)
#     # Binarisation and Otsu's threshold
#     _, img_thresh = cv2.threshold(
#         img_gray, 0, 255, cv2.THRESH_BINARY + cv2.THRESH_OTSU)
#
#     return img_thresh, img_gray
#
# def extract_all(img_src):
#     # Extract all text as one string
#     string_ocr = pytesseract.image_to_string(
#         img_thresh, lang='eng', config='--psm 6')
#     # Extract all text and meta data as dictionary
#     data_ocr = pytesseract.image_to_data(
#         img_src, lang='eng', config='--psm 6', output_type=Output.DICT)
#     # Copy source image to draw rectangles
#     img_result = img_src.copy()
#
#     # Iterate through all words
#     for i in range(len(data_ocr['text'])):
#         # Skip other levels than 5 (word)
#         if data_ocr['level'][i] != Levels.WORD:
#             continue
#         # Get bounding box position and size of word
#         (x, y, w, h) = (data_ocr['left'][i], data_ocr['top']
#                         [i], data_ocr['width'][i], data_ocr['height'][i])
#         # Draw rectangle for word bounding box
#         cv2.rectangle(img_result, (x, y), (x + w, y + h), (0,0,255), 2)
#
#     return img_result
#
# def mask_image(img_src, lower, upper):
#     """Convert image from RGB to HSV and create a mask for given lower and upper boundaries."""
#     # RGB to HSV color space conversion
#     img_hsv = cv2.cvtColor(img_src, cv2.COLOR_BGR2HSV)
#     hsv_lower = np.array(lower, np.uint8)  # Lower HSV value
#     hsv_upper = np.array(upper, np.uint8)  # Upper HSV value
#
#     # Color segmentation with lower and upper threshold ranges to obtain a binary image
#     img_mask = cv2.inRange(img_hsv, hsv_lower, hsv_upper)
#
#     return img_mask, img_hsv
#
# def denoise_image(img_src):
#     """Denoise image with a morphological transformation."""
#
#     # Morphological transformations to remove small noise
#     kernel = cv2.getStructuringElement(cv2.MORPH_RECT, (3, 3))
#     img_denoised = cv2.morphologyEx(
#         img_src, cv2.MORPH_OPEN, kernel, iterations=1)
#
#     return img_denoised
#
# def apply_mask(img_src, img_mask):
#     """Apply bitwise conjunction of source image and image mask."""
#
#     img_result = cv2.bitwise_and(img_src, img_src, mask=img_mask)
#
#     return img_result
# def draw_contour_boundings(img_src, img_mask, threshold_area=400):
#     """Draw contour bounding and contour bounding box"""
#     # Contour detection
#     contours, hierarchy, = cv2.findContours(
#         img_mask, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
#
#     # Create two copies of source image
#     img_contour = img_src.copy()
#     img_box = img_src.copy()
#
#     for idx, c in enumerate(contours):
#         # Skip small contours because its probably noise
#         if  cv2.contourArea(c) < threshold_area:
#             continue
#
#         # Draw contour in red
#         cv2.drawContours(img_contour, contours, idx, (0, 0, 255), 2, cv2.LINE_4, hierarchy)
#
#         # Get bounding box position and size of contour
#         x, y, w, h = cv2.boundingRect(c)
#         # Draw bounding box in blue
#         cv2.rectangle(img_box, (x, y), (x + w, y + h), (255, 0, 0), 2, cv2.LINE_AA, 0)
#
#     return img_contour, img_box
#
# def find_highlighted_words(img_mask, data_ocr, threshold_percentage=25):
#     """Find highlighted words by calculating how much of the words area contains white pixels compared to balack pixels."""
#
#     # Initiliaze new column for highlight indicator
#     data_ocr['highlighted'] = [False] * len(data_ocr['text'])
#
#     for i in range(len(data_ocr['text'])):
#         # Get bounding box position and size of word
#         (x, y, w, h) = (data_ocr['left'][i], data_ocr['top']
#                         [i], data_ocr['width'][i], data_ocr['height'][i])
#         # Calculate threshold number of pixels for the area of the bounding box
#         rect_threshold = (w * h * threshold_percentage) / 100
#         # Select region of interest from image mask
#         img_roi = img_mask[y:y+h, x:x+w]
#         # Count white pixels in ROI
#         count = cv2.countNonZero(img_roi)
#         # Set word as highlighted if its white pixels exceeds the threshold value
#         if count > rect_threshold:
#             data_ocr['highlighted'][i] = True
#
#     return data_ocr
#
# import fitz
#
# doc = fitz.open('output.pdf')
#
# page = doc.load_page
# highlights = ""
# for page in doc:
#      for annot in page.annots():
#         highlights += page.get_textbox(annot.rect)
# print(highlights)

from PIL import Image
from pytesseract import pytesseract

# Defining paths to tesseract.exe
# and the image we would be using
path_to_tesseract = r"C:/Program Files (x86)/Tesseract-OCR/tesseract.exe"

image_path = r"wordimage.png"

# Opening the image & storing it in an image object
img = Image.open(image_path)

# Providing the tesseract
# executable location to pytesseract library
pytesseract.tesseract_cmd = path_to_tesseract

# Passing the image object to
# image_to_string() function
# This function will
# extract the text from the image
text = pytesseract.image_to_string(img)

# Displaying the extracted text
print(text[:-1])
