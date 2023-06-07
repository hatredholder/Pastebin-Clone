<h1 align="center">Pybin - Pastebin Clone</h1>

<div align="center">
    	<a href="#sparkles-features">Features</a>
  <span> • </span>
       	<a href="#mag-preview">Preview</a>
  <span> • </span>
  	<a href="#open_book-instructions">Instructions</a>
  <span> • </span>
	<a href="#test_tube-testing">Testing</a>
  <p></p>
  
</div> 

<div align="center">

![Python](https://img.shields.io/badge/Python-3776AB?logo=python&logoColor=3776AB&labelColor=adbabd)
![Flask](https://img.shields.io/badge/Flask-FFFFFF?color=000000&logo=flask&logoColor=000000&labelColor=adbabd)
![MongoDB](https://img.shields.io/badge/MongoDB-FFFFFF?color=47A248&logo=mongodb&logoColor=47A248&labelColor=adbabd)
![Docker](https://img.shields.io/badge/Docker-2496ED?logo=Docker&logoColor=2496ED&labelColor=adbabd)

![Pytest](https://github.com/hatredholder/Pastebin-Clone/workflows/tests/badge.svg)
[![Coverage Status](https://coveralls.io/repos/github/hatredholder/Pastebin-Clone/badge.svg?branch=main&)](https://coveralls.io/github/hatredholder/Pastebin-Clone?branch=main)

</div>

## :sparkles: Features

- OAuth Authentication
- Email Verification
- Syntax Highlighting
- Search Pastes
- Paste Commenting and Rating
- Public and Private Paste Creation
- Welcoming Message on User Signup

## :mag: Preview

![Preview](https://user-images.githubusercontent.com/86254474/231093069-1e3616f5-50a2-41cd-9737-d093b0328603.png)

## :open_book: Instructions

### 1. Clone this **repository** onto your local machine, **cd** into it
```
git clone git@github.com:hatredholder/Pastebin-Clone.git
cd Pastebin-Clone
```

### 2. Update enviroment variables in **.env** to match your preferences
```
# Flask Settings
FLASK_SECRET_KEY="your_secret_key_here"
FLASK_EMAIL_VERIFICATION_ENABLED=false
FLASK_SOCIAL_AUTHENTICATION_ENABLED=false

# Mongo Settings
FLASK_MONGODB_SETTINGS={"db": "pastebinCloneDb", "host": "db", "port": 27017}
```

<details>
  <summary><b>To Enable Email Verification</b></summary>
  
  <p></p>
  
- [X] *Set `FLASK_EMAIL_VERIFICATION_ENABLED` to true*
  ```
  FLASK_EMAIL_VERIFICATION_ENABLED=true
  ```
  
  <p></p>
  
- [X] *Set these enviroment variables to your email credentials*
  ```
  FLASK_MAIL_SERVER="smtp.gmail.com"
  FLASK_MAIL_USERNAME="example@gmail.com"
  FLASK_MAIL_PASSWORD="example_password"
  FLASK_MAIL_PORT=587
  FLASK_MAIL_USE_TLS=true
  FLASK_MAIL_USE_SSL=false
  ```
  > NOTE: In order for GMail to work as your email server you need to setup two-factor authorization **(2FA)**
  
</details>

<details>
  <summary><b>To Enable OAuth Authentication</b></summary>
  
  <p></p>
  
- [X] *Set `FLASK_EMAIL_VERIFICATION_ENABLED` to true*
  ```
  FLASK_SOCIAL_AUTHENTICATION_ENABLED=true
  ```
  
  <p></p>
  
- [X] *Create a new project in Google Cloud*
  
* Go to https://console.cloud.google.com/ 
* Register a service with Google > create a new project
* Within the new project, go to APIs + Services > Create credentials > Configure Consent Screen > External Users > name the project again > enter user support email > leave defaults
* Go back to dashboard > Credentials > Create Creds > OAuth Client ID > web app > define your redirect url of your web app (http://localhost/login/callback)
* Create the call back > download your creds as a json file 

- [X] *Put the `client_secret.json` file to your source directory (next to app.py)*

#### Your project filetree should look like this
```
├── authentication/
├── pybin/
├── requirements/
├── static/
├── templates/
├── tests/
├── .env
├── .gitignore
├── Dockerfile
├── README.md
├── app.py
├── client_secret.json
├── docker-compose.yml
└── setup.cfg
```

</details>


### 3. Run the server with **docker-compose**
```
docker-compose up -d
```

## :test_tube: Testing

### 1. To use the **tests** you need to install **local** module requirements first, to do that, use:
```
pip install -r requirements/local.txt
```

### 2. Run the **tests** and check the **coverage**:
```
pytest -k "not email_configured and not oauth_configured" --cov
```

### 3. Generate an HTML **coverage** report:
```
pytest -k "not email_configured and not oauth_configured" --cov-report html:cov_html --cov
```

### 4. Test the **code quality** (see if there are any PEP8 errors):
```
ruff --check .
```