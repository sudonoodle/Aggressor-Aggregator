#!/usr/bin/python3
# Name: Aggressor-Aggregator.py
# Author: @infosecnoodle
# Date: 11/04/2024

import os
import argparse
import requests
import subprocess

class Interface:
    @staticmethod
    def info(message: str):
        print("[i]", message)

    @staticmethod
    def warn(message: str):
        print("\033[93m[!]", message + "\033[0m")

    @staticmethod
    def bad(message: str):
        print("\033[91m[-]", message + "\033[0m")

    @staticmethod
    def good(message: str):
        print("\033[92m[+]", message + "\033[0m")

def aggregateRepos(url: str) -> list[str]:
    cnas: list[str] = []
    if url.endswith(".cna"):
        response = requests.get(url)
        cna_path = os.path.abspath(os.path.basename(url))
        with open(cna_path, "wb") as file:
            file.write(response.content)
        cnas.append(cna_path)
        Interface.good(cna_path)

        return cnas

    try:
        # Clone the repo if the URL is not pointing to a .cna file
        subprocess.run(["git", "clone", "--quiet", url], check=True)
    except subprocess.CalledProcessError:
        Interface.bad(f"Failed to clone {url}")
        return []

    repo_name = os.path.basename(url.rstrip("/"))

    for root, _, files in os.walk(repo_name):
        for file in files:
            if file.endswith(".cna"):
                cna_path = os.path.abspath(os.path.join(root, file))
                cnas.append(cna_path)
                Interface.good(cna_path)
    if not cnas:
        Interface.bad("No CNA file")
        return []

    found_binary = False
    for root, _, files in os.walk(repo_name):
        for file in files:
            if file.endswith(".dll") or file.endswith(".o"):
                binary_path = os.path.abspath(os.path.join(root, file))
                found_binary = True
                Interface.info(binary_path)
    if not found_binary:
        Interface.warn("No compiled object files were found. (.dll or .o)")
        Interface.warn("You may need to compile manually or check releases before use.")

    return cnas

def generateLoader(cna_list: list[str]) -> None:
    print("")
    Interface.info("Writing to loader.cna...")
    scripts_to_load = "@scripts_to_load = @(\n"
    for cna in cna_list:
        cna_path = os.path.normpath(cna.strip())
        # Format path for Windows
        if os.name == "nt":
            cna_path = cna_path.replace(os.sep, os.sep * 2)
        scripts_to_load += f'        "{cna_path}",\n'
    scripts_to_load += ");"

    # https://amonsec.net/posts/2020/07/00000004/
    with open("loader.cna", "r") as f:
        content = f.read()
    start_index = content.find("@scripts_to_load = @(")
    end_index = content.find(");", start_index) + 2
    modified_content = content[:start_index] + scripts_to_load + content[end_index:]

    # Write the modified content back to loader.cna
    with open("loader.cna", "w") as f:
        f.write(modified_content)

    loader_path = os.path.abspath("loader.cna")
    Interface.info("Paste in Script Console:")
    print("")
    print("load " + loader_path)
    print("")

def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument(
        "--file",
        help="Specify a text file containing a list of repository URLs, one per line.",
    )
    args = parser.parse_args()

    if not args.file:
        Interface.info("Please specify a file of URLs.")
        return

    all_cnas: list[str] = []
    with open(args.file) as file:
        urls = file.readlines()
        for url in urls:
            url = url.strip()

            print("")
            Interface.info(url)
            cnas = aggregateRepos(url)
            all_cnas.extend(cnas)
    generateLoader(all_cnas)

if __name__ == "__main__":
    main()
