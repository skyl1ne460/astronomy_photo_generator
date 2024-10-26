import requests
from tkinter import * 
from tkinter import messagebox
from PIL import ImageTk, Image
from io import BytesIO

def find_apod():
    year = year_entry.get()
    month = month_entry.get()
    day = day_entry.get()

    month = month.zfill(2)
    day = day.zfill(2)

    date = f"{year}-{month}-{day}"

    endpoint = "https://api.nasa.gov/planetary/apod"
    parameters = {"date": date,
                      "api_key": "DEMO_KEY"}

    response = requests.get(url=endpoint, params=parameters)

    if response.ok:
        try:
            data = response.json()

            if 'url' in data:
                image_url = data['url']

                image_response = requests.get(image_url)

                if image_response.ok:

                    image_data = BytesIO(image_response.content)
                    pil_image = Image.open(image_data)
                    nasa_image = ImageTk.PhotoImage(pil_image)

                    canvas.create_image(0, 0, anchor=NW, image=nasa_image)
                    canvas.image = nasa_image

                    window.ai_image = nasa_image
                    window.update()
                else:
                    print("Error downloading image")
            else:
                print("Error: Response does not contain an image URL")

        except Exception as e:
            print("Error processing response:", e)
    else:
        messagebox.showerror("Error: {response.status_code}", "Date Entered Does Not Exist, Enter Valid Date")



window = Tk()
window.config(bg="#141414")
window.title("Astronomy Picture of the Day")
canvas = Canvas(width=500, height=500, bg="#141414", highlightthickness=0)
canvas.grid(pady=15, column=0, row=0, columnspan=7)
year_label = Label(text="YYYY:", bg="#141414", fg="white")
year_label.grid(pady=15, column=1, row=1, sticky="w")
year_entry = Entry(bg="#141414", fg="white")
year_entry.grid(pady=15, column=2, row=1, sticky="w", padx=5)
month_label = Label(text="MM:", bg="#141414", fg="white")
month_label.grid(pady=15, column=3, row=1, sticky="w")
month_entry = Entry(bg="#141414", fg="white")
month_entry.grid(pady=15, column=4, row=1, sticky="w", padx=5)
day_label = Label(text="DD:", bg="#141414", fg="white")
day_label.grid(pady=15, column=5, row=1, sticky="w")
day_entry = Entry(bg="#141414", fg="white")
day_entry.grid(pady=15, column=6, row=1, sticky="w", padx=5)
button = Button(text="Find APOD", command=find_apod, bg="#141414", fg="white")
button.grid(pady=15, padx=15, column=0, row=1)

window.mainloop()