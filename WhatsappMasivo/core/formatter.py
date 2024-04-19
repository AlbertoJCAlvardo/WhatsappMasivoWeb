import pandas as pd 

def format_string(text:str,data:pd.DataFrame):

    words, tokens = [],[]
    formatted = ""
    lst = text.split("{")
    for i in lst:
        
        if "}" in i:

            lst2 = i.split("}")
            if len(lst2) == 1:
                key = lst2[0]
                if key in data.axes[0]:
                    formatted += f"{data[key]}"
                else:
                    formatted += f"{{{key}}}"

            if len(lst2) > 0:
                key = lst2[0]
                if key in data.axes[0]:
                    formatted += f"{data[key]}"
                else:
                    formatted += f"{{{key}}}"
                formatted += f"{lst2[1]}"
            
        else:
            formatted += i
    

    return formatted

def format_phone_numbers(numbers):
    valid_numbers = []
    formatted_numbers = {}
    for i in numbers:
        if i.isdigit():
            if len(i) == 10:
                valid_numbers.append(i)
                formatted_numbers[i] =  "+52"+i
            if len(i) == 12:
                if i[0:2] == "52":
                    valid_numbers.append(i)
                    formatted_numbers[i] = "+"+i
        
        if i[0:1] == "+" and i[1:len(i)].isdigit():
            if len(i) == 13:
                    if i[0:3] == "+52":
                        valid_numbers.append(i)
                        formatted_numbers[i] = i
    return valid_numbers, formatted_numbers

                


        

def set_wa_format(message, data:pd.DataFrame):
    tokens = {}
    

    index = 1
    formatted = ""
    lst = message.split("{")
    
    for i in lst:
        
        if "}" in i:

            lst2 = i.split("}")
            if len(lst2) == 1:
                key = lst2[0]
                if key in data.keys():
                    if key in tokens.keys():
                        formatted += f"{{{tokens[key]}}}"
                    else:
                        tokens[key] = str(index)
                        index += 1
                        formatted += f" {{{{{tokens[key]}}}}}"
                else:
                    formatted += f"{key}"

            if len(lst2) > 0:
                key = lst2[0]
                if key in tokens.keys():
                        formatted += f"{{{{{tokens[key]}}}}}"
                else:
                        tokens[key] = str(index)
                        index += 1
                        formatted += f" {{{{{tokens[key]}}}}}"
                formatted += f"{lst2[1]}"
            
        else:
            formatted += i
    

    return formatted, tokens

                
    