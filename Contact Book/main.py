import sys
from PyQt6.QtWidgets import QListWidgetItem
from PyQt6.QtWidgets import QMessageBox  
from PyQt6.QtCore import QEasingCurve
from PyQt6.QtCore import QPropertyAnimation, QRect
from PyQt6.QtWidgets import QApplication, QWidget, QLabel, QPushButton, QLineEdit, QListWidget
from PyQt6.QtGui import QPixmap, QIntValidator
from PyQt6.QtCore import Qt

app = QApplication(sys.argv)

# --- Main Window ---
window = QWidget()
window.setWindowTitle("Floating Contact Book")

# Set window size to match your images (512x512)
window.setFixedSize(512, 512)

# Make window frameless and transparent
window.setWindowFlag(Qt.WindowType.FramelessWindowHint)
window.setAttribute(Qt.WidgetAttribute.WA_TranslucentBackground)

window.oldPos = None
def mousePressEvent(event):
    if event.button() == Qt.MouseButton.LeftButton:
        window.oldPos = event.globalPosition().toPoint()

def mouseMoveEvent(event):
    if window.oldPos:
        delta = event.globalPosition().toPoint() - window.oldPos
        window.move(window.x() + delta.x(), window.y() + delta.y())
        window.oldPos = event.globalPosition().toPoint()

window.mousePressEvent = mousePressEvent
window.mouseMoveEvent = mouseMoveEvent

# --- Real content sizes (snipped) ---
cover_content_width = 291
cover_content_height = 327
page_content_width = 491
page_content_height = 514

# --- COVER IMAGE ---
cover = QLabel(window)
cover_pixmap = QPixmap("images/cover.png")

# Increase cover size a bit (e.g., 20% bigger)
scale_factor = 1.2
cover_width = int(cover_content_width * scale_factor)   # 291 * 1.2 ≈ 349
cover_height = int(cover_content_height * scale_factor) # 327 * 1.2 ≈ 392

cover_scaled = cover_pixmap.scaled(cover_width, cover_height,
                                   Qt.AspectRatioMode.KeepAspectRatio,
                                   Qt.TransformationMode.SmoothTransformation)

# Center cover in window
cover_x = (512 - cover_scaled.width()) // 2  + 15
cover_y = (512 - cover_scaled.height()) // 2 

cover.setPixmap(cover_scaled)
cover.setGeometry(cover_x, cover_y, cover_scaled.width(), cover_scaled.height())

# --- OPEN BUTTON ---
open_button = QPushButton("Open Book", window)
open_button.setGeometry(206, 460, 100, 30)  # centered at bottom

# --- PAGES IMAGE ---
pages = QLabel(window)
page_pixmap = QPixmap("images/pages.png")

# Scale page to match cover content size visually
# (We can use same width/height as cover so it aligns perfectly)
page_scaled = page_pixmap.scaled(cover_scaled.width(), cover_scaled.height(),
                                 Qt.AspectRatioMode.KeepAspectRatio,
                                 Qt.TransformationMode.SmoothTransformation)

# Center page in the window
page_x = (512 - page_scaled.width()) // 2
page_y = (512 - page_scaled.height()) // 2

pages.setPixmap(page_scaled)
pages.setGeometry(page_x, page_y, page_scaled.width(), page_scaled.height())
pages.hide()

# --- PAGE 2 IMAGE ---
pages2 = QLabel(window)
page2_pixmap = QPixmap("images/pages_2.png")

page2_scaled = page2_pixmap.scaled(
    cover_scaled.width(),
    cover_scaled.height(),
    Qt.AspectRatioMode.KeepAspectRatio,
    Qt.TransformationMode.SmoothTransformation
)

pages2.setPixmap(page2_scaled)
pages2.setGeometry(page_x, page_y, page2_scaled.width(), page2_scaled.height())
pages2.hide()

# --- ADD CONTACT FIELDS (aligned to page only) ---

name_field = QLineEdit(window)
name_field.setPlaceholderText("Name")
name_field.setGeometry(page_x + 115, page_y + 80, 170, 28)
name_field.hide()

phone_field = QLineEdit(window)
phone_field.setPlaceholderText("Phone")
phone_field.setGeometry(page_x + 115, page_y + 120, 170, 28)
phone_field.setMaxLength(13)
phone_field.hide()

email_field = QLineEdit(window)
email_field.setPlaceholderText("Email")
email_field.setGeometry(page_x + 115, page_y + 160, 170, 28)
email_field.hide()

address_field = QLineEdit(window)
address_field.setPlaceholderText("Address")
address_field.setGeometry(page_x + 115, page_y + 200, 170, 28)
address_field.hide()

save_button = QPushButton("Save Contact", window)
save_button.setGeometry(page_x + 140, page_y + 240, 120, 32)
save_button.hide()

#next Button
next_page_button = QPushButton("Next Page", window)
next_page_button.setGeometry(page_x + 140, page_y + 310, 120, 32)
next_page_button.hide()

#previous Button
prev_page_button = QPushButton("Previous Page", window)
prev_page_button.setGeometry(page_x + 140, page_y + 350, 120, 32)
prev_page_button.hide()


success_label = QLabel("Contact saved successfully!", window)
success_label.setGeometry(page_x + 120, page_y + 275, 200, 25)
success_label.setStyleSheet("color: green; font-weight: bold;")
success_label.hide()

title_label = QLabel("Add Contact", window)
title_label.setGeometry(page_x + 140, page_y + 40, 120, 30)
title_label.setAlignment(Qt.AlignmentFlag.AlignCenter)
title_label.hide()

contact_info_label = QLabel("Contact Info", window)
contact_info_label.setGeometry(page_x + 140, page_y + 40, 120, 30)
contact_info_label.setAlignment(Qt.AlignmentFlag.AlignCenter)
contact_info_label.hide()

search_field = QLineEdit(window)
search_field.setPlaceholderText("Search")
search_field.setGeometry(page_x + 115, page_y + 80, 170, 28)
search_field.hide()


# same X as name field
# same Y as phone field (so it starts below search)




close_button = QPushButton("✕", window)
close_button.setGeometry(page_x + 270, page_y + 30, 24, 24)

close_button.setStyleSheet("""
QPushButton {
    background-color: white;
    color: red;
    border-radius: 12px;
    border: 1px solid red;
    font-weight: bold;
}
QPushButton:hover {
    background-color: #ffe5e5;
}
""")
close_button.clicked.connect(app.quit)
# close_button.hide()

contacts = []

# --- After defining contact_list ---
contact_list = QListWidget(window)
contact_list.setGeometry(page_x + 115, page_y + 120, 170, 110)
contact_list.hide()
contact_list.setStyleSheet("""
QListWidget::item:selected {
    background-color: #87CEFA;
    color: black;
}
""")

def refresh_contact_list():
    contact_list.clear()

    if not contacts:
        # Placeholder when no contacts
        placeholder_item = QListWidgetItem("No saved contacts")
        placeholder_item.setFlags(Qt.ItemFlag.NoItemFlags)  # unselectable
        placeholder_item.setForeground(Qt.GlobalColor.gray)
        placeholder_item.setTextAlignment(Qt.AlignmentFlag.AlignCenter)
        contact_list.addItem(placeholder_item)
    else:
        # Add real contacts
        for contact in contacts:
            item = QListWidgetItem(contact["name"])
            contact_list.addItem(item)


# Now call refresh
refresh_contact_list()

def save_contact():
    name = name_field.text().strip()
    phone = phone_field.text().strip()
    email = email_field.text().strip()
    address = address_field.text().strip()

    # Check if ALL fields are empty
    if not name and not phone and not email and not address:
        success_label.setText("Error: All fields are empty")
        success_label.setStyleSheet("color: red; font-weight: bold;")
        success_label.raise_()
        success_label.show()
        return

    # Check empty fields
    if name == "":
        success_label.setText("Name field has not been filled")
        success_label.setStyleSheet("color: red; font-weight: bold;")
        success_label.raise_()
        success_label.show()
        return

    if phone == "":
        success_label.setText("Phone field has not been filled")
        success_label.setStyleSheet("color: red; font-weight: bold;")
        success_label.raise_()
        success_label.show()
        return

    if email == "":
        success_label.setText("Email field has not been filled")
        success_label.setStyleSheet("color: red; font-weight: bold;")
        success_label.raise_()
        success_label.show()
        return

    if address == "":
        success_label.setText("Address field has not been filled")
        success_label.setStyleSheet("color: red; font-weight: bold;")
        success_label.raise_()
        success_label.show()
        return

    # Phone validation
    valid_phone = False

    # Case 1: 10 digits
    if phone.isdigit() and len(phone) == 10:
        valid_phone = True

    # Case 2: +91 followed by 10 digits
    elif phone.startswith("+91") and phone[3:].isdigit() and len(phone) == 13:
        valid_phone = True

    if not valid_phone:
        success_label.setText("Invalid phone number")
        success_label.setStyleSheet("color: red; font-weight: bold;")
        success_label.raise_()
        success_label.show()
        return



    # Email validation
    if not email.endswith("@gmail.com") or email.startswith("@"):
        success_label.setText("Invalid email")
        success_label.setStyleSheet("color: red; font-weight: bold;")
        success_label.raise_()
        success_label.show()
        return

    # Save contact
    contacts.append({
        
        "name": name,
        "phone": phone,
        "email": email,
        "address": address
    })

    refresh_contact_list()

    success_label.setText("Contact saved successfully!")
    success_label.setStyleSheet("color: green; font-weight: bold;")
    success_label.raise_()
    success_label.show()

    name_field.clear()
    phone_field.clear()
    email_field.clear()
    address_field.clear()


def open_book():
    open_button.hide()

    # Show pages behind the cover first
    pages.show()
    pages.lower()

    # Animate cover shrinking (flip)
    window.anim = QPropertyAnimation(cover, b"geometry")
    window.anim.setDuration(900)  # slightly slower for smoother feel
    window.anim.setStartValue(cover.geometry())

    end_rect = QRect(
        cover.x(),
        cover.y(),
        0,
        cover.height()
    )



    window.anim.setEndValue(end_rect)

    # Smooth motion
    window.anim.setEasingCurve(QEasingCurve.Type.InOutCubic)

    def on_finished():
        cover.hide()
        pages.raise_()

        title_label.show()
        name_field.show()
        phone_field.show()
        email_field.show()
        address_field.show()
        save_button.show()
        close_button.show()
        next_page_button.show()



        # Bring inputs above the page image
        title_label.raise_()
        name_field.raise_()
        phone_field.raise_()
        email_field.raise_()
        address_field.raise_()
        save_button.raise_()
        success_label.raise_()
        close_button.raise_()
        next_page_button.raise_()

    window.anim.finished.connect(on_finished)
    window.anim.start()

def open_page2():

    pages.setGeometry(page_x, page_y, page_scaled.width(), page_scaled.height())
    pages.show()
    pages.raise_()

    pages2.setGeometry(page_x, page_y, page2_scaled.width(), page2_scaled.height())
    pages2.show()
    pages2.lower()

    # hide page 1 widgets
    title_label.hide()
    name_field.hide()
    phone_field.hide()
    email_field.hide()
    address_field.hide()
    save_button.hide()
    success_label.hide()
    next_page_button.hide()

    # show page 2 behind page 1 first
    pages2.show()
    pages2.raise_()

    window.anim2 = QPropertyAnimation(pages, b"geometry")
    window.anim2.setDuration(900)
    window.anim2.setStartValue(pages.geometry())

    end_rect = QRect(
        pages.x(),
        pages.y(),
        0,
        pages.height()
    )

    window.anim2.setEndValue(end_rect)
    window.anim2.setEasingCurve(QEasingCurve.Type.InOutCubic)

    def finished():
        pages.hide()
        pages2.raise_()
        contact_info_label.show()
        contact_info_label.raise_()
        search_field.show()
        search_field.raise_()
        contact_list.show()
        contact_list.raise_()
        prev_page_button.show()
        prev_page_button.raise_()
        close_button.raise_()
        
    window.anim2.finished.connect(finished)
    window.anim2.start()



def go_back_page1():

    # restore original sizes
    pages.setGeometry(page_x, page_y, page_scaled.width(), page_scaled.height())
    pages2.setGeometry(page_x, page_y, page2_scaled.width(), page2_scaled.height())

    window.anim3 = QPropertyAnimation(pages2, b"geometry")
    window.anim3.setDuration(900)
    window.anim3.setStartValue(pages2.geometry())

    end_rect = QRect(
        pages2.x(),
        pages2.y(),
        0,
        pages2.height()
    )

    window.anim3.setEndValue(end_rect)
    window.anim3.setEasingCurve(QEasingCurve.Type.InOutCubic)

    def finished():

        pages2.hide()

        pages.show()
        pages.raise_()

        title_label.show()
        name_field.show()
        phone_field.show()
        email_field.show()
        address_field.show()
        save_button.show()
        next_page_button.show()

        prev_page_button.hide()
        contact_info_label.hide()
        search_field.hide()
        contact_list.hide()

        # VERY IMPORTANT: bring widgets above page image
        title_label.raise_()
        name_field.raise_()
        phone_field.raise_()
        email_field.raise_()
        address_field.raise_()
        save_button.raise_()
        next_page_button.raise_()
        close_button.raise_()
        success_label.raise_()

    window.anim3.finished.connect(finished)
    window.anim3.start()



def show_contact_details_floating(item):
    # --- Ignore placeholder click ---
    if item.text() == "No saved contacts":
        return

    # --- Close any previous floating window ---
    if hasattr(window, "detail_window") and window.detail_window.isVisible():
        window.detail_window.close()

    name = item.text()

    # find the contact
    for contact in contacts:
        if contact["name"] == name:
            # Create a floating window as child of main window
            detail_window = QWidget()
            window.detail_window = detail_window  # store reference
            detail_window.setWindowTitle(f"{contact['name']} - Details")
            detail_window.setGeometry(150, 150, 320, 220)
            detail_window.setWindowFlags(Qt.WindowType.Window | Qt.WindowType.WindowStaysOnTopHint)

            # --- Editable fields ---
            name_edit = QLineEdit(contact['name'], detail_window)
            name_edit.setGeometry(20, 20, 280, 25)
            name_edit.setFocus()

            phone_edit = QLineEdit(contact['phone'], detail_window)
            phone_edit.setGeometry(20, 55, 280, 25)

            email_edit = QLineEdit(contact['email'], detail_window)
            email_edit.setGeometry(20, 90, 280, 25)

            address_edit = QLineEdit(contact['address'], detail_window)
            address_edit.setGeometry(20, 125, 280, 25)

            # --- Buttons ---
            save_btn = QPushButton("Save", detail_window)
            save_btn.setGeometry(10, 180, 100, 30)

            delete_btn = QPushButton("Delete", detail_window)
            delete_btn.setStyleSheet("background-color: red; color: white; font-weight: bold;")
            delete_btn.setGeometry(210, 180, 100, 30)

            # --- Feedback label ---
            saved_label = QLabel("", detail_window)
            saved_label.setGeometry(110, 180, 100, 20)
            saved_label.setAlignment(Qt.AlignmentFlag.AlignCenter)

            # --- Delete function ---
            def delete_contact():
                reply = QMessageBox.question(
                detail_window, "Confirm Delete",
                f"Are you sure you want to delete {contact['name']}?",
                QMessageBox.StandardButton.Yes | QMessageBox.StandardButton.No
            )
                if reply == QMessageBox.StandardButton.Yes:
                    # Remove from contacts list
                    contacts.remove(contact)

                    refresh_contact_list()

                    
                    # Close ONLY the floating window (no setParent)
                    detail_window.close()                                               

            delete_btn.clicked.connect(delete_contact)

            # --- Save changes function ---
            def save_changes():
                new_name = name_edit.text().strip()
                new_phone = phone_edit.text().strip()
                new_email = email_edit.text().strip()
                new_address = address_edit.text().strip()

                # Validation
                if not new_name or not new_phone or not new_email or not new_address:
                    saved_label.setText("All fields required")
                    saved_label.setStyleSheet("color: red; font-weight: bold;")
                    return

                # Phone validation
                valid_phone = (new_phone.isdigit() and len(new_phone) == 10) or \
                              (new_phone.startswith("+91") and new_phone[3:].isdigit() and len(new_phone) == 13)
                if not valid_phone:
                    saved_label.setText("Invalid phone")
                    saved_label.setStyleSheet("color: red; font-weight: bold;")
                    return

                # Email validation
                if not new_email.endswith("@gmail.com") or new_email.startswith("@"):
                    saved_label.setText("Invalid email")
                    saved_label.setStyleSheet("color: red; font-weight: bold;")
                    return

                # Update contact
                contact['name'] = new_name
                contact['phone'] = new_phone
                contact['email'] = new_email
                contact['address'] = new_address

                item.setText(contact['name'])
                saved_label.setText("Saved!")
                saved_label.setStyleSheet("color: green; font-weight: bold;")

                from PyQt6.QtCore import QTimer
                QTimer.singleShot(2000, lambda: saved_label.setText(""))
                refresh_contact_list()

            save_btn.clicked.connect(save_changes)

            # --- Show floating window ---
            detail_window.show()
            break


    
def search_contact():
    search_text = search_field.text().strip().lower()
    
    # Clear previous selection
    contact_list.clearSelection()
    
    # Loop through all items in the list
    for i in range(contact_list.count()):
        item = contact_list.item(i)
        if search_text == item.text().lower():  # exact match
            contact_list.setCurrentItem(item)  # selects/highlights the item
            contact_list.scrollToItem(item)
            break





open_button.clicked.connect(open_book)
save_button.clicked.connect(save_contact)
next_page_button.clicked.connect(open_page2)
prev_page_button.clicked.connect(go_back_page1)
contact_list.itemDoubleClicked.connect(show_contact_details_floating)
search_field.returnPressed.connect(search_contact)

window.show()
sys.exit(app.exec())