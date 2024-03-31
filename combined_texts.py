import os
from reportlab.lib.pagesizes import A4
from reportlab.platypus import SimpleDocTemplate, Paragraph, Spacer
from reportlab.lib.styles import getSampleStyleSheet
from reportlab.pdfbase.ttfonts import TTFont
from reportlab.pdfbase import pdfmetrics

# pip install fpdf2
# pip install reportlab

# the reportlab library for this task because of its robust support for different languages and character sets, including Turkish.

def txt_files_to_pdf(folder_path, output_pdf_path):
    # Register a Unicode-compatible font
    pdfmetrics.registerFont(TTFont('NotoSans', 'NotoSans-Regular.ttf'))

    # Create a SimpleDocTemplate object with A4 page size
    doc = SimpleDocTemplate(output_pdf_path, pagesize=A4)
    
    # Get the default styles and customize for our text
    styles = getSampleStyleSheet()
    style = styles['Normal']
    style.fontName = 'NotoSans'
    style.fontSize = 12
    style.leading = 14  # Line spacing. Adjust as needed.
    
    # List to hold elements to add to the document
    elements = []
    
    for filename in sorted(os.listdir(folder_path)):
        if filename.endswith('.txt'):
            file_path = os.path.join(folder_path, filename)
            with open(file_path, 'r', encoding='utf-8') as f:
                # Split the text into paragraphs by blank lines
                paragraphs = f.read().split('\n\n')
                for paragraph in paragraphs:
                    # Remove any leading/trailing whitespace and replace multiple newlines with a single newline
                    cleaned_paragraph = paragraph.strip().replace('\n', '<br/>')
                    # Add the paragraph to the document
                    elements.append(Paragraph(cleaned_paragraph, style))
                    # Add a spacer after each paragraph for better separation, adjust the height as needed
                    elements.append(Spacer(1, 12))
    
    # Build the PDF document with the elements list
    doc.build(elements)

# Define the directory path where your .txt files are located
directory_path = './FAQ_Data/'
# Replace 'your_folder_path' with the path to your folder containing .txt files
# Specify the path and name for the output PDF file
txt_files_to_pdf(directory_path, 'Vodafone_FAQ_Data_combined_texts.pdf')
