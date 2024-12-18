import base64
from langchain_core.tools import tool


@tool
def extract_text_from_base64(base64_data, output_file_path=None):
    """create the document from base64 documents"""
    try:
        decoded_data = base64.b64decode(base64_data)
        output_file_path = "./docs/" + output_file_path
        try:
            decoded_text = decoded_data.decode('utf-16')
            if output_file_path:
                with open(output_file_path, 'w') as output_file:
                    output_file.write(decoded_text)
        except UnicodeDecodeError:
            if output_file_path:
                with open(output_file_path, 'wb') as output_file:
                    output_file.write(decoded_data)
    except (base64.binascii.Error, ValueError) as e:
        print(f"Error: Failed to decode Base64 content. Details: {e}")