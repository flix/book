#!/usr/bin/env python3

import os
import glob
import tempfile
import subprocess
import shutil

SRC_DIR = "src"
_BUILD_DIR = tempfile.TemporaryDirectory("flix-test-snippets")
BUILD_DIR = _BUILD_DIR.name
SNIPPET_DIR = os.path.join(BUILD_DIR, "snippets")
os.mkdir(SNIPPET_DIR)
FLIX_PATH = os.path.abspath("flix.jar")

# returns all the code snippets in the given file as a tuple: (content, language, line)
# file_name is relative to the src directory
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

def getSubject(file):
    file_name = os.path.basename(file)
    subject = os.path.splitext(file_name)[0]
    return subject

# make snippets files for the given file_path
# file_name is relative to the src directory
def makeSnippetFilesForFile(file_name):
    for (block, language, linenum) in extract_code_snippets(file_name):
        if "flix" in language and "ignore" not in language:
            subject = getSubject(file_name)
            test_file = f"{subject}_{linenum}.flix"
            with open(os.path.join(SNIPPET_DIR, test_file), "w") as file:
                file.write(block)

# make snippets for all the source files and put them in the snippet directory
def makeSnippetFiles():
    files = glob.glob("*.md", root_dir=SRC_DIR)
    for file in files:
        makeSnippetFilesForFile(file)

def flix(cmd, *, cwd):
    return subprocess.run(f"java -jar {FLIX_PATH} {cmd}", cwd=cwd, shell=True)

# file_name is relative to the snippet directory
def checkFlixFile(file_name):
    # create a project for the file
    subject = getSubject(file_name)
    project_dir = os.path.join(BUILD_DIR, subject)
    os.mkdir(project_dir)
    flix("init", cwd=project_dir)

    # delete the Main.flix file
    main = os.path.join(project_dir, "src", "Main.flix")
    os.remove(main)

    # copy the flix file to the project
    source = os.path.join(SNIPPET_DIR, file_name)
    target = os.path.join(project_dir, "src", file_name)
    shutil.copy(source, target)

    # type-check the project
    return flix("check --no-install", cwd=project_dir)

def checkFlixFiles():
    files = glob.glob("*.flix", root_dir=SNIPPET_DIR)
    failures = []
    for file in files:
        result = checkFlixFile(file)
        if result.returncode != 0:
            failures.append(file)
    return failures

makeSnippetFiles()
failures = checkFlixFiles()

if failures != []:
    print(f"Errors in {len(failures)} snippet(s).")
    for failure in failures:
        print(failure)
    exit(1)
else:
    print("All snippets compiled successfully.")
    exit(0)