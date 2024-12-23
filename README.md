# Xmas Application 🎄

This Python application processes CSV files to perform specific operations and writes the results to an output directory. The program is containerized using Docker, making it easy to run in any environment.

---

## Prerequisites

Before running the program, ensure the following directory structure is set up in the location where you execute the commands:

### Required Directories

1. **`data/`**: Contains input files required by the program. Ensure this folder includes:
   - `payments_1.csv`
   - `providers_1.csv`
   - `ex_rates.csv`

2. **`result/`**: This folder will store the output generated by the application.

---

## Running the Program

### Method 1: Build and Run the Docker Image Locally

1. **Clone the repository** (if not already done):
   ```bash
   git clone https://github.com/AlexandrZiminov/HACK_XMAS_TEAM_AIG
   cd <repository-folder>
   
2. **Build the Docker Image:**
   ```bash
   docker build -t my-python-app .
   
3. **Run the Docker Container:**
   ```bash
   docker run -it --rm \
    -v $(pwd)/data:/app/data \
    -v $(pwd)/result:/app/result \
    my-python-app
   
### Method 2: Use Prebuilt Docker Image from Docker Hub

1. **Run the Docker Container:**
   ```bash
   docker run -it --rm \
    -v $(pwd)/data:/app/data \
    -v $(pwd)/result:/app/result \
    alexandrziminov/xmas:latest

## Notes

1. **Ensure Required Files are Present**:
     - The `data/` directory must include:
     - `payments_1.csv`
     - `providers_1.csv`
     - `ex_rates.csv`

2. **Output Directory**:
   - The results will be written to the `result/` directory.

3. **Cross-Platform Usage**:
   - If running on **Windows**, replace `$(pwd)` with the full path to the current directory.
