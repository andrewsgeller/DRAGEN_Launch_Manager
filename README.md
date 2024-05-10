# DRAGEN Launch Manager

## Overview

DRAGEN Launch Manager is a Python-based GUI application designed for launching DRAGEN Bio-IT Platform pipelines via a user-friendly interface. It simplifies the process of setting up and running genomic data analysis workflows using the BaseSpace CLI tools and the DRAGEN engines.

## Features

- **Graphical Interface:** Simplifies the execution of genomic pipelines through a graphical interface, making it accessible to users with limited command line experience.
- **Pipeline Configuration Management:** Easily manage different pipeline configurations and versions using external YAML configuration files.
- **Logging and Error Handling:** Detailed logs are maintained for troubleshooting and process verification. Errors are displayed through GUI dialogs to inform the user of any issues during the pipeline setup or execution.
- **BaseSpace CLI Checks:** Before running any pipelines, the system checks for the presence and configuration of the BaseSpace CLI and the user's authentication.

## System Requirements

- Python 3.6 or higher
- BaseSpace CLI installed and configured
- Appropriate permissions to access BaseSpace sequences and projects

## Installation

1. Clone the repository or download the source code:
   ```
   git clone https://github.com/andrewsgeller/DRAGEN_Launch_Manager.git
   cd dragen_launch_manager
   ```
2. **Install Dependencies and Set Up the DRAGEN Launch Manager**
   Use the following command in the root directory of the project to install the manager and its dependencies:
   ```
   python setup.py install
   ```

## Usage

To start the DRAGEN Launch Manager, you can use the following command after installation:

```
dragen-launcher
```

This command will open up the graphical user interface where you can:

- Specify the run name.
- Choose the desired DRAGEN pipeline from available configurations.
- Enter the version of the DRAGEN engine to use.
- Select specific biosamples to process.
- Review and launch the command to initiate the processing on the DRAGEN Bio-IT platform.

## Folder Structure

The following directory tree outlines the main components of the DRAGEN Launch Manager:

```
/DRAGEN_Launch_Manager
├── config
│   ├── DRAGEN_Enrichment_config.yaml
│   ├── DRAGEN_Germline_config.yaml
│   └── DRAGEN_RNA_config.yaml
├── logs
│   └── dragen_launcher.log
├── src
│   ├── config_loader.py
│   ├── launcher.py
│   └── main.py
└── README.md
```
`config/`: Contains YAML configuration files for different DRAGEN pipelines.

`logs/`: Stores log files which record the operations and errors for debugging.

`src/`: Contains the Python scripts for the application's functionality.

- **config_loader.py** deals with loading pipeline configurations from the YAML files.
- **launcher.py** handles the execution logic, including pre-checks and subprocess management.
- **main.py** sets up the GUI and links user inputs to pipeline execution commands.

## Contributing

Contributions to the DRAGEN Launch Manager are welcome! Please fork the repository and submit pull requests with your proposed changes. Ensure to follow the existing coding styles and add appropriate tests if applicable.

## Support and Documentation

For issues, questions, or requests for additional features, please open an issue in the project's GitHub repository. Further documentation, including detailed setup and usage instructions, can be found in the `docs` folder.

## License

This project is licensed under the terms of the MIT license. Please see the LICENSE file for full details.

---

Thank you for choosing DRAGEN Launch Manager for your genomic data processing needs! We hope this tool simplifies and enhances your bioinformatics workflows.
