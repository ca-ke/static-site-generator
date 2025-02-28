
## Visitor Pattern
Um Design Pattern que permite que você adicione novos comportamentos a uma classe sem que você modifique o código original dela. Ao invés de modificarmos a classe, criamos um "visitante" que contém a lógica extra a ser executada.

1. Cria-se uma interface Visitor que define diferente métodos de visita para cada tipo de objeto.
2. Cada classe de estrutura aceita um visitante, chamando o método correspondente (accept(visitor))
