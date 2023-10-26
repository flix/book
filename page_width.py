import os
import fileinput

PAGE_WIDTH_LIMIT = 100

# Read all files in current directory
DIRS = os.fwalk(os.curdir + os.sep + 'src')

# Filter out hidden directories
shown: list[tuple[str, list[str], list[str], int]] = []
for d in DIRS:
    dir_name, _ , _, _ = d
    if not dir_name.startswith('./.'):
        shown.append(d)

# Filter only markdown files
md_files: list[str] = []
for d in shown:
    dir_name, _, names, _ = d
    for name in names:
        if name.endswith('.md'):
            md_files.append(dir_name + '/' + name)

# Helper function that checks page width
def under_page_width_limit(line: str) -> bool:
    stripped = line.strip()
    return stripped.__len__() < PAGE_WIDTH_LIMIT

# Check page width for each line of each file
exit_status = 0
with fileinput.input(files = md_files, encoding = "utf-8") as f:
    for line in f:
        if not under_page_width_limit(line):
            exit_status = 1
            print("Page width exceeded in", f.filename(), "on line", f.filelineno(), os.linesep, '\t', line)

exit(exit_status)
