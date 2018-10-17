
#####################################################################################################################
##      NOTE: all defined functions and the main() function are presented in the same file (main.py) to avoid      ##
##            switching from one file to another when exploring the code.                                          ##
#####################################################################################################################

#---Packages for main script----------------------------------------------------------------------------------------#
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns

#---Defined functions-----------------------------------------------------------------------------------------------#
def factorial(x):
    """
    :Goal: determine the number of ways that one can arrange a group of objects.
    :Package(s): none.

    factorial() is a 3 steps process:
        1- variable num is initiated to 1 so it can be multiplied by anything ;
        2- num is multiplied by parameter x to initiate the factorial operation from x ;
        3- x is multiplied to its descending numbers in a loop until x = 1.

    :param x: the number to calculate the factorial from.
    :return: the result of x!.
    """
    num = 1.
    if x == 0:
        return num
    else:
        while x > 0:
            num = num * x
            x -= 1
        return num

#-------------------------------------------------------------------------------------------------------------------#
def coeff_binom(x, n):
    """
    :Goal: determine the number of combinations that can be created when choosing x objects from a set of n objects.
    :Package(s): none.

    coeff_binom() is a 4 steps process:
        1- x! is calculated and stored in the variable fac_x ;
        2- n! is calculated and stored in the variable fac_n ;
        3- (n-x)! is calculated and stored in the variable fac_nx ;
        4- the number of combinations is calculated by the formula n!/x!(n-x)!.

    :param x: number of objects chosen from the set of n objects.
    :param n: number of objects to choose x objects from.
    :return: the number of possible combinations.
    """
    fac_x = factorial(x)
    fac_n = factorial(n)
    fac_nx = factorial(n-x)
    comb = fac_n / (fac_x *(fac_nx))
    return int(comb)

#-------------------------------------------------------------------------------------------------------------------#
def proba_binom(x, n, p):
    """
    :Goal: compute the probability that a specified number of successes occur (eg: what is the probability to get 6
    heads out of 10 coin flips?).
    :Package(s): none.

    proba_binom() is a 1 step process:
        1- the result is calculated by the formula (n! / x! (n-x)!).(p**x).((1-p)**(n-x)).

    :param x: number of successes during a series of trials.
    :param n: number of trials.
    :param p: probability of success on a single trial.
    :return: the probability that x successes occur.
    """
    prob = coeff_binom(x, n) * (p**x) * ((1-p)**(n-x))
    return prob

#####################################################################################################################

#---Main script-----------------------------------------------------------------------------------------------------#
def main():
    # Table statistique pour 30 dés avec probabilité 1/3
    n = 30
    p = 1/3

    # Calculs de probabilités sous forme de dict transforme en df
    df_proba = pd.DataFrame()

    for j in range(n, 1, -1):
        data = {'n = ' + str(j): [F.proba_binom(i, j, p) for i in np.arange(j + 1)]}
        df_proba = pd.concat([df_proba, pd.DataFrame(data)], axis=1)

    df_proba.index.name = 'x dice'

    # Calculs de probabilites cumuleées à partir du df de résultats précédent
    df_stat = df_proba.copy()

    for j in range(0, n - 1):
        for i in range(0, n + 1):
            df_stat.iloc[i, j] = (np.sum(df_stat.iloc[i:, j]))

    # Export des tableaux de résultats dans un fichier Excel
    writer = pd.ExcelWriter('/Users/mattiou/Desktop/Perudo_res.xlsx')
    df_proba.to_excel(writer, sheet_name='Sheet1')
    df_stat.to_excel(writer, sheet_name='Sheet2')
    writer.save()

    # Analyse des distributions de probabilité et export des figures
    sns.set()
    df_proba['n = 30'].plot(legend=True)
    df_proba['n = 25'].plot(legend=True)
    df_proba['n = 20'].plot(legend=True)
    df_proba['n = 15'].plot(legend=True)
    df_proba['n = 10'].plot(legend=True)
    df_proba['n = 5'].plot(legend=True)
    plt.ylabel('Probability')
    plt.title('Probability distribution to get x dice among n')
    plt.savefig('/Users/mattiou/Desktop/df_proba_multi.pdf')
    plt.show()

#---Call main()-----------------------------------------------------------------------------------------------------#
main()
