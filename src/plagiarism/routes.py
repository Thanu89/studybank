from process import Main_Class


def add_routes_to_resource(_api):
    _api.add_resource(Main_Class, '/get_demo', strict_slashes=False)
