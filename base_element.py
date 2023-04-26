import numpy as np
import yaml
import os
import threading
import time
from matplotlib import pyplot as plt

class BaseElement(object):
    def __init__(self,name,T_step,file):
        self.name = name
        self.T_step = T_step
        self.load_conf(file)
        # log
        self.time_list = []
        self.input_list = []
        self.output_list = []
        # 
        self.input = 0
        self.output = 0
        return
    
    def load_conf(self,file):
        self.model_conf = dict()
        with open(file) as f:
            data = yaml.load_all(f)
            for d in data:
                self.model_conf.update(d)
        print("model_conf: ",self.model_conf)
    
    def update_input(self,input):
        self.input = input
        return

    def get_output(self):
        return self.output
    
    def loop_thread(self):
        while self.is_running:
            self.run_once()
            self.log()
            time.sleep(self.T_step)
        return
    
    def run_once(self):
        pass
            
    def thread_start(self):
        self.is_running = True
        t = threading.Thread(target=self.loop_thread)
        t.daemon = True
        t.start()
        return

    def stop_thread(self):
        self.is_running = False
        return

    def log(self):
        self.time_list.append(time.time())
        self.input_list.append(self.input)
        self.output_list.append(self.output)
        return

    def plot_data(self):
        plt.figure()
        plt.title(self.name)
        plt.plot(self.time_list,self.input_list,label='input')
        plt.plot(self.time_list,self.output_list,label='output')
        plt.grid()
        plt.legend()
        return