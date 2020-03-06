# rbl-checker

Help you to check if any IP in your IP range is blacklisted

*Author : sycured*

*LICENSE : GNU GENERAL PUBLIC LICENSE Version 3*

# Install

Git clone the repository and install all requirements.

If you use virtual environment, you can create it directly here.

This is the list of name included in the .gitignore for it :

- .env
- env
- ENV
- venv

You also need [CrateDB](https://crate.io/download).


## CrateDB : Setup table

    python3 setup_crate.py

## List of IP range

You need to create the file :

    ip_range.list

It's a simple text file like ip_range.example but it's included in .gitignore.

Your ip_range.list must be in the same directory of ip_range.example.

# Run

    python3 run.py

# Update

You can easily update using

    git pull
