import numpy as np
import math

def annualizer(daliy_return, investment_period):

    annualized_return = daliy_return ** (365/investment_period) - 1

    return annualized_return



