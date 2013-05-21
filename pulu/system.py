import os
import sys
import codecs
import base64
from .utils import system


def write_post(path, texts):
    '''
    Writes a new post.

    :arg path: Path of the post .txt file
    :arg texts: List containing the text message
    '''
    fobj = codecs.open(path, 'w', encoding='utf-8')
    for i, line in enumerate(texts):
        fobj.write(line)
    fobj.close()


def create_task(title, text, tags=[]):
    '''
    Creares a new home task with the given
    text.

    One can pass different data files also along the text
    '''
    htmlpath = None
    purl = 'http://dgplug.org/summertraining/2013/'
    post_create_command = 'pushd .;cd 2013;nikola new_post -t "%s";popd' % title

    #First create the post file
    out, err = system(post_create_command)
    filepath = ''
    for line in out.split('\n'):
        if line.startswith("Your post's text is at:"):
            filepath = line.split(':')[1]
            filepath = filepath.strip()

    if filepath:
        htmlpath = filepath.replace('.txt', '.html')
        filepath = os.path.join('2013', filepath)

    fobj = codecs.open(filepath, 'r', encoding='utf-8')
    lines = fobj.readlines()
    fobj.close()

    resulttext = []
    for line in lines:
        if line.startswith('.. link:'):
            line = '.. link: %s%s\n' % (purl, htmlpath)
        elif line.startswith('.. tags: '):
            line = '.. tags: %s' % ', '.join(tags)
        elif line == 'Write your post here.':
            line = u'\n' + text
        elif line == '\n':
            continue
        resulttext.append(line)

    #Write the edited text back on disk
    write_post(filepath, resulttext)
    run_build()




def run_build():
    '''
    Runs Nikola build for a given user

    :return: The build message 
    '''
    build_command = 'pushd .;cd 2013;nikola build;popd'
    out, err = system(build_command)
    return out



