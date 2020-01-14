def recursiveDivide(poly1, poly2):
	if poly2.exponent() >= poly1.exponent() or poly1.exponent() == 0:
		fractionPol = Poly()
		fractionPol.fraction = [Poly(), Poly()]
		fractionPol.fraction[0] = poly1
		fractionPol.fraction[1] = poly2
		if poly2.terms() == 1:
			coef = poly2.coef_list[poly2.exponent()]
			for i in range(len(poly2.coef_list)):
				fractionPol.fraction[1].coef_list[i] /= coef
			for i in range(len(poly1.coef_list)):
				fractionPol.fraction[0].coef_list[i] /= coef
 
		return fractionPol
	else:
		base = poly1.exponent() - poly2.exponent()
		num = poly1.coef_list[poly1.exponent()] / poly2.coef_list[poly2.exponent()]
		newPoly = Poly()
		while len(newPoly.coef_list) < base - 1:
			newPoly.coef_list.append(0)
		newPoly.coef_list.append(num)
		return newPoly + recursiveDivide(poly1 - (poly2*newPoly), poly2)

class Poly:
	def __init__(self, *args, **kargs):
		self.coef_list = []
		self.fraction = [0,1]
		if len(args) == 1 and isinstance(args[0], str):
			itemsList = args[0].split()
			for i in range(len(itemsList)):
				if itemsList[i] != "-" and itemsList[i] != "+":
					splitTerm = itemsList[i].split("x")
					if len(splitTerm) == 1:
						coefficient = int(splitTerm[0])
						if i != 0 and itemsList[i-1] == "-":
							coefficient *= -1
						while len(self.coef_list) < 1:
							self.coef_list.append(0)
						self.coef_list[0] += coefficient
					else:
						coefficient = int(splitTerm[0])
						if i != 0 and itemsList[i-1] == "-":
							coefficient *= -1
						if("^" in splitTerm[1]):
							splitTerm[1] = splitTerm[1][1:]
						if len(splitTerm[1]) == 0:
							splitTerm[1] = "1"
						while len(self.coef_list) <= int(splitTerm[1]):
							self.coef_list.append(0)
						self.coef_list[int(splitTerm[1])] += coefficient
		
		elif len(args) == 0: #if empty
			self.coef_list = [0]
		elif len(args) == 1: #if only one entry
			self.coef_list = list(args[0])
		else: #if multiple entry
			for item in args:
				self.coef_list.append(item)

		if len(kargs.keys()) != 0:
			maxLen = int(sorted(kargs.keys(), key = lambda x: int(x[1:]), reverse = True)[0][1:])
			while len(self.coef_list) <= maxLen:
				self.coef_list.append(0)
			for key, val in kargs.items():
				self.coef_list[int(key[1:])] = val

	def exponent(self):
		for i in range(len(self.coef_list)):
			if self.coef_list[len(self.coef_list) - 1 - i] != 0:
				return len(self.coef_list) - 1 - i
		return 0

	def terms(self):
		termCount = 0
		for i in self.coef_list:
			if i != 0:
				termCount += 1
		return termCount

	def __eq__(self, obj):
		if self.exponent() == 0:
			return obj == self.coef_list[0]
		if not isinstance(obj, Poly):
			return False
		if self.coef_list != obj.coef_list or self.fraction != obj.fraction:
			return False
		return True

	def __ne__(self, obj):
		return not self == obj

	def __str__(self):
		poly_str = ''
		exp = len(self.coef_list) - 1
		for item in self.coef_list[::-1]:
			if exp == 0:
				if item != 0:
					if poly_str != '':
						poly_str += ' {} '.format('+')
					poly_str += str(item)
			else:
				if item != 0:
					if poly_str != '':
						poly_str += ' {} '.format('+')
					poly_str += str(item) + 'x^' + str(exp)
			exp-=1
		if self.fraction[0] != 0:
			if poly_str != "":
				poly_str += " + "
			if self.fraction[1].exponent == 0 and self.fraction[1].coef_list[0] == 1:
				poly_str += str(self.fraction[0])
			else:
				poly_str += "(" + str(self.fraction[0]) + ")/(" + str(self.fraction[1]) + ")"
		return poly_str

	def get_coefs(self):
		return self.coef_list

	def __mul__(self, poly2):
		newCoefs = []

		if isinstance(poly2, int) or isinstance(poly2, float):
			for item in self.coef_list:
				newCoefs.append(item * poly2)
			return Poly(newCoefs)
		else:
			coefs2 = poly2.get_coefs()
			for i in range((len(coefs2))+(len(self.coef_list))):
				newCoefs.append(0)
			for in1 in range(len(self.coef_list)):
				#print('in1',in1)
				for in2 in range(len(coefs2)):
					#print('in2',in2)
					newCoefs[in1+in2] += self.coef_list[in1]*coefs2[in2]
			return Poly(newCoefs)

	def __add__(self, poly2):
		new_poly = Poly(self.coef_list)
		if type(poly2) == float or type(poly2) == int:
			if len(new_poly.get_coefs()) == 0:
				new_poly.coef_list[0] = 0
			new_poly.coef_list[0] += poly2
		elif type(poly2) == Poly:
			maxLen = max(len(new_poly.get_coefs()), len(poly2.get_coefs()))
			while len(new_poly.get_coefs()) <= maxLen:
				new_poly.coef_list.append(0)
			for i in range(len(poly2.get_coefs())):
				new_poly.coef_list[i] += poly2.get_coefs()[i]
		if self.fraction[0] != 0 and poly2.fraction[0] != 0:
			new_poly.fraction[0] = self.fraction[0]*poly2.fraction[1] + poly2.fraction[0]*self.fraction[1]
			new_poly.fraction[1] = self.fraction[1]*poly2.fraction[1]
		elif self.fraction[0] != 0:
			new_poly.fraction = self.fraction
		elif poly2.fraction[0] != 0:
			new_poly.fraction = poly2.fraction

		return new_poly

	def __radd__(self, poly2):
		return self + poly2

	def __sub__(self, poly2):
		return self + (poly2*-1)

	def __truediv__(self, poly2):
		return recursiveDivide(self, poly2)

	# def __rsub__(self, poly2):
	# 	return self + (poly2*-1)

#p = Poly(_0=1, _2 = 1, _4 = 1)
#p2 = Poly(1,1,1)
#p3 = Poly(1,1,1)
#p4 = Poly("3x^3 + 1x")
# p5 = Poly("")
# print(p)
# print(p2)
# print(p3)
# print((p+p2)*p3 + 3)
# print(1+Poly())
# print(p4)
# print(p5)
#print(p2 - p)