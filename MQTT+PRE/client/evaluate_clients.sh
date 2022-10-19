#!/bin/bash

killall -9 python3
echo -n "" > n_of_subs.txt



echo "Removing Last Evaluation ..."

rm -rf evaluation/delay*
rm -rf evaluation/start*
rm -rf evaluation/end*



#python3 broker-reencription-subA.py &
python3 broker-reencription-subB.py &




#header for delay file
sleep 4

echo "PID, Clients, Delay (ms)" >> evaluation/delay.csv
echo -n "8 Pubs and Subs " > n_of_subs.txt


for i in {1..4}
do
    #process client
    #python3 sub_re_enc_TOPIC_A.py  &
    python3 sub_re_enc_TOPIC_B.py  &

done



#for TPS calculation
echo "Starting 4 Publisher and Subscribers Evaluation ... "
sleep 3

python3 start_evaluation_time.py
for i in {1..4}
do
    #process client
    ./run_publisher.sh &

done




