import os.path
import re
import shutil
import time
import urllib.request


# Handles downloading and caching of html-files
class Cacher:
    def __init__(self, overseer, language):
        self.overseer = overseer
        self.lang = overseer.lang_shorthand[language]
        self.cache_path = os.path.abspath(os.path.join(os.path.dirname(__file__), "..", ".cache"))

        self.last_request = time.time()
        self.rate_limiting = abs(self.overseer.dev_settings["no_rate_limiting"] - 1)
        self.rate_per_sec = self.overseer.settings["rate_per_sec"]

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
                with open(os.path.join(self.lang_path, url_simple), mode="rb") as data_file:
                    html = data_file.read()
            else:
                html = self.get_file(url)
                with open(os.path.join(self.lang_path, url_simple), mode="wb") as data_file:
                    data_file.write(html)
        else:
            html = self.get_file(url)
        return html.decode("utf-8", "ignore")

    # Checks whether caching is enabled for the given file
    def caching_allowed(self, url):
        if (
                self.overseer.caching["overviews"] and re.fullmatch(".*/(items|heroes)", url) or
                self.overseer.caching["items"] and re.fullmatch(".*/items/.*", url) or
                self.overseer.caching["heroes"] and re.fullmatch(".*/heroes/[a-z\-]*", url) or
                self.overseer.caching["abilities"] and re.fullmatch(".*/heroes/.*/abilities", url)
           ):
            return True

    # Gets the requested file from the source specified by the settings
    def get_file(self, url):
        if self.overseer.dev_settings["local_cache"] == 1:
            url_simple = re.sub("/", "_", url) + ".html"
            path = self.overseer.settings["local_cache_path"].split("/")
            path.append(self.lang)
            path.append(url_simple)
            cache_path = os.path.abspath(os.path.join(os.path.dirname(__file__), *path))
            with open(cache_path, mode="rb") as data_file:
                html = data_file.read()
        elif self.overseer.dev_settings["server_cache"] == 1:
            url_simple = re.sub("/", "_", url) + ".html"
            cache_url = self.overseer.settings["server_cache_url"]
            full_url = cache_url + "/" + self.lang + "/" + url_simple
            html = self.request_url(full_url)
        else:
            full_url = "https://" + self.lang + "." + url
            html = self.request_url(full_url)
        return html

    # Retrieves the file specified by the url and returns it (with rate limiting)
    def request_url(self, url):
        if self.rate_limiting == 1:
            now = time.time()
            difference = now - self.last_request
            if difference < self.rate_per_sec:
                time.sleep(self.rate_per_sec - difference)
        req = urllib.request.Request(url, headers={"User-Agent": "Mozilla/5.0"})
        self.last_request = time.time()
        html = urllib.request.urlopen(req).read()
        return html
