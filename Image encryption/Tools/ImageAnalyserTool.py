
import os
from tkinter import *
from tkinter import filedialog

from PIL import ImageTk, Image
from coplot import coplot_horizontal
from correlationcofficient import corr_of_rgb_horizontal
from vertical import corr_of_rgb_vertical
from diagonal import corr_of_rgb_dia
from histogram import redhistogram, greenhistogram, bluehistogram
from npcr import npcrv
from uaci import rootmeansquareerror, uaci
root = Tk()
root.geometry("1200x900")
root.configure(background="#019ad2")
root.title("Image Analysis tool")

curr = os.getcwd()




def allanalysis():
    global output_loc
    corrvalue = corr_of_rgb_horizontal(loc1.get())
    cv = Label(root, text=corrvalue)
    cv.grid(row=3, column=1)
    corrvalue1 = corr_of_rgb_vertical(loc1.get())
    cv1 = Label(root, text=corrvalue1)
    cv1.grid(row=4, column=1)
    corrvalue2 = corr_of_rgb_dia(loc1.get())
    cv2 = Label(root, text=corrvalue2)
    cv2.grid(row=5, column=1)
    coplot_horizontal(loc1.get(), output_loc,
                      "/coplot_horizontal_original.png")
    coplot = Image.open(output_loc+"/coplot_horizontal_original.png")
    redhistogram(loc1.get(), output_loc, "/original_red.png")
    greenhistogram(loc1.get(), output_loc, "/original_green.png")
    bluehistogram(loc1.get(), output_loc, "/original_blue.png")
    coplot.show()



def allanalysis2():
    global output_loc
    corrvalue = corr_of_rgb_horizontal(loc2.get())
    cv = Label(root, text=corrvalue)
    cv.grid(row=3, column=3)
    corrvalue1 = corr_of_rgb_vertical(loc2.get())
    cv1 = Label(root, text=corrvalue1)
    cv1.grid(row=4, column=3)
    corrvalue2 = corr_of_rgb_dia(loc2.get())
    cv2 = Label(root, text=corrvalue2)
    cv2.grid(row=5, column=3)
    coplot_horizontal(loc2.get(), output_loc,
                      "/coplot_horizontal_encrypted.png")
    coplot = Image.open(output_loc+"/coplot_horizontal_encrypted.png")
    redhistogram(loc2.get(), output_loc, "/encrypted_red.png")
    greenhistogram(loc2.get(), output_loc, "/encrypted_green.png")
    bluehistogram(loc2.get(), output_loc, "/encrypted_blue.png")
    coplot.show()



# def rmse():
#     value = rootmeansquareerror(loc1.get(), loc2.get())
#     vrms = Label(root, text=value)
#     vrms.grid(row=10, column=1)



def npcr():
    value = npcrv(loc1.get(), loc2.get())
    npvalue = Label(root, text=value)
    npvalue.grid(row=9, column=1)


def uac():
    value = uaci(loc1.get(), loc2.get())
    ua = Label(root, text=value)
    ua.grid(row=11, column=1)


def askopenfile1():
    path = filedialog.askopenfilename(filetypes=[("Image File", '.jpg'), (
        "Image File", '.png'), ("Image File", '.tiff')])  # allowed image formats are .jpg and .png

    # Delete the address value present in the address bar
    loc1.delete(0, 'end')
    im = Image.open(path)  # Opening image with the previous fetched path
    loc1.insert(END, path)  # inserting the file location in the address bar
    print(path)
    im = im.resize((200, 200), Image.ANTIALIAS)  # resizing the fetched image
    tkimage = ImageTk.PhotoImage(im)  # defining the format of the image
   # print(getsize(path))
    # Displaying the image on the window with the help of label object
    myvar = Label(root, image=tkimage)
    myvar.image = tkimage  # assigning the image value
    # Placing the image using grid layout
    myvar.grid(row=2, column=0, pady=5, padx=20)


def askopenfile2():
    path = filedialog.askopenfilename(filetypes=[("Image File", '.jpg'), (
        "Image File", '.png'), ("Image File", '.tiff')])  # allowed image formats are .jpg and .png
    # Delete the address value present in the address bar
    loc2.delete(0, 'end')
    im = Image.open(path)  # Opening image with the previous fetched path
    loc2.insert(END, path)  # inserting the file location in the address bar
    im = im.resize((200, 200), Image.ANTIALIAS)  # resizing the fetched image
    tkimage = ImageTk.PhotoImage(im)  # defining the format of the image
   # print(getsize(path))
    # Displaying the image on the window with the help of label object
    myvar = Label(root, image=tkimage)
    myvar.image = tkimage  # assigning the image value
    myvar.grid(row=2, column=2, pady=5)  # Placing the image using grid layout

#
# def doegraphplot():
#
#     loc2 = output_loc+"/output.png"
#     coplot_horizontal(loc2)
#
#
# def doographplot():
#     loc = loc1.get()
#     coplot_horizontal(loc)
#
#
def askdirectory():
    global output_loc
    output_loc = filedialog.askdirectory()
    outputl = Label(root, text=output_loc)
    outputl.grid(row=1, column=1)
#
#
# def bifurcation():
#     im = Image.open("bifurcation.png")
#     im.show()

browse1 = Button(root, text="Browse Image", command=askopenfile1,
                 width=15, height=2, bg="#657cc3")
browse2 = Button(root, text="Browse Image", command=askopenfile2,
                 width=15, height=2, bg="#657cc3")
loc1 = Entry(root, width=28)
loc2 = Entry(root, width=28)


browse1.grid(row=0, column=0, padx=10, pady=20)
loc1.grid(row=0, column=1, padx=10, pady=20)
browse2.grid(row=0, column=2, padx=10, pady=20)
loc2.grid(row=0, column=3, padx=10, pady=20)

chooseloc = Button(root, text="Output location",
                   command=askdirectory, width=15, height=2, bg="#657cc3")
chooseloc.grid(row=1, column=0, pady=10)

corrcoff1 = Label(root, text="Correlation-Coefficient(Horizontal)")
corrcoff2 = Label(root, text="Correlation-Coefficient(Horizontal)")
corrcoff1.grid(row=3, column=0)
corrcoff2.grid(row=3, column=2)
corrcoff3 = Label(root, text="Correlation-Coefficient(Vertical)")
corrcoff4 = Label(root, text="Correlation-Coefficient(Vertical)")
corrcoff3.grid(row=4, column=0)
corrcoff4.grid(row=4, column=2)
corrcoff5 = Label(root, text="Correlation-Coefficient(Diagonal)")
corrcoff6 = Label(root, text="Correlation-Coefficient(Diagonal)")
corrcoff5.grid(row=5, column=0)
corrcoff6.grid(row=5, column=2)

histo1 = Label(root, text="Histogram-Analysis")
histo2 = Label(root, text="Histogram-Analysis")
histo1.grid(row=6, column=0, pady=20)
histo2.grid(row=6, column=2, pady=20)

coplot1 = Label(root, text="Correlation Plot")
coplot2 = Label(root, text="Correlation Plot")
coplot1.grid(row=7, column=0, pady=10)
coplot2.grid(row=7, column=2, pady=10)
analyze1 = Button(root, text="Analyse", bg="#f2b91f", command=allanalysis)
analyze2 = Button(root, text="Analyse", bg="#f2b91f", command=allanalysis2)
analyze1.grid(row=12, column=0, pady=20)
analyze2.grid(row=12, column=2, pady=20)

npcr = Button(root, text="NPCR Test", bg="#f2b91f", command=npcr)
npcr.grid(row=9, column=2, pady=10)

# rms = Button(root, text="RMSE Test", bg="#f2b91f", command=rmse)
# rms.grid(row=10, column=2)

uac = Button(root, text="UACI Test", bg="#f2b91f", command=uac)
uac.grid(row=11, column=2, pady=10)
root.mainloop()
