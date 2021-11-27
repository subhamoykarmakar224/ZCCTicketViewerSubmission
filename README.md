# Zendesk Intern Coding Challenge (2021) - Ticket Viewer
##Content
- Introduction
- Setup & Installation
- Documentation
- APIs
- References

## Introduction {#id-intro}
This project is the

## Setup & Installation
After cloning the project, please go through the following steps to get the project up and running.
### Step 1
In this step one needs to generate the oauth client and the secret key so that they can have secure access to APIs. 
- One need to login to ones zendesk account. 
- Create an OAuth client 
  - In Admin Center, click the Apps and integrations icon in the sidebar, 
  - then select APIs > Zendesk API > OAuth Clients. Complete the form.
- When finished the user will get the following information:
  - Client Id
  - Secret key
- Then create a ***.env*** file inside the root directory of the project and add the following values in the file, 
filling up all the required values without the angle brackets(*<>*). It will look something like this:    
```
DOMAIN=<your_domain_name>
CLIENT_ID=<client_id>
CLIENT_SECRET=<secret_key>
```
**Note**: All values inside the ***.env*** file are case-sensitive.

### Step 2
Install the python dependencies :
```
pip3 install -r <project_root_directory>/requirements.txt
```
Done. You are all set!

### Step 3
One needs to go to the root directory of the project and run the following script using your favorite terminal:
```
python3 ZCCApp.py
```

The app will then be deployed at `http:localhost:3001`. Paste this link to your browser to start using the application.

## Documentation
The project structure is as follows:
- Root-Directory
  - static
    - css
    - js
  - tmp
  - views
  
The static folder contains the `css` and `js` files. Since using a database was out of scope of this project, `tmp` 
folder is being used to store files which are doing some work of database. The `view` folder contains the templates
that are being used in the project to generate the web views.

In addition to the `ZCCApp.py` file, there are 3 important files `Constant.py` and `Helper.py`. `Constant.py` contains the 
constants that are being used all throughout the project. `Helper.py` contains some helper functions that are being used 
by the app.

The login is being done using oAuth and the application gets an access token which is then stored in a cookie 
with a lifespan of *session*. So for testing purpose it is suggested to use the incognito mode of a web browser.

When logged in the 25 (As defined in the `Constants.py` file) tickets are shown per page. Where clicking next or previous 
page will result in the next 25 or previous 25 tickets respectively. As suggested in the documentations, all tickets 
are not fetched at once but 25 tickets at a time and the next page url and the previous page url are read from the json
result.

The file `test_ZCApp.py` is one which has all the uni-test cases. To run the unit test case file use the following script:
```
python3 test_ZCApp.py
```

## APIs
The following are the apis used to make this project:
- https://<domain_name>.zendesk.com/api/v2/tickets.json?page[size]=25
- https://<domain_name>.zendesk.com/oauth/tokens
- https://<domain_name>.zendesk.com/api/v2/tickets/count.json
- https://<domain_name>.zendesk.com/api/v2/users/me.json
- https://<domain_name>.zendesk.com/oauth/authorizations/new

## References
- [Zendesk Developer Documentation](https://developer.zendesk.com/documentation/)
- [Zendesk Api Reference](https://developer.zendesk.com/api-reference/)
- [OAuth to Authenticate Zendesk API request](https://developer.zendesk.com/documentation/ticketing/working-with-oauth/using-oauth-to-authenticate-zendesk-api-requests-in-a-web-app/)
- [Bottle: Python Web Framework](https://bottlepy.org/docs/dev/)
- [Jinja](https://jinja.palletsprojects.com/en/3.0.x/)