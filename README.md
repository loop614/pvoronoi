## Description
- [Voronoi diagram](https://en.wikipedia.org/wiki/Voronoi_diagram) png generator with distinct colors
- Two methods to fill the canvas are used
- Starting with method fill_by_circles only when seeds are far apart, finished with fill_by_calculating_distance

## Requirements
- python3, python3-venv and requirements.txt

## Status
- poc done

## Quick Start
```console
$ python3 -m venv venv/
$ source venv/bin/activate
$ pip install -r requirements.txt
$ python3 main.py
$ deactivate
```

```console
$ python3 main.py
```

## Method fill_by_circles at 10%
<div align="left"><img src="https://raw.githubusercontent.com/loop614/pvoronoi/main/method_fill_by_circles.png" width=320 height=180 alt="output"/></div>

## Output
<div align="left"><img src="https://raw.githubusercontent.com/loop614/pvoronoi/main/output.png" width=320 height=180 alt="output"/></div>
