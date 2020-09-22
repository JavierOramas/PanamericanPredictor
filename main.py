import numpy as np
import pandas as pd
from sklearn.preprocessing import PolynomialFeatures
from sklearn.linear_model import LinearRegression
import matplotlib.pyplot as plt
#objeto medalla
class Medallas:
    _name = ''
    _gold = ''
    _gold_range = ''
    _silver = ''
    _silver_range = ''
    _bronze = ''
    _bronze_range = ''

    def __gt__(self,other):
        if self._gold > other._gold:
            return True
        if self._gold < other._gold:
            return False
        if self._gold == other._gold:
            if self._silver > other._silver:
                return True
            if self._silver < other._silver:
                return False
            if self._silver == other._silver:
                if self._bronze > other._bronze:
                    return True
                return False
class predictor:   
    def __init__(self):
        #leemos los datos
        file = pd.read_csv('panamericanos.csv')
        participantes = pd.read_csv('participantes.csv')
        #separamos los datos por países
        matrix = np.array(file)
        self.part_list = np.array(participantes)
        countries = {a : i for i, a in enumerate(set([a[0] for a in matrix[:, 1:2]]))}
        self.dic = dict(countries)
        for i in self.dic:
            self.dic[i] = []
        for i in matrix:
            self.dic[i[1]].append([[i[0]],[i[2]],[i[3]],[i[4]]])


        #calcula las medallas para un país específico
    def calculate_medals(self,current_data,current_target,year):
        pr = PolynomialFeatures(degree=2)
        pr4 = PolynomialFeatures(degree=4)
        poly_data = pr.fit_transform(current_data)
        poly_data4 = pr4.fit_transform(current_data)
        pr.fit(poly_data,current_target)
        pr4.fit(poly_data4,current_target)
        linear_reg = LinearRegression(normalize = True)
        linear_reg.fit(poly_data,current_target)
        linear_reg4 = LinearRegression(normalize = True)
        linear_reg4.fit(poly_data4,current_target)
        temp = linear_reg.predict(pr.fit_transform(year))
        temp2 = linear_reg4.predict(pr4.fit_transform(year)) 
        range = '['+str(self.remove_negatives(temp2[0][0]))+' - '+str(self.remove_negatives(temp[0][0]))+']'
        return (self.remove_negatives(temp[0][0])+self.remove_negatives(temp2[0][0]))/2, range

    def remove_negatives(self,temp):
        if (temp < 0):
            return 0
        return temp 
        
    def get_list(self,year):
        medallas2019 = []
        for item in self.dic:
            if item in self.part_list:
                newCountry = Medallas()
                newCountry._name = item
                value = self.dic[item][:]  
                data = [x[0] for x in value]
                target = [x[1] for x in value]
                temp,range = self.calculate_medals(data,target,year)
                newCountry._gold = np.rint(self.remove_negatives(temp))
                newCountry._gold_range=range
                target = [x[2] for x in value]
                temp,range = self.calculate_medals(data,target,year)
                newCountry._silver = np.rint(self.remove_negatives(temp))
                target = [x[3] for x in value]
                temp,range = self.calculate_medals(data,target,year)
                newCountry._bronze = np.rint(self.remove_negatives(temp))
                medallas2019.append(newCountry)
        medallas2019.sort(reverse = True)
        return medallas2019
        
    def get_graphics(self,country):
        value = self.dic[country][:]  
        current_data = [x[0] for x in value]
        for item in range(3):
            current_target = [x[item+1] for x in value]
            pr = PolynomialFeatures(degree=2)
            pr4 = PolynomialFeatures(degree=4)
            poly_data = pr.fit_transform(current_data)
            poly_data4 = pr4.fit_transform(current_data)
            pr.fit(poly_data,current_target)
            pr4.fit(poly_data4,current_target)
            linear_reg = LinearRegression(normalize = True)
            linear_reg.fit(poly_data,current_target)
            linear_reg4 = LinearRegression(normalize = True)
            linear_reg4.fit(poly_data4,current_target)
            plt.scatter(current_data,current_target, color = 'blue', label="medallas historicas")
            plt.plot(current_data,linear_reg.predict(pr.fit_transform(current_data)), color="red",label="prediccion polinomio grado 2")
            plt.plot(current_data,linear_reg4.predict(pr4.fit_transform(current_data)), color="orange", label="prediccion polinomio grado 4")
            plt.legend()
            if(item == 0):
                plt.xlabel('Oro')
                plt.savefig('/img/Oro.png')
            if(item == 1):
                plt.xlabel('Plata')
                plt.savefig('/img/' + country + 'Plata.png')
            if(item == 2):
                plt.xlabel('Bronce')
                plt.savefig('/img/' + country + 'Bronce.png')

a = predictor()
