# Insurance_Aggregator

## Table of contents
1. [Introduction](#introduction)
2. [Prerequisites](#prerequisites)
3. [Getting Started](#start)
    1. [Clone Repository](#clone_repository)
    2. [Database Setup](#database_setup)
    3. [Environment Check](#env_check)
4. [Running the Application](#run_app)
    1. [Start Docker Containers](#start_docker)
    2. [Configure Kong API Gateway](#configure_kong)
5. [Navigating the Application](#nav_app)
    1. [Customer](#customer)
    2. [Agent](#agent)
5. [Technical Overview](#tech_overview)
    1. [Database Schema](#database_schema)
    2. [Microservices](#microservices)
    3. [API Gateway](#api_gateway)

<br>

## Introduction <a name="introduction"></a>
With many insurance companies offering a multitude of policies, customers may find it difficult to find a policy that best suits their needs. As such, an insurance policy aggregator platform comes in handy! It aggregate policies from various insurance companies and through a simple scoring algorithm, it recommends the top 5 policies that are best suited for the customer.

This repository contains instructions of setting up and running the application on localhost, meant for **Windows** or **Mac** OS. Ensure that you also have all the [prerequisites](#prerequisites) covered before you [get started](#start).

[Back To The Top](#Insurance_Aggregator)

<br>

## Prerequisites <a name="prerequisites"></a>
- [Python](https://www.python.org/downloads/): >= 3.8
- [Docker Desktop](https://docs.docker.com/get-docker/)
- [WAMP](https://www.wampserver.com/en/download-wampserver-64bits/) (Windows)/ [MAMP](https://www.mamp.info/en/downloads/) (Mac)
- [Paypal](https://developer.paypal.com/docs/api-basics/sandbox/accounts/#create-a-personal-sandbox-account) Account Credentials
- [SendGrid](https://signup.sendgrid.com/) API Key

[Back To The Top](#Insurance_Aggregator)

<br>

## Getting Started <a name="start"></a>
To get things started, you need to:
1. [Clone this repository](#clone_repository) into your local machine
2. [Set up database](#database_setup) using phpMyAdmin

<br>

### Clone Repository <a name="clone_repository"></a>
Since the UI will be hosted on WAMP/MAMP, clone the repository into your WAMP/MAMP root folder.
Windows - "www" folder
Mac - "htdocs" folder

<br>

Navigate to the root folder and run the following command to change directory into Xampp's htdocs:
```
git clone https://github.com/sszh1904/Insurance_Aggregator_Platform.git
```
You will be prompted to log in to a Github account. Please log in to your Github account and you will be able to access this public repository.

<br>

### Database Setup <a name="database_setup"></a>
To setup the MySQL database:
1. Launch your web browser and type "localhost/phpmyadmin"
2. Login and ensure that the port number phpMyAdmin is running on is 3306
3. At the homepage of “localhost/phpmyadmin”:
    - Click “Import” at the top
    - Click the “Choose File” button
    - Navigate to the “Insurance Aggregator” folder which was placed in the WAMP/MAMP root folder and select the “agent.sql” file
    - Click “Go”
4. Go back to the homepage of phpMyAdmin (http://localhost/phpmyadmin/index.php)
5. Repeat steps 3 & 4 to import “customer.sql” and “transaction.sql”

<br>

Upon completion, you should see 3 separate database schemas created, namely “agent”, “customer” and “transaction”. 

<br>

### Environment Check <a name="env_check"></a>
Launch Docker Desktop and ensure that none of your existing containers are using the following ports:
- 1337
- 5432
- 5672
- 8000
- 15672

<br>

If they do, please shut down the containers. If not, you're now ready to [run the application](#run_app)!

[Back To The Top](#Insurance_Aggregator)

<br>

## Running the Application <a name="run_app"></a>
To get a functioning application, you need to:
1. [Start Docker Containers](#start_docker)
2. [Configure Kong API Gateway](#configure_kong)

<br>

### Start Docker Containers <a name="start_docker"></a>
Navigate to the app folder in this repository. After which, run the following command to build the Docker containers:
```
docker-compose build
```

<br>

Run the following command to start the Docker containers:
```
docker-compose up
```

<br>

#### Additional Information

To **stop** the Docker containers, press ```Ctrl``` or ```Cmd``` + ```C```. Alternatively, run the following command:
```
docker-compose down
```
<br>

To stop and remove containers, networks, images, and volumes - run the following command:
```
docker-compose down -v
```

<br>

### Configure Kong API Gateway <a name="configure_kong"></a>
To configure Kong API Gateway:
1. Launch your web browser and type "localhost:1337"
2. Create the administrator account with the following details:
    - Username: admin
    - Email: <enter your email address>
    - Password: adminadmin
    - Confirm password: adminadmin
3. Login using the username and password above
4. Set up the Connection to Kong Admin using the following details:
    - Name: default
    - Kong Admin URL: http://kong:8001
5. Click on “SNAPSHOTS” at the left menu bar
6. Click “IMPORT FROM FILE”
7. Navigate to the “Insurance Aggregator” folder which was placed in the WAMP/MAMP root folder
8. Select and import the “konga_snapshot.json” file
9. Click on “DETAILS”
10. Click on the “RESTORE” green button
11. Click on the checkbox for “services” and leave the rest unchecked
12. Click the “IMPORT OBJECTS” button
    - You should see that 9 services are imported and 0 has failed
13. Close the modal
14. Repeat step 10
15. Click on the checkbox for “routes” and leave the rest unchecked
16. Repeat step 12 & 13

<br>

Now, go to "http://localhost/Insurance_Aggregator_Platform/app/templates" on your browser and you may start [navigating the application](#nav_app)!

[Back To The Top](#Insurance_Aggregator)

<br>

## Navigating the Application <a name="nav_app"></a>
There are 2 different user types - [customer](#customer) and [agent](#agent). 

<br>

### Customer <a name="customer"></a>
Customers will need to first register an account, then the application would retrieve the customer's details from SingPass Sandbox API and store it in the customer's database. 

#### Registration
NRIC - choose from one of the dummy NRICs stated below:
- S9812381D
- S9812382B
- S9812385G
- S9812387C
- S9912363Z
- S9912366D
- S9912369I
- S9912370B
- S9912372I
- S9912374E
- S6005053H
- S6005055D

Password - no requirements

Email Address - your email address

<br>

Upon successful registration, you will be redirected to the login page. You may then log in with the new customer account and explore the features for customers!

<br>

### Agent <a name="agent"></a>
Agents do not need to register for an account, as dummy agent accounts already exist in the database.

*Dummy Agent Account* <br>
*NRIC: S1234567A* <br>
*Password: sam123* <br>

Use the above account credentials and check the "I am an agent" checkbox to log in as an agent. Have fun exploring the features as an agent!

[Back To The Top](#Insurance_Aggregator)
