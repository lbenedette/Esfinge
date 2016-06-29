# Esfinge

## Requisitos
* Python                3.5.1
* Flask                 0.11.1
* Flask-Login           0.3.2
* Flask-SQLAlchemy      2.1
* sqlalchemy-migrate    0.10.0
* bcrypt                2.0.0

## Como utilizar
1. Rode o programa utilizando o comando `python Esfinge.py`. Se você possuir mais de uma versão do Python instalada, pode ser necessário mudar o comando, por exemplo, para `python3 Esfinge.py`.
2. Ao rodar o programa, você verá uma linha `* Running on http://127.0.0.1:5000/ (Press CTRL+C to quit)` ou algo similar. Acesse este endereço através do navegador para acessar o Esfinge.
3. Ao entrar no Esfinge pela primeira vez, será necessário criar uma conta. Para isso, clique no link de "Ainda não possui uma conta? Registre-se clicando aqui."
4. Preencha com as suas informações (ainda não há verificação via email, portanto não precisa ser um email real) e clique em Criar Conta.
5. Ao ser redirecionado à página de login com uma mensagem de sucesso na criação da conta, entre com as credenciais cadastradas.
6. Você está agora na sua linha do tempo. Você pode criar novas perguntas e ver as perguntas das pessoas que você segue a partir desta página.
7. Para seguir outros usuários, basta entrar em sua página, cujo endereço é `[endereco_do_esfinge]/profile/[id_perfil]` trocando o endereço do esfinge pelo link mostrado no passo 2 e o ID do perfil pelo número que representa o perfil do usuário desejado.
8. Você pode responder às perguntas de outros usuários visualizando a página dos mesmos ou na sua timeline, caso você o siga.
9. Para visualizar seu próprio perfil, basta clicar em **Minha Página**, no topo da página.
10. Você pode excluir suas perguntas e respostas ou respostas às suas perguntas clicando no **x** próximo à pergunta/resposta.