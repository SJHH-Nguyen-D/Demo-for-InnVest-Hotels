"""
These are all constants for use in any of the python scripts within /v1/
"""
import re

PATTERNSTOREMOVE = (
    "<.*?>",
    "</.*?>",
    r"<iframe.*?</iframe",
    r"<link.*?\s/",
    "<div.*?</div",
    "&lt;iframe(.*?)&gt;",
    "It appears you are trying to access this site using an outdated browser. As a result, parts of the site may not function properly for you. We recommend updating your browser to its most recent version at your earliest convenience.",
)


TAG_RM = {
    "role": [
        "complementary",
        "button",
        "dialog",
        "search",
        "contentinfo",
    ],
    "id": [
        "footerSocialContainer",
        "footerNav",
        "contactMainContainer",
        "def-top",
        "logo",
        "headerLeft",
        "headerInner",
        "headerRight",
        "headerRightTop",
        "topNav",
        "headerRightBottom",
        "pageHeading",
        "actions",
        "Share",
        "banner",
        "emergencyBarWrapper",
        "actionsContainer",
        "navTab01",
        "subNavWrapper",
        "bottomInteriorLinks",
        "footerInner",
        "emergencyBarWrapper",
        "skipContentWrapper",
        "subNavBtn",
        "breadcrumbs",
    ],
    "class": ["twoBoxes", "global-header"],
}

EMOJI_PATTERNS = re.compile(
    "["
    "\U0001F600-\U0001F64F"  # emoticons
    "\U0001F300-\U0001F5FF"  # symbols & pictographs
    "\U0001F680-\U0001F6FF"  # transport & map symbols
    "\U0001F1E0-\U0001F1FF"  # flags (iOS)
    "\U00002500-\U00002BEF"  # chinese char
    "\U00002702-\U000027B0"
    "\U00002702-\U000027B0"
    "\U000024C2-\U0001F251"
    "\U0001f926-\U0001f937"
    "\U00010000-\U0010ffff"
    "\u2640-\u2642"
    "\u2600-\u2B55"
    "\u200d"
    "\u23cf"
    "\u23e9"
    "\u231a"
    "\ufe0f"  # dingbats
    "\u3030"
    "\u23f0"
    "\u00A9"
    "\uf0b7"
    "\uf0d8"
    "]+",
    flags=re.UNICODE,
)

EXCLUDE_WEBSITES = ["facebook.com", "twitter.com"]

URL_PARTS_EXCLUDED = ["https:", "http:", "aspx", "html", "htm", "www", "com", "ca"]

PREPROCESSOR_CONFIG = {
    "patterns": PATTERNSTOREMOVE,
}

FILE_EXTS = [
    "csv",
    "json",
    "pdf",
    "doc",
    "docx",
    "odt",
    "txt",
    "xls",
    "xlsx",
    "ppt",
    "pptx",
]

EXCLUDED_LANGUAGES = [
    "fra",
    "fil",
    "pt-br",
    "es",
    "pa",
    "ko",
    "ar",
    "it",
    "ru",
    "ur",
    "pl",
    "zh-hant",
    "zh-hans",
]

SUBSTRINGS = [
    "www.canada.ca",
    "about-us",
    "about",
    "contact-us",
    "contact",
    "login",
]

EXTRACTOR_CONFIG = {
    "excluded languages": EXCLUDED_LANGUAGES,
    "file extension": FILE_EXTS,
    "exclude pages": SUBSTRINGS,
}

BUSINESS_STAGE_MAP = {}

PDF_DATA = {"IMAGE": "/XObject", "TEXT": "/Font", "ALL_DATA": "/Resources"}

TABLE_TYPES = ["pages", "resources", "forms", "images", "metadata", "jsonlines"]
