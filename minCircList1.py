"""
This program finds the smallest number in a constantly increasing circular list.
Requirement: Make your program as readable as possible.

Author:  Nse Ekpoudom
Created:  July 11, 2018
"""

# Get the list.  Assumes keyboard entry of a single circular list
# and converting the string input to a list of integers
lst = list(map(int, input('Please enter a circular list that is constantly increasing\n \
(separate numbers with a comma): ').split(',')))

# Output the smallest number in the list
print("The smallest number in the list is: %s" % min(lst))


