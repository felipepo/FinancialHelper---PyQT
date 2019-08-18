from FinHelper import main
import traceback

def testvenv():
    import sys
    print("-----------------")
    [print(path) for path in sys.path]

if __name__ == "__main__":
    try:
        main.main()
    except Exception:
        traceback.print_exc()
        input("Press enter to continue...")
    # pyinstaller --noconsole --icon=FinHelper/data/images/Desktop.ico FinHelper/main.py
    # testvenv()
    # print("PO")