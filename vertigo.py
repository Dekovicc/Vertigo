import matplotlib.pyplot as plt
from matplotlib.widgets import Slider, Button, CheckButtons
from numpy import linspace, sin, cos, exp
import tkinter as tk
from tkinter import messagebox

# Initial parameters
initial_amplitude_x = 1.0
initial_amplitude_y = 1.4
initial_rotation_factor = 450.0
initial_aspect_x = 1.0
initial_aspect_y = 1.0
initial_resolution = 5000
keep_aspect_ratio = True

# Function to update the plot
def update(val):
    global i
    resolution = int(slider_resolution.val)
    i = linspace(0, 5000, resolution)

    amp_x = initial_amplitude_x * cos(i / 10.0) * exp(-i / 2500.0) * slider_amplitude_x.val
    amp_y = initial_amplitude_y * sin(i / 10.0) * exp(-i / 2500.0) * slider_amplitude_y.val
    rotation_factor = slider_rotation.val

    vx = cos(i / rotation_factor) * amp_x - sin(i / rotation_factor) * amp_y
    vy = sin(i / rotation_factor) * amp_x + cos(i / rotation_factor) * amp_y

    ax.clear()
    ax.plot(vx, vy, "k")

    # Hide coordinate system
    ax.set_xticks([])
    ax.set_yticks([])
    ax.set_frame_on(False)

    # Adjust aspect ratio
    if keep_aspect_ratio:
        ax.set_aspect('equal')
    else:
        ax.set_aspect(slider_aspect_x.val / slider_aspect_y.val)

    plt.draw()

# Function to export only the graph (no GUI)
def export_file(file_format):
    resolution = int(slider_resolution.val)
    i = linspace(0, 5000, resolution)

    amp_x = initial_amplitude_x * cos(i / 10.0) * exp(-i / 2500.0) * slider_amplitude_x.val
    amp_y = initial_amplitude_y * sin(i / 10.0) * exp(-i / 2500.0) * slider_amplitude_y.val
    rotation_factor = slider_rotation.val

    vx = cos(i / rotation_factor) * amp_x - sin(i / rotation_factor) * amp_y
    vy = sin(i / rotation_factor) * amp_x + cos(i / rotation_factor) * amp_y

    # Create a new figure for export
    export_fig, export_ax = plt.subplots(figsize=(6, 6) if keep_aspect_ratio else (8, 6))
    export_ax.plot(vx, vy, "k")

    # Hide coordinate system
    export_ax.set_xticks([])
    export_ax.set_yticks([])
    export_ax.set_frame_on(False)

    # Set aspect ratio
    if keep_aspect_ratio:
        export_ax.set_aspect('equal')
    else:
        export_ax.set_aspect(slider_aspect_x.val / slider_aspect_y.val)

    # Save the file
    export_fig.savefig(f"output.{file_format}", format=file_format, bbox_inches='tight', transparent=True)
    plt.close(export_fig)  # Close the extra figure to avoid display issues
    show_message(f"{file_format.upper()} Exported", f"File saved as output.{file_format}")

# Show confirmation message
def show_message(title, message):
    root = tk.Tk()
    root.withdraw()
    messagebox.showinfo(title, message)
    root.destroy()

# Function to toggle aspect ratio setting
def toggle_aspect(event):
    global keep_aspect_ratio
    keep_aspect_ratio = not keep_aspect_ratio

    if keep_aspect_ratio:
        slider_aspect_x.set_val(1.0)
        slider_aspect_y.set_val(1.0)

    slider_aspect_x.set_active(not keep_aspect_ratio)
    slider_aspect_y.set_active(not keep_aspect_ratio)
    update(None)

# Create figure and axes
fig, ax = plt.subplots()
plt.subplots_adjust(left=0.1, bottom=0.55)

# Create sliders
ax_slider_rotation = plt.axes([0.1, 0.02, 0.65, 0.03])
ax_slider_amplitude_x = plt.axes([0.1, 0.07, 0.65, 0.03])
ax_slider_amplitude_y = plt.axes([0.1, 0.12, 0.65, 0.03])
ax_slider_resolution = plt.axes([0.1, 0.17, 0.65, 0.03])
ax_slider_aspect_x = plt.axes([0.1, 0.32, 0.65, 0.03])
ax_slider_aspect_y = plt.axes([0.1, 0.37, 0.65, 0.03])

slider_rotation = Slider(ax_slider_rotation, 'Rotation Factor', 100, 1000, valinit=initial_rotation_factor)
slider_amplitude_x = Slider(ax_slider_amplitude_x, 'X Amplitude', 0.5, 2.0, valinit=1.0)
slider_amplitude_y = Slider(ax_slider_amplitude_y, 'Y Amplitude', 0.5, 2.0, valinit=1.0)
slider_resolution = Slider(ax_slider_resolution, 'Resolution', 500, 10000, valinit=initial_resolution, valstep=500)
slider_aspect_x = Slider(ax_slider_aspect_x, 'Aspect Ratio X', 0.5, 2.0, valinit=initial_aspect_x)
slider_aspect_y = Slider(ax_slider_aspect_y, 'Aspect Ratio Y', 0.5, 2.0, valinit=initial_aspect_y)

slider_aspect_x.set_active(False)
slider_aspect_y.set_active(False)

slider_rotation.on_changed(update)
slider_amplitude_x.on_changed(update)
slider_amplitude_y.on_changed(update)
slider_resolution.on_changed(update)
slider_aspect_x.on_changed(update)
slider_aspect_y.on_changed(update)

# Create export buttons
ax_button_svg = plt.axes([0.1, 0.43, 0.2, 0.05])
button_svg = Button(ax_button_svg, 'Export SVG')
button_svg.on_clicked(lambda event: export_file("svg"))

ax_button_png = plt.axes([0.35, 0.43, 0.2, 0.05])
button_png = Button(ax_button_png, 'Export PNG')
button_png.on_clicked(lambda event: export_file("png"))

# Create checkbox for aspect ratio
ax_checkbox = plt.axes([0.75, 0.43, 0.15, 0.05])
checkbox = CheckButtons(ax_checkbox, ['1:1 Aspect'], [True])
checkbox.on_clicked(toggle_aspect)

# Initial plot
update(None)

# Show interactive window
plt.show()
