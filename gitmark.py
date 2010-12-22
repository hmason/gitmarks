#!/usr/bin/env python
# encoding: utf-8
"""
gitmark.py

Created by Hilary Mason on 2010-09-24.
Copyright (c) 2010 Hilary Mason. All rights reserved.
"""

import sys, os
import urllib
import re
import hashlib
import csv
import subprocess
from optparse import OptionParser

from settings import *

# Arguments are passed directly to git, not through the shell, to avoid the
# need for shell escaping. On Windows, however, commands need to go through the
# shell for git to be found on the PATH, but escaping is automatic there. So
# send git commands through the shell on Windows, and directly everywhere else.
USE_SHELL = os.name == 'nt'

class gitMark(object):
    
    def __init__(self, options, args):
        modified = [] # track files we need to add - a hack, because it will add files that are already tracked by git
        
        try:
            url = args[0].strip('/')
        except IndexError, e:
            print >>sys.stderr, ("Error: No url found")
            return

        content = self.getContent(url)
        title = self.parseTitle(content)
        content_filename = self.generateHash(url)
        
        modified.append(self.saveContent(content_filename, content))
        tags = ['all']
        tags.extend(options['tags'].split(','))
        for tag in tags:
            t = tag.strip()
            if not t:
                continue
            if '/' in t:
                t = ''.join(t.split('/'))
            modified.append(self.saveTagData(t, url, title, content_filename))
            
        self.gitAdd(modified)
        
        commit_msg = options['msg']
        if not commit_msg:
            commit_msg = 'adding %s' % url
        
        self.gitCommit(commit_msg)
        
        if options['push']:
            self.gitPush()

    def gitAdd(self, files):
        subprocess.call(['git', 'add'] + files, shell=USE_SHELL)
        
    def gitCommit(self, msg):
        subprocess.call(['git', 'commit', '-m', msg], shell=USE_SHELL)
        
    def gitPush(self):
        pipe = subprocess.Popen("git push origin master", shell=True)
        pipe.wait()
        
    def saveContent(self, filename, content):
        try:
            f = open('%s%s' % (CONTENT_PATH, filename), 'w')
        except IOError: #likely the dir doesn't exist
            os.mkdir(CONTENT_PATH,0755)
            f = open('%s%s' % (CONTENT_PATH, filename), 'w')
            
        f.write(content)
        f.close()
        return '%s%s' % (CONTENT_PATH, filename)
        
    def saveTagData(self, tag, url, title, content_filename):
        try:
            tag_writer = csv.writer(open('%s%s' % (TAG_PATH, tag), 'a'))
        except IOError:
            os.mkdir(TAG_PATH,0755)
            tag_writer = csv.writer(open('%s%s' % (TAG_PATH, tag), 'a'))
            
        tag_writer.writerow([url, title, content_filename])
        return '%s%s' % (TAG_PATH, tag)

    def parseTitle(self, content):
        re_htmltitle = re.compile(".*<title>(.*)</title>.*")
        t = re_htmltitle.search(content)
        try:
            title = t.group(1)
        except AttributeError:
            title = '[No Title]'
        
        return title
        
    def generateHash(self, text):
        m = hashlib.md5()
        m.update(text)
        return m.hexdigest()
        
    def getContent(self, url):
        try:
            h = urllib.urlopen(url)
            content = h.read()
            h.close()
        except IOError, e:
            print >>sys.stderr, ("Error: could not retrieve the content of a"
                " URL. The bookmark will be saved, but its content won't be"
                " searchable. URL: <%s>. Error: %s" % (url, e))
            content = ''
        return content
        


if __name__ == '__main__':
    parser = OptionParser("usage: %prog [options] <url>")
    parser.add_option("-p", "--push", dest="push", action="store_false", default=True, help="don't push to origin.")
    parser.add_option("-t", "--tags", dest="tags", action="store", default='notag', help="comma seperated list of tags")
    parser.add_option("-m", "--message", dest="msg", action="store", default=None, help="specify a commit message (default is 'adding [url]')")
    (options, args) = parser.parse_args()
    
    opts = {'push': options.push, 'tags': options.tags, 'msg': options.msg}
    
    g = gitMark(opts, args)
