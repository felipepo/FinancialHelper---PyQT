from FinHelper import main

def testvenv():
    import sys
    print("-----------------")
    [print(path) for path in sys.path]

if __name__ == "__main__":
    main.main()
    # pyinstaller --noconsole --icon=FinHelper/data/images/Desktop.ico FinHelper/main.py
    # testvenv()
    # print("PO")