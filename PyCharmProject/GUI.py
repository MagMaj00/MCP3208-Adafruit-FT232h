import tkinter as tk
import board
import digitalio
import matplotlib.pyplot as plt
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg


# Adafruit ft323H configuration

chip_s = digitalio.DigitalInOut(board.C0)
chip_s.direction = digitalio.Direction.OUTPUT

D_out = digitalio.DigitalInOut(board.C2)
D_out.direction = digitalio.Direction.OUTPUT

Clock = digitalio.DigitalInOut(board.C3)
Clock.direction = digitalio.Direction.OUTPUT

D_in = digitalio.DigitalInOut(board.C1)
D_in.direction = digitalio.Direction.INPUT

chip_s.value = True
D_out.value = False
Clock.value = False

Mcp3208_channel = [
            "Channel 0",
            "Channel 1",
            "Channel 2",
            "Channel 3",
            "Channel 4",
            "Channel 5",
            "Channel 6",
            "Channel 7",
        ]
Mcp3208_channel_diff = [
            "CH0 - CH1",
            "CH1 - CH0",
            "CH2 - CH3",
            "CH3 - CH2",
            "CH4 - CH5",
            "CH5 - CH4",
            "CH6 - CH7",
            "CH7 - CH6",
        ]

Mcp3208_mode = [
            "Single",
            "Differential"
        ]

#ADC chip
class MCP3208:

    def __init__(self,Vref):
        self.Vref = Vref

    def read_adc(self,channel,mcp_mode):
        adcvalue = 0
        if mcp_mode == 0:
            sendbits = 0b11000000  #start-bit, mode-bit - single mode
        else:
            sendbits = 0b10000000  # start-bit, mode-bit - diff mode

        sendbits |= ((channel - 1) << 3)
        chip_s.value = False
        for i in range(7, 2, -1):
            if (sendbits & (1 << i)) == 0:
                D_out.value = False

            else:
                D_out.value = True
            Clock.value = True
            Clock.value = False

        Clock.value = True
        Clock.value = False
        Clock.value = True
        Clock.value = False

        for i in range(11, -1, -1):
            if D_in.value == True:
                adcvalue |= 1 << i
            else:
                adcvalue |= 0 << i

            Clock.value = True
            Clock.value = False

        chip_s.value = True
        return adcvalue

    def ADC_encoding(self,ADC_value,):
        Voltage = ADC_value * self.Vref / 4096
        Voltage = round(Voltage,4)
        return Voltage


class MCP_MODE(enumerate):
    SINGLE_MODE = 0
    DIFFERENTIAL_MODE = 1

MCP3208_ob = MCP3208(5.0)

class GUI:
    def __init__(self,mes_delay, x_maxlim):

        self.root = tk.Tk()

        # variables
        self.mes_flag = 1
        self.voltage_value = 0
        self.time_graph = 0
        self.channel = 0
        self.last_channel = 0
        self.mes_delay_ms = mes_delay
        self.mes_delay_sec = mes_delay / 1000
        self.x_maxlim = x_maxlim
        self.mcp_mode_flag = MCP_MODE.SINGLE_MODE
        self.mcp_mode_flag_last = MCP_MODE.SINGLE_MODE

        #main window
        self.root.geometry("1000x600")
        self.root.title("MCP3208")
        self.label = tk.Label(self.root, text = "Voltage value",font = ('Arial',10))
        self.label.pack(padx =20, pady=20)
        self.label.place(x=450, y=40, height=20, width=100)
        self.Output_string_voltage = tk.Text(self.root, font = ('Arial',15))
        self.Output_string_voltage.place(x=450, y=80, height=30, width=100)

        # button
        self.start_button = tk.Button(self.root, text = "START", font=('Arial',10),command = self.start_mes_flag)
        self.start_button.pack(padx = 10,pady = 20)
        self.start_button.place(x=20,y=40,height=80, width=150)

        self.stop_button = tk.Button(self.root, text="STOP", font=('Arial', 10), command=self.stop_mes_flag)
        self.stop_button.pack(padx=10, pady=20)
        self.stop_button.place(x=220, y=40, height=80, width=150)

        # combo box - channel
        self.variable = tk.StringVar(self.root)
        self.variable.set(Mcp3208_channel[0])
        self.Variable_channel = tk.OptionMenu(self.root, self.variable, *Mcp3208_channel)
        self.Variable_channel.pack()
        self.Variable_channel.place(x=610,y=40,height=80, width=150)

        # combo box - mode
        self.mcp_mode = tk.StringVar(self.root)
        self.mcp_mode.set(Mcp3208_mode[0])
        self.mcp_mode_box = tk.OptionMenu(self.root, self.mcp_mode, *Mcp3208_mode)
        self.mcp_mode_box.pack()
        self.mcp_mode_box.place(x=810, y=40, height=80, width=150)

        # graph
        self.fig, self.ax = plt.subplots(figsize=(9, 4))
        self.line, = self.ax.plot([], [], 'o')
        self.canvas = FigureCanvasTkAgg(self.fig, master=self.root)
        self.canvas.get_tk_widget().place(x=50, y=180)
        self.ax.set_xlabel('Time [sec]')
        self.ax.set_ylabel('Voltage value [mV]')
        self.ax.set_xlim(0, self.x_maxlim)
        self.ax.set_ylim(0, 5000)
        self.x_values = [0]
        self.y_values = [0]
        self.update_plot()

        #close aplication
        self.root.protocol("WM_DELETE_WINDOW", self.on_closing)

        self.root.mainloop()


    def reset_live_graph(self):
        self.x_values = [0]
        self.y_values = [0]
        self.time_graph = 0
        self.ax.set_xlim(0, self.x_maxlim)

    def update_plot(self):

        self.check_change_channel()
        self.check_combo_mode()

        self.x_values.append(self.time_graph)
        self.y_values.append(self.voltage_value*1000)
        if self.x_values[-1] > self.x_maxlim:
            self.ax.set_xlim(self.x_values[-1]-self.x_maxlim, self.x_values[-1])
            self.x_values = self.x_values[1:]
            self.y_values = self.y_values[1:]

        self.line.set_data(self.x_values, self.y_values)
        self.ax.relim()
        self.time_graph = self.time_graph + self.mes_delay_sec
        self.canvas.draw()

    def stop_mes_flag(self):
        self.mes_flag = 0
        self.reset_live_graph()

    def start_mes_flag(self):
        self.mes_flag = 1
        self.start_mes()

    def start_mes(self):
        if self.mes_flag == 0:
            return
        if self.mcp_mode_flag == MCP_MODE.SINGLE_MODE:
            if self.variable.get() == Mcp3208_channel[0]:
                x = 1
                self.ax.set_title('Channel 0')
            elif self.variable.get() == Mcp3208_channel[1]:
                x = 2
                self.ax.set_title('Channel 1')
            elif self.variable.get() == Mcp3208_channel[2]:
                x = 3
                self.ax.set_title('Channel 2')
            elif self.variable.get() == Mcp3208_channel[3]:
                x = 4
                self.ax.set_title('Channel 3')
            elif self.variable.get() == Mcp3208_channel[4]:
                x = 5
                self.ax.set_title('Channel 4')
            elif self.variable.get() == Mcp3208_channel[5]:
                x = 6
                self.ax.set_title('Channel 5')
            elif self.variable.get() == Mcp3208_channel[6]:
                x = 7
                self.ax.set_title('Channel 6')
            elif self.variable.get() == Mcp3208_channel[7]:
                x = 8
                self.ax.set_title('Channel 7')
        elif self.mcp_mode_flag == MCP_MODE.DIFFERENTIAL_MODE:
            if self.variable.get() == Mcp3208_channel[0]:
                x = 1
                self.ax.set_title('Channel 0 - Channel 1')
            elif self.variable.get() == Mcp3208_channel[1]:
                x = 2
                self.ax.set_title('Channel 1 - Channel 0')
            elif self.variable.get() == Mcp3208_channel[2]:
                x = 3
                self.ax.set_title('Channel 2 - Channel 3')
            elif self.variable.get() == Mcp3208_channel[3]:
                x = 4
                self.ax.set_title('Channel 3 - Channel 2')
            elif self.variable.get() == Mcp3208_channel[4]:
                x = 5
                self.ax.set_title('Channel 4- Channel 5')
            elif self.variable.get() == Mcp3208_channel[5]:
                x = 6
                self.ax.set_title('Channel 5 - Channel 4')
            elif self.variable.get() == Mcp3208_channel[6]:
                x = 7
                self.ax.set_title('Channel 6 - Channel 7')
            elif self.variable.get() == Mcp3208_channel[7]:
                x = 8
                self.ax.set_title('Channel 7 - Channel 6')


        readvalue = MCP3208_ob.read_adc(x,self.mcp_mode_flag)
        self.voltage_value = MCP3208_ob.ADC_encoding(readvalue)
        self.Output_string_voltage.delete(1.0, tk.END)
        self.Output_string_voltage.insert(tk.END, self.voltage_value)
        self.update_plot()
        self.root.after(self.mes_delay_ms, self.start_mes)

    def check_change_channel(self):
        self.channel = self.variable.get()
        if self.channel != self.last_channel:
            self.reset_live_graph()
        self.last_channel = self.variable.get()


    def check_combo_mode(self):
        if self.mcp_mode.get() == "Single":
            self.mcp_mode_flag = MCP_MODE.SINGLE_MODE
        elif self.mcp_mode.get() == "Differential":
            self.mcp_mode_flag = MCP_MODE.DIFFERENTIAL_MODE
        if self.mcp_mode_flag != self.mcp_mode_flag_last:
            self.reset_live_graph()
        self.mcp_mode_flag_last = self.mcp_mode_flag


    def on_closing(self):
        self.root.quit()
        self.root.destroy()


GUI(1000,60)
