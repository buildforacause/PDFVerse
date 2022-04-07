from tkinter import *
import fitz
from PyPDF2 import PdfFileReader


def addtonotes():
    notes = str(notereader.get("1.0", END))
    noteslist.append(notes)


def savenotes():
    doc = fitz.open(r"samplepdf.pdf")
    page = doc[0]
    for text in noteslist:
        text_instances = page.searchFor(text)
        ### HIGHLIGHT
        for inst in text_instances:
            print(inst, type(inst))
            highlight = page.addHighlightAnnot(inst)
    ### OUTPUT
    doc.save(r"output.pdf", garbage=4, deflate=True, clean=True)


noteslist = []
highlightroot = Tk()
highlightroot.title("Note Maker")
highlightroot.geometry('1000x300')
highlightroot.resizable(False, False)

input_pdf=PdfFileReader(open('samplepdf.pdf','rb'))
pdfpage=input_pdf.getPage(1)
print("")

pdfreader = Text(highlightroot, bg="black", fg="white", height=5, width=125)
pdfreader.grid(row=1,column=0,columnspan=3)
notereader = Text(highlightroot, height=2, width=100)
notereader.grid(row=3,column=0,columnspan=2)

addbutton=Button(highlightroot,command=addtonotes,text="Add to notes",width=27,height=2,relief="groove")
addbutton.grid(row=3,column=2)
savebutton=Button(highlightroot,command=savenotes,text="Save")
savebutton.grid(row=4,column=1)

pdflabel=Label(highlightroot,text="Pdf:")
pdflabel.grid(row=0,column=1)
notelabel=Label(highlightroot,text="Add your notes here from PDF:")
notelabel.grid(row=2,column=1)

highlightroot.mainloop()
