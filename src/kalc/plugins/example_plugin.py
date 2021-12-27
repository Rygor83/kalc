from yapsy.IPlugin import IPlugin  # obligatory import of IPlugin


class Example_plugin(IPlugin):  # define class that will contain functions (methods)
    """ Custom defined plugin with constants and functions """

    # Constants
    root2 = 1.41421356237309504880168872420969808  # Pythagoras' constant. The square root of 2, often known as root 2, radical 2, or Pythagoras' constant

    # Functions
    def sinterest(self, percent, base_amount, days_in_month: int = 30, days_in_year: int = 360):
        """
        Simple interest is a method to calculate the amount of interest charged on a principal amount at a given rate of interest and for a given period of time

        :param percent: Rate of interest, for example 12
        :param base_amount: Principal amount, for example 1000000
        :param days_in_month: Days in given period of time, for example: 1 month = 30 days
        :param days_in_year: Days in year, for example, 360/365/366
        :return: Maturity amount

        https://www.cuemath.com/commercial-math/simple-interest/
        """
        return base_amount * percent * days_in_month / days_in_year / 100

    def compound_interest(self):
        """
        https://www.thecalculatorsite.com/articles/finance/compound-interest-formula.php
        """
        pass
