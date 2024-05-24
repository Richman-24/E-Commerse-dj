﻿from django.contrib.postgres.search import (
    SearchQuery,
    SearchRank,
    SearchVector,
    SearchHeadline,
)
from .models import Products

def q_search(query):

    vector = SearchVector("name", "description")
    query = SearchQuery(query)

    result = (
        Products.objects.annotate(
            rank = SearchRank(vector, query))
            .filter(rank__gt=0)
            .order_by("-rank")
        )

    result = result.annotate(
        headline = SearchHeadline(
            "name",
            query,
            start_sel='<span style="background-collor: yellow;">',
            stop_sel='</span>')
    )

    result = result.annotate(
        bodyline = SearchHeadline(
            "description",
            query,
            start_sel='<span style="background-collor: yellow;">',
            stop_sel='</span>')
    )

    return result