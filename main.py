import tkinter as tk
from tkinter import ttk, messagebox
from PIL import Image, ImageTk
import random
import time
import os
import json

# Load configuration
with open('config.json', 'r') as config_file:
    config = json.load(config_file)

class CropSettings:
    def __init__(self, thresholds):
        self.thresholds = thresholds

    def check_conditions(self, sensor_data):
        alerts = []
        for sensor, threshold in self.thresholds.items():
            if sensor in ['temperature', 'moisture']:
                if sensor_data[sensor] > threshold["max"]:
                    alerts.append((f"{sensor.capitalize()} too high", 
                                   f"{sensor.capitalize()} is {sensor_data[sensor]:.1f}, maximum is {threshold['max']}",
                                   f"Decrease {sensor}"))
                elif sensor_data[sensor] < threshold["min"]:
                    alerts.append((f"{sensor.capitalize()} too low", 
                                   f"{sensor.capitalize()} is {sensor_data[sensor]:.1f}, minimum is {threshold['min']}",
                                   f"Increase {sensor}"))
        return alerts

class GreenhouseSection:
    def __init__(self, name, crop_type, thresholds):
        self.name = name
        self.crop_type = crop_type
        self.thresholds = thresholds
        self.sensor_data = self.initialize_sensor_data()
        self.crop_settings = CropSettings(thresholds)

    def initialize_sensor_data(self):
        return {
            "temperature": (self.thresholds["temperature"]["min"] + self.thresholds["temperature"]["max"]) / 2,
            "moisture": (self.thresholds["moisture"]["min"] + self.thresholds["moisture"]["max"]) / 2,
            "humidity": 50.0,
            "light_intensity": 20000.0,
            "crop_growth": 1.0
        }

    def update_sensor(self, sensor, change):
        self.sensor_data[sensor] += change

    def check_alerts(self):
        return self.crop_settings.check_conditions(self.sensor_data)

class GreenhouseUI(tk.Tk):
    def __init__(self):
        super().__init__()
        self.title("Smart Greenhouse System")
        self.configure(bg=config['ui_settings']['background_color'])
        self.geometry(f"{config['ui_settings']['window_size']['width']}x{config['ui_settings']['window_size']['height']}")
        self.resizable(False, False)
        self.images = {}
        self.load_images()

        self.sections = [
            GreenhouseSection("Section 1", "Cucumber", config['crop_thresholds']['Cucumber']),
            GreenhouseSection("Section 2", "Tomato", config['crop_thresholds']['Tomato']),
            GreenhouseSection("Section 3", "Squash", config['crop_thresholds']['Squash'])
        ]

        self.create_widgets()

    def load_images(self):
        for key, filename in config['image_files'].items():
            try:
                image_path = os.path.join("images", filename)
                image = Image.open(image_path)
                image = image.resize((50, 50))
                self.images[key] = ImageTk.PhotoImage(image)
            except FileNotFoundError:
                print(f"Warning: Image file {filename} not found. Using placeholder.")
                self.images[key] = None

    def create_widgets(self):
        self.create_greenhouse_area()
        self.create_sensor_labels()
        self.create_control_buttons()
        self.update_time()

    def create_greenhouse_area(self):
        self.canvas = tk.Canvas(self, width=config['ui_settings']['canvas_size']['width'], 
                                height=config['ui_settings']['canvas_size']['height'], 
                                bg=config['ui_settings']['canvas_color'])
        self.canvas.pack(pady=20)

        section_width = 400 // 3
        for i, section in enumerate(self.sections):
            x1 = 50 + i * section_width
            x2 = x1 + section_width
            self.canvas.create_rectangle(x1, 50, x2, 250, fill=config['ui_settings']['greenhouse_color'], outline="black")
            self.canvas.create_text(x1 + section_width // 2, 70, text=f"{section.name}\n({section.crop_type})", font=('Helvetica', 10, 'bold'))

        image_positions = config['image_positions']
        for key, pos in image_positions.items():
            if self.images[key]:
                self.canvas.create_image(pos[0], pos[1], image=self.images[key], tags=key)
            else:
                self.canvas.create_rectangle(pos[0]-25, pos[1]-25, pos[0]+25, pos[1]+25, fill="gray", tags=key)

    def create_sensor_labels(self):
        labels_frame = ttk.Frame(self)
        labels_frame.pack(pady=10)

        self.sensor_labels = {}
        for i, section in enumerate(self.sections):
            section_frame = ttk.LabelFrame(labels_frame, text=f"{section.name} ({section.crop_type})")
            section_frame.grid(row=0, column=i, padx=10, pady=5)

            section_labels = {}
            for sensor in section.sensor_data:
                label = ttk.Label(section_frame, text=f"{sensor.capitalize()}: {section.sensor_data[sensor]:.1f}", font=('Helvetica', 10))
                label.pack(pady=2)
                section_labels[sensor] = label

            self.sensor_labels[section.name] = section_labels

    def create_control_buttons(self):
        button_frame = ttk.Frame(self)
        button_frame.pack(pady=10)

        for i, section in enumerate(self.sections):
            section_frame = ttk.LabelFrame(button_frame, text=section.name)
            section_frame.grid(row=0, column=i, padx=10, pady=5)

            button_config = [
                ("Increase Temp", lambda s=section: self.update_sensor(s, "temperature", 0.5)),
                ("Decrease Temp", lambda s=section: self.update_sensor(s, "temperature", -0.5)),
                ("Increase Moisture", lambda s=section: self.update_sensor(s, "moisture", 2)),
                ("Decrease Moisture", lambda s=section: self.update_sensor(s, "moisture", -2)),
            ]

            for j, (text, command) in enumerate(button_config):
                btn = ttk.Button(section_frame, text=text, command=command, width=15)
                btn.grid(row=j//2, column=j%2, padx=5, pady=5)

    def update_sensor(self, section, sensor, change):
        section.update_sensor(sensor, change)
        self.update_labels(section)
        self.check_alerts(section)

    def update_labels(self, section):
        for sensor, label in self.sensor_labels[section.name].items():
            label.config(text=f"{sensor.capitalize()}: {section.sensor_data[sensor]:.1f}")

    def check_alerts(self, section):
        alerts = section.check_alerts()
        for alert in alerts:
            self.show_alert_popup(section, *alert)

    def show_alert_popup(self, section, title, message, action):
        popup = tk.Toplevel(self)
        popup.title(f"{section.name} - {title}")
        ttk.Label(popup, text=message, font=('Helvetica', 12)).pack(padx=20, pady=10)
        ttk.Button(popup, text=action, command=lambda: self.handle_alert_action(section, action, popup)).pack(pady=10)

    def handle_alert_action(self, section, action, popup):
        if action == "Increase temperature":
            self.update_sensor(section, "temperature", 0.5)
        elif action == "Decrease temperature":
            self.update_sensor(section, "temperature", -0.5)
        elif action == "Increase moisture":
            self.update_sensor(section, "moisture", 2)
        elif action == "Decrease moisture":
            self.update_sensor(section, "moisture", -2)
        popup.destroy()

    def update_time(self):
        current_time = time.strftime("%Y-%m-%d %H:%M:%S")
        self.canvas.delete("time")
        self.canvas.create_text(400, 290, text=f"Time: {current_time}", font=('Helvetica', 12), fill="black", tags="time")
        self.after(1000, self.update_time)
        for section in self.sections:
            self.check_alerts(section)  # Check alerts for each section every second

if __name__ == "__main__":
    app = GreenhouseUI()
    app.mainloop()
