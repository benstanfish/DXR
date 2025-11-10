
import os, sys, shutil


from PyQt6.QtWidgets import QApplication, QFileDialog



from bid.bidreport import create_bid_log



app = QApplication(sys.argv)
create_bid_log()
exit()
sys.exit(app.exec())