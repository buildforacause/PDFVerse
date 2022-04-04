import os
from tkinter import *
from tkinter.filedialog import askopenfilename
from tkinter.messagebox import showinfo
from tkinter.ttk import *
import tkinter
from tkinter import filedialog
from PyPDF2 import PdfFileReader, PdfFileWriter
import fitz
from fpdf import FPDF


window = tkinter.Tk()
window.minsize(width=626, height=352)
window.maxsize(width=626, height=352)
window.resizable(False, False)
sourceFile = ''


class Notepad:
    __root = Tk()
    __thisWidth = 300
    __thisHeight = 300
    thisTextArea = Text(__root)
    __thisMenuBar = Menu(__root)
    __thisFileMenu = Menu(__thisMenuBar, tearoff=0)
    __thisEditMenu = Menu(__thisMenuBar, tearoff=0)
    __thisHelpMenu = Menu(__thisMenuBar, tearoff=0)
    __thisScrollBar = Scrollbar(thisTextArea)
    __file = None

    def __init__(self, **kwargs):
        try:
            self.__root.wm_iconbitmap("Notepad.ico")
        except:
            pass
        try:
            self.__thisWidth = kwargs['width']
        except KeyError:
            pass
        try:
            self.__thisHeight = kwargs['height']
        except KeyError:
            pass
        self.__root.title("Untitled - Notepad")
        screenWidth = self.__root.winfo_screenwidth()
        screenHeight = self.__root.winfo_screenheight()
        left = (screenWidth / 2) - (self.__thisWidth / 2)
        top = (screenHeight / 2) - (self.__thisHeight / 2)
        self.__root.geometry('%dx%d+%d+%d' % (self.__thisWidth + 300,
                                              self.__thisHeight + 300,
                                              left, top))
        self.__root.grid_rowconfigure(0, weight=1)
        self.__root.grid_columnconfigure(0, weight=1)
        self.thisTextArea.grid(sticky=N + E + S + W)
        self.__thisFileMenu.add_command(label="New",
                                        command=self.__newFile)
        self.__thisFileMenu.add_command(label="Open",
                                        command=self.__openFile)
        self.__thisFileMenu.add_command(label="Save",
                                        command=self.__saveFile)
        self.__thisFileMenu.add_separator()
        self.__thisFileMenu.add_command(label="Exit",
                                        command=self.__quitApplication)
        self.__thisMenuBar.add_cascade(label="File",
                                       menu=self.__thisFileMenu)
        self.__thisEditMenu.add_command(label="Cut",
                                        command=self.__cut)
        self.__thisEditMenu.add_command(label="Copy",
                                        command=self.__copy)
        self.__thisEditMenu.add_command(label="Paste",
                                        command=self.__paste)
        self.__thisMenuBar.add_cascade(label="Edit",
                                       menu=self.__thisEditMenu)
        self.__thisHelpMenu.add_command(label="About Notepad",
                                        command=self.__showAbout)
        self.__thisMenuBar.add_cascade(label="Help",
                                       menu=self.__thisHelpMenu)
        self.__root.config(menu=self.__thisMenuBar)
        self.__thisScrollBar.pack(side=RIGHT, fill=Y)
        self.__thisScrollBar.config(command=self.thisTextArea.yview)
        self.thisTextArea.config(yscrollcommand=self.__thisScrollBar.set)

    def __quitApplication(self):
        self.__root.destroy()

    def __showAbout(self):
        showinfo("Notepad", "PDFverse")

    def __openFile(self):
        self.__file = askopenfilename(defaultextension=".txt",
                                      filetypes=[("All Files", "*.*"),
                                                 ("Text Documents", "*.txt")])

        if self.__file == "":
            self.__file = None
        else:
            self.__root.title(os.path.basename(self.__file) + " - Notepad")
            self.thisTextArea.delete(1.0, END)
            file = open(self.__file, "r")
            self.thisTextArea.insert(1.0, file.read())
            file.close()

    def __newFile(self):
        self.__root.title("Untitled - Notepad")
        self.__file = None
        self.thisTextArea.delete(1.0, END)

    def __saveFile(self):
        text = self.thisTextArea.get(1.0, END)
        with open("sample.txt", "w") as file:
            file.writelines(text)
        pdf = FPDF()
        pdf.add_page()
        pdf.set_font("Arial", size=15)
        file = open("sample.txt", "r")
        for x in file:
            pdf.cell(200, 10, txt=x[:-1], ln=1, align='L')
        file.close()
        pdf.output(sourceFile)

    def __cut(self):
        self.thisTextArea.event_generate("<<Cut>>")

    def __copy(self):
        self.thisTextArea.event_generate("<<Copy>>")

    def __paste(self):
        self.thisTextArea.event_generate("<<Paste>>")

    def run(self):
        self.__root.mainloop()


def toText():
    chooseFile()
    with fitz.open(sourceFile) as doc:
        text = ""
        for page in doc:
            text += page.get_text()
    notepad = Notepad(width=600, height=400)
    Notepad.thisTextArea.insert(1.0, text)
    notepad.run()


def chooseFile():
    global sourceFile
    sourceFile = filedialog.askopenfilename(parent=window, initialdir="/", title='Please select a file',
                                            filetypes=[("Pdf files", ".pdf")])


def encrypt():
    chooseFile()
    output_pdf = PdfFileWriter()
    file = PdfFileReader(sourceFile)
    num = file.numPages
    for i in range(num):
        page = file.getPage(i)
        output_pdf.addPage(page)
    password = "pass"
    output_pdf.encrypt(password)
    with open(sourceFile, "wb") as f:
        output_pdf.write(f)


def decrypt():
    chooseFile()
    out = PdfFileWriter()
    file = PdfFileReader(sourceFile)
    password = "pass"
    if file.isEncrypted:
        file.decrypt(password)
        for idx in range(file.numPages):
            page = file.getPage(idx)
            out.addPage(page)
        with open(sourceFile, "wb") as f:
            out.write(f)
        print("File decrypted Successfully.")
    else:
        print("File already decrypted.")


image = tkinter.PhotoImage(file="wallpaper.png")
canvas = tkinter.Canvas(window, width=626, height=352, bg="#f7f5dd", highlightthickness=0)
canvas.create_image(313, 176, image=image)
canvas.place(x=0, y=0, relwidth=1, relheight=1)
file_button = tkinter.Button(window, text="Encrypt", width=15, height=2, command=encrypt)
file_button.place(x=50, y=50)
file_button1 = tkinter.Button(window, text="Decrypt", width=15, height=2, command=decrypt)
file_button1.place(x=170, y=50)
file_button2 = tkinter.Button(window, text="To Text", width=15, height=2, command=toText)
file_button2.place(x=280, y=150)

window.mainloop()
