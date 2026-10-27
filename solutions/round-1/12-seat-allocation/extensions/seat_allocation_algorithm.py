"""Assign prioritized groups to contiguous blocks of seats."""

import math
import unittest


def allocate_seats(rows, groups):
    """Allocate whole groups using a deterministic best-fit policy.

    Rows map names to seat dictionaries with number, accessible, and available
    fields. Higher-priority groups are processed first. Candidate blocks must
    be consecutive, free, and wholly accessible when requested. Ties use row
    insertion order followed by the first seat number.
    """
    if not isinstance(rows, dict) or not isinstance(groups, (list, tuple)):
        raise ValueError("rows and groups have invalid shapes")
    normalized_rows = []
    for row_name, seats in rows.items():
        if not isinstance(seats, (list, tuple)):
            raise ValueError("each row must contain a seat list")
        numbers = set()
        copied = []
        for seat in seats:
            if not isinstance(seat, dict):
                raise ValueError("seat entries must be dictionaries")
            number = seat.get("number")
            accessible = seat.get("accessible")
            available = seat.get("available")
            if isinstance(number, bool) or not isinstance(number, int) or number <= 0 or number in numbers:
                raise ValueError("seat numbers must be unique positive integers per row")
            if not isinstance(accessible, bool) or not isinstance(available, bool):
                raise ValueError("seat accessibility and availability must be booleans")
            numbers.add(number)
            copied.append({"number": number, "accessible": accessible, "available": available})
        normalized_rows.append((row_name, sorted(copied, key=lambda seat: seat["number"])))

    checked_groups = []
    group_ids = set()
    for index, group in enumerate(groups):
        if not isinstance(group, dict):
            raise ValueError("group entries must be dictionaries")
        group_id = group.get("group_id")
        size = group.get("size")
        priority = group.get("priority", 0)
        accessible = group.get("requires_accessible", False)
        if not isinstance(group_id, str) or not group_id.strip() or group_id in group_ids:
            raise ValueError("group IDs must be nonblank strings and unique")
        if isinstance(size, bool) or not isinstance(size, int) or size <= 0:
            raise ValueError("group size must be a positive integer")
        if isinstance(priority, bool) or not isinstance(priority, (int, float)):
            raise ValueError("priority must be a finite number")
        try:
            finite_priority = math.isfinite(priority)
        except OverflowError:
            finite_priority = False
        if not finite_priority:
            raise ValueError("priority must be a finite number")
        if not isinstance(accessible, bool):
            raise ValueError("accessible requirement must be boolean")
        group_ids.add(group_id)
        checked_groups.append((index, group_id, size, priority, accessible))

    assigned = {}
    unassigned = []
    availability = {name: [seat["available"] for seat in seats] for name, seats in normalized_rows}
    order = sorted(checked_groups, key=lambda item: (-item[3], item[0]))
    for _, group_id, size, _, requires_accessible in order:
        options = []
        for row_index, (row_name, seats) in enumerate(normalized_rows):
            free_count = sum(availability[row_name])
            for start in range(len(seats) - size + 1):
                block = seats[start:start + size]
                if len(block) != size or any(not availability[row_name][start + offset] for offset in range(size)):
                    continue
                if any(block[offset + 1]["number"] != block[offset]["number"] + 1 for offset in range(size - 1)):
                    continue
                if requires_accessible and not all(seat["accessible"] for seat in block):
                    continue
                options.append((free_count - size, row_index, block[0]["number"], row_name, start, block))
        if not options:
            unassigned.append(group_id)
            continue
        _, _, _, row_name, start, block = min(options, key=lambda item: item[:3])
        assigned[group_id] = [{"row": row_name, "seat": seat["number"]} for seat in block]
        for offset in range(size):
            availability[row_name][start + offset] = False
    return {"assigned": assigned, "unassigned": unassigned}


def row(*seat_flags):
    return [{"number": index + 1, "accessible": accessible, "available": True} for index, accessible in enumerate(seat_flags)]


class SeatAllocationTests(unittest.TestCase):
    def test_group_gets_contiguous_seats_in_one_row(self):
        result = allocate_seats({"A": row(False, False, False, False)}, [{"group_id": "g", "size": 3}])
        self.assertEqual([item["seat"] for item in result["assigned"]["g"]], [1, 2, 3])

    def test_groups_never_split_across_rows(self):
        self.assertEqual(allocate_seats({"A": row(False, False), "B": row(False, False)}, [{"group_id": "g", "size": 3}])["unassigned"], ["g"])

    def test_occupied_seat_breaks_a_contiguous_block(self):
        seats = row(False, False, False)
        seats[1]["available"] = False
        self.assertEqual(allocate_seats({"A": seats}, [{"group_id": "g", "size": 2}])["unassigned"], ["g"])

    def test_accessible_requirement_applies_to_every_seat(self):
        self.assertEqual(allocate_seats({"A": row(True, False, True)}, [{"group_id": "g", "size": 2, "requires_accessible": True}])["unassigned"], ["g"])

    def test_all_accessible_block_is_assignable(self):
        result = allocate_seats({"A": row(True, True)}, [{"group_id": "g", "size": 2, "requires_accessible": True}])
        self.assertEqual([seat["seat"] for seat in result["assigned"]["g"]], [1, 2])

    def test_higher_priority_groups_are_considered_first(self):
        result = allocate_seats({"A": row(False, False)}, [{"group_id": "small", "size": 1, "priority": 1}, {"group_id": "large", "size": 2, "priority": 5}])
        self.assertEqual(list(result["assigned"]), ["large"])
        self.assertEqual(result["unassigned"], ["small"])

    def test_best_fit_row_leaves_more_capacity_elsewhere(self):
        result = allocate_seats({"A": row(False, False, False, False), "B": row(False, False)}, [{"group_id": "g", "size": 2}])
        self.assertEqual(result["assigned"]["g"][0]["row"], "B")

    def test_ties_use_row_insertion_order_and_lowest_seat(self):
        result = allocate_seats({"Z": row(False, False), "A": row(False, False)}, [{"group_id": "g", "size": 1}])
        self.assertEqual(result["assigned"]["g"], [{"row": "Z", "seat": 1}])

    def test_input_seat_maps_are_not_mutated(self):
        seats = row(False, False)
        allocate_seats({"A": seats}, [{"group_id": "g", "size": 1}])
        self.assertTrue(all(seat["available"] for seat in seats))

    def test_invalid_sizes_and_duplicate_group_ids_are_rejected(self):
        for groups in ([{"group_id": "g", "size": True}], [{"group_id": "g", "size": 1}, {"group_id": "g", "size": 1}]):
            with self.subTest(groups=groups), self.assertRaises(ValueError):
                allocate_seats({"A": row(False)}, groups)

    def test_group_ids_must_be_nonblank_strings(self):
        for group_id in (None, "", "   ", 7, []):
            with self.subTest(group_id=group_id), self.assertRaises(ValueError):
                allocate_seats({"A": row(False)}, [{"group_id": group_id, "size": 1}])

    def test_priority_must_be_finite(self):
        for priority in (float("nan"), float("inf"), float("-inf")):
            with self.subTest(priority=priority), self.assertRaises(ValueError):
                allocate_seats({"A": row(False)}, [{"group_id": "g", "size": 1, "priority": priority}])


if __name__ == "__main__":
    unittest.main()
