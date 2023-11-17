# Marcus Wågberg's Homeassistant Addons
My repository of homeassistant addons.


## Addons

### Intermedium
Intermedium is a smtp to homeassistant notify proxy, writen by myself.

### Radicale
Radicale is a small but powerful CalDAV (calendars, to-do lists) and CardDAV (contacts) server. This addon also includes RadicaleInfCloud which integrates InfCloud into Radicale's web interface. InfCloud allows you to to manage appointments, tasks and contacts in the browser.


## Building, running, publishing, etc
Requierments:
* linux
* nix
* docker

Clone git repository:
```Bash
$ git clone https://github.com/MarcusWagberg/homeassistant-addons.git
```

Change directory into the repository:
```Bash
$ cd homeassistant-addons
```

Enter nix devshell:
```Bash
$ nix develop --no-write-lock-file
```

### Building
```Bash
$ build [addon]
```

### Running
```Bash
$ run [addon]
```

### Publishing
```Bash
$ publish [addon] [version]
```

### Checking outdated packages
```Bash
$ outdated
```
