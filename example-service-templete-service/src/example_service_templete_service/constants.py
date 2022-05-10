DEFAULT_CONFIG_PATH = '/etc/md-dl-face-clustering-service/dlfaceclustering-config.yaml'
DEFAULT_SERVICE_PORT = 5000
DEFAULT_PROMETHEUS_PORT = 8080
DEFAULT_SILENCE_KLEIN_LOGS = True
DEFAULT_MAX_WORKERS = 4
DEFAULT_LOG_LEVEL = 'info'
LOCALHOST = '127.0.0.1'
PROJECT_NAME = 'service-templete-test-service'
PROJECT_DESCRIPTION = 'Face Clustering Service'
API_VERSION_PREFIX = '/api/1'

PREPROCESSOR_PCA_ENABLED_KEY = 'preprocessors.pca.enabled'
PREPROCESSOR_PCA_ENABLED_DEFAULT = True
PREPROCESSOR_PCA_COMPONENTS_KEY = 'preprocessors.pca.components'
PREPROCESSOR_PCA_COMPONENTS_DEFAULT = 60

PREPROCESSOR_VECTOR_NORM_ENABLED_KEY = 'preprocessors.vectorNorm.enabled'
PREPROCESSOR_VECTOR_NORM_ENABLED_DEFAULT = True
PREPROCESSOR_VECTOR_NORM_MIN_NORM_KEY = 'preprocessors.vectorNorm.minNorm'
PREPROCESSOR_VECTOR_NORM_MIN_NORM_DEFAULT = 6.5

HDBSCAN_CLUSTERER_DISTANCE_METRIC_KEY = 'clusterer.hdbscan.distanceMetric'
HDBSCAN_CLUSTERER_DISTANCE_METRIC_DEFAULT = 'cosine' #or euclidean
