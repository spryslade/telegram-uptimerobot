import requests

from typing import List


class UptimeRobot:
    """Small UptimeRobot wrapper class"""
    class MonitorLog:
        """Container class for monitor log objects"""
        def __init__(self, datetime: int, duration: int, status_code: int, status_reason: str):
            self.datetime: int = datetime
            self.duration: int = duration
            self.status_code: int = status_code
            self.status_reason: str = status_reason

        def dict(self) -> dict:
            """Returns self as dictionary"""
            return {
                'datetime': self.datetime,
                'duration': self.duration,
                'status_code': self.status_code,
                'status_reason': self.status_reason
            }

    class Monitor:
        """Container class for monitor objects"""
        STATUSES = {
            0: 'paused',
            1: 'not checked yet',
            2: 'up',
            8: 'down (maybe?)',
            9: 'down'
        }

        def __init__(self, id: int, friendly_name: str, url: str, status: int, create_datetime: int, logs: List):
            self.id: int = id
            self.friendly_name: str = friendly_name
            self.url: str = url
            self.status: str = self.STATUSES[status]
            self.create_datetime: int = create_datetime
            self.logs: List[UptimeRobot.MonitorLog] = logs

        def dict(self) -> dict:
            return {
                'id': self.id,
                'friendly_name': self.friendly_name,
                'url': self.url,
                'status': self.status,
                'create_datetime': self.create_datetime,
                'logs': [log.dict() for log in self.logs]
            }

    def __init__(self, api_token: str):
        self.api_key: str = api_token
        self.UPTIMEROBOT_API_ENDPOINT: str = 'https://api.uptimerobot.com/v2/'
        self.UPTIMEROBOT_GET_MONITORS_API: str = 'getMonitors'

    def get_monitors(self) -> List[Monitor]:
        """Return list of monitors from UptimeRobot API"""
        response = requests.post(self.UPTIMEROBOT_API_ENDPOINT + self.UPTIMEROBOT_GET_MONITORS_API,
                                 data={'api_key': self.api_key, 'format': 'json', 'logs': 1}).json()['monitors']
        return [self.Monitor(monitor['id'], monitor['friendly_name'], monitor['url'], monitor['status'],
                             monitor['create_datetime'], [self.MonitorLog(log['datetime'], log['duration'],
                                                                          log['reason']['code'], log['reason']['detail'])
                                                          for log in monitor['logs']]) for monitor in response]
