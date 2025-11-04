import zmq
import threading
import sys
import time
from constPS import *

def receiver_thread(sub_socket, stop_event):
    while not stop_event.is_set():
        try:
            if sub_socket.poll(timeout=500):
                message = sub_socket.recv_string()
                sys.stdout.write('\r' + ' ' * 80 + '\r')
                print(message)
                sys.stdout.write(f'[{username} @ {current_topic or "Nenhum Canal"}]> ')
                sys.stdout.flush()
        except zmq.ZMQError:
            break

def main():
    global username, current_topic

    username = input("Digite seu nome de usuário: ")
    initial_topic = input("Digite o canal inicial que deseja entrar (ex: #geral): ")

    if not initial_topic.startswith('#'):
        initial_topic = '#' + initial_topic

    subscribed_topics = {initial_topic}
    current_topic = initial_topic

    context = zmq.Context()
    stop_event = threading.Event()

    sub_socket = context.socket(zmq.SUB)
    sub_socket.connect(f"tcp://{HOST}:{CLIENT_SUBSCRIBE_PORT}")
    sub_socket.setsockopt_string(zmq.SUBSCRIBE, initial_topic)

    pub_socket = context.socket(zmq.PUB)
    pub_socket.connect(f"tcp://{HOST}:{CLIENT_PUBLISH_PORT}")

    receiver = threading.Thread(target=receiver_thread, args=(sub_socket, stop_event))
    receiver.start()

    time.sleep(1)

    print("\nBem-vindo ao chat! Digite /help para ver os comandos.")

    try:
        while not stop_event.is_set():
            prompt = f'[{username} @ {current_topic or "Nenhum Canal"}]> '
            try:
                message_input = input(prompt)
            except EOFError:
                stop_event.set()
                continue

            if message_input.startswith('/'):
                parts = message_input.split(' ', 1)
                command = parts[0].lower()

                if command == '/quit':
                    stop_event.set()

                elif command == '/help':
                    print("\nComandos disponíveis:")
                    print("  /join <#topico>   - Entra em um novo canal.")
                    print("  /leave <#topico>  - Sai de um canal.")
                    print("  /switch <#topico> - Muda o seu canal ativo.")
                    print("  /quit             - Sai do chat.\n")

                elif command == '/join':
                    if len(parts) > 1 and parts[1].startswith('#'):
                        new_topic = parts[1]
                        if new_topic not in subscribed_topics:
                            subscribed_topics.add(new_topic)
                            sub_socket.setsockopt_string(zmq.SUBSCRIBE, new_topic)
                            print(f"Você entrou no canal: {new_topic}")
                        else:
                            print(f"Você já está no canal: {new_topic}")
                    else:
                        print("Uso inválido. Formato: /join <#topico>")

                elif command == '/leave':
                    if len(parts) > 1 and parts[1].startswith('#'):
                        topic_to_leave = parts[1]
                        if topic_to_leave in subscribed_topics:
                            sub_socket.setsockopt_string(zmq.UNSUBSCRIBE, topic_to_leave)
                            subscribed_topics.remove(topic_to_leave)
                            print(f"Você saiu do canal: {topic_to_leave}")

                            if topic_to_leave == current_topic:
                                if subscribed_topics:
                                    new_active = next(iter(subscribed_topics))
                                    current_topic = new_active
                                    print(f"Canal ativo foi alterado para: {current_topic}")
                                else:
                                    current_topic = None
                                    print("Você saiu do seu último canal. Use /join para entrar em um novo.")
                        else:
                            print(f"Você não está no canal {topic_to_leave}.")
                    else:
                        print("Uso inválido. Formato: /leave <#topico>")

                elif command == '/switch':
                    if len(parts) > 1 and parts[1].startswith('#'):
                        new_topic = parts[1]
                        if new_topic in subscribed_topics:
                            current_topic = new_topic
                        else:
                            print(f"Você não está no canal {new_topic}. Use /join {new_topic} primeiro.")
                    else:
                        print("Uso inválido. Formato: /switch <#topico>")
                else:
                    print(f"Comando desconhecido: {command}")
            else:
                if not current_topic:
                    print("Você não está em um canal ativo. Use /join para entrar ou /switch para ativar um.")
                elif message_input:
                    full_message = f"{current_topic} [{username}]: {message_input}"
                    pub_socket.send_string(full_message)

    except KeyboardInterrupt:
        print("\nSaindo do chat (Ctrl+C pressionado)...")
        stop_event.set()
    finally:
        print("Encerrando conexões...")
        receiver.join(timeout=2)
        sub_socket.close()
        pub_socket.close()
        context.term()
        print("Até logo!")

if __name__ == "__main__":
    main()
