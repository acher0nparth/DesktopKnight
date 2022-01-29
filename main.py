from concurrent.futures import thread
import tkinter as tk
import time
import random
import winsound
#import questReminders
import math
import pathlib
import pyautogui
import math
import threading

pathlib.Path(__file__).parent.resolve()

pathname = "swamp/Lib/DesktopKnight/"


class pet:
    def __init__(self):
        # create a window
        self.window = tk.Tk()
        # self.state = 0
        self.cycle = 0
        self.aggro = 3
        self.aggro_curr = 0
        # dictionary to hold gifs:
        # indexed 0-8, holds a tuple ([photoimage],num of frames)
        self.states = dict()
        self.states["idle_right"] = (
            [
                tk.PhotoImage(
                    file=pathname + "Images/idle_right.gif",
                    format="gif -index %i" % (i),
                )
                for i in range(9)
            ],
            10,
        )
        self.states["idle_left"] = (
            [
                tk.PhotoImage(
                    file=pathname + "Images/idle_left.gif", format="gif -index %i" % (i)
                )
                for i in range(8)
            ],
            9,
        )
        self.states["running_right"] = (
            [
                tk.PhotoImage(
                    file=pathname + "Images/running_right.gif",
                    format="gif -index %i" % (i),
                )
                for i in range(8)
            ],
            9,
        )
        self.states["running_left"] = (
            [
                tk.PhotoImage(
                    file=pathname + "Images/running_left.gif",
                    format="gif -index %i" % (i),
                )
                for i in range(9)
            ],
            10,
        )
        self.states["attack_right"] = (
            [
                tk.PhotoImage(
                    file=pathname + "Images/attack_right.gif",
                    format="gif -index %i" % (i),
                )
                for i in range(10)
            ],
            11,
        )
        self.states["attack_left"] = (
            [
                tk.PhotoImage(
                    file=pathname + "Images/attack_left.gif",
                    format="gif -index %i" % (i),
                )
                for i in range(9)
            ],
            10,
        )
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
        self.y = 0
        self.window.geometry(
            "{w}x{h}+{x}+{y}".format(
                x=str(self.x),
                y=str(self.y),
                # w=self.states[self.default_state][0][0].width(),
                # h=self.states[self.default_state][0][0].height(),
                w=200,
                h=200,
            )
        )
        self.center = (self.x + 100, self.y + 100)

        self.chasing = False
        # add the image to our label
        self.label.configure(image=self.img)

        # give window to geometry manager (so it will appear)
        self.label.pack()

        # self.play("privparts.wav")

        self.sound_thread = threading.Thread(target=self.play, args=("fart.wav",))

        self.mouse_x, self.mouse_y = pyautogui.position()

        # run self.update() after 0ms when mainloop starts
        self.window.after(0, self.update)
        self.window.mainloop()

    def change_state(self):
        # self.state = 0
        #self.state = random.choice(list(self.states))
        chase_distance = 1000
        attack_distance = 200
        dx = self.mouse_x - self.center[0]
        dy = self.mouse_y - self.center[1]
        distance = math.sqrt(dx * dx + dy * dy)
        if self.state == "idle_right" or self.state == "idle_left":
            if distance < chase_distance:
                if self.mouse_x > self.x:
                    self.state = "running_right"
                else:
                    self.state = "running_left"
            else:
                if self.state == "idle_right":
                    self.state = "idle_left"
                else:
                    self.state = "idle_right"
        elif self.state == "running_left" or self.state == "running_right":
            if distance < attack_distance:
                if self.mouse_x < self.x:
                    self.state = "attack_left"
                else:
                    self.state = "attack_right"
            elif distance > chase_distance:
                self.state = "idle_right"
            else:
                if self.mouse_x > self.x:
                    self.state = "running_right"
                else:
                    self.state = "running_left"
        else:
            if distance < attack_distance:
                if self.aggro_curr < self.aggro:
                    self.aggro_curr += 1
                else:
                    self.state = "idle_right"
                    self.aggro_curr = 0
            else:
                self.state = "idle_left"
        
            

    def movement(self):
        # if self.state == "running_right":
        #     self.x += 5
        # elif self.state == "running_left":
        #     self.x -= 5

        dx = self.mouse_x - self.center[0]
        dy = self.mouse_y - self.center[1]
        distance = math.sqrt(dx * dx + dy * dy)
        if distance < 600:
            self.chase(dx, dy, distance)
        else:
            self.chasing = False

    def chase(self, dx, dy, distance):
        # self.play("bitelegs.wav")
        if not self.sound_thread.is_alive() and not self.chasing:
            self.chasing = True
            self.sound_thread = threading.Thread(
                target=self.play, args=("bitelegs.wav",)
            )
            #self.sound_thread.start()
        if distance < 90:
            if not self.sound_thread.is_alive():
                self.sound_thread = threading.Thread(
                    target=self.play, args=("mp_grail.wav",)
                )
                #self.sound_thread.start()
        else:
            try:
                dx /= distance
                dy /= distance
                self.x += round(dx)
                self.y += round(dy)
            except (ZeroDivisionError):
                pass

    def update(self):
        # self.x += 1

        if time.time() > self.timestamp + 0.09:
            self.timestamp = time.time()
            # advance the frame by one, wrap back to 0 at the end
            self.frame_index = (self.frame_index + 1) % (self.states[self.state][1] - 1)
            self.img = self.states[self.state][0][self.frame_index]

        self.mouse_x, self.mouse_y = pyautogui.position()
        self.center = (self.x + 100, self.y + 100)
        self.movement()

        if self.frame_index == 0:
            self.change_state()

        self.movement()
        # create the window
        self.window.geometry(
            "{w}x{h}+{x}+{y}".format(
                x=str(self.x),
                y=str(self.y),
                # w=self.states[self.default_state][0][0].width(),
                # h=self.states[self.default_state][0][0].height(),
                w=200,
                h=200,
            )
        )
        # add the image to our label
        self.label.configure(image=self.img)
        # give window to geometry manager (so it will appear)
        self.label.pack()

        # call update after 10ms
        self.window.after(10, self.update)

    def play(self, filename):
        winsound.PlaySound(pathname + "Sounds/" + filename, winsound.SND_ALIAS)


if __name__ == "__main__":
    pet()
