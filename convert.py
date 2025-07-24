import base64
import os
from mistralai import Mistral
from dotenv import load_dotenv
import fitz  # PyMuPDF
from PIL import Image
import io
from tqdm import tqdm

def encode_image(image):
    """Encode the image to base64."""
    try:
        img_byte_arr = io.BytesIO()
        image.save(img_byte_arr, format='PNG')
        return base64.b64encode(img_byte_arr.getvalue()).decode('utf-8')
    except Exception as e:
        print(f"Error: {e}")
        return None

def save_md_response(page_content, output_path):
    """Save or append the page content to a Markdown file."""
    try:
        with open(output_path, 'a', encoding='utf-8') as md_file:
            md_file.write(page_content + "\n")
    except Exception as e:
        print(f"Error saving Markdown response: {e}")

def extract_text_from_pdf(pdf_path, md_path):
    """Extract text from PDF and save to Markdown."""
    load_dotenv(override=True)
    api_key = os.getenv("MISTRAL_API_KEY")
    if api_key is None:
        print("MISTRAL_API_KEY not found in the local .env file.")
        return

    client = Mistral(api_key=api_key)

    try:
        pdf_document = fitz.open(pdf_path)
        for page_number in tqdm(range(len(pdf_document)), desc="Processing Pages"):
            page = pdf_document.load_page(page_number)
            pix = page.get_pixmap()
            img = Image.frombytes("RGB", [pix.width, pix.height], pix.samples)
            base64_image = encode_image(img)
            if base64_image is None:
                continue

            ocr_response = client.ocr.process(
                model="mistral-ocr-latest",
                document={
                    "type": "image_url",
                    "image_url": f"data:image/png;base64,{base64_image}"
                },
                include_image_base64=True
            )

            for page in ocr_response.pages:
                save_md_response(page.markdown, md_path)

    except Exception as e:
        print(f"Error processing OCR: {e}")

    finally:
        pdf_document.close()

def process_pdf_files(pdf_folder, md_folder):
    """Process all PDF files in the pdf_folder and save them as Markdown files in the md_folder."""
    os.makedirs(md_folder, exist_ok=True)

    pdf_files = [filename for filename in os.listdir(pdf_folder) if filename.endswith(".pdf")]
    with tqdm(total=len(pdf_files), desc="Processing PDF Files") as pbar:
        for filename in pdf_files:
            pdf_path = os.path.join(pdf_folder, filename)
            md_filename = os.path.splitext(filename)[0] + ".md"
            md_path = os.path.join(md_folder, md_filename)

            if not os.path.exists(md_path):
                print(f"Processing {filename}...")
                extract_text_from_pdf(pdf_path, md_path)
            else:
                print(f"Skipping {filename}, Markdown file already exists.")

            pbar.update(1)

if __name__ == "__main__":
    pdf_folder = "pdf"
    md_folder = "md"
    process_pdf_files(pdf_folder, md_folder)
