# bevilacqua.us — Flask App

A faithful Flask port of [www.bevilacqua.us](https://www.bevilacqua.us), packaged in a Docker container built on **Arch Linux** with **Python 3.14**

## Project structure

```
bevilacqua/
├── app.py                  # Flask application & post data
├── requirements.txt        # Flask + Gunicorn
├── Dockerfile              # Two-stage Arch Linux build
├── docker-compose.yml      # One-command deploy
├── templates/
│   └── index.html          # Jinja2 template
└── static/
    └── css/
        └── style.css       # Site stylesheet
```

## Quick start (Docker Compose)

## How it works

### `app.py`
All blog posts are stored as a plain Python list of dicts (`POSTS`). Each post may have:
- `title` / `date` — displayed as heading and dateline
- `body` — plain text paragraph
- `body_html` — pre-rendered HTML for rich posts (safe-marked in Jinja2)
- `images` — list of `{src, alt}` dicts rendered as a flex photo grid
- `code_blocks` — list of `{lang, code}` dicts highlighted by Highlight.js

Flask's single route (`/`) renders `templates/index.html` with the post list.

Edit the `POSTS` list in `app.py`. A minimal post looks like:

```python
{
    "title": "My new post",
    "date": "Jun 13, 2026",
    "body": "Some text here.",
    "images": [
        {"src": "https://example.com/photo.jpg", "alt": "A photo"},
    ],
}
```
