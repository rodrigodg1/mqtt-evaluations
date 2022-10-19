In the mosquitto server:

```
cd server/
```

run the config. file  [`server-config.conf`]:


```
mosquitto -c server-config.conf
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
python3 tps.py
```