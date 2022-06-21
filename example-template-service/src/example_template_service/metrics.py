import prometheus_client as pc

__all__ = ('metrics',)


class ServiceMetrics:
    def __init__(self) -> None:
        self.calls_counter = pc.Counter(
            'example_template_service_calls', 'Amount of times the endpoint is called', labelnames=['endpoint']
        )

        self.failed_calls_counter = pc.Counter(
            'example_template_service_failed_calls',
            'Amount of times the endpoint is called & failed',
            labelnames=['endpoint'],
        )

    def called(self, endpoint: str) -> None:
        self.calls_counter.labels(endpoint).inc()

    def call_failed(self, endpoint: str) -> None:
        self.failed_calls_counter.labels(endpoint).inc()


metrics = ServiceMetrics()  # singleton; there should only be one
