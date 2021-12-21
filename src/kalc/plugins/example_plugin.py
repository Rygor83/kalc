from yapsy.IPlugin import IPlugin   # obligatory import of IPlugin

class PluginOne(IPlugin):           # define class that will contain functions (methods)
    """ Custom defined plugin with constants and functions """
    
    # Constants
    root2 = 1.41421356237309504880168872420969808  # Pythagoras' constant. The square root of 2, often known as root 2, radical 2, or Pythagoras' constant

	# Functions
    def percent(self, percent, base_amount, days_in_month: int = 30, days_in_year: int = 360):
        """
        Calculate percnet amount with the following parameters

        :param percent: Rate of interest, 12
        :param base_amount: Principal amount
        :param days_in_month: Days in period
        :param days_in_year: Days in year
        :return: Maturity amount
        """
        return base_amount * percent * days_in_month / days_in_year / 100
