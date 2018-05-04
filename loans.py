# -*- coding: utf-8 -*-
import decimal as dc
import numpy as np
import pandas as pd
from datetime import datetime
from dateutil.relativedelta import relativedelta

# increase decimal precision
dc.getcontext().prec = 64

def compute_annuity(apr,principal,nterms):
    """Computes and returns the annuity of a basic consumer loan.

    Args:
        apr: The APR of the loan.
        principal: The initial size of the loan.
        nterms: The number of terms (in month) of the loan.

    Returns:
        decimal: A Decimal object representing the monthly annuity.
    """
    
    # typecasting to make sure type for precise computation
    principal = dc.Decimal(str(principal))
    nterms = int(nterms)
    
    # compute the monthly interest rate
    interest = compute_monthly_rate(apr)
    
    # compute the annuity
    A = principal*(interest*(1+interest)**nterms)/(-1+(1+interest)**nterms)
    
    # returns the annuity
    return A

def compute_monthly_rate(apr):
    """Computes and returns the monthly rate of an APR

    Args:
        apr: The APR of the loan.

    Returns:
        decimal: A Decimal object representing the monthly rate.
    """
    apr = dc.Decimal(str(apr))
    return (1 + apr) ** (dc.Decimal('1.0') / dc.Decimal('12.0')) - 1

def get_cashflow_schedule(apr,principal,nterms,date0,dateT):
    """Computes and returns a dataframe of cashflow schedule.

    Args:
        apr: The APR of the loan.
        principal: The initial size of the loan.
        nterms: The number of terms (in month) of the loan.
        date0: The start date of the loan.
        dateT: The repayment date of the loan.

    Returns:
        dataframe: A Pandas object with the cashflow schedule.
    """
    # initial balance
    balance = dc.Decimal(principal)
    # compute annuity
    annuity = compute_annuity(apr,principal,nterms)
    
    # initial cashflow list of list of strings
    cashflow_list = [['0','0','0',principal]]
    
    # initialise list of payment dates
    date_list = [date0]
    
    # for each term
    for i in xrange(int(nterms)):
        # current payment is the annuity
        payment = annuity
        # compute interest component
        interest_component = compute_monthly_rate(apr)*balance
        # compute principal component
        principal_component = payment-interest_component
        # adjust balance
        balance = abs(balance-principal_component)
        # append to cashflow list of list
        info_list = [payment,interest_component,principal_component,balance]
        cashflow_list.append(map(round_to_penny,info_list))
        # get next payment date
        next_date = datetime.strptime(date_list[-1],'%Y-%m-%d')+relativedelta(months=1)
        date_list.append(next_date.strftime('%Y-%m-%d'))
        
    # make dataframe less payment dates
    df = pd.DataFrame(cashflow_list,
                      columns=['Annuity (£)',
                               'Interest Component (£)',
                               'Principal Component (£)',
                               'Balance (£)'])
    # complete data frame with payment dates
    df['Date'] = date_list
    
    return df

def round_to_penny(amount):
    """Rounds a decimal object amount to penny.

    Args:
        amount: The amount to round.

    Returns:
        string: A string stating the amount rounded to penny.
    """
    return amount.quantize(dc.Decimal('0.01'),rounding=dc.ROUND_HALF_UP)