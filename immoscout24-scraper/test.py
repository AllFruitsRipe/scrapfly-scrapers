from cerberus import Validator
import immoscout24
import pytest
import pprint
import json

pp = pprint.PrettyPrinter(indent=4)


def validate_or_fail(item, validator):
    if not validator.validate(item):
        pp.pformat(item)
        pytest.fail(
            f"Validation failed for item: {pp.pformat(item)}\nErrors: {validator.errors}"
        )


property_schema = {
    "schema": {
        "type": "dict",
        "schema": {
            "lister": {
                "type": "dict",
                "schema": {
                    "legalName": {"type": "string"},
                    "website": {
                        "type": "dict",
                        "schema": {
                            "value": {"type": "string"}
                        }
                    },
                    "address": {
                        "type": "dict",
                        "schema": {
                            "locality": {"type": "string"},
                            "country": {"type": "string"},
                            "street": {"type": "string"},
                            "postalCode": {"type": "string"},
                        }
                    }
                }
            },
            "characteristics": {
                "type": "dict",
                "schema": {
                    "numberOfRooms": {"type": "integer"},
                    "yearBuilt": {"type": "integer"},
                    "floor": {"type": "integer"},
                    "livingSpace": {"type": "integer"},
                }
            }
        },
    },
}


search_schema = {
    "schema": {
        "type": "dict",
        "schema": {
            "id": {"type": "integer"},
            "accountId": {"type": "integer"},
            "companyId": {"type": "integer"},
            "memberPackageId": {"type": "integer"},
            "agency": {
                "type": "dict",
                "schema": {
                    "companyCity": {"type": "string"},
                    "companyName1": {"type": "string"},
                    "companyPhoneBusiness": {"type": "string"},
                    "companyStreet": {"type": "string"},
                    "companyZip": {"type": "string"},
                    "firstName": {"type": "string"},
                    "gender": {"type": "string"},
                    "gendshowLogoOnSerper": {"type": "boolean"},
                    "lastName": {"type": "string"},
                    "logoUrl": {"type": "string"},
                    "logoUrlDetailPage": {"type": "string"},
                    "nameFormatted": {"type": "string"},
                },
            },
            "availableFrom": {"type": "string"},
            "availableFromFormatted": {"type": "string"},
            "cityId": {"type": "integer"},
            "cityName": {"type": "string"},
            "commuteTimes": {
                "type": "dict",
                "schema": {
                    "defaultPois": {
                        "type": "list",
                        "schema": {
                            "type": "dict",
                            "schema": {
                                "defaultPoiId": {"type": "integer"},
                                "label": {"type": "string"},
                                "transportations": {
                                    "type": "list",
                                    "schema": {
                                        "type": "dict",
                                        "schema": {
                                            "transportationTypeId": {"type": "integer"},
                                            "travelTime": {"type": "integer"},
                                            "isReachable": {"type": "boolean"},
                                        },
                                    },
                                },
                            },
                        },
                    }
                },
            },
            "countryId": {"type": "integer"},
            "extraPrice": {"type": "integer"},
            "geoAccuracy": {"type": "integer"},
            "grossPrice": {"type": "integer"},
            "hasNewBuildingProject": {"type": "boolean"},
            "hasVirtualTour": {"type": "boolean"},
            "isHighlighted": {"type": "boolean"},
            "isNeubauLite": {"type": "boolean"},
            "isNeubauLitePremium": {"type": "boolean"},
            "isHgCrosslisting": {"type": "boolean"},
            "latitude": {"type": "integer"},
            "longitude": {"type": "integer"},
            "netPrice": {"type": "integer"},
            "numberOfRooms": {"type": "integer"},
            "price": {"type": "integer"},
            "propertyUrl": {"type": "string"},
            "propertyCategoryId": {"type": "integer"},
            "propertyTypeId": {"type": "integer"},
            "state": {"type": "string"},
            "street": {"type": "string"},
            "surfaceLiving": {"type": "integer"},
            "images": {
                "type": "list",
                "schema": {
                    "type": "dict",
                    "schema": {
                        "url": {"type": "string"},
                        "originalWidth": {"type": "integer"},
                        "originalHeight": {"type": "integer"},
                        "id": {"type": "integer"},
                    },
                },
            },
            "lastPublished": {"type": "string"},
            "sortalgoScore": {"type": "integer"},
            "sortalgoScore2": {"type": "integer"},
        },
    }
}


@pytest.mark.asyncio
async def test_properties_scraping():
    properties_data = await immoscout24.scrape_properties(
        urls=[
            "https://www.immoscout24.ch/rent/4000630232",
            "https://www.immoscout24.ch/rent/4000519178",
            "https://www.immoscout24.ch/rent/4000519178",
        ]
    )
    validator = Validator(property_schema, allow_unknown=True)
    for item in properties_data:
        validate_or_fail(item, validator)
    assert len(properties_data) >= 1


@pytest.mark.asyncio
async def test_search_scraping():
    search_data = await immoscout24.scrape_search(
        url="https://www.immoscout24.ch/en/real-estate/rent/city-bern",
        scrape_all_pages=False,
        max_scrape_pages=2,
    )
    validator = Validator(search_schema, allow_unknown=True)
    for item in search_data:
        validate_or_fail(item, validator)
    assert len(search_data) >= 2
