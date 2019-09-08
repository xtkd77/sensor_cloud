
# Preparation

### Install Paho-mqtt

'''
python3 -m pip install paho-mqtt
'''

### Prevent suspend when raptop PC cover is wrapped.
 
-  Set the value of HandleLidSwitch "ignore", not "snspend"

'''/etc/systemd/logind.conf
HandleLidSwitch=ignore
'''

- Restart the login:
'''
sudo systemctl restart systemd-logind
'''

### plot

- prepare data:

'''
cat test_connection/*.log | grep -v  ^d > tmp.csv
python3 plot_csv.py tmp.csv
'''
