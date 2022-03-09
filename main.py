import tkinter
from tkinter import filedialog
from PyPDF2 import PdfFileReader, PdfFileWriter


window = tkinter.Tk()
window.minsize(width=626, height=352)
window.maxsize(width=626, height=352)
window.resizable(False, False)
sourceFile = ''


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


image = tkinter.PhotoImage(file="wallpaper.png")
canvas = tkinter.Canvas(window, width=626, height=352, bg="#f7f5dd", highlightthickness=0)
canvas.create_image(313, 176, image=image)
canvas.place(x=0, y=0, relwidth=1, relheight=1)
file_button = tkinter.Button(window, text="Choose File", width=15, height=2, command=encrypt)
file_button.place(x=50, y=50)


window.mainloop()
print(sourceFile)
