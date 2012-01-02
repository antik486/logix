from __future__ import with_statement
import os, ConfigParser

from kombu import BrokerConnection
from kombu.utils.debug import setup_logging

setup_logging(loglevel="INFO")

config_file = '../etc/logix.conf'
if not os.path.isfile(config_file):
    print "Config file %s not found" % config_file
    sys.exit(1)

config = ConfigParser.RawConfigParser()
config.read(config_file)

with BrokerConnection(config.get('transport','url')) as conn:
    with conn.SimpleQueue(config.get('transport', 'queue'), serializer="json",
            compression="zlib") as queue:
        message = queue.get(block=True, timeout=10)
        if message:
            print message.payload
            message.ack()

