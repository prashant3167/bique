
# Bique

Bique aims to empower individuals with the tools and resources needed to achieve financial freedom by simplifying financial management and providing expert financial advice through our user-friendly interface offering a personalized yet seamless experience. Encompassing a variety of tasks like sharing profile with family members, defining combined budgetary limits, competing to achieve financial goals, etc. We aspire to make financial management for our users effortless and enjoyable. With all these functionalities, we intend to be the leader in financial advisory, management and assistance in the market for individuals and families. BIQUE does not only understand ESG (environmental, social and governance) as one of the most crucial goals, often supported by investors as well as the customers for our company’s success but also shall constantly strive towards meeting them.

## Installations needed
- Docker
- Mongo

## Installing Steps for MongoDB 4.4 on Ubuntu

This guide will walk you through the steps to install MongoDB 4.4 on Ubuntu. MongoDB is a NoSQL document-oriented database program that is widely used for its flexibility, scalability, and performance.

### Prerequisites

Before starting the installation process, make sure that you have the following prerequisites:

- Ubuntu operating system (version 18.04 or later)
- sudo privileges
- Access to the internet
- Git installation on the virtual machine

### Step 1: Import the MongoDB public GPG key

The first step is to import the MongoDB public GPG key to the system. This key is used to sign the packages, and it ensures that the packages are authentic and from a trusted source.


```perl
sudo apt-key adv --keyserver hkp://keyserver.ubuntu.com:80 --recv EA312927
```
### Step 2: Add MongoDB repository

Next, you need to add the MongoDB repository to the system. Create the list file for MongoDB with the following command:

```bash

echo "deb [ arch=amd64,arm64 ] https://repo.mongodb.org/apt/ubuntu $(lsb_release -sc)/mongodb-org/4.4 multiverse" | sudo tee /etc/apt/sources.list.d/mongodb-org-4.4.list
```

### Step 3: Install MongoDB 4.4

Once the repository is added, update the package list and install MongoDB 4.4 using the following commands:

```

sudo apt update
sudo apt install mongodb-org
```

### Step 4: Start MongoDB service

MongoDB service should start automatically after the installation is complete. However, you can start it manually using the following command:

```sudo systemctl start mongod```

To ensure that MongoDB starts automatically on boot, enable the service using the following command:

```bash

sudo systemctl enable mongod```

## Step 5: Verify MongoDB installation

Finally, verify that MongoDB is installed and running properly by connecting to the database using the mongo shell:

```mongo```

This will open the MongoDB shell, and you should see the following output:

```python

MongoDB shell version v4.4.x
connecting to: mongodb://127.0.0.1:27017/?compressors=disabled&gssapiServiceName=mongodb
```

Congratulations! You have successfully installed MongoDB 4.4 on your Ubuntu machine.

### Installing Docker on Ubuntu

This steps will walk you through to install Docker on Ubuntu. Docker is a popular platform for developing, packaging, and deploying containerized applications.



### Step 1: Install Docker CE

To install Docker CE (Community Edition) on Ubuntu, you need to add the Docker repository to the system. Run the following commands to add the repository and install Docker CE:

```sql

sudo apt-get update
sudo apt-get install apt-transport-https ca-certificates curl gnupg lsb-release```

Add Docker’s official GPG key:

```arduino

curl -fsSL https://download.docker.com/linux/ubuntu/gpg | sudo apt-key add -
```

Add the Docker repository to the system:

```bash

sudo add-apt-repository "deb [arch=amd64] https://download.docker.com/linux/ubuntu $(lsb_release -cs) stable"
```
Install Docker CE:

```sql

sudo apt-get update
sudo apt-get install docker-ce docker-ce-cli containerd.io
```

Step 2: Verify Docker installation

After the installation is complete, verify that Docker is installed correctly by running the following command:

```arduino

sudo docker run hello-world
```

This command will download a small Docker image and run it in a container. If Docker is installed correctly, you should see the following output:

```

Hello from Docker!
This message shows that your installation appears to be working correctly.
...
```

Congratulations! You have successfully installed Docker on your Ubuntu machine.

## Deployment

To deploy this project run the below lines

### Step 1: Clone the repository inside the virtual machine
```bash
  git clone https://github.com/prashant3167/bique.git
```

### Step 2: Create mongo user inside which can be accesed by bique gate
```
mongo
use bique
db.createUser(
  {
    user: "bdm",
    pwd: "bdm",
    roles: [
       { role: "readWrite", db: "bique" }
    ]
  }
)
```

### Step 3: Get ip address of the vm
```hostname -I | awk '{print $1}'
```
###Step 4: Edit config file inside src to provide the mongo credentials inside bique/bique-gate/src
```[Mongo]
host = "10.4.41.51"
user = "bdm"
passsword = "bdm"
```

### Step 5: Go inside the bique-gate folder
```bash
  cd bique/bique-gate
```

### Step 6: Bring the docker-compose infra for bique
```bash
  sudo docker-compose up -d --build
```

### Step 6: Check Service is up
```bash
  curl localhost:8000
  welcome to bique-gat
```

<b>🥳 Bique gateway is up and ready to receive your requests</b>

## Contributors

Zyad | Prashant | Rishika |
--- | --- | --- |
| <img src="./assets/zyad.jpg" width="200" height="200" /> | <img src="./assets/prashant.jpg" width="200" height="200" /> |<img src="./assets/rishika.jpg" width="200" height="200" />|
