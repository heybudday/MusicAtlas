from app.services.identity_relationships import IdentityRelationships


def test_duplicate_aliases_removed():
    resolver = IdentityRelationships()

    result = resolver.resolve(
        {
            "aliases": [
                "Purpose Maker",
                "Purpose Maker",
                "The Wizard",
            ],
        }
    )

    assert result["related_names"] == [
        "Purpose Maker",
        "The Wizard",
    ]


def test_groups_included():
    resolver = IdentityRelationships()

    result = resolver.resolve(
        {
            "aliases": [
                "The Wizard",
            ],
            "groups": [
                "Underground Resistance",
            ],
        }
    )

    assert result["related_names"] == [
        "The Wizard",
        "Underground Resistance",
    ]


def test_members_included():
    resolver = IdentityRelationships()

    result = resolver.resolve(
        {
            "members": [
                "Jeff Mills",
                "Mike Banks",
            ],
        }
    )

    assert result["related_names"] == [
        "Jeff Mills",
        "Mike Banks",
    ]


def test_empty_values_ignored():
    resolver = IdentityRelationships()

    result = resolver.resolve(
        {
            "aliases": [
                "Purpose Maker",
                "",
                " ",
                None,
                "The Wizard",
            ],
        }
    )

    assert result["related_names"] == [
        "Purpose Maker",
        "The Wizard",
    ]


def test_original_arrays_preserved():
    resolver = IdentityRelationships()

    result = resolver.resolve(
        {
            "aliases": [
                "Purpose Maker",
                "Purpose Maker",
                "The Wizard",
            ],
            "groups": [
                "Underground Resistance",
            ],
            "members": [
                "Jeff Mills",
            ],
        }
    )

    assert result["aliases"] == [
        "Purpose Maker",
        "The Wizard",
    ]
    assert result["groups"] == [
        "Underground Resistance",
    ]
    assert result["members"] == [
        "Jeff Mills",
    ]