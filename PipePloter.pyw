# ===============================================
# GremDev
# Contact: greminoficial@gmail.com
# 2019
#
# ===============================================

import numpy as np

from mpl_toolkits.mplot3d import Axes3D
import matplotlib.pyplot as plt
from matplotlib import cm

import collections
import itertools
import os



def Graficar(data):
	"""
		Recive un multiarray de datos del formato:
		- [Pozo ,Formación, valor_x , valor_y , valor_z],
		- [Pozo ,Formación, valor_x , valor_y , valor_z]
	"""


	# Creo los elementos para la graficacion ------------------------------ ****

	canvas = plt.figure()
	ax = Axes3D(canvas)

	# LLamado a las funciones independientes de graficación
	try:
		create_surface(data, ax)
		create_pipes(data, ax)

		plt.show()

	except expression as identifier:
		pass


#


def create_surface(data = [] , enviroment = None):
	"""
		Documentation
	"""

	# Asignacion de ambiente o creacion de uno.
	if enviroment is not None:
		axis = enviroment
	else:
		__canvas = plt.figure()
		axis = Axes3D(__canvas)

	if not data:
		print('Data array invalid')
		return Exception


	# Agrupo los datos por formacion -------------------------------------- ****
	diccionario_formaciones = collections.defaultdict(list)
	for sublist in data:
		diccionario_formaciones[sublist[1]].append(sublist)

	# Creo las superficies ------------------------------------------------- ****

	for sub in diccionario_formaciones:

		formacion = np.array(diccionario_formaciones[sub])

		# Se extrane los valores X y Y y se ordenan
		X = formacion[:,2]
		X = [float(i) for i in X]
		X.sort()
		X = np.array(
				[X]
			)

		Y = formacion[:,3]
		Y = [float(i) for i in Y]
		Y.sort()
		Y = np.array(
				[Y]
			)



		# Hay que reescribir este codigo para generar  una mesh resultante con
		# profundidades exactas
		Z = formacion[:,4]
		Z = [float(i) for i in Z]
		Z.sort()
		Z = np.array(
				[Z]
			)

		# print(X)
		# print(Y)
		# print(Z)
		# print('--------------------------------------------------------')


		X, Y  = np.meshgrid(X, Y)
		axis.plot_surface(X, Y, Z,linewidth=100, antialiased=False, alpha=0.9)



def create_pipes(data = [] , enviroment = None):

	# Asignacion de ambiente o creacion de uno.
	if enviroment is not None:
		axis = enviroment
	else:
		__canvas = plt.figure()
		axis = Axes3D(__canvas)

	if not data:
		print('Data array invalid')
		return Exception

	# Agrupo los datos por pozo ------------------------------------------- ****
	diccionario_pozos = collections.defaultdict(list)
	for sublist in data:
		diccionario_pozos[sublist[0]].append(sublist)

	# Creo las tuberias --------------------------------------------------- ****

		# Itero sobre cada elementos del diccionario, en este caso
		# sobre cada pozo. 		Solo sobre el indice, no los valores.
	for d in diccionario_pozos:
		# print(diccionario[d]) # 2

		# Extrae los valores del diccionario segun el indice
		# Es decir segun el pozo
		dat = diccionario_pozos[d]
		dat = np.array(dat)

		dat = dat[:,2:5]

		reductor = 1

		x = dat[:,0]
		x = [(float(i))/reductor for i in x]
		# Convierte a flotante y de paso divide por si acaso.
		# Los datos son string antes de realizar esta conversión.
		y = dat[:,1]
		y = [(float(i))/reductor for i in y]

		z = dat[:,2]
		z = [(float(i))/reductor for i in z]

		# print(x)
		# print(y)
		# print(z)
		# print('------------------------')

		axis.plot(xs=x, ys=y, zs=z, alpha = 1, linewidth = 1.5)








import tkinter as tk
from tkinter import ttk
from tkinter import filedialog

class Ventana(tk.Tk):

	def __init__(self):
		"""
			Genera una ventana con la funcionalidad de generar un FileDialog.
		"""
		tk.Tk.__init__(self)
		self.title('Graficar datos')

		# Configuración basica de componentes de interfaz
		self.quitButton = tk.Button(self, width=12, text='Abrir archivo', bg='grey',command=self.buscar_archivo)
		self.quitButton.grid(row=0, column=0, padx=8, pady=8)

		self.lbl_archivo = tk.Label(self, text='')
		self.lbl_archivo.grid(row=0, column=1, padx=8, pady=8)

		self.geometry('400x200')


		# Iniciación de variables

		self.__datos_pozos_actual = []
		self.last_path = '/'

	def buscar_archivo(self):
		archivo_pozos = filedialog.askopenfilename(initialdir= self.last_path,title = 'Elige un archivo',filetype=(('csv','*.csv'),('Excél','*.xlsx')))
		try:
			if archivo_pozos is not '':
				salida = []
				__salida = []


				# Y procesa los datos dentro agregandolos al array de salida
				with open(archivo_pozos, mode = 'r', encoding='utf-8') as f:
					self.lbl_archivo.configure(text = os.path.basename(f.name), foreground = 'black')

					self.last_path = os.path.dirname(archivo_pozos)

					# print('Antes del split')
					# print(f)

					# Las siguientes lineas se encargan de procesar el archivo
					lineas = f.read().splitlines()
					# print(lineas)

					# Separo los elementos por tuplas que contienen un string de todos los valores separados por ;
					for i in lineas:
						salida.append(i.split(','))

						print(i)

					#Separo el string de acuerdo al ;
					for f in salida:
						f = f[0].split(';')
						__salida.append(f)

				# Se elimina la primera linea, correspondiente a los labels
				__salida.pop(0)

				self.__datos_pozos_actual = __salida

				# Creo el botón graficár en caso de que todo este correcto
				self.quitButton = tk.Button(self, width=12, text='Graficar',command=self.call_plot)
				self.quitButton.grid(row=1, column=0, padx=8, pady=8)

			else:
				self.lbl_archivo.configure(text = 'Seleccione un archivo!', foreground = 'red')
				self.__datos_pozos_actual = []
		except IOError:
			self.lbl_archivo.configure(text = 'Error al intentar abrir el archivo', foreground = 'red')

	# Manda  a llamar a la funcionar Graficar, traida desde este propio documento
	# Seccion principal encargada del tratamiento de los datos
	def call_plot(self):
		if self.__datos_pozos_actual:
			Graficar(self.__datos_pozos_actual)
		else:
			self.lbl_archivo.configure(text = 'No hay datos')


if __name__ == "__main__":

	ventana = Ventana()
	ventana.mainloop()



"""
	The next lines are the format example of the input files
	if the file choosen arent like this format it will not work properly
"""
# [
# 	['T-1', 'FILISOLA', 476051.01, 1979266.25, 0],
# 	['T-1', 'MIOCENO', 476051.01, 1979266.25, -2778],
# 	['T-1', 'OLIGOCENO', 476053.11, 1979267.97, -3062],
# 	['T-1', 'EOCENO', 476025.58, 1979280.97, -3473]
# ]

# [
# 	['T-1001', 'FILISOLA', 476048.4, 1979191.82, 0],
# 	['T-1001', 'MIOCENO', 476048.4, 1979191.82, -2780],
# 	['T-1001', 'OLIGOCENO', 476048.25, 1979178.36, -3039],
# 	['T-1001', 'EOCENO', 476049.89, 1979174.71, -3519]
# ]

# [
# 	['T-11', 'FILISOLA', 474768.61, 1979910.34, 0],
# 	['T-11', 'MIOCENO', 474768.61, 1979910.34, -2567],
# 	['T-11', 'OLIGOCENO', 474620.66, 1979645.54, -3068],
# 	['T-11', 'EOCENO', 474504.87, 1979435.57, -3464]
# ]
