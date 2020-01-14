from polyMult import Poly
import tkinter as tk

polys = []
poly1 = Poly()
poly2 = Poly()
polyLabels = []

def add():
	output.config(text= "Answer: " + str(poly1+poly2))

def sub():
	output.config(text= "Answer: " + str(poly1-poly2))

def mult():
	output.config(text= "Answer: " + str(poly1*poly2))

def div():
	output.config(text= "Answer: " + str(poly1/poly2))

window = tk.Tk()
window.title("Polynomial")

canvas = tk.Canvas(window)
scroll = tk.Scrollbar(canvas, orient = "vertical", command = canvas.yview)
polyFrame = tk.Frame(canvas)
canvas.create_window(0, 0, anchor='nw', window=polyFrame)

def on_configure(event):
	canvas.configure(scrollregion=canvas.bbox('all'), yscrollcommand=scroll.set)	

canvas.pack(fill='both', expand=True, side='left')
scroll.pack(fill='y', side='right')

buttonFrame = tk.Frame(window)
addButton = tk.Button(buttonFrame, text= "Add", command= add, width = 11)
subtractButton = tk.Button(buttonFrame, text= "Subtract", command= sub, width = 11)
multiplyButton = tk.Button(buttonFrame, text= "Multiply", command= mult, width = 11)
divideButton = tk.Button(buttonFrame, text= "Divide", command= div, width = 11)
addButton.grid(row = 0, column = 0)
subtractButton.grid(row = 0, column = 1)
multiplyButton.grid(row = 0, column = 2)
divideButton.grid(row = 0, column = 3)

topLine = tk.Frame(window)

tk.Label(topLine, text="First Polynomial", anchor = "w").grid(row=0)
tk.Label(topLine, text="Second Polynomial", anchor = "w").grid(row=1)
output = tk.Label(window, text = "Answer: ")


s1 = tk.Entry(topLine, width = 2)
s2 = tk.Entry(topLine, width = 2)

s1.grid(row = 0, column = 1)
s2.grid(row = 1, column = 1)



p1 = tk.Label(topLine, text = "", width = 40)
p2 = tk.Label(topLine, text = "", width = 40)

p1.grid(row = 0, column = 2)
p2.grid(row = 1, column = 2)


def updatePolys(event):
	global poly1
	global poly2
	e1 = s1.get()
	e2 = s2.get()

	if e1 == "":
		poly1 = Poly()
	elif int(e1) - 1 < len(polys):
		poly1 = polys[int(e1) - 1]
	else:
		poly1 = Poly()

	if e2 == "":
		poly2 = Poly()
	elif int(e2) - 1 < len(polys):
		poly2 = polys[int(e2) - 1]
	else:
		poly2 = Poly()


	p1.config(text=str(poly1))
	p2.config(text=str(poly2))

s1.bind('<Return>', updatePolys)
s2.bind('<Return>', updatePolys)
canvas.bind('<Configure>', on_configure)

entryLine = tk.Frame(window)
entry = tk.Entry(entryLine, width = 44)
entry.grid(row = 0, column = 1)

l1 = tk.Label(entryLine, text = "Enter a polynomial: ")
l1.grid(row = 0, column = 0)

def addPoly():
	toAppend = Poly(entry.get())
	polys.append(toAppend)
	polyLabels.append(tk.Label(polyFrame, text= str(len(polyLabels) + 1) + ".   " + str(toAppend), anchor = 'w'))
	polyLabels[len(polyLabels) - 1].pack(anchor = "w")
	canvas.update_idletasks()
	scroll.update_idletasks()
	canvas.configure(scrollregion=canvas.bbox('all'), yscrollcommand=scroll.set)	


	


b1 = tk.Button(entryLine, command = addPoly, text = "Add")
b1.grid(row = 0, column = 2)


#pack widgets
topLine.pack(side = tk.TOP)
output.pack(anchor = "w")
buttonFrame.pack(side = tk.TOP)
entryLine.pack(side = tk.TOP)
canvas.pack(side = tk.BOTTOM)
window.mainloop()