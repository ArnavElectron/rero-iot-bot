# Entrypoint
# Runs ./user.py inside a subprocess with a global timeout

# TODO : integrate kill switch

# Imports
import subprocess


def main():

    try:
        result = subprocess.run(
            ["python", "user.py"],
            stdout=subprocess.PIPE,
            stderr=subprocess.PIPE,
            text=True,
            timeout=300,
        )

        if result.returncode == 0:
            print("Script ran successfully.")
            print("Output:", result.stdout)
        else:
            print(f"Script exited with return code {result.returncode}.")
            print("Error Output:", result.stderr)

    except subprocess.TimeoutExpired:
        print("The script took too long and was terminated.")

    except subprocess.CalledProcessError as e:
        print(f"CalledProcessError: {e}")
        print(f"Script Output: {e.output}")
        print(f"Script Error: {e.stderr}")

    except Exception as e:
        print(f"An unexpected error occurred: {e}")


if __name__ == "__main__":
    main()
