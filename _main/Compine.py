import re
import sys
import threading
from PyQt5.QtWidgets import (
    QApplication, QMainWindow, QVBoxLayout, QScrollArea, QWidget, QLineEdit, QTabWidget, QToolBar, QDialog, QPushButton, QAction, QMenuBar
)
from PyQt5.QtWebEngineWidgets import QWebEngineView, QWebEngineDownloadItem
from PyQt5.QtPrintSupport import QPrinter, QPrintDialog
from PyQt5.QtCore import QUrl
from PyQt5.QtGui import QIcon, QColor

# Configuration du serveur Flask
import requests
from flask import Flask, request, redirect, Response

app = Flask(__name__)
GOOGLE_URL = "https://www.google.com"
HEADERS = {
    "User-Agent": (
        "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 "
        "(KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36"
    )
}

CUSTOM_LOGO_URL = "https://www.cjoint.com/doc/24_11/NKquHQQMUIP_b22f9be8-076d-47a5-9dc8-7a2b13cafb27-removebg-preview.png"
HOME_STYLE = ""


@app.route("/")
def home():
    return redirect("/home")


@app.route("/home")
def compine_home():
    global HOME_STYLE
    html_content = f"""
    <!DOCTYPE html>
    <html lang="en">
    <head>
        <meta charset="UTF-8">
        <meta name="viewport" content="width=device-width, initial-scale=1.0">
        <title>Compine</title>
        <style>
            body {{
                font-family: Arial, sans-serif;
                text-align: center;
                margin: 0;
                padding: 0;
                background-color: #f2f2f2;
            }}
            .logo-container {{
                display: flex;
                justify-content: center;
                align-items: center;
                margin-top: 10vh;
            }}
            .logo {{
                width: 150px;
                height: auto;
                margin-right: 20px;
            }}
            .site-name {{
                font-size: 48px;
                font-weight: bold;
                color: #4285f4;
                display: inline-block;
            }}
            .search-bar {{
                margin-top: 20px;
            }}
            input[type="text"] {{
                width: 50%;
                padding: 10px;
                font-size: 18px;
                border: 1px solid #ddd;
                border-radius: 24px;
                box-shadow: 0 2px 4px rgba(0, 0, 0, 0.1);
                outline: none;
            }}
            input[type="submit"] {{
                padding: 10px 20px;
                font-size: 18px;
                color: white;
                background-color: #4285f4;
                border: none;
                border-radius: 24px;
                cursor: pointer;
                box-shadow: 0 2px 4px rgba(0, 0, 0, 0.2);
            }}
            input[type="submit"]:hover {{
                background-color: #357ae8;
            }}
            {HOME_STYLE}
        </style>
    </head>
    <body>
        <div class="logo-container">
            <img src="{CUSTOM_LOGO_URL}" alt="Compine Logo" class="logo">
            <div class="site-name">Compine</div>
        </div>
        <div class="search-bar">
            <form action="http://127.0.0.1:5000/search" method="GET">
                <input type="text" name="q" placeholder="Search Compine..." autofocus>
                <input type="submit" value="Search">
            </form>
        </div>
    </body>
    </html>
    """
    return Response(html_content, status=200, headers={"Content-Type": "text/html"})


@app.route("/search")
def search():
    query = request.args.get("q", "")
    try:
        google_response = requests.get(
            GOOGLE_URL + "/search",
            params={"q": query},
            headers=HEADERS
        )
        content = google_response.text

        # Remplacer le logo Google par le logo personnalisé
        content = content.replace(
            'https://www.google.com/images/branding/googlelogo/1x/googlelogo_color_272x92dp.png',
            CUSTOM_LOGO_URL
        )
        # Remplacer les mentions de "Google" par "Compine"
        content = content.replace("Google", "Compine")

        return Response(content, status=google_response.status_code, headers={
            "Content-Type": "text/html"
        })
    except Exception as e:
        return f"Une erreur s'est produite : {e}"


def run_proxy():
    app.run(port=5000, debug=False, use_reloader=False)


# Classe pour gérer les thèmes
class ThemeManager(QDialog):
    def __init__(self, parent):
        super().__init__(parent)
        self.setWindowTitle("Choisir un thème")
        self.setModal(True)
        self.setFixedSize(400, 600)

        # Liste des thèmes
        self.themes = [
            {"name": "Rosé sombre", "bg_color": "#300000", "text_color": "#FFD1DC"},
            {"name": "Océan profond", "bg_color": "#002b5c", "text_color": "#FFFFFF"},
            {"name": "Sable doré", "bg_color": "#F4A460", "text_color": "#2F4F4F"},
            {"name": "Vert forêt", "bg_color": "#228B22", "text_color": "#FFFFFF"},
            {"name": "Minuit bleu", "bg_color": "#191970", "text_color": "#87CEEB"},
            {"name": "Lavande douce", "bg_color": "#E6E6FA", "text_color": "#6A5ACD"},
            {"name": "Coucher de soleil", "bg_color": "#FF4500", "text_color": "#FFD700"},
            {"name": "Glacier", "bg_color": "#E0FFFF", "text_color": "#4682B4"},
            {"name": "Pastel rose", "bg_color": "#FFB6C1", "text_color": "#8B0000"},
            {"name": "Citron vert", "bg_color": "#32CD32", "text_color": "#000000"},
            {"name": "Brume violette", "bg_color": "#9400D3", "text_color": "#E6E6FA"},
            {"name": "Orange automne", "bg_color": "#FF8C00", "text_color": "#2E8B57"},
            {"name": "Rouge passion", "bg_color": "#DC143C", "text_color": "#FFFFFF"},
            {"name": "Bleu clair", "bg_color": "#ADD8E6", "text_color": "#00008B"},
            {"name": "Blanc classique", "bg_color": "#FFFFFF", "text_color": "#000000"},
            {"name": "Noir ébène", "bg_color": "#000000", "text_color": "#FFFFFF"},
            {"name": "Gris perle", "bg_color": "#D3D3D3", "text_color": "#2F4F4F"},
            {"name": "Bleu royal", "bg_color": "#4169E1", "text_color": "#FFFFFF"},
            {"name": "Or antique", "bg_color": "#FFD700", "text_color": "#8B0000"},
            {"name": "Bleu acier", "bg_color": "#4682B4", "text_color": "#E0FFFF"},
            {"name": "Rose vif", "bg_color": "#FF1493", "text_color": "#FFFFFF"},
            {"name": "Soleil jaune", "bg_color": "#FFFF00", "text_color": "#8B4513"},
            {"name": "Vert menthe", "bg_color": "#98FF98", "text_color": "#006400"},
            {"name": "Bleu ciel", "bg_color": "#87CEEB", "text_color": "#191970"},
            {"name": "Prune sombre", "bg_color": "#8B008B", "text_color": "#DDA0DD"},
            {"name": "Corail doux", "bg_color": "#F08080", "text_color": "#2F4F4F"},
            {"name": "Argenté", "bg_color": "#C0C0C0", "text_color": "#2E8B57"},
            {"name": "Vert olive", "bg_color": "#808000", "text_color": "#FFFFFF"},
            {"name": "Marron terre", "bg_color": "#8B4513", "text_color": "#FFDAB9"},
            {"name": "Bleu nuit", "bg_color": "#191970", "text_color": "#FFFFFF"},
        ]

        # Layout principal
        layout = QVBoxLayout()

        # ScrollArea pour permettre le défilement
        scroll_area = QScrollArea()
        scroll_content = QWidget()
        scroll_layout = QVBoxLayout(scroll_content)

        for theme in self.themes:
            button = QPushButton(theme["name"])
            button.setStyleSheet(f"background-color: {theme['bg_color']}; color: {theme['text_color']};")
            button.clicked.connect(lambda _, t=theme: self.apply_theme(t))
            scroll_layout.addWidget(button)

        scroll_area.setWidget(scroll_content)
        layout.addWidget(scroll_area)
        self.setLayout(layout)

    def apply_theme(self, theme):
        global HOME_STYLE
        HOME_STYLE = f"body {{ background-color: {theme['bg_color']}; color: {theme['text_color']}; }}"
        self.parent().refresh_home()  # Mettre à jour la page d'accueil

class CompineBrowser(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Compine")
        self.setGeometry(100, 100, 1024, 768)
        
        # Définir l'icône de la fenêtre
        self.setWindowIcon(QIcon('icons/logo.png'))  # Assurez-vous que 'logo.png' est dans le dossier 'icons'
        
        # Initialiser la liste des favoris et de l'historique
        self.bookmarks = []
        self.history = []
        self.is_dark_mode = False

        # Créer le navigateur
        self.browser = QWebEngineView()
        self.browser.setUrl(QUrl("http://127.0.0.1:5000/home"))
        self.setCentralWidget(self.browser)

        # Connecter l'événement de téléchargement
        self.browser.page().profile().downloadRequested.connect(self.on_download_requested)

        # Ajouter la barre d'outils
        self.toolbar = QToolBar()
        self.addToolBar(self.toolbar)

        # Ajouter des actions à la barre d'outils
        self.toolbar.addAction(QIcon('icons/back.png'), "Retour", self.go_back)
        self.toolbar.addAction(QIcon('icons/forward.png'), "Avancer", self.go_forward)
        self.toolbar.addAction(QIcon('icons/refresh.png'), "Rafraîchir", self.refresh)
        self.toolbar.addAction(QIcon('icons/new_tab.png'), "Ouvrir un onglet", self.open_new_tab)

        # Ajouter un champ de recherche à la barre d'outils
        self.search_bar = QLineEdit()
        self.search_bar.setPlaceholderText("Rechercher ou entrer une URL...")
        self.search_bar.setFixedWidth(300)
        self.toolbar.addWidget(self.search_bar)

        # Connecter l'événement de la barre de recherche (entrée)
        self.search_bar.returnPressed.connect(self.perform_search_or_navigate)

        # Créer la fenêtre de navigation avec gestion des onglets
        self.tab_widget = QTabWidget(self)
        self.tab_widget.addTab(self.create_browser_view(), "Compine")
        self.setCentralWidget(self.tab_widget)

        self.tab_widget.setTabsClosable(True)
        self.tab_widget.tabCloseRequested.connect(self.close_tab)

        # Connecter le signal de changement d'URL pour mettre à jour la barre de recherche
        self.tab_widget.currentWidget().urlChanged.connect(self.update_search_bar)

        # Connecter le signal de changement de titre pour mettre à jour le nom de l'onglet
        self.tab_widget.currentWidget().titleChanged.connect(self.update_tab_title)

        # Menu déroulant pour la gestion des actions
        self.menu_bar = self.menuBar()
        self.create_navigation_menu()
        self.create_view_menu()

    def create_navigation_menu(self):
        navigation_menu = self.menu_bar.addMenu("Navigation")

        # Ajouter une action pour aller à la page d'accueil
        home_action = QAction("Page d'accueil", self)
        home_action.triggered.connect(self.go_home)
        navigation_menu.addAction(home_action)

        # Ajouter une action pour gérer les favoris
        bookmarks_action = QAction("Favoris", self)
        bookmarks_action.triggered.connect(self.open_bookmarks)
        navigation_menu.addAction(bookmarks_action)

        # Ajouter une action pour afficher l'historique
        history_action = QAction("Historique", self)
        history_action.triggered.connect(self.open_history)
        navigation_menu.addAction(history_action)

    def create_view_menu(self):
        view_menu = self.menu_bar.addMenu("Affichage")

        # Ajouter une action pour le mode sombre
        dark_mode_action = QAction("Mode Sombre", self)
        dark_mode_action.triggered.connect(self.toggle_dark_mode)
        view_menu.addAction(dark_mode_action)

        # Ajouter une action pour le zoom avant
        zoom_in_action = QAction("Zoom avant", self)
        zoom_in_action.triggered.connect(self.zoom_in)
        view_menu.addAction(zoom_in_action)

        # Ajouter une action pour le zoom arrière
        zoom_out_action = QAction("Zoom arrière", self)
        zoom_out_action.triggered.connect(self.zoom_out)
        view_menu.addAction(zoom_out_action)

        # Ajouter une action pour imprimer la page
        print_action = QAction("Imprimer la page", self)
        print_action.triggered.connect(self.print_page)
        view_menu.addAction(print_action)

    def update_search_bar(self, url):
        """Mettre à jour la barre de recherche avec l'URL actuelle."""
        self.search_bar.setText(url.toString())

    def update_tab_title(self, title):
        """Mettre à jour le titre de l'onglet avec le titre de la page."""
        current_index = self.tab_widget.currentIndex()
        if title:
            self.tab_widget.setTabText(current_index, title)
        else:
            url = self.tab_widget.currentWidget().url()
            domain_name = url.host()
            self.tab_widget.setTabText(current_index, domain_name)

    def perform_search_or_navigate(self):
        search_text = self.search_bar.text().strip()
        if search_text:
            # Vérifier si le texte est une URL valide
            if search_text.startswith(('http://', 'https://')):
                self.tab_widget.currentWidget().setUrl(QUrl(search_text))
            else:
                search_url = f"http://127.0.0.1:5000/search?q={search_text}"
                self.tab_widget.currentWidget().setUrl(QUrl(search_url))

    def create_browser_view(self):
        browser = QWebEngineView()
        browser.setUrl(QUrl("http://127.0.0.1:5000/home"))
        return browser

    def refresh_home(self):
        self.tab_widget.currentWidget().setUrl(QUrl("http://127.0.0.1:5000/home"))

    def open_new_tab(self):
        new_browser = self.create_browser_view()
        self.tab_widget.addTab(new_browser, "Nouvel onglet")
        new_browser.urlChanged.connect(self.update_search_bar)
        new_browser.titleChanged.connect(self.update_tab_title)

    def close_tab(self, index):
        self.tab_widget.removeTab(index)

    def go_back(self):
        self.tab_widget.currentWidget().back()

    def go_forward(self):
        self.tab_widget.currentWidget().forward()

    def refresh(self):
        self.tab_widget.currentWidget().reload()

    def go_home(self):
        self.tab_widget.currentWidget().setUrl(QUrl("http://127.0.0.1:5000/home"))

    def open_bookmarks(self):
        # Afficher une boîte de dialogue avec les favoris
        bookmarks_dialog = QDialog(self)
        bookmarks_dialog.setWindowTitle("Favoris")
        layout = QVBoxLayout()
        for url in self.bookmarks:
            button = QPushButton(url)
            layout.addWidget(button)
        bookmarks_dialog.setLayout(layout)
        bookmarks_dialog.exec_()

    def open_history(self):
        # Afficher une boîte de dialogue avec l'historique
        history_dialog = QDialog(self)
        history_dialog.setWindowTitle("Historique")
        layout = QVBoxLayout()
        for url in self.history:
            button = QPushButton(url)
            layout.addWidget(button)
        history_dialog.setLayout(layout)
        history_dialog.exec_()

    def toggle_dark_mode(self):
        if self.is_dark_mode:
            self.setStyleSheet("background-color: white; color: black;")
        else:
            self.setStyleSheet("background-color: #121212; color: white;")
        self.is_dark_mode = not self.is_dark_mode

    def zoom_in(self):
        browser = self.tab_widget.currentWidget()
        current_zoom = browser.zoomFactor()
        browser.setZoomFactor(current_zoom + 0.1)

    def zoom_out(self):
        browser = self.tab_widget.currentWidget()
        current_zoom = browser.zoomFactor()
        browser.setZoomFactor(current_zoom - 0.1)

    def print_page(self):
        # Obtenez le navigateur actuel
        browser = self.tab_widget.currentWidget()
        
        # Créez un objet QPrinter
        printer = QPrinter()
        
        # Ouvrir la boîte de dialogue d'impression
        print_dialog = QPrintDialog(printer, self)
        
        if print_dialog.exec_() == QPrintDialog.Accepted:
            # Si l'utilisateur accepte, imprimez la page
            browser.page().print(printer, self.handle_print_finished)
    
    def handle_print_finished(self, success):
        """Callback qui se déclenche une fois l'impression terminée."""
        if success:
            print("L'impression a réussi.")
        else:
            print("L'impression a échoué.")

    # Fonction pour ajouter un favori
    def add_to_bookmarks(self, url):
        if url not in self.bookmarks:
            self.bookmarks.append(url)

    # Fonction pour enregistrer l'historique
    def add_to_history(self, url):
        if url not in self.history:
            self.history.append(url)

    def on_download_requested(self, download):
        # Gérer le téléchargement (par exemple, demander à l'utilisateur où enregistrer le fichier)
        download.accept()  # Accepter le téléchargement
        download.setPath("C:/path/to/your/downloads/")  # Spécifiez un chemin d'enregistrement si nécessaire
        download.finished.connect(self.on_download_finished)

    def on_download_finished(self):
        print("Téléchargement terminé!")

def run_application():
    app = QApplication(sys.argv)
    window = CompineBrowser()
    window.show()
    sys.exit(app.exec_())

if __name__ == "__main__":
    # Démarrer le serveur Flask dans un thread séparé
    threading.Thread(target=run_proxy, daemon=True).start()

    # Démarrer l'application PyQt
    run_application()
