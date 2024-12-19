#!/usr/bin/env python3

import os
import glob
import tempfile
import subprocess

SRC_DIR = "src"
SNIPPET_DIR = tempfile.TemporaryDirectory()

# returns all the code snippets in the given file as a tuple: (content, language, line)
def extract_code_snippets(file_name):
    snippets = []

    with open(os.path.join(SRC_DIR, file_name), 'r', encoding='utf-8') as file:
        lines = file.readlines()

    in_code_block = False
    language = None
    block_start_line = None
    block_content = []

    for i, line in enumerate(lines):
        stripped_line = line.strip()

        if stripped_line.startswith("```"):
            if in_code_block:
                # End of a code block
                snippets.append(("".join(block_content), language, block_start_line))
                in_code_block = False
                block_content = []
                language = None
            else:
                # Start of a new code block
                in_code_block = True
                language = stripped_line[3:].strip()  # Extract language if specified
                block_start_line = i + 1  # 1-based line number
        elif in_code_block:
            block_content.append(line)

    return snippets

# make snippets files for the given file_path
def makeSnippetFilesForFile(file_name):
    for (block, language, linenum) in extract_code_snippets(file_name):
        if "flix" in language and "ignore" not in language:
            test_file = f"{file_name}_{linenum}.flix"
            with open(os.path.join(SNIPPET_DIR, test_file), "w") as file:
                file.write(block)

# make snippets for all the source files and put them in the snippet directory
def makeSnippetFilesForDir():
    files = glob.glob("*.md", root_dir=SRC_DIR)
    for file in files:
        makeSnippetFilesForFile(file)


makeSnippetFilesForDir("/tmp/matttest/")

def checkFlixFile(file):
    subprocess.run("java -jar flix.jar check")