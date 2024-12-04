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

    #### NewStreamlitApp/
    ├── app.py                # Main application file
    ├── auth/
    │   └── login.py          # Authentication logic
    ├── db.py                 # SQLite database     
    
    #### connection and helpers
    ├── nav.py                # Navigation settings
    ├── page/
    │   ├── home.py           # Home page
    │   ├── management.py     # Management page
    │   ├── architecture.py   # Architecture page
    │   └── development.py    # Development page
    ├── sessions/
    │   └── state.py          # Session management 
    
    #### logic
    ├── requirements.txt      # Python dependencies
    ├── app.db                # SQLite database 
    └── .streamlit/           # Streamlit configuration 
    


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