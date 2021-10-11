import docker
import dockerpty

client = docker.Client()
container = client.create_container(
image='foilv/tournaments_go:bot15',
   stdin_open=True,
   tty=True,
   command='/bin/sh',
)
client.start(container)
dockerpty.PseudoTerminal(client, container).start()