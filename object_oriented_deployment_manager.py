class Deployment:
    """
    Manages the state and version history of a software deployment.
    """

    def __init__(self, service_name: str, environment: str):
        """
        Initializes a new Deployment instance.
        """

        # ---- Input validation ----
        if not isinstance(service_name, str):
            raise TypeError("service_name must be a string")

        if not isinstance(environment, str):
            raise TypeError("environment must be a string")

        if not service_name:
            raise ValueError("service_name must not be empty")

        if not environment:
            raise ValueError("environment must not be empty")

        # ---- State initialization ----
        self.service_name = service_name
        self.environment = environment
        self.status = "pending"
        self._history = []

    def deploy(self, new_version: str):
        """
        Deploys a new version by adding it to the history.
        """

        # ---- Input validation ----
        if not isinstance(new_version, str):
            raise TypeError("new_version must be a string")

        if not new_version:
            raise ValueError("new_version must not be empty")

        # ---- Core logic ----
        self._history.append(new_version)
        self.status = "deployed"

    def rollback(self) -> bool:
        """
        Rolls back to the previous version by removing the current one from history.
        """

        if len(self._history) < 2:
            return False

        self._history.pop()
        self.status = "rolled_back"
        return True

    def check_status(self) -> dict:
        """
        Returns a dictionary representing the current state of the deployment.
        """

        current_version = self._history[-1] if self._history else None

        return {
            "service_name": self.service_name,
            "environment": self.environment,
            "version": current_version,
            "status": self.status,
        }

d = Deployment("payments", "prod")
print(d.check_status())

d.deploy("v1.0")
print(d.check_status())

d.deploy("v1.1")
print(d.check_status())

d.rollback()
print(d.check_status())
