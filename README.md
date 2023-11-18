## Description
- [Voronoi diagram](https://en.wikipedia.org/wiki/Voronoi_diagram) png generator with distinct colors
- Two methods to fill the canvas are used
- Starting with method fill_by_circles, finished with fill_by_calculating_distance
- Using 10% fill_by_circles and 90% fill_by_calculating_distance seems like a best ratio

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
<div align="left"><img src="https://raw.githubusercontent.com/loop614/pvoronoi/main/method_fill_by_circles.png" alt="output"/></div>

## Output
<div align="left"><img src="https://raw.githubusercontent.com/loop614/pvoronoi/main/output.png" alt="output"/></div>
