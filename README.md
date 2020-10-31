# MyBB Scraper Tools

## Installation

These tools require [Python 3](https://www.python.org/downloads/) to run.

1. Run `git clone https://github.com/zinabat/mybb-scraper-tools.git`
1. `cd mybb-scraper-tool`
1. Ensure the tool script is executable with `chmod +x generate_random_char.sh`
1. Run the script

## Random Active Character Selector

Chooses an active character at random and generates a character of the month template.

```bash
sh generate_random_char.sh
```

The first time the script runs, it will scrape all active characters and cache them. On subsequent runs, the script will simply choose a random character and display a template.

### Options

`--reset-cache`: Re-scrapes all of the active characters and saves to the cache

## Future Extensions

Want something not listed here? Create a Github Issue!

- deploy to a publicly accessible website
- group characters by OOC user so that all users have an equal chance
