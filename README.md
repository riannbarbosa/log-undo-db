# **BANCO DE DADOS II - LOG UNDO (EM PYTHON)**

Univeridade Federal da Fronteira Sul - Campus Chapecó

Ciência da Computação - Banco de Dados II – 2023.1

Prof. Guilherme Dal Bianco

Acadêmico: **Rian Borges Barbosa**


---


## 💾 **Implementando o Mecanismo de UNDO LOGGING com Checkpoint**

### **Objetivo**
Implementar o mecanismo de log Undo com checkpoint usando o SGBD 

### **Funcionamento**
O código, que poderá utilizar qualquer linguagem de programação, deverá ser capaz de ler o arquivo de log (entradaLog) e o arquivo de Metadado e validar as informações no banco de dados através do modelo UNDO. 
O código receberá como entrada o arquivo de metadados (dados salvos) e os dados da tabela que irá operar no banco de dados. 


### **Detalhes**:
Funções a implementadas:
1. Carregar o banco de dados com a tabela antes de executar o código do log (para zerar as configurações e dados parciais);
2. Carregar o arquivo de log;
3. Verifique quais transações devem realizar REDO. Imprimir o nome das transações que irão sofrer REDO.
4. Checar quais valores estão salvos nas tabelas e atualizar valores inconsistentes;
5. Reportar quais dados foram atualizados;
6. Seguir o fluxo de execução conforme o método de REDO.


---


## 🚀 **Começando**

### **1. Dependências**
Para executar o projeto você vai precisar:
- [Python 3.x](https://www.python.org/downloads/)
- [Postgres 14.x](https://www.postgresql.org/download/)

### **2. Configuração**

Feito a instalação das dependências do projeto, é necessário obter uma cópia do projeto.

Para isso, rode:

``` powershell
git clone --recurse-submodules https://github.com/Dutraz/db-log-redo && cd db-log-redo
```

#### **2.1 Python**

Serão necessárias algumas dependências para que o projeto rode corretamente.
Para isso localize a pasta 'Requirements.txt' e rode o comando abaixo:

``` powershell
pip install -r requirements.txt
```
#### **2.2 Banco de Dados**

O projeto usa o banco de dados padrão do postgres, mas para usar o seu, apenas modifique o .env com a configuração do seu banco localizado na pasta do projeto. 

``` SQL
CREATE DATABASE logredo;
```

---


## 📋 **Testando:**

Entre na pasta src com o comando:
``` powershell
cd src
```

E então, execute o projeto com:
``` powershell
python main.py
```

---


## 📋 **Descrição:**

Dado um *Arquivo de Metadados (json)*, como:
```javascript
{  
    "INITIAL": {
        "A": [20,20],
        "B": [55,30]
    }
}
```

O programa deve ser capaz de criar e preencher uma *tabela do banco de dados* como segue:

|  ID  |  A  |  B  |
|------|-----|-----|
|  01  |  20 |  55 |
|  02  |  20 |  30 |


Após isso, o programa deve ler o *arquivo de log* que segue o formato:

><transação, “id da tupla”, ”coluna”, “valor antigo”, “valor novo”>.

```html
<start T1>
<T1,1,A,20,500>
<start T2>
<commit T1>
<CKPT (T2)>
<T2,2,A,20,50>
<start T3>
<start T4>
<commit T2>
<T4,1,B,20,100>
```

E por fim identificar e realizar todos os REDO's necessários para que haja a integridade do banco de dados. Retornando a saída como:

>Transação T2 realizou REDO

>Transação T3 não realizou REDO

>Transação T4 não realizou REDO
 
>```javascript
>{  
>    "INITIAL": {
>        "A": [500,20],
>        "B": [20,30]
>    }
>}
>```