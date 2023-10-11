---
title: "Local Onebox Installation"
slug: "local-onebox-installation"
hidden: true
createdAt: "2022-06-01T17:56:11.451Z"
updatedAt: "2022-09-14T20:07:46.121Z"
---
## Onebox

Onebox enables users to experience Fiddler’s leading explanations, analytics, and monitoring capabilities by running Fiddler locally using their own models and data (or the included samples).

## Setup

**Time**: 10 mins

**Dependencies**:

- Docker (v19+). Install here - <https://docs.docker.com/docker-for-mac/install/>

> 🚧 Note
> 
> If you are using a Mac to run Onebox, make sure to allocate the maximum (or at least 4GB) memory reserved for docker (via  Docker Icon > Preferences > Advanced > Memory)

- Mac or Linux. MacOS Sierra 10.12 or newer is supported
- To install Onebox on AWS EC2 or similar VMs, Make sure you read the [onebox requirements](onebox.md#systems-requirements) section below

**Steps**:

1.Download Onebox  
Click on the time-sensitive download link included in the email with the included credentials to download fiddler-onebox-1.x.xx.tar.gz. This is a large 4GB+ size file.

Alternatively, you can download from the command line:

```bsh
curl --output fiddler-1.x.xx.tar.gz https://s3-us-xxxx-x.amazonaws.com/fiddler.ai/download/fiddler-1.x.xx-5743889dc.tar.gz
```



2.Untar (replace with latest file name):

```bsh
tar zxvf fiddler-1.x.xx-edXNtP4SAe8FvxKp.tar.gz
```



- Note: The download link will expire automatically after a period of time (30, 60, or 90 days. depending on the license).

  3.Run Onebox

```
```



```
```



- Loads fiddler images into docker. Note: Make sure Docker is running

```
```



Starts fiddler containers. The output will look like:

```bsh
Starting Fiddler
e7a5faf0511c4bbe100abc6bed1718775db66ed72c7bd9323cfa9ca086ddef9c
0615a9ca695ead38d0390ad405921d2a480f316e75f58dbd8e9de4ba5d7c680f
2467341e00b8e3f59390825fd239034d7b883c74f166bc156d1cfc87f06a209a
48dbd78bd9e09bcf8952644ff0d71fbe3cc9b350d4811fdd312375f27104c584
Fiddler hosted at: http://localhost:4100
```



4.Optionally, the service can support HTTPS access over port 443. This can be enabled by providing appropriate TLS certificate during startup:

```
```



**Directory Structure**

![](https://files.readme.io/52fe5ce-Onebox_File_Structure.png "Onebox_File_Structure.png")

Under the fiddler directory, you’ll see a repo directory containing the onebox directory. The onebox directory contains project directories (e.g. `bank_churn`, `iris_classification`, `lending`). It also contains dataset directories, found within datasets (e.g. `p2p_loans`, `winequality`).

**Commands**

```
```



```bsh
   $ cd samples
   $ ./deploy
```



Fiddler Onebox comes with pre-loaded samples. If samples don't exist, then run the above command to imports all dataset and models to Fiddler

```
```



```
```



**Accessing the UI**

You can access the Fiddler UI locally with Onebox using <http://localhost:4100>.

You will be prompted to log in. Use the following credentials:

- Username: onebox@fiddler.ai
- Default password: xai/4u  
  		\* You can change the password in Settings → General.

Once user logs into fiddler, a home page appears as seen in the below screenshot.

![](https://files.readme.io/49ad4c6-Home_Page_1.png "Home_Page (1).png")

For the next steps in the onboarding, visit our [Quick Start](doc:quick-start) guide to get started.

## Upgrade

If you’re upgrading from an older Onebox solution and you want to transfer all your data and model changes to the new version, follow these steps:

1. Copy your local `fiddler` folder to a new folder called `fiddler-backup`.
2. Follow the steps in the **Setup** section above to install the latest version of Onebox.
3. Copy the `license.key` file from your new `fiddler/repo/onebox/common` folder and put it in a safe place.
4. Delete the `repo` and `data` directories from your new `fiddler` directory.
5. Copy the `repo` and `data` directories from your `fiddler-backup` directory into your new `fiddler` directory.
6. Replace the `license.key` file in your `repo/onebox/common` folder with the copy that you saved in step 3.
7. (Optional) If you want to save space, you can delete the fiddler-backup directory.

## Systems requirements

- Image - Linux (Supported distro: Amazon AMI HVM, Ubuntu, Centos, RHEL, Mac OS)
- Compute - 8 cores, 32GB or larger machines
- Storage - min. 128GB
- Port - 4100 or 443 (HTTPS support on port 443)  
  		- Internally uses 5100, 6100, 27017, 5432, 4369
- Docker - min. Docker ver 19+

> 🚧 Note
> 
> If you are using a Mac to run Onebox, make sure to allocate the maximum (or at least 4GB) memory reserved for docker (via  Docker Icon > Preferences > Advanced > Memory)

### Supporting packages

- Linux 64bits with docker support
- `bash` for scripts
- `nc` (net cat) for establishing command line tcp connection
- `curl`
- internet connection for pip install packages

### Server Setup

Please run the following commands or equivalent depending on where Fiddler is running. These instructions are for an AWS EC2 instance.

Once the EC2 instance is successfully started, SSH into the machine.

```bash
ssh -i "../deploy/secret/fiddler-service.pem" \
   ec2-user@ec2-<--ipaddress-->.<region>.compute.amazonaws.com
```



Perform the yum update, followed by installing docker and adding your user to the docker group:

```
sudo yum update -y
sudo amazon-linux-extras install docker
sudo service docker start
sudo usermod -a -G docker ec2-user
```



Next, install `nc`

```
sudo yum install nc
```



Log out and SSH into the machine again, then run the following commands:

```
docker info
docker images
```



[^1]\: _Join our [community Slack](https://www.fiddler.ai/slackinvite) to ask any questions_