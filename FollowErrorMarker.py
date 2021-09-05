from math import fabs, sin
import numpy as np

class MarkFollowError:
    def __init__(self):
        self.data1 = []
        self.data2 = []
        self.max_error = 0
        self.window = 0
        self.__error_flag = []
        self.__sample_size = 0
    
    def setError(self, error):
        self.max_error = error
    
    def setWindow(self, window):
        self.window = window

    def appendData1(self, data1):
        self.data1 += data1

    def appendData2(self, data2):
        self.data2 += data2

    def _freshErrorFlag(self):
        self.__error_flag.clear()
        self.__sample_size = min(len(self.data1), len(self.data2))
        for i in range(0, self.__sample_size):
            if fabs(self.data2[i] - self.data1[i]) > self.max_error:
                self.__error_flag.append(True)
            else:
                self.__error_flag.append(False)
    
    def markStart(self, pos):
        pass
    
    def markEnd(self, pos):
        pass
    
    def markTrue(self, pos):
        pass
    
    def markFalse(self, pos):
        pass
    
    def markFollowError(self):
        self._freshErrorFlag()
        error_continue = True
        error_start_flag = False
        for i in range(0, len(self.__error_flag)):
            # fresh the flag
            error_continue = error_continue and self.__error_flag[i]
            if error_continue:
                # draw a short v line to mark "True"
                self.markTrue(i)
                # jump to next cycle if error keep "True" continuously for more than time which windows set
                if error_start_flag:
                    continue
                # to avoid cross the boader
                if i < len(self.__error_flag) - self.window:
                    for p in range(i + 1, i + self.window):
                        error_continue = error_continue and self.__error_flag[p]
                    if error_continue:
                        error_start_flag = True
                        # draw a v line to mark "error start"
                        self.markStart(i)
                    else:
                        error_continue = True
                        continue
            else:
                # draw a short v line to mark "False"
                self.markFalse(i)
                # if this is the first "False" after "error start", draw a line to mark "error end"
                if error_start_flag:
                    self.markEnd(i)
                error_start_flag = False
                error_continue = True
                continue    

import matplotlib.pyplot as plt
class PlotFollowError(MarkFollowError):
    def __init__(self):
        super().__init__()

    def markStart(self, pos):
        plt.vlines(pos, -5, 5, colors = "red", linestyles = "dashed")
            
    def markEnd(self, pos):
        plt.vlines(pos, -5, 5, colors = "green", linestyles = "dashed")
    
    def markTrue(self, pos):
        plt.vlines(pos, 6, 8, colors = "c", linestyles = "dashed")
    
    def markFalse(self, pos):
        plt.vlines(pos, -8, -6, colors = "c", linestyles = "dashed")
        
    def plotCurve(self):
        plt.plot(range(0,len(self.data1)),self.data1)
        plt.plot(range(0,len(self.data2)),self.data2)

    def show(self):
        plt.show()

x = range(0,200)
y = []
y_r = []
for i in x:
    y.append(sin(i) + np.random.normal(0,0.8)) 
    y_r.append(sin(i))

test = PlotFollowError()
test.setError(0.1)
test.setWindow(5)
test.appendData1(y)
test.appendData2(y_r)
test.plotCurve()
test.markFollowError()
test.show()