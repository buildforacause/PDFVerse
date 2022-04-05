# from tkinter import *
# from tkinter import ttk
#
# root = Tk()
#
# # fill rest of root with a Text and put some text there
# BotInput = "This usually links to a database dictionary of responses."
#
#
# ###This is were the magic happens###
# # action-function for the Button: highlight all occurrences of string
# def find():
#     # get string to look for (if empty, no searching)
#     s = "Bottity Bottity Bot Bot:"
#     if s:
#         # start from the beginning (and when we come to the end, stop)
#         idx = '1.0'
#
#         while 1:
#             # find next occurrence, exit loop if no more
#             idx = text.search(s, idx, nocase=1, stopindex=END)
#             if not idx: break
#             # index right after the end of the occurrence
#
#             lastidx = '%s+%dc' % (idx, len(s))
#
#             # tag the whole occurrence (start included, stop excluded)
#             text.tag_add('found', idx, lastidx)
#             # prepare to search for next occurrence
#             idx = lastidx
#         # use a red foreground for all the tagged occurrences
#         text.tag_config('found', foreground='red')
#
#
# # This displays the entries from the Bot and the User in the text
# def display_entry(*args):
#     UserInput = Comment.get()
#     text.insert(END,
#                 'Bottity Bottity Bot Bot: ' + BotInput + '\n')
#     text.insert(END,
#                 'User: ' + UserInput + '\n')
#     Comment.delete(0, END)
#     # Runs the function
#     find()
#
#
# # Creat text wiget
# text = Text(root)
#
# text.pack()
#
# # Entry field to add content to text wiget.
# Comment_Lbl = ttk.Label(root, text="Comment here:")
# Comment_Lbl.pack()
#
# Comment = ttk.Entry(root)
# Comment.pack()
# Comment.bind("<Return>", display_entry)
# Comment.focus()
# Comment_Button = ttk.Button(root, text="Enter", command=lambda: display_entry(None))
#
# Comment_Button.pack()
#
# root.mainloop()



import tkinter
from tkinter import filedialog
from PyPDF2 import PdfFileReader, PdfFileWriter
from pdf2docx import parse
import subprocess
import tabula


window = tkinter.Tk()
window.minsize(width=626, height=352)
window.maxsize(width=626, height=352)
window.resizable(False, False)
sourceFile_word = ''
sourceLoc = ''
sourceFile_pdf = ''


def chooseFile_pdf():
    global sourceFile_pdf
    sourceFile_pdf = filedialog.askopenfilename(parent=window, initialdir="/", title='Please select a file',
                                                filetypes=[("Pdf files", ".pdf")])


def chooseFile_word():
    global sourceFile_word
    sourceFile_word = filedialog.askopenfilename(parent=window, initialdir="/", title='Please select a file',
                                                 filetypes=[("Word files", ".docx")])


def chooseFile_pptx():
    global sourceFile_pptx
    sourceFile_pptx = filedialog.askopenfilename(parent=window, initialdir="/", title='Please select a file',
                                                filetypes=[("Ppt files", ".pptx")])

# def chooseLoc():
#     global sourceLoc
#     sourceLoc = filedialog.askdirectory(parent=window, initialdir="/", title='Please select a location')


def encrypt():
    chooseFile_pdf()
    output_pdf = PdfFileWriter()
    file = PdfFileReader(sourceFile_pdf)
    num = file.numPages
    for i in range(num):
        page = file.getPage(i)
        output_pdf.addPage(page)
    password = "pass"
    output_pdf.encrypt(password)
    with open(sourceFile_pdf, "wb") as f:
        output_pdf.write(f)


def pdf_to_word():
    chooseFile_pdf()
    pdf_file = sourceFile_pdf
    docx_file = sourceFile_pdf[:-4] + "-converted-to-word.docx"
    parse(pdf_file, docx_file)


# def word_to_pdf():
#     chooseFile_word()
#     docx_file = sourceFile_word
#     pdf_file = sourceFile_word[:-5] + "-converted-to-pdf"
#     convert(docx_file, pdf_file)


def pdf_to_pptx():
    chooseFile_pdf()
    list_files = subprocess.run(["pdf2pptx", sourceFile_pdf])
    print("The files are converted successfully")


def pdf_to_csv():
    chooseFile_pdf()
    pdf_file = sourceFile_pdf
    tabula.convert_into(pdf_file, sourceFile_pdf[:-4] + "-converted-to-csv", output_format="csv", stream=True)


# image = tkinter.PhotoImage(file="wallpaper.png")
canvas = tkinter.Canvas(window, width=626, height=352, bg="#f7f5dd", highlightthickness=0)
# canvas.create_image(313, 176, image=image)
canvas.place(x=0, y=0, relwidth=1, relheight=1)
file_button = tkinter.Button(window, text="Pdf to word", width=15, height=2, command=pdf_to_word)
file_button.grid(row=0, column=0)
file_button2 = tkinter.Button(window, text="Pdf to ppt", width=15, height=2, command=pdf_to_pptx)
file_button2.grid(row=1, column=0)
file_button3 = tkinter.Button(window, text="Pdf to csv", width=15, height=2, command=pdf_to_csv)
file_button3.grid(row=2, column=0)

window.mainloop()
print(sourceFile_word)
