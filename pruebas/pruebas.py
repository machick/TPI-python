# Online Python compiler (interpreter) to run Python online.
# Write Python 3 code in this online editor and run it.
dolars = [{"date":"2023-10-20","source":"Blue","value_sell":900.0,"value_buy":880.0},{"date":"2023-10-19","source":"Blue","value_sell":900.0,"value_buy":880.0},{"date":"2023-10-18","source":"Blue","value_sell":905.0,"value_buy":885.0},{"date":"2023-10-17","source":"Blue","value_sell":985.0,"value_buy":965.0},{"date":"2023-10-16","source":"Blue","value_sell":980.0,"value_buy":960.0},{"date":"2023-10-13","source":"Blue","value_sell":980.0,"value_buy":960.0},{"date":"2023-10-12","source":"Blue","value_sell":980.0,"value_buy":960.0},{"date":"2023-10-11","source":"Blue","value_sell":1010.0,"value_buy":990.0},{"date":"2023-10-10","source":"Blue","value_sell":1010.0,"value_buy":990.0}]


filtered_data = [item for item in dolars if item["source"] == "Blue" and item["date"] < "2023-10-18" ]


def filtrar_x(data): 
    fecha_str = data["date"]
        # Elimina los guiones de la cadena de fecha
    fecha_sin_guiones = fecha_str.replace("-", "")
    
    # Convierte la cadena en un número entero
    numero = int(fecha_sin_guiones)

    return numero

    
def filtrar_y(data): 
    return data["value_sell"]
        

arrayX = map(filtrar_x, filtered_data) 
arrayY = map(filtrar_y, filtered_data) 
#print(filtered_data)
print(list(arrayX))
print(list(arrayY))