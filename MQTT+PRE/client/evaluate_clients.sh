#!/bin/bash

killall -9 python3
echo -n "" > n_of_subs.txt



echo "Removing Last Evaluation ..."
rm -rf evaluation/delay*
rm -rf evaluation/start*
rm -rf evaluation/end*


echo "Starting re-encryption process code"
#python3 broker-reencription-subA.py &
python3 broker-reencription-subB.py &

sleep 4


echo "Delay (s)" >> evaluation/delay.csv
#echo -n "{$N_CLIENTS} Pubs and Subs " > n_of_subs.txt

START=1
N_PUB_SUB=16





for (( c=$START; c<=$N_PUB_SUB; c++ ))
do
    #process client
    #python3 sub_re_enc_TOPIC_A.py  &
    python3 sub_re_enc_TOPIC_B.py  &

done




echo "Starting ${N_PUB_SUB} Publisher and Subscribers Evaluation ... "
sleep 3

#for TPS calculation
python3 start_evaluation_time.py
for (( c=$START; c<=$N_PUB_SUB; c++ ))
do
    #process client
    echo $i
    ./run_publisher.sh &


done




