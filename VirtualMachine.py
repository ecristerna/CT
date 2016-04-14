import CT as compiler

# ---------------------------------------
# VARIABLES GLOBALES
# ---------------------------------------

global_memory = [[], [], [], [], [], [], [], []]
local_actual_memory = [[], [], [], [], [], [], [], []]
local_next_memory = [[], [], [], [], [], [], [], []]

instructionPointer = 0

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
END = 400

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
	if address >= compiler.MIN_INT_GLOBAL and address <= compiler.MAX_INT_GLOBAL:
		return global_memory[0][address - compiler.MIN_INT_GLOBAL]
	elif address >= compiler.MIN_FLOAT_GLOBAL and address <= compiler.MAX_FLOAT_GLOBAL:
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
	leftValue = getValueForAddress(leftOp)
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

	if leftValue < rightValue:
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
	global local_actual_memory

	local_actual_memory = [[], [], [], [], [], [], [], []]

	for x in range(0, size[0]):
		local_actual_memory[0].append(0)

	for x in range(0, size[1]):
		local_actual_memory[1].append(0)

	for x in range(0, size[2]):
		local_actual_memory[2].append(False)

	for x in range(0, size[3]):
		local_actual_memory[3].append("")

	for x in range(0, size[4]):
		local_actual_memory[4].append(0)

	for x in range(0, size[5]):
		local_actual_memory[5].append(0)

	for x in range(0, size[6]):
		local_actual_memory[6].append(False)

	for x in range(0, size[7]):
		local_actual_memory[7].append("")

	print(local_actual_memory)

# ---------------------------------------
# PROGRAMA PRINCIPAL
# ---------------------------------------

def initMemoriaGlobal():
	for variable in compiler.vars_global:
		varType = compiler.getTypeForAddress(compiler.vars_global[variable])

		if varType == INT:
			global_memory[0].append(0)
		elif varType == FLOAT:
			global_memory[1].append(0)
		elif varType == BOOL:
			global_memory[2].append(False)
		elif varType == STRING:
			global_memory[3].append("")

def main():
	global instructionPointer

	cuadruplo = (400, "", "", "")
	compiler.cuadruplos.append(cuadruplo)

	print("---------------")
	print("Virtual Machine")
	print("---------------")

	currentQuadruple = compiler.cuadruplos[instructionPointer]
	actualCode = currentQuadruple[0]
	instructionPointer += 1

	initMemoriaGlobal()

	print(global_memory)

	while actualCode != END:
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
			currentQuadruple = compiler.cuadruplos[instructionPointer]
			actualCode = currentQuadruple[0]
			instructionPointer += 1
		elif actualCode == READ:
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
			currentQuadruple = compiler.cuadruplos[instructionPointer]
			actualCode = currentQuadruple[0]
			instructionPointer += 1
		elif actualCode == RETORNO:
			currentQuadruple = compiler.cuadruplos[instructionPointer]
			actualCode = currentQuadruple[0]
			instructionPointer += 1
		elif actualCode == PARAM:
			currentQuadruple = compiler.cuadruplos[instructionPointer]
			actualCode = currentQuadruple[0]
			instructionPointer += 1
		elif actualCode == FUNCRETURN:
			currentQuadruple = compiler.cuadruplos[instructionPointer]
			actualCode = currentQuadruple[0]
			instructionPointer += 1

	print(local_actual_memory)


main()










