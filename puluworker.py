import os
import shutil
import codecs
from retask.queue import Queue
from retask.task import Task
from pprint import pprint
from datetime import datetime
from pulu.utils import system
from pulu.system import create_task


def get_timestamp():
    '''
    Returns the current time as string.
    '''
    d = datetime.now()
    return d.strftime('%Y%m%d-%H%M%S')


def get_commits_text(commits):
    '''
    Returns nice unicode representation of the commits
    '''
    msg = u'''\n
Commit details
===============
'''
    for c in commits:
        text = u'\n`%s <%s>`_ Timestamp: %s\n::\n\n' % (c['id'], c['url'], c['timestamp'])
        msg += text
        for line in c['message'].split('\n'):
            msg += u'\t%s\n' % line

    return msg


def blog_post(user, name, path, commits):
    '''
    Convert the given path into a blog post.

    :arg user: User who is posting
    :arg name: Name of the problem/directory
    :arg path: Path to the git source.
    :arg commits: Github commit details
    '''
    text = u''
    if commits:
        commits.reverse()
    system('pushd .;cd gitsources/%s;git pull;popd' % user)
    fpath = os.path.join(path, 'solution.rst')
    if os.path.exists(fpath):
        # First remove the old listing directory
        try:
            shutil.rmtree(os.path.join('2013/listings/', user, name))
        except OSError as e:
            print e
        # Then copy the directory to the listing
        shutil.copytree(path, '2013/listings/%s/%s' % (user, name))

        title = '%s %s %s' %(user, name, get_timestamp())
        try:
            fobj = codecs.open(fpath, 'r', encoding='utf-8')
            text = fobj.read()
            fobj.close()
        except Exception, e:
            print e

        text = text + '\n' + get_commits_text(commits)

        create_task(title, text, tags=[user,])
        print "blog posted for", user, name


def reload_blog():
    system('pushd .;cd 2013;nikola deploy;popd')

def main():
    q = Queue('puluupdates')
    q.connect()
    while True:
        task = q.wait()
        data = task.data
        user = data['repository']['owner']['name']
        if user not in ['kushaldas']:
            return
        reponame = data['repository']['name']
        names = set()
        # Now go through all commits and find the unique directory names
        for commit in data['commits']:
            for fpath in commit['added']:
                names.add(fpath.split('/')[0])
            for fpath in commit['modified']:
                names.add(fpath.split('/')[0])

        # Now for each name, update the blog posts
        for name in names:
            if os.path.isdir(os.path.join('gitsources', user, name)):
                blog_post(user, name,
                          os.path.join('gitsources', user, name), data['commits'])
        reload_blog()

if __name__ == '__main__':
    main()
