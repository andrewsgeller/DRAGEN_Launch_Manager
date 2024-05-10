import tkinter as tk
from tkinter import ttk
from tkinter import messagebox
import logging
import os
from src.config_loader import load_config
from src.launcher import launch_pipeline, check_bs_cli, check_bs_user, get_project_id, get_biosamples_from_project, verify_dragen_version, select_biosamples_gui
import subprocess

# Set up logging
log_directory = os.path.join(os.path.dirname(os.path.dirname(__file__)), 'logs')
if not os.path.exists(log_directory):
    os.makedirs(log_directory)
log_file_path = os.path.join(log_directory, 'dragen_launcher.log')
logging.basicConfig(
    level=logging.INFO,  # Set to INFO to capture everything
    format='%(asctime)s - %(levelname)s - %(message)s',
    datefmt='%Y-%m-%d %H:%M:%S',
    handlers=[
        logging.FileHandler(log_file_path),  # File handler for all log levels
        logging.StreamHandler()  # Stream handler for ERROR level only
    ]
)
logging.getLogger().handlers[1].setLevel(logging.ERROR)  # Set console to log only ERRORs

def main():
    # Check BaseSpace CLI setup
    try:
        check_bs_cli()
        check_bs_user()
    except RuntimeError as e:
        messagebox.showerror("Setup Error", str(e))
        return  # Exit the application if the checks fail

    # GUI setup
    root = tk.Tk()
    root.title("DRAGEN Pipeline Launcher")
    root.geometry("500x400")  # Adjusted for better layout visibility

    # Variables
    run_name_var = tk.StringVar()
    pipeline_var = tk.StringVar()
    version_var = tk.StringVar()
    selected_biosamples = tk.StringVar()

    def on_submit():
        run_name = run_name_var.get()
        if not run_name:
            messagebox.showerror("Error", "Run name cannot be empty.")
            return
        
        if not version_var.get().strip() or not verify_dragen_version(version_var.get()):
            messagebox.showerror("Version Error", "DRAGEN Version not found or invalid.")
            return
        
        project_id = get_project_id(run_name)
        if project_id:
            biosamples = get_biosamples_from_project(run_name)
            if biosamples:
                selected_biosample_ids = select_biosamples_gui(biosamples, run_name)
                if selected_biosample_ids:
                    selected_biosamples.set(selected_biosample_ids)
                    launch_command(project_id)  # Pass project_id to launch_command
                else:
                    messagebox.showerror("Selection Error", "No biosamples selected.")
            else:
                messagebox.showerror("Error", "No biosamples found for the project.")
        else:
            messagebox.showerror("Error", "Invalid project ID or unable to retrieve project.")

    def preview_and_launch_command(command):
        def launch_command():
            try:
                output = subprocess.check_output(command, shell=True, text=True)
                messagebox.showinfo("Success", "Command executed successfully:\n" + output)
            except subprocess.CalledProcessError as e:
                messagebox.showerror("Error", "Failed to execute command:\n" + str(e))
            preview_window.destroy()

        def cancel_command():
            preview_window.destroy()

        # Create a top-level window for the command preview
        preview_window = tk.Toplevel(root)
        preview_window.title("Preview Command")
        preview_window.geometry("600x200")
        
        # Display the command
        ttk.Label(preview_window, text="Preview of Command to be Executed:", font=('Arial', 12)).pack(pady=10)
        command_label = ttk.Label(preview_window, text=command, font=('Arial', 10), wraplength=500)
        command_label.pack(pady=10)

        # Buttons to confirm or cancel
        ttk.Button(preview_window, text="OK", command=launch_command).pack(side='left', padx=20, pady=20)
        ttk.Button(preview_window, text="Cancel", command=cancel_command).pack(side='right', padx=20, pady=20)

        preview_window.mainloop()


    def launch_command(project_id):
        command = build_command(project_id)  # Get the command from the build_command function
        if command:
            preview_and_launch_command(command)  # Use the new function to preview and potentially execute the command
        else:
            messagebox.showerror("Error", "No command to execute. Please check the configurations.")

    def build_command(project_id):
        try:
            pipeline_config = load_config(pipeline_var.get())
            # Remove newlines and add space and backslash for shell command continuation
            formatted_command = ' '.join(pipeline_config['command'].strip().splitlines())
            formatted_command = formatted_command.replace('\n', ' \\\n').format(
                version=version_var.get(),
                run_name=run_name_var.get(),
                project_id=project_id,
                biosamples=selected_biosamples.get()
            )
            return formatted_command
        except Exception as e:
            logging.error("Failed to build the command: %s", e, exc_info=True)
            messagebox.showerror("Error", "Failed to build the command. Check logs for details.")
            return None

    # GUI Components
    ttk.Label(root, text="Run Name:").pack()
    ttk.Entry(root, textvariable=run_name_var).pack()

    ttk.Label(root, text="Select Pipeline:").pack()
    pipeline_combo = ttk.Combobox(root, textvariable=pipeline_var, values=["DRAGEN_Germline", "DRAGEN_Enrichment", "DRAGEN_RNA"], state="readonly")
    pipeline_combo.pack()

    ttk.Label(root, text="Version:").pack()
    ttk.Entry(root, textvariable=version_var).pack()

    submit_button = ttk.Button(root, text="Submit", command=on_submit)
    submit_button.pack()

    root.mainloop()

if __name__ == "__main__":
    main()
