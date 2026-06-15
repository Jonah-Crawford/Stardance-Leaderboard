import os
import re
import csv
import time
import requests

from bs4 import BeautifulSoup

BASE = "https://stardance.hackclub.com/projects/{}"
OUTPUT_FILE = "stardance_projects.csv"
TEMP_FILE = "stardance_projects.tmp.csv"

START_ID = 1
END_ID = 100_000

MAX_CONSECUTIVE_404S = 100

DELAY = 0.4

def get_project(pid):
  url = BASE.format(pid)

  try:
    response = requests.get(url, timeout=8, headers={
      "User-Agent": "Stardance leaderboard experiment by @The_Craw"
    })
  except requests.RequestException: return "ERROR"

  if response.status_code == 404: return "404"

  if response.status_code != 200: return "ERROR"

  soup = BeautifulSoup(response.text, "html.parser")
  text = soup.get_text("\n", strip=True)

  title_tag = soup.find("h1")
  title = title_tag.get_text(strip=True) if title_tag else None

  if not title: return "ERROR"

  author = None
  author_match = re.search(r"By\s+(@[\w.-]+)", text)
  if author_match: author = author_match.group(1)

  devlogs = None
  devlog_match = re.search(r"(\d+)\s+Devlogs", text)
  if devlog_match: devlogs = int(devlog_match.group(1))

  hours = None
  hours_match = re.search(r"(\d+)\s+Total hours", text)
  if hours_match: hours = int(hours_match.group(1))

  followers = None
  followers_match = re.search(r"(\d+)\s+followers", text)
  if followers_match: followers = int(followers_match.group(1))

  return {
    "id": pid,
    "title": title,
    "author": author,
    "devlogs": devlogs,
    "hours": hours,
    "followers": followers,
    "url": url
  }

def main():
  with open(TEMP_FILE, "a", newline="", encoding="utf-8") as file:
    writer = csv.DictWriter(file, fieldnames=[
      "id",
      "title",
      "author",
      "devlogs",
      "hours",
      "followers",
      "url"
    ])

    writer.writeheader()
    file.flush()

    start = time.time()
    consecutive_404s = 0

    start = time.time()

    for pid in range(START_ID, END_ID + 1):
      result = get_project(pid)

      if result == "404":
        consecutive_404s += 1
        print(f"[{pid}] 404 ({consecutive_404s}/{MAX_CONSECUTIVE_404S})")

        if consecutive_404s >= MAX_CONSECUTIVE_404S:
          print(f"Stopping after {MAX_CONSECUTIVE_404S} consecutive 404s")
          break

      elif result == "ERROR": print(f"[{pid}] Request error")

      else:
        consecutive_404s = 0
        writer.writerow(result)
        file.flush()

        print(
          f"[{pid}] {result['title']} | "
          f"{result['hours']} hours | "
          f"{result['followers']} followers"
        )

      time.sleep(DELAY)

  os.replace(TEMP_FILE, OUTPUT_FILE)

  print(f"Completed in {time.time() - start:.2} seconds.")

if __name__ == "__main__": main()
