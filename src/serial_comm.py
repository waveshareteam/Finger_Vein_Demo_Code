class SerialComm:
    def __init__(self, port, baudrate=9600):
        self.port = port
        self.baudrate = baudrate
        self.serial = None

    def open_connection(self):
        import serial
        try:
            self.serial = serial.Serial(self.port, self.baudrate)
            print(f"Connection opened on {self.port} at {self.baudrate} baud.")
        except serial.SerialException as e:
            print(f"Error opening serial port: {e}")

    def send_data(self, data):
        if self.serial and self.serial.is_open:
            try:
                self.serial.write(data.encode())
                print(f"Data sent: {data}")
            except Exception as e:
                print(f"Error sending data: {e}")
        else:
            print("Serial port is not open.")

    def receive_data(self):
        if self.serial and self.serial.is_open:
            try:
                data = self.serial.readline().decode().strip()
                print(f"Data received: {data}")
                return data
            except Exception as e:
                print(f"Error receiving data: {e}")
        else:
            print("Serial port is not open.")

    def close_connection(self):
        if self.serial and self.serial.is_open:
            self.serial.close()
            print("Connection closed.")