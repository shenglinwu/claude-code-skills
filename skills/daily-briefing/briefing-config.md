# Briefing config

Settings for the daily-briefing skill. The skill copies this file into the working
folder on the first run. Edit the copy in the working folder, not this one.

## Publishing

- **Vercel project:** daily-briefing
- **Live URL:** https://daily-briefing-puce.vercel.app
- **Publish to Vercel:** yes

These are the author's values. On your own account, set your own project name and
leave the live URL blank (the skill then uses the URL the deploy prints), or set
"Publish to Vercel" to no.

## Google News is a topic signal, not a story source

The Google News feed (`web-proxy-smoky.vercel.app/google/...`) gives only headlines and
locked redirect links, so its items rarely have enough content to summarize.

- Use its headlines to see which topics are big today, and rank matching stories higher.
- Pick a story only when a direct feed (or the publisher's own page) gives enough text.
- Don't decode Google News redirect links.
- Search a Google News headline only when the topic is big and no direct feed covers it.
  Keep it to about 5 searches per run.

## Feeds that give only links or short blurbs

- `hnrss.org/frontpage` lists links to other sites. Open the linked article for content.
- `feed.infoq.com` gives only short blurbs. Open the linked article for content.
- `ai-muninn.com/zh-TW/feed.xml` gives only short blurbs. Its article pages load with plain
  `curl` and carry the full text. The feed is large (about 200 KB, every post ever), and
  each `pubDate` is the date only, at 00:00 UTC. Compare by date, so a post from yesterday
  is not dropped from the 24-hour window.

Skip items whose page can't be read.

## Logs

Write feed status, failures, and length-check results to `briefing-YYYY-MM-DD.log`
in the working folder. Don't put a 來源說明 section in the HTML page.
