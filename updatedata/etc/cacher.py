import os.path
import re
import shutil
import time
import urllib.request

from util.overseer import base_path, cache_path


# Handles downloading and caching of html-files
class Cacher:
    def __init__(self, overseer, language):
        self.overseer = overseer
        self.lang = overseer.lang_shorthand[language]
        self.lang_path = os.path.join(cache_path, self.lang)

        prepare_folder_structure(self.overseer, self.lang_path)
        self.files = next(os.walk(os.path.join(cache_path, self.lang)))[2]

        self.last_request = time.time()
        self.rate_limiting = abs(self.overseer.dev_settings["no_rate_limiting"] - 1)
        self.rate_per_sec = self.overseer.rate_per_sec

    # Retrieves the requested html-file either from cache or downloads it
    def get(self, url):
        url = "https://" + self.lang + "." + url
        if self.caching_allowed(url):
            html = self.get_from_cache(url)
        else:
            html = self.request_url(url)
        return html.decode("utf-8", "ignore")

    # Checks whether caching is enabled for the given url
    def caching_allowed(self, url):
        if (
                self.overseer.caching["overviews"] and re.fullmatch(".*/(items|heroes)", url) or
                self.overseer.caching["items"] and re.fullmatch(".*/items/.*", url) or
                self.overseer.caching["heroes"] and re.fullmatch(".*/heroes/[a-z\-]*", url) or
                self.overseer.caching["abilities"] and re.fullmatch(".*/heroes/.*/abilities", url)
           ):
            return True

    # Returns the html after acquiring it from the appropriate source
    # (custom- an server-caches must contain all requested files)
    def get_from_cache(self, url):
        simple_url = url.split(".", 1)[1]
        simple_url = re.sub("/", "_", simple_url) + ".html"
        cache_to_disk = True

        if self.overseer.dev_settings["custom_cache"] == 1:
            custom_path = self.overseer.custom_cache_path.split("/") + [self.lang, simple_url]
            path = os.path.join(base_path, *custom_path)
            html = read(path)
        elif simple_url in self.files:
            path = os.path.join(self.lang_path, simple_url)
            html = read(path)
            cache_to_disk = False
        elif self.overseer.dev_settings["server_cache"] == 1:
            server_path = self.overseer.server_cache_url.split("/") + [self.lang, simple_url]
            server_url = "/".join(server_path)
            html = self.request_url(server_url)
        else:
            html = self.request_url(url)

        if cache_to_disk:
            write(os.path.join(self.lang_path, simple_url), html)
        return html

    # Retrieves and returns the file specified by the url
    def request_url(self, url):
        self.ratelimit()
        req = urllib.request.Request(url, headers={"User-Agent": "Mozilla/5.0"})
        self.last_request = time.time()
        html = urllib.request.urlopen(req).read()
        if self.overseer.dev_settings["verbose_console"] == 1:
            print("Request: " + url)
        return html

    # Implements basic rate limiting
    def ratelimit(self):
        if self.rate_limiting == 1:
            now = time.time()
            difference = now - self.last_request
            if difference < self.rate_per_sec:
                time.sleep(self.rate_per_sec - difference)


# Prepares the .cache folder for use
def prepare_folder_structure(overseer, lang_path):
    if overseer.dev_settings["conserve_cache"] == 0:
        if os.path.isdir(cache_path):
            shutil.rmtree(cache_path)

    if not os.path.isdir(cache_path):
        os.mkdir(cache_path)

    if not os.path.isdir(lang_path):
        os.mkdir(lang_path)


# Returns the bytes read from the given file
def read(path):
    with open(path, mode="rb") as data_file:
        data = data_file.read()
    return data


# Writes the given data to the given file
def write(path, data):
    with open(path, mode="wb") as data_file:
        data_file.write(data)
