import PyPDF2, os

# Get all the PDF filenames.
pdfFiles = []

root_dir = 'C:\Users\Dalei\Dropbox\Courses\Information Retrieval\Slides'

for filename in os.listdir(root_dir):
    if filename.endswith('.pdf'):
        pdfFiles.append(root_dir + '\\' + filename)

pdfFiles.sort(key=str.lower)
 
pdfWriter = PyPDF2.PdfFileWriter()
for filename in pdfFiles:
    pdfReader = PyPDF2.PdfFileReader(open(filename, 'rb'))
    for pageNum in range(0, pdfReader.numPages):
        pageObj = pdfReader.getPage(pageNum)
        pdfWriter.addPage(pageObj)
 
pdfOutput = open('allminutes.pdf', 'wb')
pdfWriter.write(pdfOutput)
pdfOutput.close()