from playwright.sync_api import sync_playwright
from PyQt5.QtWidgets import QApplication, QWidget, QVBoxLayout, QLabel, QLineEdit, QPushButton, QComboBox, QSpinBox

class YouTubeScraperApp(QWidget):
    def __init__(self):
        super().__init__()
        
        self.setWindowTitle("YouTube Video Scraper")
        self.setGeometry(100, 100, 400, 300)
        
        layout = QVBoxLayout()

        self.query_label = QLabel("Search Query:")
        self.query_input = QLineEdit(self)
        layout.addWidget(self.query_label)
        layout.addWidget(self.query_input)

        self.timeframe_label = QLabel("Timeframe:")
        self.timeframe_combo = QComboBox(self)
        self.timeframe_combo.addItems(["Last hour", "Today", "This week", "This month", "This year"])
        layout.addWidget(self.timeframe_label)
        layout.addWidget(self.timeframe_combo)

        self.video_count_label = QLabel("Number of Videos:")
        self.video_count_spinner = QSpinBox(self)
        self.video_count_spinner.setRange(1, 20)
        self.video_count_spinner.setValue(5)
        layout.addWidget(self.video_count_label)
        layout.addWidget(self.video_count_spinner)

        self.scrape_button = QPushButton("Scrape Videos", self)
        self.scrape_button.clicked.connect(self.scrape_videos)
        layout.addWidget(self.scrape_button)

        self.result_label = QLabel("Results will appear here.", self)
        layout.addWidget(self.result_label)

        self.setLayout(layout)

    def scrape_videos(self):
        query = self.query_input.text()
        timeframe = self.timeframe_combo.currentText()
        video_count = self.video_count_spinner.value()

        timeframe_dict = {
            "Last hour": "EgQIAhAB",
            "Today": "EgQIAhAD",
            "This week": "EgQIAhAE",
            "This month": "EgQIBBAB",
            "This year": "EgQIBRAB"
        }

        timeframe_code = timeframe_dict.get(timeframe, "EgQIBBAB")
        self.result_label.setText(f"Scraping {video_count} videos on '{query}' from YouTube...")

        with sync_playwright() as p:
            browser = p.chromium.launch(headless=True)
            page = browser.new_page()
            
            search_url = f'https://www.youtube.com/results?search_query={query}&sp={timeframe_code}&hl=en&gl=US'
            page.goto(search_url)

            video_elements = page.query_selector_all('ytd-video-renderer')[:video_count]

            results = []
            for index, video in enumerate(video_elements, start=1):
                title_element = video.query_selector('#video-title')
                views_element = video.query_selector('span.inline-metadata-item')

                if title_element and views_element:
                    title = title_element.inner_text().strip()
                    views = views_element.inner_text().strip()
                    results.append(f"{index}. Video Title: {title}\n   {views}")
                else:
                    results.append(f"{index}. Video Title and Views Not Found.")

            self.result_label.setText("\n\n".join(results))

            browser.close()

if __name__ == '__main__':
    app = QApplication([])
    window = YouTubeScraperApp()
    window.show()
    app.exec_()
