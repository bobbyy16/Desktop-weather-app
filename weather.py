from tkinter import *
from tkinter import messagebox
from configparser import ConfigParser
import requests
import json
from PIL import ImageTk, Image
import PIL.Image


url = 'http://api.openweathermap.org/data/2.5/weather?q={}&appid={}'

config_file = 'config.ini'
config = ConfigParser()
config.read(config_file)
api_key = config['api_key']['key']


def get_weather(city):
    result = requests.get(url.format(city, api_key))
    if result:
        json = result.json()
        # (city, country, temp_celsius, temp_faranheit, icon, weather)
        city = json['name']
        country = json['sys']['country']
        temp_kelvin = json['main']['temp']
        temp_celsius = temp_kelvin - 273.15
        temp_faranheit = (temp_kelvin - 273.15) * 9/5 + 32
        icon = json["weather"][0]["icon"]
        weather = json['weather'][0]['main']
        final = (city, country, temp_celsius, temp_faranheit, icon, weather)
        return final
    else:
        return None


def search():
    city = city_text.get()
    weather = get_weather(city)
    if weather:
        city = city_text.get()
        location_lbl['text'] = '{}, {}'.format(weather[0], weather[1])
        img["file"] = 'icons\\{}.gif'.format(weather[4])
        temp_lbl['text'] = '{:.2f}°C, {:.2f}°F'.format(weather[2], weather[3])
        weather_lbl['text'] = weather[5]

    else:
        messagebox.showerror('Error', 'Cannot find city {}'.format(city))


app = Tk()
app.title("Desktop Weather App")
app.geometry("700x350")
app.config(bg="deep sky blue")

city_text = StringVar()
city_entry = Entry(app, textvariable=city_text)
city_entry.pack()

search_button = Button(app, text="Search Weather",
                       bg="cyan", width=12, command=search)
search_button.pack()

location_lbl = Label(app, text="", bg="deep sky blue", font=('bold', 20))
location_lbl.pack()


img = PhotoImage(file="")
Image = Label(app, image=img, bg="deep sky blue")
Image.pack()


temp_lbl = Label(app, text="", bg="deep sky blue")
temp_lbl.pack()

weather_lbl = Label(app, text="", bg="deep sky blue")
weather_lbl.pack()

app.mainloop()
