from confusable_homoglyphs import confusables
from django.contrib.auth import get_user_model
import re

User = get_user_model()

SPECIAL_HOSTNAMES = [
    # Hostnames with special/reserved meaning.
    "autoconfig",  # Thunderbird autoconfig
    "autodiscover",  # MS Outlook/Exchange autoconfig
    "broadcasthost",  # Network broadcast hostname
    "isatap",  # IPv6 tunnel autodiscovery
    "localdomain",  # Loopback
    "localhost",  # Loopback
    "wpad",  # Proxy autodiscovery
]

PROTOCOL_HOSTNAMES = [
    # Common protocol hostnames.
    "ftp",
    "imap",
    "mail",
    "news",
    "pop",
    "pop3",
    "smtp",
    "usenet",
    "uucp",
    "webmail",
    "www",
]

CA_ADDRESSES = [
    # Email addresses known used by certificate authorities during
    # verification.
    "admin",
    "administrator",
    "hostmaster",
    "info",
    "is",
    "it",
    "mis",
    "postmaster",
    "root",
    "ssladmin",
    "ssladministrator",
    "sslwebmaster",
    "sysadmin",
    "webmaster",
]

RFC_2142 = [
    # RFC-2142-defined names not already covered.
    "abuse",
    "marketing",
    "noc",
    "sales",
    "security",
    "support",
]

NOREPLY_ADDRESSES = [
    # Common no-reply email addresses.
    "mailer-daemon",
    "nobody",
    "noreply",
    "no-reply",
]

SENSITIVE_FILENAMES = [
    # Sensitive filenames.
    "clientaccesspolicy.xml",  # Silverlight cross-domain policy file.
    "crossdomain.xml",  # Flash cross-domain policy file.
    "favicon.ico",
    "humans.txt",
    "keybase.txt",  # Keybase ownership-verification URL.
    "robots.txt",
    ".htaccess",
    ".htpasswd",
]

OTHER_SENSITIVE_NAMES = [
    # Other names which could be problems depending on URL/subdomain
    # structure.
    "account",
    "accounts",
    "blog",
    "buy",
    "clients",
    "contact",
    "contactus",
    "contact-us",
    "copyright",
    "dashboard",
    "doc",
    "docs",
    "download",
    "downloads",
    "enquiry",
    "faq",
    "help",
    "inquiry",
    "license",
    "login",
    "logout",
    "me",
    "myaccount",
    "payments",
    "plans",
    "portfolio",
    "preferences",
    "pricing",
    "privacy",
    "profile",
    "register" "secure",
    "settings",
    "signin",
    "signup",
    "ssl",
    "status",
    "subscribe",
    "terms",
    "tos",
    "user",
    "users",
    "weblog",
    "work",
    "activate",
    "password_reset",
    "reset",
    "check_authentication"
]

DEFAULT_RESERVED_NAMES = (*SPECIAL_HOSTNAMES,
                          *PROTOCOL_HOSTNAMES,
                          *CA_ADDRESSES,
                          *RFC_2142,
                          *NOREPLY_ADDRESSES,
                          *SENSITIVE_FILENAMES,
                          *OTHER_SENSITIVE_NAMES)

# errors
large_length = "Имя пользователя больше 20-ти символов"
forbidden_characters = "Имя пользователя может содержать только буквы и символы @ + . _ -"
username_is_busy = "Имя пользователя занято"
confusable = "Имя пользователя занято"
reserved_name = "Имя пользователя не может быть зарегистрировано"
empty_username = "Имя пользователя не может быть пустым"

class UsernameValidator(object):
    """Checks the username for validity and returns a list with errors otherwise"""

    def __init__(self, reserved_names=DEFAULT_RESERVED_NAMES):
        self.reserved_names = reserved_names
        self.errors = []

    def __validate_length(self, username):
        if len(username) > 20:
            self.errors.append(large_length)
        if len(username) <1:
            self.errors.append(empty_username)

    def __validate_reserved(self, value):
        if value in self.reserved_names or value.startswith(".well-known"):
            self.errors.append(reserved_name)

    def __validate_confusables(self, value):
        if confusables.is_dangerous(value):
            self.errors.append(confusable)

    def __character_validation(self, username):
        pattern = r'^[a-zA-Zа-яА-Я0-9@+._-]+$'
        if re.match(pattern, username) is None:
            self.errors.append(forbidden_characters)

    def __checking_uniqueness(self, input_username):
        if User.objects.filter(username=input_username).exists():
            self.errors.append(username_is_busy)

    def validate_all(self, username):
        if isinstance(username, str):
            self.__validate_reserved(username)
            self.__validate_confusables(username)
            self.__character_validation(username)
            self.__validate_length(username)
            self.__checking_uniqueness(username)
        else:
            raise Exception('Имя пользователя должно быть строкой')
        return self.errors
