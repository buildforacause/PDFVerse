import os
from pygame import mixer
from tkinter import *
from tkinter.filedialog import askopenfilename
from tkinter.messagebox import showinfo, askquestion
from tkinter.ttk import *
import tkinter
from tkinter import filedialog
from PyPDF2 import PdfFileReader, PdfFileWriter
import fitz
from fpdf import FPDF
from pdf2docx import parse
import pdf2pptx
import subprocess
import pyttsx3


window = tkinter.Tk()
window.title("PDFVerse")
window.minsize(width=626, height=352)
window.maxsize(width=626, height=352)
window.resizable(False, False)
sourceFile = ''


class MP:
    def __init__(self, win):
        self.win = win
        # Create Tkinter window
        win.geometry('400x400')
        win.title('Music Player')
        win.resizable(0, 0)

        # StringVar to change button text later
        self.play_restart = tkinter.StringVar()
        self.pause_resume = tkinter.StringVar()
        self.play_restart.set('Play')
        self.pause_resume.set('Pause')

        load_button = Button(win, text='Upload', width=10, command=play_pdf)
        load_button.place(x=100, y=60, anchor='center')

        play_button = Button(win, textvariable=self.play_restart, width=10, command=self.play)
        play_button.place(x=100, y=180, anchor='center')

        pause_button = Button(win, textvariable=self.pause_resume, width=10, command=self.pause)
        pause_button.place(x=100, y=240, anchor='center')

        stop_button = Button(win, text='Stop', width=10, command=self.stop)
        stop_button.place(x=100, y=300, anchor='center')

        close_button = Button(win, text='Close', width=10, command=self.close)
        close_button.place(x=100, y=360, anchor='center')

        self.music_file = False
        self.playing_state = False

    def play(self):
        self.music_file = "string.wav"
        self.play_restart.set('Play')
        mixer.init()
        try:
            mixer.music.load(str(self.music_file))
        except:
            showinfo("Error", "Please upload a PDF file first")
        else:
            mixer.music.play()
            self.playing_state = False
            self.play_restart.set('Restart')
            self.pause_resume.set('Pause')

    def pause(self):
        if not self.playing_state:
            mixer.music.pause()
            self.playing_state = True
            self.pause_resume.set('Resume')
        else:
            mixer.music.unpause()
            self.playing_state = False
            self.pause_resume.set('Pause')

    def stop(self):
        mixer.music.stop()

    def close(self):
        self.win.destroy()


class Notepad():
    def __init__(self, **kwargs):
        self.__root = Toplevel(window)
        self.__thisWidth = 300
        self.__thisHeight = 300
        self.thisTextArea = Text(self.__root)
        self.__thisMenuBar = Menu(self.__root)
        self.__thisFileMenu = Menu(self.__thisMenuBar, tearoff=0)
        self.__thisEditMenu = Menu(self.__thisMenuBar, tearoff=0)
        self.__thisHelpMenu = Menu(self.__thisMenuBar, tearoff=0)
        self.__thisScrollBar = Scrollbar(self.thisTextArea)
        self.__file = None
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
        self.__thisHelpMenu.add_command(label="Highlight",
                                        command=self.__highlight)
        self.__thisHelpMenu.add_command(label="Clear",
                                        command=self.__clearHighlight)
        self.__thisMenuBar.add_cascade(label="Highlight",
                                       menu=self.__thisHelpMenu)
        self.__root.config(menu=self.__thisMenuBar)
        self.__thisScrollBar.pack(side=RIGHT, fill=Y)
        self.__thisScrollBar.config(command=self.thisTextArea.yview)
        self.thisTextArea.config(yscrollcommand=self.__thisScrollBar.set)

    def __quitApplication(self):
        self.__root.destroy()

    def __highlight(self):
        try:
            self.thisTextArea.tag_add("start", "sel.first", "sel.last")
        except tkinter.TclError:
            pass
        else:
            self.thisTextArea.tag_configure("start", background="yellow", foreground="black")

    def __clearHighlight(self):
        self.thisTextArea.tag_remove("start", "1.0", 'end')

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
        pdf.set_font("Arial", size=10)
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
    try:
        if sourceFile:
            with fitz.open(sourceFile) as doc:
                text = ""
                for page in doc:
                    text += page.get_text()
            notepad = Notepad(width=600, height=400)
            notepad.thisTextArea.insert(1.0, text)
            notepad.run()
    except:
        showinfo("Error")


def chooseFile():
    global sourceFile
    sourceFile = filedialog.askopenfilename(parent=window, initialdir="/", title='Please select a file',
                                            filetypes=[("Pdf files", ".pdf")])

def play_pdf():
    chooseFile()
    with fitz.open(sourceFile) as doc:
        text = ""
        for page in doc:
            text += page.get_text()

    speechengine = pyttsx3.init()

    voices = speechengine.getProperty('voices')
    speechengine.setProperty('voice', voices[2].id)
    string=str(text)
    speechengine.setProperty("rate",125)
    speechengine.setProperty("gender","female")
    speechengine.save_to_file(string,"string.wav")
    speechengine.runAndWait()


def encrypt():
    global temp_win, entry, output_pdf
    chooseFile()
    output_pdf = PdfFileWriter()
    file = PdfFileReader(sourceFile)
    num = file.numPages
    for i in range(num):
        page = file.getPage(i)
        output_pdf.addPage(page)
    temp_win = Toplevel(window)
    temp_win.title("Enter password!")
    temp_win.geometry("300x70")
    entry = Entry(temp_win)
    entry.pack()
    button = Button(temp_win, text="Ok", command=get_pass_encrypted)
    button.pack()


def get_pass_encrypted():
    password = str(entry.get())
    temp_win.destroy()
    output_pdf.encrypt(password)
    showinfo("Success", "File encrypted!")
    with open(sourceFile, "wb") as f:
        output_pdf.write(f)


def decrypt():
    global temp_win, entry, out, file
    chooseFile()
    out = PdfFileWriter()
    file = PdfFileReader(sourceFile)
    temp_win = Toplevel(window)
    temp_win.title("Enter password!")
    temp_win.geometry("300x70")
    entry = Entry(temp_win)
    entry.pack()
    button = Button(temp_win, text="Ok", command=get_pass_decrypted)
    button.pack()


def get_pass_decrypted():
    password = str(entry.get())
    temp_win.destroy()
    if file.isEncrypted:
        file.decrypt(password)
        for idx in range(file.numPages):
            page = file.getPage(idx)
            out.addPage(page)
        with open(sourceFile, "wb") as f:
            out.write(f)
        showinfo("Success", "File decrypted Successfully.")
    else:
        showinfo("Info", "File already decrypted.")


def run():
    win = Toplevel(window)
    MP(win)


def pdf_to_word():
    chooseFile()
    pdf_file = sourceFile
    docx_file = sourceFile[:-4] + "-converted-to-word.docx"
    try:
        parse(pdf_file, docx_file)
    except:
        showinfo("Oops!", "Your file was not converted successfully :(")
    else:
        showinfo("Success", "The file has been converted and saved in the same directory!!")


def pdf_to_pptx():
    chooseFile()
    list_files = subprocess.run(["pdf2pptx", sourceFile])
    showinfo("Success", "The file has been converted and saved in the same directory!!")


image = tkinter.PhotoImage(file="wallpaper.png")
canvas = tkinter.Canvas(window, width=626, height=352, bg="#f7f5dd", highlightthickness=0)
canvas.create_image(313, 176, image=image)
canvas.place(x=0, y=0, relwidth=1, relheight=1)
file_button = tkinter.Button(window, text="Encrypt", width=15, height=2, command=encrypt)
file_button.grid(row=0, column=0, padx=20, pady=8)
file_button1 = tkinter.Button(window, text="Decrypt", width=15, height=2, command=decrypt)
file_button1.grid(row=1, column=0, padx=20, pady=8)
file_button2 = tkinter.Button(window, text="To Text", width=15, height=2, command=toText)
file_button2.grid(row=2, column=0, padx=20, pady=8)
file_button3 = tkinter.Button(window, text="To Word", width=15, height=2, command=pdf_to_word)
file_button3.grid(row=3, column=0, padx=20, pady=8)
file_button4 = tkinter.Button(window, text="To Ppt", width=15, height=2, command=pdf_to_pptx)
file_button4.grid(row=4, column=0, padx=20, pady=8)
file_button5 = tkinter.Button(window, text="To Audio", width=15, height=2, command=run)
file_button5.grid(row=5, column=0, padx=20, pady=8)


window.mainloop()
