class Deployment:
    def __init__(self, service_name: str, environment: str):
        """
        Initialize a Deployment.

        - status starts as 'pending'
        - no deployed version (None)
        - keep a history stack of previous versions to support rollback
        """
        self.service_name = service_name
        self.environment = environment
        self.status = "pending"
        self._current_version = None
        self._history = []

    def deploy(self, new_version: str):
        """
        Deploy a new version:
        - if there is a current version, push it onto history
        - set the current version to new_version
        - mark status as 'deployed'
        """
        if self._current_version is not None:
            self._history.append(self._current_version)
        self._current_version = new_version
        self.status = "deployed"

    def rollback(self) -> bool:
        """
        Roll back to the immediately previous version.
        - If there is no previous version, return False.
        - Otherwise, pop the previous version from history, make it current,
          set status to 'rolled_back' and return True.
        """
        if not self._history:
            return False

        previous = self._history.pop()
        self._current_version = previous
        self.status = "rolled_back"
        return True

    def check_status(self) -> dict:
        """
        Return the status dictionary:
        {
            'service_name': ...,
            'environment': ...,
            'status': 'pending'|'deployed'|'rolled_back',
            'version': <current version string or None>
        }
        """
        return {
            "service_name": self.service_name,
            "environment": self.environment,
            "status": self.status,
            "version": self._current_version,
        }
    
d = Deployment("payment-service", "staging")
print(d.check_status())
# {'service_name': 'payment-service', 'environment': 'staging', 'status': 'pending', 'version': None}

d.deploy("v1.0.0")
print(d.check_status())
# status -> 'deployed', version -> 'v1.0.0'

d.deploy("v1.1.0")
print(d.check_status())
# version -> 'v1.1.0', history contains ['v1.0.0']

ok = d.rollback()
print(ok)            # True
print(d.check_status())
# status -> 'rolled_back', version -> 'v1.0.0'

ok = d.rollback()
print(ok)            # False (no earlier history)
