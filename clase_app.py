#/usr/bin/env python
# -*- coding: utf-8 -*-
#
#  app.py
#
#  Aplicación del método de la inversa a un Proyecto de Inversión
#  
#  Copyright 2013 facundo <flores.facundogabriel@gmail.com>
#  
#  This program is free software; you can redistribute it and/or modify
#  it under the terms of the GNU General Public License as published by
#  the Free Software Foundation; either version 2 of the License, or
#  (at your option) any later version.
#  
#  This program is distributed in the hope that it will be useful,
#  but WITHOUT ANY WARRANTY; without even the implied warranty of
#  MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
#  GNU General Public License for more details.
#  
#  You should have received a copy of the GNU General Public License
#  along with this program; if not, write to the Free Software
#  Foundation, Inc., 51 Franklin Street, Fifth Floor, Boston,
#  MA 02110-1301, USA.
#  
#  

import numpy as np
import matplotlib.pyplot as plt
import random 
import math

def dist_triangular(a, b, c):
	r = random.random()
	if r < float(b - a) / float(c - a):
		return a + math.sqrt(r * (b - a) * (c - a))
	return c - math.sqrt((1 - r) * (c - a) * (c - b))

class Flujo_Fondos:
	def __init__(self, duracion, ventas, costos_anuales_sin_amort,
							porcentaje_valor_residual, tasa_impuesto, 
							iat, iaf, tasa_inflacion):
		self.duracion = duracion
		self.ventas = ventas
		self.costos_anuales_sin_amort = costos_anuales_sin_amort
		self.porcentaje_valor_residual = porcentaje_valor_residual
		self.tasa_impuesto = tasa_impuesto
		self.iat = iat
		self.iaf = iaf
		self.tasa_inflacion = tasa_inflacion

		#Vectores del calculo de Flujo de Fondos
		self.ventas_totales = []
		self.costos_totales_sin_amor = []
		self.utilidades_netas = []
		self.ffo = []
		self.fft = []
		self.fft_inflacion = []

		self.tir = 0

	def calc_costos_totales(self):				
		costo = (self.iaf - self.iaf * self.porcentaje_valor_residual) / self.duracion
		costo = costo + self.costos_anuales_sin_amort
		return [costo] * (self.duracion + 1)
	
	def calc_utilidad_neta(self):
		v = [0] * (self.duracion + 1)
		for i in range(self.duracion):
			v[i + 1] = (self.ventas_totales[i] - self.costos_totales_sin_amor[i]) * (1 - self.tasa_impuesto)
		return v
		
	def calc_ffo(self):
		v = [0] * (self.duracion + 1)
		delta_aj = (self.iaf - self.iaf * self.porcentaje_valor_residual) / self.duracion
		for i in range(self.duracion):
			v[i + 1] = self.utilidades_netas[i + 1] + delta_aj
		v[self.duracion] = v[self.duracion] + self.iaf * self.porcentaje_valor_residual + self.iat
		return v
	
	def calc_fft(self):
		return [(self.iat + self.iaf) * (-1)] + self.ffo[1:]

	def calc_inflacion(self):
		v = [0] * (self.duracion + 1)
		for i in range(self.duracion + 1):
			v[i] = self.fft[i] / math.pow(1 + self.tasa_inflacion, i)
		return v

	def calc_tir(self):
		v = [int(x) for x in self.fft_inflacion]
		self.tir = round(np.irr(v), len(v))

	def calc_flujo_fondos(self):
	
		self.ventas_totales = [self.ventas] * (self.duracion + 1)
		self.costos_totales_sin_amor = self.calc_costos_totales()
		self.utilidades_netas = self.calc_utilidad_neta()
		self.ffo = self.calc_ffo()
		self.fft = self.calc_fft()
		self.fft_inflacion = self.calc_inflacion()


	def calcular_tir(self):
		self.calc_tir()

	def get_tir(self):
		return self.tir

class Simulador_Flujo_Fondos():

	def __init__(self, Cantidad_Simulaciones):
		self.times = Cantidad_Simulaciones
		self.v_tirs = []
		self.tir_optimista = 0
		self.tir_pesimista = 0

	def plotear_histograma(self):
		a = np.array(self.v_tirs)
		plt.hist(a, 32, normed=0, facecolor='blue', alpha = 0.25)
		plt.title("Histograma de la simulacion con " + str(self.times) + " pruebas")
		plt.savefig("histograma.png")
		#plt.clf()

	def plotear_ojiva(self):
		a = np.array(self.v_tirs)
		bins = np.arange(int(self.tir_pesimista), int(self.tir_optimista) + 2)
		histogram = np.histogram(a, bins = bins, normed = True)
		v = []
		s = 0.0
		for e in histogram[0]:
			s = s + e
			v.append(s)
		v[0] = histogram[0][0]
		plt.plot(v)
		plt.title("Ojiva de la simulacion con " + str(self.times) + "pruebas")
		plt.savefig("ojiva.png")
		#plt.clf()

	def Simular(self):

		print "Inicio de Simulacion"
		
		optimista = Flujo_Fondos(10, 1500000, 380000, 0.2, 0.3 , 100000, 1500000, 0.15)
		pesimista = Flujo_Fondos(10, 1250000, 395000, 0.2, 0.3, 300000, 2000000, 0.25)

		optimista.calc_flujo_fondos()
		pesimista.calc_flujo_fondos()

		optimista.calcular_tir()
		pesimista.calcular_tir()

		self.tir_optimista = optimista.get_tir() * 100
		self.tir_pesimista = pesimista.get_tir() * 100

		self.v_tirs.append(self.tir_optimista)
		self.v_tirs.append(self.tir_pesimista)

		for i in range(self.times):
			iaf = dist_triangular(1500000, 1800000, 2000000)
			iat = dist_triangular(100000, 220000, 300000)
			ventas_anuales = dist_triangular(1250000, 1400000, 1500000)
			costos_sin_amort = dist_triangular(380000, 390000, 395000)
			tasa_inflacion = dist_triangular(0.15, 0.20, 0.25)

			estocastico = Flujo_Fondos(10, ventas_anuales, costos_sin_amort,
										0.2, 0.3, iat, iaf, tasa_inflacion)

			estocastico.calc_flujo_fondos()
			estocastico.calcular_tir()

			tir_estocastica = estocastico.get_tir() * 100
			self.v_tirs.append(tir_estocastica)

		print "Fin de la simulacion"

	def Guardar_Imagenes(self):
		self.plotear_ojiva()
		self.plotear_histograma()
		print "Imagenes Guardadas"

def main():
	S = Simulador_Flujo_Fondos(100000)
	S.Simular()
	S.Guardar_Imagenes()
	return 

if __name__ == '__main__':
	main()



		