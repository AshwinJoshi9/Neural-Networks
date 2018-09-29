# Joshi, Ashwin
# 1001-554-272
# 2018-09-23
# Assignment-02-01

import sys
import scipy as sp
import matplotlib as mpl
import Joshi_02_02
import self as self
if sys.version_info[0] < 3:
    import Tkinter as tk
else:
    import tkinter as tk
from tkinter import simpledialog
from tkinter import filedialog
import matplotlib
import random
from  matplotlib.colors import LinearSegmentedColormap
matplotlib.use('TkAgg')
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
import matplotlib.pyplot as plt
import numpy as np

class MainWindow(tk.Tk):
    """
    This class creates and controls the main window frames and widgets"""
    def __init__(self, debug_print_flag=False):
        tk.Tk.__init__(self)
        self.debug_print_flag = debug_print_flag
        self.master_frame = tk.Frame(self)
        self.master_frame.grid(row=0, column=0, sticky=tk.N + tk.E + tk.S + tk.W)
        self.rowconfigure(0, weight=1, minsize=500)
        self.columnconfigure(0, weight=1, minsize=500)
        self.master_frame.rowconfigure(2, weight=10, minsize=400, uniform='xx')
        self.master_frame.rowconfigure(3, weight=1, minsize=10, uniform='xx')
        self.master_frame.columnconfigure(0, weight=1, minsize=200, uniform='xx')
        self.master_frame.columnconfigure(1, weight=1, minsize=200, uniform='xx')
        # create all the widgets
        self.left_frame = tk.Frame(self.master_frame)

        self.status_bar = StatusBar(self, self.master_frame, bd=1, relief=tk.SUNKEN)
        # Arrange the widgets
        self.left_frame.grid(row=2, columnspan=2, sticky=tk.N + tk.E + tk.S + tk.W)

        self.status_bar.grid(row=3, columnspan=2, sticky=tk.N + tk.E + tk.S + tk.W)
        # Create an object for plotting graphs in the left frame
        self.display_activation_functions = LeftFrame(self, self.left_frame, debug_print_flag=self.debug_print_flag)

class MyDialog(tk.simpledialog.Dialog):
    def body(self, parent):
        tk.Label(parent, text="Integer:").grid(row=0, sticky=tk.W)
        tk.Label(parent, text="Float:").grid(row=1, column=0, sticky=tk.W)
        tk.Label(parent, text="String:").grid(row=1, column=2, sticky=tk.W)
        self.e1 = tk.Entry(parent)
        self.e1.insert(0, 0)
        self.e2 = tk.Entry(parent)
        self.e2.insert(0, 4.2)
        self.e3 = tk.Entry(parent)
        self.e3.insert(0, 'Default text')
        self.e1.grid(row=0, column=1)
        self.e2.grid(row=1, column=1)
        self.e3.grid(row=1, column=3)
        self.cb = tk.Checkbutton(parent, text="Hardcopy")
        self.cb.grid(row=3, columnspan=2, sticky=tk.W)

    def apply(self):
        try:
            first = int(self.e1.get())
            second = float(self.e2.get())
            third = self.e3.get()
            self.result = first, second, third
        except ValueError:
            tk.tkMessageBox.showwarning("Bad input", "Illegal values, please try again")

class StatusBar(tk.Frame):
    def __init__(self, root, master, *args, **kwargs):
        tk.Frame.__init__(self, master, *args, **kwargs)
        self.label = tk.Label(self)
        self.label.grid(row=0, sticky=tk.N + tk.E + tk.S + tk.W)

    def set(self, format, *args):
        self.label.config(text=format % args)
        self.label.update_idletasks()

    def clear(self):
        self.label.config(text="")
        self.label.update_idletasks()


class LeftFrame:
    """
    This class creates and controls the widgets and figures in the left frame which
    are used to display the activation functions."""

    def __init__(self, root, master, debug_print_flag=False):
        self.master = master
        self.root = root
        #########################################################################
        #  Set up the constants and default values
        #########################################################################
        self.xmin = -10
        self.xmax = 10
        self.ymin = -10
        self.ymax = 10
        self.sampleFlag = 0
        self.input_weight = 1
        self.input_weight1 = 1
        self.bias = 0.0
        self.weight_array = np.array([self.input_weight, self.input_weight1])
        self.plotLine = None
        self.plotFlag = False
        self.activation_type = "Symmetrical Hardlimit"
        #########################################################################
        #  Set up the plotting frame and controls frame
        #########################################################################
        master.rowconfigure(0, weight=10, minsize=200)
        master.columnconfigure(0, weight=1, minsize=500)
        self.plot_frame = tk.Frame(self.master, borderwidth=10, relief=tk.SUNKEN)
        self.plot_frame.grid(row=0, column=0, columnspan=2, sticky=tk.N + tk.E + tk.S + tk.W)
        self.plot_frame.rowconfigure(0, weight=1, minsize=200)
        self.plot_frame.columnconfigure(0, weight=1,minsize=500)
        self.figure = plt.figure("")
        self.axes = self.figure.add_axes([0.15, 0.15, 0.6, 0.8])
        # self.axes = self.figure.add_axes()
        self.axes = self.figure.gca()
        self.axes.set_xlabel('INPUT')
        self.axes.set_ylabel('OUTPUT')
        self.axes.set_visible(True)
        # self.axes.margins(0.5)
        self.axes.set_title("Binary Class Decision Boundary", loc='center')
        plt.xlim(self.xmin, self.xmax)
        plt.ylim(self.ymin, self.ymax)
        self.canvas = FigureCanvasTkAgg(self.figure, master=self.plot_frame)
        self.plot_widget = self.canvas.get_tk_widget()
        self.plot_widget.grid(row=0, column=0, sticky=tk.N + tk.E + tk.S + tk.W)
        # Create a frame to contain all the controls such as sliders, buttons, ...
        self.controls_frame = tk.Frame(self.master)
        self.controls_frame.grid(row=1, column=0, sticky=tk.N + tk.E + tk.S + tk.W)
        #########################################################################
        #  Set up the control widgets such as sliders and selection boxes
        #########################################################################

        self.input_weight_slider = tk.Scale(self.controls_frame, variable=tk.DoubleVar(), orient=tk.HORIZONTAL,
                                            from_=-10.0, to_=10.0, resolution=0.01, bg="#DDDDDD",
                                            activebackground="#FF0000", highlightcolor="#00FFFF", label="Input Weight 1",
                                            command=lambda event: self.input_weight_slider_callback())
        self.input_weight_slider.set(self.input_weight)
        self.input_weight_slider.bind("<ButtonRelease-1>", lambda event: self.input_weight_slider_callback())
        self.input_weight_slider.grid(row=0, column=0, sticky=tk.N + tk.E + tk.S + tk.W)


        self.input_weight_slider1 = tk.Scale(self.controls_frame, variable=tk.DoubleVar(), orient=tk.HORIZONTAL,
                                            from_=-10.0, to_=10.0, resolution=0.01, bg="#DDDDDD",
                                            activebackground="#FF0000", highlightcolor="#00FFFF", label="Input Weight 2",
                                            command=lambda event: self.input_weight_slider1_callback())
        self.input_weight_slider1.set(self.input_weight1)
        self.input_weight_slider1.bind("<ButtonRelease-1>", lambda event: self.input_weight_slider1_callback())
        self.input_weight_slider1.grid(row=0, column=1, sticky=tk.N + tk.E + tk.S + tk.W)

        self.bias_slider = tk.Scale(self.controls_frame, variable=tk.DoubleVar(), orient=tk.HORIZONTAL, from_=-10.0,
                                    to_=10.0, resolution=0.01, bg="#DDDDDD", activebackground="#FF0000",
                                    highlightcolor="#00FFFF", label="Bias",
                                    command=lambda event: self.bias_slider_callback())
        self.bias_slider.set(self.bias)
        self.bias_slider.bind("<ButtonRelease-1>", lambda event: self.bias_slider_callback())
        self.bias_slider.grid(row=0, column=2, sticky=tk.N + tk.E + tk.S + tk.W)
        self.trainButton = tk.Button(self.controls_frame, text="Train", command=self.trainNeuralNetwork)
        self.trainButton.grid(row=0, column=4, sticky=tk.N + tk.E + tk.S + tk.W)
        self.randomPoints = tk.Button(self.controls_frame, text="Create Random Data", command=self.randomPointsGenerate)
        self.randomPoints.grid(row=0, column=5, sticky=tk.N + tk.E + tk.S + tk.W)
        #########################################################################
        #  Set up the frame for drop down selection
        #########################################################################
        self.label_for_activation_function = tk.Label(self.controls_frame, text="Activation Function Type:",
                                                      justify="center")
        self.label_for_activation_function.grid(row=0, column=3, sticky=tk.N + tk.E + tk.S + tk.W)
        self.activation_function_variable = tk.StringVar()
        self.activation_function_dropdown = tk.OptionMenu(self.controls_frame, self.activation_function_variable,
                                                          "Linear", "Hyperbolic Tangent", "Symmetrical Hardlimit", command=lambda
                event: self.activation_function_dropdown_callback())
        self.activation_function_variable.set("Symmetrical Hardlimit")
        self.activation_function_dropdown.grid(row=0, column=3, sticky=tk.N + tk.E + tk.S + tk.W)
        self.canvas.get_tk_widget().bind("<ButtonPress-1>", self.left_mouse_click_callback)
        self.canvas.get_tk_widget().bind("<ButtonPress-1>", self.left_mouse_click_callback)
        self.canvas.get_tk_widget().bind("<ButtonRelease-1>", self.left_mouse_release_callback)
        self.canvas.get_tk_widget().bind("<B1-Motion>", self.left_mouse_down_motion_callback)
        self.canvas.get_tk_widget().bind("<ButtonPress-3>", self.right_mouse_click_callback)
        self.canvas.get_tk_widget().bind("<ButtonRelease-3>", self.right_mouse_release_callback)
        self.canvas.get_tk_widget().bind("<B3-Motion>", self.right_mouse_down_motion_callback)
        self.canvas.get_tk_widget().bind("<Key>", self.key_pressed_callback)
        self.canvas.get_tk_widget().bind("<Up>", self.up_arrow_pressed_callback)
        self.canvas.get_tk_widget().bind("<Down>", self.down_arrow_pressed_callback)
        self.canvas.get_tk_widget().bind("<Right>", self.right_arrow_pressed_callback)
        self.canvas.get_tk_widget().bind("<Left>", self.left_arrow_pressed_callback)
        self.canvas.get_tk_widget().bind("<Shift-Up>", self.shift_up_arrow_pressed_callback)
        self.canvas.get_tk_widget().bind("<Shift-Down>", self.shift_down_arrow_pressed_callback)
        self.canvas.get_tk_widget().bind("<Shift-Right>", self.shift_right_arrow_pressed_callback)
        self.canvas.get_tk_widget().bind("<Shift-Left>", self.shift_left_arrow_pressed_callback)
        self.canvas.get_tk_widget().bind("f", self.f_key_pressed_callback)
        self.canvas.get_tk_widget().bind("b", self.b_key_pressed_callback)

    def key_pressed_callback(self, event):
        self.root.status_bar.set('%s', 'Key pressed')

    def up_arrow_pressed_callback(self, event):
        self.root.status_bar.set('%s', "Up arrow was pressed")

    def down_arrow_pressed_callback(self, event):
        self.root.status_bar.set('%s', "Down arrow was pressed")

    def right_arrow_pressed_callback(self, event):
        self.root.status_bar.set('%s', "Right arrow was pressed")

    def left_arrow_pressed_callback(self, event):
        self.root.status_bar.set('%s', "Left arrow was pressed")

    def shift_up_arrow_pressed_callback(self, event):
        self.root.status_bar.set('%s', "Shift up arrow was pressed")

    def shift_down_arrow_pressed_callback(self, event):
        self.root.status_bar.set('%s', "Shift down arrow was pressed")

    def shift_right_arrow_pressed_callback(self, event):
        self.root.status_bar.set('%s', "Shift right arrow was pressed")

    def shift_left_arrow_pressed_callback(self, event):
        self.root.status_bar.set('%s', "Shift left arrow was pressed")

    def f_key_pressed_callback(self, event):
        self.root.status_bar.set('%s', "f key was pressed")

    def b_key_pressed_callback(self, event):
        self.root.status_bar.set('%s', "b key was pressed")

    def left_mouse_click_callback(self, event):
        self.root.status_bar.set('%s', 'Left mouse button was clicked. ' + 'x=' + str(event.x) + '   y=' + str(
            event.y))
        self.x = event.x
        self.y = event.y
        self.canvas.focus_set()

    def left_mouse_release_callback(self, event):
        self.root.status_bar.set('%s',
                                 'Left mouse button was released. ' + 'x=' + str(event.x) + '   y=' + str(event.y))
        self.x = None
        self.y = None

    def left_mouse_down_motion_callback(self, event):
        self.root.status_bar.set('%s', 'Left mouse down motion. ' + 'x=' + str(event.x) + '   y=' + str(event.y))
        self.x = event.x
        self.y = event.y

    def right_mouse_click_callback(self, event):
        self.root.status_bar.set('%s', 'Right mouse down motion. ' + 'x=' + str(event.x) + '   y=' + str(event.y))
        self.x = event.x
        self.y = event.y

    def right_mouse_release_callback(self, event):
        self.root.status_bar.set('%s',
                                 'Right mouse button was released. ' + 'x=' + str(event.x) + '   y=' + str(event.y))
        self.x = None
        self.y = None

    def right_mouse_down_motion_callback(self, event):
        self.root.status_bar.set('%s', 'Right mouse down motion. ' + 'x=' + str(event.x) + '   y=' + str(event.y))
        self.x = event.x
        self.y = event.y

    def left_mouse_click_callback(self, event):
        self.root.status_bar.set('%s', 'Left mouse button was clicked. ' + 'x=' + str(event.x) + '   y=' + str(
            event.y))
        self.x = event.x
        self.y = event.y

    def randomPointsGenerate(self):
        self.axes.cla()
        self.plotLine = None
        self.bias = 0
        self.bias_slider.set(self.bias)
        self.input_weight = self.weight_array[0] = 1
        self.input_weight_slider.set(self.input_weight)
        self.input_weight1 = self.weight_array[1] = 1
        self.input_weight_slider1.set(self.input_weight1)
        self.display_activation_function()
        self.N = 4
        self.x = np.random.randint(-10, 10, self.N)
        self.y = np.random.randint(-10, 10, self.N)
        self.class1X = self.x[:int(self.N/2)]
        self.class1Y = self.y[:int(self.N/2)]
        self.class2X = self.x[int(self.N/2):]
        self.class2Y = self.y[int(self.N/2):]
        plt.xlim(self.xmin, self.xmax)
        plt.ylim(self.ymin, self.ymax)
        plt.plot(self.class1X, self.class1Y, 'yo', markersize=6, label='Class 1')
        plt.plot(self.class2X, self.class2Y, 'bo', markersize=6, label='Class -1')
        plt.legend(loc='upper left',  bbox_to_anchor=(1, 1))
        plt.title("Binary Class Decision Boundary", loc='center')
        self.target = np.array([1, -1])
        self.plotFlag = False
        self.canvas.draw()

    def trainNeuralNetwork(self, plotFlag=False):
        self.plotFlag = plotFlag
        if self.plotLine != None:
            try:
                for line in self.plotLine:
                    line.remove()
            except:
                pass
        epochs = 100
        inputarr = []
        if self.plotFlag == False:
            for index, element in enumerate(self.x):
                inputarr.append([element, self.y[index]])
            input_array = np.array(inputarr)
            epochCounter = 0
            plotLine1 = None
            for epoch in range(0, epochs):
                if plotLine1 != None:
                    for line in plotLine1:
                        line.remove()
                epochCounter += 1
                #errorList = []
                for index, inputIter in enumerate(input_array):
                    activation, net_value = Joshi_02_02.calculate_activation_function(self.weight_array, self.bias, inputIter,
                                                               self.activation_type)
                    np.add(self.weight_array, ((self.target[int(index / 2)]) - activation) * inputIter, out=self.weight_array, casting='unsafe')
                    self.bias += (self.target[int(index / 2)] - activation)
        
        self.display_activation_function()
        self.plotFlag = False

    def display_activation_function(self):
        if self.plotLine != None:
            try:
                for line in self.plotLine:
                    line.remove()
            except:
                pass
        resolution = 100
        xs = np.linspace(-10., 10., resolution)
        ys = np.linspace(-10., 10., resolution)
        xx, yy = np.meshgrid(xs, ys)
        zz = (self.weight_array[0] * xx) + (self.weight_array[1] * yy) + self.bias
        if self.activation_type == "Linear":
            gradientNorm = MidpointNormalize()
            quad = self.axes.pcolormesh(xs, ys, zz,
                                        cmap=LinearSegmentedColormap.from_list('rg', ["r", "w", "g"], N=256),
                                        norm=gradientNorm)
        elif self.activation_type == "Symmetrical Hardlimit":
            zz[zz < 0] = -1
            zz[zz >= 0] = +1
            quad = self.axes.pcolormesh(xs, ys, zz, cmap=LinearSegmentedColormap.from_list('rg', ["r", "w", "g"], N=256))
        elif self.activation_type == "Hyperbolic Tangent":
            zz = np.tanh(zz)
            quad = self.axes.pcolormesh(xs, ys, zz, cmap=LinearSegmentedColormap.from_list('rg', ["r", "w", "g"], N=256))

        plt.xlim(self.xmin, self.xmax)
        plt.ylim(self.ymin, self.ymax)
        ax1 = self.figure.gca()
        if self.weight_array[1] != 0:
            self.plotLine = ax1.plot(xx[0], (-self.bias - (self.weight_array[0] * xx[0])) / self.weight_array[1], xx[1],
                                     (- self.bias - (self.weight_array[0] * xx[1])) / self.weight_array[1], 'k')
        elif self.weight_array[1] == 0:
            if self.weight_array[0] == 0:
                self.plotLine = ax1.plot(xx[0] * 0 - (self.bias), xx[0],
                                         xx[1] * 0 - (self.bias), xx[1], 'k')
            else:
                self.plotLine = ax1.plot(xx[0] * 0 - (self.bias / self.weight_array[0]), xx[0],
                                         xx[1] * 0 - (self.bias / self.weight_array[0]), xx[1], 'k')

        self.canvas.draw()

    def input_weight_slider_callback(self):
        self.input_weight = np.float(self.input_weight_slider.get())
        self.weight_array[0] = self.input_weight
        self.display_activation_function()
        #self.trainNeuralNetwork(True)

    def input_weight_slider1_callback(self):
        self.input_weight1 = np.float(self.input_weight_slider1.get())
        self.weight_array[1] = self.input_weight1
        self.display_activation_function()
        #self.trainNeuralNetwork(True)

    def bias_slider_callback(self):
        self.bias = np.float(self.bias_slider.get())
        self.display_activation_function()
        #self.trainNeuralNetwork(True)

    def activation_function_dropdown_callback(self):
        self.activation_type = self.activation_function_variable.get()
        self.display_activation_function()

def close_window_callback(root):
    if tk.messagebox.askokcancel("Quit", "Do you really wish to quit?"):
        root.destroy()


#Gradient Normalization Center Shifting  => Reference: https://stackoverflow.com/questions/7404116/defining-the-midpoint-of-a-colormap-in-matplotlib
class MidpointNormalize(mpl.colors.Normalize):
    def __init__(self, vmin=None, vmax=None, midpoint=0, clip=False):
        self.midpoint = midpoint
        mpl.colors.Normalize.__init__(self, vmin, vmax, clip)

    def __call__(self, value, clip=None):
        normalized_min = max(0, 1 / 2 * (1 - abs((self.midpoint - self.vmin) / (self.midpoint - self.vmax))))
        normalized_max = min(1, 1 / 2 * (1 + abs((self.vmax - self.midpoint) / (self.midpoint - self.vmin))))
        normalized_mid = 0.5
        x, y = [self.vmin, self.midpoint, self.vmax], [normalized_min, normalized_mid, normalized_max]
        return sp.ma.masked_array(sp.interp(value, x, y))

main_window = MainWindow(debug_print_flag=False)
main_window.wm_state('zoomed')
main_window.title('Assignment_02 --  Joshi')
main_window.minsize(800, 600)
main_window.protocol("WM_DELETE_WINDOW", lambda root_window=main_window: close_window_callback(root_window))
main_window.mainloop()
