from urllib.parse import urlparse
from types import SimpleNamespace
import argparse, os
import logging

from vectorsageui import VectorSageUI

# Setup logging
logging.basicConfig(level=logging.INFO)

def initialize_vector_sage(args: argparse.Namespace):
    """Initialize the application configuration from command line arguments and environment variables."""
    def is_valid_url(url):
        try:
            result = urlparse(url)
            # Check if the scheme and netloc are present
            return all([result.scheme, result.netloc])
        except ValueError:
            return False

    config = SimpleNamespace()

    host = args.llm_rag_services_host if args.llm_rag_services_host else os.environ.get("LLM_RAG_SERVICES_HOST", "")
    
    if is_valid_url(host):
        config.llm_rag_services_host = host
    else:
        logging.error("Invalid llm host string provided. Ensure proper URL format, e.g. http(s)://service.domain.com")
        exit(1)

    # Gradio
    config.listen_port = int(args.port if args.port else os.environ.get("PORT", "8080"))

    return vars(config)

if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("-l", "--llm_rag_services_host", help="The host providing llm services", type=str, required=False)
    parser.add_argument("-p", "--port", help="The listening port of that chat for browser access", type=int, required=False, default=8080)

    config = initialize_vector_sage(parser.parse_args())

    VectorSageUI(**config).start()