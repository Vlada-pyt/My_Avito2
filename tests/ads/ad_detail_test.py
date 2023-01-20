import pytest

from ads.serializers import AdsDetailSerializer
from tests.factories import AdsFactory


@pytest.mark.django_db
def test_ad_detail(client, access_token):
    ad = AdsFactory.create()

    response = client.get(f"/ads/{ad.pk}/", HTTP_AUTHORIZATION="Bearer " + access_token)
    assert response.status_code == 200
    assert response.data == AdsDetailSerializer(ad).data

