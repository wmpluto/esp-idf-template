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
# main 
name = 'main'
path = os.path.join(PROJECT_PATH, name)
src = Glob(os.path.join(path, '*.c'))
group.append({
	'name': name,
	'path': path,
	'src': src
	})

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
name = 'fatfs'
path = os.path.join(COMPONENT_DIR, name)
src = [ Glob(os.path.join(path, item)) for item in [
				'src/*.c',
				'src/option/*.c'
				]]
CPPPATH = ['src']
group.append({
	'name': name,
	'path': path,
	'src': sum(src, []),
	'CPPPATH': CPPPATH,
	})

# freertos
name = 'freertos'
path = os.path.join(COMPONENT_DIR, name)
src = Glob(os.path.join(path, '*.[cS]'))
CPPPATH = ['/include', '/include/freertos', '/include/rtthread']
LINKFLAGS = ['-Wl,--undefined=uxTopUsedPriority']
group.append({
	'name': name,
	'path': path,
	'src': src,
	'CPPPATH': CPPPATH,
	'LINKFLAGS': LINKFLAGS
	})

# json
name = 'json'
path = os.path.join(COMPONENT_DIR, name)
src = [ Glob(os.path.join(path, item)) for item in [
				'library/*.c',
				'port/*.c'
				]]
CPPPATH = ['include', 'port/include']
group.append({
	'name': name,
	'path': path,
	'src': sum(src, []),
	'CPPPATH': CPPPATH,
	})

# log
name = 'log'
path = os.path.join(COMPONENT_DIR, name)
src = Glob(os.path.join(path, '*.c'))
CPPPATH = ['include']
group.append({
	'name': name,
	'path': path,
	'src': src,
	'CPPPATH': CPPPATH
	})

# lwip
name = 'lwip'
path = os.path.join(COMPONENT_DIR, name)
src = [ Glob(os.path.join(path, item)) for item in [
				'api/*.c',                                                                      
				'apps/sntp/*.c',
				'apps/ping/*.c',
				'apps/*.c',
				'core/ipv4/*.c',
				'core/ipv6/*.c',
				'core/*.c',
				'netif/*.c',
				'port/freertos/*.c',
				'port/netif/*.c',
				'port/*.c'
				]]
CPPPATH = ['include/lwip', 'include/lwip/port', 'include/lwip/posix', 'apps/ping']
LOCAL_CCFLAGS = ['-Wno-address', '-Wno-unused-but-set-variable', '-Wno-unused-variable']
group.append({
	'name': name,
	'path': path,
	'src': sum(src, []),
	'CPPPATH': CPPPATH,
	'LOCAL_CCFLAGS': LOCAL_CCFLAGS
	})

# mbedtls
name = 'mbedtls'
path = os.path.join(COMPONENT_DIR, name)
src = [ Glob(os.path.join(path, item)) for item in [
				'library/*.c',
				'port/*.c'
				]]
CPPPATH = ['include', 'port/include', '/port/include/mbedtls']
CCFLAGS = ['-DMBEDTLS_CONFIG_FILE=\'"mbedtls/esp_config.h"\'']
group.append({
	'name': name,
	'path': path,
	'src': sum(src, []),
	'CPPPATH': CPPPATH,
	'CCFLAGS': CCFLAGS
	})

# mdns
name = 'mdns'
path = os.path.join(COMPONENT_DIR, name)
src = Glob(os.path.join(path, '*.c'))
CPPPATH = ['include']
group.append({
	'name': name,
	'path': path,
	'src': src,
	'CPPPATH': CPPPATH
	})

# micro-ecc
name = 'micro-ecc'
path = os.path.join(COMPONENT_DIR, name)
src = Glob(os.path.join(path, 'micro-ecc/uECC.c'))
CPPPATH = ['include']
group.append({
	'name': name,
	'path': path,
	'src': src,
	'CPPPATH': CPPPATH
	})

# newlib
name = 'newlib'
path = os.path.join(COMPONENT_DIR, name)
src = Glob(os.path.join(path, '*.c'))
CPPPATH = ['include', 'platform_include']
LIBPATH = ['lib', '.']
LIBS = os.path.join(os.path.join(path, 'lib'),
					 'libm.a')
if GetDepend(BuildOptions, 'CONFIG_NEWLIB_NANO_FORMAT'):
	LIBS = os.path.join(os.path.join(path, 'lib'),
					 'libc_nano.a')
else:
	LIBS = os.path.join(os.path.join(path, 'lib'),
					 'libc.a')
group.append({
	'name': name,
	'path': path,
	'src': src,
	'CPPPATH': CPPPATH,
	'LIBS': LIBS,
	'LIBPATH': LIBPATH
	})

# nghttp

# nvs_flash
name = 'nvs_flash'
path = os.path.join(COMPONENT_DIR, name)
src = Glob(os.path.join(path, 'src/*.cpp'))
CPPPATH = ['include']
group.append({
	'name': name,
	'path': path,
	'src': src,
	'CPPPATH': CPPPATH
	})

# openssl
name = 'openssl'
path = os.path.join(COMPONENT_DIR, name)
src = [ Glob(os.path.join(path, item)) for item in [
				'library/*.c',
				'platform/*.c'
				]]
CPPPATH = ['include', 'include/internal', 'include/platform', 'include/openssl']
group.append({
	'name': name,
	'path': path,
	'src': sum(src, []),
	'CPPPATH': CPPPATH,
	})

# sdmmc
name = 'sdmmc'
path = os.path.join(COMPONENT_DIR, name)
src = Glob(os.path.join(path, '*.c'))
CPPPATH = ['include']
group.append({
	'name': name,
	'path': path,
	'src': src,
	'CPPPATH': CPPPATH
	})

# spi_flash
name = 'spi_flash'
path = os.path.join(COMPONENT_DIR, name)
src = Glob(os.path.join(path, '*.c'))
CPPPATH = ['include']
group.append({
	'name': name,
	'path': path,
	'src': src,
	'CPPPATH': CPPPATH
	})

# tcpip_adapter
name = 'tcpip_adapter'
path = os.path.join(COMPONENT_DIR, name)
src = Glob(os.path.join(path, '*.c'))
CPPPATH = ['include']
group.append({
	'name': name,
	'path': path,
	'src': src,
	'CPPPATH': CPPPATH
	})

# ulp
name = 'ulp'
path = os.path.join(COMPONENT_DIR, name)
src = Glob(os.path.join(path, '*.c'))
CPPPATH = ['include']
group.append({
	'name': name,
	'path': path,
	'src': src,
	'CPPPATH': CPPPATH
	})

# vfs
name = 'vfs'
path = os.path.join(COMPONENT_DIR, name)
src = Glob(os.path.join(path, '*.c'))
CPPPATH = ['include']
group.append({
	'name': name,
	'path': path,
	'src': src,
	'CPPPATH': CPPPATH
	})

# wpa_supplicant
name = 'wpa_supplicant'
path = os.path.join(COMPONENT_DIR, name)
src = [ Glob(os.path.join(path, item)) for item in [
				'port/*.c',
				'src/crypto//*.c'
				]]
CPPPATH = ['include', 'port/include']
LOCAL_CCFLAGS = ['-DEMBEDDED_SUPP', '-D__ets__', '-Wno-strict-aliasing']
group.append({
	'name': name,
	'path': path,
	'src': sum(src, []),
	'CPPPATH': CPPPATH,
	'LOCAL_CCFLAGS': LOCAL_CCFLAGS
	})

# xtensa-debug-module
name = 'xtensa-debug-module'
path = os.path.join(COMPONENT_DIR, name)
src = Glob(os.path.join(path, '*.c'))
CPPPATH = ['include']
group.append({
	'name': name,
	'path': path,
	'src': src,
	'CPPPATH': CPPPATH
	})
print [item['name'] for item in group]