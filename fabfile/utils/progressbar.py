import sys
import time
import threading

class progress_bar_loading(threading.Thread):

    def __init__(self, stop, kill, message):
        super(progress_bar_loading, self).__init__()
        self.stop = False
        self.kill = False
        self.message = message

    def run(self):

        print self.message,
        sys.stdout.flush()
        i = 0
        while self.stop != True:
                if (i%4) == 0:
                    sys.stdout.write('\b/')
                elif (i%4) == 1:
                    sys.stdout.write('\b-')
                elif (i%4) == 2:
                    sys.stdout.write('\b\\')
                elif (i%4) == 3:
                    sys.stdout.write('\b|')

                sys.stdout.flush()
                time.sleep(0.2)
                i+=1

        if self.kill == True:
            print '\b\b\b\b ABORT!'
        else:
            print '\b\b done!'


# kill = False
# stop = False
# p = progress_bar_loading(stop, kill)
# p.start()
#
# try:
#     #anything you want to run.
#     time.sleep(10)
#     p.stop = True
# except KeyboardInterrupt or EOFError:
#      p.kill = True
#      p.stop = True