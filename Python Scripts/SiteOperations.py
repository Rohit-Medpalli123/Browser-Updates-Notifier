import logging

# Import BeautifulSoup (to parse what we download)
import bs4 as bs

# Import requests (to download the page)
import requests

import os


class SiteData:
    """ This class performs all operations related to the remote website like downloads the page,processes it,compares the data,
    provides the differences"""

    # Initializer / Instance Attributes
    def __init__(self, page_url, parser):
        self.page_link = page_url
        self.parser = parser
        self.stored_file_path = os.path.join(os.getcwd(),".\\Logs\\Stored_Browser_Data.txt")
        self.log_file_path = os.path.join(os.getcwd(),".\\Logs\\Versions_update.log")

        try:
            # Here data is stored for comparision with the fetched site data
            with open(self.stored_file_path, "r") as Stored_data_file:
                self.stored_browser_data = eval(Stored_data_file.read())

        except FileNotFoundError:
            print("File not Found.... Please check file in the directory")

        self.list_of_browsers = eval(self.parser.get('required_code_data', 'list_of_browsers'))

    def fetch_data_from_site(self):
        """This function fetches the content from the url using the requests library and returns the outer container div"""

        self.page_response = requests.get(self.page_link, timeout=10)

        # We have used the html parser to parse the url content and store it in a variable.

        self.page_content = bs.BeautifulSoup(self.page_response.content, "html.parser")

        self.mydivs = self.page_content.find('div', attrs={'class': 'support-container view-mode-normal'}).find_all( 'div')

        return self.mydivs

    def process_divs(self, gen_divs):
        """ This function processes the outer container and extracts(returns) the required data(browser name,browser latest version)
        for only required browsers"""

        self.gen_divs = gen_divs

        # To store data fetched from site
        self.data_from_site = {}

        self.ignored_browsers = eval(self.parser.get('required_code_data', 'ignored_browsers'))

        for self.i in self.gen_divs:
            self.browser_name = self.i.find('h4').text
            if self.browser_name in self.ignored_browsers:
                continue
            self.browser_ver1 = self.i.find('li', {"class": ["stat-cell y current ", "stat-cell a #1 current ", "stat-cell n current "]})
            self.browser_ver2 = self.browser_ver1.find('b', attrs={'class': 'stat-cell__label'}).text
            self.browser_current_version = self.browser_ver2[:-2]
            self.data_from_site[self.browser_name] = self.browser_current_version
        return self.data_from_site

    def compare_data(self, site_browser_data):
        """This fuctions takes two operands (site_browser_data,stored_browser_data) compares them and returns the difference
        between them"""

        self.site_browser_data = site_browser_data

        self.result = []
        for i in range(len(self.list_of_browsers)):
            if self.site_browser_data[self.list_of_browsers[i]] != self.stored_browser_data[self.list_of_browsers[i]]:
                self.result.extend((self.list_of_browsers[i], self.site_browser_data[self.list_of_browsers[i]],
                                    self.stored_browser_data[self.list_of_browsers[i]]))
        return self.result

    def update_stored_browser_data(self, updata_data):
        """This function updates the stored data with the newly fetched values """

        try:
            with open(self.stored_file_path, "w") as updatefile:
                updatefile.write(updata_data)
            print("***** Updated the Stored data with new values successfully *****")

        except FileNotFoundError:
            print("***** File not Found.... Please check file in the directory *****")

    def diff_result_log(self,res):
        """This function logs the Version update data into a file"""
        try:
            logging.basicConfig(filename=self.log_file_path, level=logging.DEBUG, format='%(asctime)s %(message)s',
                            datefmt='%m/%d/%Y %I:%M:%S %p')
            logging.info(res)
            print("***** Completed Logging successfully *****")

        except FileNotFoundError:
            print("***** File not Found.... Please check file in the directory *****")