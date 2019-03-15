#Import os module (to read the email password stored as environment variable)
import os

#Import smtplib (to allow us to send email)
import smtplib

#Import email(to allow us to process email parameters)
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText

#Boto is the Amazon Web Services (AWS) SDK for Python
#Boto is used for sending email via amazon ses service
import boto3
from botocore.exceptions import ClientError

#Import string template module (to allow us to generate email template)
from string import Template

class EmailOperation:
    """ This class performs the operation of sending email if there is a difference in the browser versions """
    # Initializer / Instance Attributes
    def __init__(self, differences_result, parser):
        self.differences_result = differences_result
        self.parser = parser

    def row_generator(self):
        """This function generates n number of blank rows depending on the difference in stored and fetched data"""
        self.row_template = """<tr>
                                    <td>{}</td>
                                    <td>{}</td>
                                    <td>{}</td>
                              </tr>"""
        self.blank_rows = self.row_template * (len(self.differences_result) / 3)
        return self.blank_rows

    def fill_data_into_rows(self, blank_gen_rows):
        """This function adds the formatted data into the rows"""
        self.blank_gen_rows = blank_gen_rows
        for x in zip(*[iter(self.differences_result)] * len(self.differences_result)):
            self.data_into_rows = self.blank_gen_rows.format(*x)
        return self.data_into_rows

    def gen_html_template(self, rows_with_data, html_filename):
        """This function generates the entire html with row data for email """
        self.rows_with_data = rows_with_data
        self.html_filename = html_filename

        with open(self.html_filename, 'r') as template_file:
            template_file_content = template_file.read()
        self.t = Template(template_file_content)
        self.html_template = self.t.substitute(rows_with_data=self.rows_with_data)
        return self.html_template

    def gen_No_diff_html_template(self, No_diff_html_filename):
        """This function generates the entire html for the email if there is no difference"""
        self.No_diff_html_filename = No_diff_html_filename

        with open(self.No_diff_html_filename, 'r') as template_file:
            self.template_file_content = template_file.read()
        return self.template_file_content

    def diff_email_details(self):
        """This function provides the details required for an email"""
        Subject = self.parser.get('email_data_setup', 'Available_updates_subject')
        receiver = self.parser.get('email_data_setup', 'multiple_recipients')
        sender = self.parser.get('email_data_setup', 'sender')
        return Subject, receiver, sender

    def no_diff_email_details(self):
        """This function provides the details required for an email"""
        Subject = self.parser.get('email_data_setup', 'No_updates_subject')
        receiver = self.parser.get('email_data_setup', 'single_receiver')
        sender = self.parser.get('email_data_setup', 'sender')
        return Subject, receiver, sender

    def send_email_to_team(self, Subject, html_template, receiver,sender):
        """This function sends a email notification to team using email module """
        self.Subject = Subject
        self.html_template = html_template
        # set the 'from' address,
        self.sender = sender
        # set receiver's address
        self.receiver = receiver

        # Create message container - the correct MIME type is multipart/alternative.
        self.msg = MIMEMultipart('alternative')
        self.msg['Subject'] = self.Subject
        self.msg['From'] = self.sender

        #set 'To' parameter for multiple receivers
        if type(self.receiver) is list:
            self.msg['To'] = ', '.join(self.receiver)

        #set 'To' parameter for single receiver
        else:
            self.msg['To'] = self.receiver

        self.part2 = MIMEText(self.html_template, 'html')

        # Attach parts into message container.The HTML message, is best and preferred.
        self.msg.attach(self.part2)

        try:
            # setup the email server,
            self.server = smtplib.SMTP('smtp.gmail.com', 587)
            self.server.starttls()

            #fetch email password stored as environment variable
            self.email_password = os.environ["BB"]

            # Login into Gmail with Sender credentials
            self.server.login(self.sender, self.email_password)

            # send the email
            # self.msg['To'] = ', '.join(self.multiple_recipients)
            self.server.sendmail(self.sender, self.receiver, self.msg.as_string())

            # disconnect from the server
            self.server.quit()
            print("***** Successfully sent email *****")

        except smtplib.SMTPException:
            print("***** Error: unable to send email *****")

    def ses_email_to_team(self, Subject, html_template, receiver):
        """This function sends a email notification to team using boto module """
        self.SENDER = self.parser.get('email_data_setup', 'sender')

        self.RECIPIENT = receiver

        # If necessary, replace us-west-2 with the AWS Region you're using for Amazon SES.
        self.AWS_REGION = "us-east-1"

        # The subject line for the email.
        self.SUBJECT = Subject

        # The HTML body of the email.
        self.BODY_HTML = html_template

        # The character encoding for the email.
        self.CHARSET = "UTF-8"

        # Create a new SES resource and specify a region.
        self.client = boto3.client('ses', region_name=self.AWS_REGION)

        # Try to send the email.
        try:
            # Provide the contents of the email.
            self.response = self.client.send_email(
                Destination={
                    'ToAddresses': [
                        self.RECIPIENT,
                    ],
                },
                Message={
                    'Body': {
                        'Html': {
                            'Charset': self.CHARSET,
                            'Data': self.BODY_HTML,
                        },

                    },
                    'Subject': {
                        'Charset': self.CHARSET,
                        'Data': self.SUBJECT,
                    },
                },
                Source=self.SENDER,
            )
        # Display an error if something goes wrong.
        except ClientError as e:
            print(e.response['Error']['Message'])
        else:
            print("Email sent! Message ID:"),
            print(self.response['MessageId'])




