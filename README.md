# CSESoc Scavhunt
---

![UNSW CSESoc Logo](site/assets/img/csesocgreyblue.png)
[Original repo](https://github.com/featherbear/UNSW-CompClub2019Summer-CTF)

---
## Features
The admin can create/edit:
- Categories

All questions and submissions must be associated with a category.

- Questions

Users can submit an answer. There can only be one correct answer for a question. It is not case sensitive.

- Submissions

Users can submit an entry for a submission. The admin can approve/unapprove submissions.

Questions and submissions that have been approved are awarded points.


The admin can view a user's username, points and solves. They can also delete a user.
Users can be viewed sorted by:
- Username (Descending)
- Username (Ascending)
- Points (Descending)
- Points (Ascending)
- Solves (Descending)
- Solves (Ascending)


Both users and the admin can view the leaderboard where users are ranked by points. The admin is not on the leaderboard.

Solved questions and submissions (submissions that have been approved by the admin) appear green to users.

Pending submissions (submissions that have not been approved by the admin) appear yellow to users.

## Installation
A [_requirements.txt_](server/requirements.txt) file is located in the _server_ folder  
`python3 -m pip install -r requirements.txt`

## Run
```bash
cd ~/scavhunt/server
python3 -m pip install -r requirements.txt
python3 server.py
```

## Run on Server
```bash
cd ~/scavhunt/server
sudo lsof -t -i tcp:443 -s tcp:listen | sudo xargs kill
sudo nohup python3 server.py &
```

## Configuration File
When the server first runs, a `settings.ini` file will be automatically created from the `settings.example.ini` skeleton.

```ini
[SERVER]
port = 443               # Port to listen on
database = data.sqlite3 # SQLite database file 

[SITE]
templatesDir = ../site  # Jinja template base path
staticDir = ../site     # Static file base path

[ADMIN]
username = admin        # Superuser username
password = password     # Superuser password
```

---
## Credits

This was originally created by Andrew Wong for the CSESoc Compclub 2019 Summer CTF.

It has been modified by Michael Gribben for CSESoc's Scavhunt.

### Server (Python)
[`Jinja2`](http://jinja.pocoo.org) - _Version 2.10.1_  
[`tornado`](//www.tornadoweb.org) - _Version 5.1.1_

### Website
[`bulma.css`](//bulma.io) - _Version 0.7.2_  
[`Bulma-extensions`](//wikiki.github.io)  
[`normalize.css`](//necolas.github.io/normalize.css) - _Version 8.0.1_  
[`three.js`](//threejs.org) - _Version 98_  

[`Font Awesome`](//fontawesome.com)  
[`Hack`](//sourcefoundry.org/hack) - _Version 3.3.0_  

### Snippets / Resources
[`glitch - sketch of three.js`](//ykob.github.io/sketch-threejs/sketch/glitch.html) by yoichi kobayashi  
[`Jinja2 Rendering stub for Tornado`](https://bibhasdn.com/blog/using-jinja2-as-the-template-engine-for-tornado-web-framework/) by Bibhas Debnath  
[Dotted World Map](//www.deviantart.com/snowfleikun/art/Dots-world-map-179891314) by sNowFleikuN  
[CSS Scanlines](//codepen.io/meduzen/pen/zxbwRV) by meduzen  

---
## License
This software is licensed under the MIT License.  
You are free to redistribute it and/or modify it under the terms of the license.  
