"""
    authors:
    Abdulellah Shahrani, Chengyi Zhang, Haoran Li, and Sachin Paramesha
    the code:
    The simple GUI for the tiny project first-version using library tkinter
"""

import tkinter
import tkinter.messagebox
from tkinter import BOTTOM

from PIL import ImageTk, Image
import urllib.error
import GoogleMapAPI

screen = tkinter.Tk()
screen.title("Travel Companion")
screen.geometry("1000x800")

canvas = tkinter.Canvas(screen, height=233, width=750)
image_file = tkinter.PhotoImage(file="Image.gif")
image = canvas.create_image(30, 20, anchor='nw', image=image_file)
canvas.pack(side='top')

tkinter.Label(screen, text='Origin Address: ').place(x=50, y=240)
tkinter.Label(screen, text='Destination Address: ').place(x=50, y=300)

origin_address = tkinter.StringVar()
entry_origin = tkinter.Entry(screen, textvariable=origin_address, width=80)
entry_origin.place(x=200, y=240)
destination_address = tkinter.StringVar()
entry_destination = tkinter.Entry(screen, textvariable=destination_address, width=80)
entry_destination.place(x=200, y=300)


def reset():
    entry_destination.delete(0, 'end')
    entry_origin.delete(0, 'end')


def getLocOrigin():
    coordinates = GoogleMapAPI.get_location()
    entry_origin.insert(0, coordinates['neighborhood'])
    origin_coordinates = coordinates['lat'] + coordinates['lng']
    return origin_coordinates


def getLocDestina():
    coordinates = GoogleMapAPI.get_location()
    entry_destination.insert(0, coordinates['neighborhood'])
    destination_coordinates = coordinates['lat'] + coordinates['lng']
    return destination_coordinates


def calc():
    originAddress = origin_address.get()
    destinationAddress = destination_address.get()
    try:
        theDistance, theDuration, originWeather, destinationWeather = GoogleMapAPI.main(originAddress, destinationAddress)
        output = "Distance between origin and destination is about {}\n and the duration of the drive is {}." \
                 "\n\nThe temperature at destination" \
                 " address is {}°F,\n and at origin is {}°F".format(theDistance, theDuration, originWeather,
                                                                  destinationWeather)
        tkinter.Label(screen, text=output).place(x=40, y=440)
    except (ValueError, IndexError, urllib.error.URLError):
        tkinter.messagebox.showerror(title='Error!',
                                     message='Please make sure you enter your one-line address correctly.')
    except urllib.error.HTTPError:
        tkinter.messagebox.showerror(title='Error!',
                                     message='Connection Error!')


def show_map():
    originAddress = GoogleMapAPI.read_address(origin_address.get())
    destinationAddress = GoogleMapAPI.read_address(destination_address.get())
    try:
        GoogleMapAPI.get_map(originAddress, destinationAddress)
        #w = tkinter.Frame(screen, height=500, width=500).place(x=600, y=600)
        #w.pack(side=BOTTOM)
        # loading the image
        img = ImageTk.PhotoImage(Image.open("GoogleMapsImage.png"))
        # reading the image
        panel = tkinter.Label(screen, image=img).place(x=500, y=400)
        # setting the application
        panel.pack(side="bottom", fill="both",
                   expand="yes")
        #panel.pack()
        #w.create_image(100, 20, anchor='s', image=GMImage)

    except (ValueError, IndexError, urllib.error.URLError):
        tkinter.messagebox.showerror(title='Error!',
                                     message='Please make sure you enter your address correctly.')
    except urllib.error.HTTPError:
        tkinter.messagebox.showerror(title='Error!',
                                     message='Connection Error!')


btn_reset = tkinter.Button(screen, text='Reset', command=reset)
btn_reset.place(x=300, y=370)
btn_currLoc1 = tkinter.Button(screen, text='Current Location', command=getLocOrigin)
btn_currLoc1.place(x=650, y=270)
btn_currLoc2 = tkinter.Button(screen, text='Current Location', command=getLocDestina)
btn_currLoc2.place(x=650, y=330)
btn_calc = tkinter.Button(screen, text='Calculate', command=calc)
btn_calc.place(x=400, y=370)
btn_show_map = tkinter.Button(screen, text='Show Directions on Google Maps', command=show_map)
btn_show_map.place(x=500, y=370)

screen.mainloop()
