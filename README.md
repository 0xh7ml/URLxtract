![URLxtract](../assets/urlxtract.png?raw=true)

<h1 align="center">URLxtract</h1>

URLxtract is a tool designed to extract URLs from text files. It is simple to use and can handle large files efficiently.

## Installation

To install URLxtract, clone the repository and install the required dependencies:

```bash
git clone https://github.com/0xh7ml/URLxtract.git
cd URLxtract
pip install -r requirements.txt
chmod +x urlxtract.py
```

## Usage

URLxtract uses argparse to handle command-line arguments. Below is the usage information:

```sh
./urlxtract.py -f <input_file> --fqdn --uniq --silent
```


```console
HELP:
-h, --help    show this help message and exit

INPUT:
-u , --url    single URL to extract domain from
-f , --file   file containing URLs to extract domains from

OUTPUT:
--fqdn        extract fully qualified domain names (FQDN)
--apex        extract apex (registered) domains
--uniq        only output unique domains

DEBUG:
--silent      silent mode
```

## ToDo
- [ ] Add extracting paths

## Alternative Tools
- [unfurl](https://github.com/tomnomnom/unfurl)