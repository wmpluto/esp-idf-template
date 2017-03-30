import os
import re
import sys
import SCons
import string


PROJECT_NAME = 'template'
PROJECT_PATH = sys.path[0]
IDF_PATH = os.getenv('IDF_PATH')

VDIR = 'build'
BUILD_DIR_BASE = os.path.join(PROJECT_PATH, VDIR)

COMPONENT_DIR = os.path.join(IDF_PATH, 'components')

IDF_VER = os.popen('git -C %s describe' % IDF_PATH).read().strip()

PREFIX = 'xtensa-esp32-elf-'

CC = PREFIX + 'gcc'
CXX = PREFIX + 'c++'
AS = PREFIX + 'gcc'
AR = PREFIX + 'ar'
LD = PREFIX + 'gcc'
SIZE = PREFIX + 'size'
OBJDUMP = PREFIX + 'objdump'
OBJCPY = PREFIX + 'objcopy'

LDFLAGS  = ' -nostdlib'
LDFLAGS += ' -ucall_user_start_cpu0'
LDFLAGS += ' -Wl,--gc-sections'
LDFLAGS += ' -Wl,-static'
LDFLAGS += ' -Wl,--start-group'
LDFLAGS += ' -lgcc'
LDFLAGS += ' -lstdc++'
LDFLAGS += ' -Wl,--allow-multiple-definition'

CPPFLAGS = ' -DESP_PLATFORM -D IDF_VER=\\"%s\\" -MMD -MP' % IDF_VER

COMMON_WARNING_FLAGS  = ' -Wall -Werror=all'
COMMON_WARNING_FLAGS += ' -Wno-error=unused-function'
COMMON_WARNING_FLAGS += ' -Wno-error=unused-but-set-variable'
COMMON_WARNING_FLAGS += ' -Wno-error=unused-variable'
COMMON_WARNING_FLAGS += ' -Wno-error=deprecated-declarations'
COMMON_WARNING_FLAGS += ' -Wextra'
COMMON_WARNING_FLAGS += ' -Wno-unused-parameter -Wno-sign-compare'

COMMON_FLAGS  = ' -ffunction-sections -fdata-sections'
COMMON_FLAGS += ' -fstrict-volatile-bitfields'
COMMON_FLAGS += ' -mlongcalls'
COMMON_FLAGS += ' -nostdlib'

# if BuildOptions.has_key('CONFIG_OPTIMIZATION_LEVEL_RELEASE'):
#     OPTIMIZATION_FLAGS = ' -Os'
#     CPPFLAGS += ' -DNDEBUG'
# else:
#     OPTIMIZATION_FLAGS = ' -Og'
OPTIMIZATION_FLAGS = ' -Os -ggdb'
CPPFLAGS += ' -DNDEBUG'

CFLAGS  = ' -std=gnu99'
CFLAGS += OPTIMIZATION_FLAGS
CFLAGS += COMMON_FLAGS
CFLAGS += COMMON_WARNING_FLAGS + ' -Wno-old-style-declaration'

CXXFLAGS  = ' -std=gnu++11'
CXXFLAGS += ' -fno-exceptions'
CXXFLAGS += ' -fno-rtti'
CXXFLAGS += OPTIMIZATION_FLAGS
CXXFLAGS += COMMON_FLAGS
CXXFLAGS += COMMON_WARNING_FLAGS

CPPPATH  = [PROJECT_PATH]

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
		return os.makedirs(path)

def GetDepend(BuildOptions, depend):
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
