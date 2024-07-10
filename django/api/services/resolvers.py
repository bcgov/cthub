from dns.resolver import Resolver


def get_google_resolver():
    resolver = Resolver()
    resolver.nameservers = ["8.8.8.8"]
    return resolver
