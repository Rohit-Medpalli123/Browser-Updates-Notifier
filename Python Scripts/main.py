#Import ConfigParser(to allow us to save and retrieve code related data)
from ConfigParser import SafeConfigParser

from SiteOperations import SiteData
from EmailNotification import EmailOperation
import os

if __name__ == '__main__':

    # By using the parser we can access(read/modify) the configuration file
    parser = SafeConfigParser()

    #Navigate to project root directory
    os.chdir('..')
    parser.read('Browser_update_Bot_Config.ini')

    # This is the url which maintains the browser versions data and we need to scrape this information
    page_link = parser.get('required_code_data', 'page_url')
    print(page_link)

    # Instantiate the Site_Data object
    req_site_data = SiteData(page_link, parser)

    gen_divss = req_site_data.fetch_data_from_site()

    site_browser_data = req_site_data.process_divs(gen_divss)
    print(site_browser_data)

    differences_result = req_site_data.compare_data(site_browser_data)

    print(differences_result)

    #keep log of version updates for future use
    req_site_data.diff_result_log(differences_result)

    # Instantiate the Site_Data object
    send_email = EmailOperation(differences_result, parser)

    if (len(differences_result)) != 0:

        req_site_data.update_stored_browser_data(str(site_browser_data))

        blank_gen_rows = send_email.row_generator()

        rows_with_data = send_email.fill_data_into_rows(blank_gen_rows)

        diff_html_template_path = os.path.join(os.getcwd(),".\\Templates\\Diff_html_template.txt")
        html_template = send_email.gen_html_template(rows_with_data, diff_html_template_path)

        Subject, receiver, sender = send_email.diff_email_details()

        send_email.send_email_to_team(Subject, html_template, receiver,sender)
        #send_email.ses_email_to_team(Subject, html_template, multiple_recipients)

    else:
        no_diff_html_template_path = os.path.join(os.getcwd(),".\\Templates\\No_diff_html template.txt")
        html_template = send_email.gen_No_diff_html_template(no_diff_html_template_path)
        Subject, receiver, sender = send_email.no_diff_email_details()

        send_email.send_email_to_team(Subject, html_template, receiver,sender)
        #send_email.ses_email_to_team(Subject, html_template, Single_reciever)