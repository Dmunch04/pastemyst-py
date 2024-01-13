class API(object):
    """
    API class

    This class provides access to the API endpoints for interacting with the given host.

    Attributes:
        HOST (str): The main host URL.
        BETA_HOST (str): The beta host URL.
        API_VERSION (int): The API version.
        HTTP_ENDPOINT (str): The main HTTP endpoint URL.
        BETA_HTTP_ENDPOINT (str): The beta HTTP endpoint URL.

    """

    HOST: str = "https://paste.myst.rs"
    BETA_HOST: str = "https://pmb.myst.rs"
    API_VERSION: int = 2
    HTTP_ENDPOINT: str = f"{HOST}/api/v{API_VERSION}"
    BETA_HTTP_ENDPOINT: str = f"{BETA_HOST}/api/v{API_VERSION}"
