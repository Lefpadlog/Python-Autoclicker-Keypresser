import random
import time
from threading import Thread
import customtkinter
import pyautogui
import pynput
import pyperclip

root = customtkinter.CTk()
root.title("Auto clicker / Keyboard presser")
root.attributes('-topmost', True)
root.geometry("400x350")
root.resizable(False, False)

running = True


ac_click_delay = 100
ac_random_click_delay = [0, 0]
ac_running = False
ac_start_key = "F1"
ac_stop_key = "F2"


kp_running = False
kp_start_key = "F3"
kp_stop_key = "F4"


customtkinter.set_appearance_mode("Dark")
customtkinter.set_default_color_theme("dark-blue")


tabview_root = customtkinter.CTkTabview(root, width=365, height=330)
tabview_root.pack()
tabview_root.add("Auto clicker")
tabview_root.add("Key presser")



def stop_root():
    global running
    running = False

    root.destroy()


def on_press(key):
    try:
        key = str(key.char)
    except AttributeError:
        key = str(key).split(".")[1].capitalize()


    if key == ac_start_key:
        ac_start()
    elif key == ac_stop_key:
        ac_stop()
    elif key == kp_start_key:
        kp_start()
    elif key == kp_stop_key:
        kp_stop()


def start():
    listener = pynput.keyboard.Listener(on_press=on_press)
    listener.start()
    listener.join()


def update():
    global kp_running
    time.sleep(3)
    while running:
        while ac_running:
            if ac_mouse_button.get() == "Left":
                pyautogui.click()
            elif ac_mouse_button.get() == "Middle":
                pyautogui.middleClick()
            else:
                pyautogui.rightClick()

            if ac_random_click_delay[0] < ac_random_click_delay[1]:
                time.sleep(ac_click_delay/100 + random.randint(ac_random_click_delay[0]*10, ac_random_click_delay[1]*10)/100)
            elif ac_random_click_delay[0] > ac_random_click_delay[1]:
                time.sleep(ac_click_delay/100 + random.randint(ac_random_click_delay[1]*10, ac_random_click_delay[0]*10)/100)
            else:
                if ac_click_delay != 1:
                    time.sleep(ac_click_delay/100)

        while kp_running:
            if kp_repeating_switch.get() == 0:
                kp_running = 0

            # removes all the commands
            clear_code = ""
            for line in str(kp_keys_textbox.get("0.0", customtkinter.END)).splitlines():
                if "//" in line:
                    clear_code += line.replace(line[line.find("//"):], "").strip() + "\n"

                else:
                    clear_code += line.strip() + "\n"

            clear_code = clear_code.strip()

            # runs line for line
            for line in clear_code.splitlines():
                times = 1
                if "*" in line:
                    times = int(line.split("*")[1].strip())
                    line = line.split("*")[0].strip()


                if line.startswith("press"):
                    key = line.replace("press", "").strip()
                    for _ in range(times):
                        pyautogui.press(key)
                elif line.startswith("hold"):
                    key = line.replace("hold", "").strip()
                    for _ in range(times):
                        pyautogui.keyDown(key)
                elif line.startswith("release"):
                    key = line.replace("release", "").strip()
                    for _ in range(times):
                        pyautogui.keyUp(key)
                elif line.startswith("wait"):
                    delay = line.replace("wait", "").strip()
                    if "," in delay:
                        del1 = int(delay.split(",")[0].strip())
                        del2 = int(delay.split(",")[1].strip())
                        if del1 < del2:
                            for _ in range(times):
                                time.sleep(random.randint(del1, del2)/1000)
                        elif del1 > del2:
                            for _ in range(times):
                                time.sleep(random.randint(del2, del1)/1000)
                        else:
                            for _ in range(times):
                                time.sleep(del1)

                    else:
                        for _ in range(times):
                            time.sleep(int(delay)/1000)


        ac_start_button.configure(text=f"Start ({ac_start_key})")
        ac_stop_button.configure(text=f"Stop ({ac_stop_key})")

        kp_start_button.configure(text=f"Start ({kp_start_key})")
        kp_stop_button.configure(text=f"Stop ({kp_stop_key})")

        time.sleep(0.02)


def ac_start():
    global ac_running
    ac_running = True


def ac_stop():
    global ac_running
    ac_running = False


def ac_rec(k):
    global ac_start_key
    global ac_stop_key

    def on_press_ac(key):
        global ac_start_key
        global ac_stop_key

        try:
            key = str(key.char)
        except AttributeError:
            key = str(key).split(".")[1].capitalize()

        if k == "start":
            ac_start_key = key

        else:
            ac_stop_key = key

        listener.stop()

    listener = pynput.keyboard.Listener(on_press=on_press_ac)
    listener.start()
    listener.join()


def ac_click_delay_change(value):
    global ac_click_delay
    ac_click_delay = value
    ac_click_delay_label.configure(text=f"Click delay: {ac_click_delay/100:.2f}")


def ac_from_random_click_delay_change(value):
    global ac_random_click_delay
    ac_random_click_delay = value, ac_random_click_delay[1]
    ac_from_random_click_delay_label.configure(text=f"From: {ac_random_click_delay[0]/10:.2f}")


def ac_to_random_click_delay_change(value):
    global ac_random_click_delay
    ac_random_click_delay = ac_random_click_delay[0], value
    ac_to_random_click_delay_label.configure(text=f"To: {ac_random_click_delay[1]/10:.2f}")


def kp_start():
    global kp_running
    kp_running = True


def kp_stop():
    global kp_running
    kp_running = False


def kp_rec(k):
    global kp_start_key
    global kp_stop_key

    def on_press_kp(key):
        global kp_start_key
        global kp_stop_key

        try:
            key = str(key.char)
        except AttributeError:
            key = str(key).split(".")[1].capitalize()

        key = key.replace("Enter", "Return").replace("Esc", "Escape").replace("Backspace", "BackSpace").\
            replace("Shift_r", "Shift_R").replace("Shift_l", "Shift_L").replace("Ctrl_l", "Control_L").\
            replace("Ctrl_r", "Control_R").replace("Alt_l", "Alt_L").replace("Alt_r", "Alt_R")


        if k == "start":
            kp_start_key = key

        else:
            kp_stop_key = key

        listener.stop()

    listener = pynput.keyboard.Listener(on_press=on_press_kp)
    listener.start()
    listener.join()


def kp_copy():
    pyperclip.copy(kp_keys_textbox.get("0.0", customtkinter.END))


# auto clicker

# mouse button switch
ac_mouse_button = customtkinter.CTkSegmentedButton(tabview_root.tab("Auto clicker"), values=["Left", "Middle", "Right"], width=200, height=30)
ac_mouse_button.pack()
ac_mouse_button.set("Left")


# click delay
ac_click_delay_label = customtkinter.CTkLabel(tabview_root.tab("Auto clicker"), text=f"Click delay: {ac_click_delay/100}")
ac_click_delay_label.pack()

ac_click_delay_slider = customtkinter.CTkSlider(tabview_root.tab("Auto clicker"), from_=1, to=1000, command=ac_click_delay_change)
ac_click_delay_slider.pack()
ac_click_delay_slider.set(ac_click_delay)



# random click delay
ac_random_click_delay_label = customtkinter.CTkLabel(tabview_root.tab("Auto clicker"), text=f"Random click delay")
ac_random_click_delay_label.pack(pady=10)


# from
ac_from_random_click_delay_label = customtkinter.CTkLabel(tabview_root.tab("Auto clicker"), text=f"From: {ac_random_click_delay[0]/10}")
ac_from_random_click_delay_label.place(x=0, y=115)

ac_from_random_click_delay_slider = customtkinter.CTkSlider(tabview_root.tab("Auto clicker"), from_=0, to=30, command=ac_from_random_click_delay_change)
ac_from_random_click_delay_slider.place(x=75, y=120)
ac_from_random_click_delay_slider.set(ac_random_click_delay[0])


# to
ac_to_random_click_delay_label = customtkinter.CTkLabel(tabview_root.tab("Auto clicker"), text=f"To: {ac_random_click_delay[1]/10}")
ac_to_random_click_delay_label.place(x=0, y=145)

ac_to_random_click_delay_slider = customtkinter.CTkSlider(tabview_root.tab("Auto clicker"), from_=0, to=30, command=ac_to_random_click_delay_change)
ac_to_random_click_delay_slider.place(x=75, y=150)
ac_to_random_click_delay_slider.set(ac_random_click_delay[1])



# rec buttons
ac_rec_start_button = customtkinter.CTkButton(tabview_root.tab("Auto clicker"), text=f"Rec start", height=40, width=175, command=lambda: ac_rec("start"))
ac_rec_start_button.place(x=0, y=200)

ac_rec_stop_button = customtkinter.CTkButton(tabview_root.tab("Auto clicker"), text=f"Rec stop", height=40, width=175, command=lambda: ac_rec("stop"))
ac_rec_stop_button.place(x=178, y=200)


# start / stop buttons
ac_start_button = customtkinter.CTkButton(tabview_root.tab("Auto clicker"), text=f"Start ({ac_start_key})", height=40, width=175, command=ac_start)
ac_start_button.pack(side=customtkinter.LEFT, anchor=customtkinter.S)

ac_stop_button = customtkinter.CTkButton(tabview_root.tab("Auto clicker"), text=f"Stop ({ac_stop_key})", height=40, width=175, command=ac_stop)
ac_stop_button.pack(side=customtkinter.RIGHT, anchor=customtkinter.S)



# key presser
kp_keys_label = customtkinter.CTkLabel(tabview_root.tab("Key presser"), text="Script")
kp_keys_label.pack()

# textbox
kp_keys_textbox = customtkinter.CTkTextbox(tabview_root.tab("Key presser"), height=127, width=350)
kp_keys_textbox.pack()
kp_keys_textbox.insert("0.0", "press k                        // Command\n"
                              "wait 1000                    // in ms\n"
                              "hold k \n"
                              "wait 0, 1000               // random time\n"
                              "release k\n"
                              "press a * 10               // presses a 10 times")


# repeating switch
kp_repeating_switch = customtkinter.CTkSwitch(tabview_root.tab("Key presser"), text="Repeating")
kp_repeating_switch.place(x=0, y=165)
kp_repeating_switch.select()

# copy button
kp_copy_button = customtkinter.CTkButton(tabview_root.tab("Key presser"), text=f"copy", height=35, width=50, command=kp_copy)
kp_copy_button.place(x=302, y=160)



# rec buttons
kp_rec_start_button = customtkinter.CTkButton(tabview_root.tab("Key presser"), text=f"Rec start", height=40, width=175, command=lambda: kp_rec("start"))
kp_rec_start_button.place(x=0, y=200)

kp_rec_stop_button = customtkinter.CTkButton(tabview_root.tab("Key presser"), text=f"Rec stop", height=40, width=175, command=lambda: kp_rec("stop"))
kp_rec_stop_button.place(x=178, y=200)


# start / stop buttons
kp_start_button = customtkinter.CTkButton(tabview_root.tab("Key presser"), text=f"Start ({kp_start_key})", height=40, width=175, command=kp_start)
kp_start_button.pack(side=customtkinter.LEFT, anchor=customtkinter.S)

kp_stop_button = customtkinter.CTkButton(tabview_root.tab("Key presser"), text=f"Stop ({kp_stop_key})", height=40, width=175, command=kp_stop)
kp_stop_button.pack(side=customtkinter.RIGHT, anchor=customtkinter.S)




Thread(target=update).start()
Thread(target=start).start()


root.protocol('WM_DELETE_WINDOW', stop_root)
root.mainloop()
