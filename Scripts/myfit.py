import numpy as np
from scipy.stats import chi2



# Function to fit a polynomial to data
def fit_polynomial(x, y, y_errors, degree ):
    """
    Fits a polynomial to the given data using least squares.

    Parameters:
        x (array-like): Independent variable.
        y (array-like): Dependent variable.
        yerr (array-like): Error (standard deviation) on the dependent variable.
        degree (int): Degree of the polynomial.

    Returns:
        tuple: Coefficients of the polynomial, 
               their errors, 
               the covariance matrix,
               the Reduced Chi-squared,
               the Root Mean Squared Residual (RMSR),
               the Weighted Root Mean Squared Residual (WRMSR),
               the fitting function
    """
    
    # Perform a weighted polynomial fit
    # in np.polyfit the weight w=1/sigma is equivalent to a weight of 1/sigma^2 
    # in methods which minimize the chi2, as scipy.optimize.curve_fit
    coeffs, cov = np.polyfit(x, y, degree, w=1/y_errors, cov=True)

    # Errors on the coefficients of the fit
    coeffs_err = cov.diagonal()**0.5
    
    # Create the polynomial model
    polynomial = np.poly1d(coeffs)

    # Calculate model predictions
    y_model = polynomial(x)
    
    # Compute residuals
    residuals = y - y_model
    
    # Compute RMSR
    RMSR = np.sqrt(np.mean(residuals**2))

    # Compute chi-squared
    chi_squared = np.sum((residuals / y_errors) ** 2)

    # Degrees of freedom
    N = len(y)  # Number of data points
    k = degree + 1  # Number of parameters in the model
    dof = N - k
    
    # Reduced chi-squared
    chi_squared_reduced = chi_squared / dof

    # Compute Weighted Root Mean Squared Residual
    weights = 1 / y_errors**2  # Weights for the WRMSR calculation
    WRMSR = np.sqrt(np.sum(weights * residuals**2) / np.sum(weights))

    return coeffs, coeffs_err, cov, chi_squared_reduced, RMSR, WRMSR, polynomial


################################################################################


#    Given Y function of X and dependent on padameters a, b, c, ...:
#        Y = a + b X + c X^2 + ...
#    It's variance, from OLS fit, is:
#        Var(Y) = Var(a) + 
#                 Var(b) X^2 + 2 Cov(a,b) X + 
#                 Var(c) X^4 + 2 Cov(a,c) X^2 + 2 Cov(b,c) X^3 + 
#                 ...
#    So, the corresponding error is:
#        Sigma(Y) = sqrt( Var(Y) )
#    This function gives the variance of Y.

def fun_var_y(x, cov):
    """
    Calculates the variance of Y as a function of X and the covariance matrix of the fit parameters.

    Parameters:
    ----------
    x : float
        The value of the independent parameter X.
    cov : numpy.ndarray
        Covariance matrix (square) of the polynomial model parameters.

    Returns:
    -------
    var_y : float
        The variance of Y as a function of X.
    """
    s = 0.0
    # Ensure that the covariance matrix is square
    assert cov.shape[0] == cov.shape[1], "The covariance matrix must be square"
    
    n = cov.shape[0]
    
    # Iterate through all elements of the covariance matrix
    for i in range(n):
        for j in range(n):
            # Accumulate contributions from the covariance matrix elements
            s += cov[i, j] * x**(i + j)
    
    return s




################################################################################

def fun_lin(x, a, b):
    # Linear function: calculates y = a + b * x
    return a + b * x


def fun_quad(x, a, b, c):
    # Quadratic function: calculates y = a + b * x + c * x^2
    return a + b * x + c * x**2


def fun_cub(x, a, b, c, d):
    # Cubic function: calculates y = a + b * x + c * x^2 + d * x^3
    return a + b * x + c * x**2 + d * x**3


def fun_p4(x, a0, a1, a2, a3, a4):
    # Fourth-degree polynomial function: calculates y = a0 + a1 * x + a2 * x^2 + a3 * x^3 + a4 * x^4
    return a0 + a1 * x + a2 * x**2 + a3 * x**3 + a4 * x**4


# Definition of a generic polynomial function
def fun_poly(x, *coeffs):
    """
    Calculates the value of a polynomial based on the provided coefficients.

    Parameters:
        x (float or array-like): The independent variable.
        *coeffs (float): Coefficients of the polynomial.

    Returns:
        float or array-like: The value of the polynomial for the given x.
    """
    return sum(c * x**i for i, c in enumerate(coeffs))


# Definition of chi-squared function
def chi_squared(y_observed, y_expected, error):
    """
    Calculates the chi-squared value.

    Parameters:
        y_observed (array-like): Observed data values.
        y_expected (array-like): Expected data values.
        error (array-like): Error associated with the observed values.

    Returns:
        float: Chi-squared statistic.
    """
    return np.sum(((y_observed - y_expected) / error) ** 2)


# Reduced chi-squared function
def reduced_chi_squared(y_observed, y_expected, error, dof):
    """
    Calculates the reduced chi-squared value.

    Parameters:
        y_observed (array-like): Observed data values.
        y_expected (array-like): Expected data values.
        error (array-like): Error associated with the observed values.
        dof (int): Degrees of freedom.

    Returns:
        float: Reduced chi-squared statistic.
    """
    chi2_value = chi_squared(y_observed, y_expected, error)
    return chi2_value / dof


# Function to calculate the p-value
def p_value(chi2_value, dof):
    """
    Calculates the p-value for a given chi-squared value and degrees of freedom.

    Parameters:
        chi2_value (float): Chi-squared statistic.
        dof (int): Degrees of freedom.

    Returns:
        float: p-value.
    """
    return 1 - chi2.cdf(chi2_value, dof)


