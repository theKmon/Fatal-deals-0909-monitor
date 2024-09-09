# Price Monitoring and Notification System

## Overview

This Python-based project is designed to monitor hotel prices on [Fattal-Alazman](https://www.fattal-alazman.co.il/) and send email alerts when prices drop below a specified threshold. It uses Selenium to automate price checking, and email notifications are sent using Gmail's SMTP service.

## Features

- Monitors hotel prices automatically.
- Sends email alerts when prices fall below a certain value.
- Can be customized to monitor different URLs and price thresholds.
- Uses environment variables for sensitive data such as email credentials.

## Prerequisites

Make sure you have the following installed on your system:

- Python 3.x
- [ChromeDriver](https://sites.google.com/a/chromium.org/chromedriver/) (required for Selenium to interact with the browser)
- A Gmail account for sending email alerts

## Setup and Installation

### 1. Clone the repository

```bash
git clone https://github.com/theKmon/Fatal-deals-0909-monitor.git
cd Fatal-deals-0909-monitor
```

### 2. Create a Virtual Environment
It is recommended to use a virtual environment to manage dependencies.

```bash
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate
```

### 3. Install Dependencies
Install all the necessary Python libraries using the requirements.txt file.
```bash
pip install -r requirements.txt
```

### 4. Set up Environment Variables

To send email alerts, you'll need to set up the following environment variables:

- `SENDER_EMAIL`: The Gmail address from which the alert emails will be sent.
- `RECEIVER_EMAIL`: The email address to receive the alerts.
- `EMAIL_PASSWORD`: The app-specific password for the sender Gmail account. (You must generate an app password from Gmail if you have 2-factor authentication enabled.)

#### How to Set Environment Variables

On **Linux/macOS**:

```bash
export SENDER_EMAIL="your-email@gmail.com"
export RECEIVER_EMAIL="receiver-email@gmail.com"
export EMAIL_PASSWORD="your-app-specific-password"
```

On **Windows** (PowerShell):
```powershell
$env:SENDER_EMAIL="your-email@gmail.com"
$env:RECEIVER_EMAIL="receiver-email@gmail.com"
$env:EMAIL_PASSWORD="your-app-specific-password"
```
Alternatively, you can add these environment variables to your `.env` file (make sure this file is listed in `.gitignore` to avoid exposing sensitive information):
```bash
SENDER_EMAIL=your-email@gmail.com
RECEIVER_EMAIL=receiver-email@gmail.com
EMAIL_PASSWORD=your-app-specific-password
```
See [How to generate Gmail app passwords](https://knowledge.workspace.google.com/kb/how-to-create-app-passwords-000009237)
### 5. Running the Project

Once you have the environment variables set and all dependencies installed, you can run the project:

```bash
python main.py
```
This will start the price monitoring script. The system will check for price updates and send an email when the price drops below the defined threshold.

### 6. **(Optional) Updating** `requirements.txt`
If you install additional libraries, remember to update the `requirements.txt` file:
```bash
pip freeze > requirements.txt
```

### Project Structure

```plaintest
├── README.md               # Project readme file
├── requirements.txt        # Project dependencies
├── main.py                 # Main script that starts the price monitoring
├── email_sender.py         # Handles email notifications
├── custom_logger.py        # Custom logging functionality
├── .gitignore              # Files/folders to ignore in Git
└── venv/                   # Virtual environment folder (should not be included in Git)
```
### Troubleshooting

#### Common Issues
- **Selenium WebDriver Issues:** Ensure that ChromeDriver is installed and the version matches your Chrome browser.
- **Email Sending Errors:** Ensure you have set up the environment variables correctly and that you're using an app-specific password from Gmail if you have 2-factor authentication enabled.
- **Permission Denied Errors:** Double-check file permissions and make sure the virtual environment is properly activated.

### License

This project is licensed under the MIT License. See the `LICENSE` file for more details.