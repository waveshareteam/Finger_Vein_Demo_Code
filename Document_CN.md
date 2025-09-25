# 简介
这个文件是介绍main.py中的函数和对应的参数
# 函数
## 发送指令包
`
def UartSendCmd(timeout = 3)
`
* 功能：
  串口发送指令包, 将CMD的数据传入cmd数组，并通过串口发送
* 参数：
  time_out: 设置串口读取返回信息的超时间，单位是s， 默认为3秒
* 返回：
  调用Rx_Cmd()函数并返回，具体参考Rx_Cmd()函数说明
* 调用参考
  `ret = UARTSendCmd(4)` 或者 ` ret = UARTSendCmd()`

## 处理返回数据
`
def Rx_CMD_Process(flag)
`
* 功能：
  处理串口返回的数据包， 将串口接收的数据传入RSP中，并计算checksum
* 参数
  flag: 预留，没有实际使用，直接置1即可
* 返回：
  空
* 调用参考
  `Rx_CMD_Process(1)`
##接收返回数据
`
def Rx_Cmd(timeout = 3)
`
* 功能：读取串口返回信息，并检查校验码
* 参数：
  timeout: 超时时间，默认3s
* 返回：
  XG_ERR_SUCCESS: 读取成功
  XG_ERR_DATA: 数据校验错误
  XG_ERR_TIME_OUT：读取超时
  XG_ERR_COM：串口错误
* 调用参考：
  `ret = Rx_Cmd(3) ` 或者 `ret = Rx_Cmd() `

## 打开设备连接
`
def ConnectDev(DevAddress = 0, Password = '00000000')
`
* 功能：连接设备
* 参数：
  DevAddress: 设备ID， 默认为0, 多设备连接的时候需要指定设备ID
  Password：设备密码，默认为'00000000', 预留功能
* 返回：
  XG_ERR_SUCCESS: 连接成功
  XG_ERR_FAIL: 连接失败
* 调用参考：
  `ret = ConnectDev(DevAddress = 0, Password = '00000000')` 或者 `ret = ConnectDev()`

## 关闭设备连接
`
def CloseConnectDev(DevAddress = 0)
`
* 功能：关闭设备
* 参数：
  DevAddress: 设备ID， 默认为0, 多设备连接的时候需要指定设备ID
* 返回：
  XG_ERR_SUCCESS: 关闭成功
  XG_ERR_FAIL: 关闭失败
* 调用参考
  `ret = CloseConnectDev(DevAddress = 0)` 或者 `ret = CloseConnectDev()`

## 获取设备设置信息
`
def GetDevSetting(DevAddress = 0)
`
* 功能：获取设备当前设置信息
* 参数：
  DevAddress: 设备ID， 默认为0, 多设备连接的时候需要指定设备ID
* 返回：
  XG_ERR_SUCCESS: 获取信息成功
  XG_ERR_FAIL: 获取信息失败
  RSP.bData: 返回信息， 具体参考程序中RSP数据包结构
* 调用参考
  `ret, array = GetDevSetting(DevAddress = 0)` 或者 `ret, array = GetDevSetting()`

## 恢复出厂设置
`
def SetDevFactory(DevAddress = 0)
`
* 功能：将设备恢复到出厂设置
* 参数：
  DevAddress: 设备ID， 默认为0, 多设备连接的时候需要指定设备ID
* 返回：
  XG_ERR_SUCCESS: 恢复出厂设置成功
  XG_ERR_FAIL:恢复出厂设置失败
* 调用参考
  `ret = SetDevFactory(DevAddress = 0)` 或者 `ret = SetDevFactory()`

## 设置设备ID
`
def SetDevID(NDevAddress, ODevAddress = 0, Timeout = 0.2):
`
* 功能：设置设备的ID
* 参数：
  NDevAddress: 新设备ID，1 ~ 255 范围
  ODevAddress: 旧设备ID， 默认为0, 多设备连接的时候需要指定设备ID
  Tiemout: 预留
* 返回：
  XG_ERR_SUCCESS: 设置设备ID成功
  XG_ERR_FAIL:设置设备ID失败
* 调用参考
  `ret = SetDevID(NDevAddress = 1, ODevAddress = 0)` 或者 `ret = SetDevID(1)`

## 设置串口波特率
`
def SetDevBaud(bBaud, DevAddress = 0)
`
* 功能：设置设备的串口波特率
* 参数：
  bBaud: 波特率设置，0=9600, 1=19200, 2=38400, 3=57600, 4=115200
  DevAddress: 设备ID， 默认为0, 多设备连接的时候需要指定设备ID
* 返回：
  XG_ERR_SUCCESS: 设置串口波特率成功
  XG_ERR_FAIL:设置串口波特率失败
* 调用参考
  `ret = SetDevBaud(bBaud = 1, DevAddress = 0)` 或者 `ret = SetDevBaud(1)`

## 设置比对等级
`
def SetDevSecurity(bSecurity, DevAddress = 0)
`
* 功能：设置设备的比对等级
* 参数：
  bSecurity: 比对等级，0， 1， 3， 数值越高，比对越严格，拒真率越高
  DevAddress: 设备ID， 默认为0, 多设备连接的时候需要指定设备ID
* 返回：
  XG_ERR_SUCCESS: 设置等级成功
  XG_ERR_FAIL:设置等级失败
* 调用参考
  `ret = SetDevSecurity(bSecurity = 1, DevAddress = 0)` 或者 `ret = SetDevSecurity(1)`

## 设置等待静脉录入超时时间
`
def SetDevCheckFingerTimeout(bTimeout, DevAddress = 0)
`
* 功能：设置等待静脉录入的超时时间, 1 ~ 255 (s)
* 参数：
  bTimeout: 比对等级，0， 1， 3， 数值越高，比对越严格，拒真率越高
  DevAddress: 设备ID， 默认为0, 多设备连接的时候需要指定设备ID
* 返回：
  XG_ERR_SUCCESS: 设置成功
  XG_ERR_FAIL:设置失败
* 调用参考
  `ret = SetDevCheckFingerTimeout(bTimeout = 7, DevAddress = 0)` 或者 `ret = SetDevCheckFingerTimeout(7)`

## 设置重复登记检查
`
def SetDevDupCheck(bDupCheck, DevAddress = 0)
`
* 功能：设置是否开启重复用户录入的检查
* 参数：
  bDupCheck: 1： 开启检查， 0：关闭检查
  DevAddress: 设备ID， 默认为0, 多设备连接的时候需要指定设备ID
* 返回：
  XG_ERR_SUCCESS: 设置成功
  XG_ERR_FAIL:设置失败
* 调用参考
  `ret = SetDevDupCheck(bDupCheck = 1, DevAddress = 0)` 或者 `ret = SetDevDupCheck(1)`

## 设置相同手指录入检查
`
def SetDevSameFingerCheck(bSameFingerCheck, DevAddress = 0)
`
* 功能：设置是否开启重复手指录入的检查
* 参数：
  bSameFingerCheck: 1： 开启检查， 0：关闭检查
  DevAddress: 设备ID， 默认为0, 多设备连接的时候需要指定设备ID
* 返回：
  XG_ERR_SUCCESS: 设置成功
  XG_ERR_FAIL:设置失败
* 调用参考
  `ret = SetDevSameFingerCheck(bSameFingerCheck = 1, DevAddress = 0)` 或者 `ret = SetDevSameFingerCheck(1)`

## 设置设备密码
`
def SET_Password(password, DevAddress = 0)
`
预留功能，谨慎使用

## 检查设备密码
`
def Check_Password(password, DevAddress = 0)
`
预留功能，谨慎使用

## 重启设备
`
def RebootDev(DevAddress = 0)
`
* 功能：重启设备
* 参数：
  DevAddress: 设备ID， 默认为0, 多设备连接的时候需要指定设备ID
* 返回：
  XG_ERR_SUCCESS: 重启成功
  XG_ERR_FAIL:重启失败
* 调用参考
  `ret = RebootDev(DevAddress = 0)` 或者 `ret = RebootDev(1)`

## 检查手指放置状态
`
def CheckFinger(DevAddress = 0)
`
* 功能：检查手指放置状态
* 参数：
  DevAddress: 设备ID， 默认为0, 多设备连接的时候需要指定设备ID
* 返回：
  1: 手指检查成功
  0: 没有检测到手指，或者手指放置不正确
* 调用参考
  `ret = CheckFinger(DevAddress = 0)` 或者 `ret = CheckFinger(1)`

## 删除指定用户
`
def CleanUser(UserID, DevAddress = 0)
`
* 功能：删除指定用户ID的静脉信息
* 参数：
  UserID： 用户ID
  DevAddress: 设备ID， 默认为0, 多设备连接的时候需要指定设备ID
* 返回：
  XG_ERR_SUCCESS: 删除用户成功
  XG_ERR_FAIL:删除用户失败
  XG_ERR_INVALID_ID：ID不正确或者没有该用户ID
* 调用参考
  `ret = CleanUser(UserID = 1, DevAddress = 0)` 或者 `ret = CleanUser(1)`

## 删除所有用户
`
def CleanAllUser(DevAddress = 0)
`
* 功能：删除所有用户的静脉信息
* 参数：
  DevAddress: 设备ID， 默认为0, 多设备连接的时候需要指定设备ID
* 返回：
  XG_ERR_SUCCESS: 删除所有用户成功
  XG_ERR_FAIL:删除所有用户失败
* 调用参考
  `ret = CleanAllUser(DevAddress = 0)` 或者 `ret = CleanAllUser()`

## 获取可注册的用户ID
`
def GetEmptyID(StartID = 0, EndID = 100, DevAddress = 0)
`
* 功能：获取可用于注册的用户ID，返回最小可用的用户ID
* 参数：
  StartID: 开始的ID号， 默认为0
  EndID: 结束的ID号， 默认为100
  DevAddress: 设备ID， 默认为0, 多设备连接的时候需要指定设备ID
* 返回：
  XG_ERR_FAIL: 获取空ID失败
  XG_NO_NULL_ID：数据库已满，无可用ID号
  pUserID: 可用的最小空ID号，只有在获取成功情况下返回
* 调用参考
  `ret = GetEmptyID(StartID = 10, EndID = 200, DevAddress = 0)` 或者 `ret = GetEmptyID()`

## 比对用户静脉
`
def VerifyUser(UserID = 0, DevAddress = 0)
`
* 功能：比对当前指静脉
* 参数：
  UserID: 比对的用户ID，如果默认0，使用1：N比对， 如果ID>0, 使用指定ID 1:1比对
  DevAddress: 设备ID， 默认为0, 多设备连接的时候需要指定设备ID
* 返回：
  XG_ERR_SUCCESS: 比对用户成功
  XG_ERR_FAIL: 比对用户失败
  XG_ERR_NO_VEIN：用户未录入
  pID：比对成功的用户ID，仅有比对成功下会直接打印
* 调用参考
  `ret = VerifyUser(UserID = 0, DevAddress = 0)` 或者 `ret = VerifyUser()`

## 录入用户
`
def EnrollUser(UserID, DevAddress = 0, Group_ID = 1, Temp_Num = 3)
`
* 功能：使用指定ID，录入用户
* 参数：
  UserID: 需要录入的用户ID
  DevAddress: 设备ID， 默认为0, 多设备连接的时候需要指定设备ID
  Group_ID： 预留参数
  Temp_Num: 预留参数
* 返回：
  XG_ERR_SUCCESS: 录入用户成功
  XG_ERR_FAIL: 录入用户失败
  XG_ERR_INVALID_ID：用户ID不可用
  XG_ERR_NOT_ENOUGH： 数据库已满
  XG_ERR_TIME_OUT： 录入超时
  XG_ERR_DUPLICATION_ID： 用户ID已存在
  XG_ERR_NO_SAME_FINGER： 该手指信息已存在
  XG_ERR_NO_VEIN： 未检测到手指
* 调用参考
  `ret = EnrollUser(UserID = 1, DevAddress = 0)` 或者 `ret = EnrollUser(1)`

## 查询已录入的用户数量
`
def GetEnrollInfo(DevAddress = 0)
`
* 功能：查询数据库中的用户数量
* 参数：
  DevAddress: 设备ID， 默认为0, 多设备连接的时候需要指定设备ID
* 返回：
  XG_ERR_SUCCESS: 获取数据成功
  XG_ERR_FAIL: 获取数据失败
  pUserNum：已经录入的用户数量
  pUserMax： 模块容量，支持录入的总数量
* 调用参考
  `ret = GetEnrollInfo(DevAddress = 0)` 或者 `ret = GetEnrollInfo()`

## 查询指定用户的模板信息
`
def GetIDEnroll(UserID, DevAddress = 0)
`
* 功能：查询指定用户的信息
* 参数：
  UserID：查询的用户ID
  DevAddress: 设备ID， 默认为0, 多设备连接的时候需要指定设备ID
* 返回：
  XG_ERR_SUCCESS: 查询用户数据成功
  XG_ERR_FAIL: 查询用户数据失败
  template_num：该用户的模板数量
* 调用参考
  `ret = GetIDEnroll(UserID = 1, DevAddress = 0)` 或者 `ret = GetIDEnroll(1)`