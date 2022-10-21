#!/bin/bash

killall python3
echo -n "" > n_of_subs.txt



echo "Removing Last Evaluation ..."


rm -rf evaluation/delay*
rm -rf evaluation/start*
rm -rf evaluation/end*

sleep 3


#header for delay file
echo "Delay (ms)" >> evaluation/delay.csv
#echo -n "8 Pubs and Subs " > n_of_subs.txt


START=1
N_PUB_SUB=16

for (( c=$START; c<=$N_PUB_SUB; c++ ))
do
    #process client
    python3 subscriber.py  &
    #./run_publisher.sh &


done


echo "Starting ${N_PUB_SUB} Publisher and Subscribers Evaluation ... "


sleep 4


python3 start_evaluation_time.py
for (( c=$START; c<=$N_PUB_SUB; c++ ))
do
    #process client
    ./run_publisher.sh &

done




