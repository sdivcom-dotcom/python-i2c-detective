import pandas as pd
import re
import subprocess
data = [
    {"name": "ADC122C04", "description": "ThermocoupleAmplifier", "col1": "0x40", "col2": "0x4F", "col3": "0x00", "col4": "0x00"},
    {'name': 'ZMOD4450', 'description': 'GasSensor', 'col1': '0x40', 'col2': '0x32', 'col3': '0x01', 'col4': '0x10'}
]
df = pd.DataFrame(data)

address1 = "0x40"
address2 = "0x4F"
address3 = "0x00"
address4 = "0x00"
result = df.loc[(df["col1"] == address1) & (df["col2"] == address2) & (df["col3"] == address3) & (df["col4"] == address4)]
print(result)


output = subprocess.check_output(["i2cdetect","-r", "-y", "6"])
lines = output.decode().split("\n")[1:-1]  # пропускаем первую и последнюю строки

addresses = []
for line in lines:
    matches = re.findall(r"\s([0-9a-f]{2})\s", line)
    addresses.extend(matches)

print(addresses)