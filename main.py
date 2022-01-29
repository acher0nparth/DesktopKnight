import tkinter as tk
import time
import winsound
import pyautogui

class pet:
    def __init__(self):
        # create a window
        self.window = tk.Tk()

        # placeholder image
        self.drinking = [
            tk.PhotoImage(
                file="Images/knight_drinking.gif", format="gif -index %i" % (i)
            )
            for i in range(31)
        ]
        self.frame_index = 0
        self.img = self.drinking[self.frame_index]

        # timestamp to check whether to advance frame
        self.timestamp = time.time()

        # set focushighlight to black when the window does not have focus
        self.window.config(highlightbackground="black")

        # make window frameless
        self.window.overrideredirect(True)

        # make window draw over all others
        self.window.attributes("-topmost", True)

        # turn black into transparency
        self.window.wm_attributes("-transparentcolor", "black")

        # create a label as a container for our image
        self.label = tk.Label(self.window, bd=0, bg="black")

        # create a window of size 128x128 pixels, at coordinates 0,0
        self.x = 0
        dim = self.drinking[0].height() * self.drinking[0].width()
        self.window.geometry(
            "{w}x{h}+{x}+0".format(
                x=str(self.x),
                w=self.drinking[0].width(),
                h=self.drinking[0].height(),
            )
        )

        # add the image to our label
        self.label.configure(image=self.img)

        # give window to geometry manager (so it will appear)
        self.label.pack()

        self.play("privparts.wav")

        # run self.update() after 0ms when mainloop starts
        self.window.after(0, self.update)
        self.window.mainloop()


    def update(self):
        # move right by one pixel
        # self.x += 1

        # advance frame if 50ms have passed
        if time.time() > self.timestamp + 0.09:
            self.timestamp = time.time()
            # advance the frame by one, wrap back to 0 at the end
            self.frame_index = (self.frame_index + 1) % 31
            self.img = self.drinking[self.frame_index]

        # create the window
        self.window.geometry(
            "{w}x{h}+{x}+0".format(
                x=str(self.x),
                w=self.drinking[0].width(),
                h=self.drinking[0].height(),
            )
        )
        # add the image to our label
        self.label.configure(image=self.img)
        # give window to geometry manager (so it will appear)
        self.label.pack()

    

        # call update after 10ms
        self.window.after(10, self.update)


    def play(self, filename):
        winsound.PlaySound('Sounds/' + filename, winsound.SND_ALIAS | winsound.SND_ASYNC)


pet()
