from __future__ import annotations


class IdentityRelationships:
    """
    Normalizes aliases, artist name variations, group memberships,
    and member names into a single related_names collection.
    """

    RELATIONSHIP_FIELDS = (
        "aliases",
        "anvs",
        "side_projects",
        "groups",
        "members",
    )

    def resolve(self, result: dict) -> dict:
        normalized = dict(result)

        related_names = []

        for field in self.RELATIONSHIP_FIELDS:
            if field not in normalized:
                continue

            normalized[field] = self._clean_values(normalized.get(field))
            related_names.extend(normalized[field])

        if related_names:
            normalized["related_names"] = self._clean_values(related_names)

        return normalized

    def _clean_values(self, values) -> list[str]:
        cleaned = []

        for value in values or []:
            if value is None:
                continue

            value = str(value).strip()

            if not value:
                continue

            cleaned.append(value)

        return sorted(set(cleaned))