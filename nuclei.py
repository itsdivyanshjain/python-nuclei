import sys
from core.runner import Runner

# print(sys.argv)
# not using argparse for simplicity
if len(sys.argv) < 3 or len(sys.argv) > 3:
    print('''Usage:
        -python main.py target (Full URl) template/template path
        E.g: python https://example.com cves
        ''')

elif len(sys.argv) == 3:
    hello = Runner(sys.argv[1], sys.argv[2])
    # print(hello)
    hello.runenum()
