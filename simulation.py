from pure_delay_element import PureDelayElement
from first_order_inertial_element import FirstOrderInertialElement
from pid_controller import PID
from matplotlib import pyplot as plt
import time
import numpy as np

modules_dict = {
                "pure_delay":PureDelayElement(),
                "first_order":FirstOrderInertialElement(),
                "PID":PID()
                }

class Simulation(object):
    def __init__(self):
        self.input = 0
        self.output = 0
        return

    def run_once(self,loop=False):
        if loop:
            output = [self.input,self.output]
        else:
            output = self.input

        for module in self.modules_list:
            self.modules_dict[module].update_input(output)
            output = self.modules_dict[module].get_output()
        self.output = output
        return

    def update_input(self,input):
        self.input = input
        return

    def get_output(self):
        return self.output
    
    def build_up_system(self,modules_list,modules_dict):
        self.modules_list = modules_list
        self.modules_dict = modules_dict
        return

    def start_modules(self):
        for key in self.modules_dict:
            print(key)
            self.modules_dict[key].thread_start()
        return

    def stop_modules(self):
        for key in self.modules_dict:
            self.modules_dict[key].stop_thread()
        return
    
    def simulate(self,modules_list,modules_plot,is_close_system,count,T_s=0.01):
        self.build_up_system(modules_list,modules_dict)
        input_list = []
        output_list = []
        time_list = []

        self.start_modules()
        time_start = time.time()
        for i in np.arange(count):
            u = 1
            time_now = time.time()
            self.update_input(u)
            self.run_once(loop=is_close_system)
            output = self.get_output()
            time_list.append(time_now-time_start)
            input_list.append(u)
            output_list.append(output)
            time.sleep(T_s)

        self.stop_modules()
        plt.title('simulation')
        plt.plot(time_list,input_list,label='input')
        plt.plot(time_list,output_list,label='output')
        plt.grid()
        plt.legend()
        for module in modules_plot:
            modules_dict[module].plot_data()

        plt.grid()
        return

    def test(self):
        modules_plot = ["PID","pure_delay","first_order"]
        modules_list = ["PID","pure_delay","first_order"]
        self.simulate(modules_list,modules_plot,True,600)
        return
    
    def test2(self):
        modules_plot = ["pure_delay","first_order"]
        modules_list = ["pure_delay","first_order"]
        self.simulate(modules_list,modules_plot,False,600)
        return

def main():
    simu = Simulation()
    simu.test()
    plt.show()

if __name__ == '__main__':
    main()