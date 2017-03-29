import os.path
import urllib.request
import shutil
import re


# Handles downloading and caching of html-files
class Cacher:
    def __init__(self, overseer):
        self.overseer = overseer
        self.cache_path = os.path.abspath(os.path.join(os.path.dirname(__file__), "..", ".cache"))
        if not self.overseer.caching_enabled:
            if os.path.isdir(self.cache_path):
                shutil.rmtree(self.cache_path)
        else:
            if not os.path.isdir(self.cache_path):
                os.mkdir(self.cache_path)
            self.files = next(os.walk(self.cache_path))[2]

    # Retrieves the requested html-file either from cache or downloads it
    def get(self, url):
        url_simple = url.lstrip("https://www.").replace("/", "_")
        if self.caching_allowed(url):
            if (url_simple + ".html") in self.files:
                with open(os.path.join(self.cache_path, url_simple + ".html"), mode="r") as data_file:
                    html = data_file.read()
            else:
                html = request_url(url)
                with open(os.path.join(self.cache_path, url_simple + ".html"), mode="w") as data_file:
                    data_file.write(str(html))
                self.files.append(url_simple)
        else:
            html = request_url(url)
        return html

    # Checks whether caching is enabled for the given file
    def caching_allowed(self, url):
        if (
                self.overseer.caching["overviews"] and re.fullmatch(".*/(items|heroes)", url) or
                self.overseer.caching["items"] and re.fullmatch(".*/items/.*", url) or
                self.overseer.caching["heroes"] and re.fullmatch(".*/heroes/.[a-z\-]*", url) or
                self.overseer.caching["abilities"] and re.fullmatch(".*/heroes/.*/abilities", url)
           ):
            print("Caching: " + url)  # For debug purposes
            return True


# Retrieves the file specified by the url and returns it
def request_url(url):
    req = urllib.request.Request(url, headers={"User-Agent": "Mozilla/5.0"})
    html = urllib.request.urlopen(req).read()
    print("Requesting: " + url)  # For debug purposes
    return html
