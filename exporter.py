import re

def parse_string(input_string):
    # Задаем регулярное выражение, соответствующее строке в нужном формате
    pattern = r'{\s*"([\w\d]+)",\s*([\w\d\s]+),\s*(0x[\dA-Fa-f]{2}),\s*(0x[\dA-Fa-f]{2}),\s*(0x[\dA-Fa-f]{2}),\s*(0x[\dA-Fa-f]{2})\s*}'

    # Ищем соответствия в строке
    match = re.match(pattern, input_string)
    if match:
        # Если найдено соответствие, извлекаем значения групп
        values = match.groups()
        
        # Создаем словарь с нужными ключами и значениями
        output_dict = {
            "name": values[0],
            "description": values[1],
            "col1": values[2],
            "col2": values[3],
            "col3": values[4],
            "col4": values[5]
        }
        return output_dict
    else:
        # Если соответствие не найдено, возвращаем None
        return None

with open("t.txt", "r") as input_file:
    with open("output.txt", "w") as output_file:
        for i in range(175):
            first_line = input_file.readline()
            first_line = first_line.replace('\n', '')
            #print(first_line)
            output_dict = parse_string(first_line)
            #print(output_dict)
            output_dict = str(output_dict) 
            if output_dict == "None":
                print(first_line)
            else:
                output_file.write(output_dict)
                output_file.write("\n")

