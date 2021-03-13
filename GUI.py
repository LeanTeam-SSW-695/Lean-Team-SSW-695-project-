"""
    authors:
    Abdulellah Shahrani, Chengyi Zhang, Haoran Li, and Sachin Paramesha
    the code:
    The simple GUI for the tiny project first-version using library tkinter
"""

import tkinter
import tkinter.messagebox
import urllib.error
import pickle
import webbrowser
import main

screen = tkinter.Tk()
screen.title("Travel Companion")
screen.geometry("800x600")


canvas = tkinter.Canvas(screen, height=233, width=750)
image_file = tkinter.PhotoImage(file="Image.gif")
image = canvas.create_image(30, 20, anchor='nw', image=image_file)
canvas.pack(side='top')


tkinter.Label(screen, text='Origin Address: ').place(x=50, y=300)
tkinter.Label(screen, text='Destination Address: ').place(x=50, y=360)

origin_address = tkinter.StringVar()
entry_origin = tkinter.Entry(screen, textvariable=origin_address, width=80)
entry_origin.place(x=200, y=300)
destination_address = tkinter.StringVar()
entry_destination = tkinter.Entry(screen, textvariable=destination_address, width=80)
entry_destination.place(x=200, y=360)


def reset():
    entry_destination.delete(0, 'end')
    entry_origin.delete(0, 'end')


def calc():
    originAddress = origin_address.get()
    destinationAddress = destination_address.get()
    try:
        answer, originWeather, destinationWeather = main.main(originAddress, destinationAddress)
        output = "Distance between origin and destination is about {} miles.\nThe temperature at destination" \
                 " address is {}°C, and at origin is {}°C".format(answer, originWeather, destinationWeather)
        tkinter.Label(screen, text=output).place(x=50, y=500)
    except (ValueError, IndexError, urllib.error.URLError):
        tkinter.messagebox.showerror(title='Error!',
                                     message='Please make sure you enter your one-line address correctly.')
    except urllib.error.HTTPError:
        tkinter.messagebox.showerror(title='Error!',
                                     message='Connection Error!')


btn_reset = tkinter.Button(screen, text='Reset', command=reset)
btn_reset.place(x=300, y=460)
btn_calc = tkinter.Button(screen, text='Calculate', command=calc)
btn_calc.place(x=500, y=460)

screen.mainloop()

