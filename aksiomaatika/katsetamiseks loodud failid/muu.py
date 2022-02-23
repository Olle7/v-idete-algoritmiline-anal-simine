
from math import sqrt


def standard_deviation(lst, population):
    """Calculates the standard deviation for a list of numbers."""
    num_items = len(lst)
    mean = sum(lst) / num_items
    differences = [x - mean for x in lst]
    sq_differences = [d ** 2 for d in differences]
    ssd = sum(sq_differences)

    # Note: it would be better to return a value and then print it outside
    # the function, but this is just a quick way to print out the values along
    # the way.
    if population is 0:
        print("mingi imelik variant")
        variance=ssd/num_items/(num_items-1)
    elif population is 1:
        print('This is POPULATION standard deviation.')
        variance = ssd / num_items
    elif population is 2:
        print('This is SAMPLE standard deviation.')
        variance = ssd / (num_items - 1)
    sd=sqrt(variance)
    # You could `return sd` here.

    print('The mean of {} is {}.'.format(lst, mean))
    print('The differences are {}.'.format(differences))
    print('The sum of squared differences is {}.'.format(ssd))
    print('The variance is {}.'.format(variance))
    print('The standard deviation is {}.'.format(sd))
    print('--------------------------')


s = [0.1825, 0.097, 0.177, 0.118, 0.2775, 0.1385, 0.1705, 0.1535, 0.1725, 0.106]
standard_deviation(s,0)
