# Alexa Cookied

My bachelor's project in Universitat Politécnica de Barcelona (UPC).
It is a PoC tool that given the cookies from a user that logged in Alexa webpage outputs personal information of him.

## Getting Started

These instructions will get you a copy of the project up and running on your local machine for development and testing purposes.
Once you have set it up just follow the instructions shown in the prompt to obtain the desired information. Also note that the links used are from the Amazon Spain so in case the cookie session are from another country they should be changed accordingly. 

### Prerequisites

This tool is intended to work in python3. Also you need to have:

```
pip3 install requests
pip3 install matplotlib
```

### Installing
Once the prerequisites have been installed just type:

```
python3 alexaCookied.py PATH_TO_COOKIE_FILE
```

The cookie file can be obtained from the user's browser profile. Note that it has to be copied without changing any timestamps.
This can be done with this command in Linux/OS X, which will copy the cookie file into the folder Documents:

```
cp -p cookies.sqlite3 ~/Documents
```

## Authors

* **Xavier Marrugat**

## License

![License: GPL v3](https://img.shields.io/badge/License-GPLv3-blue.svg)(https://www.gnu.org/licenses/gpl-3.0)
