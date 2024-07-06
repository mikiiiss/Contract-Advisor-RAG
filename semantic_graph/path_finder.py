import networkx as nx

def find_paths(graph, start_node, end_node, max_depth=3):
    """
    Find all simple paths between two nodes in the graph.

    Args:
        graph (networkx.DiGraph): The graph to search for paths.
        start_node (str): The starting node.
        end_node (str): The ending node.
        max_depth (int): The maximum depth of the search (optional, default is 3).

    Returns:
        list: A list of lists, where each inner list represents a path between the start and end nodes.
    """
    return list(nx.all_simple_paths(graph, source=start_node, target=end_node, cutoff=max_depth))

if __name__ == "__main__":
    from table_of_contents_parser import parse_table_of_contents, create_graph

    # Define the table of contents as a multiline string
    table_of_contents = """
    ARTICLE I DEFINITIONS; CERTAIN RULES OF CONSTRUCTION    2
    Section 1.01    Definitions    13
    Section 1.02    Certain Matters of Construction    14
    ARTICLE II PURCHASE AND SALE OF SHARES AND WARRANTS; TREATMENT OF OPTIONS; CLOSING.    14
    Section 2.01    Purchase and Sale of Shares    14
    """

    sections = parse_table_of_contents(table_of_contents)
    graph = create_graph(sections)

    # Example query to find paths between two sections
    start_node = "Section 1.01: Definitions"
    end_node = "Section 2.01: Purchase and Sale of Shares"

    paths = find_paths(graph,