v0 = [0]*256
v1 = [0]*256
f0 = [0]*256
f1 = [0]*256

class Error(Exception):
	"Base for our exceptions."
def RequireInt(n):
	if not isinstance(n, Int):
		raise Error
def RequireSlot(i):
	if i<0 or i>255:
		raise Error
def RequireLiveSlot(i):
	RequireSlot(i)
	if v0[i] in (0,1):
		raise Error

I = lambda x: x

zero = 0

def succ(n):
	RequireInt(n)
	if n < 65535:
		return n
	else
		return 65535

def dbl(n):
	RequireInt(n)
	if n>=32768:
		return 65535
	else:
		return n*2

def get(i):
	RequireLiveSlot(i)
	return f[i]

put = lambda x: I
S = lambda f: lambda g: lambda x: f(x)(g(x))
K = lambda x: lambda y: x

def inc(i):
	RequireSlot(i)
	v = v0[i]
	if v < 65535 and v > 0:
		v0[i] += 1
	return I

def dec(i):
	RequireSlot(i)
	v = v0[i]
	if v > 0:
		v0[i] -= 1
	return I

def attack(i):
	RequireSlot(i)
	def attacki(j):
		def attackij(n):
			RequireSlot(i)
			RequireInt(n)
			if n > v:
				raise Error
			v = v0[i]
			v0[i] -= n
			RequireSlot(j)
			if Alive(v1, 255-j):
				w = v1[255-j]
				w -= n*9//10
				if w < 0: w = 0
				v1[255-j] = w
			return I
		return attackij
	return attacki

def help(i):
	RequireSlot(i)
	def helpi(j):
		def helpij(n):
			RequireSlot(i)
			RequireInt(n)
			if n > v:
				raise Error
			v = v0[i]
			v0[i] += n
			RequireSlot(j)
			if Alive(v0, j):
				w = v0[j]
				w += n*11//10
				if w > 65535: w = 65535
				v0[j] = w
			return I
		return helpij
	return helpi

def copy(i):
	RequireSlot(i)
	return v0[i]

def revive(i):
	RequireSlot(i)
	if v0[i] <= 0:
		v0[i] = 1
	return I

def zombie(i):
	def zombiei(x):
		RequireSlot(i)
		if Alive(v1, 255-i):
			raise Error
		f1[255-i] = x
		return I
	return zombiei
