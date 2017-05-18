#!/usr/bin/env python

# ----------------------------------------------------------------------------- #
# Developer: Andrew Kirfman                                                     #
# Project: PythonRobinhood Trading Functions                                    #
#                                                                               #
# File: ./robinhood.py                                                          #
# ----------------------------------------------------------------------------- #

# ----------------------------------------------------------------------------- #
# Imports                                                                       #
# ----------------------------------------------------------------------------- #

from subprocess import check_output
import json
import logging
import sys
import os
import requests
import getpass

# ----------------------------------------------------------------------------- #
# Logging Utility                                                               #
# ----------------------------------------------------------------------------- #

# Nice print statements are fun.  Setup a logger to do this
print_logger = logging.getLogger(__name__)

# TODO: This should be specifiable through an argparse option.  Right now, just set
# the logging utility to the highest verbosity level
print_logger.setLevel(logging.DEBUG)

# Add a handler to tell the system where to send messages.  This one sends
# everything to the console using standard out.
print_console_handler = logging.StreamHandler(sys.stdout)
print_logger.addHandler(print_console_handler)

# To print to a file as well, uncomment the following lines and add a path
# to your desired log file.
#    print_file_handler = logging.FileHandler('<path to file here!>')
#    print_logger.addHandler(print_file_handler)

# ----------------------------------------------------------------------------- #
# Defines                                                                       #
# ----------------------------------------------------------------------------- #

# URLs to the robinhood API
API_URLS = {
        'login'             : 'https://api.robinhood.com/api-token-auth/',
        'logout'            : 'https://api.robinhood.com/api-token-logout/',
        'reset-password'    : 'https://api.robinhood.com/password_reset/request/',

        'user-info'         : 'https://api.robinhood.com/user/',
        'basic-info'        : 'https://api.robinhood.com/user/basic_info/'


        }

# Paths to configuration files
CONFIGURATION_DIRECTORY_PATH = "./configuration"
LOGIN_CONFIGURATION_FILE = "%s/credentials.txt" % CONFIGURATION_DIRECTORY_PATH

# Account Information Parameters
GET_ALL = "all"
GET_USERNAME = "username"
GET_FIRST_NAME = "first_name"
GET_LAST_NAME = "last_name"
GET_ID_INFO = "id_info"
GET_URL = "url"
GET_BASIC_INFO = "basic_info"
GET_EMAIL = "email"
GET_INVESTMENT_PROFILE = "investment_profile"
GET_ID = "id"
GET_INTERNATIONAL_INFO = "international_info"
GET_EMPLOYMENT = "employment"
GET_ADDITIONAL_INFO = "additional_info"

# User Basic Info
GET_ADDRESS = "address"
GET_CITIZENSHIP = "citizenship"
GET_CITY = "city"
GET_COUNTRY_OF_RESIDENCE = "country_of_residence"
GET_DATE_OF_BIRTH = "date_of_birth"
GET_MARITAL_STATUS = "marital_status"
GET_NUMBER_OF_DEPENDANTS = "number_dependents"
GET_PHONE_NUMBER = "phone_number"
GET_STATE = "state"
GET_TAX_ID_SSN = "tax_id_ssn"
GET_UPDATED_AT = "updated_at"
GET_ZIPCODE = "zipcode"

# ----------------------------------------------------------------------------- #
# Build Directory Structure
# ----------------------------------------------------------------------------- #

# Users have the option of using a configuration file to store their username
# and password.  Create that directory now.




#try:
#    os.exists(CONFIGURATION_DIRECTORY_PATH)



# ----------------------------------------------------------------------------- #
# Exception Handling                                                            #
# ----------------------------------------------------------------------------- #

class NotLoggedIn(Exception):
    pass

class BadArgument(Exception):

# ----------------------------------------------------------------------------- #
# RobinhoodInstance Class                                                       #
# ----------------------------------------------------------------------------- #

class RobinhoodInstance:
    def __init__(self):
        self.logged_in = False
        self.login_token = ""

        self.username = None
        self.password = None

        self.login_session = None


    # ------------------------------------------------------------------------- #
    # Login/Authentication Functions                                            #
    # ------------------------------------------------------------------------- #

    def is_logged_in(self):
        return not (self.login_session is None or self.login_token is None)

    def login(self):
        """
        Attempt to log into the Robinhood account referenced by the input
        arguments, username and password.

        Returns True if the login was successful and False otherwise.

        Logging in successfully also stores the login token in the RobinhoodInstance
        class.  A flag is also set which indicates that the api is ready to receive
        and respond to commands using the retrieved token.
        """

        # See if the user has defined a file with their username and password.
        # If not, prompt them on the command line for it.
        data_dict = {}

        try:
            credential_file = open(LOGIN_CONFIGURATION_FILE, "r")

            username = credential_file.readline()
            password = credential_file.readline()

            data_dict = {
                    'username' : username,
                    'password' : password
                    }
        except IOError:
            data_dict = self.get_login_credentials()

        # Create a login session that will persist through through the entire
        # runtime of the program
        self.login_session = requests.session()

        response = self.login_session.post(API_URLS['login'], data_dict)
        response = response.json()

        # Check and see if we need to do multifactor authentication
        if 'mfa_type' in response.keys() and 'mfa_required' in response.keys():
            if response['mfa_required'] is True:
                mfa_code = raw_input("Input Multifactor Identification Key: ")

                data_dict.update({'mfa_code' : mfa_code})
                response = self.login_session.post(API_URLS['login'], data_dict)
                response = response.json()

        if 'token' not in response.keys():
            print_logger.error("[ERROR]: Login Failed!")
            self.login_session = None
        else:
            self.login_token = response['token']


    def get_login_credentials(self):
        """
        Used to acquire the login credentials from the command line.
        """

        username = raw_input("Input Username: ")
        password = getpass.getpass("Input Password: ")

        data_dict = {
                'username' : username,
                'password' : password
                }

        return data_dict




    def logout(self):
        """
        Attempt to log out of the previously logged in robinhood account.  If you haven't
        logged in before, don't do anything.

        Returns True if the logout was successfull and False otherwise for any reason.
        """

        if self.login_session is None or self.login_token is None:
            print_logger.warning("[WARNING]: Cannot logout without logging in first!")

        self.login_session.post(API_URLS['logout'])

        self.login_session = None
        self.login_token = None


    def reset_password(self, new_password = ""):
        """
        Submit a request to reset a user's password.

        The robinhood API appears to then send an email to the account associated with the
        provided email address.  I can grab the email address from the user's account, but
        I cannot log into the email account and read the recovery email.  (I mean, I could,
        but that would be beyond the scope of what this function should be able to do)
        """

        if not self.is_logged_in():
            raise NotLoggedIn()

        account_email_address = self.get_email()



    # ------------------------------------------------------------------------- #
    # Get Fundamentals                                                          #
    # ------------------------------------------------------------------------- #

    def get_fundamentals_singleton(self, ticker_symbol):
        pass

    def get_fundamentals_multiple(self, list_of_tickers):
        pass

    # ------------------------------------------------------------------------- #
    # Buy Orders                                                                #
    # ------------------------------------------------------------------------- #

    def buy_order(self, ticker_symbol, order_type, time_in_force, quantity, price = "0.01", trigger = "immediate"):
        """
        Main function for issuing buy orders.

        Note: Price is only truly required for limit orders, but I get a nasty
        message back from the API if I don't include it on market orders.  Therefore,
        the default value of $0.01 is used unless specified otherwise.
        """

        # If you aren't logged in, then don't do anything.
        if self.logged_in is False or self.login_token == "":
            print_logger.error("[ERROR]: Cannot issue buy order without being logged in.")
            return False

        # Get relevant data to submit the order
        instrument_id = RobinhoodInstance.get_instrument_id(ticker_symbol)
        account_number = self.get_account_number()

        out = check_output('curl -v https://api.robinhood.com/orders/ \
                -H "Accept: application/json" \
                -H "Authorization: Token %s" \
                -d account=https://api.robinhood.com/accounts/%s/ \
                -d instrument=https://api.robinhood.com/instruments/%s/ \
                -d symbol=%s \
                -d type=%s \
                -d time_in_force=%s \
                -d price=%s \
                -d trigger=%s \
                -d quantity=%s \
                -d side=buy' % (self.login_token, account_number, instrument_id,\
                ticker_symbol, order_type, time_in_force, price, trigger, quantity),\
                shell=True)

        buy_order_response = json.loads(out)

        # If something went wrong with the buy order, then the response will be extremely short.
        if len(buy_order_response) < 3:
            # Try to print out the error response code.  If you can't, that's ok.
            try:
                print_logger.error("[ERROR]: Buy order failed: %s" % buy_order_response["detail"])
            except NameError:
                print_logger.error("[ERROR]: Buy order failed.")

            return False
        else:
            return buy_order_response

    # ------------------------------------------------------------------------- #
    # Sell Orders                                                               #
    # ------------------------------------------------------------------------- #

    def sell_order(self, ticker_symbol, order_type, time_in_force, quantity, price = "0.01", trigger = "immediate"):
        """
        Main function for issuing buy orders.

        Note: Price is only truly required for limit orders, but I get a nasty
        message back from the API if I don't include it on market orders.  Therefore,
        the default value of $0.01 is used unless specified otherwise.
        """

        # If you aren't logged in, then don't do anything.
        if self.logged_in is False or self.login_token == "":
            print_logger.error("[ERROR]: Cannot issue buy order without being logged in.")
            return False

        # Get relevant data to submit the order
        instrument_id = RobinhoodInstance.get_instrument_id(ticker_symbol)
        account_number = self.get_account_number()

        out = check_output('curl -v https://api.robinhood.com/orders/ \
                -H "Accept: application/json" \
                -H "Authorization: Token %s" \
                -d account=https://api.robinhood.com/accounts/%s/ \
                -d instrument=https://api.robinhood.com/instruments/%s/ \
                -d symbol=%s \
                -d type=%s \
                -d time_in_force=%s \
                -d price=%s \
                -d trigger=%s \
                -d quantity=%s \
                -d side=sell' % (self.login_token, account_number, instrument_id,\
                ticker_symbol, order_type, time_in_force, price, trigger, quantity),\
                shell=True)

        sell_order_response = json.loads(out)

        # If something went wrong with the buy order, then the response will be extremely short.
        if len(sell_order_response) < 3:
            # Try to print out the error response code.  If you can't, that's ok.
            try:
                print_logger.error("[ERROR]: Sell order failed: %s" % sell_order_response["detail"])

                import code; code.interact(local=locals())
            except NameError:
                print_logger.error("[ERROR]: Sell order failed.")

            import code; code.interact(local=locals())

            return False
        else:
            return sell_order_response

    # ------------------------------------------------------------------------- #
    # Instrument Helper Functions                                               #
    # ------------------------------------------------------------------------- #

    @staticmethod
    def get_all_instruments():
        """
        Return a JSON object containing every single publicly traded stock.
        """

        json_result = None
        out = check_output('curl -v https://api.robinhood.com/instruments/ \
                -H "Accept: application/json"', shell=True)

        next_object = json.loads(out)
        stocks_list = next_object["results"]

        while True:
            if "unicode" not in str(type(next_object["next"])):
                break

            out = check_output('curl -v %s\
                    -H "Accept: application/json"' % next_object["next"], shell=True)

            next_object = json.loads(out)
            stocks_list = stocks_list + next_object["results"]

        with open("stock_json.txt", "w") as outfile:
            json.dump(stocks_list, outfile)

        with open("stock_list.txt", "w") as outfile:
            for stock in stocks_list:
                outfile.write("%s\n" % stock["symbol"])


    @staticmethod
    def get_instrument_id(ticker_symbol):
        """
        Orders require the instrument ID for the chosen security from the robinhood API.

        Note: This function can be called without being logged in.  I made it a
        static method so that you can call it without having to declare an instance of
        this class.
        """

        out = check_output('curl -v https://api.robinhood.com/instruments/?symbol=%s \
                -H "Accept: application/json"' % ticker_symbol, shell=True)

        # Check to make sure that the keys that we need are in the output json.
        # I don't want any of these commands to throw exceptions because of bad data
        # and potentially kill the program.
        instrument_data = json.loads(out)

        if "results" in instrument_data.keys():
            if "id" in instrument_data["results"][0].keys():
                return instrument_data["results"][0]["id"]

        # If we get here, something bad happened.
        return False

    # ------------------------------------------------------------------------- #
    # Account Helper Functions                                                  #
    # ------------------------------------------------------------------------- #

    def get_account_number(self):
        """
        Robinhood uses a string to identify your account.  It seems like this data
        is necessary in order to issue a buy order.  Grab this id from your login
        token.
        """

        if self.logged_in is False or self.login_token == "":
            print_logger.error("[ERROR]: Cannot get acount number if you aren't logged in.")
            return False

        out = check_output('curl -v https://api.robinhood.com/accounts/ \
                -H "Accept: application/json" \
                -H "Authorization: Token %s"' % self.login_token, shell=True)

        # Based on the robinhood API github page, all accounts should share
        # this pattern.  If this proves to not be the case, I'll change it later
        account_data = json.loads(out)
        if "results" in account_data.keys():
            try:
                return account_data["results"][0]["account_number"]
            except NameError:
                print_logger.error("[ERROR]: Unexpected result from get_account_number().")
                return False

        return False

    # ------------------------------------------------------------------------- #
    # User Information Helper Functions                                         #
    # ------------------------------------------------------------------------- #

    def get_user_data(self, param):
        """
        Query the API for all data associated with the logged in user's account.

        Returns the json data associated with user account info.

        The following macros can be passed as param to retrieve.
          - GET_ALL: Returns the whole json dump containing all user data.
          - GET_FIRST_NAME: Returns the first name of the logged in user.
          - GET_LAST_NAME: Returns the last name of the logged in user.
          - GET_ID_INFO: TODO: FILL IN
          - GET_URL: TODO: FILL IN
          - GET_BASIC_INFO: TODO: FILL IN
          - GET_EMAIL: Returns the email address associated with the logged in user
          - GET_INVESTMENT_PROFILE: TODO: FILL IN
          - GET_ID: Returns the unique ID that Robinhood uses to identify this account
          - GET_INTERNATIONAL_INFO: TODO: FILL IN
          - GET_EMPLOYMENT: Link to employment info associated with the account
          - GET_ADDITIONAL_INFO: Returns a link to any additional information associated with the logged in user
        """

        if not self.is_logged_in():
            raise NotLoggedIn()

        # Making an API call here with post was rejected by the API server.  Curl
        # should work where post failed.
        response = check_output('curl -v %s \
                -H "Accept: application/json" \
                -H "Authorization: Token %s"' % (API_URLS['user-info'], self.login_token), shell=True)

        # The result returned by curl is a string.  Cast this to a json dict
        response = json.loads(response)

        if param == GET_ALL:
            return response
        elif param in response.keys():
            return response[param]
        else:
            raise BadArgument()

    def get_basic_user_info(self, param):
        """
        Query the api to gather all personal data associated with the logged in user.

        The following macros can be passed as param to retrieve.
          - GET_ALL: Returns the whole json dump containing all user data.
          - GET_ADDRESS: Returns the user's street address.
          - GET_CITY: Returns the user's city
          - GET_COUNTRY_OF_RESIDENCE: Returns the user's two letter country code.
          - GET_DATE_OF_BIRTH: Returns the user's date of birth.
          - GET_MARITAL_STATUS: Returns whether or not the user is married or single.
          - GET_NUMBER_DEPENDENTS: Returns the number of children that the user has.
          - GET_PHONE_NUMBER: Returns the user's phone number.
          - GET_STATE: Returns the user's resident state (as two character abbreviation).
          - GET_TAX_ID_SSN: Returns the last 4 digits of the user's social.
          - GET_UPDATED_AT: Returns the last date/time when this information was updated.
          - GET_ZIPCODE: Returns the user's zipcode.
        """

        if not self.is_logged_in():
            return NotLoggedIn()

        response = check_output('curl -v %s \
                -H "Accept: application/json" \
                -H "Authorization: Token %s"' % (API_URLS['basic-info'], self.login_token), shell=True)

        response = json.loads(response)

        if param == GET_ALL:
            return response
        elif param in response.keys():
            return response[param]
        elif:
            raise BadArgument()

    def get_affiliation_information(self, param):
        """
        Get user information associated with SEC Rule 405.

        TODO: This function.  This information isn't super useful, so I'm not going to do it now.
        """

        pass






if __name__ == "__main__":

    A = RobinhoodInstance()

    A.get_all_instruments()

    import code; code.interact(local=locals())
