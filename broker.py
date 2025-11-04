import zmq

def main():
    context = zmq.Context()
    frontend = context.socket(zmq.XSUB)
    frontend.bind(f"tcp://*:{CLIENT_PUBLISH_PORT}")
    backend = context.socket(zmq.XPUB)
    backend.bind(f"tcp://*:{CLIENT_SUBSCRIBE_PORT}")
    print(f"Broker iniciado. Escutando publicações na porta {CLIENT_PUBLISH_PORT} e distribuindo na porta {CLIENT_SUBSCRIBE_PORT}.")
    try:
        zmq.proxy(frontend, backend)
    except KeyboardInterrupt:
        print("Broker encerrado.")
    finally:
        frontend.close()
        backend.close()
        context.term()

if __name__ == "__main__":
    from constPS import CLIENT_PUBLISH_PORT, CLIENT_SUBSCRIBE_PORT
    main()
