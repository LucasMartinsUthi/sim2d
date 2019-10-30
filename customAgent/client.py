#!/usr/bin/env python3

import threading
import time
import getch

import sock

class Agent:
    def __init__(self):
        self.__connected = False
        self.__parsing = False
        self.__sock = None
        self.__thinking = False
        self.__think_thread = None

    def connect(self, host, port, teamname, version = 11):
        self.__sock = sock.Socket(host, port)

        init_address = self.__sock.address
        init_msg = "(init %s (version %d))"
        self.__sock.send(init_msg % (teamname, version))

        self.__sock.send("move(0 0)")

        while self.__sock.address == init_address:
            time.sleep(0.0001)

        self.__thinking = False
        self.__think_thread = threading.Thread(target = self.__think_loop, name = "think_loop")
        self.__think_thread.daemon = True

    def play(self):
        print("play")
        self.__thinking = True
        self.__think_thread.start()

    def __think_loop(self):
        print("think loop", self.__thinking)
        while self.__thinking:
            key = getch.getch()

            if key == 'w':
                self.__sock.send("(dash 100)")
            elif key == 's':
                self.__sock.send("(dash -100)")
            elif key == 'a':
                self.__sock.send("(turn -20)")
            elif key == 'd':
                self.__sock.send("(turn 20)")

a = Agent()
a.connect('localhost', 6000, 'Lucas')
a.play()
