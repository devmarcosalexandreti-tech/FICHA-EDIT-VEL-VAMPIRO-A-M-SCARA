import unittest

from src.vampiro_sheet import data


def safe_name(value):
    return "".join(character for character in value if character.isalnum())


class SystemDataContractTests(unittest.TestCase):
    def test_supported_character_types_remain_available(self):
        self.assertEqual(
            ["Vampiro jogador", "Mortal", "Carnical", "Antagonista"],
            data.CHARACTER_TYPES,
        )

    def test_core_trait_groups_have_expected_shape(self):
        self.assertEqual(
            {"Fisicos": 3, "Sociais": 3, "Mentais": 3},
            {group: len(traits) for group, traits in data.ATTRIBUTES.items()},
        )
        self.assertEqual(
            {"Talentos": 10, "Pericias": 10, "Conhecimentos": 10},
            {group: len(traits) for group, traits in data.ABILITIES.items()},
        )

    def test_generated_trait_names_are_unique(self):
        attribute_names = [
            "atributo_" + safe_name(group) + "_" + safe_name(trait)
            for group, traits in data.ATTRIBUTES.items()
            for trait in traits
        ]
        ability_names = [
            "habilidade_" + safe_name(trait)
            for traits in data.ABILITIES.values()
            for trait in traits
        ]
        self.assertEqual(len(attribute_names), len(set(attribute_names)))
        self.assertEqual(len(ability_names), len(set(ability_names)))

    def test_clan_disciplines_reference_known_disciplines(self):
        for clan, discipline_list in data.CLAN_DISCIPLINES.items():
            if clan == "Caitiff":
                continue
            with self.subTest(clan=clan):
                disciplines = [item.strip() for item in discipline_list.split(",")]
                self.assertEqual(3, len(disciplines))
                self.assertTrue(all(discipline in data.DISCIPLINES for discipline in disciplines))

    def test_generation_options_and_table_stay_consistent(self):
        self.assertEqual(list(data.GENERATION_TABLE), data.GENERATION_OPTIONS)
        self.assertEqual(("5", "10", "1"), data.GENERATION_TABLE["13+"])
        self.assertEqual(("5", "10/8 util", "1"), data.GENERATION_TABLE["14"])

    def test_all_standard_clans_have_discipline_data(self):
        selectable_clans = {
            clan for clan in data.CLANS if clan not in {"Mortal/Carnical", "Outro antagonista"}
        }
        self.assertEqual(selectable_clans, set(data.CLAN_DISCIPLINES))


if __name__ == "__main__":
    unittest.main()
