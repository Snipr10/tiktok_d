from pyppeteer import chromium_downloader

# from utils.logging import get_logger

# logger = get_logger(__name__)

# from pyppeteer.__chromium_revision__
DEFAULT_CHROMIUM_VERSION = '588429'


def set_chromium_version(chromium_version):
    if not chromium_version:
        chromium_version = DEFAULT_CHROMIUM_VERSION

    chromium_downloader.REVISION = chromium_version

    chromium_downloader.downloadURLs = {
        'linux': f'{chromium_downloader.BASE_URL}/Linux_x64/{chromium_downloader.REVISION}/chrome-linux.zip',
        'mac': f'{chromium_downloader.BASE_URL}/Mac/{chromium_downloader.REVISION}/chrome-mac.zip',
        'win32': f'{chromium_downloader.BASE_URL}/Win/{chromium_downloader.REVISION}/{chromium_downloader.windowsArchive}.zip',
        'win64': f'{chromium_downloader.BASE_URL}/Win_x64/{chromium_downloader.REVISION}/{chromium_downloader.windowsArchive}.zip',
    }

    chromium_downloader.chromiumExecutable = {
        'linux': chromium_downloader.DOWNLOADS_FOLDER / chromium_downloader.REVISION / 'chrome-linux' / 'chrome',
        'mac': chromium_downloader.DOWNLOADS_FOLDER / chromium_downloader.REVISION / 'chrome-mac' / 'Chromium.app' / 'Contents' / 'MacOS' / 'Chromium',
        'win32': chromium_downloader.DOWNLOADS_FOLDER / chromium_downloader.REVISION / chromium_downloader.windowsArchive / 'chrome.exe',
        'win64': chromium_downloader.DOWNLOADS_FOLDER / chromium_downloader.REVISION / chromium_downloader.windowsArchive / 'chrome.exe',
    }
    #
    # logger.info(f"Using chromium revision = {chromium_version}")
    # logger.info(f"chromium_executable = {chromium_downloader.chromium_executable()}")


def revert_to_original_chromium_version():
    set_chromium_version(DEFAULT_CHROMIUM_VERSION)


def download_chromium(chromium_version=None):
    try:
        set_chromium_version(chromium_version)
        if not chromium_downloader.check_chromium():
            # logger.info(f"Downloading chromium from {chromium_downloader.get_url()}")
            chromium_downloader.download_chromium()
    finally:
        revert_to_original_chromium_version()
