# ECIES.py
# 1st November 2015
# Mohit  Bhura 11CS30019
# Yash Shrivastava 13CS10054
# Souvik Sonar 15CS91S01
# Nadeem Shaik 11CS30033

from sage.all import *
from random import randint
from math import *

#input : a point belonging to the elliptic curve
#return : a point 
def point_double(P):
	p1 = map(int,P.xy());
	q1 = map(int,P.xy());
	lam = 3*p1[0]*p1[0]+a;
	lam/=(2*p1[1]);
	xr = lam*lam - p1[0] - q1[0];
	yr = lam*(p1[0]-xr)-q1[1];
	R = E(xr,yr);
	return R;

#input : 2 points belonging to the elliptic curve
#return : a point 
def point_addition(P,Q):
	p1 = map(int,P.xy());
	q1 = map(int,Q.xy());
	if(p1 == q1):
		return point_double(P);
	lam = (q1[1]-p1[1])/(q1[0]-p1[0]);
	xr = lam*lam - p1[0] - q1[0];
	yr = lam*(p1[0]-xr)-q1[1];
	R = E(xr,yr);
	return R;

#input : an integer, a point belonging to the elliptic curve
#return : a point 
def point_multiply(d,P):
	p1 = map(int,P.xy());
	m = log(d,2)+1;
	d = bin(d)[2:]
	Q  = E(0,0);
	for i in d:
		if i :
			Q = point_addition(P,Q);
		P = point_double(P);
	return Q


def point_compress(P):

	l = P.xy();
	return [int(l[0]),int(l[1])%2];


# input : a tuple consisiting of the return of point_compress
# return : a tuple [x0/m,y0/m]
def point_decompress(x,i):

	z = (x**3 + a*x + b)%p;
	if power_mod(z,(p-1)/2,p) == -1 :
		return "failure";
	y = int(Mod(z,p).sqrt());
	if y%2 == i:
		return [x,y];
	else:
		return [x,p-y];


#encryption
def encrypt(x):

	encryption = [point_compress(l),(x*int(R.xy()[0]))%p];
	return encryption;

#decryption
def decrypt(encryption):

	y1 = encryption[0];
	y2 = encryption[1];
	alpha = point_decompress(y1[0],y1[1]);
	S = E(int(alpha[0]),int(alpha[1]));
	S = m*S;
	x0 = int(S.xy()[0])
	decryption = (y2*pow(x0,p-2,p))%p;
	return decryption;


def main():

	encryption = [];
	arr = [];
	x = int(raw_input("Please enter your number : "));	
	while x > 0 :	
		arr.append(x%p);	
		encryption.append(encrypt(x%p));
		x/=p;
	print 'encryption : ', encryption;
	encryption.reverse();
	decryption = 0;
	for a,i in enumerate(encryption) :
		d = decrypt(i);
		print '\t\t',arr[a],d;
		decryption*=p;
		decryption+=d;
	print 'decryption : ',decryption;

x = 6917529027641089837;
p = 36*(x**4)+36*(x**3)+24*(x**2)+6*(x)+1;
E = EllipticCurve(GF(p),[0,3]);
n = 36*(x**4)+36*(x**3)+18*(x**2)+6*(x)+1;
a = 0;
b = 3;
P = E(1,2);
m = randint(1,n);
k = randint(1,n);
Q = m*P;
R = k*Q;
l = k*P;
print ' Prime : ',p;
main();

