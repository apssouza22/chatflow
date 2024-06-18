import typing as t

from redis.commands.search.query import Query


def create_query(
        return_fields: list,
        search_type: str = "KNN",
        number_of_results: int = 20,
        vector_field_name: str = "data_vector",
        tag: t.Optional[str] = None,
):
    tag_query = "("
    if tag:
        tag_query += f"@application:{{{tag}}}"

    tag_query += ")"
    # if no tags are selected
    if len(tag_query) < 3:
        tag_query = "*"

    base_query = f'{tag_query}=>[{search_type} {number_of_results} @{vector_field_name} $vec_param AS vector_score]'
    query = (Query(base_query).
             sort_by("vector_score").
             paging(0, number_of_results).
             return_fields(*return_fields).
             dialect(2))
    print(query.get_args())
    print(query.query_string())
    return query


def create_text_query(
        return_fields: list,
        text_search: str,
        tag: str,
        number_of_results: int = 20,
):
    tag_query = f"@application:{{{tag}}}"
    text_query= ""
    if text_search != "":
        text_query = f"@text:{text_search}"

    base_query = f'{tag_query} {text_query}'
    query = Query(base_query) \
        .paging(0, number_of_results) \
        .return_fields(*return_fields) \
        .with_scores() \
        .dialect(2)

    # print(query.get_args())
    # print(query.query_string())
    return query


def count(tag: t.Optional[str] = None):
    tag_query = "("
    if tag:
        tag_query += f"@application:{{{tag}}}"
    tag_query += ")"
    # if no tags are selected
    if len(tag_query) < 3:
        tag_query = "*"

    return Query(f'{tag_query}') \
        .no_content() \
        .dialect(2)


def find_docs_by_tag_query(
        return_fields: list,
        number_of_results: int = 20,
        tag: t.Optional[str] = None,
) -> Query:
    tag_query = "("
    if tag:
        tag_query += f"@application:{{{tag}}}"

    tag_query += ")"

    # if no tags are selected
    if len(tag_query) < 3:
        tag_query = "*"

    base_query = f'{tag_query}'
    query = Query(base_query) \
        .paging(0, number_of_results) \
        .return_fields(*return_fields) \
        .dialect(2)
    print(query.get_args())
    print(query.query_string())
    return query
