""" Módulo que implementa nó de árvore de busca."""

class Node:
    """ Classe que implementa nó de árvore de busca."""

    def __init__(self, parent):
        """ Construtor do nó.

        Parameters:
            parent (Node): pai do nó construído.
        """
        self.parent = parent
        self.state = None   # estado
        self.custo_gn = 0        # g(n) custo acumulado até o nó
        self.custo_hn = 0        # h(n) heurística a partir do nó
        self.depth = 0      # armazena a profundidade do nó
        self.children = []
        self.action = 0    # ação que levou ao estado
        self.direction = 0

    def set_gn_hn(self, custo_gn, custo_hn):
        """ Atribui valores aos atributos gn e hn.

        Parameters:
            custo_gn (double): representa o custo acumulado da raiz até o nó.
            custo_hn (double): representa o valor da heurística do nó até o objetivo.
        """
        self.custo_gn = custo_gn
        self.custo_hn = custo_hn

    def get_fn(self):
        """Retorna o valor da função de avaliação f(n).

        Returns:
            double: valor da funcão de avaliacão f(n)
        """
        return self.custo_gn + self.custo_hn

    def add_child(self):
        """ Este método instância um nó de self e cria uma associação entre o pai(self) e o filho.

        Returns
            None: Instância tipo Node com o nó filho criado.
        """
        child = Node(self)
        child.depth = self.depth + 1
        self.children.append(child)
        return child

    def remove(self):
        """Remove-se da árvore cortando a ligação com o nó pai."""
        removed = self.parent.children.remove(self)
        if not removed:
            print("### Erro na remoção do nó: {}".format(self))

    def __str__(self):
        return "<{0} g:{1:.2f} h:{2:.2f} f:{3:.2f}>".format(self.state,
                                                            self.custo_gn,
                                                            self.custo_hn,
                                                            self.get_fn())
