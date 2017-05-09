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
# RobinhoodInstance Class                                                       #
# ----------------------------------------------------------------------------- #

class RobinhoodInstance:
    def __init__(self):
        self.logged_in = False
        self.login_token = ""

    # ------------------------------------------------------------------------- #
    # Login/Authentication Functions                                            #
    # ------------------------------------------------------------------------- #

    # Note: Yes, I get that it's pretty bad to store passwords in plain text.  For now,
    # I'd like to be able to login automatically without having to type my password in
    # every time.  I'll try to figure out a non-lazy solution later.
    def login(self, username, password):
        """
        Attempt to log into the Robinhood account referenced by the input
        arguments, username and password.

        Returns True if the login was successful and False otherwise.

        Logging in successfully also stores the login token in the RobinhoodInstance
        class.  A flag is also set which indicates that the api is ready to receive
        and respond to commands using the retrieved token.
        """

        out = check_output('curl -v https://api.robinhood.com/api-token-auth/ \
            -H "Accept: application/json" \
            -d "username=%s&password=%s" ' % (username, password), shell=True)

        token = json.loads(out)
        if "token" in token.keys():
            print_logger.info("[INFO]: Login for username: %s SUCCEEDED!" % username)

            self.logged_in = True
            self.login_token = token['token']

            return True
        else:
            print_logger.error("[ERROR]: Login for username: %s FAILED!" % username)

            return False

    def logout(self):
        """
        Attempt to log out of the previously logged in robinhood account.  If you haven't
        logged in before, don't do anything.

        Returns True if the logout was successfull and False otherwise for any reason.
        """

        if self.logged_in is False or self.login_token == "":
            print_logger.warning("[WARNING]: Cannot logout if you haven't logged in first!")

            return False

        out = check_output('curl -v https://api.robinhood.com/api-token-logout/ \
                -H "Accept: application/json" \
                -H "Authorization: Token %s" \
                -d ""' % self.login_token, shell=True)

        # We're now logged out.
        self.logged_in = False
        self.login_token = ""

    def reset_password(self, new_password):
        pass


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



if __name__ == "__main__":

    A = RobinhoodInstance()

    A.get_all_instruments()

    import code; code.interact(local=locals())
