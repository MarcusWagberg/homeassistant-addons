# Marcus Wågberg's Homeassistant Addons
My repository of homeassistant addons.


## Addons

### Intermedium
Intermedium is a smtp to homeassistant notify proxy, writen by myself.

### Radicale
Radicale is a small but powerful CalDAV (calendars, to-do lists) and CardDAV (contacts) server. This addon also includes RadicaleInfCloud which integrates InfCloud into Radicale's web interface. InfCloud allows you to to manage appointments, tasks and contacts in the browser.


## Building, running, publishing, etc
Requierments:
* Python3 (tested with Python 3.10.10)
* Docker  (tested with Docker 23.0.1)

Clone git repository:
```Bash
$ git clone https://github.com/MarcusWagberg/homeassistant-addons.git
```

Change directory into the repository:
```Bash
$ cd homeassistant-addons
```

Create the python venv:
```Bash
$ ./venv.sh
```

### Building
```Bash
$ ./scripts/build.py [addon]
```

### Running
```Bash
$ ./scripts/build.py [addon]
```

### Publishing
```Bash
$ ./scripts/publish.py [addon] [version]
```

### Checking outdated packages
```Bash
$ ./scripts/outdated.py
```
