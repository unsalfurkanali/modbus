# Name:     Delta VFD-EL Modbus Communication
# Author:   Ali Unsal
# Date:     2023-02-02

from pymodbus.client.sync import ModbusSerialClient as ModbusClient
import pymodbus
import time

#Slave address
DRIVER_ID = 3

#Writable addresses 
CMD_STAT = 0x2000   #Stop, Run etc status change address
CMD_FREQ = 0x2001   #Change output frequency

#Readable addresses
OUT_FREQ = 0x2103   #Return output frequency
OUT_CURR = 0x2104   #Return output current

#Commands
RUN_MODE = 0x02     #Run motor value for CMD_STAT
STP_MODE = 0x01     #Stop motor value for CMD_STAT
FWD_MODE = 0x10     #Forward mode for running
REV_MODE = 0x20     #Reverse mode for running
DIR_CHNG = 0x30     #Change direction toggle

def reqOutputFreq(client, id=DRIVER_ID):
    try:
        for i in range(3):
            data = client.read_holding_registers(OUT_FREQ, count = 1, unit = id)
            if not type(data) == pymodbus.pdu.ExceptionResponse and not type(data) == pymodbus.exceptions.ModbusIOException: 
                return data.registers[0]
        return -1
    except:
        print("Connection error!")
        raise ConnectionError

def reqOutputCurr(client, id=DRIVER_ID):
    try:
        for i in range(3):  #try 3 times for line is busy
            data = client.read_holding_registers(OUT_CURR, count = 1, unit = id)
            if not type(data) == pymodbus.pdu.ExceptionResponse and not type(data) == pymodbus.exceptions.ModbusIOException: 
                return data.registers[0]
        return -1
    except:
        print("Connection error!")
        raise ConnectionError

def runMode(client, id=DRIVER_ID, mode = 'stop'):
    try:
        if mode == 'stop':            
            data = client.write_registers(CMD_STAT, STP_MODE, unit = DRIVER_ID)
        elif mode == 'run':
            data = client.write_registers(CMD_STAT, STP_MODE, unit = DRIVER_ID)
        else:
            raise ValueError
        if type(data) == pymodbus.register_write_message.WriteMultipleRegistersResponse:
            return True
        else:
            return False
    except:
        print("Writing error")
        return None

def changeFreq(client, id=DRIVER_ID, freq=5000):
    try:
        if 0 < freq <= 5000:
            data = client.write_registers(CMD_FREQ, freq, unit = id)
            if type(data) == pymodbus.register_write_message.WriteMultipleRegistersResponse:
                return True
        else:
            raise ValueError
    except:
        print("Please check the value")
        return None
    
    

if __name__ == "__main__":
    client = ModbusClient(method='rtu', port='/dev/ttyUSB2', baudrate=9600, timeout=1, parity = 'E', stopbits = 1, bytesize = 8)
    if client.connect():
        print(reqOutputFreq(client))
        client.close()
        