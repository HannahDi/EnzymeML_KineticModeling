'''
Created on 24.05.2021

@author: HD
'''

import numpy as np
from scipy.integrate import odeint # solve ode
from lmfit import minimize, Parameters, Parameter, report_fit # fitting

class Modeler:

    def __init__(self):
        '''
        Helper Class to model data from EnzymeML document

        Args:
        '''
        pass

    def solveODE(self, f, t, w0, params):
        '''
        Solution to the ODE w'(t)=f(t,w,p) with initial condition w(0)= w0

        Args:
            f: ODEs
            t: time
            w0: vector of initial states: w0 = [v0, S0]
            params: parameters object from lmfit
        '''

        w = odeint(f, w0, t, args=(params,))
        return w

    def _residual_with_bias(self, params, t, data, f):
        '''
        Calculates residual between measured data and modeled data + bias

        Args:
            params: parameters object from lmfit
            t: time
            data: measured data
            f: ODEs
        '''

        try:
            w0 = params['v0'].value, params['S0'].value
            nW = 1
        except KeyError:
            w0 = params['S0'].value
            nW = 0
        ndata = data.shape[0]
        residual = 0.0*data[:]
        for i in range(ndata):
            model = self.solveODE(f, t, w0, params)
            s_model = model[:,nW]
            s_model_bias = s_model + params['bias'].value
            residual[i,:]=data[i,:]-s_model_bias
        return residual.flatten()

    def _residual(self, params, t, data, f):
        '''
        Calculates residual between measured data and modeled data

        Args:
            params: parameters object from lmfit
            t: time
            data: measured data
            f: ODEs
        '''

        try:
            w0 = params['v0'].value, params['S0'].value
            nW = 1
        except KeyError:
            w0 = params['S0'].value
            nW = 0
        ndata = data.shape[0]
        residual = 0.0*data[:]
        for i in range(ndata):
            model = self.solveODE(f, t, w0, params)
            s_model = model[:,nW]
            residual[i,:]=data[i,:]-s_model
        return residual.flatten()

    def _get_v(self, t, data):
        '''
        Calculates gradient for each datapoint

        Args:
            t: time
            data: measured data
        '''

        v_all = 0.0*data[:] # initialize velocity vector
        for i in range(data.shape[0]):
            prev_value = data[i,0]
            prev_time = 0.0
            for j in range(data.shape[1]):
                if t[j] == 0:
                    delta = prev_value - data[i,j]
                else:
                    delta = abs( (prev_value - data[i,j])/(t[j]-prev_time))
                v_all[i,j] = delta
                prev_value = data[i,j]
                prev_time = t[j]
        v = np.max(v_all, axis=0)
        return v

    def get_initial_vmax(self, t, data):
        '''
        Calculates vmax for parameter initialisation

        Args:
            t: time
            data: measured data
        '''

        v = self._get_v(t, data)
        return np.max(v)

    def get_initial_Km(self, t, data):
        '''
        Returns a value to initialise the Km parameter

        Args:
            t: time
            data: measured data
        '''

        v = self._get_v(t, data)
        idx_max = np.where(v == np.max(v))[0][0]
        idx_Km = (np.abs(v[idx_max:]-np.max(v)/2)).argmin()
        km = np.mean(data, axis=0)[idx_max+idx_Km]
        bias = self.get_initial_bias(data)
        if km > bias:
            km = km - bias
        return km

    def get_initial_bias(self, data):
        '''
        Returns a value to initialise the bias parameter

        Args:
            data: measured data
        '''

        bias = np.mean(data, axis=0)[-1]
        return bias

    def get_initial_S0(self, data):
        '''
        Returns the mean of the first measured value across all replicates

        Args:
            data: measured data
        '''

        s0 = np.mean(data, axis=0)[0]
        return s0

    def fit_model(self, t, data, params, ode):
        '''
        Fit the model with method of least squares

        Args:
            t: time
            data: measured data
            params: parameters object from lmfit
        '''

        try:
            b = params['bias'].value
            result = minimize(self._residual_with_bias , params, args=(t, data, ode), method='leastsq')
        except KeyError:
            result = minimize(self._residual , params, args=(t, data, ode), method='leastsq')
        return result