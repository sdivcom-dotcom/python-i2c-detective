import os
import re
import subprocess
import pandas as pd

command_lsusb = "lsusb | grep 'Silicon Labs CP2112 HID I2C Bridge'"
command_find_i2c_line  = "i2cdetect -l | grep 'CP2112 SMBus Bridge'"
command_find_addr = "i2cdetect -r -y "


UnknownDevice = "Unknown Device"


#Device  Category  From  To Reg   ID
slovar = [
{'name': 'ADC122C04', 'description': 'Thermocouple Amplifier', 'col1': '0x40', 'col2': '0x4F', 'col3': '0x00', 'col4': '0x00'},
{'name': 'ADS1015', 'description': 'Analogue to Digital Converter', 'col1': '0x48', 'col2': '0x4B', 'col3': '0x00', 'col4': '0x00'},
{'name': 'ADS1113', 'description': 'Analogue to Digital Converter', 'col1': '0x48', 'col2': '0x4B', 'col3': '0x00', 'col4': '0x00'},
{'name': 'ADS1114', 'description': 'Analogue to Digital Converter', 'col1': '0x48', 'col2': '0x4B', 'col3': '0x00', 'col4': '0x00'},
{'name': 'ADS1115', 'description': 'Analogue to Digital Converter', 'col1': '0x48', 'col2': '0x4B', 'col3': '0x00', 'col4': '0x00'},
{'name': 'ADT7410', 'description': 'Temperature Sensor', 'col1': '0x48', 'col2': '0x4B', 'col3': '0x0B', 'col4': '0xCB'},
{'name': 'ADXL343', 'description': 'Accelerometer', 'col1': '0x53', 'col2': '0x1D', 'col3': '0x00', 'col4': '0xE5'},
{'name': 'ADXL345', 'description': 'Accelerometer', 'col1': '0x53', 'col2': '0x1D', 'col3': '0x00', 'col4': '0xE5'},
{'name': 'AHT20', 'description': 'Temperature Humidity Sensor', 'col1': '0x38', 'col2': '0x38', 'col3': '0x00', 'col4': '0x00'},
{'name': 'AM2315', 'description': 'Humidity Temperature Sensor', 'col1': '0x5C', 'col2': '0x5C', 'col3': '0x00', 'col4': '0x00'},
{'name': 'AM2320', 'description': 'Humidity Temperature Sensor', 'col1': '0x5C', 'col2': '0x5C', 'col3': '0x00', 'col4': '0x00'},
{'name': 'AMG8831', 'description': 'IRThermal Camera', 'col1': '0x68', 'col2': '0x69', 'col3': '0x00', 'col4': '0x00'},
{'name': 'AMG8833', 'description': 'IRThermal Camera', 'col1': '0x68', 'col2': '0x69', 'col3': '0x00', 'col4': '0x00'},
{'name': 'AS7265x', 'description': 'Triad Spectroscopy Sensor', 'col1': '0x49', 'col2': '0x49', 'col3': '0x00', 'col4': '0x00'},
{'name': 'AS7341', 'description': 'Light Colour Sensor', 'col1': '0x39', 'col2': '0x39', 'col3': '0x92', 'col4': '0x24'},
{'name': 'ATECC608', 'description': 'Cryptographic Device', 'col1': '0x60', 'col2': '0x60', 'col3': '0x00', 'col4': '0x00'},
{'name': 'BH1750', 'description': 'Light Sensor', 'col1': '0x5C', 'col2': '0x23', 'col3': '0x00', 'col4': '0x00'},
{'name': 'BMA180', 'description': 'Accelerometer', 'col1': '0x77', 'col2': '0x77', 'col3': '0x00', 'col4': '0x03'},
{'name': 'BME280', 'description': 'Temperature Pressure Humidity Sensor', 'col1': '0x76', 'col2': '0x77', 'col3': '0xD0', 'col4': '0x60'},
{'name': 'BME680', 'description': 'Temperature Pressure Humidity Gas Sensor', 'col1': '0x76', 'col2': '0x77', 'col3': '0xD0', 'col4': '0x61'},
{'name': 'BMI270', 'description': 'Accelerometer Gyroscope', 'col1': '0x68', 'col2': '0x69', 'col3': '0x00', 'col4': '0x24'},
{'name': 'BMP085', 'description': 'Temperature Pressure Sensor', 'col1': '0x77', 'col2': '0x77', 'col3': '0x00', 'col4': '0x00'},
{'name': 'BMP180', 'description': 'Temperature Pressure Sensor', 'col1': '0x77', 'col2': '0x77', 'col3': '0xD0', 'col4': '0x55'},
{'name': 'BMP280', 'description': 'Temperature Pressure Sensor', 'col1': '0x76', 'col2': '0x77', 'col3': '0xD0', 'col4': '0x58'},
{'name': 'BMP388', 'description': 'Pressure Sensor', 'col1': '0x76', 'col2': '0x77', 'col3': '0x00', 'col4': '0x50'},
{'name': 'BMP390', 'description': 'Pressure Sensor', 'col1': '0x76', 'col2': '0x77', 'col3': '0x00', 'col4': '0x60'},
{'name': 'BNO055', 'description': 'Accelerometer Gyroscope Magnetometer', 'col1': '0x28', 'col2': '0x29', 'col3': '0x00', 'col4': '0xA0'},
{'name': 'CAP1188', 'description': 'CapacitiveTouchSensor', 'col1': '0x28', 'col2': '0x2D', 'col3': '0xFD', 'col4': '0x50'},
{'name': 'CCS811', 'description': 'VOC Sensor', 'col1': '0x5A', 'col2': '0x5B', 'col3': '0x20', 'col4': '0x81'},
{'name': 'DHT12', 'description': 'Humidity Temperature Sensor', 'col1': '0x5C', 'col2': '0x5C', 'col3': '0x00', 'col4': '0x00'},
{'name': 'DPS310', 'description': 'Pressure Sensor', 'col1': '0x76', 'col2': '0x77', 'col3': '0x0D', 'col4': '0x10'},
{'name': 'DRV2605', 'description': 'Motor Driver', 'col1': '0x5A', 'col2': '0x5A', 'col3': '0x00', 'col4': '0x60'},
{'name': 'DS1307', 'description': 'Real Time Clock', 'col1': '0x68', 'col2': '0x68', 'col3': '0x00', 'col4': '0x00'},
{'name': 'DS1841', 'description': 'Digital Potentiometer', 'col1': '0x28', 'col2': '0x2B', 'col3': '0x03', 'col4': '0x03'},
{'name': 'DS3231', 'description': 'Real Time Clock', 'col1': '0x68', 'col2': '0x68', 'col3': '0x00', 'col4': '0x00'},
{'name': 'DS3502', 'description': 'Digital Potentiometer', 'col1': '0x28', 'col2': '0x2B', 'col3': '0x00', 'col4': '0x40'},
{'name': 'EMC2101', 'description': 'Fan Controller', 'col1': '0x4C', 'col2': '0x4C', 'col3': '0x00', 'col4': '0x00'},
{'name': 'FT6x06', 'description': 'Capacitive Touch Sensor', 'col1': '0x38', 'col2': '0x38', 'col3': '0x00', 'col4': '0x00'},
{'name': 'FXAS21001', 'description': 'Gyroscope', 'col1': '0x20', 'col2': '0x21', 'col3': '0x00', 'col4': '0x00'},
{'name': 'FXOS8700', 'description': 'Accelerometer Magnetometer', 'col1': '0x1C', 'col2': '0x1F', 'col3': '0x0D', 'col4': '0xC7'},
{'name': 'H3LIS331DL', 'description': 'Accelerometer', 'col1': '0x18', 'col2': '0x19', 'col3': '0x0F', 'col4': '0x32'},
{'name': 'HDC1008', 'description': 'Temperature Humidity Sensor', 'col1': '0x40', 'col2': '0x43', 'col3': '0x02', 'col4': '0x10'},
{'name': 'HDC1008', 'description': 'Humidity Temperature Sensor', 'col1': '0x40', 'col2': '0x43', 'col3': '0x00', 'col4': '0x00'},
{'name': 'HMC5883', 'description': 'Magnetometer', 'col1': '0x1E', 'col2': '0x1E', 'col3': '0x0A', 'col4': '0x48'},
{'name': 'HT16K33', 'description': 'LED Matrix Driver', 'col1': '0x70', 'col2': '0x77', 'col3': '0x00', 'col4': '0x00'},
{'name': 'HTS221', 'description': 'Temperature Humidity Sensor', 'col1': '0x5F', 'col2': '0x5F', 'col3': '0x0F', 'col4': '0xBC'},
{'name': 'INA219', 'description': 'Current Voltage Sensor', 'col1': '0x40', 'col2': '0x4F', 'col3': '0x00', 'col4': '0x39'},
{'name': 'INA260', 'description': 'Current Power Sensor', 'col1': '0x40', 'col2': '0x4F', 'col3': '0x00', 'col4': '0x61'},
{'name': 'IS31FL3731', 'description': 'LED Charlieplex Driver', 'col1': '0x74', 'col2': '0x77', 'col3': '0x00', 'col4': '0x00'},
{'name': 'ISL29125', 'description': 'Colour Sensor', 'col1': '0x44', 'col2': '0x44', 'col3': '0x00', 'col4': '0x7D'},
{'name': 'ISM330DHCX', 'description': 'Accelerometer Gyroscope', 'col1': '0x6A', 'col2': '0x6B', 'col3': '0x0F', 'col4': '0x6B'},
{'name': 'ITG3200', 'description': 'Gyroscope', 'col1': '0x68', 'col2': '0x69', 'col3': '0x00', 'col4': '0x00'},
{'name': 'KT0915', 'description': 'DSPRadio', 'col1': '0x35', 'col2': '0x35', 'col3': '0x00', 'col4': '0x00'},
{'name': 'L3GD20H', 'description': 'Gyroscope', 'col1': '0x6A', 'col2': '0x6B', 'col3': '0x0F', 'col4': '0xD7'},
{'name': 'LIS2MDL', 'description': 'Magnetometer', 'col1': '0x1E', 'col2': '0x1E', 'col3': '0x4F', 'col4': '0x40'},
{'name': 'LIS331', 'description': 'Accelerometer', 'col1': '0x18', 'col2': '0x19', 'col3': '0x0F', 'col4': '0x32'},
{'name': 'LIS3DH', 'description': 'Accelerometer', 'col1': '0x18', 'col2': '0x19', 'col3': '0x0F', 'col4': '0x33'},
{'name': 'LIS3MDL', 'description': 'Magnetometer', 'col1': '0x1E', 'col2': '0x1C', 'col3': '0x00', 'col4': '0x00'},
{'name': 'LPS22HB', 'description': 'PressureSensor', 'col1': '0x5C', 'col2': '0x5D', 'col3': '0x0F', 'col4': '0xB1'},
{'name': 'LPS25HB', 'description': 'PressureSensor', 'col1': '0x5C', 'col2': '0x5D', 'col3': '0x0F', 'col4': '0xBD'},
{'name': 'LPS33HW', 'description': 'PressureSensor', 'col1': '0x5C', 'col2': '0x5D', 'col3': '0x0F', 'col4': '0xB1'},
{'name': 'LPS35HW', 'description': 'PressureSensor', 'col1': '0x5C', 'col2': '0x5D', 'col3': '0x0F', 'col4': '0xB1'},
{'name': 'LSM303AGR', 'description': 'Accelerometer Magnetometer', 'col1': '0x1E', 'col2': '0x1E', 'col3': '0x4F', 'col4': '0x40'},
{'name': 'LSM303AGR', 'description': 'Accelerometer Magnetometer', 'col1': '0x19', 'col2': '0x19', 'col3': '0x0F', 'col4': '0x33'},
{'name': 'LSM303D', 'description': 'Accelerometer Magnetometer', 'col1': '0x1D', 'col2': '0x1E', 'col3': '0x0F', 'col4': '0x49'},
{'name': 'LSM303DLHC', 'description': 'Accelerometer Magnetometer', 'col1': '0x1E', 'col2': '0x1E', 'col3': '0x0C', 'col4': '0x33'},
{'name': 'LSM303DLHC', 'description': 'Accelerometer Magnetometer', 'col1': '0x19', 'col2': '0x19', 'col3': '0x20', 'col4': '0x07'},
{'name': 'LSM6DS33', 'description': 'Accelerometer Gyroscope', 'col1': '0x6A', 'col2': '0x6B', 'col3': '0x0F', 'col4': '0x69'},
{'name': 'LSM6DSOX', 'description': 'Accelerometer Gyroscope', 'col1': '0x6A', 'col2': '0x6B', 'col3': '0x0F', 'col4': '0x6C'},
{'name': 'LSM9DS0', 'description': 'Accelerometer GyroscopeMagnetometer', 'col1': '0x1E', 'col2': '0x1D', 'col3': '0x0F', 'col4': '0x49'},
{'name': 'LSM9DS0', 'description': 'Accelerometer GyroscopeMagnetometer', 'col1': '0x6B', 'col2': '0x6A', 'col3': '0x0F', 'col4': '0xD4'},
{'name': 'LSM9DS1', 'description': 'Accelerometer GyroscopeMagnetometer', 'col1': '0x1E', 'col2': '0x1C', 'col3': '0x0F', 'col4': '0x3D'},
{'name': 'LSM9DS1', 'description': 'Accelerometer GyroscopeMagnetometer', 'col1': '0x6B', 'col2': '0x6A', 'col3': '0x0F', 'col4': '0x68'},
{'name': 'MAG3110', 'description': 'Magnetometer', 'col1': '0x0E', 'col2': '0x0E', 'col3': '0x00', 'col4': '0x00'},
{'name': 'MAX17055', 'description': 'Fuel Gauge', 'col1': '0x36', 'col2': '0x36', 'col3': '0x00', 'col4': '0x00'},
{'name': 'MAX30101', 'description': 'Pulse Oximetry Sensor', 'col1': '0x57', 'col2': '0x57', 'col3': '0xFF', 'col4': '0x15'},
{'name': 'MAX77650', 'description': 'Power Management IC', 'col1': '0x48', 'col2': '0x40', 'col3': '0x00', 'col4': '0x00'},
{'name': 'MB85RC', 'description': 'Ferroelectric RAM', 'col1': '0x50', 'col2': '0x57', 'col3': '0x00', 'col4': '0x00'},
{'name': 'MB85RC256V', 'description': 'Ferroelectric RAM', 'col1': '0x50', 'col2': '0x57', 'col3': '0x00', 'col4': '0x00'},
{'name': 'MCP23008', 'description': 'GPIO Expander', 'col1': '0x20', 'col2': '0x27', 'col3': '0x00', 'col4': '0x00'},
{'name': 'MCP23017', 'description': 'GPIO Expander', 'col1': '0x20', 'col2': '0x27', 'col3': '0x00', 'col4': '0x00'},
{'name': 'MCP4725A1', 'description': 'Digital to Analogue Converter', 'col1': '0x62', 'col2': '0x63', 'col3': '0x00', 'col4': '0x00'},
{'name': 'MCP4725A2', 'description': 'Digital to Analogue Converter', 'col1': '0x64', 'col2': '0x65', 'col3': '0x00', 'col4': '0x00'},
{'name': 'MCP4725A3', 'description': 'Digital to Analogue Converter', 'col1': '0x66', 'col2': '0x67', 'col3': '0x00', 'col4': '0x00'},
{'name': 'MCP4728', 'description': 'Digital to Analogue Converter', 'col1': '0x60', 'col2': '0x67', 'col3': '0x00', 'col4': '0x00'},
{'name': 'MCP9600', 'description': 'Thermocouple Amplifier', 'col1': '0x60', 'col2': '0x67', 'col3': '0x20', 'col4': '0x40'},
{'name': 'MCP9808', 'description': 'Temperature Sensor', 'col1': '0x18', 'col2': '0x1F', 'col3': '0x07', 'col4': '0x04'},
{'name': 'MLX9061x', 'description': 'IR Temperature Sensor', 'col1': '0x5A', 'col2': '0x5A', 'col3': '0x00', 'col4': '0x00'},
{'name': 'MLX90640', 'description': 'IR Thermal Camera', 'col1': '0x33', 'col2': '0x33', 'col3': '0x00', 'col4': '0x00'},
{'name': 'MMA7455L', 'description': 'Accelerometer', 'col1': '0x1C', 'col2': '0x1D', 'col3': '0x0F', 'col4': '0x3D'},
{'name': 'MMA8451Q', 'description': 'Accelerometer', 'col1': '0x1C', 'col2': '0x1D', 'col3': '0x0D', 'col4': '0x1A'},
{'name': 'MMA8452Q', 'description': 'Accelerometer', 'col1': '0x1C', 'col2': '0x1D', 'col3': '0x0D', 'col4': '0x2A'},
{'name': 'MMA8453Q', 'description': 'Accelerometer', 'col1': '0x1C', 'col2': '0x1D', 'col3': '0x0D', 'col4': '0x3A'},
{'name': 'MMA8652FC', 'description': 'Accelerometer', 'col1': '0x1D', 'col2': '0x1D', 'col3': '0x0D', 'col4': '0x4A'},
{'name': 'MMA8653FC', 'description': 'Accelerometer', 'col1': '0x1D', 'col2': '0x1D', 'col3': '0x0D', 'col4': '0x5A'},
{'name': 'MPL115A2', 'description': 'Pressure Sensor', 'col1': '0x60', 'col2': '0x60', 'col3': '0x00', 'col4': '0x00'},
{'name': 'MPL3115A2', 'description': 'Pressure Sensor', 'col1': '0x60', 'col2': '0x60', 'col3': '0x0C', 'col4': '0xC4'},
{'name': 'MPR121', 'description': 'Capacitive Touch Sensor', 'col1': '0x5A', 'col2': '0x5D', 'col3': '0x5C', 'col4': '0x10'},
{'name': 'MPRLS', 'description': 'Pressure Sensor', 'col1': '0x18', 'col2': '0x18', 'col3': '0x00', 'col4': '0x00'},
{'name': 'MS5607', 'description': 'Pressure Sensor', 'col1': '0x76', 'col2': '0x77', 'col3': '0x00', 'col4': '0x00'},
{'name': 'MS5611', 'description': 'Pressure Sensor', 'col1': '0x76', 'col2': '0x77', 'col3': '0x00', 'col4': '0x00'},
{'name': 'MSA301', 'description': 'Accelerometer', 'col1': '0x26', 'col2': '0x26', 'col3': '0x01', 'col4': '0x13'},
{'name': 'NAU7802', 'description': 'Load Cell Scale', 'col1': '0x2A', 'col2': '0x2A', 'col3': '0x00', 'col4': '0x00'},
{'name': 'NCD2400M', 'description': 'Digital Capacitor', 'col1': '0x60', 'col2': '0x60', 'col3': '0x00', 'col4': '0x00'},
{'name': 'NCD2400M1', 'description': 'Digital Capacitor', 'col1': '0x61', 'col2': '0x61', 'col3': '0x00', 'col4': '0x00'},
{'name': 'Nintendo', 'description': 'Nunchuck Controller', 'col1': '0x52', 'col2': '0x52', 'col3': '0x00', 'col4': '0x00'},
{'name': 'PA1010D', 'description': 'GPS GNSS Receiver', 'col1': '0x10', 'col2': '0x10', 'col3': '0x00', 'col4': '0x00'},
{'name': 'PCA9685', 'description': 'PWM Driver', 'col1': '0x7F', 'col2': '0x40', 'col3': '0x00', 'col4': '0x00'},
{'name': 'PCF8523', 'description': 'Real Time Clock', 'col1': '0x68', 'col2': '0x68', 'col3': '0x00', 'col4': '0x00'},
{'name': 'PCF8591', 'description': 'ADC DAC', 'col1': '0x48', 'col2': '0x4F', 'col3': '0x00', 'col4': '0x00'},
{'name': 'PMSA003I', 'description': 'Air Quality Sensor', 'col1': '0x12', 'col2': '0x12', 'col3': '0x00', 'col4': '0x00'},
{'name': 'PN532', 'description': 'NFC RFID Reader', 'col1': '0x48', 'col2': '0x48', 'col3': '0x00', 'col4': '0x00'},
{'name': 'SCD30', 'description': 'CO2 Sensor', 'col1': '0x61', 'col2': '0x61', 'col3': '0x00', 'col4': '0x00'},
{'name': 'SGP30', 'description': 'Gas Sensor', 'col1': '0x58', 'col2': '0x58', 'col3': '0x00', 'col4': '0x00'},
{'name': 'SGP40', 'description': 'Gas Sensor', 'col1': '0x59', 'col2': '0x59', 'col3': '0x00', 'col4': '0x00'},
{'name': 'SH1106', 'description': 'OLED Display', 'col1': '0x3C', 'col2': '0x3D', 'col3': '0x00', 'col4': '0x00'},
{'name': 'SHT30', 'description': 'Humidity Temperature Sensor', 'col1': '0x44', 'col2': '0x45', 'col3': '0x00', 'col4': '0x00'},
{'name': 'SHT31', 'description': 'Humidity Temperature Sensor', 'col1': '0x44', 'col2': '0x45', 'col3': '0x00', 'col4': '0x00'},
{'name': 'SHT35', 'description': 'Humidity Temperature Sensor', 'col1': '0x44', 'col2': '0x45', 'col3': '0x00', 'col4': '0x00'},
{'name': 'SHTC3', 'description': 'Temperature Humidity Sensor', 'col1': '0x70', 'col2': '0x70', 'col3': '0x00', 'col4': '0x00'},
{'name': 'SSD1305', 'description': 'OLED Display', 'col1': '0x3C', 'col2': '0x3D', 'col3': '0x00', 'col4': '0x00'},
{'name': 'SSD1306', 'description': 'OLED Display', 'col1': '0x3C', 'col2': '0x3D', 'col3': '0x00', 'col4': '0x00'},
{'name': 'SSD1327', 'description': 'OLED Display', 'col1': '0x7A', 'col2': '0x78', 'col3': '0x00', 'col4': '0x00'},
{'name': 'ST25DV16K', 'description': 'RFID Tag', 'col1': '0x57', 'col2': '0x53', 'col3': '0x00', 'col4': '0x00'},
{'name': 'ST25DV16K', 'description': 'RFID Tag', 'col1': '0x2D', 'col2': '0x2D', 'col3': '0x00', 'col4': '0x00'},
{'name': 'STMPE610', 'description': 'Resistive Touch Controller', 'col1': '0x44', 'col2': '0x41', 'col3': '0x00', 'col4': '0x08'},
{'name': 'STMPE811', 'description': 'Resistive Touch Controller', 'col1': '0x44', 'col2': '0x41', 'col3': '0x00', 'col4': '0x08'},
{'name': 'Si1145', 'description': 'Light Sensor', 'col1': '0x60', 'col2': '0x60', 'col3': '0x00', 'col4': '0x45'},
{'name': 'Si1146', 'description': 'Light Sensor', 'col1': '0x60', 'col2': '0x60', 'col3': '0x00', 'col4': '0x46'},
{'name': 'Si1147', 'description': 'Light Sensor', 'col1': '0x60', 'col2': '0x60', 'col3': '0x00', 'col4': '0x47'},
{'name': 'Si4712', 'description': 'FM Transmitter', 'col1': '0x63', 'col2': '0x11', 'col3': '0x00', 'col4': '0x00'},
{'name': 'Si4713', 'description': 'FM Transmitter', 'col1': '0x63', 'col2': '0x11', 'col3': '0x00', 'col4': '0x00'},
{'name': 'Si5351A', 'description': 'Clock Generator', 'col1': '0x60', 'col2': '0x61', 'col3': '0x00', 'col4': '0x00'},
{'name': 'Si7021', 'description': 'Humidity Temperature Sensor', 'col1': '0x40', 'col2': '0x40', 'col3': '0x00', 'col4': '0x00'},
{'name': 'TC74A0', 'description': 'Temperature Sensor', 'col1': '0x48', 'col2': '0x48', 'col3': '0x00', 'col4': '0x00'},
{'name': 'TCA9548A', 'description': 'Multiplexer', 'col1': '0x70', 'col2': '0x77', 'col3': '0x00', 'col4': '0x00'},
{'name': 'TCS34721', 'description': 'Colour Sensor', 'col1': '0x39', 'col2': '0x39', 'col3': '0x92', 'col4': '0x44'},
{'name': 'TCS34723', 'description': 'Colour Sensor', 'col1': '0x39', 'col2': '0x39', 'col3': '0x92', 'col4': '0x4D'},
{'name': 'TCS34725', 'description': 'Colour Sensor', 'col1': '0x29', 'col2': '0x29', 'col3': '0x92', 'col4': '0x44'},
{'name': 'TCS34727', 'description': 'Colour Sensor', 'col1': '0x29', 'col2': '0x29', 'col3': '0x92', 'col4': '0x4D'},
{'name': 'TEA5767', 'description': 'Radio Receiver', 'col1': '0x60', 'col2': '0x60', 'col3': '0x00', 'col4': '0x00'},
{'name': 'TLV493D', 'description': 'Magnetometer', 'col1': '0x5E', 'col2': '0x5E', 'col3': '0x00', 'col4': '0x00'},
{'name': 'TMP006', 'description': 'IR Temperature Sensor', 'col1': '0x40', 'col2': '0x47', 'col3': '0xFE', 'col4': '0x54'},
{'name': 'TMP007', 'description': 'IR Temperature Sensor', 'col1': '0x40', 'col2': '0x47', 'col3': '0xFE', 'col4': '0x54'},
{'name': 'TMP102', 'description': 'Temperature Sensor', 'col1': '0x48', 'col2': '0x4B', 'col3': '0x00', 'col4': '0x00'},
{'name': 'TMP117', 'description': 'Temperature Sensor', 'col1': '0x48', 'col2': '0x49', 'col3': '0x00', 'col4': '0x00'},
{'name': 'TPA2016', 'description': 'Amplifier', 'col1': '0x58', 'col2': '0x58', 'col3': '0x00', 'col4': '0x00'},
{'name': 'TSL2561', 'description': 'Light Sensor', 'col1': '0x49', 'col2': '0x49', 'col3': '0x00', 'col4': '0x00'},
{'name': 'TSL2561', 'description': 'Light Sensor', 'col1': '0x39', 'col2': '0x29', 'col3': '0x00', 'col4': '0x00'},
{'name': 'TSL2591', 'description': 'Light Sensor', 'col1': '0x28', 'col2': '0x29', 'col3': '0x12', 'col4': '0x50'},
{'name': 'VCNL4000', 'description': 'Proximity Sensor', 'col1': '0x13', 'col2': '0x13', 'col3': '0x81', 'col4': '0x11'},
{'name': 'VCNL4010', 'description': 'Proximity Sensor', 'col1': '0x13', 'col2': '0x13', 'col3': '0x81', 'col4': '0x21'},
{'name': 'VCNL4020', 'description': 'Proximity Sensor', 'col1': '0x13', 'col2': '0x13', 'col3': '0x81', 'col4': '0x21'},
{'name': 'VCNL4040', 'description': 'Proximity Light Sensor', 'col1': '0x60', 'col2': '0x60', 'col3': '0x0C', 'col4': '0x86'},
{'name': 'VEML6070', 'description': 'UV Light Sensor', 'col1': '0x38', 'col2': '0x39', 'col3': '0x00', 'col4': '0x00'},
{'name': 'VEML6075', 'description': 'UV Light Sensor', 'col1': '0x10', 'col2': '0x10', 'col3': '0x0C', 'col4': '0x26'},
{'name': 'VEML7700', 'description': 'Light Sensor', 'col1': '0x10', 'col2': '0x10', 'col3': '0x00', 'col4': '0x00'},
{'name': 'VL53L0X', 'description': 'TimeofFlight Sensor', 'col1': '0x29', 'col2': '0x29', 'col3': '0xC0', 'col4': '0xEE'},
{'name': 'VL53L1X', 'description': 'TimeofFlight Sensor', 'col1': '0x29', 'col2': '0x29', 'col3': '0xC0', 'col4': '0xEE'},
{'name': 'VL53L3CX', 'description': 'TimeofFlight Sensor', 'col1': '0x29', 'col2': '0x29', 'col3': '0x00', 'col4': '0x00'},
{'name': 'VL6180X', 'description': 'TimeofFlight Sensor', 'col1': '0x29', 'col2': '0x29', 'col3': '0x00', 'col4': '0xB4'},
{'name': 'WT2003S', 'description': 'MP3Player', 'col1': '0x37', 'col2': '0x37', 'col3': '0x00', 'col4': '0x00'},
{'name': 'XA1110', 'description': 'GPSGNSS Receiver', 'col1': '0x10', 'col2': '0x10', 'col3': '0x00', 'col4': '0x00'},
{'name': 'ZMOD4450', 'description': 'Gas Sensor', 'col1': '0x32', 'col2': '0x32', 'col3': '0x00', 'col4': '0x00'},
{'name': 'HTU21D-F', 'description': 'Humidity Temperature Sensor', 'col1': '0x40', 'col2': '0x40', 'col3': '0x00', 'col4': '0x00'},
{'name': 'ICM-20649', 'description': 'Accelerometer Gyroscope', 'col1': '0x68', 'col2': '0x69', 'col3': '0x00', 'col4': '0xE1'},
{'name': 'ICM-20948', 'description': 'Accelerometer Gyroscope Magnetometer', 'col1': '0x68', 'col2': '0x69', 'col3': '0x00', 'col4': '0xEA'},
{'name': 'LTR-390', 'description': 'UVLightSensor', 'col1': '0x53', 'col2': '0x53', 'col3': '0x06', 'col4': '0xB2'},
{'name': 'MPU-6000', 'description': 'Accelerometer Gyroscope', 'col1': '0x68', 'col2': '0x69', 'col3': '0x00', 'col4': '0x00'},
{'name': 'MPU-6050', 'description': 'Accelerometer Gyroscope', 'col1': '0x68', 'col2': '0x69', 'col3': '0x00', 'col4': '0x00'},
{'name': 'MPU-9250', 'description': 'Accelerometer Gyroscope Magnetometer', 'col1': '0x68', 'col2': '0x69', 'col3': '0x00', 'col4': '0x48'},
{'name': 'NEO-M9N', 'description': 'GPS GNSS Receiver', 'col1': '0x42', 'col2': '0x42', 'col3': '0x00', 'col4': '0x00'},
{'name': 'ZOE-M8Q', 'description': 'GPS GNSS Receiver', 'col1': '0x42', 'col2': '0x42', 'col3': '0x00', 'col4': '0x00'}
]
df = pd.DataFrame(slovar)

def lsusb_find():
    val = os.system(command_lsusb)
    #print(val)
    if val == 0:
        value = 1
    else:
        value = 0
    return value

# Find i2c line cp2112
def find_i2c_line():
    fin = lsusb_find()
    if fin == 1:
        val = os.system(command_find_i2c_line)
        if val == 0:
            string = subprocess.check_output(command_find_i2c_line, shell=True)
            string = str(string)
            #print(string)
            decoded_string = string.encode().decode('unicode_escape')  # декодируем строку из байтового формата и удаляем экранирование
            pattern = r"i2c-(\d+).*"

            match = re.search(pattern, decoded_string)
            if match:
                value = match.group(1)
                #print(value,type(value))
        else:
            value = 0
    else:
        value = 0
    return value

def final_find_address():
    output = subprocess.check_output(["i2cdetect","-r", "-y", "6"])
    lines = output.decode().split("\n")[1:-1]  # пропускаем первую и последнюю строки
    addresses = []
    for line in lines:
        matches = re.findall(r"\s([0-9a-f]{2})\s", line)
        addresses.extend(matches)

    addresses_str = " ".join(addresses)
    #print(addresses_str)
    return addresses_str


def address_searcher():
    address = final_find_address()
    address = "0x" + address
    #print(address)
    result = df.loc[(df["col1"] == address)]
    print(result)


def rebounder_register():
    command_get = "i2cget -y "
    line = find_i2c_line()
    address = final_find_address()
    address = "0x" + address
    for i in range(256):
        hexer = hex(i)[2:].zfill(2)
        hexer = "0x" + hexer
        command = command_get + line + " " + address + " " + hexer
        string = subprocess.check_output(command, shell=True)
        string = str(string)
        decoded_string = string.encode().decode('unicode_escape')  # декодируем строку из байтового формата и удаляем экранирование
        decoded_string = str(decoded_string)
        decoded_string = (decoded_string[2:6])
        result = df.loc[(df["col3"] == hexer) & (df["col4"] == decoded_string)]
        if not result.empty:
            print(result)




def final_searcher(address, register, to_reg, value):
    result = df.loc[(df["col1"] == address) & (df["col2"] == register) & (df["col3"] == to_reg) & (df["col4"] == value)]
    print(result)


address_searcher()
print("\n")
print("\n")
print("!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!")
print("\n")
print("\n")
rebounder_register()