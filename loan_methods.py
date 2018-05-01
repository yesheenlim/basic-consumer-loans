import decimal as dc

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
    apr = dc.Decimal(str(apr))
    principal = dc.Decimal(str(principal))
    nterms = int(nterms)
    
    # compute the monthly interest rate
    i = (1 + apr) ** (dc.Decimal('1.0') / dc.Decimal('12.0')) - 1
    
    # compute the annuity
    A = principal*(i*(1+i)**60)/(-1+(1+i)**nterms)
    
    # returns the annuity rounded to nearest penny
    return A.quantize(dc.Decimal('0.01'),rounding=dc.ROUND_HALF_UP)