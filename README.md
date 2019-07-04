# mx3creations
The source code of my website's full rewrite, in django.
You can visit it right now at [mx3creations.com/beta](https://mx3creations.com/beta)

## Roadmap / TODO list
- [ ] Global audio player
- ~~Continuous audio playback w/ cookies storing playback position info~~
- [ ] Home button in navmenu ? (somewhere easy at least)
- [ ] Searchbar use POST intead of get
- [ ] download all dependencies for local import instead of CDNs
- [ ] optimize header images
- [x] /track/: fix URL not changing when redirecting from /search/
- [ ] \<ajax-search\>: delay before showing "Searching..."
- [ ] /search/: replace url (in history & in JS) to add /search/\<q\> instead of /search/
- [ ] /home/@mobile::carousel: change \<a\> links color based on current carousel page
- [ ] /home/@mobile::carousel: animations
- [ ] /listen/: Fix icon centering on mobile
- [ ] sass: make mixin for .cover and other stuff
- [ ] Icons as template tag
- [ ] /statistics/: Use GH api to get projects count (rn it's just a random int)
- [ ] Use current website footer social media style
- [ ] Move `globs.py`, it's not an elegant solution at all
- [ ] `music.views.track.btn_array_class`: Figure out more elegant solution
- [ ] /listen/: Work time / duration ratio
- [x] /home/: typed.js
- [x] \<ajax-search\>: show panel when typing, not onfocus
- [x] /home/@mobile::carousel: auto switch slides if no user input
- [x] /listen/: Fix weird icon bug for /listen/circular@desktop (.cls-2{stroke:none})
- [x] /home/: header-image: collage of screencaps from different softs reprensenting each thing
- [x] /listen/: Reorganize infos (too messy atm)
- [x] Translations
- [x] Contact form CSS
- [x] Stats page
- [x] Pull tweets w/ tweepy for /news/
- [x] Redirect /stats/ to /statistics/
- [X] custom icons
- [x] Import TODOs here

## Contributing
To request bugs or feature requests, you can either:
- Contact me on [my current website](https://mx3creations.com/bug-report)
- Create a pull request.
Please provide as much details you can in your request, feel free to include images if you have a design in mind.

If you just found a bug, and already know how to fix it, you can create a pull request.

## What do I do ?
I won't go too much into the details here, but I create electronic music and everything
that goes with it (artworks, scripts, etc)
Learn (way) more [here](https://mx3creations.com/about-me)
