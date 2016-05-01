from __future__ import print_function
from math import sqrt
import CT as compiler
import numpy as np
import matplotlib.pyplot as plt
import matplotlib.patches as patches
import matplotlib.path as path
from matplotlib.gridspec import GridSpec
import sys

# ---------------------------------------
# VARIABLES GLOBALES
# ---------------------------------------

global_memory = [[], [], [], [], [], [], [], []]
local_actual_memory = [[], [], [], [], [], [], [], []]
local_next_memory = [[], [], [], [], [], [], [], []]

instructionPointer = 0
memoriesStack = []
pointersStack = []

# ---------------------------------------
# CODIGOS DE OPERACION
# ---------------------------------------

ADD = 100
SUBSTRACT = 110
MULTIPLY = 120
DIVISION = 130
RESIDUE = 140
LESS_THAN = 150
GREATER_THAN = 160
LESS_EQUAL = 170
GREATER_EQUAL = 180
EQUAL = 190
DIFFERENT = 200
AND = 210
OR = 220
ASSIGN = 230
PRINT = 240
READ = 250
GOTOF = 260
GOTOV = 270
GOTO = 280
ERA = 290
GOSUB = 300
RETORNO = 310
PARAM = 320
FUNCRETURN = 330
VER = 340
NEG = 350
AVERAGE = 360
VARIANCE = 370
STDEV = 380
SUM = 390
MUL = 400
BARS = 410
DBARS = 420
STACKED = 430
PIE = 440
HISTO = 450
END = 500

# ---------------------------------------
# TYPES
# ---------------------------------------

INT = 10
FLOAT = 20
BOOL = 30
STRING = 40
ERROR = 50
PROGRAM = 60
FUNC = 70
MAIN = 80

# ---------------------------------------
# METODOS AUXILIARES
# ---------------------------------------

def getValueForAddress(address):
	
	if isinstance(address, str):
		if '|' in address:
			return int(address[1:-1])
		if '(' in address:
			address = getValueForAddress(int(address[1:-1]))

	if address >= compiler.MIN_INT_GLOBAL and address <= compiler.MAX_INT_GLOBAL:
		return global_memory[0][address - compiler.MIN_INT_GLOBAL]
	elif address >= compiler.MIN_FLOAT_GLOBAL and address <= compiler.MAX_FLOAT_GLOBAL:
		print(address - compiler.MIN_BOOL_GLOBAL)
		print(global_memory)
		return global_memory[1][address - compiler.MIN_FLOAT_GLOBAL]
	elif address >= compiler.MIN_BOOL_GLOBAL and address <= compiler.MAX_BOOL_GLOBAL:
		return global_memory[2][address - compiler.MIN_BOOL_GLOBAL]
	elif address >= compiler.MIN_STRING_GLOBAL and address <= compiler.MAX_STRING_GLOBAL:
		return global_memory[3][address - compiler.MIN_STRING_GLOBAL]

	if address >= compiler.MIN_INT and address <= compiler.MAX_INT:
		return local_actual_memory[0][address - compiler.MIN_INT]
	elif address >= compiler.MIN_FLOAT and address <= compiler.MAX_FLOAT:
		return local_actual_memory[1][address - compiler.MIN_FLOAT]
	elif address >= compiler.MIN_BOOL and address <= compiler.MAX_BOOL:
		return local_actual_memory[2][address - compiler.MIN_BOOL]
	elif address >= compiler.MIN_STRING and address <= compiler.MAX_STRING:
		return local_actual_memory[3][address - compiler.MIN_STRING]

	if address >= compiler.MIN_TEMP_INT and address <= compiler.MAX_TEMP_INT:
		return local_actual_memory[4][address - compiler.MIN_TEMP_INT]
	elif address >= compiler.MIN_TEMP_FLOAT and address <= compiler.MAX_TEMP_FLOAT:
		return local_actual_memory[5][address - compiler.MIN_TEMP_FLOAT]
	elif address >= compiler.MIN_TEMP_BOOL and address <= compiler.MAX_TEMP_BOOL:
		return local_actual_memory[6][address - compiler.MIN_TEMP_BOOL]
	elif address >= compiler.MIN_TEMP_STRING and address <= compiler.MAX_TEMP_STRING:
		return local_actual_memory[7][address - compiler.MIN_TEMP_STRING]

	value = list(compiler.constants_table.keys())[list(compiler.constants_table.values()).index(address)]
	
	if address >= compiler.MIN_CONST_INT and address <= compiler.MAX_CONST_INT:
		return value
	elif address >= compiler.MIN_CONST_FLOAT and address <= compiler.MAX_CONST_FLOAT:
		return float(value)
	elif address >= compiler.MIN_CONST_BOOL and address <= compiler.MAX_CONST_BOOL:
		if value == 'true':
			return True

		return False
	elif address >= compiler.MIN_CONST_STRING and address <= compiler.MAX_CONST_STRING:
		return value

def saveValueToAddress(value, address):

	if isinstance(address, str):
		if '(' in address:
			address = getValueForAddress(int(address[1:-1]))

	if address >= compiler.MIN_INT_GLOBAL and address <= compiler.MAX_INT_GLOBAL:
		global_memory[0][address - compiler.MIN_INT_GLOBAL] = value
	elif address >= compiler.MIN_FLOAT_GLOBAL and address <= compiler.MAX_FLOAT_GLOBAL:
		global_memory[1][address - compiler.MIN_FLOAT_GLOBAL] = value
	elif address >= compiler.MIN_BOOL_GLOBAL and address <= compiler.MAX_BOOL_GLOBAL:
		global_memory[2][address - compiler.MIN_BOOL_GLOBAL] = value
	elif address >= compiler.MIN_STRING_GLOBAL and address <= compiler.MAX_STRING_GLOBAL:
		global_memory[3][address - compiler.MIN_STRING_GLOBAL] = value

	if address >= compiler.MIN_INT and address <= compiler.MAX_INT:
		local_actual_memory[0][address - compiler.MIN_INT] = value
	elif address >= compiler.MIN_FLOAT and address <= compiler.MAX_FLOAT:
		local_actual_memory[1][address - compiler.MIN_FLOAT] = value
	elif address >= compiler.MIN_BOOL and address <= compiler.MAX_BOOL:
		local_actual_memory[2][address - compiler.MIN_BOOL] = value
	elif address >= compiler.MIN_STRING and address <= compiler.MAX_STRING:
		local_actual_memory[3][address - compiler.MIN_STRING] = value

	if address >= compiler.MIN_TEMP_INT and address <= compiler.MAX_TEMP_INT:
		local_actual_memory[4][address - compiler.MIN_TEMP_INT] = value
	elif address >= compiler.MIN_TEMP_FLOAT and address <= compiler.MAX_TEMP_FLOAT:
		local_actual_memory[5][address - compiler.MIN_TEMP_FLOAT] = value
	elif address >= compiler.MIN_TEMP_BOOL and address <= compiler.MAX_TEMP_BOOL:
		local_actual_memory[6][address - compiler.MIN_TEMP_BOOL] = value
	elif address >= compiler.MIN_TEMP_STRING and address <= compiler.MAX_TEMP_STRING:
		local_actual_memory[7][address - compiler.MIN_TEMP_STRING] = value

def saveValueToNewMemory(value, address):
	if address >= compiler.MIN_INT and address <= compiler.MAX_INT:
		local_next_memory[0][address - compiler.MIN_INT] = value
	elif address >= compiler.MIN_FLOAT and address <= compiler.MAX_FLOAT:
		local_next_memory[1][address - compiler.MIN_FLOAT] = value
	elif address >= compiler.MIN_BOOL and address <= compiler.MAX_BOOL:
		local_next_memory[2][address - compiler.MIN_BOOL] = value
	elif address >= compiler.MIN_STRING and address <= compiler.MAX_STRING:
		local_next_memory[3][address - compiler.MIN_STRING] = value

def getArrayValues(initialAddress, lenght):
	arrayToReturn = []

	if initialAddress >= compiler.MIN_INT_GLOBAL and initialAddress <= compiler.MAX_INT_GLOBAL:
		for x in range(0, lenght):
			arrayToReturn.append(global_memory[0][initialAddress + x - compiler.MIN_INT_GLOBAL])
	elif initialAddress >= compiler.MIN_FLOAT_GLOBAL and initialAddress <= compiler.MAX_FLOAT_GLOBAL:
		for x in range(0, lenght):
			arrayToReturn.append(global_memory[1][initialAddress + x - compiler.MIN_FLOAT_GLOBAL])
	elif initialAddress >= compiler.MIN_STRING_GLOBAL and initialAddress <= compiler.MAX_STRING_GLOBAL:
		for x in range(0, lenght):
			arrayToReturn.append(global_memory[3][initialAddress + x - compiler.MIN_STRING_GLOBAL])
	elif initialAddress >= compiler.MIN_BOOL_GLOBAL and initialAddress <= compiler.MAX_BOOL_GLOBAL:
		for x in range(0, lenght):
			arrayToReturn.append(global_memory[2][initialAddress + x - compiler.MIN_BOOL_GLOBAL])
	elif initialAddress >= compiler.MIN_INT and initialAddress <= compiler.MAX_INT:
		for x in range(0, lenght):
			arrayToReturn.append(local_actual_memory[0][initialAddress + x - compiler.MIN_INT])
	elif initialAddress >= compiler.MIN_FLOAT and initialAddress <= compiler.MAX_FLOAT:
		for x in range(0, lenght):
			arrayToReturn.append(local_actual_memory[1][initialAddress + x - compiler.MIN_FLOAT])
	elif initialAddress >= compiler.MIN_STRING and initialAddress <= compiler.MAX_STRING:
		for x in range(0, lenght):
			arrayToReturn.append(local_actual_memory[3][initialAddress + x - compiler.MIN_STRING])
	elif initialAddress >= compiler.MIN_BOOL and initialAddress <= compiler.MAX_BOOL:
		for x in range(0, lenght):
			arrayToReturn.append(local_actual_memory[2][initialAddress + x - compiler.MIN_BOOL])

	print("toReturn ", arrayToReturn)

	return arrayToReturn

def semanticErrorHalt(error):
	print("Semantic Error: " + error)

	sys.exit()

# ---------------------------------------
# OPERACIONES
# ---------------------------------------

def add(leftOp, rightOp, result):
	leftValue = getValueForAddress(leftOp)
	rightValue = getValueForAddress(rightOp)

	saveValueToAddress(leftValue + rightValue, result)

def substract(leftOp, rightOp, result):
	leftValue = getValueForAddress(leftOp)
	rightValue = getValueForAddress(rightOp)
	
	saveValueToAddress(leftValue - rightValue, result)

def multiply(leftOp, rightOp, result):
	if isinstance(leftOp, list):
		leftValue = leftOp[0]
	else:
		leftValue = getValueForAddress(leftOp)

	if isinstance(rightOp, list):
		rightValue = rightOp[0]
	else:
		rightValue = getValueForAddress(rightOp)
	
	saveValueToAddress(leftValue * rightValue, result)

def divide(leftOp, rightOp, result):
	leftValue = getValueForAddress(leftOp)
	rightValue = getValueForAddress(rightOp)
	
	saveValueToAddress(leftValue / rightValue, result)

def residue(leftOp, rightOp, result):
	leftValue = getValueForAddress(leftOp)
	rightValue = getValueForAddress(rightOp)
	
	saveValueToAddress(leftValue % rightValue, result)

def assign(rightOp, result):
	value = getValueForAddress(rightOp)

	saveValueToAddress(value, result)

def lessThan(leftOp, rightOp, result):
	leftValue = getValueForAddress(leftOp)
	rightValue = getValueForAddress(rightOp)

	if leftValue < rightValue:
		saveValueToAddress(True, result)
	else:
		saveValueToAddress(False, result)

def lessThanEqual(leftOp, rightOp, result):
	leftValue = getValueForAddress(leftOp)
	rightValue = getValueForAddress(rightOp)

	if leftValue <= rightValue:
		saveValueToAddress(True, result)
	else:
		saveValueToAddress(False, result)

def greaterThan(leftOp, rightOp, result):
	leftValue = getValueForAddress(leftOp)
	rightValue = getValueForAddress(rightOp)

	if leftValue > rightValue:
		saveValueToAddress(True, result)
	else:
		saveValueToAddress(False, result)

def greaterThanEqual(leftOp, rightOp, result):
	leftValue = getValueForAddress(leftOp)
	rightValue = getValueForAddress(rightOp)

	if leftValue >= rightValue:
		saveValueToAddress(True, result)
	else:
		saveValueToAddress(False, result)

def equal(leftOp, rightOp, result):
	leftValue = getValueForAddress(leftOp)
	rightValue = getValueForAddress(rightOp)

	if leftValue == rightValue:
		saveValueToAddress(True, result)
	else:
		saveValueToAddress(False, result)

def different(leftOp, rightOp, result):
	leftValue = getValueForAddress(leftOp)
	rightValue = getValueForAddress(rightOp)

	if leftValue != rightValue:
		saveValueToAddress(True, result)
	else:
		saveValueToAddress(False, result)

def andOp(leftOp, rightOp, result):
	leftValue = getValueForAddress(leftOp)
	rightValue = getValueForAddress(rightOp)

	if leftValue and rightValue:
		saveValueToAddress(True, result)
	else:
		saveValueToAddress(False, result)

def orOp(leftOp, rightOp, result):
	leftValue = getValueForAddress(leftOp)
	rightValue = getValueForAddress(rightOp)

	if leftValue or rightValue:
		saveValueToAddress(True, result)
	else:
		saveValueToAddress(False, result)

def era(size):
	global local_next_memory

	local_next_memory = [[], [], [], [], [], [], [], []]

	for x in range(0, size[0]):
		local_next_memory[0].append(0)

	for x in range(0, size[1]):
		local_next_memory[1].append(0)

	for x in range(0, size[2]):
		local_next_memory[2].append(False)

	for x in range(0, size[3]):
		local_next_memory[3].append("")

	for x in range(0, size[4]):
		local_next_memory[4].append(0)

	for x in range(0, size[5]):
		local_next_memory[5].append(0)

	for x in range(0, size[6]):
		local_next_memory[6].append(False)

	for x in range(0, size[7]):
		local_next_memory[7].append("")

	# print(local_next_memory)

def initMemoriaGlobal():
	global global_memory

	for proc in compiler.dir_procs:
		if proc[3] == 10:
			global_memory[0].append(0)
		if proc[3] == 20:
			global_memory[1].append(0)
		if proc[3] == 30:
			global_memory[2].append(0)
		if proc[3] == 40:
			global_memory[3].append(0)
	
	size = compiler.dir_procs[0][6]
	
	for x in range(0, size[0]):
		global_memory[0].append(0)

	for x in range(0, size[1]):
		global_memory[1].append(0)

	for x in range(0, size[2]):
		global_memory[2].append(False)

	for x in range(0, size[3]):
		global_memory[3].append("")


def getAverage(initialAddress, lenght):
	data = getArrayValues(initialAddress, lenght)
	accum = 0.0

	for x in range(0, len(data)):
		accum += data[x]

	return accum / lenght

def getVariance(initialAddress, lenght):
	data = getArrayValues(initialAddress, lenght)
	accum = 0.0

	average = getAverage(initialAddress, lenght)

	for x in range(0, len(data)):
		accum += pow(data[x] - average, 2)

	return accum / lenght

def getStdDeviation(initialAddress, lenght):
	return sqrt(getVariance(initialAddress, lenght))

def getSum(initialAddress, lenght):
	data = getArrayValues(initialAddress, lenght)
	accum = 0.0

	for x in range(0, len(data)):
		accum += data[x]

	return accum

def getMul(initialAddress, lenght):
	data = getArrayValues(initialAddress, lenght)
	accum = 1.0

	for x in range(0, len(data)):
		accum *= data[x]

	return accum

def bars(dataA, arrLabels, length, labelGroup):
	fig, ax = plt.subplots()
	index = np.arange(length)
	bar_width = 0.35

	opacity = 0.4
	error_config = {'ecolor': '0.3'}

	rects1 = plt.bar(index, dataA, bar_width,
	                 alpha=opacity,
	                 color='b',
	                 error_kw=error_config,
	                 label=labelGroup)
	plt.xticks(index + bar_width, arrLabels)
	plt.legend()

	plt.tight_layout()
	plt.show()

	return

def stacked(dataA, dataB, length, labelA, labelB):
	ind = np.arange(length)
	width = 0.35  

	p1 = plt.bar(ind, dataA, width, color='r')
	p2 = plt.bar(ind, dataB, width, color='b',
	             bottom=dataA)

	plt.ylabel('Scores')
	plt.title('Scores by group')
	plt.xticks(ind + width/2., ('G1', 'G2', 'G3', 'G4', 'G5'))
	plt.yticks(np.arange(0, 100, 300))
	plt.legend((p1[0], p2[0]), (labelA, labelB))

	plt.show()
	return

def dBars(dataA, dataB, labels, length, labelA, labelB):

	ind = np.arange(length)  # the x locations for the groups
	width = 0.35       # the width of the bars

	fig, ax = plt.subplots()
	rects1 = ax.bar(ind, dataA, width, color='r')
	rects2 = ax.bar(ind + width, dataB, width, color='y')

	# add some text for labels, title and axes ticks
	ax.set_ylabel('Scores')
	ax.set_title('Scores by group and gender')
	ax.set_xticks(ind + width)
	ax.set_xticklabels(labels)

	ax.legend((rects1[0], rects2[0]), (labelA, labelB))


	def autolabel(rects):
	    # attach some text labels
	    for rect in rects:
	        height = rect.get_height()
	        ax.text(rect.get_x() + rect.get_width()/2., 1.05*height,
	                '%d' % int(height),
	                ha='center', va='bottom')

	autolabel(rects1)
	autolabel(rects2)

	plt.show()

	return

def pie(dataA, arrLabels, length):
	the_grid = GridSpec(2, 2)
	print('-----------------------------------------')
	print(arrLabels)
	plt.pie(dataA, labels=arrLabels, autopct='%.0f%%', shadow=True)
	plt.subplot(the_grid[1, 0], aspect=1)
	patches, texts, autotexts = plt.pie(dataA, labels=arrLabels,
	                                    autopct='%.0f%%',
	                                    shadow=True, radius=1.5)

	for t in texts:
	    t.set_size('smaller')
	for t in autotexts:
	    t.set_size('x-small')
	autotexts[0].set_color('y')

	for t in texts:
	    t.set_size('smaller')
	for t in autotexts:
	    t.set_size('x-small')
	autotexts[0].set_color('y')

	plt.show()

	return

def histo(dataA, length, numGroups):
	fig, ax = plt.subplots()
	# Crear histograma con NUMPY
	n, bins = np.histogram(dataA, numGroups)
	left = np.array(bins[:-1])
	right = np.array(bins[1:])
	bottom = np.zeros(len(left))
	top = bottom + n

	XY = np.array([[left, left, right, right], [bottom, top, top, bottom]]).T

	barpath = path.Path.make_compound_path_from_polys(XY)

	patch = patches.PathPatch(
	    barpath, facecolor='blue', edgecolor='gray', alpha=0.8)
	ax.add_patch(patch)

	ax.set_xlim(left[0], right[-1])
	ax.set_ylim(bottom.min(), top.max())

	plt.show()
	
	return

# ---------------------------------------
# PROGRAMA PRINCIPAL
# ---------------------------------------

def run(fileName):

	compiler.compile(fileName)

	global instructionPointer
	global pointersStack
	global memoriesStack
	global local_actual_memory
	global local_next_memory

	cuadruplo = (END, "", "", "")
	compiler.cuadruplos.append(cuadruplo)

	print("---------------")
	print("Virtual Machine")
	print("---------------")

	currentQuadruple = compiler.cuadruplos[instructionPointer]
	actualCode = currentQuadruple[0]
	instructionPointer += 1

	initMemoriaGlobal()

	# print(global_memory)

	while actualCode != END:
		# print(local_actual_memory)

		if actualCode == ADD:
			add(currentQuadruple[1], currentQuadruple[2], currentQuadruple[3])

			currentQuadruple = compiler.cuadruplos[instructionPointer]
			actualCode = currentQuadruple[0]
			instructionPointer += 1
		elif actualCode == SUBSTRACT:
			substract(currentQuadruple[1], currentQuadruple[2], currentQuadruple[3])

			currentQuadruple = compiler.cuadruplos[instructionPointer]
			actualCode = currentQuadruple[0]
			instructionPointer += 1
		elif actualCode == MULTIPLY:
			multiply(currentQuadruple[1], currentQuadruple[2], currentQuadruple[3])

			currentQuadruple = compiler.cuadruplos[instructionPointer]
			actualCode = currentQuadruple[0]
			instructionPointer += 1
		elif actualCode == DIVISION:
			divide(currentQuadruple[1], currentQuadruple[2], currentQuadruple[3])

			currentQuadruple = compiler.cuadruplos[instructionPointer]
			actualCode = currentQuadruple[0]
			instructionPointer += 1
		elif actualCode == RESIDUE:
			residue(currentQuadruple[1], currentQuadruple[2], currentQuadruple[3])

			currentQuadruple = compiler.cuadruplos[instructionPointer]
			actualCode = currentQuadruple[0]
			instructionPointer += 1
		elif actualCode == LESS_THAN:
			lessThan(currentQuadruple[1], currentQuadruple[2], currentQuadruple[3])

			currentQuadruple = compiler.cuadruplos[instructionPointer]
			actualCode = currentQuadruple[0]
			instructionPointer += 1
		elif actualCode == GREATER_THAN:
			greaterThan(currentQuadruple[1], currentQuadruple[2], currentQuadruple[3])

			currentQuadruple = compiler.cuadruplos[instructionPointer]
			actualCode = currentQuadruple[0]
			instructionPointer += 1
		elif actualCode == LESS_EQUAL:
			lessThanEqual(currentQuadruple[1], currentQuadruple[2], currentQuadruple[3])

			currentQuadruple = compiler.cuadruplos[instructionPointer]
			actualCode = currentQuadruple[0]
			instructionPointer += 1
		elif actualCode == GREATER_EQUAL:
			greaterThanEqual(currentQuadruple[1], currentQuadruple[2], currentQuadruple[3])

			currentQuadruple = compiler.cuadruplos[instructionPointer]
			actualCode = currentQuadruple[0]
			instructionPointer += 1
		elif actualCode == EQUAL:
			equal(currentQuadruple[1], currentQuadruple[2], currentQuadruple[3])

			currentQuadruple = compiler.cuadruplos[instructionPointer]
			actualCode = currentQuadruple[0]
			instructionPointer += 1
		elif actualCode == DIFFERENT:
			different(currentQuadruple[1], currentQuadruple[2], currentQuadruple[3])

			currentQuadruple = compiler.cuadruplos[instructionPointer]
			actualCode = currentQuadruple[0]
			instructionPointer += 1
		elif actualCode == AND:
			andOp(currentQuadruple[1], currentQuadruple[2], currentQuadruple[3])

			currentQuadruple = compiler.cuadruplos[instructionPointer]
			actualCode = currentQuadruple[0]
			instructionPointer += 1
		elif actualCode == OR:
			orOp(currentQuadruple[1], currentQuadruple[2], currentQuadruple[3])

			currentQuadruple = compiler.cuadruplos[instructionPointer]
			actualCode = currentQuadruple[0]
			instructionPointer += 1
		elif actualCode == ASSIGN:
			assign(currentQuadruple[1], currentQuadruple[3])

			currentQuadruple = compiler.cuadruplos[instructionPointer]
			actualCode = currentQuadruple[0]
			instructionPointer += 1
		elif actualCode == PRINT:
			while actualCode == PRINT:
				toPrint = ''
				
				value = getValueForAddress(currentQuadruple[3])
				value = str(value)
			
				if value == '%n':
					print()
				else:
					toPrint += value
					toPrint += ' '
				
					print(toPrint, end='')
			
				currentQuadruple = compiler.cuadruplos[instructionPointer]
				actualCode = currentQuadruple[0]
				instructionPointer += 1

		elif actualCode == READ:
			toRead = raw_input()

			addressType = compiler.getTypeForAddress(currentQuadruple[3])

			if addressType == INT:
				try:
					saveValueToAddress(int(toRead), currentQuadruple[3])
				except ValueError:
					semanticErrorHalt("Invalid input for integer varaible")

			elif addressType == FLOAT:
				try:
					saveValueToAddress(float(toRead), currentQuadruple[3])
				except ValueError:
					semanticErrorHalt("Invalid input for float varaible")

			elif addressType == BOOL:
				toRead = toRead.lower()

				if toRead == 'true' or toRead == 't':
					saveValueToAddress(True, currentQuadruple[3])
				elif toRead == 'false' or toRead == 'f':
					saveValueToAddress(False, currentQuadruple[3])
				else:
					semanticErrorHalt("Invalid input for boolean variable")

			elif addressType == STRING:
				saveValueToAddress(str(toRead), currentQuadruple[3])

			currentQuadruple = compiler.cuadruplos[instructionPointer]
			actualCode = currentQuadruple[0]
			instructionPointer += 1
		elif actualCode == GOTOF:
			if not getValueForAddress(currentQuadruple[1]):
				instructionPointer = currentQuadruple[3]

			currentQuadruple = compiler.cuadruplos[instructionPointer]
			actualCode = currentQuadruple[0]
			instructionPointer += 1
		elif actualCode == GOTOV:
			if getValueForAddress(currentQuadruple[1]):
				instructionPointer = currentQuadruple[3]

			currentQuadruple = compiler.cuadruplos[instructionPointer]
			actualCode = currentQuadruple[0]
			instructionPointer += 1
		elif actualCode == GOTO:
			toAddress = currentQuadruple[3]
			instructionPointer = toAddress

			currentQuadruple = compiler.cuadruplos[instructionPointer]
			actualCode = currentQuadruple[0]
			instructionPointer += 1
		elif actualCode == ERA:
			procName = currentQuadruple[1]
			size = []

			for proc in compiler.dir_procs:
				if proc[0] == procName:
					size = proc[6]

					break

			era(size)

			currentQuadruple = compiler.cuadruplos[instructionPointer]
			actualCode = currentQuadruple[0]
			instructionPointer += 1
		elif actualCode == GOSUB:
			memoriesStack.append(local_actual_memory)
			local_actual_memory = local_next_memory
			pointersStack.append(instructionPointer)

			instructionPointer = currentQuadruple[3]

			currentQuadruple = compiler.cuadruplos[instructionPointer]
			actualCode = currentQuadruple[0]
			instructionPointer += 1
		elif actualCode == RETORNO:
			instructionPointer = pointersStack.pop()
			local_actual_memory = memoriesStack.pop()

			currentQuadruple = compiler.cuadruplos[instructionPointer]
			actualCode = currentQuadruple[0]
			instructionPointer += 1
		elif actualCode == PARAM:
			saveValueToNewMemory(getValueForAddress(currentQuadruple[1]), currentQuadruple[3])
			
			currentQuadruple = compiler.cuadruplos[instructionPointer]
			actualCode = currentQuadruple[0]
			instructionPointer += 1
		elif actualCode == FUNCRETURN:
			value = getValueForAddress(currentQuadruple[1])
			saveValueToAddress(value, currentQuadruple[3])

			currentQuadruple = compiler.cuadruplos[instructionPointer]
			actualCode = currentQuadruple[0]
			instructionPointer += 1
		elif actualCode == VER:
			value = getValueForAddress(currentQuadruple[3])

			if value < currentQuadruple[1] or value > currentQuadruple[2]:
				semanticErrorHalt("Array index out of range")

			currentQuadruple = compiler.cuadruplos[instructionPointer]
			actualCode = currentQuadruple[0]
			instructionPointer += 1
		elif actualCode == NEG:
			value = getValueForAddress(currentQuadruple[1])

			if compiler.getTypeForAddress(currentQuadruple[3]) == BOOL:
				saveValueToAddress(not value, currentQuadruple[3])
			else:
				saveValueToAddress(-1 * value, currentQuadruple[3])

			currentQuadruple = compiler.cuadruplos[instructionPointer]
			actualCode = currentQuadruple[0]
			instructionPointer += 1
		elif actualCode == AVERAGE:
			result = getAverage(currentQuadruple[1], getValueForAddress(currentQuadruple[2]))
			saveValueToAddress(result, currentQuadruple[3])

			currentQuadruple = compiler.cuadruplos[instructionPointer]
			actualCode = currentQuadruple[0]
			instructionPointer += 1
		elif actualCode == VARIANCE:
			result = getVariance(currentQuadruple[1], getValueForAddress(currentQuadruple[2]))
			saveValueToAddress(result, currentQuadruple[3])

			currentQuadruple = compiler.cuadruplos[instructionPointer]
			actualCode = currentQuadruple[0]
			instructionPointer += 1
		elif actualCode == STDEV:
			result = getStdDeviation(currentQuadruple[1], getValueForAddress(currentQuadruple[2]))
			saveValueToAddress(result, currentQuadruple[3])

			currentQuadruple = compiler.cuadruplos[instructionPointer]
			actualCode = currentQuadruple[0]
			instructionPointer += 1
		elif actualCode == SUM:
			result = getSum(currentQuadruple[1], getValueForAddress(currentQuadruple[2]))
			
			if compiler.getTypeForAddress(currentQuadruple[3]) == INT:
				result = int(result)
			
			saveValueToAddress(result, currentQuadruple[3])

			currentQuadruple = compiler.cuadruplos[instructionPointer]
			actualCode = currentQuadruple[0]
			instructionPointer += 1
		elif actualCode == MUL:
			result = getMul(currentQuadruple[1], getValueForAddress(currentQuadruple[2]))

			if compiler.getTypeForAddress(currentQuadruple[3]) == INT:
				result = int(result)
			
			saveValueToAddress(result, currentQuadruple[3])

			currentQuadruple = compiler.cuadruplos[instructionPointer]
			actualCode = currentQuadruple[0]
			instructionPointer += 1

		elif actualCode == STACKED:
			length = getValueForAddress(currentQuadruple[3])
			dataA = getArrayValues(currentQuadruple[1], length)
			dataB = getArrayValues(currentQuadruple[2], length)

			stacked(dataA, dataB, length, getValueForAddress(currentQuadruple[4]), getValueForAddress(currentQuadruple[5]))

			currentQuadruple = compiler.cuadruplos[instructionPointer]
			actualCode = currentQuadruple[0]
			instructionPointer += 1

		elif actualCode == BARS:
			length = getValueForAddress(currentQuadruple[3])
			dataA = getArrayValues(currentQuadruple[1], length)
			print(local_actual_memory)
			print(currentQuadruple[2])
			labels = getArrayValues(currentQuadruple[2], length)



			bars(dataA, labels, length, getValueForAddress(currentQuadruple[4]))

			currentQuadruple = compiler.cuadruplos[instructionPointer]
			actualCode = currentQuadruple[0]
			instructionPointer += 1

		elif actualCode == DBARS:
			length = getValueForAddress(currentQuadruple[4])
			dataA = getArrayValues(currentQuadruple[1], length)
			dataB = getArrayValues(currentQuadruple[2], length)
			labels = getArrayValues(currentQuadruple[3], length)

			dBars(dataA, dataB, labels, length, getValueForAddress(currentQuadruple[5]), getValueForAddress(currentQuadruple[6]))

			currentQuadruple = compiler.cuadruplos[instructionPointer]
			actualCode = currentQuadruple[0]
			instructionPointer += 1

		elif actualCode == PIE:
			length = getValueForAddress(currentQuadruple[3])

			dataA = getArrayValues(currentQuadruple[1], length)
			arrLabels = getArrayValues(currentQuadruple[2], length)

			print("----------------")
			print(arrLabels)
			print(length)

			pie(dataA, arrLabels, length)

			currentQuadruple = compiler.cuadruplos[instructionPointer]
			actualCode = currentQuadruple[0]
			instructionPointer += 1

		elif actualCode == HISTO:
			print("Empieza Histo")
			length = getValueForAddress(currentQuadruple[2])
			dataA = getArrayValues(currentQuadruple[1], length)

			histo(dataA, length, getValueForAddress(currentQuadruple[3]))

			currentQuadruple = compiler.cuadruplos[instructionPointer]
			actualCode = currentQuadruple[0]
			instructionPointer += 1

	# print(global_memory)
	# print(local_actual_memory)

	print("\nEND OF PROGRAM\n\n")

run("tests/input4.txt")
