# ecommerce site Titled: Nuno shop
  Author: Vishnusekar C

# Setup Prerequisites - Required Softwares
1. Python3 Virtual Environment with Pip
2. WSL using Ubuntu or similar distro
3. Code editing software such as Visual Studio
4. API call software such as Postman (or similar extensions offered in VSCode such as Thunder Client)
5. Ngrock toolkit
6. Razorpay Test mode account

# Setup Instructions

1. Download the WSL 1 or 2 software and setup a local environment
2. Ensure the system is available in its latest version
   ```
   apt-get update
   ```
4. Install the pip package and then the python virtual environment
   ``` 
   apt install python3-pip
   pip3 install virtualenv
   apt install python3.10-venv
   ```
6. Verify the installation
   ```
   python3 -V
   which python
   pip3 list
   ```
8. Navigate to the path where the sourcecode is available and create a virtual environment from that location
   ```
   cd /mnt/e/WILP/Sem3/Service\ Oriented\ Computing/Assignment/
   python3 -m venv ecommerce_env
   ```
10. Activate the virtual environment
    ```
    source ecom_env/bin/activate
    ```
12. Setup the django environment from the repository code
    ```
    python -m django --version
    python manage.py makeserver
    python manage.py migrate
    python3 manage.py runserver 8000
    ```
14. Install ngrock and run it on http port 8000
    ```
    curl -s https://ngrok-agent.s3.amazonaws.com/ngrok.asc | sudo tee /etc/apt/trusted.gpg.d/ngrok.asc >/dev/null && echo "deb https://ngrok-agent.s3.amazonaws.com buster main" | sudo tee /etc/apt/sources.list.d/ngrok.list && sudo apt update && sudo apt install ngrok
    ngrok config add-authtoken <<token-from-ngrok-website>>
    ngrok http 8000
    ```
