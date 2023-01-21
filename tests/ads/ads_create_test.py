import pytest


@pytest.mark.django_db
def test_create_ads(client, access_token, users, categories):
    data = {
        "author": users.pk,
        "category": categories.pk,
        "name": "test test test",
        "price": 28400,
        "description": "m"
    }

    expected_data = {
        "id": 5,
        "is_published": False,
        "name": "test test test",
        "price": 28400,
        "description": "m",
        "image": None,
        "author": users.pk,
        "category": categories.pk
    }


    response = client.post("/ads/", data, HTTP_AUTHORIZATION="Bearer " + access_token)
    assert response.status_code == 201
    assert response.data == expected_data
