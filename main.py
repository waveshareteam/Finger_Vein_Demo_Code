import serial
import time
import threading
import serial_comm

PREFIX_CODE = 0xAABB  # Prefix code 0xAABB in little-endian format
bAddress = 0x00  #Device address

#********************************* Comamnd List *********************************#
XG_CMD_CONNECTION = 0x01                # Connect device
XG_CMD_CLOSE_CONNECTION = 0x02          # Close connection
XG_CMD_GET_SYSTEM_INFO = 0x03           # Get version number and system information
XG_CMD_FACTORY_SETTING = 0x04           # Restore factory settings
XG_CMD_SET_DEVICE_ID = 0x05             # Set device ID 0-255
XG_CMD_SET_BAUDRATE = 0x06              # Set baud rate 0-4
XG_CMD_SET_SECURITYLEVEL = 0x07         # Set security level 0-4
XG_CMD_SET_TIMEOUT = 0x08               # Set fingerprint waiting timeout 1-255 seconds
XG_CMD_SET_DUP_CHECK = 0x09             # Set duplicate registration check 0-1
XG_CMD_SET_PASSWORD = 0x0A              # Set communication password
XG_CMD_CHECK_PASSWORD = 0x0B            # Verify if the communication password is correct
XG_CMD_REBOOT = 0x0C                    # Reset device
XG_CMD_SET_SAME_FV = 0x0D               # Whether the same finger is used during registration
XG_CMD_SET_USB_MODE = 0x0E              # Set USB working mode
XG_CMD_GET_DUID = 0x0F                  # Get device serial number
XG_CMD_FINGER_STATUS = 0x10             # Detect fingerprint status
XG_CMD_CLEAR_ENROLL = 0x11              # Delete fingerprint ID registration data
XG_CMD_CLEAR_ALL_ENROLL = 0x12          # Delete all ID registration data
XG_CMD_GET_EMPTY_ID = 0x13              # Get empty, no registration data, ID
XG_CMD_GET_ENROLL_INFO = 0x14           # Get the number of registered users and the maximum number of users
XG_CMD_GET_ID_INFO = 0x15               # Get specified ID registration information
XG_CMD_ENROLL = 0x16                    # Fingerprint ID registration
XG_CMD_VERIFY = 0x17                    # 1:1 verification or 1:N identification
#** Reserved
XG_CMD_READ_DATA = 0x20                 # Read data from the device
XG_CMD_WRITE_DATA = 0x21                # Write data to the device
XG_CMD_READ_ENROLL = 0x22               # Read fingerprint ID registration data
XG_CMD_WRITE_ENROLL = 0x23              # Write (overwrite) fingerprint ID registration data
XG_CMD_GET_CHARA = 0x28                 # Get the currently collected feature code
XG_CMD_READ_USER_DATA = 0x29            # Read data from the user extended storage area, up to 4K
XG_CMD_WRITE_USER_DATA = 0x2A           # Write data to the user extended storage area, up to 4K
XG_CMD_GET_SYS_SET = 0x2E               # Get D700 device system setting data structure
XG_CMD_SET_SYS_SET = 0x2F               # Set D700 system setting data structure
XG_CMD_OPEN_DOOR = 0x32                 # Open door
XG_CMD_READ_LOG = 0x33                  # Read access control log
XG_CMD_SET_DEVNAME = 0x34               # Set device name
XG_CMD_GET_DATETIME = 0x35              # Get access control real-time clock
XG_CMD_SET_DATETIME = 0x36              # Set access control real-time clock
XG_CMD_ENROLL_EXT = 0x38                # Extended fingerprint registration
XG_CMD_VERIFY_EXT = 0x39                # Extended fingerprint verification
XG_CMD_DEL_LOG = 0x3A                   # Delete access control log
XG_CMD_PLAY_VOICE = 0x3B                # Play voice
XG_CMD_GET_USER_BATCH = 0x51            # Batch get user information
XG_CMD_SET_USER_BATCH = 0x52            # Batch write user information
XG_CMD_READ_CARDNO = 0x53               # D700 read card number through user card swipe

#********************************* Error Codes *********************************#
XG_ERR_SUCCESS = 0x00                   # Operation successful
XG_ERR_FAIL = 0x01                      # Operation failed
XG_ERR_COM = 0x02                       # Communication error
XG_ERR_DATA = 0x03                      # Data checksum error
XG_ERR_INVALID_PWD = 0x04               # Password error
XG_ERR_INVALID_PARAM = 0x05             # Parameter error
XG_ERR_INVALID_ID = 0x06                # ID error
XG_ERR_EMPTY_ID = 0x07                  # Specified ID is empty, no registration data
XG_ERR_NOT_ENOUGH = 0x08                # Not enough registration space
XG_ERR_NO_SAME_FINGER = 0x09            # Not the same finger
XG_ERR_DUPLICATION_ID = 0x0A            # Duplicate registration ID
XG_ERR_TIME_OUT = 0x0B                  # Fingerprint waiting timeout
XG_ERR_VERIFY = 0x0C                    # Verification failed
XG_ERR_NO_NULL_ID = 0x0D                # No empty ID
XG_ERR_BREAK_OFF = 0x0E                 # Communication interrupted
XG_ERR_NO_CONNECT = 0x0F                # Not connected
XG_ERR_NO_SUPPORT = 0x10                # Function not supported
XG_ERR_NO_VEIN = 0x11                   # No fingerprint data
XG_ERR_MEMORY = 0x12                    # Insufficient memory
XG_ERR_NO_DEV = 0x13                    # Device not found
XG_ERR_ADDRESS = 0x14                   # Device address error
XG_ERR_NO_FILE = 0x15                   # File not found
XG_ERR_VER = 0x16                       # Version error
XG_ERR_BREAK_CARD = 0x17                # Card swipe interrupted

#********************************* Status Codes *********************************
XG_INPUT_FINGER = 0x20                  # Please place your finger
XG_RELEASE_FINGER = 0x21                # Please lift your finger

ser_com = serial_comm.get_serial_port()

# Command Buff
cmd = [0x00] * 24
rsp = [0x00] * 24

Baudrate = {0:9600, 1:19200, 2:38400, 3:57600, 4:115200}
Devpassword ='00000000'
cmd_test = [0xBB, 0xAA, 0x00, 0x01, 0x00, 0x08, 0x30, 0x30, 0x30, 0x30, 0x30, 0x30, 0x30, 0x30, 0x00, 0x00, 0x00, 0x00
, 0x00, 0x00, 0x00, 0x00, 0xee, 0x02]
#*********************************************
ser = serial.Serial(
    ser_com, 
    baudrate = Baudrate[3],
    rtscts=False,
    dsrdtr=False,
    timeout=1
    )

def rx_monitor():
    while True:
        try:
            if ser.in_waiting:
                remaining = ser.read(24)
                print("Received raw data:", [hex(x) for x in remaining])
                if len(remaining) != 24:
                    print("Error: Incomplete packet received")
                    continue
        except Exception as e:
            print("Error reading from serial port:", e)
            time.sleep(0.1)

rx_thread = threading.Thread(target=rx_monitor, daemon=True)
#rx_thread.start()

class Cmd_Packet: #Command package for sending, 24 bytes
    def __init__(self):
        self.wPrefix        = PREFIX_CODE   # 2 bytes
        self.bAddress       = bAddress      # 1 byte
        self.bCmd           = 0x00          # 1 byte
        self.bEncode        = 0x00          # 1 byte
        self.bDataLen       = 0x00          # 1 byte
        self.bData          = [0x00] * 16   # 16 bytes
        self.wCheckSum      = 0x000         # 2 bytes

class Rsp_Packet: #Response package for receiving, 24 bytes
    def __init__(self):
        self.wPrefix        = PREFIX_CODE   # 2 bytes
        self.bAddress       = bAddress      # 1 byte
        self.bCmd           = 0x00          # 1 byte
        self.bEncode        = 0x00          # 1 byte
        self.bDataLen       = 0x00          # 1 byte
        self.bData          = [0x00] * 16   # 16 bytes
        self.wCheckSum      = 0x000         # 2 bytes

CMD = Cmd_Packet()
RSP = Rsp_Packet()

#*********************************************
#Function: Send Command via serial port
#pBuf: Buffer address to send data
#Len: Length of data to be sent
#Return: Number of bytes sent

def UartSendCmd(timeout = 3):
    Checksum = 0x00
    global CMD, cmd
    cmd[0] = (CMD.wPrefix & 0xFF)         # Low byte of wPrefix
    cmd[1] = (CMD.wPrefix >> 8) & 0xFF    # High byte of wPrefix
    cmd[2] = CMD.bAddress
    cmd[3] = CMD.bCmd
    cmd[4] = CMD.bEncode
    cmd[5] = CMD.bDataLen & 0xFF
    for i in range(16):
        cmd[6 + i] = CMD.bData[i]
    for i in range(22): # Calculate checksum for the first 22 bytes
        Checksum += cmd[i]
    cmd[22] = Checksum & 0xFF             # Low byte of wCheckSum
    cmd[23] = (Checksum >> 8) & 0xFF      # High byte of wCheckSum
    #print("Sending command:", [hex(x) for x in cmd])
    #for i in range(24):
    #    ser.write(cmd[i])
    ser.write(cmd)
    #print(cmd)
    cmd = [0x00] * 24
    CMD = Cmd_Packet() #Reset the CMD packet
    return Rx_Cmd(timeout)

def Rx_CMD_Process(flag):
    checksum = 0
    RSP.wPrefix =rsp[0] + (rsp[1] << 8)
    RSP.bAddress = rsp[2]
    RSP.bCmd = rsp[3]
    RSP.bEncode = rsp[4]
    RSP.bDataLen = rsp[5]
    for i in range(16):
        RSP.bData[i] = rsp[6 + i]
    RSP.wCheckSum = rsp[22] | (rsp[23] << 8)


#*********************************************
#Function: Receive a command vai serial port
#Return: 
#   XG_ERR_SUCCESS : Received Successful
#   XG_ERR_DATA : Data error
#*********************************************
def Rx_Cmd(timeout = 3):
    start_time = time.time()
    global rsp
    while time.time() - start_time < timeout:
        try:
            if ser.inWaiting():
                rsp = ser.read(24)
                #print("Received response:", [hex(x) for x in rsp])
                if rsp[23] != 0x00 and rsp[22] !=0x00:
                    checksum = 0
                    Rx_CMD_Process(1)
                    for i in range(22): # Calculate checksum for the first 22 bytes
                        checksum += rsp[i]
                    #print("received checksum:",hex(checksum))
                    if checksum == RSP.wCheckSum:
                        #print("Checksum valid")
                        rsp = [0x00] * 24

                        return XG_ERR_SUCCESS
                    else:
                        print("Checksum error")
                        return XG_ERR_DATA
        except Exception as e:
            print("Error reading from serial port:", e)
            return XG_ERR_COM
    print("Error: Timeout waiting for response")
    return XG_ERR_TIME_OUT



#*********************************************
#Function: Connect to the device
#DevAddress: Device address, default is 0， generally required for multple devices
#Return:
#   XG_ERR_SUCCESS : Connected Successful
#   XG_ERR_FAIL : Connection Failed
#*********************************************

def ConnectDev(DevAddress = 0, Password = '00000000'):
    CMD.bCmd = XG_CMD_CONNECTION
    CMD.bAddress = DevAddress
    CMD.bDataLen = 0x08
    print("Connecting to device...")
    for i in range(16):
        if Password is not None and i < len(Password):
            CMD.bData[i] = ord(Password[i])
        else:
            CMD.bData[i] = 0x00
    ret= UartSendCmd()
    #ret = Rx_Cmd()
    #print(ret)
    if ret == XG_ERR_SUCCESS:
        if RSP.bData[0] == XG_ERR_SUCCESS:
            Devname = bytes(CMD.bData[1:15]).decode('ASCII').rstrip('\x00')
            print(f"Connected to device: {Devname}")
            return XG_ERR_SUCCESS
        else:
            print("Connection failed")
            return RSP.bData[1]
    return XG_ERR_FAIL

#*********************************************
#Function: Close the device connection
#Timeout: Timeout in ms
#Return:
#   XG_ERR_SUCCESS : Closed Successful
#   XG_ERR_FAIL : Close Failed
#*********************************************
def CloseConnectDev(DevAddress = 0):
    CMD.bCmd = XG_CMD_CLOSE_CONNECTION
    CMD.bAddress = DevAddress
    CMD.bDataLen = 0
    #gUartByte = 0  # Prepare to receive data
    ret = UartSendCmd()
    if ret == XG_ERR_SUCCESS:
        if RSP.bData[0] == XG_ERR_SUCCESS:
            print("Connection closed")
            return XG_ERR_SUCCESS
    return XG_ERR_FAIL

#*********************************************
#Function: Get the device setting
#Timeout: Timeout in ms
#Return:
#   XG_ERR_SUCCESS : Get Successful
#   XG_ERR_FAIL : Get Failed
#*********************************************
def GetDevSetting(DevAddress = 0):
    CMD.bCmd = XG_CMD_GET_SYSTEM_INFO
    CMD.bAddress = DevAddress
    CMD.bDataLen = 0
    ret = UartSendCmd()   
    #ret = Rx_Cmd()
    if ret == XG_ERR_SUCCESS:
        if RSP.bData[0] == XG_ERR_SUCCESS:
            DevVer = f"{RSP.bData[1]}.{RSP.bData[2]}"
            DevID = RSP.bData[3]
            DevBaud = RSP.bData[4]
            DevSecurity = RSP.bData[5]
            DevTimeout = RSP.bData[6]
            DevDupCheck = RSP.bData[7]
            DevSameFingerCheck = RSP.bData[8]
            print(f"Device Version: {DevVer}")
            print(f"Device ID: {DevID}")
            print(f"Device Baud Rate: {Baudrate[DevBaud]}")
            print(f"Device Security Level: {DevSecurity}")
            print(f"Device Timeout: {DevTimeout} seconds")
            print(f"Device Duplicate Check: {'Enabled' if DevDupCheck else 'Disabled'}")
            print(f"Device Same Finger Check: {'Enabled' if DevSameFingerCheck else 'Disabled'}")
            return XG_ERR_SUCCESS, RSP.bData
    else:
            return XG_ERR_FAIL, RSP.bData


#*********************************************
#Function: Restore factory settings
#DevAddress: The Device ID, default be 0
#Return:
#   XG_ERR_SUCCESS : Restore Successful
#   XG_ERR_FAIL : Restore Failed
#*********************************************
def SetDevFactory(DevAddress = 0):
    CMD.bCmd = XG_CMD_FACTORY_SETTING
    CMD.bAddress = DevAddress
    CMD.bDataLen = 0x00
    ret = UartSendCmd()
    if ret == XG_ERR_SUCCESS:
        if RSP.bData[0] == XG_ERR_SUCCESS:
            print("Device is restore to factory setting properly")
            return XG_ERR_SUCCESS
    return XG_ERR_FAIL

#*********************************************
#Function: Set device ID
#NDevAddress: The new Device ID you need to set (0 ~ 255)
#ODevAddress: The old Device ID, default be 0
#Timeout: Timeout in ms
#Return:
#   XG_ERR_SUCCESS : Restore Successful
#   XG_ERR_FAIL : Restore Failed
#*********************************************
def SetDevID(NDevAddress, ODevAddress = 0, Timeout = 0.2):
    CMD.bCmd = XG_CMD_SET_DEVICE_ID
    CMD.bAddress = ODevAddress
    CMD.bDataLen = 0x01
    if NDevAddress == ODevAddress:
        print("The new password is the same as old one, please try other ID")
    elif NDevAddress != 0 or ODevAddress != 0:
        CMD.bData[0] = NDevAddress
        ret = UartSendCmd()
        if ret == XG_ERR_SUCCESS:
            if RSP.bData[0] == XG_ERR_SUCCESS:
                print("The Device ID is set properly, you can use GetDevSetting(DevAddress) function with the new ID to check the device")
                return XG_ERR_SUCCESS
        else:
            return RSP.bData[1]
    return XG_ERR_FAIL

#*********************************************
#Function: Set baud rate
#Baud: Baud rate to be set, valid values are 0=9600, 1=19200, 2=38400, 3=57600, 4=115200
#DevAddress: The Device ID, default the 0
#Return:
#   XG_ERR_SUCCESS : Set Successful
#   XG_ERR_FAIL : Set Failed
def SetDevBaud(bBaud, DevAddress = 0):
    CMD.bCmd = XG_CMD_SET_BAUDRATE
    CMD.bAddress = DevAddress
    CMD.bDataLen = 0x01
    CMD.bData[0] = bBaud
    ret = UartSendCmd()
    if ret == XG_ERR_SUCCESS:
        if RSP.bData[0] == XG_ERR_SUCCESS:
            print("The baudrate is changed, please use the new baudrate for communicate")
            return XG_ERR_SUCCESS
    return XG_ERR_FAIL

#*********************************************
#Function: Set security level
#Security: Security level to be set, valid values are 0=low, 1=medium, 3=high
#DevAddress: Device ID, default 0
#Return:
#   XG_ERR_SUCCESS : Set Successful
#   XG_ERR_FAIL : Set Failed
#*********************************************
def SetDevSecurity(bSecurity, DevAddress = 0):
    CMD.bCmd = XG_CMD_SET_SECURITYLEVEL
    CMD.bAddress = DevAddress
    CMD.bDataLen = 0x01
    CMD.bData[0] = bSecurity
    if bSecurity != 0 and bSecurity != 1 and bSecurity != 2:
        print("Wrong Security number, it should be 0 or 1 or 3, please reset again")
        return XG_ERR_FAIL
    ret = UartSendCmd()
    if ret == XG_ERR_SUCCESS:
        if RSP.bData[0] == XG_ERR_SUCCESS:
            print("The Security level is set to:", bSecurity)
            return XG_ERR_SUCCESS
    return XG_ERR_FAIL

#*********************************************
#Function: Set timeout duration for finger detection
#DevAddress: Device ID, default 0
#Timeout: Timeout duration to be set in seconds (1-255) 
#Return:
#   XG_ERR_SUCCESS : Set Successful
#   XG_ERR_FAIL : Set Failed
#*********************************************
def SetDevCheckFingerTimeout(bTimeout, DevAddress = 0):
    CMD.bCmd = XG_CMD_SET_TIMEOUT
    CMD.bAddress = DevAddress
    CMD.bDataLen = 0x01
    CMD.bData[0] = bTimeout
    if bTimeout < 1 | bTimeout > 255 :
        print("The timeout value is wrong, should be in range of 1 ~ 255 (s)")
        return XG_ERR_FAIL
    ret = UartSendCmd()
    if ret == XG_ERR_SUCCESS:
        if RSP.bData[0] == XG_ERR_SUCCESS:
            print("The tiemout for finger detectioin is set to ", bTimeout)
            return XG_ERR_SUCCESS
    return XG_ERR_FAIL


#*********************************************
#Function: Set duplicate check
#DevAddress: Device ID, default 0
#DupCheck: Duplicate check setting, 0=disable, 1=enable
#Return:
#   XG_ERR_SUCCESS : Set Successful
#   XG_ERR_FAIL : Set Failed
#*********************************************
def SetDevDupCheck(bDupCheck, DevAddress = 0):
    CMD.bCmd = XG_CMD_SET_DUP_CHECK
    CMD.bAddress = DevAddress
    CMD.bDataLen = 0x01
    CMD.bData[0] = bDupCheck
    if bDupCheck != 0 and bDupCheck != 1: 
        print("Wrong value, please try again")
        return XG_ERR_FAIL
    ret = UartSendCmd()
    if ret == XG_ERR_SUCCESS:
        if RSP.bData[0] == XG_ERR_SUCCESS:
            return XG_ERR_SUCCESS
    return XG_ERR_FAIL


#*********************************************
#Function: Set same finger check
#DevAddress: Device ID, default 0
#SameFingerCheck: Same finger check setting, 0=disable, 1=enable
#Return:
#   XG_ERR_SUCCESS : Set Successful
#   XG_ERR_FAIL : Set Failed
#*********************************************
def SetDevSameFingerCheck(bSameFingerCheck, DevAddress = 0):
    CMD.bCmd = XG_CMD_SET_SAME_FV
    CMD.bAddress = DevAddress
    CMD.bDataLen = 0x01
    CMD.bData[0] = bSameFingerCheck
    if bSameFingerCheck != 0 and bSameFingerCheck != 1:
        print("Wrong value, please use correct value and test it again")
        return XG_ERR_FAIL
    ret = UartSendCmd()
    if ret == XG_ERR_SUCCESS:
        if RSP.bData[0] == XG_ERR_SUCCESS:
            print("The Same Finger check option is set")
            return XG_ERR_SUCCESS
    return XG_ERR_FAIL

#*********************************************
#Function:Modify the password
#DevAddress: Device ID, default 0
#Password: The password: 8 ~ 14 characters
#Return:
#   XG_ERR_SUCCESS : Modify Successful
#   XG_ERR_FAIL : Modify Failed
#*********************************************
def SET_Password(password, DevAddress = 0):
    CMD.bCmd = XG_CMD_SET_PASSWORD
    CMD.bAddress = DevAddress
    CMD.bDataLen = len(password)
    if CMD.bDataLen < 8 or CMD.bDataLen > 14 :
        print("Wrong password length, should be in range 8 ~ 14")
        return XG_ERR_FAIL
    for i in range (CMD.bDataLen):
        CMD.bData[i] = ord(password[i])
    ret = UartSendCmd()
    if ret == XG_ERR_SUCCESS:
        if RSP.bData[0] == XG_ERR_SUCCESS:
            print("The password is set successful, please use new password to open the device again")
            return XG_ERR_SUCCESS
    return XG_ERR_FAIL

#*********************************************
#Function:Check the password
#DevAddress: Device ID, default 0
#Password: The password: 8 ~ 14 characters
#Return:
#   XG_ERR_SUCCESS : Modify Successful
#   XG_ERR_FAIL : Modify Failed
#*********************************************
def Check_Password(password, DevAddress = 0):
    CMD.bCmd = XG_CMD_CHECK_PASSWORD
    CMD.bAddress = DevAddress
    CMD.bDataLen = len(password)
    if CMD.bDataLen < 8 or CMD.bDataLen > 14 :
        print("Wrong password length, should be in range 8 ~ 14")
        return XG_ERR_FAIL
    for i in range (CMD.bDataLen):
        CMD.bData[i] = ord(password[i])
    ret = UartSendCmd()
    if ret == XG_ERR_SUCCESS:
        if RSP.bData[0] == XG_ERR_SUCCESS:
            print("The password is check successful, please use new password to open the device again")
            return XG_ERR_SUCCESS
        else:
            print("The Password is wrong, please check it again")
            return XG_ERR_FAIL
    return XG_ERR_FAIL

#*********************************************
#Function: Reboot Device
#DevAddress: Device ID, default 0
#Return:
#   XG_ERR_SUCCESS : Reset Successful
#   XG_ERR_FAIL : Reset Failed
#*********************************************
def RebootDev(DevAddress = 0):
    CMD.bCmd = XG_CMD_REBOOT
    CMD.bAddress = DevAddress
    ret = UartSendCmd()
    if ret == XG_ERR_SUCCESS:
        if RSP.bData[0] == XG_ERR_SUCCESS:
            print("The Device reboot successfully")
            return XG_ERR_SUCCESS
    return XG_ERR_FAIL


#*********************************************
#Function: Check fingerprint status
#DevAddress: Device ID, default 0
#Return:
#   1 : Finger detected
#   0 : No finger detected or error
#*********************************************
def CheckFinger(DevAddress = 0):
    CMD.bCmd = XG_CMD_FINGER_STATUS
    CMD.bAddress = DevAddress
    print("Please Put you finger to the scanner in 3 seconds")
    time.sleep(3)
    ret = UartSendCmd()
    if ret == XG_ERR_SUCCESS:
        if RSP.bData[0] == XG_ERR_SUCCESS:
            if RSP.bData[1] == 1:
                print("Finger is detected properly")
            else:
                print("Finger isn't detected or do not put properly, please try it again")
            return RSP.bData[1]  # 1: finger detected, 0: no finger
    print("Faild to check finger status, please try it again")
    return 0

#*********************************************
#Function: Delete the certian User
#DevAddress: Device ID, default 0
#UserID: The ID of user going to be deleted
#Return:
#XG_ERR_SUCCESS: deleted successfully
#XG_ERR_FAIL: deleted fail
#XG_ERR_INVALID_ID : Invalid ID or empty ID
#*********************************************
def CleanUser(UserID, DevAddress = 0):
    CMD.bCmd = XG_CMD_CLEAR_ENROLL
    CMD.bAddress = DevAddress
    CMD.bDataLen = 0x04
    CMD.bData[0] = UserID & 0xFF
    CMD.bData[1] = (UserID >> 8) & 0xFF
    CMD.bData[2] = (UserID >> 16) & 0xFF
    CMD.bData[3] = (UserID >> 24) & 0xFF
    ret = UartSendCmd()
    if ret == XG_ERR_SUCCESS:
        if RSP.bData[0] == XG_ERR_SUCCESS:
            print("User is deleted successfully")
            return XG_ERR_SUCCESS
        elif RSP.bData[0] == XG_ERR_INVALID_ID or RSP.bData[0] == XG_ERR_EMPTY_ID:
            print("Invalid ID or the ID is not exist, please try again with correct ID")
            return XG_ERR_INVALID_ID
    print("Faild to Delected User")
    return XG_ERR_FAIL

#*********************************************
#Function: Delete all registered users
#DevAddress: Device ID, default 0
#Return:
#   XG_ERR_SUCCESS : Deletion Successful
#   XG_ERR_FAIL : Deletion Failed
#*********************************************
def CleanAllUser(DevAddress = 0):
    CMD.bCmd = XG_CMD_CLEAR_ALL_ENROLL
    CMD.bAddress = DevAddress
    ret = UartSendCmd(timeout = 5)
    if ret == XG_ERR_SUCCESS:
        if RSP.bData[0] == XG_ERR_SUCCESS:
            print("All User is cleaned")
    print("Fail to clear")
    return XG_ERR_FAIL


#*********************************************
#Function: Get empty ID, which is an unregistered ID
#DevAddress: Device ID, default 0
#StartID: The Start ID to check the empty ID that can be registered
#EndID: The End ID to check the empty ID that can be registered
#Return:
#   XG_ERR_SUCCESS : Get Successful
#   XG_ERR_FAIL : Get Failed
#   XG_ERR_NO_EMPTY_ID : No empty ID available
#*********************************************  
def GetEmptyID(StartID = 0, EndID = 100, DevAddress = 0):
    CMD.bCmd = XG_CMD_GET_EMPTY_ID
    CMD.bAddress = 0
    #CMD.bDataLen = 0x08
    CMD.bData[0] = StartID & 0xFF
    CMD.bData[1] = (StartID >> 8) & 0xFF
    CMD.bData[2] = (StartID >> 16) & 0xFF
    CMD.bData[3] = (StartID >> 24) & 0xFF
    CMD.bData[4] = EndID & 0xFF
    CMD.bData[5] = (EndID >> 8) & 0xFF
    CMD.bData[6] = (EndID >> 16) & 0xFF
    CMD.bData[7] = (EndID >> 24) & 0xFF
    ret = UartSendCmd()
    if ret == XG_ERR_SUCCESS:
        if RSP.bData[0] == XG_ERR_SUCCESS:
            pUserID = RSP.bData[1] + (RSP.bData[2] << 8) + (RSP.bData[2] << 16) + (RSP.bData[4] << 24)
            print("The Empty ID is ", pUserID)
            return pUserID
        elif RSP.bData[0] == XG_ERR_NO_NULL_ID:
            print("The database is fulled, has no empty ID")
            return XG_ERR_NO_NULL_ID
    print("Fail to get Empty ID")
    return XG_ERR_FAIL

#*********************************************
#Function：Verify user fingerprint and get the returned user ID
#DevAddress: Device ID, default 0
#UserID: Array to receive the verified user ID, if keep default the ID 0, 
#         it will verify in 1:N mode., otherwise, it verify in 1:1 mode
#Return:
#   XG_ERR_SUCCESS : Verification Successful
#   XG_ERR_FAIL : Verification Failed
#   XG_ERR_NO_USER : No such user
#*********************************************
def VerifyUser(UserID = 0, DevAddress = 0):
    ret, Data = GetDevSetting()
    CMD.bCmd = XG_CMD_VERIFY
    CMD.bAddress = DevAddress
    CMD.bDataLen = 0x04
    if ret == XG_ERR_SUCCESS:
        time_out = Data[6]
        print("timeout:", time_out)
    #if UserID is not None:
    CMD.bData[0] = UserID & 0xFF
    CMD.bData[1] = (UserID >> 8) & 0xFF
    CMD.bData[2] = (UserID >> 18) & 0xFF
    CMD.bData[3] = (UserID >> 24) & 0xFF 
    #CMD.bData[4] = Group_ID
    #CMD.bData[5] = Num #The number of ID to continue verify
    print("Please put your finger to the scanner to verify")
    ret = UartSendCmd(time_out)
    while True:
        if ret == XG_ERR_SUCCESS:
            if RSP.bData[0] == XG_ERR_SUCCESS:
                pID = RSP.bData[1] + (RSP.bData[2] << 8) + (RSP.bData[3] << 16) + (RSP.bData[3] << 24)
                print("The User: %d is detected" % (pID))
                return XG_ERR_SUCCESS
            elif RSP.bData[0] == XG_INPUT_FINGER:
                print("Please put your finger")
            elif RSP.bData[0] == XG_RELEASE_FINGER:
                print("Please release your finger") 
            else:
                if RSP.bData[1] == XG_ERR_NO_VEIN:
                    print("No finger vein detected, please try again")
                else:
                    print("Faild to Verify finger.")
                    break
        else:
            print("Verification error:", RSP.bData[1])
            return XG_ERR_FAIL
        ret = Rx_Cmd(time_out)

#*********************************************
#Function: Register a new user fingerprint
#DevAddress: Device ID, default 0
#UserID: User ID to be registered
#Return:
#   XG_ERR_SUCCESS : Registration Successful
#   XG_ERR_FAIL : Registration Failed
#   XG_ERR_USER_EXIST : User ID already exists
#   XG_ERR_DUPLICATION_ID: Duplicate ID
#   XG_ERR_NO_SAME_FINGER: The finger is not the same
#   XG_ERR_NO_VEIN: No finger is detected
#*********************************************
def EnrollUser(UserID, DevAddress = 0, Group_ID = 1, Temp_Num = 3):
    CMD.bCmd = XG_CMD_ENROLL
    CMD.bAddress = DevAddress
    CMD.bDataLen = 0x04
    CMD.bData[0] = UserID & 0xFF
    CMD.bData[1] = (UserID >> 8) & 0xFF
    CMD.bData[2] = (UserID >> 16) & 0xFF
    CMD.bData[3] = (UserID >> 24) & 0xFF
    CMD.bData[4] = Group_ID
    CMD.bData[5] = Temp_Num #Number of successful collections, as long as 3 successful collections are registered successfully.
    ret = UartSendCmd(timeout = 6)
    while True:
        if ret != XG_ERR_SUCCESS:
            print("RegUser RecvPack error:", ret)
            break
        if RSP.bData[0] == XG_ERR_SUCCESS:
            print("Registration successful")
            break
        elif RSP.bData[0] == XG_INPUT_FINGER:
            print ("Please place your finger again")
            ret = Rx_Cmd()
        elif RSP.bData[0] == XG_RELEASE_FINGER:
            print("Please release your finger")
            ret = Rx_Cmd()
        else:
            ret = RSP.bData[1]
            if ret == XG_ERR_INVALID_ID:
                print("Invalid User ID")
                break
            elif ret == XG_ERR_NOT_ENOUGH:
                print("The memory if full, please delete some users")
                break
            elif ret == XG_ERR_TIME_OUT:
                print("Operation timeout, please try again")
                break
            elif ret == XG_ERR_DUPLICATION_ID:
                print("Duplicate User ID")
                break
            elif ret == XG_ERR_NO_SAME_FINGER:
                print("The finger is not the same as the previous one, please try again")
                break
            elif ret == XG_ERR_NO_VEIN:
                print("No finger vein detected, please try again")
            else:
                print("Registration error:", ret)
            break
    return ret

#*********************************************
#Function: Get registered information
#DevAddress: Device ID, default 0
#pUserNum: Array to receive the number of registered users
#pUserMax: Maximum number of users that can be registered
#Return:
#   XG_ERR_SUCCESS : Get Successful
#   XG_ERR_FAIL : Get Failed
#*********************************************
def GetEnrollInfo(DevAddress = 0):
    CMD.bCmd = XG_CMD_GET_ENROLL_INFO
    CMD.bAddress = DevAddress
    ret = UartSendCmd()
    if ret == XG_ERR_SUCCESS:
        if RSP.bData[0] == XG_ERR_SUCCESS:
            pUserNum = RSP.bData[1] + (RSP.bData[2] << 8) + (RSP.bData[2] << 16) + (RSP.bData[3] << 24)
            pUserMax = RSP.bData[9] + (RSP.bData[10] << 8) + (RSP.bData[11] << 16) + (RSP.bData[12] << 24)
            print("The registed users:", pUserNum, "The maximum users:", pUserMax)
            return XG_ERR_SUCCESS
    print("Fail to get informatiom")
    return XG_ERR_FAIL

#*********************************************
#Function: Get registration information for a specified user ID
#DevAddress: Device ID, default 0
#UserID: User ID to query
#Return:
#XG_ERR_SUCCESS: The user information is get successfully
#XG_ERR_INVALID_ID: The user ID is invalid
#XG_ERR_FAIL: Fail to get user information
#*********************************************
def GetIDEnroll(UserID, DevAddress = 0):
    CMD.bCmd = XG_CMD_GET_EMPTY_ID
    CMD.bDataLen = 0x04
    CMD.bData[0] = UserID & 0xFF
    CMD.bData[1] = (UserID >> 8) & 0xFF
    CMD.bData[2] = (UserID >> 16) & 0xFF
    CMD.bData[3] = (UserID >> 24) & 0xFF
    ret = UartSendCmd()
    if ret == XG_ERR_SUCCESS:
        if RSP.bData[0] == XG_ERR_SUCCESS:
            template_num = RSP.bData[1]
            print("The ID exist with %d template" % (template_num))
            return XG_ERR_SUCCESS
        elif RSP.bData[0] == XG_ERR_INVALID_ID:
            print("Invalid ID")
            return XG_ERR_INVALID_ID
    return XG_ERR_FAIL


def main():
    # Testing Connection
    print("Testing device connection...")
    ConnectDev(Password=Devpassword)
    time.sleep(1)   
    GetDevSetting()
    #SetDevID(1,0)
    #GetDevSetting()
    #SetDevFactory()
    #SetDevBaud(4)
    #SetDevSecurity(1)
    #SetDevCheckFingerTimeout(7)
    #SetDevDupCheck(0)
    #SetDevSameFingerCheck(0)
    #GetEnrollInfo()
    #GetIDEnroll(1)
    #GetEmptyID()
    #EnrollUser(GetEmptyID())
    #VerifyUser()
    #CleanAllUser()
    #RebootDev()
    #CheckFinger()
    #GetDevSetting()
    CloseConnectDev()
    #time.sleep(2)
if __name__ == "__main__":
    main()