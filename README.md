# ARDA Scraper
Tooling for acquiring church location and details from the Association of Religion Data Archives

### Objective

Allow users to collect attributes and geometry of church locations as GeoJSON

### Installation

Requires Python3.5+

First you need to unzip ```data/us_counties.zip``` to the ```data``` directory

Next, install the requirements.

```bash
(my_venv) $ pip install -r requirements.txt
```

### Usage

Let's get the church point locations and attributes for Indiana

```bash
(my_venv) $ python arda_scraper.py IN ~/in_arda.geojson
```

### License

Copyright 2018 Aaron Burgess

Permission is hereby granted, free of charge, to any person obtaining a copy of this software and associated documentation files (the "Software"), to deal in the Software without restriction, including without limitation the rights to use, copy, modify, merge, publish, distribute, sublicense, and/or sell copies of the Software, and to permit persons to whom the Software is furnished to do so, subject to the following conditions:

The above copyright notice and this permission notice shall be included in all copies or substantial portions of the Software.

THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY, FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM, OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE SOFTWARE.

