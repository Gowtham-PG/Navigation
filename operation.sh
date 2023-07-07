#!/bin/bash

# Open a new terminal window and run land1.py command
gnome-terminal --tab --title="land1.py" --command="bash -c 'dronekit-sitl copter --home=12.9714906,80.0439110,123,354 -I1'"

# Open a new terminal window and run land11.py command
#gnome-terminal --tab --title="land11.py" --command="bash -c 'dronekit-sitl copter --home=26.9890221,80.8928812,123,354 -I2'"

# Open a new terminal window and run land111.py command
gnome-terminal --tab --title="land111.py" --command="bash -c 'dronekit-sitl copter --home=12.9711168,80.0440103,123,354 -I3'"

# Open a new terminal window and run land111.py command
#gnome-terminal --tab --title="land111.py" --command="bash -c 'dronekit-sitl copter --home=26.98831348,80.9043207764626,123,354 -I4 '"

# Open a new terminal window and run land1.py command
gnome-terminal --tab --title="land1.py" --command="bash -c 'mavproxy.py --master tcp:127.0.0.1:5770 --out 192.168.81.48:14550'"

# Open a new terminal window and run land11.py command
#gnome-terminal --tab --title="land11.py" --command="bash -c 'mavproxy.py --master tcp:192.168.81.48:15000 --out 192.168.81.105:14560'"

# Open a new terminal window and run land111.py command
gnome-terminal --tab --title="land111.py" --command="bash -c 'mavproxy.py --master tcp:127.0.0.1:5790 --out 192.168.81.48:14570'"

# Open a new terminal window and run land111.py command
#gnome-terminal --tab --title="land111.py" --command="bash -c 'mavproxy.py --master tcp:127.0.0.1:5800 --out 192.168.81.48:14580'"