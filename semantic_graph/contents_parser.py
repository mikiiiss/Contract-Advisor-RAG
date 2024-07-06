import re
import networkx as nx

def parse_table_of_contents(table_of_contents):
    """
    Parse the table of contents into sections.

    Args:
        table_of_contents (str): The table of contents as a multiline string.

    Returns:
        list: A list of tuples containing the title, description, and page number for each section.
    """
    sections = re.findall(r'(ARTICLE [IVXLCDM]+|Section \d+\.\d+)\s+(.*?)\s+(\d+)', table_of_contents)
    return sections

def create_graph(sections):
    """
    Create a NetworkX graph from the parsed table of contents.

    Args:
        sections (list): A list of tuples containing the title, description, and page number for each section.

    Returns:
        networkx.DiGraph: A directed graph representing the table of contents.
    """
    G = nx.DiGraph()

    # Add nodes to the graph
    for title, desc, page in sections:
        node_id = f"{title}: {desc}"
        G.add_node(node_id, page=page, title=title, description=desc)

    # Define edges between sections (example: sequential order)
    for i in range(len(sections) - 1):
        from_node = f"{sections[i][0]}: {sections[i][1]}"
        to_node = f"{sections[i + 1][0]}: {sections[i + 1][1]}"
        G.add_edge(from_node, to_node)

    return G

if __name__ == "__main__":
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

    # Print all nodes to verify identifiers
    print("Nodes in the graph:")
    for node in graph.nodes:
        print(node)