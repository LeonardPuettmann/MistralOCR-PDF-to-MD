PDF to Markdown Converter using Mistral OCR

This script converts all PDF files in a specified folder to Markdown files using OCR (Optical Character Recognition). The Markdown files are saved in a separate folder with the same name as the original PDF files.

You can install the required libraries using pip:

```pip install mistralai python-dotenv pymupdf pillow tqdm```

## Setup

    Create a `.env` file in the root directory of the project and add your Mistral API key:

```MISTRAL_API_KEY=your_api_key_here```

    Create a folder named pdf in the root directory of the project and place all the PDF files you want to convert into this folder.

## Usage

Run the script using Python:

```python convert.py```

The script will process all PDF files in the pdf folder and save the converted Markdown files in a folder named md.
Notes

    The script will skip any PDF files that already have corresponding Markdown files in the md folder.
    The script uses OCR to extract text from the PDF files, so the accuracy of the conversion depends on the quality of the PDF files.
