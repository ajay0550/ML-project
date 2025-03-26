import cv2
import pytesseract
import json
import os

# Set Tesseract OCR Path (Only needed for Windows users, adjust if needed)
pytesseract.pytesseract.tesseract_cmd = r"C:\Program Files\Tesseract-OCR\tesseract.exe"

def redact_pii(results):
    """Blurs or masks detected PII in images based on the detection results."""
    
    for item in results:
        img_path = item["file_path"]
        pii_texts = item["identifiers"] + item["emails"] + item["phone_numbers"] + item["addresses"]

        if os.path.exists(img_path):
            image = cv2.imread(img_path)
            gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)

            # Use OCR to detect text locations
            d = pytesseract.image_to_data(gray, output_type=pytesseract.Output.DICT)

            for i, word in enumerate(d["text"]):
                if word in pii_texts:
                    (x, y, w, h) = (d["left"][i], d["top"][i], d["width"][i], d["height"][i])
                    cv2.rectangle(image, (x, y), (x + w, y + h), (0, 0, 0), -1)  # Black-out text

            # Save redacted image
            new_path = img_path.replace(".jpg", "_redacted.jpg").replace(".png", "_redacted.png")
            cv2.imwrite(new_path, image)
            print(f"Redacted image saved: {new_path}")

if __name__ == "__main__":
    # Load detection results from output.json
    with open("output.json", "r") as f:
        results = json.load(f)
    redact_pii(results)
