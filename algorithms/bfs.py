from collections import deque
from puzzle.base_search import BaseSearch
from puzzle.state import State
from puzzle.result import SearchResult


class BFS(BaseSearch):

    def search(self, initial: State) -> SearchResult:
        """Busca em Largura: expande sempre o nó menos profundo (fronteira FIFO).

        Busca em grafo: estados já alcançados não entram de novo na fronteira.
        O teste de objetivo é feito na geração do filho, o que mantém a solução
        ótima (todos os movimentos custam 1) e evita expandir um nível inteiro a mais.
        """
        nos_gerados = 1          # o estado inicial conta como gerado
        nos_expandidos = 0

        if initial.is_goal:
            return SearchResult(initial, nos_expandidos, nos_gerados, 1, 0)

        fronteira = deque([initial])
        alcancados = {initial.tiles}
        max_fronteira = len(fronteira)

        while fronteira:
            no = fronteira.popleft()
            nos_expandidos += 1

            for filho in no.neighbors():
                nos_gerados += 1
                if filho.tiles in alcancados:
                    continue
                if filho.is_goal:
                    return SearchResult(
                        solution=filho,
                        nodes_expanded=nos_expandidos,
                        nodes_generated=nos_gerados,
                        max_frontier_size=max_fronteira,
                        depth=filho.cost - initial.cost,
                    )
                alcancados.add(filho.tiles)
                fronteira.append(filho)

            max_fronteira = max(max_fronteira, len(fronteira))

        # Fronteira vazia: todos os estados alcançáveis foram expandidos sem achar o objetivo.
        return SearchResult(None, nos_expandidos, nos_gerados, max_fronteira, 0)
