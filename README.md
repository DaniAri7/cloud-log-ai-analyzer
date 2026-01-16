# 🛡️ AI-Powered Cloud Security Analyzer - Project Overview

[![GitHub Repo](https://img.shields.io/badge/github-repo-lightblue?logo=github)](https://github.com/DaniAri7/cloud-log-ai-analyzer)
![CI Status](https://github.com/DaniAri7/cloud-log-ai-analyzer/actions/workflows/python-app.yml/badge.svg)
![Docker](https://img.shields.io/badge/container-docker-blue)
![Python](https://img.shields.io/badge/python-3.11-yellow)
![Security](https://img.shields.io/badge/focus-Zero%20Trust-red)
[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](LICENSE)

A **Cloud-Native Security Tool** that simulates, detects, and analyzes suspicious activities in AWS CloudTrail logs using **Pandas** for data engineering and **LangChain/OpenAI** for generative AI threat analysis. Fully automated via Dockerized CI Pipeline.

Designed with a **DevOps mindset**, this project features a fully containerized architecture (Docker) and an automated CI pipeline (GitHub Actions).

---

## 🚀 Key Features

* **Mock Data Generation**: Simulates realistic AWS CloudTrail logs (JSON) with random user activities and injected security threats.
* **Data Engineering & Filtering**: Uses **Pandas** to efficiently ingest logs and apply boolean logic filters:
    * *Condition A*: Failed Console Logins.
    * *Condition B*: Access from Unauthorized IPs (Zero Trust model).
* **AI Threat Analysis**: Suspicious logs are passed to **GPT-3.5** via **LangChain** to generate a structured security report (Risk Level, Technical Analysis, Remediation).
* **Dockerized Architecture (Cloud-Native Ready)**: Runs in an isolated, lightweight `python:3.11-slim` container to guarantee reproducibility.
* **CI/CD Pipeline**: Automated testing via **GitHub Actions**, running `pytest` directly inside the Docker container to ensure environment consistency.
**Zero-Trust Filtering**: Automatic identification of unauthorized IP addresses and failed login attempts.
---

## 🛠️ Tech Stack

* **Language**: Python 3.11 (Core logic)
* **Data Processing**: Pandas (Data Analysis & Filtering)
* **AI & LLM**: LangChain, OpenAI API (AI Security Insights)
* **Containerization**: Docker (Environment Isolation)
* **Testing**: Pytest (Automated Testing)
* **CI/CD**: GitHub Actions (Pipeline)
* **Environment**: Dotenv for secret management

---

## 📂 Project Structure

```text
.
├── .github/workflows/
│   └── python-app.yml    # CI Pipeline configuration (Dockerized)
├── analyzer.py           # Main logic: Ingestion, Filtering, and AI Analysis
├── log_generator.py      # Script to generate mock AWS CloudTrail logs
├── test_analyzer.py      # Unit tests for security filtering logic
├── Dockerfile            # Instructions to build the container image
├── requirements.txt      # Python dependencies
├── .env                  # API Keys (Excluded from Git)
└── README.md             # Project 
```

## ⚡ Getting Started
* **Prerequisites**
    * Docker installed on your machine.
    * OpenAI API key (store it in a `.env` file).

* 1. Clone the repository:
        ```bash
        git clone https://github.com/DaniAri7/cloud-log-ai-analyzer.git
        ```
* 2. Set up your environment variables:
    * Create a `.env` file in the root directory to store your OpenAI API key securely. This file is automatically ignored by Git/Docker for security.
    * Add your OpenAI API key:
        ```
        OPENAI_API_KEY=your_api_key_here
        ```
## 🐳Running with Docker:
* Build the Docker image:
    This installs a minimal Python environment with the required dependencies.
    ```bash
    docker build -t cloud-security-analyzer .
    ```
* Run the container:
    ```bash
    docker run --rm --env-file .env cloud-security-analyzer
    ```
**What Happens Next?**
* The container will:
    * The app loads the `mock_logs.json` file (the default one is included in the Docker image).

    * Pandas filters the logs for threats (Failed Logins / Unknown IPs).
    * The AI analyzes the threats and prints a security report to your console.
## 🔧 Testing with Custom Logs
By default, the container analyzes the logs provided in the repo. If you want to generate and analyze new scenarios:
* **1. Generate new logs locally**
Use this command to generate a new mock_logs.json directly in your current folder using the container's logic. *(Note: We use -v to persist the generated file on your machine).*
    ```bash
    docker run --rm -v ${PWD}:/app cloud-security-analyzer python log_generator.py
    ```
* **2. Run analysis without rebuilding**: If you want to analyze different logs without rebuilding the image every time, you can 'override' the internal file with a local one using volumes:

    * **In Powershell**:
    ```bash
    docker run --rm -v ${PWD}/mock_logs.json:/app/mock_logs.json --env-file .env cloud-security-analyzer
    ```
    * **In Bash (Linux/Mac/Git Bash)**:
    ```bash
    docker run --rm -v $(pwd)/mock_logs.json:/app/mock_logs.json --env-file .env cloud-security-analyzer
    ```
    * **In Windows CMD**:
    ```bash
    docker run --rm -v %cd%/mock_logs.json:/app/mock_logs.json --env-file .env cloud-security-analyzer
    ```
## 🧪 Development & Testing (Docker)

**Running Tests (CI Simulation)**
To ensure the logic is robust, we use **Pytest**. You can run the tests exactly as the CI pipeline does, directly inside Docker:
    ```docker run --rm cloud-security-analyzer pytest
    ```
**What Happens Next?**
* Pytest will execute the tests defined in `test_analyzer.py`.
* The results will be displayed in your console, showing whether each test passed or failed.

## 🐍 Local Python - Running & Testing
Use this if you prefer working directly with your local Python environment.
* **1. Setup**
    ``` bash
    pip install -r requirements.txt
    ```
* **2. Generate & Analyze:**
    ``` bash 
    python log_generator.py
    python analyzer.py
    ```
* **3. Test Locally**
    ``` bash
    pytest
    ```

## Continuous Integration (GitHub Actions)
The project includes a **Dockerized CI Pipeline** ```(.github/workflows/python-app.yml)```. Every time code is pushed to the ```main``` branch:
* GitHub spins up an Ubuntu runner.
* It builds the Docker image from scratch.
* It runs the unit tests inside the container.

This guarantees that **if it works in CI, it works in Production.**

🧠 **Engineering Decisions**
* **Why Docker?** To solve the "it works on my machine" problem. The application runs in a pristine ```python-slim``` environment, reducing the attack surface and image size.
* **Why Pandas?** For scalability. While standard Python lists work for small logs, Pandas enables vectorised operations, making the tool ready for larger datasets.
* **Security First**: Secrets are managed via ```.env``` and never hardcoded. The ```.dockerignore``` file prevents sensitive files and virtual environments from being copied into the final image.

## 📝 License
This project is licensed under the MIT License. See the `LICENSE` file for details.
