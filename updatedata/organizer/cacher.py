import os.path
import urllib.request
import shutil
import re
import time


# Handles downloading and caching of html-files
class Cacher:
    def __init__(self, overseer, language):
        self.overseer = overseer
        self.lang = overseer.lang_shorthand[language]
        self.cache_path = os.path.abspath(os.path.join(os.path.dirname(__file__), "..", ".cache"))

        self.last_request = time.time()
        self.rate_limiting = abs(self.overseer.dev_settings["no_rate_limiting"] - 1)

        if self.overseer.dev_settings["conserve_cache"] == 0:
            if os.path.isdir(self.cache_path):
                shutil.rmtree(self.cache_path)
            self.lang_path = self.create_folders()
            self.files = []
        else:
            self.lang_path = self.create_folders()
            self.files = next(os.walk(os.path.join(self.cache_path, self.lang)))[2]

    # Sets up the folder structure for the given language
    def create_folders(self):
        if not os.path.isdir(self.cache_path):
            os.mkdir(self.cache_path)

        lang_path = os.path.join(self.cache_path, self.lang)
        if not os.path.isdir(lang_path):
            os.mkdir(lang_path)
        return lang_path

    # Retrieves the requested html-file either from cache or downloads it
    def get(self, url):
        url_simple = re.sub("/", "_", url) + ".html"
        if self.caching_allowed(url):
            if url_simple in self.files:
                with open(os.path.join(self.lang_path, url_simple), mode="r") as data_file:
                    html = data_file.read()
            else:
                html = self.request_url(url)
                with open(os.path.join(self.lang_path, url_simple), mode="w") as data_file:
                    data_file.write(str(html))
                self.files.append(url_simple)
        else:
            html = self.request_url(url)
        return html

    # Checks whether caching is enabled for the given file
    def caching_allowed(self, url):
        if (
                self.overseer.caching["overviews"] and re.fullmatch(".*/(items|heroes)", url) or
                self.overseer.caching["items"] and re.fullmatch(".*/items/.*", url) or
                self.overseer.caching["heroes"] and re.fullmatch(".*/heroes/[a-z\-]*", url) or
                self.overseer.caching["abilities"] and re.fullmatch(".*/heroes/.*/abilities", url)
           ):
            return True

    # Retrieves the file specified by the url and returns it
    def request_url(self, url):
        if self.rate_limiting == 1:
            now = time.time()
            difference = now - self.last_request
            if difference < 1:
                time.sleep(difference)
            self.last_request = now
        print("request")
        req = urllib.request.Request("https://" + self.lang + "." + url, headers={"User-Agent": "Mozilla/5.0"})
        html = urllib.request.urlopen(req).read()
        return html
