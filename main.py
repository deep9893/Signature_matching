import tkinter as tk
from tkinter.filedialog import askopenfilename
from tkinter import messagebox
import os
import cv2
from numpy import result_type
from signature import match


# Mach Threshold
THRESHOLD = 85


def browsefunc(ent):
    filename = askopenfilename(filetypes=([
        ("image", ".jpeg"),
        ("image", ".png"),
        ("image", ".jpg"),
    ]))
    ent.delete(0, tk.END)
    ent.insert(tk.END, filename)  # add this


def capture_image_from_cam_into_temp(sign=1):
    cam = cv2.VideoCapture(0, cv2.CAP_DSHOW)

    cv2.namedWindow("test")

    # img_counter = 0

    while True:
        ret, frame = cam.read()
        if not ret:
            print("failed to grab frame")
            break
        cv2.imshow("test", frame)

        k = cv2.waitKey(1)
        if k % 256 == 27:
            # ESC pressed
            print("Escape hit, closing...")
            break
        elif k % 256 == 32:
            # SPACE pressed
            if not os.path.isdir('temp'):
                os.mkdir('temp', mode=0o777)  # make sure the directory exists
            # img_name = "./temp/opencv_frame_{}.png".format(img_counter)
            if(sign == 1):
                img_name = "./temp/test_img1.png"
            else:
                img_name = "./temp/test_img2.png"
            print('imwrite=', cv2.imwrite(filename=img_name, img=frame))
            print("{} written!".format(img_name))
            # img_counter += 1
    cam.release()
    cv2.destroyAllWindows()
    return True


def captureImage(ent, sign=1):
    if(sign == 1):
        filename = os.getcwd()+'\\temp\\test_img1.png'
    else:
        filename = os.getcwd()+'\\temp\\test_img2.png'
    # messagebox.showinfo(
    #     'SUCCESS!!!', 'Press Space Bar to click picture and ESC to exit')
    res = None
    res = messagebox.askquestion(
        'Click Picture', 'Press Space Bar to click picture and ESC to exit')
    if res == 'yes':
        capture_image_from_cam_into_temp(sign=sign)
        ent.delete(0, tk.END)
        ent.insert(tk.END, filename)
    return True


def checkSimilarity(window, path1, path2):
    result = match(path1=path1, path2=path2)
    if(result <= THRESHOLD):
        messagebox.showerror("Failure: Signatures Do Not Match",
                             "Signatures are "+str(result)+f" % similar!!")
        pass
    else:
        messagebox.showinfo("Success: Signatures Match",
                            "Signatures are "+str(result)+f" % similar!!")
    return True


root = tk.Tk()
root.title("Signature Matching")
root.geometry("600x500")  # 300x200
uname_label = tk.Label(root, text="Compare Two Signatures", font=('Arial', 18, 'bold'), bg='orange')
uname_label.place(x=110, y=40)

img1_message = tk.Label(root, text="Signature 1", font=('Ariel',18,'bold'),bg='orange')
img1_message.place(x=10, y=120)

image1_path_entry = tk.Entry(root, font=15)
image1_path_entry.place(x=170, y=123)

img1_capture_button = tk.Button(
    root, text="Capture", font=('Ariel',18,'bold'),bg='orange', command=lambda: captureImage(ent=image1_path_entry, sign=1))
img1_capture_button.place(x=410, y=90)

img1_browse_button = tk.Button(
    root, text="Browse", font=('Ariel',18,'bold'),bg='orange', command=lambda: browsefunc(ent=image1_path_entry))
img1_browse_button.place(x=410, y=150)

image2_path_entry = tk.Entry(root, font=15)
image2_path_entry.place(x=170, y=255)

img2_message = tk.Label(root, text="Signature 2", font=('Ariel',18,'bold'),bg='orange')
img2_message.place(x=10, y=250)

img2_capture_button = tk.Button(
    root, text="Capture", font=('Ariel',18,'bold'),bg='orange', command=lambda: captureImage(ent=image2_path_entry, sign=2))
img2_capture_button.place(x=410, y=210)

img2_browse_button = tk.Button(
    root, text="Browse", font=('Ariel',18,'bold'),bg='orange', command=lambda: browsefunc(ent=image2_path_entry))
img2_browse_button.place(x=410, y=270)

compare_button = tk.Button(
    root, text="Compare", font=('Ariel',18,'bold'),bg='orange', command=lambda: checkSimilarity(window=root,
                                                                   path1=image1_path_entry.get(),
                                                                   path2=image2_path_entry.get(),))

compare_button.place(x=200, y=320)
root.config(bg='yellow')
root.mainloop()
