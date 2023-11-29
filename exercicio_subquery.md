### Exercícios com Subqueries em Banco de Dados

#### Exercício 1:
Considere as seguintes tabelas:

**Tabela 1: Funcionários**
| ID | Nome | Departamento |
|----|------|--------------|
| 1  | João | Vendas       |
| 2  | Maria| RH           |
| 3  | Pedro| Vendas       |

**Tabela 2: Vendas**
| ID | Funcionário_ID | Valor |
|----|----------------|-------|
| 1  | 1              | 200   |
| 2  | 2              | 150   |
| 3  | 3              | 300   |

Escreva uma consulta que retorne o nome dos funcionários que realizaram vendas acima da média de vendas da empresa.

#### Exercício 2:
Considere as seguintes tabelas:

**Tabela 1: Produtos**
| ID | Nome     | Preço |
|----|----------|-------|
| 1  | Celular  | 1000  |
| 2  | Notebook | 2000  |
| 3  | Tablet   | 800   |

**Tabela 2: Vendas**
| ID | Produto_ID | Quantidade |
|----|------------|------------|
| 1  | 1          | 5          |
| 2  | 2          | 3          |
| 3  | 3          | 8          |

Escreva uma consulta que retorne o nome e preço dos produtos que tiveram vendas acima da média de quantidade de vendas.