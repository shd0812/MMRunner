import sys
from Crypto.Cipher import AES
from binascii import b2a_hex, a2b_hex
import hashlib
import  time

class prpcrypt():
	def __init__(self):
		self.key = b'sxsadjgdAkg_llhs'
		self.mode = AES.MODE_CBC

		# 加密函数，如果text不是16的倍数【加密文本text必须为16的倍数！】，那就补足为16的倍数

	def encrypt(self,text):
		#print(text)
		cryptor = AES.new(self.key, self.mode, self.key)
		# 这里密钥key 长度必须为16（AES-128）、24（AES-192）、或32（AES-256）Bytes 长度.目前AES-128足够用
		length = 16
		count = len(text)
		if count < length :
			add = (length-count)
			text = text + ('\0' * add)
		elif count > length:
			add = (length-(count % length))
			text = text + ('\0' * add)
		self.ciphertext = cryptor.encrypt(text.encode())
			# 因为AES加密时候得到的字符串不一定是ascii字符集的，输出到终端或者保存时候可能存在问题
			# 所以这里统一把加密后的字符串转化为16进制字符串
		return str(b2a_hex(self.ciphertext),'utf-8')


	# 解密后，去掉补足的空格用strip() 去掉
	def decrypt(self, text):
		# print(type(self.key))
		cryptor = AES.new(self.key, self.mode, b'sxsadjgdAkg_llhs')
		plain_text = cryptor.decrypt(a2b_hex(text))
		# print(plain_text.decode())
		return plain_text.decode()
class Sign():
	def __init__(self):
		self.key='sxsadjgdAkg_llhs'

	def getTimestamp(self):
		# 获取当前时间
		time_now = int(time.time())
		# 转换成localtime
		time_local = time.localtime(time_now)
		# 转换成新的时间格式(2016-05-09 18:59:20)
		dt = time.strftime("%Y-%m-%d %H:%M:%S", time_local)
		timeArray = time.strptime(dt, "%Y-%m-%d %H:%M:%S")
		# 转换成时间戳
		timestamp = time.mktime(timeArray)
		#print('当前时间%s 时间戳%s' % (dt,timestamp))
		return int(timestamp)
	#进行hash256
	def get_hash(self,str):
		data=hashlib.sha256(str.encode('utf-8')).hexdigest()
		return  data
	#获取sign
	def get_sign(self,serial_num,t_code,c_code):
		key=self.key
		data=serial_num+c_code+t_code+key

		# print('sha前 %s' % data)

		sign=self.get_hash(data)
		#print('sha后 %s' % sign)
		#print(c_code,t_code,serial_num,key)
		return  sign

if __name__ == '__main__':
	#key = b'sxs_djgdAkg_llhs'
	pc = prpcrypt()  # 初始化密钥
	e = pc.encrypt("19919920005")

	s='270650ddf25bb6465ea1fc62ace14c70'
	d = pc.decrypt(s)
	print(s)

	# bb=Sign()
	# ss=bb.get_sign()
	# print(ss)
