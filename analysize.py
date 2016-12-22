#!/bash/python

import os
import sys
import json
from getopt import getopt, GetoptError
from subprocess import Popen, PIPE


def usage():
    print '''usage:      analysize [-n|-h]
            -n      task name
            -h      help'''
    exit(1)

def format_print(task_info):
    if type(task_info)!= dict:
        print "task info error1"
    else:
        title = ['state', 'retval/exc']
        print "%5s %15s\n" %(title[0], title[1])
        try:
            print "%5s %15s\n" %(task_info['state'], task_info['retval/exc'])
        except KeyError:
            print "task info error2"

if __name__ == '__main__':
    rdb_path = 'rdb'
    dump_path = 'local_test/dump.rdb'
    # check .rdb file exist
    if os.path.exists(dump_path) != True:
        print "%s not exists" % dump_path
        exit(1)

    cmd = "%s --command json %s" % (rdb_path, dump_path)
    args = cmd.split(' ')
    p = Popen(args, stdout=PIPE, stderr=PIPE)
    (out, error) = p.communicate()
    out =  eval(out)

    success_list = []
    fail_list = []
    task_list = []
    if len(out) == 0:
        print "jobs are pending"
    elif len(out) == 1:
        all_infos = out[0]
        if 'success_list' in all_infos:
            success_list = all_infos['success_list']
        if 'fail_list' in all_infos:
            fail_list = all_infos['fail_list']
        if 'tasks_info' in all_infos:
            task_list = all_infos['tasks_info']
    else:
        pass
    success_task_id = []
    task_infos = {}
    # remove duplicate
    success_list = list(set(success_list))
    fail_list = list(set(fail_list))
    # task info joint
    for success_task in success_list:
        success_task = eval(success_task)
        task_id = success_task['task_id']
        task_retval = success_task['retval']
        success_task_id.append(task_id)
        for task in task_list:
            task = eval(task)
            if task_id == task['task_id']:
                task_info = {'task_id': task_id,
                             'task_cmd': task['task_cmd'],
                             'state':'success',
                             'retval/exc': task_retval}
                task_infos[task['task_name']] = task_info
    for fail_task in fail_list:
        fail_task = eval(fail_task)
        task_id = fail_task['task_id']
        task_exc = fail_task['exc']
        if fail_task['task_id'] in success_task_id:
            continue
        else:
            for task in task_list:
                task = eval(task)
                if task_id == task['task_id']:
                    task_info = {'task_id': task_id,
                                 'task_cmd': task['task_cmd'],
                                 'state':'success',
                                 'retval/exc': task_retval}
                    task_infos[task['task_name']] = task_info

    try:
        opts, args = getopt(sys.argv[1:], "hn:", ["task_name=", "help"])
        if len(opts) == 0:
            print 'success tasks  %d, fail tasks %d' %(len(success_list),len(fail_list))
        else:
            for opt, argv in opts:
                if opt in ('-h', "--help"):
                    usage()
                elif opt in ('-n', "--task_name"):
                    if argv in task_infos:
                        format_print(task_infos[argv])
                    else:
                        print "task name erroe"
                else:
                    pass
    except GetoptError:
        usage()