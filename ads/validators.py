import datetime
from dateutil.relativedelta import relativedelta as date_diff
from datetime import date
from rest_framework import serializers
from django.core.exceptions import ValidationError

def not_null(value):
    if value:
        raise serializers.ValidationError("Значение не может быть True")


def check_birth_date(value: date):
    age = date_diff(datetime.date.today(), value).years
    if age < 9:
        raise serializers.ValidationError(f"Возраст {age} меньше 9!")


def check_email(value: str):
    if "rambler.ru" in value:
        raise ValidationError("Can't create with this domain")

