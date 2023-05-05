
Team Members:
Eric Chen

List of External Libraries:

rpi side:
- time
- grovepi
- paho-mqtt

laptop side:
- flask
- paho-mqtt
- web

Notes before compilation:
- sensor.py will only run a rpi becuase the grovepi library only runs without error on a rpi
- make sure the default 5000 port is not used for the machine running web.py

Commands to use before compilation:
On the computer side:
- export FLASK_APP=web
- flask run

On the rpi side:
- python sensor.py

Use your web browser and enter the local host address, and the process will start as shown in the
videos. For every new query click the refresh button on the local host web page.

Demo Video Links:
- Full Demo Video for first 4 parts on the rubric: https://youtu.be/Bi8DUGcrLlE
- Basic Query Demonstration: https://youtube.com/shorts/K3O9U-_9BSQ
- Adjusting the response speed: https://youtube.com/shorts/hdKfjMennH8
