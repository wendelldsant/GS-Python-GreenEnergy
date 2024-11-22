# Sun Catcher - Plataforma de Monitoramento Solar ☀️  
**Desenvolvido por:** Wendell dos Santos Silva - RM558859  

---

## 📖 Sobre o Projeto  
**Sun Catcher** é uma plataforma de monitoramento inteligente para dispositivos de rastreamento solar, projetada para otimizar sistemas de energia limpa.  
- O projeto foi desenvolvido como parte da **Global Solution 2024**, cujo tema principal é a geração de energia sustentável.  
- **Trabalho solo:** Este projeto foi criado inteiramente por mim, sem a colaboração de outros membros.  

A plataforma permite que usuários:
- Cadastrem dispositivos solares.
- Monitorem dados em tempo real (simulados no código).  
- Gerenciem configurações dos dispositivos cadastrados.

Os dados monitorados pelos dispositivos são fictícios, criados por funções no código, mas simulam condições reais de operação.  

---

## 🛠️ Requisitos  
Certifique-se de atender aos seguintes requisitos para executar o projeto:  
1. **Python 3.8 ou superior** instalado no sistema.  
2. **MongoDB** instalado e em execução no endereço `localhost:27017`.  
   - Para instalação e configuração do MongoDB, siga a [documentação oficial](https://www.mongodb.com/try/download/community).  
3. Instale a biblioteca necessária utilizando o `pip`:  
   ```bash
   pip install pymongo
   
 ---  
 
## 🚀 Como Rodar o Código

Certifique-se de que o MongoDB está em execução no endereço localhost:27017.

- Clone ou faça o download deste repositório.
- Abra o terminal e navegue até o diretório do projeto.
- Execute o script principal:
python nome_do_arquivo.py
- A plataforma será iniciada no terminal, apresentando o menu inicial com as opções de:
1. Cadastro
2. Login
3. Gerenciamento de Dispositivos

## 🗂️ Estrutura do Projeto

Cadastro de Usuários:
- Criação de contas com nome de usuário e senha seguros.
- A senha deve conter:
1. Pelo menos uma letra maiúscula e minúscula.
2. Um número.
3. Um caractere especial.

Login:
- O usuário faz login utilizando suas credenciais cadastradas.
  
Gerenciamento de Dispositivos:
- Dispositivos podem ser adicionados ao perfil do usuário utilizando IDs pré-definidos.
- Cada dispositivo recebe um apelido personalizado.

Simulação de Dados:
- Dados fictícios são gerados para os dispositivos (como leituras de sensores e ângulos).

Edição e Exclusão de Conta:
- Alteração de nome de usuário e senha.
- Exclusão da conta do sistema.
- Estrutura do Banco de Dados
- Banco de Dados: SunCatcher

Coleções:
- users: Contém informações dos usuários cadastrados.
- devices: Contém dispositivos disponíveis para registro.

Dispositivos Disponíveis para Simulação:
- IDs disponíveis ao iniciar o código:
- 1234
- 6969
- 5151
- 2424

## 🌟 Contribuições e Créditos
- Este projeto foi desenvolvido por Wendell dos Santos Silva - RM558859 como parte de um desafio acadêmico.

Wendell dos Santos Silva - RM558859
