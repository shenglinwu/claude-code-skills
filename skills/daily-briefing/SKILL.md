---
name: "daily-briefing"
description: "Generate a daily tech news briefing: read RSS feeds, curate 40 de-duplicated items from the past 24 hours, summarize and translate them, and output an HTML page with source links."
---

# Daily Briefing

Build a daily news briefing for engineers from a list of RSS feeds. Read the feeds, keep what was posted in the past 24 hours, pick the 40 items the audience will care about most, summarize each one, translate the summaries, and publish everything as a single self-contained HTML page with the original links.

## Settings

Use these defaults unless the user says otherwise in their request or in a `briefing-config.md` file next to the source list:

- **Working folder:** the folder that holds `news-sources.lst`. If the user doesn't name one, ask once. If the folder has no `news-sources.lst`, create one from the default list below.
- **Audience:** engineers interested in breaking news, technology trends, new releases, hands-on guides, and popular tools.
- **Item count:** 40.
- **Window:** the 24 hours before the run starts, in the user's local time zone.
- **Output language:** Traditional Chinese (Taiwan), in natural Taiwanese phrasing (軟體, 程式, 資料, 影片, 伺服器, 網路, 記憶體, 晶片, 使用者, 預設, 支援, 資安, 開源, 輝達 for NVIDIA). Users can set another language.
- **Summary length:** 200–300 English words, which is about 450–700 characters in Chinese.
- **Suggestions:** after each summary, add about 100 English words (roughly 150–250 Chinese characters) under the heading 「建議」, covering the likely impact on the reader and concrete actions they could take. Users can turn this off.
- **Page title:** 科技新聞精選 followed by the date. Leave the audience out of the title.
- **Output files:** `briefing-YYYY-MM-DD.html` in the working folder, where the date is today's date in the user's time zone, worked out at run time (never a date from an earlier run, an old file name, or this skill's text). Every run also overwrites `briefing-today.html` in the same folder with an exact copy of the file it just made, so the user can reload one fixed file to see the latest briefing. See step 7.
- **Vercel publishing:** after `briefing-today.html` passes the step 7 check, redeploy it to the Vercel project `daily-briefing` in production, so https://daily-briefing-puce.vercel.app always shows the latest briefing. See step 8. Users can turn this off or name another project in `briefing-config.md`.

## Default source list

If the working folder has no `news-sources.lst`, write this one, with one feed URL per line:

```
https://rsshub.ktachibana.party/36kr/information/AI
https://paddo.dev/rss.xml
http://feeds.feedburner.com/MachineLearningMastery
https://web-proxy-smoky.vercel.app/marktechpost/feed
https://web-proxy-smoky.vercel.app/google/rss/topics/CAAqIAgKIhpDQkFTRFFvSEwyMHZNRzFyZWhJQ1pXNG9BQVAB?hl=en-US&gl=US&ceid=US:en
https://rsshub.umzzz.com/juejin/category/ai
https://www.linuxtoday.com/feed/
http://devops.com/feed/
https://tools.wingzero.tw/rss
http://feeds.feedburner.com/freegroup
https://www.therundown.ai/feed
https://techcrunch.com/category/artificial-intelligence/feed/
https://cyberq.tw/category/news/feed/
https://simonwillison.net/atom/everything/
https://www.theverge.com/rss/index.xml
https://feeds.arstechnica.com/arstechnica/index
https://www.theregister.com/headlines.atom
https://thehackernews.com/feeds/posts/default
https://www.404media.co/rss/
https://krebsonsecurity.com/feed/
https://hnrss.org/frontpage
```

The Google News entry gives only headlines and redirect links, so it serves as a topic signal (see step 2). The direct feeds after Simon Willison's give real article links, and most carry the full text.

The two `web-proxy-smoky.vercel.app` entries go through a personal Vercel proxy run by the author of this skill, and it may not stay available. Tell users who share this skill that they can deploy their own proxy (see "Setting up your own proxy" at the end) and swap the URLs. Lines that are blank or start with `#` are not feeds.

## How to run it

### 1. Read the feeds

Read every feed in `news-sources.lst`. Use whatever fetch tool the environment has. If the shell has network access, `curl` with a browser User-Agent works too.

- Long feeds come back cut off. Keep reading at later offsets until you reach items older than the window, or the end of the feed.
- If a feed fails, try it twice more before giving up.
- RSSHub mirrors (any feed whose host name contains `rsshub`, such as `rsshub.ktachibana.party` and `rsshub.umzzz.com`) often fail to respond for a while and then recover. Try each one once in the first pass. If it fails, move on without the immediate retries, and come back after every other feed has been read. Then retry it up to 3 more times, with a short pause between tries and a fresh-copy parameter each time (`?v=2`, `?v=3`, `?v=4`, or `&v=N` when the URL already has a query string). Give up only after all 3 retries fail, and report how many attempts were made.
- Some fetch tools cache results for several minutes. If a feed failed and you are retrying, add a dummy query parameter (such as `?v=2`, or `&v=2` when the URL already has a query string) so you get a fresh copy.
- Record which feeds worked, which failed and why, and which had no items in the window.

Keep items whose publish date falls in the window. Convert every date to UTC before comparing, because feeds use different time zones.

### 2. Pick the items

- **Merge duplicates.** When several sources cover the same event, make it a single item and list every source link. Never list the same URL twice.
- **Rank for the audience.** Put hands-on guides, new tools and releases, security incidents, and major industry news first. Drop event listings, job posts, and stories that matter only to consumers.
- **Use Google News as a topic signal.** Its headlines show which topics are big today, so rank matching stories from other feeds higher. Pick a Google News story itself only when a direct feed or the publisher's own page gives enough text. Don't try to decode its redirect links.
- **Fill 40 slots.** If the window has fewer than 40 distinct items, use what exists and don't pad with older news.
- **Don't pick items you can't summarize.** If neither the feed nor the article has enough real content to write the summary, skip the item and choose another.

### 3. Get enough content to summarize

Many feed descriptions are too short for a 200–300 word summary.

- Open the article when the feed text is thin.
- When the article page blocks you, check whether the feed itself carries the full text in `content:encoded`. MarkTechPost, Juejin, 36Kr, and CyberQ do, so read the feed rather than the article page for those. Simon Willison's Atom feed carries the full post in its `summary` element.
- Simon Willison's feed mixes long posts with short link posts, quotes, and release notes. Merge the short ones into related stories or skip them, rather than giving each its own item.
- Google News feed links are redirect addresses (`news.google.com/rss/articles/...`) that fetch tools usually can't follow. First look for the same story in the direct feeds. Search for the headline only when the topic is big and no direct feed covers it, and keep it to about 5 searches per run. If you only find coverage from other outlets, use that, and list it as an extra link.
- The Hacker News front page feed (`hnrss.org/frontpage`) lists links to other sites. Open the linked article for content, and skip items whose page can't be read.
- If you can't get enough content, write a shorter summary and say inside the item what it was based on (for example, "based only on the RSS description").

### 4. Write each item

For each item:

- **Title:** a translated headline in the output language.
- **Original title:** the headline as the source published it.
- **Source and time:** the outlet name and the publish time in the user's time zone.
- **Summary:** what happened, with the key numbers, names, dates, and versions. Base it only on what the sources say. Mark vendor-reported benchmarks or claims as self-reported, and note any limitations the source mentions.
- **Suggestions (建議):** likely impact on an engineer and concrete next steps, such as what to check, try, patch, or watch. Keep it practical and tied to this story. This is the one place for your own judgment; mark it as advice, not fact.
- **Links:** every source link for the item. For Google News redirect links, label them as redirects (for example "Ars Technica（Google News 轉址）").

### 5. Build the page

Write one self-contained HTML file with inline CSS and no external scripts or fonts. Generate it with a script from structured data (a list of items) rather than by hand, so you can check counts and lengths.

Page layout:

- A header with the title, the date, the covered window, and the item count.
- A sticky row of category links with item counts. Suggested categories: 焦點新聞, 資安, AI 模型與研究, 開發者工具與實務, 基礎設施與能源, 產業與市場. Drop categories that end up empty.
- One card per item, numbered within the page, holding the meta line, title, original title, summary, 建議 block (visually distinct, for example a tinted box), and links.

Don't put a source-status section (來源說明) on the page. Readers don't need it. Write it to `briefing-YYYY-MM-DD.log` in the working folder instead: which feeds were read, which failed and why, which had nothing in the window, the item count, thin or merged items, and the step 6 check results.
- Readable on phone and desktop, with support for dark mode via `prefers-color-scheme`. Use `lang="zh-Hant-TW"` for Traditional Chinese.

### 6. Check it and report

Before delivering, run checks in code:

- The page parses, and the number of cards matches the number of items.
- No URL appears twice.
- Summary and suggestion lengths fall in range. List any that don't.
- For Chinese output, search for common Simplified characters (such as 数据, 软件, 视频, 信息, 网络). Only original headlines quoted as-is may contain them.

### 7. Save both files and confirm the copy

This step is required on every run. The run isn't finished until `briefing-today.html` holds today's briefing.

1. Write today's dated file, `briefing-YYYY-MM-DD.html`, to the working folder.
2. Overwrite `briefing-today.html` in the same folder with the same bytes, and copy from the file you just wrote, never from an older dated file. Use whatever reaches the working folder:
   - **Local shell:** `cp briefing-YYYY-MM-DD.html briefing-today.html`, or on Windows PowerShell `Copy-Item briefing-YYYY-MM-DD.html briefing-today.html -Force`.
   - **Remote folder through a file bridge** (for example, a cloud session writing to the user's computer with a commit or upload tool): send the same generated file twice, once to each path, in the same call or right after. Overwrite the existing `briefing-today.html` even though it is older; don't skip it because it already exists, and don't keep an old version on the grounds that the file changed since it was last read.
   - **No access to the user's folder:** send both files to the user and say that they need to replace `briefing-today.html` themselves.
3. Check the result by listing or reading back the folder. `briefing-today.html` must have the same size as today's dated file (or the same hash, where you can compute one), and its `<title>` must contain today's date. If either check fails, copy again once, check again, and if it still fails, tell the user plainly that `briefing-today.html` was not updated.
4. If the dated file couldn't be written, leave `briefing-today.html` as it was, so it never points at a half-written briefing.

### 8. Redeploy to Vercel

Run this step only after step 7 confirmed that `briefing-today.html` holds today's briefing. If step 7 failed, skip it, so the live site never shows a broken or old briefing, and say so in the report.

1. **Copy.** Copy `briefing-today.html` to `vercel-site/index.html` inside the working folder (create `vercel-site/` if it is missing). Only that one file goes in `vercel-site/`, so nothing else from the working folder is uploaded.
2. **Check login.** Run `vercel whoami`. If the CLI is missing or logged out, don't deploy. Tell the user to run `! vercel login` (or install the CLI with `npm i -g vercel`), and report that the site was not updated.
3. **Deploy.** From `vercel-site/`, run:
   ```
   vercel deploy --prod --yes --project daily-briefing
   ```
   This updates the existing production site. The user approved production deploys of this project for this skill. If the project is missing (for example, a new account), add `--create-if-missing`.
4. **Verify.** Fetch https://daily-briefing-puce.vercel.app/ with `curl`. It must return HTTP 200, the same byte size as `briefing-today.html`, and a `<title>` with today's date. A CDN cache can serve the old page for a short time: if the check fails, wait about 10 seconds and fetch again, up to 3 times.
5. **On failure.** If the deploy command fails or the check still fails, run `vercel inspect <deployment-url>` and `vercel logs <deployment-url>`, show the error lines, and tell the user plainly that the live site still shows the older briefing. Don't retry the deploy more than once.

The local files from step 7 are the main output. A failed deploy never undoes them.

Then tell the user:

- the output paths (the dated file and `briefing-today.html`), and that the copy was checked
- the Vercel result: the live URL, and that it was checked (or why the deploy was skipped or failed)
- how many feeds were read, which failed (and the error), and which had no items in the window
- the item count
- any summaries based on thin content, and any merged stories

## Setting up your own proxy

Google News blocks automated readers, and MarkTechPost's firewall blocks requests for its feed that don't look like a browser. A small Vercel project gets around both.

`vercel.json`:

```json
{
  "rewrites": [
    { "source": "/google/:path*", "destination": "https://news.google.com/:path*" },
    { "source": "/marktechpost/feed", "destination": "/api/marktechpost-feed" },
    { "source": "/marktechpost/:path*", "destination": "https://www.marktechpost.com/:path*" }
  ]
}
```

`api/marktechpost-feed.js`:

```js
export default async function handler(req, res) {
  const upstream = await fetch("https://www.marktechpost.com/feed/", {
    headers: {
      "User-Agent":
        "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 " +
        "(KHTML, like Gecko) Chrome/131.0.0.0 Safari/537.36",
      "Accept": "application/rss+xml,application/xml;q=0.9,text/html;q=0.8,*/*;q=0.7",
      "Accept-Language": "en-US,en;q=0.9",
      "Referer": "https://www.marktechpost.com/",
    },
  });
  const body = await upstream.text();
  res.setHeader("Content-Type", "application/rss+xml; charset=utf-8");
  res.setHeader("Cache-Control", "s-maxage=1800, stale-while-revalidate=3600");
  res.status(upstream.status).send(body);
}
```

The feed rule has to come before the catch-all `/marktechpost/:path*` rule, because Vercel uses the first match. Plain rewrites can't change request headers, which is why the feed needs a function. After deploying, replace `web-proxy-smoky.vercel.app` in `news-sources.lst` with your own domain.

Other Google News topics or searches work through the same `/google/` route, for example `/google/rss/search?q=site:example.com&hl=en-US&gl=US&ceid=US:en`. Keep proxy URLs short, because some fetch tools reject very long URLs.

If a site blocks you, check that working around the block fits its terms. Caching responses, as the function above does, keeps the load on the site small.
