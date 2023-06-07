import uuid
from fastapi import FastAPI, HTTPException, Request, Depends, Query
from typing import List
from pydantic import BaseModel
import sqlite3

# Definimos los modelos de datos


class Company(BaseModel):
    company_id: int
    company_name: str
    company_api_key: str

class Location(BaseModel):
    location_id: int
    company_id: int
    location_name: str
    location_api_key: str

class LocationCreate(BaseModel):
    location_name: str
    location_country: str
    location_city: str
    location_meta: str
    
class Sensor(BaseModel):
    sensor_id: int
    location_id: int
    sensor_name: str
    sensor_category: str
    sensor_meta: str
    sensor_api_key: str

class SensorCreate(BaseModel):
    sensor_name: str
    sensor_category: str
    sensor_meta: str

class SensorData(BaseModel):
    sensor_id: int
    variable1: float
    variable2: float
    timestamp: int

class SensorDataItem(BaseModel):
    variable1: float
    variable2: float
    timestamp: int

class SensorDataPOST(BaseModel):
    api_key: str
    json_data: List[SensorDataItem]

# Creamos la aplicación FastAPI
app = FastAPI()

@app.get("/api/v1/location")
async def get_locations(request: Request, location_id: int = Query(None)):
    db = sqlite3.connect("database.db")
    api_key = request.headers.get('company_api_key')
    # Verificamos la clave API de la compañía
    cursor = db.execute(
        "SELECT * FROM Company WHERE company_api_key=?", (api_key,))
    company = cursor.fetchone()
    if not company:
        raise HTTPException(status_code=401, detail="Clave API inválida.")

    if location_id is not None:
        cursor = db.execute("SELECT * FROM Location WHERE location_id = ?", (location_id,))
    else:
        cursor = db.execute("SELECT * FROM Location")
    locations = cursor.fetchall()
    
    location_list = []
    for location in locations:
        location_dict = {
            "location_id": location[0],
            "company_id": location[1],
            "location_name": location[2],
            "location_country": location[3],
            "location_city": location[4],
            "location_meta": location[5],
            "location_api_key": location[6]
        }
        location_list.append(location_dict)
    db.close()
    if(len(location_list) == 1):
        return location_list[0]
    return {"Locations": location_list}

@app.post("/api/v1/location")
async def create_location(location: LocationCreate, request: Request):
    db = sqlite3.connect("database.db")
    
    # Verificamos la clave API de la compañía
    api_key = request.headers.get('company_api_key')

    cursor = db.execute("SELECT * FROM Company WHERE company_api_key=?", (api_key,))
    company = cursor.fetchone()
    if not company:
        raise HTTPException(status_code=401, detail="Clave API inválida.")
    
    # Generamos una clave API única para el Location
    location_api_key = str(uuid.uuid4())
    
    cursor.execute("SELECT location_id FROM Location ORDER BY location_id DESC LIMIT 1")
    location_id = cursor.fetchone()
    location_id = location_id[0] + 1
    # Insertamos el Location en la base de datos
    db.execute("INSERT INTO Location (company_id, location_name, location_country, location_city, location_meta, location_api_key) VALUES (?, ?, ?, ?, ?, ?)",
               (company[0], location.location_name, location.location_country, location.location_city, location.location_meta, location_api_key))
    
    # Guardamos los cambios
    db.commit()
    db.close()
    
    return {
        "location_id": location_id,
        "company_id": company[0],
        "location_name": location.location_name,
        "location_country": location.location_country,
        "location_city": location.location_city,
        "location_meta": location.location_meta,
        "location_api_key": location_api_key
    }

@app.delete("/api/v1/location/{location_id}")
async def delete_location(location_id: int, request: Request):
    db = sqlite3.connect("database.db")
    
    # Verificamos la clave API de la compañía
    api_key = request.headers.get('company_api_key')
    cursor = db.execute("SELECT * FROM Company WHERE company_api_key=?", (api_key,))
    company = cursor.fetchone()
    if not company:
        raise HTTPException(status_code=401, detail="Clave API inválida.")
    
    # Verificamos si el Location existe
    cursor = db.execute("SELECT * FROM Location WHERE location_id=?", (location_id,))
    location = cursor.fetchone()
    if not location:
        raise HTTPException(status_code=404, detail="Location no encontrado.")
    
    # Eliminamos el Location de la base de datos
    db.execute("DELETE FROM Location WHERE location_id=?", (location_id,))
    
    # Guardamos los cambios
    db.commit()
    db.close()
    
    return {"status_code": 200, "detail": "Location eliminado exitosamente"}

@app.put("/api/v1/location/{location_id}")
async def update_location(location_id: int, request: Request, update_data: dict,):
    db = sqlite3.connect("database.db")
    # Verificamos la clave API de la compañía
    api_key = request.headers.get('company_api_key')
    cursor = db.execute("SELECT * FROM Company WHERE company_api_key=?", (api_key,))
    company = cursor.fetchone()
    if not company:
        raise HTTPException(status_code=401, detail="Clave API inválida.")

    # Verificar si la ubicación existe
    cursor = db.execute("SELECT * FROM Location WHERE location_id=?", (location_id,))
    location = cursor.fetchone()
    if not location:
        raise HTTPException(status_code=404, detail="La ubicación no existe.")

    # Actualizar las variables de la ubicación
    allowed_fields = ['location_name', 'location_country', 'location_city', 'location_meta']
    update_fields = {key: value for key, value in update_data.items() if key in allowed_fields}

    if update_fields:
        set_fields = ", ".join([f"{field} = ?" for field in update_fields])
        update_values = tuple(update_fields.values()) + (location_id,)
        update_query = f"UPDATE Location SET {set_fields} WHERE location_id = ?"
        db.execute(update_query, update_values)
        db.commit()

    db.close()
    return {"message": "Ubicación actualizada correctamente."}


@app.get("/api/v1/sensor")
def get_sensors(request: Request, sensor_id: int = Query(None)):
    db = sqlite3.connect("database.db")
    api_key = request.headers.get('company_api_key')
    cursor = db.execute(
        "SELECT * FROM Company WHERE company_api_key=?", (api_key,))
    company = cursor.fetchone()
    print(api_key)
    if not company:
        raise HTTPException(status_code=401, detail="Clave API inválida.")

    if sensor_id is not None:
        cursor = db.execute("SELECT * FROM Sensor WHERE sensor_id = ?", (sensor_id,))
    else:
        cursor = db.execute("SELECT * FROM Sensor")
    sensors = cursor.fetchall()
    
    sensor_list = []
    for sensor in sensors:
        sensor_dict = {
            "sensor_id": sensor[0],
            "location_id": sensor[1],
            "sensor_name": sensor[2],
            "sensor_category": sensor[3],
            "sensor_meta": sensor[4],
            "sensor_api_key": sensor[5]
        }
        sensor_list.append(sensor_dict)
    db.close()
    if(len(sensor_list) == 1):
        return sensor_list[0]
    return {"Sensors": sensor_list}

@app.post("/api/v1/sensor")
async def create_sensor(sensor: SensorCreate, request: Request):
    db = sqlite3.connect("database.db")
    # Verificamos la clave API de location
    api_key = request.headers.get('location_api_key')
    cursor = db.execute(
        "SELECT * FROM Location WHERE location_api_key=?", (api_key,))
    location = cursor.fetchone()
    if not location:
        raise HTTPException(status_code=401, detail="Clave API inválida.")

    # Generamos una clave API única para el sensor
    sensor_api_key = str(uuid.uuid4())
    # Insertamos el sensor en la base de datos
    cursor.execute("SELECT sensor_id FROM Sensor ORDER BY sensor_id DESC LIMIT 1")
    sensor_id = cursor.fetchone()
    sensor_id = sensor_id[0] + 1

    db.execute("INSERT INTO Sensor (location_id, sensor_name, sensor_category, sensor_meta, sensor_api_key) VALUES (?, ?, ?, ?, ?)",
                  (location[0], sensor.sensor_name, sensor.sensor_category, sensor.sensor_meta, sensor_api_key))
    # Guardamos los cambios
    db.commit()
    db.close()
    return {
        "sensor_id": sensor_id,
        "location_id": location[0],
        "sensor_name": sensor.sensor_name,
        "sensor_category": sensor.sensor_category,
        "sensor_meta": sensor.sensor_meta,
        "sensor_api_key": sensor_api_key
    }

@app.put("/api/v1/sensor/{sensor_id}")
async def update_sensor(sensor_id: int, request: Request, update_data: dict):
    db = sqlite3.connect("database.db")
    # Verificamos la clave API de location
    api_key = request.headers.get('company_api_key')
    cursor = db.execute("SELECT * FROM Company WHERE company_api_key=?", (api_key,))
    company = cursor.fetchone()
    if not company:
        raise HTTPException(status_code=401, detail="Clave API inválida.")

    # Verificar si el sensor existe
    cursor = db.execute("SELECT * FROM Sensor WHERE sensor_id=?", (sensor_id,))
    sensor = cursor.fetchone()
    if not sensor:
        raise HTTPException(status_code=404, detail="El sensor no existe.")

    # Actualizar las variables del sensor
    allowed_fields = ['sensor_name', 'sensor_category', 'sensor_meta']
    update_fields = {key: value for key, value in update_data.items() if key in allowed_fields}

    if update_fields:
        set_fields = ", ".join([f"{field} = ?" for field in update_fields])
        update_values = tuple(update_fields.values()) + (sensor_id,)
        update_query = f"UPDATE Sensor SET {set_fields} WHERE sensor_id = ?"
        db.execute(update_query, update_values)
        db.commit()

    db.close()
    return {"message": "Sensor actualizado correctamente."}

# Definimos el endpoint para insertar datos de sensores
@app.post("/api/v1/sensor_data")
async def insert_sensor_data(sensor_data: SensorDataPOST, request: Request):
    db = sqlite3.connect("database.db")
    
    # Verificar la clave API del sensor
    api_key = sensor_data.api_key
    cursor = db.execute("SELECT * FROM Sensor WHERE sensor_api_key=?", (api_key,))
    sensor = cursor.fetchone()
    
    if not sensor:
        raise HTTPException(status_code=400, detail="Clave API inválida.")
    
    # Insertar los datos del sensor en la base de datos
    for data in sensor_data.json_data:
        db.execute("INSERT INTO SensorData (sensor_id, variable1, variable2, timestamp) VALUES (?, ?, ?, ?)",
                   (sensor[0], data.variable1, data.variable2, data.timestamp))
    
    # Guardar los cambios
    db.commit()
    db.close()
    
    return {"status_code": 201, "detail": "Datos del sensor insertados exitosamente"}


# Definimos el endpoint para consultar la información de Sensor Data
@app.get("/api/v1/sensor_data")
async def get_sensor_data(request: Request, start: int, to: int):
    db = sqlite3.connect("database.db")
    try:
        sensor_id = await request.json()
        sensor_id = sensor_id['sensor_id']
    except:
        raise HTTPException(status_code=400, detail="Missing Sensor IDs in Body (favor usar formato JSON)")

    # Verificamos la clave API del sensor
    api_key = request.headers.get('company_api_key')
    cursor = db.execute(
        "SELECT * FROM Company WHERE company_api_key=?", (api_key,))
    company = cursor.fetchone()
    if not company:
        raise HTTPException(status_code=401, detail="Clave API inválida.")
    
    # Consultamos la información de Sensor Data
    cursor = db.execute(
        "SELECT * FROM SensorData WHERE sensor_id IN ({}) AND timestamp >= ? AND timestamp <= ?".format(','.join('?'*len(sensor_id))), (*sensor_id, start, to))
    sensor_data = cursor.fetchall()

    # Convertimos los resultados a objetos SensorData
    sensor_data_list = []
    for row in sensor_data:
        sensor = SensorData(
            sensor_data_id=row[0],
            sensor_id=row[1],
            variable1=row[2],
            variable2=row[3],
            timestamp=row[4]
        )
        sensor_data_list.append(sensor)
    db.close()
    if(len(sensor_data_list) == 0):
        return HTTPException(status_code=404)
    return sensor_data_list

@app.delete("/api/v1/sensor/{sensor_id}")
async def delete_sensor(sensor_id: int, request: Request):
    db = sqlite3.connect("database.db")
    
    # Verificamos la clave API de la compañía
    api_key = request.headers.get('company_api_key')
    cursor = db.execute("SELECT * FROM Company WHERE company_api_key=?", (api_key,))
    company = cursor.fetchone()
    if not company:
        raise HTTPException(status_code=401, detail="Clave API inválida.")
    
    # Verificamos si el sensor existe
    cursor = db.execute("SELECT * FROM Sensor WHERE sensor_id=?", (sensor_id,))
    sensor = cursor.fetchone()
    if not sensor:
        raise HTTPException(status_code=404, detail="Sensor no encontrado.")
    
    # Eliminamos el sensor de la base de datos
    db.execute("DELETE FROM Sensor WHERE sensor_id=?", (sensor_id,))
    
    # Guardamos los cambios
    db.commit()
    db.close()
    
    return {"status_code": 200, "detail": "Sensor eliminado exitosamente"}