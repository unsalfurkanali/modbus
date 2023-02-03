# Name:     Oriental Motor BLV Series Brushless DC Motor Modbus Communication
# Author:   Ali Unsal
# Date:     2023-02-02

from pymodbus.client.sync import ModbusSerialClient as ModbusClient
import pymodbus
import time

SLAVE_ID = 1
BAUD_RATE = 9600
COMM_PORT = '/dev/ttyUSB0'
PRTY_BITS = 'E'
STOP_BITS = 1
COMM_METH = 'rtu'
BYTE_SIZE = 8

OUT_CMDA = 0x7F     #Output command register address
INP_CMDA = 0x7D     #Input command register address
ROT_SPDH = 0x480    #Rotation speed high register address       80 to 4000 r/min
ROT_SPDL = 0x481    #Rotation speed low register address
ACC_TMRH = 0x600    #Acceleration time high register address    2to150 (1 = 0.1 second)
ACC_TMRL = 0x601    #Acceleration time low register address
DEC_TMRH = 0x680    #Deceleration time high register address    2to150 (1 = 0.1 second)
DEC_TMRL = 0x681    #Deceleration time low register address
RST_ALRH = 0x180    #Reset alarm high register address
RST_ALRL = 0x181    #Reset alarm low register address

FWD_MODE = 0x28     #With deceleration stop
REV_MODE = 0x30     #With deceleration stop-
STP_MODE = 0x20     #Deceleration stop
EMG_STOP = 0x00     #Instantaneous stop emergency


class Driver():
    def __init__(self) -> None:
        self.client = 0
        self.connect()
    
    def connect(self):
        self.client = ModbusClient(method=COMM_METH, port=COMM_PORT, baudrate=BAUD_RATE, timeout=1, parity = PRTY_BITS  , stopbits = STOP_BITS, bytesize = BYTE_SIZE)
        if self.client.connect():
            return True
        else:
            raise ConnectionError
    #Connection start function

    def setRotationSpeed(self, value = 100, slave_id = 1):
        if not 0 < value < 4000:
            return False
        data = self.client.write_registers(ROT_SPDL, value, unit = slave_id)
        if type(data) == pymodbus.register_write_message.WriteMultipleRegistersResponse:
            return True
        else:
            raise ValueError
    
    def setAccTime(self, value = 20, slave_id = 1):
        if not 0 < value < 150:
            return False
        data = self.client.write_registers(ACC_TMRL, value, unit = slave_id)
        if type(data) == pymodbus.register_write_message.WriteMultipleRegistersResponse:
            return True
        else:
            raise ValueError
    
    def setDecTime(self, value = 20, slave_id = 1):
        if not 0 < value < 150:
            return False
        data = self.client.write_registers(DEC_TMRL, value, unit = slave_id)
        if type(data) == pymodbus.register_write_message.WriteMultipleRegistersResponse:
            return True
        else:
            raise ValueError
        
    def clearError(self, slave_id = 1):
        data = self.client.write_registers(RST_ALRL, 0xFF, unit = slave_id)
        if type(data) == pymodbus.register_write_message.WriteMultipleRegistersResponse:
            return True
        else:
            raise ValueError
    
    def getAlarmStatus(self, slave_id):
        data = self.client.read_holding_registers(OUT_CMDA, count = 2, unit = slave_id)
        if not type(data) == pymodbus.pdu.ExceptionResponse and not type(data) == pymodbus.exceptions.ModbusIOException: 
            return data.registers[12]
        else:
            return -1
        
    def runFWD(self, slave_id):
        data = self.client.write_registers(INP_CMDA, FWD_MODE, unit = slave_id)
        if type(data) == pymodbus.register_write_message.WriteMultipleRegistersResponse:
            return True
        else:
            return False
    
    def runREV(self, slave_id):
        data = self.client.write_registers(INP_CMDA, REV_MODE, unit = slave_id)
        if type(data) == pymodbus.register_write_message.WriteMultipleRegistersResponse:
            return True
        else:
            return False
    
    def stopRun(self, slave_id):
        data = self.client.write_registers(INP_CMDA, STP_MODE, unit = slave_id)
        if type(data) == pymodbus.register_write_message.WriteMultipleRegistersResponse:
            return True
        else:
            return False
    
    def emergencyStop(self):
        data = self.client.write_registers(INP_CMDA, EMG_STOP)
        if type(data) == pymodbus.register_write_message.WriteMultipleRegistersResponse:
            return True
        else:
            return False
    