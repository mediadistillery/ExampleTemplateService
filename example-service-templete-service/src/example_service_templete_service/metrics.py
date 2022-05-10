import prometheus_client as pc

__all__ = (
    'metrics',
)


class ServiceMetrics:
    def __init__(self) -> None:
        self.calls_counter = pc.Counter('dl_face_clustering_service_calls',
                                        'Amount of times the endpoint is called',
                                        labelnames=['endpoint'])

        self.failed_calls_counter = pc.Counter('dl_face_clustering_service_failed_calls',
                                               'Amount of times the endpoint is called & failed',
                                               labelnames=['endpoint'])

        self.request_duration_histogram = pc.Histogram('dl_face_clustering_service_seconds',
                                                       'Duration of requests in seconds',
                                                       labelnames=['path'])

    def called(self, endpoint: str) -> None:
        self.calls_counter.labels(endpoint).inc()

    def call_failed(self, endpoint: str) -> None:
        self.failed_calls_counter.labels(endpoint).inc()

    def request_duration(self, path: str, duration: float) -> None:
        self.request_duration_histogram.labels(path).observe(duration)


metrics = ServiceMetrics()  # singleton; there should only be one
