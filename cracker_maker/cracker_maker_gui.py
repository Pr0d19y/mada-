__author__ = 'nfreiman'
import os
import logging
import datetime
from cracker_maker_parts import Grinder, Water
import Tkinter as Tk
from ttk import Button, Checkbutton
from Tkinter import Text, INSERT, IntVar, Canvas, NW
from time import sleep
import threading


class View(object):
    def __init__(self, master):
        self.logger = logging.getLogger(self.__class__.__name__)
        self.logger.info('initializing View')
        self.frame = Tk.Frame(master, borderwidth=50)

        self.buttons = {}
        self.text_areas = {}
        self.status_viewers = {}
        self.manual_mode_state = IntVar()
        self.manual_mode_checkbox = None

        self.initialize_frame()
        self.initialize_buttons()
        self.initialize_text()
        self.initialize_status_viewers()

        # create layout
        self.frame.pack()

    def initialize_frame(self):
        self.logger.info('in initialize_gui')
        self.frame.columnconfigure(0, pad=3)
        self.frame.columnconfigure(1, pad=3)
        self.frame.columnconfigure(2, pad=3)
        self.frame.columnconfigure(3, pad=3)

        self.frame.rowconfigure(0, pad=3)
        self.frame.rowconfigure(1, pad=3)
        self.frame.rowconfigure(2, pad=3)
        self.frame.rowconfigure(3, pad=3)
        self.frame.rowconfigure(4, pad=3)

        manual_mode = Checkbutton(self.frame, text='Manual Mode', variable=self.manual_mode_state)
        manual_mode.grid(row=0, column=0)
        self.manual_mode_checkbox = manual_mode

    def initialize_buttons(self):
        self.logger.info('in initialize_buttons')
        grinding_button = Button(self.frame, text="Grind", state='disabled')
        grinding_button.grid(row=1, column=0)
        self.buttons['grinding_button'] = grinding_button

        water_button = Button(self.frame, text="Water", state='disabled')
        water_button.grid(row=2, column=0)
        self.buttons['water_button'] = water_button

    def initialize_text(self):
        self.logger.info('in initialize_text')
        grinding_text = Text(self.frame)
        grinding_text.insert(INSERT, 'just some text explanations for grinding')
        grinding_text.configure({'state': 'disabled', 'height': 3, 'width': 30, 'wrap': 'word'})
        grinding_text.grid(row=1, column=3)
        self.text_areas['grinding_text'] = grinding_text

        water_text = Text(self.frame)
        water_text.insert(INSERT, 'just some text explanations for water')
        water_text.configure({'state': 'disabled', 'height': 3, 'width': 30, 'wrap': 'word'})
        water_text.grid(row=2, column=3)
        self.text_areas['water_text'] = water_text

    def initialize_status_viewers(self):
        self.logger.info('in initialize_status_viewers')
        grind_status = StatusCanvasShower(frame=self.frame, on_image_path=r'graphics\green_box.gif', off_image_path=r'graphics\red_box.gif')
        grind_status.grid(row=1, column=1)
        self.status_viewers['grind_status'] = grind_status

        water_status = StatusCanvasShower(frame=self.frame, on_image_path=r'graphics\green_box.gif', off_image_path=r'graphics\red_box.gif')
        water_status.grid(row=2, column=1)
        self.status_viewers['water_status'] = water_status


class StatusCanvasShower(Canvas):
    def __init__(self, frame, on_image_path, off_image_path):
        #self.logger = logging.getLogger(self.__class__.__name__)
        Canvas.__init__(self, frame, width=100, height=100)
        self.on_image = Tk.PhotoImage(file=on_image_path)
        self.off_image = Tk.PhotoImage(file=off_image_path)
        self.image_on_canvas = self.create_image(0, 0, anchor=NW, image=self.on_image)
        self.on_state = True

    def set_on(self):
        if not self.on_state:
            self.itemconfig(self.image_on_canvas, image=self.on_image)
            self.on_state = True

    def set_off(self):
        if self.on_state:
            self.itemconfig(self.image_on_canvas, image=self.off_image)
            self.on_state = False


class Controller(object):
    def __init__(self):
        self.logger = logging.getLogger(self.__class__.__name__)
        self.logger.info('initializing Controller')
        self.root = Tk.Tk()
        self.view = View(master=self.root)
        self.model = Model()

        self.assign_buttons()
        #self.running = True
        self.status_thread = threading.Thread(target=self.graphic_status_thread)
        self.status_thread.setDaemon(True)
        self.status_thread.start()

    def assign_buttons(self):
        self.logger.info('in assign_buttons')
        buttons = self.view.buttons
        buttons['grinding_button'].bind("<Button-1>", self.model.start_grinding)
        buttons['grinding_button'].bind("<ButtonRelease-1>", self.model.stop_grinding)

        buttons['water_button'].bind("<Button-1>", self.model.start_water)
        buttons['water_button'].bind("<ButtonRelease-1>", self.model.stop_water)

        # TODO:  should this be in the Controller or Model? - maybe it depends on if this stoppes the automatic running of the machine
        #self.view.manual_mode_checkbox.configure({'command': lambda: self.model.manual_mode(self.view.manual_mode_state.get())})
        self.view.manual_mode_checkbox.configure({'command': lambda: self.manual_mode(self.view.manual_mode_state.get())})

    def run(self):
        self.logger.info('Starting GUI')
        self.root.mainloop()

    def manual_mode(self, mode):
        self.logger.info('in manual_mode, param: {}'.format(mode))
        if mode:
            self.logger.info('manual mode set, enabling manual operation')
            for button in self.view.buttons.values():
                button.configure({'state': 'enabled'})
        else:
            self.logger.info('manual mode off, disabling manual operation')
            for button in self.view.buttons.values():
                button.configure({'state': 'disabled'})

    def graphic_status_thread(self):
        while True:
            sleep(0.1)
            grind_viewer = self.view.status_viewers['grind_status']
            if self.model.grinder.grinding_state:
                grind_viewer.set_on()
            else:
                grind_viewer.set_off()

            water_viewer = self.view.status_viewers['water_status']
            if self.model.water.water_state:
                water_viewer.set_on()
            else:
                water_viewer.set_off()


class Model(object):
    def __init__(self):
        self.logger = logging.getLogger(self.__class__.__name__)
        self.logger.info('initializing Model')

        self.grinder = Grinder()
        self.water = Water()

    def start_grinding(self, event):
        self.logger.info('in start_grinding')
        self.grinder.start_grinding()

    def stop_grinding(self, event):
        self.logger.info('in stop_grinding')
        self.grinder.stop_grinding()

    def start_water(self, event):
        self.logger.info('in start_water')
        self.water.start_water()

    def stop_water(self, event):
        self.logger.info('in stop_water')
        self.water.stop_water()

    '''
    def manual_mode(self, mode):
        self.logger.info('in manual_mode, param: {}'.format(mode))
        if mode:
            self.logger.info('manual mode set, enabling manual operation')
        else:
            self.logger.info('manual mode off, disabling manual operation')
    '''


def init_logging():
    logger = logging.getLogger()
    s_handler = logging.StreamHandler()

    filename = os.path.join('logs', 'cracker_maker_{}.log'.format(datetime.datetime.now().strftime('%d-%m-%y_%H-%M-%S')))
    if not os.path.exists(os.path.dirname(filename)):
        os.makedirs(os.path.dirname(filename))

    f_handler = logging.FileHandler(filename=filename)

    formatter = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s')
    s_handler.setFormatter(formatter)
    f_handler.setFormatter(formatter)
    logger.addHandler(s_handler)
    logger.addHandler(f_handler)
    logger.setLevel(logging.DEBUG)


if __name__ == '__main__':
    init_logging()
    controller = Controller()
    controller.run()
