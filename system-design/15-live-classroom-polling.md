# Problem 15 — Live Classroom Polling

**Difficulty:** Hard

## Scenario

An instructor wants to ask a multiple-choice question during class and see responses arrive while students vote. Students should see the current results without being able to submit multiple votes accidentally. Instructors need to close a poll and retain its results after class.

Design the polling feature for a course platform with authenticated instructors and enrolled students. The initial version supports one active poll per course at a time.

## Functional Requirements

- An instructor can create a poll with a question and at least two distinct answer options for a course they teach.
- The instructor can open and close the poll. Only an open poll accepts votes. Closed polls retain their results and reject further changes.
- An enrolled student can submit one answer per poll. While the poll is open, the student may change their answer; changing it replaces the prior vote and does not increase the total vote count.
- A student who is not enrolled and an instructor who does not teach the course cannot access its polls or results.
- Results show a count per option and a total number of distinct student voters. Poll results should update for connected clients during class; clients must recover by fetching a current snapshot after reconnecting.
- The system records poll creation/open/close times and the instructor responsible. Deleting a poll with votes is not allowed; an instructor may close it instead.

## Constraints & Assumptions

- Assume course membership and identity already exist. A student may have one current vote per poll.
- Keep vote counts consistent with vote records. Do not rely on a browser's displayed count as the source of truth.
- Use a relational database for polls, options, and votes. Choose either brief polling or a server-push connection for result updates and explain the trade-off; the initial school deployment does not supply a traffic target.
- Define what happens if a student's vote races with poll closure. The system must have a clear ordering rule, with a vote accepted only if it commits while the poll is open.
- Do not expose individual student answers in the classroom results view; instructors may inspect aggregate counts only in the initial version.

## Your Task

Design the instructor and student interactions, data model, authorization checks, and live result update path. Walk through a vote submission, including how duplicate clicks and vote changes are handled. Explain how the system prevents two active polls for the same course and what a reconnecting client does after missing updates.

## Example to Work Through

An enrolled student selects option A, changes the answer to option B while the poll is open, and then reconnects after missing a result update. Describe the student's current vote, the aggregate counts, and how the client gets back in sync.

## Interviewer Follow-Ups

- An instructor wants anonymous voting while still limiting each enrolled student to one vote. What changes in the design and retention policy?
- The class has intermittent Wi-Fi and students retry submissions. How do you make retries safe and communicate the accepted vote?
- A poll option must be edited after voting starts. Should edits be allowed, and what data integrity issues follow?

## Reference Solution

[View the reference solution](../solutions/system-design/15-live-classroom-polling.md)
