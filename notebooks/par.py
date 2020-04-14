import ipyparallel as PP

RC=PP.Client(profile='pb_parallel')
d_view=RC[:]
lb_view = RC.load_balanced_view()
lb_view.block = True
x=file("../env.py",'r').read()
d_view.execute(x)

#import datetime
#print "Start ... ", datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S"), "tasks = ",len(WORK0)

#shuffle(WORK0)

#print "DB.httr_cr_v1", DB.httr_cr_fp.count()
#print "End ", datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S"), "tasks = ",len(WORK0)

