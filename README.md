# Aggressor Aggregator

## Description

A helper script for consolidating Aggressor Script and Beacon Object File (BOF) repositories into a single CNA for Cobalt Strike. Designed for automation in red team CTF environments with frequent setup/destruction of operator clients. This script is essentially a wrapper around the [_Cobalt Strike Aggressor Scripts-Ception_](https://amonsec.net/posts/2020/07/00000004/) blog post by [@am0nsec](https://twitter.com/am0nsec). Tested on Windows 10, Linux and macOS.

## Usage

1. Clone this repository
2. Create a text file with your favourite BOF/Aggressor repository URLs (or individual `.cna` URLs)
3. Run the Python script with the given text file `--file <list>`
4. Import the generated `loader.cna` via the script console

## Example

```shell
$ python3 ./aggressor-aggregator.py --file favourites.txt
```

![img1](https://github.com/sudonoodle/Aggressor-Aggregator/assets/52385049/dd082399-c3da-4493-84ee-ea5b7ec44a22)
![img2](https://github.com/sudonoodle/Aggressor-Aggregator/assets/52385049/e36e95c6-c331-49c2-b811-e5754d86c11d)

## Credits

- Paul L. ([@am0nsec](https://twitter.com/am0nsec)) for `loader.cna` ([_Cobalt Strike Aggressor Scripts-Ception_](https://amonsec.net/posts/2020/07/00000004/))
- [@bottersnike](https://github.com/Bottersnike) and [@javalogicuser](https://github.com/javalogicuser) for QA and testing
