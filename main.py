from tkinter import *
from tkinter import filedialog as fd
from tkinter.colorchooser import askcolor
import tkinter.messagebox
import PIL
from PIL import Image, ImageDraw, ImageFont, ImageTk
import matplotlib
from matplotlib import font_manager
import os

#Variables for Watermark and Image
img_main = ""
file_main = ""
opacity_main = (255,)
font_size_main = 60
height_main = 0
width_main = 0
rotation_main = 0
color_main = (255, 255, 255)
font_main = "arial"
original_height = 0
original_width = 0
BG = "#AEAEAE"
WHITE = "#FFFFFF"
BLACK = "#000000"
FONT_NAME = "Arial"


def select_img():
    global file_main
    try:
        filename = fd.askopenfilename(filetypes=[("jpeg", ".jpg .jpeg"),
                                                 ("png", ".png"),
                                                 ("bitmap", "bmp"),
                                                 ("gif", ".gif")])
        show_image(filename)
        file_main = filename
    except AttributeError:
        pass


def show_image(filename):
    global height_main, width_main, original_height, original_width
    img = (Image.open(filename))
    width, height = img.size[0], img.size[1]
    r_img = resize(img)
    panel.configure(image=r_img)
    panel.image = r_img
    image_size.config(text=f"Image size {height}/{width} (height/width)", bg=BG, fg=BLACK,
                      font=(FONT_NAME, 8))
    height_main = height / 2
    width_main = width / 2
    original_height = height
    original_width = width


def resize(img):
    size = img.size
    f_size = (700, 600)
    factor = min(float(f_size[1]) / size[1], float(f_size[0]) / size[0])
    width = int(size[0] * factor)
    height = int(size[1] * factor)
    r_img = img.resize((width, height), Image.Resampling.LANCZOS)
    return ImageTk.PhotoImage(r_img)


def watermarking():
    global img_main, file_main, font_size_main
    try:
        with Image.open(file_main).convert("RGBA") as base:
            # make a blank image for the text, initialized to transparent text color
            txt = Image.new("RGBA", base.size, (255, 255, 255, 0))
            # get a font
            fnt = ImageFont.truetype(font_main, font_size_main)
            # get a drawing context
            d = ImageDraw.Draw(txt)
            # draw text
            fill = color_main + (opacity_main,)
            d.text((width_main, height_main), f"{watermark_entry.get()}", font=fnt, fill=fill)
            rotated_txt = txt.rotate(rotation_main)
            out = Image.alpha_composite(base, rotated_txt)

            marked_img = out.convert("RGBA")
            w_img = resize(marked_img)
            panel.configure(image=w_img)
            panel.image = w_img

            img_main = marked_img
    except FileNotFoundError:
        tkinter.messagebox.showerror("Error", "No such file.")
    except PIL.UnidentifiedImageError:
        tkinter.messagebox.showerror("Error", "Wrong file extension.")
    except AttributeError:
        pass



def save(marked_img):
    path = fd.asksaveasfilename(confirmoverwrite=True, defaultextension="png", filetypes=[("jpeg", ".jpg"),
                                                                                          ("png", ".png"),
                                                                                          ("bitmap", "bmp"),
                                                                                          ("gif", ".gif")])
    if path is not None:
        if os.path.splitext(path)[1] == ".jpg":
            image = marked_img.convert("RGB")
            image.save(path)
            tkinter.messagebox.showinfo("Success", "Image got watermarked and saved.")



def color():
    global color_main
    colors = askcolor(title="Tkinter Color Chooser")
    new_color = colors[0]
    color_button.configure(bg=colors[1])
    color_main = new_color
    watermarking()


def set_opacity(value):
    global opacity_main
    opacity_main = int(value)
    watermarking()


def set_font_size():
    global font_size_main
    font_size_main = int(font_size.get())
    watermarking()


def change_font(new_font):
    global font_main
    font_main = new_font
    watermarking()




def up():
    global height_main, original_height
    if original_height > 1500:
        height_main -= 50
    else:
        height_main -= 10
    watermarking()


def down():
    global height_main, original_height
    if original_height > 1500:
        height_main += 50
    else:
        height_main += 10
    watermarking()


def left():
    global width_main, original_width
    if original_width > 1500:
        width_main -= 50
    else:
        width_main -= 10
    watermarking()


def right():
    global width_main, original_width
    if original_width > 1500:
        width_main += 50
    else:
        width_main += 10
    watermarking()


def rotate_left():
    global rotation_main
    rotation_main += 5
    watermarking()


def rotate_right():
    global rotation_main
    rotation_main -= 5
    watermarking()



window = Tk()
window.title("Watermark your Image")
window.minsize(width=500, height=100)
window.config(pady=20, padx=20, bg=BG)

empty_photo = Image.new(mode="RGBA", size=(800, 600), color=WHITE,)
image_1 = ImageTk.PhotoImage(empty_photo)
panel = Label(window, image=image_1, highlightbackground=BG, highlightthickness=0)
panel.image = image_1
panel.grid(column=0, rowspan=15)



image_size = Label(text=f"Image size {height_main}/{width_main} (height/width)",
                   bg=BG, fg=BLACK,font=(FONT_NAME, 10))
image_size.grid(column=0, row=16)

#Text Watermark

watermark = Label(text="Watermark:", width=10, bg=BG, fg=BLACK, font=(FONT_NAME, 16, "bold"))
watermark.grid(column=2, row=2, sticky=W)
watermark_entry = Entry(width=50, highlightthickness=0,highlightbackground=BG)
watermark_entry.grid(column=4, row=2, columnspan=4)
watermark_entry.get()

#Set Color

color_label = Label(text="Color:", bg=BG, fg=BLACK, font=(FONT_NAME, 16, "bold"))
color_label.grid(column=4, row=9, sticky=W)
color_button = Button(text="    ", bg=BG, fg=BLACK, command=color, highlightthickness=0, highlightbackground=BG)
color_button.grid(column=5, row=9, sticky=E)

#Set Opacity

opacity_label = Label(text="Opacity:", bg=BG, fg=BLACK, font=(FONT_NAME, 16, "bold"))
opacity_label.grid(column=4, row=10, sticky=W)
opacity = Scale(window, from_=0, to=255, orient="horizontal",
                bg=BG, fg=BLACK, highlightthickness=0, command=set_opacity)
opacity.set(255)
opacity.grid(column=5, row=10, padx=20, sticky=E)

#Set WM font size

font_label = Label(text="Font size:", bg=BG, fg=BLACK, font=(FONT_NAME, 16, "bold"))
font_label.grid(column=4, row=11, sticky=W)
def_font_size = StringVar(window)
def_font_size.set("60")
font_size = Spinbox(window, from_=1, to=1000, width=5,
                    highlightthickness=0, textvariable=def_font_size, command=set_font_size)
font_size.grid(column=5, row=11, sticky=E)

#Set WM font type

font_list = matplotlib.font_manager.findSystemFonts(fontpaths=None, fontext="ttf")
final_font_list = []
#for Mac
formatted_font_list = [x.split("/")[-1] for x in font_list]
# for Windows formatted_font_list = [x.split("\\")[-1] for x in font_list]
for font in formatted_font_list:
    if ".otf" not in font:
        final_font_list.append(font.replace(".ttf", "").replace(".TTF", "").replace(".ttc", ""))
font = StringVar(window)
font.set("arial")
font_type_label = Label(text="Font:", bg=BG, fg=BLACK, font=(FONT_NAME, 16, "bold"))
font_type_label.grid(column=4, row=12, sticky=W)
font_type = OptionMenu(window, font, *final_font_list, command=change_font)
font_type.grid(column=5, row=12, sticky=E)

#WM Button

show_watermark = Button(text="Show", bg=BG, fg=BLACK,highlightbackground=BG ,command=watermarking)
show_watermark.grid(column=8, row=2)

#Save WM image Button

save_img = Button(text="Save", bg=BG, fg=BLACK, highlightbackground=BG, command=lambda: save(img_main))
save_img.grid(column=7, row=16)

#WM Location

up_btn = Button(text="▲", font=(FONT_NAME, 20), bg=BG, fg=BLACK, command=up)
up_btn.grid(column=4, row=3, sticky=S)

down_btn = Button(text="▼", font=(FONT_NAME, 20), bg=BG, fg=BLACK, command=down)
down_btn.grid(column=4, row=5, sticky=N)

left_btn = Button(text="◀︎", font=(FONT_NAME,20), bg=BG, fg=BLACK, command=left)
left_btn.grid(column=3, row=4, sticky=E, pady=0)

right_btn = Button(text="▶︎", font=(FONT_NAME, 20), bg=BG, fg=BLACK, command=right)
right_btn.grid(column=5, row=4, sticky=W)

rotate_left_btn = Button(text="↖︎", font=(FONT_NAME, 20), bg=BG, fg=BLACK, command=rotate_left)
rotate_left_btn.grid(column=6, row=4, sticky=W)

rotate_right_btn = Button(text="↘︎", font=(FONT_NAME, 20), bg=BG, fg=BLACK, command=rotate_right)
rotate_right_btn.grid(column=7, row=4, sticky=W)

#Select Image

select = Button(text="Select", font=(FONT_NAME, 20), bg=BG, fg=BLACK, highlightbackground=BG, command=select_img)
select.grid(column=0, row=17)

window.mainloop()