# Transforms data set (.txt files) into WEKA compatible files (.arff files)
# Output files are written to same directory as data set and have same name as original file, but with .arff ext
import re
from os.path import join, abspath

# define data set
data = {
  'directory': 'data/',
  'files': [
    {'filename': 'webkb-train-stemmed.txt', 'relation': 'train'},
    {'filename': 'webkb-test-stemmed.txt', 'relation': 'test'}
  ]
}

print "\n\nConverting data set at {directory} to WEKA compatible .arff files".format(**data)


# move the 1st word (label) to the end of the string, separating from string with comma
def moveLabelToEnd(str):
  tmp = re.split(r'\s', str, maxsplit=1)
  tmp = map(lambda s: s.strip(), tmp)
  if len(tmp) == 2:
    return '"' + tmp[1] + '", ' + tmp[0]
  else:
    print '\bNad Document: ', tmp
    return '\n\nBAD STRING'

# Returns .arff file header
def getArffHeader(relation, labels):
  return "@relation " + relation + "\n" + \
    "\n@attribute Document string" + \
    "\n@attribute Class {" + ','.join(labels)  + "}\n" + \
    "\n@data\n\n"
  
  
# convert each file of data set to arff
# assumes data sets are contained in .txt files
labels = ['student', 'faculty', 'course', 'project']
for file in data['files']:
  # read file and strip extra whitespace
  fileString = open(data['directory'] + file['filename']).read().strip()
  # split by line - creates an array of documents
  fileDocuments = re.split(r'\n', fileString)
  # move the label from front of document to end of document, separated by comma
  fileDocuments = map(lambda f: moveLabelToEnd(f), fileDocuments)
  # write documents to output file in new format
  outputPath = abspath(data['directory'] + file['filename'].replace('.txt', '.arff'))
  arffOutput = open(outputPath, 'w+')
  arffOutput.write(getArffHeader(file['relation'], labels))
  arffOutput.write('\n'.join(fileDocuments))
  arffOutput.close()
  
print "\nData conversion complete\n"