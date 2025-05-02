import subprocess
import sys
import re  # Import the regular expression module
import time

def light_tworf():
    """
    Runs the `sudo ls` command, captures its output, and extracts the
    quoted text containing "scrolllock".
    """
    try:
        process = subprocess.run(
            ["ls", "/sys/class/leds/"],  # Modified to list leds directory
            capture_output=True,
            check=True,
            text=True,
        )
        output = process.stdout
        print("Output of ls /sys/class/leds/:")
        print(output)

        # Use a regular expression to find the quoted text containing "scrolllock"
        match = re.search(r"(input\d+::scrolllock)", output)  # Refined regex

        if match:
            captured_text = match.group(1)  # Extract the captured group
            print("\nCaptured text containing 'scrolllock':")
            print(captured_text)
            captured_text = str(captured_text)
            #switches on the backlights after every 5 minutes.
            subprocess.run(
            ["brightnessctl", "set", "100%" , "-d", captured_text],
            capture_output=False,
            check=True,
            text=True,
        )
        else:
            print("\nNo text containing 'scrolllock' found in the output.")

    except subprocess.CalledProcessError as e:
        print(f"Error running sudo ls: {e}")
        print(f"Return code: {e.returncode}")
        print(f"Stderr: {e.stderr}")
        sys.exit(1)
    except FileNotFoundError:
        print("Error: sudo or ls command not found.  Make sure they are in your system's PATH.")
        sys.exit(1)
    except Exception as e:
        print(f"An unexpected error occurred: {e}")
        sys.exit(1)

def main():
    """
    Main function to run the run_sudo_ls function every 5 minutes.
    """
    while True:
        light_tworf()
        time.sleep(120)  # Sleep for 5 minutes (300 seconds)



if __name__ == "__main__":
    main()
