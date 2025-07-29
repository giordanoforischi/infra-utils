# Cloud Function Deployment Helper

Interactive CLI to deploy a Google Cloud Function using `gcloud` and custom configuration prompts.

This tool simplifies the deployment of Cloud Functions by generating a `.gcloudignore`, reading environment variables from `.env`, and saving your deployment config for future use.

---

## ⚙️ Features

- Interactive prompts for region, runtime, memory, CPU, timeout, trigger type, and more
- Optional reuse of previous config (`__deployment_config.json`)
- Automatically loads `.env` variables into Cloud Function env vars
- Supports both Gen1 and Gen2 Cloud Functions
- Customizable advanced settings (RAM, CPU, min/max instances)
- Prevents accidental inclusion of sensitive files using `.gcloudignore`

---

## 🚀 Usage

1. Install dependencies (only `python-dotenv` required):
    ```bash
    pip install python-dotenv
    ```

2. Run file
    ```bash
    python cf_deploy.py
    ```