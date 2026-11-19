from puzzle.base_search import BaseSearch
from puzzle.state import State
from puzzle.result import SearchResult

DEFAULT_DEPTH_LIMIT = 50


class DFS(BaseSearch):

    def __init__(self, depth_limit: int = DEFAULT_DEPTH_LIMIT):
        self.depth_limit = depth_limit

    def search(self, initial: State) -> SearchResult:
        """Busca em Profundidade com limite: expande sempre o nó mais profundo (fronteira LIFO).

        - Nenhum nó com profundidade maior que `self.depth_limit` é gerado.
        - Para cada estado guarda a menor profundidade em que ele já foi alcançado.
          Um estado só volta para a pilha se for alcançado por um caminho mais curto;
          assim a busca não fica presa em ciclos e não perde soluções dentro do limite.
        - A solução encontrada não é necessariamente a ótima.
        """
        nos_gerados = 1          # o estado inicial conta como gerado
        nos_expandidos = 0

        if initial.is_goal:
            return SearchResult(initial, nos_expandidos, nos_gerados, 1, 0)

        fronteira = [initial]    # lista usada como pilha (LIFO)
        menor_profundidade = {initial.tiles: 0}
        max_fronteira = len(fronteira)

        while fronteira:
            no = fronteira.pop()
            profundidade = no.cost - initial.cost

            # Entrada obsoleta: o estado já foi empilhado de novo por um caminho mais curto.
            if menor_profundidade[no.tiles] < profundidade:
                continue
            # Limite de profundidade atingido: o nó não é expandido.
            if profundidade >= self.depth_limit:
                continue

            nos_expandidos += 1

            # Empilha em ordem invertida para que o primeiro filho (UP) seja explorado primeiro.
            for filho in reversed(no.neighbors()):
                nos_gerados += 1
                profundidade_filho = profundidade + 1

                if filho.is_goal:
                    return SearchResult(
                        solution=filho,
                        nodes_expanded=nos_expandidos,
                        nodes_generated=nos_gerados,
                        max_frontier_size=max_fronteira,
                        depth=profundidade_filho,
                    )

                anterior = menor_profundidade.get(filho.tiles)
                if anterior is not None and anterior <= profundidade_filho:
                    continue
                menor_profundidade[filho.tiles] = profundidade_filho
                fronteira.append(filho)

            max_fronteira = max(max_fronteira, len(fronteira))

        # Pilha vazia: não existe solução dentro do limite de profundidade.
        return SearchResult(None, nos_expandidos, nos_gerados, max_fronteira, 0)
