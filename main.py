# main.py


import os
import subprocess
import sys


def decompile_apk(apk_path):
    apk_path = os.path.abspath(apk_path)

    if not os.path.isfile(apk_path):
        print(f"ERROR: APK file not found: {apk_path}")
        return False

    if not apk_path.lower().endswith(".apk"):
        print("ERROR: File must be an APK.")
        return False

    apk_name = os.path.splitext(os.path.basename(apk_path))[0]
    output_dir = os.path.join(
        os.getcwd(),
        f"decompiled_{apk_name}"
    )

    print("=" * 60)
    print("APK Decompiler")
    print("=" * 60)
    print(f"APK    : {apk_path}")
    print(f"Output : {output_dir}")
    print("=" * 60)

    command = [
        "apktool",
        "d",
        apk_path,
        "-o",
        output_dir,
        "-f"
    ]

    try:
        subprocess.run(command, check=True)

        if not os.path.isdir(output_dir):
            print("ERROR: Output directory was not created.")
            return False

        print("\nSUCCESS!")
        print(f"Decompiled APK: {output_dir}")

        print("\nOutput files:")
        for root, dirs, files in os.walk(output_dir):
            level = root.replace(output_dir, "").count(os.sep)
            indent = "    " * level
            print(f"{indent}{os.path.basename(root)}/")

            for filename in files:
                print(f"{indent}    {filename}")

        return True

    except FileNotFoundError:
        print("ERROR: apktool was not found.")
        return False

    except subprocess.CalledProcessError as error:
        print(f"ERROR: apktool failed. Exit code: {error.returncode}")
        return False


def main():
    if len(sys.argv) < 2:
        print("Usage:")
        print("python main.py my_app.apk")
        sys.exit(1)

    apk_path = sys.argv[1]

    if not decompile_apk(apk_path):
        sys.exit(1)


if __name__ == "__main__":
    main()

