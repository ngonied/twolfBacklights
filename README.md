# twolfBacklights 

#light_tworf

This script periodically checks for a specific LED device related to "scrolllock" and then attempts to set its brightness to 100%. It's designed to potentially control keyboard backlights or similar LED indicators.

## Overview

The script operates in the following steps:

1.  **Lists LED Devices:** It uses the `ls /sys/class/leds/` command to list the available LED devices on the system.
2.  **Identifies "scrolllock" Device:** It then parses the output of this command using a regular expression to find a device directory containing "scrolllock" (specifically looking for the pattern `input\d+::scrolllock`).
3.  **Sets Brightness:** If such a device is found, the script attempts to set its brightness to 100% using the `brightnessctl` command. It uses the identified device path as the `-d` (device) argument for `brightnessctl`.
4.  **Repeats Periodically:** This entire process is repeated every 2 minutes by default.

## Prerequisites

Before running this script, ensure you have the following installed and configured:

* **Python 3:** This script is written in Python 3.
* **`brightnessctl`:** This command-line tool is used to control the brightness of various devices, including LEDs. You can usually install it using your distribution's package manager (e.g., `sudo apt-get install brightnessctl` on Debian/Ubuntu, `sudo pacman -S brightnessctl` on Arch Linux, `sudo yum install brightnessctl` on Fedora/CentOS).
* **Permissions:** The script uses `subprocess.run` to execute external commands like `ls` and `brightnessctl`. Ensure that the user running this script has the necessary permissions to execute these commands, especially `brightnessctl` with the `-d` option to modify the brightness of the identified LED device.

## How to Use

1.  **Save the script:** Save the provided Python code to a file named `light_tworf.py` (or any other `.py` extension).
2.  **Make it executable (optional):** You can make the script executable using the command `chmod +x light_tworf.py`.
3.  **Run the script:** Execute the script from your terminal using `python3 light_tworf.py` or `./light_tworf.py` if you made it executable.

The script will then run in the background, periodically checking for the "scrolllock" related LED and attempting to set its brightness.

## Explanation of the Code

* **`import subprocess`:** This module allows the script to run external commands like `ls` and `brightnessctl`.
* **`import sys`:** This module provides access to system-specific parameters and functions, used here for exiting the script in case of errors.
* **`import re`:** This module provides regular expression operations for pattern matching, used to find the "scrolllock" device in the output of `ls`.
* **`import time`:** This module provides time-related functions, used here to introduce a delay between checks.
* **`light_tworf()` function:**
    * Executes `ls /sys/class/leds/` to get a list of LED devices.
    * Uses `re.search(r"(input\d+::scrolllock)", output)` to find a line containing "scrolllock" within the output. The regular expression specifically looks for a pattern like "inputX::scrolllock" where X is a digit.
    * If a match is found, it extracts the device name and uses `subprocess.run` to execute `brightnessctl set 100% -d <device_name>` to set the brightness.
    * Includes error handling for `subprocess.CalledProcessError` (when an external command fails), `FileNotFoundError` (if `ls` or `brightnessctl` are not found), and other general exceptions.
* **`main()` function:**
    * Contains an infinite `while True` loop to continuously execute the `light_tworf()` function.
    * Uses `time.sleep(120)` to pause for 2 minutes (120 seconds) between each execution.
* **`if __name__ == "__main__":`:** This ensures that the `main()` function is called only when the script is executed directly.

## Potential Issues and Considerations

* **`brightnessctl` availability and permissions:** The script relies on `brightnessctl` being installed and the user having the necessary permissions to control the identified LED device.
* **"scrolllock" device naming:** The script assumes the "scrolllock" related LED device will follow the pattern `input\d+::scrolllock`. This might vary depending on the system and hardware. You might need to adjust the regular expression if your system uses a different naming convention.
* **Error handling:** The script includes basic error handling, but you might want to add more robust logging or error reporting.
* **Resource usage:** While the script sleeps for 2 minutes between checks, continuously running background processes can consume system resources. Consider adjusting the sleep interval if needed.
* **No guarantee of "scrolllock" controlling backlight:** The script assumes that an LED device containing "scrolllock" in its name is related to keyboard backlights. This might not always be the case.
* **Root privileges:** Depending on how LED brightness control is implemented on your system, you might need to run this script with root privileges (e.g., using `sudo`). However, the current script does not explicitly use `sudo` for `brightnessctl`. If you encounter permission issues, you might need to adjust how `brightnessctl` is executed or configure appropriate permissions.

## Customization

* **Sleep interval:** You can change the frequency of the checks by modifying the value in `time.sleep(120)` in the `main()` function. The value is in seconds.
* **Brightness level:** You can change the brightness level set by modifying `"100%"` in the `brightnessctl` command within the `light_tworf()` function.
* **Regular expression:** If your system uses a different naming convention for the "scrolllock" LED, you'll need to adjust the regular expression `r"(input\d+::scrolllock)"` in the `light_tworf()` function. You can inspect the output of `ls /sys/class/leds/` on your system to determine the correct pattern.