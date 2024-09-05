
# DEF 14A Analysis WebApp

This tool enables supervised topic modelling of form DEF 14A (Definitive Proxy Statement) filed by S&P500 corportations between the years of 2016 and 2022.

# Installation Instructions

To set up and run the WebApp locally, follow these steps:

1. **Clone the Repository**

   First, clone the repository to your local machine using Git:

    ```
    gh repo clone ResearchComputingServices/LeanneKeddie
    ```

2. **Create a Virtual Environment**

    It's recommended to create a virtual environment for Python projects. This keeps dependencies required by different projects separate. To create a virtual environment, run:

    ```
    python3 -m venv .venv
    ```

    Activate the virtual environment:

    ```
    source .venv/bin/activate
    ```

3. **Install Dependencies**

    Install all the required packages using pip:
    ```
    pip install -r requirements.txt
    ```

    The [Athabaska package](https://github.com/ResearchComputingServices/Athabasca) must be installed separately. To 
    do so run the following commands 

    ```
    gh repo clone ResearchComputingServices/Athabasca
    cd Athabasca
    pip install -e .
    ```

# Running the DEF 14A Analysis WebApp

The webapp can be run local for debugging and development by executing the following command in the `webapp/` directory of the git repo:

```
streamlit run leanne-keddie-webapp.py
```

The webapp was deployed on an Apache2 server. Two configuration files must be create as described below. One for the apache2 server and the other for streamlit. The wepapp will also need to be run using the command given above.

The Apache2 virtual host used the following configuration file:

```
<VirtualHost *:80>
   RewriteEngine On

   RewriteCond %{HTTP:Upgrade} =websocket
   RewriteRule /(.*) ws://localhost:8502/$1 [P]
   RewriteCond %{HTTP:Upgrade} !=websocket
   RewriteRule /(.*) http://localhost:8502/$1 [P]

   ProxyPassReverse / http://localhost:8502
</VirtualHost>

```

A configuration file is also required in the `webapp/.streamlit` directory:

```
[server]
headless = true
port = 8502

[browser]
serverAddress = "eng-bucking-2gtx"
```