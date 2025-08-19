# Integrated Traffic Management System

An AI-powered traffic management and violation detection system. This project uses computer vision with YOLO models to monitor traffic feeds, detect various violations, and automate the process of issuing challans.

## Key Features

- **Helmet Violation Detection**: Identifies motorcyclists who are not wearing a helmet.
- **Driver Distraction Monitoring**: Detects drivers using mobile phones while driving.
- **Traffic Signal Compliance**: Monitors vehicles for red-light violations.
- **Automated Challan System**: Capable of generating violation reports or "challans".
- [cite_start]**Email Notification**: Automatically sends violation alerts via email. [cite: 1]
- **Web-Based Dashboard**: Includes a web interface built with Flask for viewing analytics and results.

## Setup and Installation

Follow these steps to set up and run the project on your local machine.

### 1. Clone the Repository

First, clone the project from your GitHub repository.

```bash
git clone [https://github.com/basudeabhijeet/Integrated-Traffic-Management-System.git](https://github.com/basudeabhijeet/Integrated-Traffic-Management-System.git)
cd Integrated-Traffic-Management-System
```

### 2. Create a Virtual Environment

It is highly recommended to use a virtual environment to manage project dependencies.

```bash
# Create the virtual environment
python -m venv venv

# Activate the virtual environment
# On Windows:
.\venv\Scripts\activate
# On macOS/Linux:
source venv/bin/activate
```

### 3. Install Dependencies

Install all the required Python packages using the `requirements.txt` file.

```bash
pip install -r requirements.txt
```

### 4. Download the AI Models

The model files are not stored in the GitHub repository due to their large size. [cite_start]You need to download them manually and place them in the correct folders. [cite: 2]

**Create a `models` directory in the project's root folder.**

```bash
mkdir models
```

Now, download the following model files and place them inside the `models` directory:

- **`yolov5-tiny.weights`**: [**<-- INSERT DIRECT DOWNLOAD LINK HERE**]
- **`yolov8n.pt`**: [**<-- INSERT DIRECT DOWNLOAD LINK HERE**]
- **`model_v2.h5`**: [**<-- INSERT DIRECT DOWNLOAD LINK HERE**]

You will also need the `yolov8m.pt` file in the root directory:

- **`yolov8m.pt`**: [**<-- INSERT DIRECT DOWNLOAD LINK HERE**]

After downloading, your folder structure should look like this:

```
Integrated-Traffic-Management-System/
├── models/
│   ├── yolov5-tiny.weights
│   ├── yolov8n.pt
│   └── model_v2.h5
├── yolov8m.pt
├── app_v2.py
└── ... (other project files)
```

### 5. Configure Environment Variables

This project uses an `.env` file to manage sensitive information like email credentials. [cite_start]This file is not included in the repository for security. [cite: 2]

1.  Create a new file named `.env` in the root of your project directory.
2.  [cite_start]Add the following content to the file, replacing the placeholder values with your actual email credentials for sending notifications. [cite: 1]

```env
EMAIL_SENDER=your_email@gmail.com
EMAIL_PASSWORD=your_google_app_password
```
**Note**: For Gmail, you will need to generate an "App Password" from your Google Account security settings if you have 2-Step Verification enabled.

## Usage

Once you have completed the setup, you can run the main application.

```bash
python app_v2.py
```

This will start the Flask web server. You can then navigate to the provided URL (usually `http://127.0.0.1:5000`) in your web browser to access the application's dashboard.

---
````
