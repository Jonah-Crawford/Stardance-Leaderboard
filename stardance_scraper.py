import re
import csv
import time
import requests

from bs4 import BeautifulSoup

BASE = "https://stardance.hackclub.com/projects/{}"
OUTPUT_FILE = "stardance_projects.csv"

START_ID = 1
END_ID = 20000
DELAY = 0.1

def get_project(pid):
  url = BASE.format(pid)

  try:
    response = requests.get(url, timeout=8, headers={
      "User-Agent": "Stardance leaderboard experiment by @The_Craw"
    })
  except requests.RequestException:
    return None

  if response.status_code != 200:
    return None

  soup = BeautifulSoup(response.text, "html.parser")
  text = soup.get_text("\n", strip=True)

  title_tag = soup.find("h1")
  title = title_tag.get_text(strip=True) if title_tag else None

  if not title:
    return None

  author = None
  author_match = re.search(r"By\s+(@[\w.-]+)", text)
  if author_match:
    author = author_match.group(1)

  devlogs = None
  devlog_match = re.search(r"(\d+)\s+Devlogs", text)
  if devlog_match:
    devlogs = int(devlog_match.group(1))

  hours = None
  hours_match = re.search(r"(\d+)\s+Total hours", text)
  if hours_match:
    hours = int(hours_match.group(1))

  followers = None
  followers_match = re.search(r"(\d+)\s+followers", text)
  if followers_match:
    followers = int(followers_match.group(1))

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
  with open(OUTPUT_FILE, "w", newline="", encoding="utf-8") as file:
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

    for pid in range(START_ID, END_ID + 1):
      data = get_project(pid)

      if data:
        writer.writerow(data)
        file.flush()

        print(
          f"[{pid}] {data['title']} | "
          f"{data['hours']} hours | "
          f"{data['followers']} followers"
        )
      else:
        print(f"[{pid}] No project")

      time.sleep(DELAY)

  print(f"Done. Saved data to {OUTPUT_FILE} in {(time.time() - start):.2} seconds")

if __name__ == "__main__": main()
