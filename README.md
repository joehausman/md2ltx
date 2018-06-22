# md2ltx
A tool that converts a Markdown file into an incomplete LaTeX file. By "incompete" I mean that additional code will need to be added to make a valid LaTeX file.

## usage
python3 md2ltx.py infile.md outfile.tex

## supported conversions
Markdown h1 --> LaTeX section
Markdown list item --> LaTeX list item
Markdown emphasis --> LaTeX italics
Markdown newline --> LaTeX newline
