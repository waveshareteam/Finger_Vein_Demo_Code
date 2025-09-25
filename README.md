# 中文
## 支持主板
### 树莓派 
#### 关闭调试串口，并开启硬件串口
`
sudo raspi-config
`
选择Inteface Options -> Serial port , 保持Login shell disabled 和hardware serail enable

### RDK 主板
串口已经默认开启，不需要操作配置

## 安装serial库
`
sudo apt-get -y install python3-serial
sudo apt-get -y install python-serial
`
## 下载程序
`
git clone https://github.com/waveshareteam/Finger_Vein_Demo_Code
`
## 运行程序
`
cd Finger_Vein_Demo_Code/
sudo python3 main.py
`
## 文件结构说明
main.py: 主文件。 包含所有测试函数。 用户可以在main（）中根据自己的测试需求，调用函数测试模组
serial_comm.py: 串口调用函数，根据系统信息，自动获取串口接口，用户不需要操作

# English
## Supported Board
### Raspberry Pi
#### Setup
`
sudo raspi-config
`
Select Inteface Options -> Serial port, Make sure that Login shell disabled and hardware serail enable

### RDK Board
Serial port is enabled by default, do not need to operated

## Install serial libraries
`
sudo apt-get -y install python3-serial
sudo apt-get -y install python-serial
`
## Download Examples
`
git clone https://github.com/waveshareteam/Finger_Vein_Demo_Code
`
## Run the code
`
cd Finger_Vein_Demo_Code/
sudo python3 main.py
`
## File structure
main.py: Main file that includes all the functions for testing finger vein module, You can call the functions in main() to test the module.
serial_comm.py: Serial function, it will set the realted com port according to the board information. User do not need to operate it.