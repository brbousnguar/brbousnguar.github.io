### Changed
- SEO head cleanup: Twitter Card tags use `name=`, dropped `meta keywords` and the non-standard `twitter:url`, added `og:site_name`, `og:locale` and image alt text; removed `Crawl-delay` from `robots.txt`; Lighthouse workflow now audits heybrahim.com on Node 24 (#40)

### Added
- IndexNow key file and `tools/indexnow.py` to ping Bing (and through it ChatGPT search, Copilot, DuckDuckGo) after a deploy (#40)
