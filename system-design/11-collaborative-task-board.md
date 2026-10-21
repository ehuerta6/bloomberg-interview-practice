# Problem 11 — Collaborative Task Board

**Difficulty:** Medium

## Scenario

A student project team wants a shared board for coordinating work across a semester project. Team members need to see the same tasks, know who owns each task, and understand how a task reached its current state. Today, changes are discussed in chat and people sometimes overwrite one another's updates.

Design a small web application for multiple teams. A board belongs to one team, but a user may belong to several teams. The first version serves a single school and does not need public boards or cross-team task sharing.

## Functional Requirements

- An authenticated user can create a board and becomes its owner.
- The owner can add existing users to the board as editors or viewers and can remove members.
- Editors can create tasks, assign a task to a board member, set a title, description, due date, and status, and add comments.
- Viewers can read board tasks, comments, and activity history but cannot change them.
- A task has one of `todo`, `in_progress`, or `done` status. Editors may move it between any of these states.
- The board displays current task state and a chronological activity history for task creation, assignment changes, status changes, and comments.
- A user can request the board's current tasks and a task's comments/history. The initial version can use ordinary HTTP refresh; live push updates are not required.
- Removing a member prevents future access and edits through that board. Tasks assigned to the removed member remain visible and are marked unassigned until an editor assigns them again.

## Constraints & Assumptions

- Assume users have already authenticated; describe how identity reaches the application but do not design account registration.
- A user has exactly one role per board: owner, editor, or viewer. There is one owner, and ownership transfer is out of scope.
- A task's current fields and its activity record must be committed together. Activity is append-only for this version.
- The board is small enough for a relational database and paginated task lists. Do not assume a specific user count or require a separate search service.
- Clarify whether simultaneous edits should be last-write-wins or whether a stale edit should be rejected. State your choice and how clients learn about a conflict.

## Your Task

Design the system for the stated scope. Show the main components, the tables and relationships, and the authorization checks for reading and editing a board. Walk through an editor changing a task's status, including how the current task and activity history stay consistent. Explain how membership removal affects an in-flight request and how concurrent edits are handled.

## Interviewer Follow-Ups

- The team wants to see changes without refreshing. What would you add, and how would you recover a client that disconnects?
- A task can now have labels and multiple assignees. What changes in the data model and validation?
- A stale browser tab submits an edit after another editor has changed the task. How do you prevent silent data loss?

## Reference Solution

[View the reference solution](../solutions/system-design/11-collaborative-task-board.md)
