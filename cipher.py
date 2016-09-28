#!/usr/bin/python2

import socket, base64, math

def read_line(sock):
    "read a line from a socket"
    chars = []
    char = "_"
    while char != '\n' and char != "":
        char = sock.recv(1)
        chars.append(char)
    line = "".join(chars)
    print(line)
    return line

def read_line_start_with(f, marker):
    while True:
        line = f.readline().rstrip()
        print(line)
        if marker in line and line.index(marker) == 0:
            return line

s = socket.socket()
s.connect(("csie.ctf.tw", 10124))
f = s.makefile("rwb",bufsize=0)

###############
### Stage 0 ###
###############
for i in range(3):
    line = read_line_start_with(f,"Round")
    target0 = line.split(' ')[2]
    decoded0 = target0.decode("hex")
    f.write(decoded0 + "\n")
    print(decoded0)

###############
### Stage 1 ###
###############
for i in range(3):
    line = read_line_start_with(f,"Round")
    target1 = line.split(' ')[2]
    decoded1 = base64.decodestring(target1)
    f.write(decoded1 + "\n")
    print(decoded1)


# I do the previous parts with Yun-Chih, It's easy I think.


# Stage 2 ==============================================

def caesar1(target2):
	toret = ""
	for c in target2:
		if c.isalpha():
			base = 'A' if c.isupper() else'a'
			toret += chr(25 +ord(base) - ord(c) + ord(base))
		else:
        		toret += c
	return toret + "\n"

line = read_line_start_with(f,"c1")
target2 = line.split('=')[1].strip()
decoded2 = caesar1(target2)

f.write(decoded2)
print(decoded2)

# Stage 3 ==================================================

def caesar2(target3, key):
	toret = ""
	for c in target3:
		if c.isalpha():
			base = 'A' if c.isupper() else 'a'
			toret += chr((ord(c) - ord(base) - key)%26 + ord(base))
		else:
			toret += c
	return toret + "\n"

m0 = read_line_start_with(f,"m0").split('=')[1].strip()
c0 = read_line_start_with(f,"c0").split('=')[1].strip()
c1 = read_line_start_with(f,"c1").split('=')[1].strip()

for i in range(len(m0)):
	if m0[i].isalpha():
		key = ord(c0[i]) - ord(m0[i])
            	break

decoded3 = caesar2(c1,key)

f.write(decoded3)
print(decoded3)

# Stage 4 ====================================================

def vigenere(cipher, key):
	toret = ""
	nu = 0
	for c in cipher:
	        if c.isalpha():
			base = 'A' if c.isupper() else 'a'
			toret += chr(ord(base) + (ord(c)-ord(base)-key[nu % len(key)])%26)
			nu +=1
		else:
			toret += c
           
	return toret + "\n"

def find_raw_key(m0,c0):
	raw_key = []
	for i in range(len(m0)):
		if m0[i].isalpha():
			raw_key.append((ord(c0[i]) - ord(m0[i])) % 26)
	return raw_key

def find_patten(raw_key):
	for i in range(1,len(raw_key),+1):
		for j in range(len(raw_key)):
			if raw_key[j] != raw_key[j % i]:
				break
			if j == len(raw_key) - 1:
				return raw_key[0:i]
	return raw_key
			
			

m0 = read_line_start_with(f,"m0").split('=')[1].strip()
c0 = read_line_start_with(f,"c0").split('=')[1].strip()
c1 = read_line_start_with(f,"c1").split('=')[1].strip()

raw_key = find_raw_key(m0,c0)
print(raw_key)
short_key = find_patten(raw_key)
print(short_key)

decoded = vigenere(c1, short_key)
f.write(decoded)
print(decoded)


# Stage 5 ============================================
def xor_two_str(s1,s2):
	toret = ""
	for i in range(len(s1)):
		toret += chr(( ord(s1[i]) ^ ord(s2[i % len(s2)]) ) % 256)
	return toret

def hex_to_chr(s):
	toret = ""
	for i in range(0,len(s),2):
		toret += chr(int(s[i:i+2],16))
	return toret


m0 = read_line_start_with(f,"m0").split('=')[1].strip()
c0 = hex_to_chr(read_line_start_with(f,"c0").split('=')[1].strip())
c1 = hex_to_chr(read_line_start_with(f,"c3").split('=')[1].strip())

key = xor_two_str(m0,c0)
decoded = xor_two_str(c1, key)
f.write(decoded + "\n")
print(decoded)


# Stage 6 =============================================================

def test_result(m,key):
	toret =""
	for i in range(key):
		for j in range(len(m) / key + 1):
			if(j * key + i < len(m)):
				toret += m[j * key + i]
	return toret

def find_column_num(m,c):
	for i in range(1,len(m)):
		if test_result(m,i) == c:
			return i

def transposition(c, key):
	short_len = len(c) / key
	long_len = short_len + 1
	remainder = len(c) % key  #long len num
	toret = ""
	if(remainder == 0):
		long_len -= 1
	for i in range(long_len):
		long_num = remainder
		k = i
		while k < len(c):
			toret += c[k]
			if(long_num > 0):
				k += long_len
				long_num -= 1
				if(long_num == 0 and i == long_len - 1):
					break
			else:
				k += short_len
	return toret

m0 = read_line_start_with(f,"m0").split('=')[1].strip()
c0 = read_line_start_with(f,"c0").split('=')[1].strip()
c1 = read_line_start_with(f,"c1").split('=')[1].strip()


column_num = find_column_num(m0,c0)
decoded = transposition(c1, column_num)

f.write(decoded + "\n")
print(decoded)

# Stage 7 ============================================
import hashlib

def brutle_find_md5(h):
	k = 0
	while True:
		st = hashlib.md5(str(k)).hexdigest()
		if(st[0:4] == h):
			return str(k)
		k +=1
	return "nothing"
	

for i in range(3):
	h = read_line_start_with(f,"Round").split('=')[1].strip()
	ori = brutle_find_md5(h)
	f.write(ori + "\n")
	print(ori)

for i in range(10):
	print(f.readline().rstrip())
