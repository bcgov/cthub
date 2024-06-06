import logging

class HealthcheckFilter(logging.Filter):
     def filter(self, record):
         msg = record.getMessage()
         if "GET /api/healthcheck HTTP/1.1" in msg:
              return False
         return True