import tkinter as tk
import time
import random
import winsound
import questReminders
import pathlib
pathlib.Path(__file__).parent.resolve()

pathname = "swamp/Lib/DesktopKnight/"

class pet:
    def __init__(self):
        # create a window
        self.window = tk.Tk()
        #self.state = 0
        self.cycle = 0
        # dictionary to hold gifs:
        # indexed 0-8, holds a tuple ([photoimage],num of frames)
        self.states = dict()
        self.states["idle_right"] = ([
            tk.PhotoImage(
                file=pathname + "Images/idle_right.gif", format="gif -index %i" % (i)
            )
            for i in range(9)
        ], 10) 
        self.states["idle_left"] = ([
            tk.PhotoImage(
                file=pathname + "Images/idle_left.gif", format="gif -index %i" % (i)
            )
            for i in range(8)
        ], 9)
        self.states["running_right"] = ([
            tk.PhotoImage(
                file=pathname + "Images/running_right.gif", format="gif -index %i" % (i)
            )
            for i in range(8)
        ], 9) 
        self.states["running_left"] = ([
            tk.PhotoImage(
                file=pathname + "Images/running_left.gif", format="gif -index %i" % (i)
            )
            for i in range(9)
        ], 10)
        self.states["attack_right"] = ([
            tk.PhotoImage(
                file=pathname + "Images/attack_right.gif", format="gif -index %i" % (i)
            )
            for i in range(10)
        ], 11) 
        self.states["attack_left"] = ([
            tk.PhotoImage(
                file=pathname + "Images/attack_left.gif", format="gif -index %i" % (i)
            )
            for i in range(9)
        ], 10)
        self.state = random.choice(list(self.states))


        self.frame_index = 0
        self.default_state = "idle_right"
        self.img = self.states[self.default_state][0][self.frame_index]

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
        self.window.geometry(
            "{w}x{h}+{x}+0".format(
                x=str(self.x),
                # w=self.states[self.default_state][0][0].width(),
                # h=self.states[self.default_state][0][0].height(),
                w = 200, h = 200
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

    def change_state(self):
        #self.state = 0
        self.state = random.choice(list(self.states))

    def movement(self):
        if self.state == "running_right":
            self.x += 5
        elif self.state == "running_left":
            self.x -= 5

    def update(self):
        #self.x += 1

        if time.time() > self.timestamp + 0.09:
            self.timestamp = time.time()
            # advance the frame by one, wrap back to 0 at the end
            self.frame_index = (self.frame_index + 1) % (self.states[self.state][1] - 1)
            self.img = self.states[self.state][0][self.frame_index]
        
        self.movement()

        if self.frame_index == 0:
            self.change_state()
        # create the window
        self.window.geometry(
            "{w}x{h}+{x}+0".format(
                x=str(self.x),
                # w=self.states[self.default_state][0][0].width(),
                # h=self.states[self.default_state][0][0].height(),
                w = 200, h = 200
            )
        )
        # add the image to our label
        self.label.configure(image=self.img)
        # give window to geometry manager (so it will appear)
        self.label.pack()

        # call update after 10ms
        self.window.after(10, self.update)

    def play(self, filename):
        winsound.PlaySound(
            pathname + "Sounds/" + filename, winsound.SND_ALIAS | winsound.SND_ASYNC
        )


if __name__ == "__main__":
    pet()
