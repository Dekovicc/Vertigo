import matplotlib.pyplot as plt
from matplotlib.widgets import Slider
from numpy import arange, sin, cos, exp

# Initialize data points
i = arange(5000)

# Initial parameters
initial_x1 = 1.0
initial_y1 = 1.4
initial_d = 450.0

# Function to update the plot
def update(val):
    x1 = initial_x1 * cos(i/10.0) * exp(-i/2500.0) * slider_x1.val
    y1 = initial_y1 * sin(i/10.0) * exp(-i/2500.0) * slider_y1.val
    d = slider_d.val

    vx = cos(i/d) * x1 - sin(i/d) * y1
    vy = sin(i/d) * x1 + cos(i/d) * y1

    ax.clear()  # Clear previous plot
    ax.plot(vx, vy, "k")  # Plot new shape

    # Adjust aspect ratio and limits
    h = max(vy) - min(vy)
    w = max(vx) - min(vx)
    ax.set_aspect(w/h)
    ax.set_xlim(min(vx), max(vx))
    ax.set_ylim(min(vy), max(vy))

    plt.draw()

# Create figure and axes
fig, ax = plt.subplots()
plt.subplots_adjust(left=0.1, bottom=0.3)  # Make space for sliders

# Create sliders
ax_slider_d = plt.axes([0.1, 0.02, 0.65, 0.03], facecolor='lightgoldenrodyellow')
ax_slider_x1 = plt.axes([0.1, 0.07, 0.65, 0.03], facecolor='lightgoldenrodyellow')
ax_slider_y1 = plt.axes([0.1, 0.12, 0.65, 0.03], facecolor='lightgoldenrodyellow')

slider_d = Slider(ax_slider_d, 'd', 100, 1000, valinit=initial_d)
slider_x1 = Slider(ax_slider_x1, 'x1', 0.5, 2.0, valinit=1.0)
slider_y1 = Slider(ax_slider_y1, 'y1', 0.5, 2.0, valinit=1.0)

# Update plot when sliders change
slider_d.on_changed(update)
slider_x1.on_changed(update)
slider_y1.on_changed(update)

# Initial plot
update(None)

# Show interactive window
plt.show()
