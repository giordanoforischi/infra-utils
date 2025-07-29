import os
import subprocess
import shutil
import json
from dotenv import dotenv_values

CONFIG_FILENAME = '__deployment_config.json'
SEP_STR = '----------------------------------- \n'
IGNORE_STRING = """**/__pycache__
**/_pycache_
**/env
**/venv
**/node_modules
**/__deployment_config.json
**/.env
**/*.ipynb
**/cf_deploy.py
**/.gitignore
"""

def choose_option(options, prompt, default=None):
    while True:
        print(f'{SEP_STR}{prompt}\n')
        for i, option in enumerate(options, start=1):
            print(f"{i}. {option}")

        try:
            default_string = f' (DEFAULT={default})' if default is not None else ''
            choice = input(f"\nSelect an option by entering the corresponding number{default_string}: ")
            if not choice and default is not None:
                return default
            choice_idx = int(choice) - 1
            return options[choice_idx]
        except (ValueError, IndexError):
            print("Invalid input. Please enter a valid option number.")

def confirm_deployment(params):
    print(f"{SEP_STR}Deployment Summary:")
    for key, value in params.items():
        print(f"{key.capitalize()}: {value}")

    confirm = input("\nDo you want to deploy? Your gcloud CLI project will be set to the selected project. (yes/no, default=yes): ").lower()
    confirm = confirm if confirm in ['yes', 'no'] else 'yes'
    return confirm == 'yes'

def execute_deployment(params):
    gcloud_path = shutil.which('gcloud')
    if gcloud_path is None:
        print("Error: 'gcloud' executable not found.")
        return

    command = [gcloud_path, 'functions', 'deploy', params['function_name']]
    command.extend([
        '--region', params['region'],
        '--runtime', params['runtime'],
        '--entry-point', params['entry_point'],
        '--verbosity', 'debug',
        f'--trigger-{params["trigger"]}',
        '--source', './'
    ])

    if params['trigger_id']:
        command.append(params['trigger_id'])

    if params['gen_version'] == 'gen2':
        command.append('--gen2')

    if params['service_account']:
        command.extend(['--service-account', params['service_account']])

    if params['allow_unauthenticated']:
        command.append('--allow-unauthenticated')

    # Advanced settings
    command.extend([
        '--memory', params.get('ram', '512MB'),
        '--cpu', params.get('cpu', '1'),
        '--timeout', params.get('timeout', '60s'),
        '--min-instances', params.get('min_instances', '0'),
        '--max-instances', params.get('max_instances', '1')
    ])

    # Environment variables
    for key, value in params.get('env_vars', {}).items():
        command.extend(['--set-env-vars', f'{key}={value}'])

    subprocess.run(command)

def save_config(params, config_file):
    with open(config_file, 'w') as f:
        json.dump(params, f)

def load_config(config_file):
    if os.path.exists(config_file):
        with open(config_file, 'r') as f:
            return json.load(f)
    return None

def create_gcloudignore(current_dir):
    ignore_file_path = os.path.join(current_dir, ".gcloudignore")
    with open(ignore_file_path, "w") as f:
        f.write(IGNORE_STRING)

def main():
    current_dir = os.path.dirname(os.path.abspath(__file__))
    config_file = os.path.join(current_dir, CONFIG_FILENAME)

    existing_config = load_config(config_file)
    
    if existing_config:
        use_existing = input("A configuration file exists. Do you want to use the existing settings? (yes/no): ")
        if use_existing.lower() == 'yes':
            params = existing_config
            # Set defaults for new fields
            params.setdefault('ram', '512MB')
            params.setdefault('cpu', '1')
            params.setdefault('timeout', '60s')
            params.setdefault('min_instances', '0')
            params.setdefault('max_instances', '1')
        else:
            params = create_new_config(current_dir, config_file)
    else:
        params = create_new_config(current_dir, config_file)

    if confirm_deployment(params):
        gcloud_path = shutil.which('gcloud')
        if gcloud_path is None:
            print("Error: 'gcloud' executable not found.")
            return

        check_access_command = [gcloud_path, 'projects', 'describe', params['project_id']]
        access_check_result = subprocess.run(check_access_command, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
        if access_check_result.returncode != 0:
            print("Error: You don't seem to have access to the selected project. Please try again.")
            return

        change_project_command = [gcloud_path, 'config', 'set', 'project', params['project_id']]
        subprocess.run(change_project_command)

        create_gcloudignore(current_dir)
        execute_deployment(params)
        save_config(params, config_file)

def create_new_config(current_dir, config_file):
    project_id = input("Enter the GCP project ID: ")

    function_name = input("Enter the function name: ")

    region_choices = ['us-central1', 'us-east1', 'us-east4', 'southamerica-east1', 'southamerica-west1', 'europe-west1']
    default_region = 'us-central1'
    region = choose_option(region_choices, "Available regions:", default=default_region)

    runtime_choices = ['python37', 'python38', 'python39', 'python310', 'python311', 'nodejs14', 'nodejs16', 'nodejs18', 'nodejs20']
    runtime = choose_option(runtime_choices, "Available runtimes:")

    gen_version = choose_option(['gen1', 'gen2'], "Select the generation:", default='gen2')

    trigger_choices = ['http', 'topic', 'bucket']
    default_trigger = 'http'
    trigger = choose_option(trigger_choices, "Enter the trigger type:", default=default_trigger)

    trigger_id = None
    if trigger in ['topic', 'bucket']:
        trigger_id = input(f"Enter the {trigger} ID: ")

    entry_point = input(f"{SEP_STR}Enter the entry point function name (default: main): ")
    if not entry_point:
        entry_point = "main"

    service_account = input(f"{SEP_STR}Enter the service account (press Enter to use default Cloud Function service account): ")

    allow_unauthenticated = input(f"{SEP_STR}Allow unauthenticated invocations? (yes/no, default=yes): ").lower()
    allow_unauthenticated = allow_unauthenticated if allow_unauthenticated in ['yes', 'no'] else 'yes'

    transpose_env = input(f"{SEP_STR}Do you want to transpose .env variables to Cloud Function environment variables? (yes/no, default=yes): ").lower()
    transpose_env = transpose_env if transpose_env in ['yes', 'no'] else 'yes'

    print(f"{SEP_STR}Advanced settings (press Enter to use defaults):")
    ram = input("RAM (default: 512MB): ") or "512MB"
    cpu = input("CPU (default: 1): ") or "1"
    timeout = input("Timeout (default: 60s): ") or "60s"
    min_instances = input("Min instances (default: 0): ") or "0"
    max_instances = input("Max instances (default: 1): ") or "1"

    params = {
        'project_id': project_id,
        'function_name': function_name,
        'region': region,
        'runtime': runtime,
        'gen_version': gen_version,
        'entry_point': entry_point,
        'trigger': trigger,
        'trigger_id': trigger_id,
        'service_account': service_account if service_account else None,
        'allow_unauthenticated': allow_unauthenticated == 'yes',
        'transpose_env': transpose_env == 'yes',
        'env_vars': {},
        'ram': ram,
        'cpu': cpu,
        'timeout': timeout,
        'min_instances': min_instances,
        'max_instances': max_instances
    }

    dotenv_path = os.path.join(current_dir, '.env')
    if transpose_env == 'yes' and os.path.exists(dotenv_path):
        dotenv_vars = dotenv_values(dotenv_path)
        params['env_vars'] = dotenv_vars

    return params

if __name__ == '__main__':
    main()
