import os
import re
import sys
import SCons
from config import *

contents = handleConfig('sdkconfig', os.path.join(BUILD_DIR_BASE, 'include'))
PreProcessor = SCons.cpp.PreProcessor()
PreProcessor.process_contents(contents)
BuildOptions = PreProcessor.cpp_namespace

group = []
# app_update
name = 'app_update'
path = os.path.join(COMPONENT_DIR, name)
CPPPATH = ['include']
group.append({
	'name': name,
	'path': path,
	'CPPPATH': CPPPATH
	})

# bootloader_support
name = 'bootloader_support'
path = os.path.join(COMPONENT_DIR, name)
src = Glob(os.path.join(path, 'src/*.c'))
CPPPATH = ['include']
LOCAL_CPPPATH = ['include_priv']
group.append({
	'name': name,
	'path': path,
	'src': src,
	'CPPPATH': CPPPATH,
	'LOCAL_CPPPATH': LOCAL_CPPPATH
	})

# bt

# coap 

# components
# name = 'components'
# path = os.path.join(COMPONENT_DIR, name)
# src = [ Glob(os.path.join(path, item)) for item in [
# 				'drivers/src/*.c',
# 				'drivers/serial/*.c',
# 				'bsp/*.c',
# 				'finsh/*.c'
# 				]]
# CPPPATH = ['drivers/include', 'finsh', 'bsp']
# group.append({
# 	'name': name,
# 	'path': path,
# 	'src': src,
# 	'CPPPATH': CPPPATH
# 	})

# cxx
name = 'cxx'
path = os.path.join(COMPONENT_DIR, name)
src = Glob(os.path.join(path, '*.cpp'))
LINKFLAGS = ['-u __cxa_guard_dummy']
group.append({
	'name': name,
	'path': path,
	'src': src,
	'LINKFLAGS': LINKFLAGS
	})

# driver
name = 'driver'
path = os.path.join(COMPONENT_DIR, name)
src = Glob(os.path.join(path, '*.c'))
CPPPATH = ['include']
LOCAL_CPPPATH = ['include/driver']
group.append({
	'name': name,
	'path': path,
	'src': src,
	'CPPPATH': CPPPATH,
	'LOCAL_CPPPATH': LOCAL_CPPPATH
	})

# esp32
name = 'esp32'
path = os.path.join(COMPONENT_DIR, name)
src = [ Glob(os.path.join(path, item)) for item in [
				'*.c',
				'hwcrypto/*.c'
				]]
CPPPATH = ['include', '.']
LINKFLAGS = ['-T %s' % 'esp32_out.ld']
LINKFLAGS += ['-T %s' % (os.path.join(path, item)) for item in [
					'ld/esp32.common.ld',
					'ld/esp32.rom.ld',
					'ld/esp32.peripherals.ld'
					]]
LIBS = ['core', 'rtc', 'rtc_clk','hal']
if GetDepend(BuildOptions, 'CONFIG_PHY_ENABLED'):
	LIBS += ['phy', 'coexist']
if GetDepend(BuildOptions, 'CONFIG_WIFI_ENABLED'):
	LIBS += ['net80211', 'pp', 'wpa', 'smartconfig', 'coexist', 'wps', 'wpa2']
LIBPATH = ['lib', '.']
group.append({
	'name': name,
	'path': path,
	'src': sum(src, []),
	'CPPPATH': CPPPATH,
	'LINKFLAGS': LINKFLAGS,
	'LIBS': LIBS,
	'LIBPATH': LIBPATH
	})

# ethernet
name = 'ethernet'
path = os.path.join(COMPONENT_DIR, name)
src = Glob(os.path.join(path, '*.c'))
CPPPATH = ['include']
group.append({
	'name': name,
	'path': path,
	'src': src,
	'CPPPATH': CPPPATH,
	})

# expat
name = 'expat'
path = os.path.join(COMPONENT_DIR, name)
src = [ Glob(os.path.join(path, item)) for item in [
				'port/*.c',
				'library/*.c'
				]]
CPPPATH = ['include', 'port/include', 'include/expat']
LOCAL_CCFLAGS = ['-Wno-unused-function', '-DHAVE_EXPAT_CONFIG_H']
group.append({
	'name': name,
	'path': path,
	'src': sum(src, []),
	'CPPPATH': CPPPATH,
	'LOCAL_CPPPATH': LOCAL_CPPPATH
	})

# fatfs

