"""Assign prioritized groups to contiguous blocks of seats."""

import unittest


def allocate_seats(rows, groups):
    """Return assignments and the IDs of groups that could not be seated."""
    assigned = {}
    remaining = []
    for group in groups:
        size = group["size"]
        options = []
        for row_name, seats in rows.items():
            ordered = sorted(seats, key=lambda seat: seat["number"])
            for start in range(len(ordered) - size + 1):
                block = ordered[start:start + size]
                if all(seat["available"] for seat in block) and all(block[i + 1]["number"] == block[i]["number"] + 1 for i in range(len(block) - 1)):
                    if not group.get("requires_accessible", False) or block[0]["accessible"]:
                        options.append((row_name, block))
        if options:
            row_name, block = options[0]
            assigned[group["group_id"]] = [{"row": row_name, "seat": seat["number"]} for seat in block]
            for seat in block:
                seat["available"] = False
        else:
            remaining.append(group["group_id"])
    return {"assigned": assigned, "unassigned": remaining}


def row(*seat_flags):
    return [{"number": index + 1, "accessible": accessible, "available": True} for index, accessible in enumerate(seat_flags)]


class SeatAllocationTests(unittest.TestCase):
    def test_group_gets_contiguous_seats_in_one_row(self):
        result = allocate_seats({"A": row(False, False, False, False)}, [{"group_id": "g", "size": 3}])
        self.assertEqual([item["seat"] for item in result["assigned"]["g"]], [1, 2, 3])

    def test_groups_never_split_across_rows(self):
        result = allocate_seats({"A": row(False, False), "B": row(False, False)}, [{"group_id": "g", "size": 3}])
        self.assertEqual(result["unassigned"], ["g"])

    def test_occupied_seat_breaks_a_contiguous_block(self):
        seats = row(False, False, False)
        seats[1]["available"] = False
        result = allocate_seats({"A": seats}, [{"group_id": "g", "size": 2}])
        self.assertEqual(result["unassigned"], ["g"])

    def test_accessible_group_uses_only_accessible_seats(self):
        result = allocate_seats({"A": row(True, False, True)}, [{"group_id": "g", "size": 2, "requires_accessible": True}])
        self.assertEqual(result["unassigned"], ["g"])

    def test_accessible_requirement_applies_to_every_seat(self):
        result = allocate_seats({"A": row(True, False)}, [{"group_id": "g", "size": 2, "requires_accessible": True}])
        self.assertEqual(result["unassigned"], ["g"])

    def test_higher_priority_groups_are_considered_first(self):
        result = allocate_seats({"A": row(False, False)}, [{"group_id": "small", "size": 1, "priority": 1}, {"group_id": "large", "size": 2, "priority": 5}])
        self.assertIn("large", result["assigned"])
        self.assertEqual(result["unassigned"], ["small"])

    def test_best_fit_row_leaves_more_capacity_elsewhere(self):
        result = allocate_seats({"A": row(False, False, False, False), "B": row(False, False)}, [{"group_id": "g", "size": 2}])
        self.assertEqual(result["assigned"]["g"][0]["row"], "B")

    def test_separate_groups_do_not_receive_the_same_seat(self):
        result = allocate_seats({"A": row(False, False)}, [{"group_id": "one", "size": 1}, {"group_id": "two", "size": 1}])
        seats = [assignment["seat"] for block in result["assigned"].values() for assignment in block]
        self.assertEqual(len(seats), len(set(seats)))


if __name__ == "__main__":
    unittest.main()
