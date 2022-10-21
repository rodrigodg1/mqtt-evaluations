#!/bin/bash

killall -9 python3
killall node
echo -n "" > n_of_subs.txt



echo "Removing Last Evaluation ..."
sleep 3

rm -rf evaluation/delay*
rm -rf evaluation/start*
rm -rf evaluation/end*



#python3 broker-reencription-subA.py &
python3 broker-reencription-subB.py &


#echo "Starting 4 Publisher and Subscribers Evaluation ... "

#header for delay file

echo "Delay (s)" >> evaluation/delay.csv
#echo -n "4 Pubs and Subs " > n_of_subs.txt
sleep 4



START=1
N_PUB_SUB=16



echo "Starting Subs..."
for (( c=$START; c<=$N_PUB_SUB; c++ ))
do
    #process client
    #python3 sub_re_enc_TOPIC_A.py  &
    python3 sub_re_enc_TOPIC_B.py  &

done
sleep 4


echo "Server and Verifier..."
#run bbs-server and verifier process
./run_server-and-verifier.sh

sleep 10


echo "Starting evaluation..."

sleep 2
python3 start_evaluation_time.py
for (( c=$START; c<=$N_PUB_SUB; c++ ))
do
    #process client
    ./run_publisher.sh &
    #python3 publisher.py 


done





