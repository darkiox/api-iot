import sqlite3

# Conectamos a la base de datos
conn = sqlite3.connect('database.db')

#conn.execute('''INSERT INTO Sensor (sensor_id, location_id, sensor_name, sensor_category, sensor_api_key) VALUES
#(4, 1, 'Temperature', 'Environmental', '1'),
#(5, 1, 'Humidity', 'Environmental', '2'),
#(6, 2, 'Pressure', 'Environmental', '3');
#''')


#conn.execute('''INSERT INTO SensorData (sensor_data_id, sensor_id, variable1, variable2, timestamp) VALUES
#(7, 4, 61.0, 39.5, 1621977000),
#(8, 5, 1000.0, 0, 1621976400),
#(9, 6, 1001.0, 0, 1621977000),
#(10, 6, 100341, 10, 1621979000);
#''')
#conn.execute('''INSERT INTO Company (company_id, company_name, company_api_key) VALUES (3, 'Testing', 'Testing')''')
#conn.execute('''INSERT INTO Location (location_id, company_id, location_name, location_api_key) VALUES
#(4, 3, 'Testing', 'Testing');''')
# Creamos la tabla Admin
conn.execute('''CREATE TABLE IF NOT EXISTS Admin
             (username TEXT NOT NULL,
             password TEXT NOT NULL);''')
conn.execute('''INSERT INTO Admin (username, password) VALUES ('admin', 'password');''')
conn.commit()
conn.close()
