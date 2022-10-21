import paho.mqtt.client as mqtt
import pickle
import pprint
import json
from datetime import datetime
from umbral import generate_kfrags
from umbral import encrypt, decrypt_original, reencrypt
from umbral import SecretKey, Signer
from umbral import decrypt_reencrypted
import time

broker = "localhost"
broker_port = 8883


# The callback for when the client receives a CONNACK response from the server.
def on_connect(client, userdata, flags, rc):
    print("Connected with result code "+str(rc))

    # Subscribing in on_connect() means that if we lose the connection and
    # reconnect then subscriptions will be renewed.
    #client.subscribe("temp_with_suburb")
    client.subscribe("temp_with_gps_re")

    

def get_current_time():
    return time.time()

#is delegation key send via particular topic between pre and publisher ?
def on_message(client, userdata, msg):

    alices_secret_key = SecretKey.random()
    alices_public_key = alices_secret_key.public_key()

    alices_signing_key = SecretKey.random()
    alices_signer = Signer(alices_signing_key)
    alices_verifying_key = alices_signing_key.public_key()

    # Generate Umbral keys for Sub B.
    sub_b_secret_key = SecretKey.random()
    sub_b_public_key = sub_b_secret_key.public_key()



    #print(msg.topic+" "+str(msg.payload))
    received_data = json.loads(msg.payload)
    #print("RECEIVED DATA: ", received_data)


    temperature = received_data['Temperature_ReEnc']
    #capsule_temp = received_data['Capsule_Temperature']
    lat_gps = received_data['GPS_Lat_ReEnc']
    #capsule_gps_lat = received_data['Capsule_GPS_lat']
    long_gps = received_data['GPS_Long_ReEnc']
    #capsule_gps_long = received_data['Capsule_GPS_long']
    suburb = received_data['Suburb_ReEnc']
    #capsule_sub_urb = received_data['Capsule_Suburb']
    #proof_all_items = all_data['Proof_All_Items']
    #publisher_time_stamp = received_data['Publisher_Timestamp']
    
    #server_label = all_data['Server']

    #pprint.pprint(received_data)

    publisher_start_time = received_data['Publisher_Timestamp']


    # Encrypt data with Alice's public key.

    temperature = '78'
    temperature = temperature.encode()

    GPS_Lat = '30'
    GPS_Lat = GPS_Lat.encode()

    GPS_Long = '123'
    GPS_Long = GPS_Long.encode()

    Suburb = '2398'
    Suburb = Suburb.encode()

    capsule_temp, temp_ciphertext = encrypt(alices_public_key, temperature)
    capsule_gps_lat, gps_lat_ciphertext = encrypt(alices_public_key, GPS_Lat)
    capsule_gps_long, gps_long_ciphertext = encrypt(alices_public_key, GPS_Long)
    capsule_suburb, suburb_ciphertext = encrypt(alices_public_key, Suburb)
    # Decrypt data with Alice's private key.
    #cleartext = decrypt_original(alices_secret_key, capsule, ciphertext)

    
    # create a delegation key for sub B
    kfrags_sub_B = generate_kfrags(delegating_sk=alices_secret_key,
                                receiving_pk=sub_b_public_key,
                                signer=alices_signer,
                                threshold=1,
                                shares=1)



    cfrags_temp = list()          
    for kfrag_sub_B in kfrags_sub_B[:1]:
        cfrag = reencrypt(capsule=capsule_temp, kfrag=kfrag_sub_B)
        cfrags_temp.append(cfrag)    


    cfrags_gps_lat = list()          
    for kfrag_sub_B in kfrags_sub_B[:1]:
        cfrag = reencrypt(capsule=capsule_gps_lat, kfrag=kfrag_sub_B)
        cfrags_gps_lat.append(cfrag)    


    cfrags_gps_long = list()          
    for kfrag_sub_B in kfrags_sub_B[:1]:
            cfrag = reencrypt(capsule=capsule_gps_long, kfrag=kfrag_sub_B)
            cfrags_gps_long.append(cfrag)    


    cfrags_suburb = list()          
    for kfrag_sub_B in kfrags_sub_B[:1]:
            cfrag = reencrypt(capsule=capsule_suburb, kfrag=kfrag_sub_B)
            cfrags_suburb.append(cfrag)   




    temp_cleartext = decrypt_reencrypted(receiving_sk=sub_b_secret_key,
                                        delegating_pk=alices_public_key,
                                        capsule=capsule_temp,
                                        verified_cfrags=cfrags_temp,
                                        ciphertext=temp_ciphertext)

    gps_lat_cleartext = decrypt_reencrypted(receiving_sk=sub_b_secret_key,
                                        delegating_pk=alices_public_key,
                                        capsule=capsule_gps_lat,
                                        verified_cfrags=cfrags_gps_lat,
                                        ciphertext=gps_lat_ciphertext)

    gps_long_cleartext = decrypt_reencrypted(receiving_sk=sub_b_secret_key,
                                        delegating_pk=alices_public_key,
                                        capsule=capsule_gps_long,
                                        verified_cfrags=cfrags_gps_long,
                                        ciphertext=gps_long_ciphertext)

    suburb_cleartext = decrypt_reencrypted(receiving_sk=sub_b_secret_key,
                                        delegating_pk=alices_public_key,
                                        capsule=capsule_suburb,
                                        verified_cfrags=cfrags_suburb,
                                        ciphertext=suburb_ciphertext)




    end_time = get_current_time()
    delay = end_time - publisher_start_time



    f = open("evaluation/delay.csv", "a")
    f.write(str(round(delay,3)))
    f.write("\n")
    f.close()




    #end time of received transaction
    f = open("evaluation/end_evaluation_time.txt", "a")
    f.write(str(end_time))
    f.write("\n")
    f.close()


    
    #print(n_of_subs_delay_ms)


client = mqtt.Client()
client.on_connect = on_connect
client.on_message = on_message

client.connect(broker, broker_port, 60)

# Blocking call that processes network traffic, dispatches callbacks and
# handles reconnecting.
# Other loop*() functions are available that give a threaded interface and a
# manual interface.
client.loop_forever()