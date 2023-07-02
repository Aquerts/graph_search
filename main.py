from search import Search

search = Search(library='large')
search.set_targets(source_name="Robert Downey Jr.", target_name="Tom Cruise")

search.find_path(algorithm='DepthFirstSearch')  # or algorithm='BreadthFirstSearch'
search.show_path()
