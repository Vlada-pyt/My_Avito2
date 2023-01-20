import pytest

from ads.serializers import AdsListSerializer
from tests.factories import AdsFactory


@pytest.mark.django_db
def test_ads_list(client, access_token):
    ads_list = AdsFactory.create_batch(4)

    response = client.get("/ads/", HTTP_AUTHORIZATION="Bearer " + access_token)
    assert response.status_code == 200
    assert response.data == {"count": 4, "next": None,
                             "previous": None, "results": AdsListSerializer(ads_list, many=True).data}





