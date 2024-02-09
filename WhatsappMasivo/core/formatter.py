import pandas as pd 
class Formatter:

    def format_string(self,text:str,data:pd.Series):

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

    def format_phone_numbers(self,numbers):
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

                    


        

