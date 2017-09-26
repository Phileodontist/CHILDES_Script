import os
import nltk
import re
import csv
from nltk.corpus.reader import CHILDESCorpusReader

# List of paths of folders that contain xml files
file_folder = []

# Main()

print("Input Convention:------------------------------------------------------"
      "\n\t*Directory path: Type in the directory name where the files reside "
      "\n\t*File name: Type in the desired filename"
      "\n\t*Verb: Type in the desired verb under analysis"
      "\n\t*Speaker: Type in a speaker from the list: CHI, STU, etc"
      "\n----------------------------------------------------------------------"
      "-")

# Retrieves the directory pathway
directory = input("Enter directory path: ")
directory_path = nltk.data.find('corpora/CHILDES/' + directory)
file_name = input("Enter file to write to: ")

# Variables
num = 0                    # Used to iterate through list of corpra data
printFile = True           # Boolean used to print corpus info once
verb = input("Type in verb: ")
regex = ("[^\w]" + verb + "(-)?[^\w]")
speaker = input("Type in speaker: ").upper()

def xtract_XML_files(corpus_directory, extension = 'xml'):

    # Get a list of the files within the directory
    corpus_directory_files = os.listdir(corpus_directory)

    # Transverse through all the files
    for filename in corpus_directory_files:
        filepath = os.path.join(corpus_directory, filename)

        # Checks if filepath is a file, if not its a directory
        if os.path.isfile(filepath):
            # Checks if the files have the xml extension
            if not filepath.endswith(extension):
                continue
            # appends the paths of files that contain xml files to file_folder
            file_folder.append(filepath[:-(len(filename)) - 1])
            break
        elif os.path.isdir(filepath):
            # This is a directory, enter into it for further processing
            xtract_XML_files(filepath)
    return file_folder


# Iterates through the directory
xml_files = xtract_XML_files(directory_path)

# Creates a CSV file
with open(directory + '_' + file_name + '.csv', 'w') as csvfile:
    fieldnames = ['Corpus', 'File', 'Name', 'Verb', 'Age', 'Sent',
                  'Syntatic Object', 'Event or Object']
    writer = csv.DictWriter(csvfile, fieldnames=fieldnames)
    writer.writeheader()

    for xml_folder in xml_files:

        corpus_folder = CHILDESCorpusReader(xml_folder, '.*.xml')

        # Stores the data of the corpra
        corpus_data = corpus_folder.corpus(corpus_folder.fileids())

        # Prints out corpus & child information
        for file in corpus_folder.fileids():

            # Stores all the sentences spoken by the speaker
            corpus_sents = corpus_folder.sents(file, speaker=speaker)

            # Stores all the sentences, words in stem form
            corpus_sents_stems = corpus_folder.sents(file, speaker=speaker,
                                                stem=True)

            corpus_participant = corpus_folder.participants(file)

            # Searches through each sentence for a match
            for stem_sents, sents in zip(corpus_sents_stems, corpus_sents):
                # Convert to string
                sents = ' '.join(sents)
                stem_sents = ' '.join(stem_sents)
                if re.search(regex, stem_sents):
                    # Prints the header of the file if it contains a match
                    if printFile is True:
                        print("\nCorpus: ", corpus_data[num]["Corpus"])
                        print("File: ", file)
                        print("Path Directory: ", xml_folder)

                        child = corpus_participant[0][speaker]
                        print(speaker + ": ", [(k, child[k]) for k in
                                               sorted(child.keys())])
                        print(" ")
                        # Prints the header only once per file
                        printFile = False
                    # Prints the sentences that matches
                    print(sents)

                    writer.writerow({'Corpus': corpus_data[num]["Corpus"],
                                     'File': file,
                                     'Name': [child['name']],
                                     'Verb': verb,
                                     'Age': [child['age']],
                                     'Sent': sents})
            printFile = True

            num += 1
        num = 0  # Resets num after scanning each file
    csvfile.close()



