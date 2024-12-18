import os
import re
import yaml
import base64
import fitz
from docx import Document
from typing import Union, Optional
from box import ConfigBox
from box.exceptions import BoxTypeError


def read_yaml_file(path: Union[str, os.PathLike]) -> Union[str, ConfigBox]:
    """
    Read a YAML file and return its content as a ConfigBox.
    :param 
        - path: The path to the YAML file.
    :return:
        - The content of the YAML file wrapped in a ConfigBox.
        - Returns None if the file is empty or if an error occurs.
    """
    try:
        with open(path) as file:
            content = yaml.safe_load(file)
            return ConfigBox(content)
    except BoxTypeError:
        print("Configuration yaml file is empty")
    except Exception as e:
        print(e)


def read_text_file(path: Union[str, os.PathLike]) -> str:
    """
    Read a text file and return its content as a string format
    :param path: Text file path
    :return: content of the text file
    """
    with open(path, 'r') as file:
        message_content = file.read()

    return message_content


def extract_text_from_base64(
        base64_data: str, 
        output_file_path: str = None
    ) -> Optional[str]:
    """
    Extracts text from a Base64-encoded string and optionally saves it to a file.

    params:
        - base64_data (str): The Base64-encoded string that needs to be decoded.
        - output_file_path (Optional[str]): The file path where the decoded data should be saved.
      If not provided, the data is not saved to a file.

    return:
        The decoded text if decoding is successful, or `None` if an error occurs or the text 
       cannot be decoded as UTF-16.
    """
    try:
        decoded_data = base64.b64decode(base64_data)
        try:
            decoded_text = decoded_data.decode('utf-8')
            if output_file_path:
                with open(output_file_path, 'w') as output_file:
                    output_file.write(decoded_text)
            return decoded_text
        except UnicodeDecodeError:
            if output_file_path:
                with open(output_file_path, 'wb') as output_file:
                    output_file.write(decoded_data)
            return None
    except (base64.binascii.Error, ValueError) as e:
        print(f"Error: Failed to decode Base64 content. Details: {e}")

def read_pdf(file_path):
    try:
        doc = fitz.open(file_path)
        text = ""
        for page_num in range(len(doc)):
            page = doc.load_page(page_num)
            text += page.get_text()
        return text
    except Exception as e:
        return f"Error reading PDF: {e}"

def read_docx(file_path):
    try:
        doc = Document(file_path)
        text = ""
        for para in doc.paragraphs:
            text += para.text + "\n"
        return text
    except Exception as e:
        return f"Error reading DOCX: {e}"


def read_documents_in_folder():
    document_texts = {}
    for filename in os.listdir("./docs"):
        file_path = os.path.join("./docs", filename)
        if filename.endswith('.pdf'):
            document_texts[filename] = read_pdf(file_path)
        elif filename.endswith('.docx'):
            document_texts[filename] = read_docx(file_path)
    return document_texts