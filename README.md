# IoTAssignment3
COSC2674/2755 Semester 1, 2020 Assignment 3 | Extended Car Share IoT Application

# Welcome to Car Share Application
The project is about the automatic Car Share System. This system is used to book, find and unlock and lock a car. In addition, the customer
can report some issues with the car to help the company to maintain the cars. The application is created for four types of users: customer, company manager, engineers and system administrator.

The implementation of this application involves the following components:
  - Python documentation tools such as Sphinx
  - Practice third party API
  - Unit testing in Python
  - Socket Programming
  - Writing your own API using Python’s microframework Flask
  - Login using QR Code
  - Pushbullet Notifications
  - search using voice recognition
  - Programming with Cloud databases
  - Selected Software Engineering Project Management/Tools

## High level architecture diagram
![alt text](https://github.com/rmit-s3804879-sainathreddy-kodiganti/IoTAssignment3/blob/feature/meet_p/src/MP/static/img/architecture.png)



### Pre-requisites
  * python 3 - [Installation guide](https://realpython.com/installing-python/)
  * Flask - [Installation guide](https://flask.palletsprojects.com/en/1.1.x/installation/)
  * git - [Installation guide](https://www.linode.com/docs/development/version-control/how-to-install-git-on-linux-mac-and-windows/) .  
  * Google Cloud SDK - [Download page](https://cloud.google.com/deployment-manager/docs/step-by-step-guide/installation-and-setup) .  
  * Sphinx - [Installation guide](https://docs.readthedocs.io/en/stable/intro/getting-started-with-sphinx.html)
  * Google Map Api - [Getting Started with Google Map](https://developers.google.com/maps/gmp-get-started)
  * Google Calendar - [Getting started with Google Calendar Api](https://developers.google.com/calendar/overview)
  * Pushbullet Account - [Creating account on pushbullet] https://www.pushbullet.com/
  * And Raspberry pi device version 3 or 4. 

# Getting Started
Make sure you have python version 3 installed. Create a google cloud account and configure a mysql database with tables: cars, bookings and users. Table car will have the list of cars available. User needs to register with the system before booking a car. So on registration, user account information will be saved in the "users" table. When user makes booking, the booking information related to the user will be stored in the "booking" table. Please refer to Models implemented in "flask_api.py" file to compose database in mysql.

check your public ip address of your network and add it to the list of authorized networks for the database created in google cloud. Else gcloud would refuse connection unless it is hosted in the App engine. 

Please make changes the the following section inside main.py in accordance to your db credentials:
  ```
  HOST = "<hostname>"
  USER = "<username>"
  PASSWORD = "<password>"
  DATABASE = "<db name>"
  ```

## Getting code
  Either clone this repository or fork it on GitHub and clone your fork:
  ```
  git clone https://github.com/rmit-s3804879-sainathreddy-kodiganti/IoTAssignment3.git
  cd IotAssignmemt
  ```

## Master Pi: Python Flask at Server Pi
### General overview
The customers can register, logging in, search and book a car on the web-based system in MASTER PI (MP). The user registration on MP is required for the first-time user. In the home page of the web-based application provides only two options:
  - registration
  - log in
  Upon registration the details are stored in cloud database(MySQL). Upon logging in, the user is now presented with another page including following functions:
  - show a list of cars available, you need to show the detailed information of cars in the list
  such as Make, Body Type, Colour, Seats, Location, Cost per hour.
  - search for a car based on body type or other features. user can also use voice search to search cars.
  - book a car based on car identity, the user will be asked to input booking details.
  - cancel a booking
  - logout

### Technical Overview
Our backend application server is a Python Flask. The application that relies upon some 3rd Party python packages. You need to install these local dependencies. But before that, feel free to create a virtual environment for the python flask application hosted in server. This is done to install dependencies particular to project without tampering pre installed packages which may have been referenced in other projects locally. 

#### Creating virtual environment using Python 3 :
  ```shell
  cd src/MP
  sudo apt install python3-venv
  pip3 install virtualenv

  python3 -m venv venv
  source venv/bin/activate
  ```
  - For Windows users
    ```
    PS C:\DEV\aProject\env\Scripts>.\activate

    or using git-bash
    source venv/Scripts/activate
    ```
After the creation of virtual environment, try running the project:
  ```
  python3 main.py
  ```
You will encounter the error about the packages not being installed. Check the packages and make sure you install it.
**Most Importantly** do not forget to install mysqldb-client or mariadb-client.
Install local dependencies (from the project root folder):
  ```
  pip3 install -r requirements.txt #installs all the dependencies for the project.
  
  sudo apt-get install mariadb-client-10.0
  ```

## Agent Pi :Python Application at client Pi
### General overview
The customers can login to unlock and return the car. , logging in the console requeries user to havve a valid booking and once valiadated can login by either of:
  - password based login
    The user can input the password and verify thier idenity. The passwords are hased and salted for security reasons
  - QR Code based login
    The user can validate the account by scafacing the ip cam and providing the facial data to the ML model to login the user into the         system.
### Sockets
The application uses sockets to transfer the data from MP to AP and vice versa. The socket that's implemented is based on a TCP protocol and accomodates dataflow of both JSON and Filetransfer
  - The master.py will be excuted with the MP Site resembling a server
  - The reception.py will be executed with AP application resembling a client

## QR Code 
### General Overview
The application uses QR code, when admin reports faluty car then QR code is generated so engineers can see that QR code in their dashboard and retrive the issues by scanning QR code. engineers can algo login using QR code.
 * The following dependecies are required for facereognition system 
  ```shell
    pip3 install qrcode
	pip3 install pyzbar
  ```
## Voice Recognition
### General Overview
The application facilitates the voice recognition system that is developed using the google speech to text API. Admins can search cars using voice search. We need usb mic in order to make voice recognition work, as raspberry pi doesn't have built-in mic so we need to use external mic.
* The following dependecies are required for voice recognition system 
```shell
    pip3 install SpeechRecognition
	sudo apt-get install portaudio19-dev python-all-dev python3-all-dev
	pip3 install pyaudio
	pip3 install google-api-python-client
	sudo apt-get install flac
```
## Bluetooth Implementation
### General Overview
The application uses bluetooth for login to agent pi. Engineers can use bluetooth in login to the agent pi.
* The following dependencies are required for bluetooth implementation 
```shell
   sudo apt-get install python-pexpect
   pip3 install pexpect
```

## Face Recognition
### General overview
The application facilitates the face recognition system that is developed using the OpenCV and haarcascade face detection endoers the model used HSR conversion of the image to and reduces the scaling to process the images quicker. The face recognition system is implemented using ip camera as there was no physical camera available.
  * The following dependecies are required for facereognition system 
  ```shell
    sudo apt-get install python3-opencv
    sudo apt-get install libhdf5-dev
    sudo apt-get install libhdf5-serial-dev
    sudo apt-get install libatlas-base-dev
    sudo apt-get install libjasper-dev
    sudo apt-get install libqtgui4
    sudo apt-get install libqt4-test
  ```
## Documentation
The documentaion is created using the sphinx and requires the following commands to be exected to generate the documnetation once initial setup is finished. 
  ```
    make clean
    make html
  ```
  The folloing extensions were also used in the setup.
  ```
  sphinx.ext.autodoc', 'sphinx.ext.coverage', 'sphinx.ext.napoleon'
  ```
## Credentials for 3 different users

 username | password | role
 ---------|----------|------------
avishekh.bharati@gmail.com | avishekh | admin
manager@password.com | password | manager
engineer2@password.com | password | engineer
 

## Trello board usage
![alt text](https://github.com/rmit-s3804879-sainathreddy-kodiganti/IoTAssignment3/blob/master/src/MP/static/img/trelloboardusage.PNG)
 
## TaskCard
![alt text](https://github.com/rmit-s3804879-sainathreddy-kodiganti/IoTAssignment3/blob/master/src/MP/static/img/cards.PNG)

## Github contribution
![alt text](https://github.com/rmit-s3804879-sainathreddy-kodiganti/IoTAssignment3/blob/master/src/MP/static/img/github.png)

