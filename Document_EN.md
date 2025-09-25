# Introduction  
This file introduces the functions in `main.py` and their corresponding parameters.  

# Functions  

## Send Command Packet  
`  
def UartSendCmd(timeout = 3)  
`  
* Function:  
  Send a command packet via the serial port. Pass the CMD data into the `cmd` array and send it through the serial port.  
* Parameters:  
  timeout: Set the timeout for reading the return information from the serial port, in seconds. Default is 3 seconds.  
* Return:  
  Calls the `Rx_Cmd()` function and returns its result. Refer to the `Rx_Cmd()` function description for details.  
* Example:  
  `ret = UARTSendCmd(4)` or `ret = UARTSendCmd()`  

## Process Return Data  
`  
def Rx_CMD_Process(flag)  
`  
* Function:  
  Process the data packet returned by the serial port. Pass the received data into `RSP` and calculate the checksum.  
* Parameters:  
  flag: Reserved, not actually used. Set it to 1 directly.  
* Return:  
  None  
* Example:  
  `Rx_CMD_Process(1)`  

## Receive Return Data  
`  
def Rx_Cmd(timeout = 3)  
`  
* Function:  
  Read the return information from the serial port and check the checksum.  
* Parameters:  
  timeout: Timeout duration, default is 3 seconds.  
* Return:  
  - `XG_ERR_SUCCESS`: Read successfully.  
  - `XG_ERR_DATA`: Data checksum error.  
  - `XG_ERR_TIME_OUT`: Read timeout.  
  - `XG_ERR_COM`: Serial port error.  
* Example:  
  `ret = Rx_Cmd(3)` or `ret = Rx_Cmd()`  

## Open Device Connection  
`  
def ConnectDev(DevAddress = 0, Password = '00000000')  
`  
* Function:  
  Connect to the device.  
* Parameters:  
  - `DevAddress`: Device ID, default is 0. Specify the device ID when connecting multiple devices.  
  - `Password`: Device password, default is `'00000000'`. Reserved for future use.  
* Return:  
  - `XG_ERR_SUCCESS`: Connection successful.  
  - `XG_ERR_FAIL`: Connection failed.  
* Example:  
  `ret = ConnectDev(DevAddress = 0, Password = '00000000')` or `ret = ConnectDev()`  

## Close Device Connection  
`  
def CloseConnectDev(DevAddress = 0)  
`  
* Function:  
  Close the device connection.  
* Parameters:  
  - `DevAddress`: Device ID, default is 0. Specify the device ID when connecting multiple devices.  
* Return:  
  - `XG_ERR_SUCCESS`: Close successful.  
  - `XG_ERR_FAIL`: Close failed.  
* Example:  
  `ret = CloseConnectDev(DevAddress = 0)` or `ret = CloseConnectDev()`  

## Get Device Settings  
`  
def GetDevSetting(DevAddress = 0)  
`  
* Function:  
  Get the current settings of the device.  
* Parameters:  
  - `DevAddress`: Device ID, default is 0. Specify the device ID when connecting multiple devices.  
* Return:  
  - `XG_ERR_SUCCESS`: Successfully retrieved settings.  
  - `XG_ERR_FAIL`: Failed to retrieve settings.  
  - `RSP.bData`: Returned information. Refer to the `RSP` data packet structure in the program for details.  
* Example:  
  `ret, array = GetDevSetting(DevAddress = 0)` or `ret, array = GetDevSetting()`  

## Restore Factory Settings  
`  
def SetDevFactory(DevAddress = 0)  
`  
* Function:  
  Restore the device to factory settings.  
* Parameters:  
  - `DevAddress`: Device ID, default is 0. Specify the device ID when connecting multiple devices.  
* Return:  
  - `XG_ERR_SUCCESS`: Successfully restored factory settings.  
  - `XG_ERR_FAIL`: Failed to restore factory settings.  
* Example:  
  `ret = SetDevFactory(DevAddress = 0)` or `ret = SetDevFactory()`  

## Set Device ID  
`  
def SetDevID(NDevAddress, ODevAddress = 0, Timeout = 0.2):  
`  
* Function:  
  Set the device ID.  
* Parameters:  
  - `NDevAddress`: New device ID, range 1 ~ 255.  
  - `ODevAddress`: Old device ID, default is 0. Specify the device ID when connecting multiple devices.  
  - `Timeout`: Reserved.  
* Return:  
  - `XG_ERR_SUCCESS`: Successfully set the device ID.  
  - `XG_ERR_FAIL`: Failed to set the device ID.  
* Example:  
  `ret = SetDevID(NDevAddress = 1, ODevAddress = 0)` or `ret = SetDevID(1)`  

## Set Serial Port Baud Rate  
`  
def SetDevBaud(bBaud, DevAddress = 0)  
`  
* Function:  
  Set the serial port baud rate of the device.  
* Parameters:  
  - `bBaud`: Baud rate setting. 0=9600, 1=19200, 2=38400, 3=57600, 4=115200.  
  - `DevAddress`: Device ID, default is 0. Specify the device ID when connecting multiple devices.  
* Return:  
  - `XG_ERR_SUCCESS`: Successfully set the baud rate.  
  - `XG_ERR_FAIL`: Failed to set the baud rate.  
* Example:  
  `ret = SetDevBaud(bBaud = 1, DevAddress = 0)` or `ret = SetDevBaud(1)`  

## Set Security Level  
`  
def SetDevSecurity(bSecurity, DevAddress = 0)  
`  
* Function:  
  Set the security level of the device.  
* Parameters:  
  - `bSecurity`: Security level. 0, 1, 3. The higher the value, the stricter the comparison, and the higher the false rejection rate.  
  - `DevAddress`: Device ID, default is 0. Specify the device ID when connecting multiple devices.  
* Return:  
  - `XG_ERR_SUCCESS`: Successfully set the security level.  
  - `XG_ERR_FAIL`: Failed to set the security level.  
* Example:  
  `ret = SetDevSecurity(bSecurity = 1, DevAddress = 0)` or `ret = SetDevSecurity(1)`  

## Set Finger Vein Input Timeout  
`  
def SetDevCheckFingerTimeout(bTimeout, DevAddress = 0)  
`  
* Function:  
  Set the timeout for waiting for finger vein input, range 1 ~ 255 (seconds).  
* Parameters:  
  - `bTimeout`: Timeout duration.  
  - `DevAddress`: Device ID, default is 0. Specify the device ID when connecting multiple devices.  
* Return:  
  - `XG_ERR_SUCCESS`: Successfully set the timeout.  
  - `XG_ERR_FAIL`: Failed to set the timeout.  
* Example:  
  `ret = SetDevCheckFingerTimeout(bTimeout = 7, DevAddress = 0)` or `ret = SetDevCheckFingerTimeout(7)`  

## Set Duplicate Registration Check  
`  
def SetDevDupCheck(bDupCheck, DevAddress = 0)  
`  
* Function:  
  Enable or disable duplicate user registration checks.  
* Parameters:  
  - `bDupCheck`: 1: Enable check, 0: Disable check.  
  - `DevAddress`: Device ID, default is 0. Specify the device ID when connecting multiple devices.  
* Return:  
  - `XG_ERR_SUCCESS`: Successfully set the check.  
  - `XG_ERR_FAIL`: Failed to set the check.  
* Example:  
  `ret = SetDevDupCheck(bDupCheck = 1, DevAddress = 0)` or `ret = SetDevDupCheck(1)`  

## Set Same Finger Registration Check  
`  
def SetDevSameFingerCheck(bSameFingerCheck, DevAddress = 0)  
`  
* Function:  
  Enable or disable the check for registering the same finger.  
* Parameters:  
  - `bSameFingerCheck`: 1: Enable check, 0: Disable check.  
  - `DevAddress`: Device ID, default is 0. Specify the device ID when connecting multiple devices.  
* Return:  
  - `XG_ERR_SUCCESS`: Successfully set the check.  
  - `XG_ERR_FAIL`: Failed to set the check.  
* Example:  
  `ret = SetDevSameFingerCheck(bSameFingerCheck = 1, DevAddress = 0)` or `ret = SetDevSameFingerCheck(1)`  

## Set Device Password  
`  
def SET_Password(password, DevAddress = 0)  
`  
Reserved function. Use with caution.  

## Check Device Password  
`  
def Check_Password(password, DevAddress = 0)  
`  
Reserved function. Use with caution.  

## Reboot Device  
`  
def RebootDev(DevAddress = 0)  
`  
* Function:  
  Reboot the device.  
* Parameters:  
  - `DevAddress`: Device ID, default is 0. Specify the device ID when connecting multiple devices.  
* Return:  
  - `XG_ERR_SUCCESS`: Successfully rebooted.  
  - `XG_ERR_FAIL`: Failed to reboot.  
* Example:  
  `ret = RebootDev(DevAddress = 0)` or `ret = RebootDev(1)`  

## Delete Specified User  
`  
def CleanUser(UserID, DevAddress = 0)  
`  
* Function:  
  Delete the vein information of the specified user ID.  
* Parameters:  
  - `UserID`: User ID.  
  - `DevAddress`: Device ID, default is 0. Specify the device ID when connecting multiple devices.  
* Return:  
  - `XG_ERR_SUCCESS`: Successfully deleted the user.  
  - `XG_ERR_FAIL`: Failed to delete the user.  
  - `XG_ERR_INVALID_ID`: Invalid ID or the user ID does not exist.  
* Example:  
  `ret = CleanUser(UserID = 1, DevAddress = 0)` or `ret = CleanUser(1)`  

## Delete All Users  
`  
def CleanAllUser(DevAddress = 0)  
`  
* Function:  
  Delete the vein information of all users.  
* Parameters:  
  - `DevAddress`: Device ID, default is 0. Specify the device ID when connecting multiple devices.  
* Return:  
  - `XG_ERR_SUCCESS`: Successfully deleted all users.  
  - `XG_ERR_FAIL`: Failed to delete all users.  
* Example:  
  `ret = CleanAllUser(DevAddress = 0)` or `ret = CleanAllUser()`  

## Get Available User ID  
`  
def GetEmptyID(StartID = 0, EndID = 100, DevAddress = 0)  
`  
* Function:  
  Get an available user ID for registration and return the smallest available user ID.  
* Parameters:  
  - `StartID`: Starting ID, default is 0.  
  - `EndID`: Ending ID, default is 100.  
  - `DevAddress`: Device ID, default is 0. Specify the device ID when connecting multiple devices.  
* Return:  
  - `XG_ERR_FAIL`: Failed to get an empty ID.  
  - `XG_NO_NULL_ID`: The database is full, no available ID.  
  - `pUserID`: The smallest available empty ID, returned only when the operation is successful.  
* Example:  
  `ret = GetEmptyID(StartID = 10, EndID = 200, DevAddress = 0)` or `ret = GetEmptyID()`  

## Verify User Finger Vein  
`  
def VerifyUser(UserID = 0, DevAddress = 0)  
`  
* Function:  
  Verify the current finger vein.  
* Parameters:  
  - `UserID`: The user ID to verify. If the default is 0, use 1:N verification. If `ID > 0`, use 1:1 verification with the specified ID.  
  - `DevAddress`: Device ID, default is 0. Specify the device ID when connecting multiple devices.  
* Return:  
  - `XG_ERR_SUCCESS`: Successfully verified the user.  
  - `XG_ERR_FAIL`: Failed to verify the user.  
  - `XG_ERR_NO_VEIN`: The user has not been registered.  
  - `pID`: The user ID of the successfully verified user, printed only when verification is successful.  
* Example:  
  `ret = VerifyUser(UserID = 0, DevAddress = 0)` or `ret = VerifyUser()`  

## Enroll User  
`  
def EnrollUser(UserID, DevAddress = 0, Group_ID = 1, Temp_Num = 3)  
`  
* Function:  
  Enroll a user with the specified ID.  
* Parameters:  
  - `UserID`: The user ID to enroll.  
  - `DevAddress`: Device ID, default is 0. Specify the device ID when connecting multiple devices.  
  - `Group_ID`: Reserved parameter.  
  - `Temp_Num`: Reserved parameter.  
* Return:  
  - `XG_ERR_SUCCESS`: Successfully enrolled the user.  
  - `XG_ERR_FAIL`: Failed to enroll the user.  
  - `XG_ERR_INVALID_ID`: The user ID is not valid.  
  - `XG_ERR_NOT_ENOUGH`: The database is full.  
  - `XG_ERR_TIME_OUT`: Enrollment timed out.  
  - `XG_ERR_DUPLICATION_ID`: The user ID already exists.  
  - `XG_ERR_NO_SAME_FINGER`: The finger information already exists.  
  - `XG_ERR_NO_VEIN`: No finger detected.  
* Example:  
  `ret = EnrollUser(UserID = 1, DevAddress = 0)` or `ret = EnrollUser(1)`  

## Query the Number of Enrolled Users  
`  
def GetEnrollInfo(DevAddress = 0)  
`  
* Function:  
  Query the number of users in the database.  
* Parameters:  
  - `DevAddress`: Device ID, default is 0. Specify the device ID when connecting multiple devices.  
* Return:  
  - `XG_ERR_SUCCESS`: Successfully retrieved the data.  
  - `XG_ERR_FAIL`: Failed to retrieve the data.  
  - `pUserNum`: The number of enrolled users.  
  - `pUserMax`: The module capacity, the total number of users supported.  
* Example:  
  `ret = GetEnrollInfo(DevAddress = 0)` or `ret = GetEnrollInfo()`  

## Query Template Information of a Specific User  
`  
def GetIDEnroll(UserID, DevAddress = 0)  
`  
* Function:  
  Query the information of a specific user.  
* Parameters:  
  - `UserID`: The user ID to query.  
  - `DevAddress`: Device ID, default is 0. Specify the device ID when connecting multiple devices.  
* Return:  
  - `XG_ERR_SUCCESS`: Successfully retrieved the user data.  
  - `XG_ERR_FAIL`: Failed to retrieve the user data.  
  - `template_num`: The number of templates for the user.  
* Example:  
  `ret = GetIDEnroll(UserID = 1, DevAddress = 0)` or `ret = GetIDEnroll(1)`  