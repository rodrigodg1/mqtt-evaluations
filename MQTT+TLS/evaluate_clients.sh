#!/bin/bash

killall python3
echo -n "" > n_of_subs.txt



echo "Removing Last Evaluation ..."


rm -rf evaluation/delay*
rm -rf evaluation/start*
rm -rf evaluation/end*

sleep 3


#header for delay file
echo "PID, Clients, Delay (ms)" >> evaluation/delay.csv
echo -n "8 Pubs and Subs " > n_of_subs.txt





#18 subs process
for i in {1..4}
do
    #process client
    python3 subscriber.py  &
    #./run_publisher.sh &


done



echo "Starting 4 Publisher and Subscribers Evaluation ... "


sleep 4


python3 start_evaluation_time.py
for i in {1..4}
do
    #process client
    ./run_publisher.sh &

done




