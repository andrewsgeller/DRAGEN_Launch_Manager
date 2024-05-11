# DRAGEN Launch Manager

## Overview
DRAGEN Launch Manager is a Python-based GUI application designed for launching DRAGEN Bio-IT Platform pipelines via a user-friendly interface. It simplifies the process of setting up and running genomic data analysis workflows using the BaseSpace CLI tools and the DRAGEN engines.

## Features
- **Graphical Interface:** Simplifies the execution of genomic pipelines through a graphical interface, making it accessible to users with limited command line experience.
- **Pipeline Configuration Management:** Users can manage and customize different pipeline configurations using external YAML files.
- **Custom Configuration Setup:** Allows users to create personalized pipeline configurations by editing templates and defining parameters based on their specific requirements.
- **Logging and Error Handling:** Detailed logs are maintained for troubleshooting and process verification. Errors are displayed through GUI dialogs to inform the user of any issues during the pipeline setup or execution.
- **BaseSpace CLI Checks:** Before running any pipelines, the system checks for the presence and configuration of the BaseSpace CLI and the user's authentication.

## System Requirements
- Python 3.6 or higher
- BaseSpace CLI installed and configured
- Appropriate permissions to access BaseSpace sequences and projects

## Installation
1. Clone the repository or download the source code:
    ```bash
    git clone https://github.com/andrewsgeller/DRAGEN_Launch_Manager.git
    cd dragen_launch_manager
    ```
2. Install dependencies and set up the DRAGEN Launch Manager:
    ```arduino
    python setup.py install
    ```

## Configuration Setup
After installation, users must create their own configuration files:
1. Navigate to the `config/launch_sets` directory and choose the appropriate template YAML file for the desired pipeline.
2. Copy the selected template and edit it to specify custom settings based on your requirements.
3. Save the customized configuration file into the `params` directory, removing the "template_" prefix from the file name.
   - You can reference the `config/launch_options` directory to view detailed descriptions and allowable settings for each pipeline option.

## Usage
To start the DRAGEN Launch Manager, run:
```bash
dragen-launcher
```

This command opens the graphical interface where you can:

- Specify the run name.
- Choose the desired DRAGEN pipeline from the configurations you have set up.
- Enter the version of the DRAGEN engine to use.
- Select specific biosamples to process.
- Review and launch the command to initiate processing on the DRAGEN Bio-IT platform.

## Folder Structure

/DRAGEN_Launch_Manager
├── config
│   ├── launch_options
│   │   ├── dragen_enrichment_command_options.yaml
│   │   ├── dragen_germline_command_options.yaml
│   │   └── dragen_rna_command_options.yaml
│   └── launch_sets
│       ├── template_DRAGEN_Enrichment_config.yaml
│       ├── template_DRAGEN_Germline_config.yaml
│       └── template_DRAGEN_RNA_config.yaml
├── docs
├── params
│   ├── DRAGEN_Enrichment_config.yaml
│   ├── DRAGEN_Germline_config.yaml
│   └── DRAGEN_RNA_config.yaml
├── logs
│   └── dragen_launcher.log
├── src
│   ├── config_loader.py
│   ├── launcher.py
│   └── main.py
├── README.md
└── setup.py

## Contributing
Contributions to the DRAGEN Launch Manager are welcome! Please fork the repository and submit pull requests with your proposed changes. Ensure to follow the existing coding styles and add appropriate tests if applicable.

## Support and Documentation
For issues, questions, or requests for additional features, please open an issue or email me at andrew.geller@cei.eurofinsus.com

## License
This project is licensed under the terms of the MIT license. Please see the LICENSE file for full details.
