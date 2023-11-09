import os


def read_files_and_append(output_file, separator):
    # Open the output file for appending
    with open(output_file, "a", encoding="utf-8") as output:
        # Walk through all files in the current directory and its subdirectories
        for foldername, subfolders, filenames in os.walk("."):
            for filename in filenames:
                # Get the full path to the file
                file_path = os.path.join(foldername, filename)

                # Get the relative path to the file
                relative_path = os.path.relpath(file_path, ".")

                # Write the separator and relative path to the output file
                if not relative_path.startswith(".git\\") and not filename.startswith("entrega_geral.txt"):
                    output.write(f"{separator} {relative_path} {separator}\n")

                # Read the content of the file and append it to the output file
                if not filename.endswith("sqlite3") \
                    and not filename.endswith("md") \
                    and not filename.endswith("lock.json") \
                    and not filename.startswith("entrega_geral.txt") \
                    and not filename.startswith("gerar_txt_entrega") \
                    and not relative_path.startswith(".git\\"):
                    with open(file_path, "r", encoding="utf-8") as file:
                        output.write(file.read())

                # Add an extra newline for better separation between files
                if not relative_path.startswith(".git\\") and not filename.startswith("entrega_geral.txt"):
                    output.write("\n\n")


if __name__ == "__main__":
    output_file = "entrega_geral.txt"
    separator = "*****"

    # Clear the existing content of the output file
    open(output_file, "w").close()

    # Call the function to read files and append to the output file
    read_files_and_append(output_file, separator)

    print(f"Files successfully read and appended to {output_file}.")
