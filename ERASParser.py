'''import regex, text extractor, and llm packages'''
import sys
import re
import pymupdf
import json
from google import genai

def parser(filename):
    '''extract text from pdf'''
    doc = pymupdf.open(filename)
    text = ""
    for page in doc:
        text += page.get_text()

    '''search for the section of the text from Postgraduate Training through Honors. This section will contain the table we are concerned with, so we will remove the rest of the document'''
    pattern = "Postgraduate\sTraining.*?[\s\S]+?Honors"
    clean_text = re.findall(pattern, text)
    clean_text = clean_text[0]

    '''search for training type'''
    pattern = "Training\sType[\s\S]+?([^\r\n]+)[\s\S]+?Specialty"
    training_type = re.findall(pattern, clean_text)

    '''search for specialty'''
    pattern = "Specialty[\s\S]+?([^\r\n]+)[\s\S]+?Institution"
    specialty = re.findall(pattern, clean_text)

    '''search for institution'''
    pattern = "Institution[\s\S]+?([^\r\n]+)[\s\S]+?Dates\sAttended"
    institution = re.findall(pattern, clean_text)
    
    '''search for dates attended'''
    pattern = "Dates\sAttended[\s\S]+?([^\r\n]+)[\s\S]+?Location"
    dates_attended = re.findall(pattern, clean_text)
    
    '''search for location'''
    pattern = "Location[\s\S]+?([^\r\n]+)[\s\S]+?Setting"
    location = re.findall(pattern, clean_text)
    
    '''search for setting'''
    pattern = "Setting[\s\S]+?([^\r\n]+)[\s\S]+?Program\sDirector"
    setting = re.findall(pattern, clean_text)
    
    '''search for program director'''
    pattern = "Program\sDirector[\s\S]+?([^\r\n]+)[\s\S]+?Supervisor"
    program_director = re.findall(pattern, clean_text)
    
    '''search for supervisor'''
    pattern = "Supervisor[\s\S]+?([^\r\n]+)[\s\S]+?Page\s1"
    supervisor = re.findall(pattern, clean_text)

    '''check to ensure results for each category and output to json. If no results for a particular section put in "None" instead'''
    with open("results.json", "w") as json_file:
        for i in range(max(len(training_type),len(specialty),len(institution),len(dates_attended),len(location),len(setting),len(program_director),len(supervisor))):
            postgraduate_training =  {}

            if len(training_type) > i:
                postgraduate_training["training_type"] = training_type[i]
            else:
                postgraduate_training["training_type"] = "None"

            if len(specialty) > i:
                postgraduate_training["specialty"] = specialty[i]
            else:
                postgraduate_training["specialty"] = "None"

            if len(institution) > i:
                postgraduate_training["institution"] = institution[i]
            else:
                postgraduate_training["institution"] = "None"

            if len(dates_attended) > i:
                postgraduate_training["dates_attended"] = dates_attended[i]
            else:
                postgraduate_training["dates_attended"] = "None"

            if len(location) > i:
                postgraduate_training["location"] = location[i]
            else:
                postgraduate_training["location"] = "None"

            if len(setting) > i:
                postgraduate_training["setting"] = setting[i]
            else:
                postgraduate_training["setting"] = "None"

            if len(program_director) > i:
                postgraduate_training["program_director"] = program_director[i]
            else:
                postgraduate_training["program_director"] = "None"

            if len(supervisor) > i:
                postgraduate_training["supervisor"] = supervisor[i]
            else:
                postgraduate_training["supervisor"] = "None"

            json.dump(postgraduate_training, json_file, indent=4)

        '''if there are no results for any section write all sections a none to json'''
        if max(len(training_type),len(specialty),len(institution),len(dates_attended),len(location),len(setting),len(program_director),len(supervisor)) == 0:
            postgraduate_training =  {}
            postgraduate_training["training_type"] = "None"
            postgraduate_training["specialty"] = "None"
            postgraduate_training["institution"] = "None"
            postgraduate_training["dates_attended"] = "None"
            postgraduate_training["location"] = "None"
            postgraduate_training["setting"] = "None"
            postgraduate_training["program_director"] = "None"
            postgraduate_training["supervisor"] = "None"
            json.dump(postgraduate_training, json_file, indent=4)

    '''AI backup parsing and bonus point assignment'''
    client = genai.Client(api_key='AIzaSyDq2iJkCM6VpUhC6qNml2fBpnP-CDLSut4')

    myfile = client.files.upload(file=filename)
    response = client.models.generate_content(
        model="gemini-2.5-flash",
        contents=[
            myfile,
            "Please extract the contents of the Postgraduate Training table into a JSON format. Additionally list a bonus point value for the candidate. The candidate earns 70 bonus points for 11 or more months of residency/fellowship, 80 point for aligning with the specialty of psychiatry, and 50 points for thier training_type containing either ACGME or AOA. Each category of bonus points can only be earned once per candidate.",
        ],
    )
    with open("AI Output.txt", "w") as text_file:
        print(response.text,file=text_file)

if __name__ == '__main__':
    parser(sys.argv[1])