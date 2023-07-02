# Project ENA upload

This keeps track of all commands used to upload OceanOmics data to ENA. 

## Dataset structure

- All inputs (i.e. building blocks from other sources) are located in
  `inputs/`.
- All custom code is located in `code/`. It's one folder per upload.


# How to run this

Each project is one folder. It's easiest to copy an entire folder and then change details.

- 0-project: change the project alias and details in 0-study, then submit via curl and redirect to RESULTS.xml
- 0-project/umbrella_change: add the returned BioProject ID to the list and submit via curl
- 1-samples: change the Python code to your file directories and samples, run the Python code, and submit via curl and write what's returned to RESULTS.xml
- 2-runs: it takes a few hours for samples and BioProject ID to become public. In the meantime, check the CHANGEME lines in the Python script and change them. Submit via curl, write results to RESULTS.xml.
- Done!
