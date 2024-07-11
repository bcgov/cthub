from dns.resolver import Resolver
from email_validator import caching_resolver


def get_google_resolver():
    resolver = Resolver()
    resolver.nameservers = ["8.8.8.8"]
    return caching_resolver(dns_resolver=resolver)
