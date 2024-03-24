import os
from docx import Document

def convert_docx_to_txt(docx_file, txt_file):
    # Open the .docx file
    doc = Document(docx_file)

    # Extract text from paragraphs (using list-comprehension)
    text = [paragraph.text for paragraph in doc.paragraphs]

    # Write text to .txt file
    with open(txt_file, 'w', encoding='utf-8') as f:
        f.write('\n'.join(text))

def main():
    # Specify the directory containing .docx files
    data_folder = '../data'

    # Iterate over .docx files in the directory
    for filename in os.listdir(data_folder):
        if filename.endswith('.docx'):
            docx_file = os.path.join(data_folder, filename)
            txt_file = os.path.join(data_folder, filename.replace('.docx', '.txt'))
            convert_docx_to_txt(docx_file, txt_file)

if __name__ == "__main__":
    main()