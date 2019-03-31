# Browser Update Notifier [![Python 2.7](https://img.shields.io/badge/python-2.7-blue.svg)](https://www.python.org/downloads/release/python-360/)

This is a notifier utility written in python 2.7 . Here this script visits a website (https://caniuse.com/usage-table) which maintains the browser update versions history (both Desktop and mobile browsers) and notifies the QA team about the updates.

#### Motivation:
So the basic idea behind this project is to keep track of the latest browser updates so that this will be helpful for the Compatibility testing.

#### Built With:
- [Python 2.7](https://www.python.org/download/releases/2.7/)
- [Beautiful Soup](https://www.crummy.com/software/BeautifulSoup/bs4/doc/) - Python package for parsing HTML and XML documents
- [Requests](http://docs.python-requests.org/en/master/) - allows you to send organic, grass-fed HTTP/1.1 requests
- [email](https://docs.python.org/2/library/email.html#module-email) - library for sending email messages
- [boto3](https://boto3.amazonaws.com/v1/documentation/api/latest/index.html) - Boto is the Amazon Web Services (AWS) SDK for Python.Here Boto3 is used for sending email via amazon ses service.

#### Steps performed by the script are as follows:

1. Visits [can i use website](https://caniuse.com/usage-table) and pulls the required data depending upon the configuration mentioned in the config file.
2. Compares the fetched data with the stored previous versions data.
3. Generates the HTML template which has the table with the required number of rows according to the differences in the compared data.
4. Send EMAIL if there is the latest update available for a particular browser. 

   ![Sample email template for available updates ](/Images/Updates__.png "History")  
5. If no update is available then send the email to the person who is maintaining the project.

   ![email template for no available updates ](/Images/noupdates__.JPG "History1")

6. Update the stored data and keep log of version updates.


## Getting Started:

#### Prerequisites:
1. Python 2.7.x
2. This project already has pipfile so go ahead and install all the dependencies from it . Use the below command:Install from Pipfile, if there is one: Please refer to [link](https://pipenv.readthedocs.io/en/latest/basics/#example-pipenv-workflow).

```bash
pipenv install
```
#### Customizations:

###### Config File: **_Please  add the below configurations in Browser_update_Bot_Config.ini file_**
1. Mention the browsers which you don't want to fetch from the site:

    * Edit: ignored_browsers
2. Add the sender:
     
    * Edit: sender 
3. Add single receiver:
     
    * Edit: receiver
4. Add multiple receivers:
     
    * Edit: multiple_recipients

5. Add subject for single reciver:
     
    * Edit: No__updates_subject

6. Add subject for multiple recivers:
     
    * Edit: Available__updates_subject

##### Note: 
_we have two options for the sending the email_
1. Email module
2. Boto3 

 
#### How to run the script:
Here we have two options for setup.
1. Set up a _cron job_ daily (**_recommended_**)
2. Run the script manually when it's needed


## Credits:
Visit [Browser versions History table](https://caniuse.com/usage-table) for more information.











 



