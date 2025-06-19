from tkinter import *
from PIL import Image, ImageTk
from tkinter import filedialog, simpledialog
import cv2
import numpy as np
import math

global path_image, password
app = Tk()
app.configure(background='lavender')
app.title("Encrypt")
app.geometry('800x800')  # Increased window size
image_display_size = (300, 300)

def get_password():
    global password
    password = simpledialog.askstring("Password", "Set Security Key:", show="*")

def on_click():
    global path_image
    path_image = filedialog.askopenfilename(filetypes=[("Image Files", "*.png;*.jpg;*.jpeg")])
    
    if not path_image:
        print("No file selected")
        return  
    try:
        load_image = Image.open(path_image)
        load_image.thumbnail(image_display_size)
        np_load_image = np.asarray(load_image)
        np_load_image = Image.fromarray(np.uint8(np_load_image))
        render = ImageTk.PhotoImage(np_load_image)
        img1.config(image=render)
        img1.image = render
    except Exception as e:
        print("Error opening image:", e)

def encrypt_data_into_image():
    global path_image, password
    password1 = simpledialog.askstring("Password", "Enter Security Key:", show="*")
    
    if password != password1:
        error_label.config(text='Authentication Failed! Try Again.')
        return
    
    data = txt.get(1.0, "end-1c")
    img = cv2.imread(path_image)
    data = [format(ord(i), '08b') for i in data]
    _, width, _ = img.shape
    PixReq = len(data) * 3
    RowReq = math.ceil(PixReq / width)
    count, charCount = 0, 0
    
    for i in range(RowReq + 1):
        while count < width and charCount < len(data):
            char = data[charCount]
            charCount += 1
            for index_k, k in enumerate(char):
                if ((k == '1' and img[i][count][index_k % 3] % 2 == 0) or 
                    (k == '0' and img[i][count][index_k % 3] % 2 == 1)):
                    img[i][count][index_k % 3] -= 1
                img[i][count][index_k % 3] = max(0, min(img[i][count][index_k % 3], 255))
                if index_k % 3 == 2:
                    count += 1
            if charCount * 3 < PixReq and img[i][count][2] % 2 == 1:
                img[i][count][2] -= 1
            count += 1
        count = 0
    
    cv2.imwrite("encrypted_image.png", img)
    load = Image.open("encrypted_image.png")
    load.thumbnail(image_display_size)
    np_load_image = np.asarray(load)
    np_load_image = Image.fromarray(np.uint8(np_load_image))
    render = ImageTk.PhotoImage(np_load_image)
    img1.config(image=render)
    img1.image = render
    success_label.config(text='Encryption successful')

def tab2():
    def decrypt():
        global password
        password1 = simpledialog.askstring("Password", "Enter Security Key:", show="*")
        if password != password1:
            error_label.config(text='Authentication Failed! Try Again.')
            return
        
        img = cv2.imread("encrypted_image.png")
        data, stop = [], False
        for index_i, i in enumerate(img):
            for index_j, j in enumerate(i):
                if (index_j % 3 == 2):
                    data.append(bin(j[0])[-1])
                    data.append(bin(j[1])[-1])
                    if bin(j[2])[-1] == '1':
                        stop = True
                        break
                else:
                    data.append(bin(j[0])[-1])
                    data.append(bin(j[1])[-1])
                    data.append(bin(j[2])[-1])
            if stop:
                break
        
        message = ''.join([chr(int(''.join(data[i * 8:(i * 8 + 8)]), 2)) for i in range(len(data) // 8)])
        message_label.config(text=message)
    
    decrypt_button = Button(app, text="DECODE", bg='white', fg='black', command=decrypt)
    decrypt_button.place(x=210, y=460)
    message_label = Label(app, bg='lavender', font=("Times New Roman", 10))
    message_label.place(x=220, y=250)

tab1_button = Button(app, text="Choose Image", bg='white', fg='black', command=on_click)
tab1_button.place(x=250, y=10)

txt = Text(app, wrap=WORD, width=30)
txt.place(x=340, y=55, height=165)

img1 = Label(app)
img1.place(x=20, y=50)

success_label = Label(app, bg='lavender', font=("Times New Roman", 20))
success_label.place(x=160, y=300)

error_label = Label(app, bg='lavender', font=("Times New Roman", 20))
error_label.place(x=160, y=350)

encrypt_button = Button(app, text="ENCODE", bg='white', fg='black', command=encrypt_data_into_image)
encrypt_button.place(x=435, y=230)

decrypt_tab_button = Button(app, text='Start Decryption', command=tab2)
decrypt_tab_button.place(x=300, y=550)

get_password()
app.mainloop()
