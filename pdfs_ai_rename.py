import os
import tiktoken
from PyPDF2 import PdfReader
from groq import Groq
import re
import sys
import time

#client = OpenAI()
client = Groq(api_key=os.environ.get("GROQ_API_KEY"),)

max_length = 15000

def get_new_filename_from_groq(pdf_content):
    chat_completion = client.chat.completions.create(
        messages=[
            {"role": "system", "content": "You are a helpful assistant designed to extract filenames based on descriptions. Steps: 1.read the description, it's extracted by program, which may include mistake. 2.Reply with a short filename that is clear and easy to understand, which consists only of English characters and numbers only, if chinese included, automatically translate first. the name is no longer than 5 keywords, contact the keywords with `_`. e.g.:A_Prompt_engineering_cheatsheet \njust reply the final name as plain text, no code block. Rules:- Get the point, DO NOT chat. - Think step by step."},
            {"role": "user", "content": pdf_content}
        ],
        model="mixtral-8x7b-32768",
        temperature = 0.9, top_p = 0.9, max_tokens=1024, stop=None, stream=False
    )
    initial_filename = chat_completion.choices[0].message.content
    filename = validate_and_trim_filename(initial_filename)
    return filename

def validate_and_trim_filename(initial_filename):
    allowed_chars = r'[a-zA-Z0-9_]'
    
    if not initial_filename:
        timestamp = time.strftime('%Y%m%d%H%M%S', time.gmtime())
        return f'empty_file_{timestamp}'
    
    if re.match("^[A-Za-z0-9_]$", initial_filename):
        return initial_filename if len(initial_filename) <= 35 else initial_filename[:35]
    else:
        cleaned_filename = re.sub("^[A-Za-z0-9_]$", '', initial_filename)
        return cleaned_filename if len(cleaned_filename) <= 35 else cleaned_filename[:35]   

def rename_pdfs_in_directory(directory):
    pdf_contents = []
    files = [f for f in os.listdir(directory) if os.path.isfile(os.path.join(directory, f))]
    files.sort(key=lambda x: os.path.getmtime(os.path.join(directory, x)), reverse=True)
    for filename in files:
        if filename.endswith(".pdf"):
            filepath = os.path.join(directory, filename)
            print(f"Reading file {filepath}")
            pdf_content = pdfs_to_text_string(filepath)
            new_file_name = get_new_filename_from_groq(pdf_content)
            if new_file_name in [f for f in os.listdir(directory) if f.endswith(".pdf")]:
                print(f"The new filename '{new_file_name}' already exists.")
                new_file_name += "_01"

            new_filepath = os.path.join(directory, new_file_name + ".pdf")
            try:
                os.rename(filepath, new_filepath)
                print(f"File renamed to {new_filepath}")
            except Exception as e:
                print(f"An error occurred while renaming the file: {e}")

def pdfs_to_text_string(filepath):
    with open(filepath, 'rb') as file:
        reader = PdfReader(file)
        content = reader.pages[0].extract_text()
        if not content.strip():
            content = "Content is empty or contains only whitespace."
        encoding = tiktoken.get_encoding("cl100k_base")
        num_tokens = len(encoding.encode(content))
        if num_tokens > max_length:
            content = content_token_cut(content, num_tokens, max_length)
        return content
        print (content) 

def content_token_cut(content, num_tokens, max_length):
    content_length = len(content)
    while num_tokens > max_length:
        ratio = num_tokens / max_length
        new_length = int(content_length * num_tokens * (90 / 100))
        content = content[:new_length]
        num_tokens = len(tiktoken.get_encoding("cl100k_base").encode(content))
    return content

def main():
    #directory = ''  # Replace with your PDF directory path
    directory = sys.argv[1]  # 文件路径
    if directory == '':
      directory = input("Please input your path:")
    rename_pdfs_in_directory(directory)

if __name__ == "__main__":
    main()
