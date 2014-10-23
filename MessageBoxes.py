
from PyQt4.QtGui import QMessageBox

def aboutBox(parent=None, title="", msg=""):
    """Creates a message box with an OK button, suitable for displaying short 
    messages to the user."""
    
    QMessageBox.about(parent, title, msg)

def yesNoBox(parent=None, title="", msg=""):
    """Creates a message box with Yes and No buttons. Returns QMessageBox.Yes 
    if the user clicked Yes, or QMessageBox.No otherwise."""
    
    return QMessageBox.question(parent, title, msg, 
                                buttons=(QMessageBox.Yes | QMessageBox.No), 
                                defaultButton=QMessageBox.Yes)
