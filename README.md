## Project desciption
An example of using the Adafruit FT232H Breakout PCB to communicate between a PC and MCP3208 over SPI. Additionally, a Python application was developed to control the MCP3208 from a computer and visualize the data on a live graph.

MCP3208
=======
The MCP3208 is an 8-channel, 12-bit ADC chip. It offers two modes for ADC measurement. You can choose between using the analog input channels configured as single-ended inputs or as differential inputs.

To learn more details about this chip, you can refer to its datasheet:
https://www.alldatasheet.com/datasheet-pdf/pdf/74937/MICROCHIP/MCP3208.html

Adafruit-FT232h
=======
Thank you for providing the specific information about the required libraries and the link for installation instructions. Users can follow the instructions provided in the link you shared to install the "pyftdi" Python libraries for proper communication between the computer and the FT232H converter. The link you provided offers detailed steps and guidance on setting up CircuitPython on any computer with the FT232H. It is recommended to follow the instructions provided in the official Adafruit guide for a successful installation and testing of the connection:
https://learn.adafruit.com/circuitpython-on-any-computer-with-ft232h/setup

In those examples, for communication with the MCP3208, you can utilize four GPIO pins: C0 for chip select, C1 for MISO (Master In Slave Out), C2 for MOSI (Master Out Slave In), and C3 for SCK (Serial Clock). These pins are used to establish the SPI (Serial Peripheral Interface) communication between the FT232H and the MCP3208.
