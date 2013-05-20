import sys
import subprocess
from retask.queue import Queue
from retask.task import Task


def system(cmd):
    """
    Invoke a shell command.
    """
    ret = subprocess.Popen(cmd, shell=True, stdin=sys.stdin,
                stdout=subprocess.PIPE, stderr=subprocess.PIPE, close_fds=True)
    out, err = ret.communicate()
    return out, err


def update(data):
    '''
    Updates the git repo for  the given user

    :arg user: github username
    :arg repo: Code repo name
    '''
    queue = Queue('puluupdates')
    if not queue.connect():
        return

    task = Task(data=data, raw=True)
    queue.enqueue(task)
