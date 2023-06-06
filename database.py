import sqlite3

# Conectamos a la base de datos
conn = sqlite3.connect('database.db')

# Creamos la tabla Admin
conn.execute('''CREATE TABLE IF NOT EXISTS Admin
             (username TEXT NOT NULL,
             password TEXT NOT NULL);''')

# Creamos la tabla Company
conn.execute('''CREATE TABLE IF NOT EXISTS Company
             (company_id INTEGER PRIMARY KEY AUTOINCREMENT,
             company_name TEXT NOT NULL,
             company_api_key TEXT NOT NULL);''')

# Creamos la tabla Location
conn.execute('''CREATE TABLE IF NOT EXISTS Location
             (location_id INTEGER PRIMARY KEY AUTOINCREMENT,
             company_id INTEGER NOT NULL,
             location_name TEXT NOT NULL,
             location_country TEXT NOT NULL,
             location_city TEXT NOT NULL,
             location_meta TEXT NOT NULL,
             location_api_key TEXT NOT NULL,
             FOREIGN KEY (company_id) REFERENCES Company(company_id));''')

# Creamos la tabla Sensor
conn.execute('''CREATE TABLE IF NOT EXISTS Sensor
             (sensor_id INTEGER PRIMARY KEY AUTOINCREMENT,
             location_id INTEGER NOT NULL,
             sensor_name TEXT NOT NULL,
             sensor_category TEXT NOT NULL,
             sensor_meta TEXT,
             sensor_api_key TEXT NOT NULL,
             FOREIGN KEY (location_id) REFERENCES Location(location_id));''')

# Creamos la tabla SensorData
conn.execute('''CREATE TABLE IF NOT EXISTS SensorData
             (sensor_data_id INTEGER PRIMARY KEY AUTOINCREMENT,
             sensor_id INTEGER NOT NULL,
             variable1 REAL NOT NULL,
             variable2 REAL NOT NULL,
             timestamp INTEGER NOT NULL,
             FOREIGN KEY (sensor_id) REFERENCES Sensor(sensor_id));''')


conn.execute('''INSERT INTO Company (company_id, company_name, company_api_key) VALUES
(1, 'ACME Inc.', '7d5c5d5e-7f5c-4d5c-8d5c-5d5e7f5c5d5e'),
(2, 'XYZ Corp.', '5e7f5c5-5c7d-4e5c-9d5c-7f5c5d5e7f5c'),
(3, 'Testing', 'Testing');''')

conn.execute('''INSERT INTO Location (location_id, company_id, location_name, location_country, location_city, location_meta, location_api_key) VALUES
(1, 1, 'Main Office', 'Chile', 'Santiago' ,'SCL', '5c5d5e7f-7f5c-5d5e-7f5c-5d5e7f5c5d5e'),
(2, 1, 'Warehouse', 'Chile', 'Santiago' ,'SCL', '75c5d5e-5c7d-5e7f-c7d-5e75c5d5e7f'),
(3, 2, 'Headquarters', 'Estados Unidos', 'Texas' ,'TX', '5d5e7f5c-7f5c-5d5e-7f5c-5d5e7f5c5d5e');
''')

conn.execute('''INSERT INTO Sensor (sensor_id, location_id, sensor_name, sensor_category, sensor_api_key) VALUES
(1, 1, 'Temperature', 'Environmental', 'sensor1'),
(2, 1, 'Humidity', 'Environmental', 'sensor2'),
(3, 2, 'Pressure', 'Environmental', 'sensor3');
''')

conn.execute('''INSERT INTO SensorData (sensor_data_id, sensor_id, variable1, variable2, timestamp) VALUES
(1, 1, 25.5, 50.0, 1621976400),
(2, 1, 26.0, 49.5, 1621977000),
(3, 2, 60.0, 40.0, 1621976400),
(4, 2, 61.0, 39.5, 1621977000),
(5, 3, 1000.0, 0, 1621976400),
(6, 3, 1001.0, 0, 1621977000);
''')

conn.execute('''INSERT INTO Admin (username, password) VALUES ('admin', 'password');''')
# Guardamos los cambios y cerramos la conexión
conn.commit()
conn.close()
