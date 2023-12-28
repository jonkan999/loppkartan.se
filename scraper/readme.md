These files are meant to run in the order:

-- Main scraper script that scrapes content from source pages, compares to previous loads, stores new races, transforms new races and puts them up for staging.

python main_scraper.py

-- Gui that looks att all staged races and compares them to races already in production on the same day. Meant to be a checking tool so we dont load duplicate races.

python approvalGUI.py

-- Generates individual race pages per race based on a jinja template
python generate_race_pages.py
