import time
import json
from websocket import create_connection
import variables
from utils import init_logger
import logging
from agent import takeAction
import sys 

ws = ""

def doListen():
    try:
        global ws
        ws = create_connection(variables.url)
        ws.send(json.dumps({
            "eventName": "join",
            "data": {
                "playerName": variables.player_name,
                "playerNumber": variables.player_number, 
                "token": variables.token
            }
        }))
        while True:
            result = ws.recv()
            msg = json.loads(result)
            takeAction(ws, msg)
    except Exception as e:
        logging.error(e)
        doListen()


if __name__ == '__main__':


    init_logger()

    logging.debug('arg:{} len:{}'.format(sys.argv,len(sys.argv)))
    if len(sys.argv) == 5:
         variables.player_name=sys.argv[1]
         variables.player_number=sys.argv[2]
         variables.token=sys.argv[3]
         variables.url=sys.argv[4]

    logging.debug('player_name:{} player_number:{} token:{} url:{}'.format(variables.player_name,variables.player_number,variables.token,variables.url))
    try:
        doListen()
    except KeyboardInterrupt:
        logging.error("Exit by keyboard")
