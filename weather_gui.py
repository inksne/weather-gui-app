import tkinter as tk
from tkinter import messagebox
from pathlib import Path

from coordinates import get_coordinates
from weather_api_service import get_weather
from weather_formatter import format_weather
from exceptions import ApiServiceError, CantGetCoordinates
from history import save_weather, JSONFileWeatherStorage

class WeatherApp:
    def __init__(self, root):
        self.root = root
        self.root.title("Программа для погоды")
        
        self.city_label = tk.Label(root, text="Введите город:")
        self.city_label.pack(padx=10, pady=5)

        self.city_entry = tk.Entry(root)
        self.city_entry.pack(padx=10, pady=5)

        self.fetch_button = tk.Button(root, text="Получить погоду", command=self.fetch_weather)
        self.fetch_button.pack(padx=10, pady=5)

        self.weather_display = tk.Label(root, text="Информация о погоде появится здесь", wraplength=400)
        self.weather_display.pack(padx=10, pady=10)

        self.save_button = tk.Button(root, text="Сохранить погоду", command=self.save_weather, state=tk.DISABLED)
        self.save_button.pack(padx=10, pady=5)

        self.weather = None

    def fetch_weather(self):
        city = self.city_entry.get()
        if not city:
            messagebox.showerror("Ошибка ввода", "Пожалуйста, введите город.")
            return

        try:
            coordinates = get_coordinates(city)  

            weather = get_weather(coordinates)
            self.weather = weather

            formatted_weather = format_weather(weather)
            self.weather_display.config(text=formatted_weather)

            self.save_button.config(state=tk.NORMAL)
        except CantGetCoordinates:
            messagebox.showerror("Ошибка", "Не удалось получить координаты для города.")
        except ApiServiceError:
            messagebox.showerror("Ошибка", "Не удалось получить информацию о погоде.")

    def save_weather(self):
        if self.weather:
            try:
                save_weather(self.weather, JSONFileWeatherStorage(Path.cwd() / "history.json"))
                messagebox.showinfo("Успех", "Погода успешно сохранена!")
            except Exception as e:
                messagebox.showerror("Ошибка", f"Не удалось сохранить погоду: {str(e)}")
        else:
            messagebox.showerror("Ошибка", "Нет данных о погоде для сохранения.")

def main():
    root = tk.Tk()
    app = WeatherApp(root)
    root.mainloop()

if __name__ == "__main__":
    main()
