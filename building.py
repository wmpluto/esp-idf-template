import os
import re
import sys
import string

from SCons.Script import *

BuildOptions = {}
Projects = []
Rtt_Root = ''
Env = None

def PrepareBuilding(env, options):
    global BuildOptions
    global Projects
    global Env

    Env = env
    BuildOptions = options

def MergeGroup(src_group, group):
    src_group['src'] = src_group['src'] + group['src']
    if group.has_key('CCFLAGS'):
        if src_group.has_key('CCFLAGS'):
            src_group['CCFLAGS'] = src_group['CCFLAGS'] + group['CCFLAGS']
        else:
            src_group['CCFLAGS'] = group['CCFLAGS']
    if group.has_key('CPPPATH'):
        if src_group.has_key('CPPPATH'):
            src_group['CPPPATH'] = src_group['CPPPATH'] + group['CPPPATH']
        else:
            src_group['CPPPATH'] = group['CPPPATH']
    if group.has_key('CPPDEFINES'):
        if src_group.has_key('CPPDEFINES'):
            src_group['CPPDEFINES'] = src_group['CPPDEFINES'] + group['CPPDEFINES']
        else:
            src_group['CPPDEFINES'] = group['CPPDEFINES']

    # for local CCFLAGS/CPPPATH/CPPDEFINES
    if group.has_key('LOCAL_CCFLAGS'):
        if src_group.has_key('LOCAL_CCFLAGS'):
            src_group['LOCAL_CCFLAGS'] = src_group['LOCAL_CCFLAGS'] + group['LOCAL_CCFLAGS']
        else:
            src_group['LOCAL_CCFLAGS'] = group['LOCAL_CCFLAGS']
    if group.has_key('LOCAL_CPPPATH'):
        if src_group.has_key('LOCAL_CPPPATH'):
            src_group['LOCAL_CPPPATH'] = src_group['LOCAL_CPPPATH'] + group['LOCAL_CPPPATH']
        else:
            src_group['LOCAL_CPPPATH'] = group['LOCAL_CPPPATH']
    if group.has_key('LOCAL_CPPDEFINES'):
        if src_group.has_key('LOCAL_CPPDEFINES'):
            src_group['LOCAL_CPPDEFINES'] = src_group['LOCAL_CPPDEFINES'] + group['LOCAL_CPPDEFINES']
        else:
            src_group['LOCAL_CPPDEFINES'] = group['LOCAL_CPPDEFINES']

    if group.has_key('LINKFLAGS'):
        if src_group.has_key('LINKFLAGS'):
            src_group['LINKFLAGS'] = src_group['LINKFLAGS'] + group['LINKFLAGS']
        else:
            src_group['LINKFLAGS'] = group['LINKFLAGS']
    if group.has_key('LIBS'):
        if src_group.has_key('LIBS'):
            src_group['LIBS'] = src_group['LIBS'] + group['LIBS']
        else:
            src_group['LIBS'] = group['LIBS']
    if group.has_key('LIBPATH'):
        if src_group.has_key('LIBPATH'):
            src_group['LIBPATH'] = src_group['LIBPATH'] + group['LIBPATH']
        else:
            src_group['LIBPATH'] = group['LIBPATH']


def DefineGroup(name, src, depend, **parameters):
    global Env
    # find exist group and get path of group
    group_path = ''
    for g in Projects:
        if g['name'] == name:
            group_path = g['path']
    if group_path == '':
        group_path = GetCurrentDir()

    group = parameters
    group['name'] = name
    group['path'] = group_path
    if type(src) == type(['src1']):
        group['src'] = File(src)
    else:
        group['src'] = src

    if group.has_key('CCFLAGS'):
        Env.AppendUnique(CCFLAGS = group['CCFLAGS'])
    if group.has_key('CPPPATH'):
        Env.AppendUnique(CPPPATH = group['CPPPATH'])
    if group.has_key('CPPDEFINES'):
        Env.AppendUnique(CPPDEFINES = group['CPPDEFINES'])
    if group.has_key('LINKFLAGS'):
        #Env.AppendUnique(LINKFLAGS = group['LINKFLAGS'])
        Env['LINKFLAGS']+=group['LINKFLAGS']

    if group.has_key('LIBS'):
        Env.AppendUnique(LIBS = group['LIBS'])
    if group.has_key('LIBPATH'):
        Env.AppendUnique(LIBPATH = group['LIBPATH'])

    # check whether to build group library
    if group.has_key('LIBRARY'):
        if group.has_key('LOCAL_CCFLAGS') or group.has_key('LOCAL_CPPPATH') or group.has_key('LOCAL_CPPDEFINES'):
            CCFLAGS = Env.get('CCFLAGS', '') + group.get('LOCAL_CCFLAGS', '')
            CPPPATH = Env.get('CPPPATH', ['']) + group.get('LOCAL_CPPPATH', [''])
            CPPDEFINES = Env.get('CPPDEFINES', ['']) + group.get('LOCAL_CPPDEFINES', [''])

        objs = Env.Library(name, group['src'], CCFLAGS = CCFLAGS,
                    CPPPATH = CPPPATH, CPPDEFINES = CPPDEFINES)
    else:
        # only add source
        objs = group['src']

    # merge group
    for g in Projects:
        if g['name'] == name:
            # merge to this group
            MergeGroup(g, group)
            return objs

    # add a new group
    Projects.append(group)
    Export('Env')

    return objs

def GetDepend(depend):
    building = True
    if type(depend) == type('str'):
        if not BuildOptions.has_key(depend) or BuildOptions[depend] == 0:
            building = False
        elif BuildOptions[depend] != '':
            return BuildOptions[depend]

        return building

    # for list type depend
    for item in depend:
        if item != '':
            if not BuildOptions.has_key(item) or BuildOptions[item] == 0:
                building = False

    return building

def DoBuilding(target, objects):

    # merge all objects into one list
    def one_list(l):
        lst = []
        for item in l:
            if type(item) == type([]):
                lst += one_list(item)
            else:
                lst.append(item)
        return lst

    # handle local group
    def local_group(group, objects):
        if group.has_key('LOCAL_CCFLAGS') or group.has_key('LOCAL_CPPPATH') or group.has_key('LOCAL_CPPDEFINES'):
            CCFLAGS = Env.get('CCFLAGS', '') + group.get('LOCAL_CCFLAGS', '')
            CPPPATH = Env.get('CPPPATH', ['']) + group.get('LOCAL_CPPPATH', [''])
            CPPDEFINES = Env.get('CPPDEFINES', ['']) + group.get('LOCAL_CPPDEFINES', [''])

            for source in group['src']:
                objects.append(Env.Object(source, CCFLAGS = CCFLAGS,
                    CPPPATH = CPPPATH, CPPDEFINES = CPPDEFINES))

            return True

        return False

    objects = one_list(objects)

    program = None
    # check whether special buildlib option
    if 0:
        objects = [] # remove all of objects
    else:
        # remove source files with local flags setting
        for group in Projects:
            if group.has_key('LOCAL_CCFLAGS') or group.has_key('LOCAL_CPPPATH') or group.has_key('LOCAL_CPPDEFINES'):
                for source in group['src']:
                    for obj in objects:
                        if source.abspath == obj.abspath or (len(obj.sources) > 0 and source.abspath == obj.sources[0].abspath):
                            objects.remove(obj)

        # re-add the source files to the objects
        for group in Projects:
            local_group(group, objects)
#ldpath =  os.getenv('IDF_PATH') + 'components/esp32/ld/esp32.ld'
#        envld = Env.Clone()

        #outld = envld.Outld('esp32_out.ld',ldpath)
        #objects.append(outld)
        Env.Replace(LINKCOM = ['$LINK -o $TARGET $LINKFLAGS $__RPATH  $SOURCES $_LIBDIRFLAGS $_LIBFLAGS -Wl,--end-group -Wl,-EL -Wl,-Map=build/template.map'])

        program = Env.Program(target, objects)
        
        return program    
#program = Env.Program(target, objects)

def GetCurrentDir():
    conscript = File('SConscript')
    fn = conscript.rfile()
    name = fn.name
    path = os.path.dirname(fn.abspath)
    return path

def handleConfig(source, target):
	file_object = open(source)
	try:
	     sdkconfig = file_object.readlines( )
	finally:
	     file_object.close( )

	newconfig = []
	pattern = r'(.*)=(.*)'

	for line in sdkconfig:
		m = re.match(pattern, line)
		if m:
			macro  = '#define ' + m.group(1) + ' '
			macro += '1' if m.group(2) == 'y' else m.group(2)
			macro += '\n'
			newconfig.append(macro)

	checkDirs(target)
	file_object = open(target+'/sdkconfig.h', 'w')
	try:
	    file_object.writelines(newconfig)
	finally:
	     file_object.close()

	return "\n".join(newconfig)

def checkDirs(path):
	if os.path.exists(path):
		return True
	else:
		return  os.makedirs(path)
