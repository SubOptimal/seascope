# Copyright (c) 2010 Anil Kumar
# All rights reserved.
#
# License: BSD 

import os
import sys
import re

from PyQt4 import QtGui, QtCore, uic

from PyQt4.QtGui import *
from PyQt4.QtCore import *

import DialogManager

backend_plugins = []
backend_dict = {}

def _load_plugins(module, directory):
	pluginImports = __import__(module, globals(), locals())
	print 'Scanning for backend plugins...'
	plist = []
	pdict = {}
	for i in sorted(os.listdir(directory)):
		path = os.path.join( directory, i, '__init__.py' )
		if os.path.isfile( path ):
			p = __import__( '%s.%s' % (module, i), globals(), locals(), ['*'] )
			plist.append(p)
			pdict[p.name()] = p
			if not hasattr(p, 'priority'):
				p.priority = 0 
	plist = sorted(plist, key=lambda p: p.priority, reverse=True)
	for p in plist:
		print '\t', p.name()
	return (plist, pdict)

def load_plugins():
	global backend_plugins, backend_dict
	(backend_plugins, backend_dict) = _load_plugins('backend.plugins', 'backend/plugins')

def plugin_list():
	return backend_plugins

from plugins.PluginBase import ProjectBase, ConfigBase, QueryBase, QueryUiBase

prj = None

def proj_new_open_app_cb():
	prj.prj_feature_setup()

def proj_close_app_cb():
	pass

	

def _proj_new_open():
	proj_new_open_app_cb()

def msg_box(msg):
	QMessageBox.warning(None, "Seascope", msg, QMessageBox.Ok)

def proj_new(bname, proj_args):
	b = backend_dict[bname]

	global prj
	assert not prj
	prj = b.project_class().prj_new(proj_args)

	if prj:
		_proj_new_open()
	return prj != None

def proj_open(proj_path):
	be = []
	for p in backend_plugins:
		if p.is_your_prj(proj_path):
			be.append(p)
	if len(be) == 0:
		msg = "Project '%s': No backend is interested" % proj_path
		msg_box(msg)
		return
	if len(be) > 1:
		msg = "Project '%s': Many backends interested" % proj_path
		for b in be:
			msg += '\n\t' + b.name()
		msg += '\n\nGoing ahead with: ' + be[0].name()
		msg_box(msg)

	b = be[0]
	print "Project '%s': using '%s' backend" % (proj_path, b.name())

	global prj
	prj = b.project_class().prj_open(proj_path)

	if prj:
		_proj_new_open()
	return prj != None

def proj_close():
	global prj
	prj.prj_close()
	prj = None
	
	from plugins import CtagsCache
	CtagsCache.flush()

	proj_close_app_cb

def proj_is_open():
	return prj != None

def proj_name():
	return prj.prj_name() if prj else None

def proj_dir():
	return prj.prj_dir() if prj else None

def proj_src_files():
	return prj.prj_src_files()

def proj_conf():
	return prj.prj_conf()

def proj_settings_get():
	return prj.prj_settings_get()

def proj_settings_update(proj_args):
	return prj.prj_settings_update(proj_args)

def proj_is_ready():
	return prj.prj_is_ready()

def proj_query(rquery):
	return prj.prj_query(rquery)

def proj_rebuild():
	return prj.prj_rebuild()

def proj_query_fl():
	return prj.prj_query_fl()

def proj_type():
	return prj.prj_type()

def proj_feature():
	return prj.prj_feature()
