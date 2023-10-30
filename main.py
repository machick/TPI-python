from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from dolar import dolar
import json

# Abre el archivo JSON y carga los datos
#with open('dolar/dolar.json', 'r') as json_file:
#   dolars = json.load(json_file)

app = FastAPI()

origins = [
    "http://localhost:4200",
    "http://localhost:8080",
    "http://api.mercadojunior.com.ar",
]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

items = [1]

@app.get("/")
async def get_initial():
    return {"hola":"Mundo"}
        # Accede a los datos del archivo JSON
    #filtered_data = [item for item in dolars if item["source"] == "Blue"]
    
    # valor_dolar = data["valor_dolar"]
    
    # fecha = data["fecha"]

    # Imprime los datos
    # print("Valor del dólar:", valor_dolar)
    #print("Fecha:", fecha)
    
    #return {"hola":filtered_data}

# Ruta para obtener todos los elementos
@app.get("/items/")
async def get_items():
    return items

# Ruta para crear un nuevo elemento
@app.post("/items/")
async def create_item(item: dict):
    items.append(item)
    return item

@app.get("/dolar/")
async def get_dolar():
    return {"dolar": dolar.getDollar()}

@app.get("/dolar-training/")
async def get_dolar_training():
    return {dolar.getDollarTraining()}

@app.get("/saludo/")
async def getSaludo():
    return dolar.getSaludo()