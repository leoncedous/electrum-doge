import sys
sys.argv.append('--portable')
exec(open(sys._MEIPASS + "/run_electrum_doge_main.py").read())
