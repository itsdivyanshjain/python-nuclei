# Python Nuclei

#### This tool is same as project-discovery/nuclei but just written in python.

## Installation

```
git clone https://github.com/itsdivyanshjain/python-nuclei
cd python-nuclei
pip3 install -r requirements.txt
python3 nuclei.py https://example.com cves
```

### Notes

- Not fully featured as nuclei which is written in GO.
- As an Intial development, Expect having Bug issues while running.
- Complatibility tested on linux Environment with python3.8 and installed Dependencies of pyyaml and requests.
- Make sure to have nuclei-templates in home directory otherwise it will Download in that directory for now.
- usage: `python nuclei.py target-site template-path`, also target site need to be a full url.
- Result may contain False positives.
- This is just my project.
