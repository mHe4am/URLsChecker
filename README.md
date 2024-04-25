
# URLsChecker
Python script to validate URLs, identifying valid and invalid/forbidden links.


## Description

A high-speed Python script designed for lightning-fast URL validation. Utilizing concurrent processing, it swiftly verifies URLs while maintaining a structured output. Accessible via command line interface (CLI), it seamlessly operates across various platforms. Ideal for efficiently managing URL integrity tasks with speed and precision.



## Why/When to Use?

When you want to check on a list of URLs and filter the valid, invalid, and forbidden URLs.



## Prerequisites
- Python 3.7 or higher is recommended.
- Required libraries:
	- argparse
	- asyncio
	- aiohttp
- Operating System: Cross-platform compatible.


## Installation & Usage

- Open CMD and run `git clone https://github.com/mHe4am/URLsChecker.git` to download the script.
- Run `pip install -r /YOUR_FULL_PATH_HERE/requirements.txt` to install the dependencies.
> Replace **YOUR_FULL_PATH_HERE** with the script full path.
- Run `URLsChecker.py -u urls_file.txt -o output_file.txt -sep "," -v`


## Tip

Add the script to your **Environment Variables** in Windows to run it from anywhere without having to go to the script directory.  
#### Steps to add it:
1. Search for **Environment Variables** and click on **Edit the system environment variables**.  
2. Click on **Environment Variables...** at the bottom.  
3. Under System Variables, find the `Path` variable, select it, and click on **Edit**.  
4. In the Edit window, you can add the path to your script by clicking on `New` and then adding the full path to the script folder. For example, you would add `C:\Scripts` if your script is in `C:\Scripts`.


## Contributing
Contributions are welcome! Please feel free to submit a pull request.