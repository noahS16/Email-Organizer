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
* ### Dependencies:
    * Using pip or pip3. In your terminal, enter the following to install:
      * **PyQt5-tools:** `pip install pyqt5-tools`
      * **PyMongo:** ```pip install pymongo```
      * **Google API:** ```pip install --upgrade google-api-python-client google-auth-httplib2 google-auth-oauthlib```
      * **BeautifulSoup:** ```pip install beautifulsoup4```
      * **MongoDB:** Must be installed and started on your machine. See [install mongodb](https://www.mongodb.com/docs/manual/administration/install-community/).
* ### Run:
    * Once all dependencies have been installed, you may download the source code or clone this repository.
    * In the command line, navigate to the directory of the program, and run ```python3 main.py``` from the command line.
---
## To Use
* ### Add an Account:
  * Click the add account button located in the top left corner to add your first gmail account.
  * Once prompted, enter only your Gmail USERNAME in the field provided.
  * Proceed to log in to your Gmail account in your browser.
    * If a warning is displayed, select the 'advanced' option on the left, then 'go to cleanup'.
  * Accounts may be deleted by right-clicking on the account you wish to delete.
  * Double-clicking on a message will open the message in your browser.

---
