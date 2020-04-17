import os
import json
import requests
import networkx as nx
from urllib import parse
from itertools import chain
from multiprocessing import Pool


def link_to_title(link):
    return link["title"]


def clean_if_key(page, key):
    if key in page.keys():
        return map(link_to_title, page[key])
    else:
        return []


def get_wiki_linked_pages(page_title, page_number_limit=500):
    """
    Retrieve the inbound and outbound page links for
    a wikipedia page
    """
    # Properly quote the title to turn into a url
    safe_title = parse.quote(page_title)
    url = (
        f"https://en.wikipedia.org/w/api.php?action=query&prop=links|linkshere&pllimit={page_number_limit}&lhlimit={page_number_limit}&titles={safe_title}&format=json&formatversion=2"
    )
    content = requests.get(url).content
    json_content = json.loads(content)

    json_page = json_content["query"]["pages"][0]

    # inbound links are identified by "links" key
    inbound_pages = clean_if_key(json_page, "links")
    # outbound links are identified by linkshere key
    outbound_pages = clean_if_key(json_page, "linkshere")

    return dict(
        title=page_title,
        inbound_pages=list(inbound_pages),
        outbound_pages=list(outbound_pages),
    )


def flatten_network(wiki_linked_pages):
    """
    Return a list of the combine inbound and outbound links
    """
    return wiki_linked_pages["inbound_pages"] + wiki_linked_pages["outbound_pages"]


def pages_to_edges(wiki_linked_pages):
    """
    Create edges linking to (inbound) and from (outbound) a page
    """
    page = wiki_linked_pages["title"]
    in_edges = [(in_page, page) for in_page in wiki_linked_pages["inbound_pages"]]
    out_edges = [(page, out_page) for out_page in wiki_linked_pages["outbound_pages"]]
    return in_edges + out_edges


if __name__ == "__main__":
    title = "Freeman_Dyson"
    page_number_limit = 50
    # Retrieve the pages associated with the central page
    # These are first degree pages
    root_linked_pages = get_wiki_linked_pages(
        title, page_number_limit=page_number_limit
    )

    initial_network = flatten_network(root_linked_pages)

    # Retrieve the pages associated with the pages on the central page
    # These are second degree pages
    with Pool(processes=os.cpu_count()) as pool:
        all_linked_pages = pool.map(get_wiki_linked_pages, initial_network)

        # Get  a list of lists of the edges from all the pages
        edges = pool.map(pages_to_edges, all_linked_pages)

    # Flatten the list of lists to a single list (a map here)
    edges = chain.from_iterable(edges)

    # Directed graph creation
    graph = nx.DiGraph()
    for edge in edges:
        graph.add_edge(*edge)

    # Write in gexf format for Gephi
    nx.readwrite.gexf.write_gexf(
        graph, f"./{title}-{page_number_limit}_links_wiki_graph.gexf"
    )
