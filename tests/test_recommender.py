import pytest
from pathlib import Path
from ai.config import Settings
from ai.rag import PoojaRecommender
from ai.models import QueryContext


@pytest.fixture
def recommender():
    settings = Settings()
    rec = PoojaRecommender(settings, llm=None)
    rec.load_data()
    return rec


def test_health_query(recommender):
    ctx = QueryContext(user_issue="health and peace")
    recs = recommender.recommend(ctx)
    assert len(recs) > 0, "Should return at least one recommendation"
    top_pooja = recs[0].pooja
    # Expected health-related poojas
    expected_intents = {"health", "healing", "wellness"}
    pooja_intents = set(top_pooja.intents)
    assert expected_intents & pooja_intents, f"Expected health-related intents, got {pooja_intents}"


def test_wealth_query(recommender):
    ctx = QueryContext(user_issue="wealth for business")
    recs = recommender.recommend(ctx)
    assert len(recs) > 0, "Should return at least one recommendation"
    top_pooja = recs[0].pooja
    expected_intents = {"wealth", "business", "prosperity", "trade", "commerce"}
    pooja_intents = set(top_pooja.intents)
    assert expected_intents & pooja_intents, f"Expected wealth/business intents, got {pooja_intents}"


def test_marriage_query(recommender):
    ctx = QueryContext(user_issue="marriage harmony")
    recs = recommender.recommend(ctx)
    assert len(recs) > 0, "Should return at least one recommendation"
    top_pooja = recs[0].pooja
    expected_intents = {"marriage", "relationships", "family"}
    pooja_intents = set(top_pooja.intents)
    assert expected_intents & pooja_intents, f"Expected marriage-related intents, got {pooja_intents}"


def test_city_filtering(recommender):
    ctx = QueryContext(user_issue="health and peace", city="Delhi")
    recs = recommender.recommend(ctx)
    if len(recs) > 0:
        top_pooja = recs[0].pooja
        assert "Delhi" in top_pooja.cities, f"Expected Delhi in cities for {top_pooja.name}"


def test_score_sorting(recommender):
    ctx = QueryContext(user_issue="health")
    recs = recommender.recommend(ctx)
    if len(recs) > 1:
        # Verify scores are in descending order
        for i in range(len(recs) - 1):
            assert recs[i].score >= recs[i+1].score, "Scores should be descending"


def test_catalog_loaded(recommender):
    assert len(recommender._poojas) >= 25, "Catalog should have at least 25 poojas"


def test_json_export(recommender):
    ctx = QueryContext(user_issue="health")
    recs = recommender.recommend(ctx)
    json_data = recommender.to_jsonable(recs)
    assert isinstance(json_data, list), "JSON export should be a list"
    for item in json_data:
        assert "pooja" in item, "Each item should have 'pooja'"
        assert "score" in item, "Each item should have 'score'"
        assert "reason" in item, "Each item should have 'reason'"
        assert "language" in item, "Each item should have 'language'"
