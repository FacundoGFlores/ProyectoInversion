#!/usr/bin/env python
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

def calc_costos_totales(duracion, iaf, costos_anuales_sin_amort, 
							porcentaje_valor_residual):
								
	costo = (iaf - iaf * porcentaje_valor_residual) / duracion
	costo = costo + costos_anuales_sin_amort
	return [costo] * (duracion + 1)
	
def calc_utilidad_neta(duracion, ventas_totales, costos_totales, 
						tasa_impuesto):
	v = [0] * (duracion + 1)
	for i in range(duracion):
		v[i + 1] = (ventas_totales[i] - costos_totales[i]) * (1 - tasa_impuesto)
	return v
		
def calc_ffo(duracion, utilidades_netas, iaf, iat, porcentaje_valor_residual):
	v = [0] * (duracion + 1)
	delta_aj = (iaf - iaf * porcentaje_valor_residual) / duracion
	for i in range(duracion):
		v[i + 1] = utilidades_netas[i + 1] + delta_aj
	v[duracion] = v[duracion] + iaf * porcentaje_valor_residual + iat
	return v
	
def calc_fft(ffo, iat, iaf):
	return [(iat + iaf) * (-1)] + ffo[1:]

def calc_inflacion(duracion, fft, pi):
	v = [0] * (duracion + 1)
	for i in range(duracion + 1):
		v[i] = fft[i] / math.pow(1 + pi, i)
	return v

def calc_tir(fft_inflacion):
	v = [int(x) for x in fft_inflacion]
	return round(np.irr(v), len(v))
	
def calc_flujo_fondos(duracion, ventas, costos_anuales_sin_amort,
							porcentaje_valor_residual, tasa_impuesto, 
							iat, iaf, tasa_inflacion):
	
	# La aplicacion en este caso realiza el calculo de flujo de fondos
	# pero lo que importa en la presentacion del trabajo practico es 
	# el calculo de la TIR(IRR) para cada flujo de fondos, por tanto
	# la función retornará la TIR correspondiente a un FF.
	
	ventas_totales = [ventas] * (duracion + 1)
	costos_totales_sin_amor = calc_costos_totales(duracion, iaf, 
												costos_anuales_sin_amort,
												porcentaje_valor_residual)
	utilidades_netas = calc_utilidad_neta(duracion, ventas_totales, 
											costos_totales_sin_amor,
											tasa_impuesto)
	ffo = calc_ffo(duracion, utilidades_netas, iaf, iat, porcentaje_valor_residual)
	fft = calc_fft(ffo, iat, iaf)
	fft_inflacion = calc_inflacion(duracion, fft, tasa_inflacion)
	
	return calc_tir(fft_inflacion)
	
def array_ojiva(histogram):
	v = []
	s = 0.0
	for e in histogram[0]:
		s = s + e
		v.append(s)
	v[0] = histogram[0][0]
	
	return v
		
def plotear_ojiva(v_tirs, tir_pesimista, tir_optimista):
	a = np.array(v_tirs)
	bins = np.arange(int(tir_pesimista), int(tir_optimista) + 2)
	histogram = np.histogram(a, bins = bins, normed = True)
	v = []
	s = 0.0
	for e in histogram[0]:
		s = s + e
		v.append(s)
	v[0] = histogram[0][0]
	plt.plot(v)
	plt.savefig("ojiva.png")
	
def plotear_histograma(v_tirs):
	a = np.array(v_tirs)
	plt.hist(a, 32, normed=0, facecolor='blue', alpha = 0.25)
	plt.title("Histograma de la simulacion con 10000 pruebas")
	plt.savefig("histograma.png")
	
def simulacion():
	v_tirs = [] #valores de tir
	
	tir_optimista = calc_flujo_fondos(10, 1500000, 380000, 0.2, 0.3 , 100000, 1500000, 0.15) * 100
	tir_pesimista = calc_flujo_fondos(10, 1250000, 395000, 0.2, 0.3, 300000, 2000000, 0.25) * 100
	
	v_tirs.append(tir_optimista)
	v_tirs.append(tir_pesimista)
	
	for i in range(10000):
		iaf = dist_triangular(1500000, 1800000, 2000000)
		iat = dist_triangular(100000, 220000, 300000)
		ventas_anuales = dist_triangular(1250000, 1400000, 1500000)
		costos_sin_amort = dist_triangular(380000, 390000, 395000)
		tasa_inflacion = dist_triangular(0.15, 0.20, 0.25)
		
		tir = calc_flujo_fondos(10, ventas_anuales, costos_sin_amort,
									0.2, 0.3, iat, iaf, tasa_inflacion)
		v_tirs.append(tir * 100)
	
	#plotear_histograma(v_tirs)
	plotear_ojiva(v_tirs, tir_pesimista, tir_optimista)
	
def main():
	simulacion()
	print "IMAGENES GUARDADAS"
	return 

if __name__ == '__main__':
	main()

