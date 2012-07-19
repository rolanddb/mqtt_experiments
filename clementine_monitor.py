import mosquitto
import os
import time
import dbus

broker = "127.0.0.1"
port = 1883
topic = "music/nowplaying"

mypid = os.getpid()
client_uniq = "pubclient_"+str(mypid)
mqttc = mosquitto.Mosquitto(client_uniq)

#connect to broker
mqttc.connect(broker, port, 60)

# Clementine lives on the Session bus
session_bus = dbus.SessionBus()

# Get Clementine's player object, and then get an interface from that object,
# otherwise we'd have to type out the full interface name on every method call.
player = session_bus.get_object('org.mpris.clementine', '/Player')
iface = dbus.Interface(player, dbus_interface='org.freedesktop.MediaPlayer')

previous_metadata = 1

#remain connected and publish
while mqttc.loop() == 0:
    metadata = iface.GetMetadata()
    if metadata != previous_metadata:
        # new song is playing
        msg = "playing {0} - {1}".format(metadata["artist"], metadata["title"])
	print msg
        mqttc.publish(topic, msg)
        print "message published on topic " + topic
    else:
        # same song
        print "still " + msg
    time.sleep(10)
    previous_metadata = metadata
    pass
