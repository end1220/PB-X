
# gen..

import os
import os.path
import sys
import string
import shutil
import settings


src = '/protos/'
gen_tmp = '/auto_gen/lua/'


def gen_files(src_path, dst_path):
	abs_src_path = os.path.abspath('.') + src_path
	abs_dst_path = os.path.abspath('.') + dst_path
	if os.path.exists(abs_dst_path):
		shutil.rmtree(abs_dst_path)
	os.mkdir(abs_dst_path)
	msg_id_str = '-- This file is generated by PBX. You should never modify it.'
	msg_id_str = msg_id_str + '\n\nmodule(\'%s\')\n\nMsgID =\n{\n' % settings.NAME_SPACE
	file_index = 0
	os.chdir('.%s' % src)
	for file_name in os.listdir(abs_src_path):
		if file_name.find('.proto') <= 0:
			continue
		print('  %s' % file_name)
		os.system('..\\protoc.exe --plugin=protoc-gen-lua="%s/../protoc-gen-lua/plugin/protoc-gen-lua.bat" --lua_out=../%s %s' % (os.path.abspath('.'), dst_path, file_name))
		file_index = file_index + 1
		id_index = file_index * settings.MAX_ID_COUNT_PER_FILE
		msg_id_str = msg_id_str + '\n\t-- %s\n' % file_name
		f = open(abs_src_path + file_name,'r')
		lines = f.readlines()
		for line in lines:
			find_indx = line.find('message')
			if find_indx != -1:
				id_name = line[find_indx+8 : len(line)-1]
				id_index = id_index + 1
				msg_id_str += '\t%s = %d,\n' % (id_name, id_index)
	pass
	os.chdir('./../')
	msg_id_str += '\n};\n'
	open(abs_dst_path+'MsgID.lua', 'wb').write(msg_id_str)
pass


def copy_cs(abs_src_path,  abs_dst_path):
	for file in os.listdir(abs_src_path):
		sourceFile = os.path.join(abs_src_path,  file)
		targetFile = os.path.join(abs_dst_path,  file)
		if os.path.isfile(sourceFile) and sourceFile.find('.lua') > 0:
			open(targetFile, "wb").write(open(sourceFile, "rb").read())
			print('  to %s' % targetFile)
		elif os.path.isdir(sourceFile):
			copy_cs(sourceFile, abs_dst_path)
	shutil.rmtree(abs_src_path)
pass



print('\n-----Begin Gen Lua-----')
gen_files(src, gen_tmp)
print('-----End Gen Lua-----')
if settings.AUTO_COPY_FILE:
	print('-----Begin Copy-----')
	copy_cs(os.path.abspath('.') + gen_tmp, os.path.abspath('.') + settings.LUA_DEST_DIR)
	print('-----End Copy-----\n')
pass
