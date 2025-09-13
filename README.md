# ERAS-Parsing
Regex design:
  
My regex is fairly simple we first find the upper and lower limits of the section of text we are concerned with. We then limit the scope of the text to just that section by removing all other sections. Next for each section on the table we check for the heading of that   section and the heading of the next section and grab all of the text between those two. We repeat this for each section and on the final section we use the first text that appears after the table to be our lower limit. I chose to use these limits to account for when any section might have no text so that the regex doesn't grab the next section heading as a data value. 

Limitations and assumptions:

One of the limitations of my regex is that the text for the section headings must be exactly as it appears on the sample pdfs. I am assuming that the form is standardized, so this shouldn't be an issue. I am also assuming that the applicant has correctly filled out the form and the content for each section does correspond to that section. For my AI scoring I am using psychiatry as the prefered speciality since I didn't see one specified. I am also assuming that the bonus points can only be earned once per category.

AI Model:

I used google's gemini-2.5-flash as my model

Usage Instructions:

To run my program you will need to install all external libraries (listed below), place the pdf to be parsed in the same directory as the program, and provide the file name as a string command line argument when executing the program.

External libraries:

python built-in libraries:
sys
re
json

other libraries: 
pymupdf
google-genai

Example Input and Output:

If the desired input is a pdf titled "1 PG no header (1).pdf" you would input the following on the command line:
python .\ERASParser.py "1 PG no header (1).pdf"
The program will output two files:
results.json (json output of my parsing)
AI Output.txt (json output of the AI backup with the AI scoring)
