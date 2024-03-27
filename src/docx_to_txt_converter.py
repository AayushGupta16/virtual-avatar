import os
from docx import Document


def convert_docx_to_txt(docx_file, txt_file):
    # Open the .docx file
    doc = Document(docx_file)

    # Extract text from paragraphs (using list-comprehension)
    text = [paragraph.text for paragraph in doc.paragraphs]

    # Construct the full path for the output .txt file
    # output_path = os.path.join(output_folder, txt_file)

    # Write text to .txt file
    with open(txt_file, "w", encoding="utf-8") as f:
        f.write("\n".join(text))


def main():
    # Specify the directory containing .docx files
    docx_folder = "../data/docx"
    # txt_folder = "../data/txt"

    # Iterate over .docx files in the directory
    for filename in os.listdir(docx_folder):
        if filename.endswith(".docx"):
            docx_file = os.path.join(docx_folder, filename)
            txt_file = os.path.join(docx_folder, filename.replace(".docx", ".txt"))
            convert_docx_to_txt(docx_file, txt_file)


if __name__ == "__main__":
    main()
