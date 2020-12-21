from docx import Document

def file2text(myFile):
    doc = Document(myFile)
    text = []
    for para in doc.paragraphs:
        text.append(para.text)
    return '<br>'.join(text)