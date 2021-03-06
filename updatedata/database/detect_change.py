# (originally, I wanted to do this with Baked Queries, but it turns out that is not so simple in this case)


# Checks and returns whether the given object has changed in relation to the most recent entry of that object
def detect_change(session, obj):
    image_carryover(session, obj)

    attributes = list_attributes(obj)
    parameters = dict_parameters(obj, attributes)
    query = build_query(session, obj, parameters)

    if query.first():
        return False
    else:
        return True


# Lists all attributes relevant to the change detection
def list_attributes(obj):
    attributes = [i for i in dir(obj) if i[0] != "_"]
    to_remove = ["metadata", "id", "revision", "patch", "abilities", "talents"]
    for attr in to_remove:
        if attr in attributes:
            attributes.remove(attr)
    return attributes


# Returns a dict with all relevant attributes of the given object
def dict_parameters(obj, attrs):
    params = {}
    for attr in attrs:
        params.update({attr: getattr(obj, attr)})
    return params


# Builds the query for finding if the object exists in the session
def build_query(session, obj, params):
    model = type(obj)
    query = session.query(model)
    for attr, param in params.items():
        query = query.filter((getattr(model, attr) == param))
    return query


# Checks if any previous image-data is available, and if it is, attaches it to the object
def image_carryover(session, obj):
    model = type(obj)
    if model.__name__ != "Talent":
        query = session.query(model)
        query = query.filter(model.name == obj.name)
        query = query.order_by(model.patch.desc(), model.revision.desc())

        first = query.first()
        if first and first.image:
            obj.image = first.image
