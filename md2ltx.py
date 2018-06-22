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

    line = process(line, 0)

    return line


# insert LaTeX italic code
# given line and start & end points
def emphasis(line, i, j):
    return line[:i] + '\\textit{' + line[i+1:j] + '}' + line[j+1:]


# find the location of the next emphasis character
# given a string and starting position
# return -1 if no more emphasis characters
def next_emph_char(line, pos):
    i = pos
    while i < len(line):
        if line[i] == '*':
            return i
        i += 1
    return -1

def process(line, pos):
    i = next_emph_char(line, pos)

    if i == -1:
        return line
    else: # emphasis char detected
        j = next_emph_char(line, i+1)
        if j == -1:
            return line
        else:
            update = emphasis(line, i, j)
            j += 7 # to account for "\textit"
            if j < len(update):
                return process(update, j)
            else:
                return update


    # i = 0
    # update = ''
    # for x in line:
    #     char = x
    #     if char == '*' or char == '_':
    #         h = i
    #         emchar = x
    #         i += 1
    #         while line[i] != emchar:
    #             if i >= len(line):
    #                 i = -1
    #                 break
    #             i += 1
    #         # line, i = emphasis(line, i)
    #         if i == -1:
    #             break
    #
    #         emphasized = line[h+1:i-1]
    #         update = line[:h-1] + emphasized + line[i+1:]
    #     i += 1
    # return update

# check for Markdown linebreak
def end_line(line):
    line_list = list(line)
    size = len(line_list)
    # print(line_list)
    if line_list[size-1] == ' ' and line_list[size-2] == ' ':
        # print('!!!!!!!!!!!!!!!!')
        line_list[size-1] = '\\'
        line_list[size-2] = '\\'
    update = ''.join(line_list)
    return update


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
