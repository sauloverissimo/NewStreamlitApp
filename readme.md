<p align="center"><img src="logo/Streamlit-Logo-Vector.png" alt="NewStreamlitApp Logo" width="150"/></p>

<h1 align="center">NewStreamlitApp: A Multipage Streamlit Application Framework</h1>

<p align="center">
  A scalable, modular, and efficient framework to build Streamlit applications with authentication, navigation, and session management.
</p>

---

## 📖 Table of Contents

1. [Introduction](#introduction)
2. [Features](#features)
3. [Getting Started](#getting-started)
4. [File Structure](#file-structure)
5. [Technologies Used](#technologies-used)
6. [Contributing](#contributing)
7. [License](#license)

---

## 📌 Introduction

**NewStreamlitApp** is a comprehensive framework for developers to create professional multipage applications using **Streamlit**. With features like **authentication**, **navigation**, and **session management**, this framework offers all the essential tools for building scalable and interactive web applications.

---

## ✨ Features

- **🔒 Authentication:** Secure user login with SQLite and bcrypt-based password hashing.
- **📑 Multipage Navigation:** Effortless navigation between pages with a sidebar.
- **🧵 Session Management:** Persistent session states for global and page-specific data handling.
- **📦 Modular Design:** Simplified and scalable codebase structure.
- **🚀 Ready for Expansion:** Extend functionality with minimal effort.

---

## 🚀 Getting Started

### Prerequisites
- Python 3.8 or above
- pip (Python package installer)

### Installation

1. Clone the repository:
   ```bash
   git clone https://github.com/sauloverissimo/NewStreamlitApp.git
   cd NewStreamlitApp

2. Install Dependencies:
   ```bash
   pip install -r requirements.txt 

3. Run the application::
   ```bash
   streamlit run app.py 

4. File Structure


## Project Structure

````
NewStreamlitApp/

├── app.py              # Main application file
├── auth/               # Authentication module
│   ├── login.py        # Handles user login logic
├── db.py               # SQLite database configuration
├── nav.py              # Navigation settings with exemple pages
├── page/               # Application pages
│   ├── home.py         # Home exemple page
│   ├── management.py   # Management exemple page
│   ├── architecture.py # Architecture exemple page
│   ├── development.py  # Development exemple page
├── sessions/           # Session management module
│   ├── state.py        # Manages session states
├── requirements.txt    # Python dependencies
├── app.db              # SQLite database file
├── .streamlit/         # Streamlit configuration files
├── .dockerignore       # Docker ignore file
├── Dockerfile          # Docker configuration file

````


## 🐳 Docker File
Build the Docker image:

1. Terminal -> Go to NewStreamlitApp folder:
   ```bash
   docker build -t new_streamlit_app .

2. Terminal -> List Docker Images:
   ```bash
   docker images

   Result:

   REPOSITORY       | TAG         |IMAGE ID       |CREATED         |SIZE
   new_streamlit_app|   latest    |abc123456789   |2 minutes ago   |150MB

3. Terminal -> Test image Docker:
   ```bash
   docker run -p 8501:8501 new_streamlit_app

4. Terminal -> List Docker Images Running:
   ```bash
   docker ps

5. Browser:
   ```bash
   http://localhost:8501  
   
---

## 🛠️ Technologies Used
    - Streamlit: A powerful framework for building - interactive web applications.
    - SQLite: Lightweight database for local data storage.
    - bcrypt: For secure password hashing.

---

## 🤝 Contributing
### We welcome contributions! To contribute:

1. Fork the repository:
   ```bash
   git checkout -b feature/your-feature-name

2. Commit your changes:
   ```bash
   git commit -m "Add your message here"

3. Push your branch:
   ```bash
   git push origin feature/your-feature-name

4. Open a pull request.

## 📜 License

This project is licensed under the MIT License. See the LICENSE file for more details.

Este README segue boas práticas e está pronto para ser usado no GitHub. Caso precise de personalizações ou melhorias, é só avisar! 😊

