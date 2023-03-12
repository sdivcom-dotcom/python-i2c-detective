import pandas as pd

# Создание DataFrame из примера данных
data = [
    {"name": "ADC122C04", "description": "ThermocoupleAmplifier", "col1": "0x40", "col2": "0x4F", "col3": "0x00", "col4": "0x00"},
    {'name': 'ZMOD4450', 'description': 'GasSensor', 'col1': '0x32', 'col2': '0x32', 'col3': '0x00', 'col4': '0x00'}
]
df = pd.DataFrame(data)

# Поиск по третьему столбцу
search_value = "0x40"
result = df.loc[df["col1"] == search_value]

# Вывод результатов
print(result)