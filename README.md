# Effective Penetration Testing tools
A collection of tools that can be used to test for potential security flaws in your systems.

Install dependencies by running `pip install -r requirements.txt` in your console

## Contents
* [Disclaimer](#disclaimer)
* Reconnaissance tools
  * [Port Scanner](#port-scanner)
  * [Web Path Finder](#web-path-finder)
  * [Web Fingerprint](#web-fingerprint)

## Port Scanner
Supports Multi-threading, Windows and Linux OS, user-friendly. Shows open ports in desired range of any hostname/ip inputted

#### Usage:
Run the script in your console by writing `python myPortScanner.py`
Then input the required parameters

## Web Path Finder
Extracts all links from a website.

Can also search for hidden paths using `defaultPathWordlist.txt`. However, beware that brute-forcing directories and files names on deployed servers is ILLEGAL and can get you in trouble.

#### Usage:
Run the script in your console by writing `python myWebPathFinder.py`
Then input the required parameters

## Web Fingerprint
Work in progress. Finds technologies and headers used in a website.

#### Usage:
Run the script in your console by writing `python WebFingerprint.py`
Then input the required parameters


# Disclaimer
All information and code available in this repository are for educational purposes only. Use them at your own discretion. The authors of this repository cannot be held responsible for any damages caused or illegal usage of the information given.