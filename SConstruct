import os
import sys
import SCons
from building import *

PROJECT_NAME = 'template'
PROJECT_PATH = sys.path[0]
IDF_PATH = os.getenv('IDF_PATH')
Export('IDF_PATH')

VDIR = 'build'
BUILD_DIR_BASE = os.path.join(PROJECT_PATH, VDIR)
Export('BUILD_DIR_BASE')

SRCDIRS = 'main'
COMPONENT_DIRS = [os.path.join(IDF_PATH, 'components'),
        os.path.join(PROJECT_PATH, 'components')]

COMPONENTS = []
for item in COMPONENT_DIRS:
    if os.path.isfile(os.path.join(item, 'SConscript')):
        for component in os.listdir(item):
            if os.path.isfile(os.path.join(item, component, 'SConscript')):
                COMPONENTS.append(component)

COMPONENT_INCLUDES = []
COMPONENT_LDFLAGS = []
COMPONENT_SUBMODULES = []

COMPONENT_INCLUDES.append(os.path.join(BUILD_DIR_BASE, 'include'))

IDF_VER = os.popen('git -C %s describe' % IDF_PATH).read().strip()
Export('IDF_VER')

contents = handleConfig('sdkconfig', os.path.join(BUILD_DIR_BASE, 'include'))
PreProcessor = SCons.cpp.PreProcessor()
PreProcessor.process_contents(contents)
BuildOptions = PreProcessor.cpp_namespace
Export('BuildOptions')

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
# LDFLAGS += (' -L%s/' % BUILD_DIR_BASE) + (" -L%s" % BUILD_DIR_BASE).join(COMPONENTS)
# LDFLAGS += ' -L%s/' % SRCDIRS
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

if BuildOptions.has_key('CONFIG_OPTIMIZATION_LEVEL_RELEASE'):
    OPTIMIZATION_FLAGS = ' -Os'
    CPPFLAGS += ' -DNDEBUG'
else:
    OPTIMIZATION_FLAGS = ' -Og'
OPTIMIZATION_FLAGS += ' -ggdb'

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

CPPPATH  = COMPONENT_INCLUDES + [PROJECT_PATH]
Export('CPPPATH')

env = Environment(
    AS = AS, ASFLAGS = CPPFLAGS, 
    CC = CC, CFLAGS = CFLAGS + CPPFLAGS,
    AR = AR, ARFLAGS = 'cru',
    LINK = LD, LINKFLAGS = LDFLAGS,
    CXX = CXX, CXXFLAGS = CXXFLAGS + CPPFLAGS,
    CPPPATH = CPPPATH,
    ENV = os.environ)
bld = Builder(action = '$CC -o $TARGET -I%s -C -P -x c -E $SOURCE'%os.path.join(BUILD_DIR_BASE, 'include'))
env.Append(BUILDERS = {'Outld': bld})

convert = 'python %s/components/esptool_py/esptool/esptool.py --chip esp32 elf2image --flash_mode %s --flash_freq %s --flash_size %s -o $TARGET $SOURCE ' % (
                            IDF_PATH, BuildOptions['CONFIG_ESPTOOLPY_FLASHMODE'], 
                                BuildOptions['CONFIG_ESPTOOLPY_FLASHFREQ'], BuildOptions['CONFIG_ESPTOOLPY_FLASHSIZE'])
cvt= Builder(action = convert)
env.Append(BUILDERS = {'ConvertELF': cvt})
Export('env')

PrepareBuilding(env, BuildOptions)

libs = SConscript(os.path.join(SRCDIRS, 'SConscript'),
            variant_dir=os.path.join(BUILD_DIR_BASE, SRCDIRS), duplicate=0)
for item in COMPONENT_DIRS:
    script = os.path.join(item, 'SConscript')
    if os.path.isfile(script):
        libs += SConscript(script,duplicate=0)

outld = env.Outld("esp32_out.ld", IDF_PATH + '/components/esp32/ld/esp32.ld')
APP_ELF = os.path.join(BUILD_DIR_BASE , PROJECT_NAME + '.elf')
APP_MAP = os.path.join(BUILD_DIR_BASE , PROJECT_NAME + '.map')
APP_BIN = os.path.join(BUILD_DIR_BASE , PROJECT_NAME + '.bin')

program = DoBuilding(APP_ELF, libs)
env.Depends(program, outld)
binfile = env.ConvertELF(APP_BIN, program)
