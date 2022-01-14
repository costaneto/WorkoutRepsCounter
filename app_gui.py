import os
import tkinter as tk
import PIL.Image
import PIL.ImageTk
import cv2
import camera
import model


class AppGui:
    def __init__(self):
        # open the window
        self.btn_class_one = None
        self.window = tk.Tk()

        # window title
        self.window.title = "Reps Counter"

        # counter of training pictures
        self.counters = [1, 1]

        # rep counter
        self.rep_counter = 0

        # rep state
        self.armsExtended = False
        self.armsContracted = False

        # we want to count only when
        # there's change of state
        self.last_state = 0

        self.model = model.Model()

        self.counting_enabled = False
        self.camera = camera.Camera()

        self.initiate_gui()

        self.delay = 15
        self.update()

        self.window.attributes("-topmost", True)
        self.window.mainloop()

    def initiate_gui(self):
        self.canvas = tk.Canvas(self.window, width=self.camera.width, height=self.camera.height)
        self.canvas.pack()

        self.btn_toggleCounting = tk.Button(self.window, text="Toggle Counting", width=50, command=self.toggle_counting)
        self.btn_toggleCounting.pack(anchor=tk.CENTER, expand=True)

        # this button will take a snapshot
        # of current frame and save it
        # for the training model
        self.btn_class_one = tk.Button(self.window, text="Arms Extended", width=50,
                                       command=lambda: self.save_for_class(1))
        self.btn_class_one.pack(anchor=tk.CENTER, expand=True)
        self.btn_class_two = tk.Button(self.window, text="Arms Contracted", width=50,
                                       command=lambda: self.save_for_class(2))
        self.btn_class_two.pack(anchor=tk.CENTER, expand=True)

        # train model
        self.btn_train_model = tk.Button(self.window, text="Train Model", width=50, command=lambda: self.model.training_model(self.counters))
        self.btn_train_model.pack(anchor=tk.CENTER, expand=True)

        # reset counter
        self.btn_reset_counter = tk.Button(self.window, text="Reset CCounter", width=50, command=self.reset_counter)
        self.btn_reset_counter.pack(anchor=tk.CENTER, expand=True)

        self.counter_label = tk.Label(self.window, text=f"{self.rep_counter}")
        self.counter_label.config(font=("Arial", 24))
        self.counter_label.pack(anchor=tk.CENTER, expand=True)

    def update(self):
        if self.counting_enabled:
            self.predict()

        # the motion consisted of two states.
        # we can count up the rep only after
        # the two states are registered
        if self.armsExtended and self.armsContracted:
            self.armsExtended, self.armsContracted = False, False
            self.rep_counter += 1

        self.counter_label.config(text=f"{self.rep_counter}")

        ret, frame = self.camera.get_frame()
        if ret:
            self.photo = PIL.ImageTk.PhotoImage(image=PIL.Image.fromarray(frame))
            self.canvas.create_image(0, 0, image=self.photo, anchor=tk.NW)

        self.window.after(self.delay, self.update)

    def predict(self):
        frame = self.camera.get_frame()
        prediction = self.model.predict(frame)

        if prediction != self.last_state:
            if prediction == 1:
                self.armsExtended = True
                self.last_state = 1
            if prediction == 2:
                self.armsContracted = True
                self.last_state = 2

    def toggle_counting(self):
        self.counting_enabled = not self.counting_enabled

    def save_for_class(self, class_number):
        ret, frame = self.camera.get_frame()
        if not os.path.exists("1"):
            os.mkdir("1")
        if not os.path.exists("2"):
            os.mkdir("2")

        cv2.imwrite(f"{class_number}/frame{self.counters[class_number - 1]}.jpg", cv2.cvtColor(frame, cv2.COLOR_RGB2GRAY))
        img = PIL.Image.open(f"{class_number}/frame{self.counters[class_number - 1]}.jpg")
        img.thumbnail((150, 150), PIL.Image.ANTIALIAS)
        img.save(f"{class_number}/frame{self.counters[class_number - 1]}.jpg")

        self.counters[class_number - 1] += 1

    def reset_counter(self):
        self.rep_counter = 0
