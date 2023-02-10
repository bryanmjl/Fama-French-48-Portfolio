# Import Libraries
import numpy as np
import pandas as pd
import scipy.optimize as opt
from sklearn.covariance import EmpiricalCovariance
from sklearn.linear_model import LinearRegression
import statistics
import warnings
warnings.filterwarnings("ignore")
import pypfopt as pyp

# A. Portfolio Performance Functions
def estimate_V (data):
    '''
    Get the Covariance Matrix 
    :param data: data (Excess risk free) excluding Mkt-Rf, Month and RF  
    '''
    Vhat = EmpiricalCovariance().fit(data).covariance_
    
    return Vhat

def estimate_mu (data):
    '''
    Get the average return of each industry
    :param data: data (Excess risk free) excluding Mkt-Rf, Month and RF  
    '''
    mu_hat = EmpiricalCovariance().fit(data).location_
    
    return mu_hat

def evaluate_portfolio_performance_on_data(w, data_evaluate):
    '''
    Get Expected Return and Variance of portfolio
    :param w: weights of portfolio to evaluate the performance on
    :param data_evaluate: test data to evaluate performance on 
    '''
    w = w.reshape((-1))
    if (data_evaluate.shape[1] != len(w)):
        print('Warning: data and w should contain the same number of assets')
    
    V = estimate_V (data_evaluate)
    mu = estimate_mu (data_evaluate)
    
    return {'Er': mu.T @ w, 'sigma': np.sqrt(w.T @ V @ w), 
            'var': w.T @ V @ w, 'Sharpe': (mu.T @ w - 0)/(np.sqrt(w.T @ V @ w)) }

# B. Optimal Weights Function
def tangency(mu, V):
    '''
    Get the Weights of Tangency Portfolio
    :param mu: returns
    :param V: Covariance Matrix
    '''    
    # np.linalg.inv gives inverse of a matrix; mu gives mean of each column industry
    # np.linalg.inv(V) has shape of (48.48) / V has shape of (48,1)
    # np.linalg.inv(V) @ mu is a form of matrix multiplication
    w_t = np.linalg.inv(V) @ mu
    w_t /= np.sum(w_t)

    return w_t

def gmv(V):   
    '''
    Get the Weights of GMV Portfolio
    :param V: Covariance Matrix
    '''
    n = len(V)
    w_g = np.linalg.inv(V) @ np.ones(n)
    w_g /= np.sum(w_g)
    
    return w_g

def ewp(n):   
    '''
    Get the Weights of EWP Portfolio
    :param n: No of assets available  
    '''
    return np.ones(n)/n

# C. Covariance Shrinkage Estimator Function
def shrinkcovariance(data, shrinkage):      
    '''
    Get the shrinked covariance based on shrinkage factor and Constant Correlation Matrix
    Formula = Shrinkage * V_CC + (1-Shrinkage) * Cov Matrix 
    :param data: data (Excess risk free) excluding Mkt-Rf, Month and RF
    :param shrinkage:
    '''
    # Find Average Correlation
    num = len(data.corr())
    rho_bar = sum([data.corr().values[i,j] for i in range(num) for j in range(i+1,num)])  
    Denominator = (num * (num - 1))/2
    rho_bar = rho_bar/Denominator  # Get Grand average correlation rho_bar
    
    # Diagonals are left untouched as variances
    SigmaiSigmaj = ( (estimate_V(data))/(data.corr().values) )                 # Get the standard deviation matrix
    Diagonals = np.identity(num) * np.diag(SigmaiSigmaj)                       # Get Diagonals of Std Dev Matrix
    WithoutDiagonals = SigmaiSigmaj - Diagonals                                # Remove diagonals from Std Dev Matrix
    V_CC = WithoutDiagonals * rho_bar + Diagonals                              # Multiply rho_bar except for its diagonals
    Shrinked_Covariance = shrinkage * V_CC + (1-shrinkage) * estimate_V(data)  # Apply shrinkage by using V_CC
    
    return Shrinked_Covariance

# D. Black Litterman
def implied_rets(risk_aversion, sigma, w):
    '''
    Calculate the Implied excess equilibrium returns
    :param risk_aversion: Risk Aversion
    :param sigma: Covariance Matrix
    :param w: Wieghts of Industries
    '''
    # Sigma here is Cov Matrix; w is industry weights in this case
    implied_rets = risk_aversion * sigma.dot(w).squeeze()
    
    return implied_rets

# E. Stress Testing
def stress_test_mkt(val_df, alpha=0.9):
    '''
    Calculate the VaR and ES of the market portfolio worth $10M
    :param val_df: Validation dataset to be used (either val_1_mkt, val_2_mkt or val_3_mkt)
    :param alpha: Probability that VaR is the maximum loss that will occur
    :return: VaR and ES of the portfolio 
    '''
    # convert percentage into numbers
    for column in val_df.columns:
        val_df[column] = val_df[column]/100 + 1
        
    # Current position in USD = 10 Million
    positions = np.array([10000000]).reshape((1,-1))
    
    # Indices for columns with price information
    irange = [2]

    # construct the simulated scenarios
    df_simulation = val_df.iloc[0:, irange]
    df_simulation['Portfolio Value'] = np.sum(df_simulation.values * positions , axis = 1)
    df_simulation['Loss'] = np.sum(positions) - df_simulation['Portfolio Value'] 
    df_simulation.reset_index(inplace = True)
    df_simulation.rename(columns={"index": "Scenario"}, inplace = True)
    df_simulation['Scenario'] = df_simulation['Scenario']+1
    
    # Total number of scenarios
    n = len(df_simulation)
    
    # Defining the confidence level alpha 
    alpha = alpha
    
    # Ranked Loss
    df_loss = df_simulation[['Scenario','Loss']].sort_values(by = 'Loss', ascending = False)
    
    # Basic Historical Simulation Method: VaR and ES calculation using Percentile Function 
    losses = df_simulation.Loss.values

    VaR  = np.percentile(losses, alpha * 100, interpolation = 'higher') 
    ES = np.mean(losses [losses >= VaR])

    return {'VaR': VaR, 'ES': ES}


def stress_test(val_df, w, alpha=0.9):
    '''
    Calculate the VaR and ES of the other portfolios (Excluding Market Porfolio) worth $10M
    :param val_df: Validation dataset to be used (either val_1_mkt, val_2_mkt or val_3_mkt)
    :param alpha: Probability that VaR is the maximum loss that will occur
    :return: VaR and ES of the portfolio 
    '''
    # convert percentage into numbers
    val_df_copy = val_df.copy()
    
    for column in val_df_copy.columns:
        val_df_copy[column] = val_df_copy[column]/100 + 1
    
    # Current position in USD = 10 Million
    positions = np.array(w*10000000).reshape((1,-1))
    
    # Indices for columns with price information
    irange = list(range(48))

    # construct the simulated scenarios
    df_simulation = val_df_copy.iloc[0:, irange]
    df_simulation['Portfolio Value'] = np.sum(df_simulation.values * positions , axis = 1)
    df_simulation['Loss'] = np.sum(positions) - df_simulation['Portfolio Value'] 
    df_simulation.reset_index(inplace = True)
    df_simulation.rename(columns={"index": "Scenario"}, inplace = True)
    df_simulation['Scenario'] = df_simulation['Scenario']+1
    
    # Total number of scenarios
    n = len(df_simulation)
    
    # Defining the confidence level alpha 
    alpha = alpha
    
    # Ranked Loss
    df_loss = df_simulation[['Scenario','Loss']].sort_values(by = 'Loss', ascending = False)
    
    # Basic Historical Simulation Method: VaR and ES calculation using Percentile Function 
    losses = df_simulation.Loss.values

    VaR  = np.percentile(losses, alpha * 100, interpolation = 'higher') 
    ES = np.mean(losses [losses >= VaR])

    return {'VaR': VaR, 'ES': ES}




