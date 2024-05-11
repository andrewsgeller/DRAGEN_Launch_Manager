# launcher.py
import subprocess
import logging
import tkinter as tk
from tkinter import ttk


def check_bs_cli():
    try:
        version_output = subprocess.check_output("bs --version", shell=True, text=True)
        logging.info("BaseSpace CLI version: " + version_output.strip())
    except subprocess.CalledProcessError:
        logging.error("Failed to verify BaseSpace CLI version.")
        raise RuntimeError("BaseSpace CLI is not installed or not configured correctly.")

def check_bs_user():
    try:
        user_output = subprocess.check_output("bs whoami", shell=True, text=True)
        logging.info("BaseSpace CLI user info: " + user_output.strip())
    except subprocess.CalledProcessError:
        logging.error("Failed to verify BaseSpace CLI user.")
        raise RuntimeError("Unable to verify BaseSpace CLI user. Check if you have the necessary permissions.")

def verify_base_space_checks():
    try:
        check_bs_cli()
        check_bs_user()
        return "BaseSpace checks complete."
    except RuntimeError as error:
        return f"BaseSpace checks failed: {error}"

def verify_dragen_version(version):
    cmd = f"bs launch application -n 'DRAGEN Enrichment' --app-version {version} --list"
    try:
        output = subprocess.check_output(cmd, shell=True, text=True)
        if "+" in output:  # Checks if table-like structure is present
            return True
        return False
    except subprocess.CalledProcessError:
        return False
    
def get_project_id(run_name):
    cmd = f"bs get project --name {run_name} --terse"
    try:
        output = subprocess.check_output(cmd, shell=True, text=True).strip()
        return output
    except subprocess.CalledProcessError as e:
        logging.error(f"Error retrieving ProjectID for run-name {run_name}: {e}", exc_info=True)
        return None

def get_biosamples_from_project(run_name):
    cmd = f"bs list biosamples --project-name={run_name}"  # Using run_name instead of project_id
    try:
        output = subprocess.check_output(cmd, shell=True, text=True)
        return parse_biosamples(output)
    except subprocess.CalledProcessError as e:
        logging.error(f"Error retrieving biosamples for project {run_name}: {e}", exc_info=True)
        return []

def parse_biosamples(output):
    biosamples = []
    for line in output.splitlines()[3:]:  # Assuming header and two lines of dividers
        parts = line.split('|')
        if len(parts) >= 6:
            name = parts[1].strip()
            id = parts[2].strip()
            biosamples.append((name, id))
    return biosamples

def launch_pipeline(command):
    if not command:
        logging.error("No command provided for launching.")
        return
    try:
        output = subprocess.check_output(command, shell=True, text=True)
        logging.info(f"Pipeline launched successfully: {output}")
        return output
    except subprocess.CalledProcessError as e:
        logging.error(f"Error launching pipeline: {e}", exc_info=True)
        return None
    
def select_biosamples_gui(biosamples, run_name):
    selected_samples = []

    window = tk.Toplevel()
    window.title(f"Select Biosamples {run_name} to Launch DRAGEN Pipeline")
    window.geometry("600x400")
    window.resizable(True, True)

    # Apply consistent styling
    style = ttk.Style(window)
    style.configure('TLabel', font=('Arial', 12), background='white')
    style.configure('TEntry', font=('Arial', 12), padding=5)
    style.configure('TButton', font=('Arial', 12))
    style.configure('TCheckbutton', font=('Arial', 12))
    style.theme_use('clam')  # Apply a theme for a better visual appearance

    def select_all():
        is_select_all = select_all_var.get()
        for var in checkbox_vars:
            var.set(is_select_all)

    select_all_var = tk.BooleanVar(value=False)
    select_all_button = ttk.Checkbutton(window, text="Select All", variable=select_all_var, onvalue=True, offvalue=False, command=select_all, style='TCheckbutton')
    select_all_button.pack(anchor=tk.W, padx=10, pady=5)

    scrollable_frame = ttk.Frame(window)
    canvas = tk.Canvas(scrollable_frame)
    scrollbar = ttk.Scrollbar(scrollable_frame, orient="vertical", command=canvas.yview)
    canvas.configure(yscrollcommand=scrollbar.set)
    scrollbar.pack(side=tk.RIGHT, fill=tk.Y)
    canvas.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)
    frame = ttk.Frame(canvas)
    canvas.create_window((0, 0), window=frame, anchor="nw")

    checkbox_vars = []
    for biosample in biosamples:
        var = tk.BooleanVar(value=False)
        checkbox = ttk.Checkbutton(frame, text=f"{biosample[0]} (ID: {biosample[1]})", variable=var, style='TCheckbutton')
        checkbox.pack(anchor=tk.W, padx=10, pady=2)
        checkbox_vars.append(var)

    def confirm_selection():
        selected_samples.clear()
        for i, var in enumerate(checkbox_vars):
            if var.get():
                selected_samples.append(biosamples[i][1])
        window.destroy()

    confirm_button = ttk.Button(window, text="OK", command=confirm_selection, style='TButton')
    confirm_button.pack(side=tk.BOTTOM, pady=10)

    frame.bind("<Configure>", lambda e: canvas.configure(scrollregion=canvas.bbox("all")))
    scrollable_frame.pack(fill=tk.BOTH, expand=True, padx=10, pady=5)

    window.wait_window()
    return ','.join(selected_samples)