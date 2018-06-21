# @TODO:    headings / subheadings --> sections / subsections
#           convert lists
#                ordered
#                unordered
#           convert simple formatting
#               newline
#               italic
#               bold
#           ? links
#           escape characters

import sys

# symbols = '#', '-', '+', '*'

# IN_LIST = False
ITEM_WARNING = False

def header(line):
    # @TODO: add subheader logic

    # remve leading hash marks
    while line[0] == '#':
        line = line[1:]

    # remove trailing hash marks
    end = len(line)-1
    while line[end] == '#':
        line = line[:end]
        end-=1
    line = line.strip()

    # do LaTeX to it
    line = '\section{' + line + '}'
    return line

# turn line into list item
def listify(sub_line):
    sub_line = '\item ' + sub_line
    global ITEM_WARNING
    ITEM_WARNING = True
    return sub_line


def begin_line(line):
    char = '@'  # placeholder
    if len(line) > 1:
        line = end_line(line)
        char = line[0]
    if char == '#':
        line = header(line)

    elif char == '-' or char == '+' or char == '*':
        # check for unordered list
        if line[1] == ' ':
            # @TODO: make sure it isn't emphasis
            # line = '\item ' + line[2:]
            # global ITEM_WARNING
            # ITEM_WARNING = True
            line = listify(line[2:])

    elif char.isdigit():
        if line[1] == '.' and line[2] == ' ':
            line = listify(line[3:])

    line = process(line)

    return line


def emphasis(line, i):
    # @TODO: handle bold
    #        handle nested bold / italic by calling process()
    h = i
    emchar = line[i]
    i += 1
    while line[i] != emchar:
        if i >= len(line):
            return line, -1
        i += 1
    # ???? = process(line[h+1:i])
    # add the LaTeX stuff
    before = line[:h-1]
    inner = line[h+1:i-1]
    after = line [i+1:]
    print("be: '" + before + "'")
    print("in: '" + inner + "'")
    print("af: '" + after + "'")
    i = len(line) - len(after)
    line = before + '\\textit{' + inner + '}' + after
    return line, i


def process(line):
    i = 0
    for x in line:
        char = line[i]
        if char == '*' or char == '_':
            line, i = emphasis(line, i)
            if i == -1:
                break
        i += 1
    return line

# check for Markdown linebreak
def end_line(line):
    size = len(line)
    if line[size-1] == ' ' and line[size-2] == ' ':
        line[size-1] = '\\'
        line[size-2] = '\\'
    return line


# -----------------------------------
# check number of arguments
if len(sys.argv) != 3:
    print('error: incorrect number of arguments\nusage: python3 md2ltx.py infile.md outfile.tex')
    exit()

in_name = sys.argv[1]
infile = open(in_name, 'r')
in_read = infile.read()
infile.close()

markdown = in_read.splitlines()
latex = ''

for line in markdown:
    latex = latex + begin_line(line) + '\n'
    # latex = latex + process(line)

print(latex)

# @TODO: display warning when write file already exists
out_name = sys.argv[2]
outfile = open(out_name, 'w')
outfile.write(latex)
outfile.close()



if ITEM_WARNING:
    print('warning: list items created; begin and end "itemize" or "enumerate" accordingly')

# s = '#thing#'
# for ch in s:
#     if ch == '#':
#         print('okay')
