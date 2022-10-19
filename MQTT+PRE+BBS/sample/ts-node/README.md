# BBS-MQTT-PRE

The publisher sends a document (inputDocument) to the server with the following items to the "signature_data" topic:

- "Temperature",
- "GPS_Lat"
- "GPS_Long"
- "Suburb"

The server received the data and creates a two diferent versions in topics:

- Topic 1: temp_with_gps


Subscribers receive the Topic 1 with all informations (i.e., temperature, GPS_Lat, GPS_Long, and Suburb)


## Instructions

Install MQTT:

```
npm install mqtt --save
```


Install dependencies:

```
npm install
```

Install mosquitto:

```
sudo apt-get install mosquitto
```

In the mosquitto server:

```
cd server/
```

run the config. file  [`without-tls-server.conf`]:



```
mosquitto -c without-tls-server.conf
```


for automated evaluation, run:

```
cd client/
chmod +x evaluate_clients.sh
./evaluate_clients.sh
```

The evaluation results will be saved in the `client/evaluation` directory

To calculate TPS and Total Delay, run:

```
cd client/

python3 tps.py
```