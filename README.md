# DiskPurge - Storage Analyzer

#### Video URL: https://youtu.be/MnEj69c3DB8

#### Description:
**DiskPurge** is a lightweight, command-line storage profile engine written in Python. It is designed to recursively crawl complex file systems, identify storage-hogging files, aggregate space utilization metrics by file extensions, and provide an interactive terminal interface for safe data cleanup.

The primary motivation behind DiskPurge was to create a functional alternative to storage analysis applications, optimized entirely to analyze large directories in both CLI-mode (for tech bros) and GUI-mode.
---

### Architectural Design Choices

#### 1. Core Engine Isolation (`analyzer/core.py`)
To adhere strictly to professional software separation of concerns, the fundamental data collection logic is entirely separated from the user interface presentation layer.
* **The Generator Pattern (`directory_scanner`):** Standard directory traversal routines typically build and store giant lists of all paths directly in system RAM. DiskPurge solves this scale constraint by utilizing Python's `yield` keyword. It processes the files lazily, passing file path strings and raw byte sizes over a clean iterable interface stream. This guarantees optimal performance even when processing massive external hard drives containing hundreds of thousands of files.
* **Pure Mathematical Manipulation:** Functions responsible for formatting structural data, sorting file arrays (`largest_files`), and grouping dictionary components (`extension_breakdown`) utilize pure inputs and return strict structures without side effects (`print` or `input` calls), making the core backend flawlessly modular.

#### 2. Modular Presentation Layer (`project.py`)
Following the rules of the CS50P automated grader framework, the application's main entry script orchestrates processing steps through concise, specialized helper functions.
* **`scanner`**: Safely consumes the underlying custom generator, converting streamed bytes into managed evaluation lists while safely catching file path anomalies.
* **`display_largest_files`**: Transforms the heaviest system files into clear grid metrics using the third-party `tabulate` library by passing data through the core sorting algorithm.
* **`display_extension_breakdown`**: Normalizes hidden file extensions to lowercase syntax, classifies files missing extension patterns under a clean generic label, and tracks global space consumer trends.
* **`auto_clean`**: An interactive sequence that decodes human-readable selection numbers into zero-indexed file deletions, safely verifying existence flags before invoking file removal tasks.

---

### File Structure Overview

* **`project.py`**: The central application controller. Houses the terminal startup banner flow, command-line sequencing functions (`scanner`, `display_largest_files`, `display_extension_breakdown`), and the user interactive deletion loop.
* **`analyzer/`**: A tracking package subdirectory defining internal operations.
  * **`__init__.py`**: Initializes the analyzer directory namespace as an importable module packet.
  * **`core.py`**: The raw mathematics and file-system crawler workshop. Houses path normalization mechanisms, string converter formulas, the `largest_files` sorting logic, and the `directory_scanner` generator stream.
* **`test_project.py`**: Full unit test layout implemented via `pytest`. Confirms core component stability, tests exception-throwing pathways, and handles multi-tier tracking array verifications.
* **`requirements.txt`**: Declares external library targets (`tabulate`, `pyfiglet`, `pytest`).

---

### Setup and Testing Instructions

To run the software application locally or inside a virtual cloud container:
1. Initialize package assets via pip dependencies:
   
   pip install -r requirements.txt

2.1 Execute the primary controller file to begin storage tracking in CLI-mode:
    
    python project.py

2.2 Execute the primary controller file to begin storage tracking in GUI-mode:

    python gui.py

3. Run the automated verification test suites:
    
    pytest test_project.py
