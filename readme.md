# Simplified Gmail Viewer/Organizer #

This is a **Desktop App** made using python and the Gmail API to make organizing and/or cleaning out
your inboxes not only easier, but faster as well. This app is especially useful to users with thousands of emails, 
as you can now delete sender specific emails AND unsubscribe from those senders in a single click.
---
## Functionality
* Main functionality of the program includes:
    * View your emails by sender, like a common text or instant messaging layout.
    * Delete OR Trash all messages that are form the sender you select with a single click. 
    * View messages individually, so you can be more specific in which ones you would like to get rid of. 
    * Unsubscribe - will open an unsubscribe link from the sender you choose in your browser.
---
## To Install
* ### First Things First:
  * Clone this repository in your desired location
  * In order for you to be able to sign in to you Gmail account, you will need to create an **OAuth 2.0 client ID**.
  Follow [this link](https://developers.google.com/workspace/guides/create-credentials#desktop-app) to the **Google Cloud Console** to create your ID.
    * Click **Go to Credentials** under the **Oauth client ID credentials** section, and
    follow the steps provided in that same section to create your ID.
    * On the window that appears after you create your ID, click on **DOWNLOAD JSON** on the bottom.
    * Once the file is downloaded, rename it to **credentials.json**. If not renamed, the app will not run.
    * Place the renamed file in the ***creds*** folder located in the project files on your machine.
    * Back in the Google Cloud Console in the menu on the left, click ***OAuth consent screen***
    * Scroll down, and in the **Test users** section, click ***Add users***
    * Enter the emails you will be using in the app to the test users list.
* ### Dependencies:
    * **ARM architectures such as the Apple M1 chip are not supported.**
    * The following libraries will be needed to run this app:
      * [PyQt5-tools](https://pypi.org/project/pyqt5-tools/)
      * [PyMongo](https://pypi.org/project/pymongo/)
      * [Google API](https://developers.google.com/gmail/api/reference/rest)
      * **MongoDB:** Must be installed and started on your machine. See [install mongodb](https://www.mongodb.com/docs/manual/administration/install-community/).
    * From the command line, run ```pip3 install --upgrade -r requirements.txt``` in the same directory as the repository to install all required libraries.
      Use ```pip install --upgrade -r requirements.txt``` if the above command fails.
* ### Run:
    * In the command line, navigate to the directory of the repository (if not already), and run ```python3 main.py``` from the command line.
---
## To Use
* ### Add an Account:
  * Click the add account button located in the top left corner to add your first gmail account.
  * Once prompted, enter **only your Gmail USERNAME** in the field provided. The app will then begin fetching
  all the emails from your inbox. This may take a while, depending on how many emails you have.
  * Proceed to log in to your Gmail account in your browser.
  * Accounts may be deleted by right-clicking on the account you wish to delete.
  * Double-clicking on a message will open the message in your browser.
* ### Troubleshooting:
  * If a warning is displayed upon login, select the 'advanced' option on the left, then 'go to (***your OAuth ID name***)'.
  * If the app quits, make sure the **Gmail API** is enabled in your [Google Cloud Console](https://console.cloud.google.com/apis/dashboard)
    * Also make sure your OAuth 2.0 ID is stored correctly and with the correct name as mentioned above.

---
## License
This project is licensed under the MIT License.

---
