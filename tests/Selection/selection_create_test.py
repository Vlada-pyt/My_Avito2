import pytest

from tests.factories import AdsFactory


@pytest.mark.django_db
def test_create_selection(client, access_token):
    ads_list = AdsFactory.create_batch(3)
    data = {
        "name": "Новая подборка",
        "user": "test_user",
        "items": [ad.pk for ad in ads_list]

    }

    expected_data = {
        "id": 1,
        "name": "Новая подборка",
        "user": "test_user",
        "items": [ad.pk for ad in ads_list]
    }


    response = client.post("/selection/", data, HTTP_AUTHORIZATION="Bearer " + access_token)
    assert response.status_code == 201
    assert response.data == expected_data