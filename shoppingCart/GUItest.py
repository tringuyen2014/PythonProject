#!/usr/bin/env python3

import tkinter as tk
from tkinter import ttk

class MyFrame(ttk.Frame):
    def __init__(self, master):
        self.master = master
        self.frame = tk.Frame(self.master)
        self.button1 = tk.Button(self.frame, text = 'New Window', width = 25, command = self.new_window)
        self.button1.pack()
        self.frame.pack()
        
        ttk.Frame.__init__(self, master, padding="10 10 10 10")
        self.pack()

        # Define string variables for text entry fields
        self.milesDriven = tk.StringVar()
        self.gallonsUsed = tk.StringVar()
        self.milesPerGallon = tk.StringVar()

        # Display the grid of components
        ttk.Label(self, text="Miles Driven:").grid(
            column=0, row=0, sticky=tk.E)
        ttk.Entry(self, width=30, textvariable=self.milesDriven).grid(
            column=1, row=0)

        ttk.Label(self, text="Gallons of Gas Used:").grid(
            column=0, row=1, sticky=tk.E)
        ttk.Entry(self, width=30, textvariable=self.gallonsUsed).grid(
            column=1, row=1)

        ttk.Label(self, text="Miles Per Gallon:").grid(
            column=0, row=2, sticky=tk.E)
        ttk.Entry(self, width=30, textvariable=self.milesPerGallon,
                  state="readonly").grid(column=1, row=2)

        ttk.Button(self, text="Calculate",command=self.calculate).grid(
            column=1, row=3, sticky=tk.E)

        # Add padding to all components
        for child in self.winfo_children():
            child.grid_configure(padx=5, pady=3)

    def new_window(self):
        self.newWindow = tk.Toplevel(self.master)
        self.app = Demo2(self.newWindow)


    def calculate(self):
        # Get numbers from the first two text entry fields
        milesDriven = float(self.milesDriven.get())
        gallonsUsed = float(self.gallonsUsed.get())

        # Calculate the miles per gallon (mpg)
        mpg = milesDriven / gallonsUsed
        mpg = round(mpg, 2)

        # Display the miles per gallon in the third text field
        self.milesPerGallon.set(mpg)

class Demo2:
    def __init__(self, master):
        self.master = master
        self.frame = tk.Frame(self.master)
        self.quitButton = tk.Button(self.frame, text = 'Quit', width = 25, command = self.close_windows)
        self.quitButton.pack()
        self.frame.pack()

    def close_windows(self):
        self.master.destroy()

def main(): 
        root = tk.Tk()
        root.title("Miles Per Gallon Calculator")
        app = MyFrame(root)
        root.mainloop()

if __name__ == "__main__":
    main()
