# Problem 06 — Student Marketplace

**Difficulty:** Easy

## Scenario

A campus wants a simple marketplace where students can sell used textbooks, calculators, and small electronics to other students. Sellers create listings; buyers browse by category and search terms, open a listing, and contact its seller. A seller can mark an item sold or remove a listing. The first version serves one campus and does not process payments or arrange shipping.

## Functional Requirements

- A signed-in student can create a listing with a title, description, category, condition, asking price, and optional photo references.
- A listing belongs to exactly one seller. The seller can edit or remove their own active listing.
- Students can browse active listings by category and search title/description. Results show enough information to identify a listing and its current status.
- A buyer can start a conversation with the seller about an active listing. Conversation messages are visible only to its participants.
- A seller can mark an active listing sold. Sold or removed listings no longer appear in active search results and cannot start new conversations.
- Existing conversations remain readable after a listing is sold or removed.

## Constraints & Assumptions

- The first release covers one campus and authenticated student accounts. Assume identity verification has already happened elsewhere.
- A listing describes one item; quantity and checkout are out of scope.
- No payments, shipping, recommendations, public reviews, or real-time chat are required. Polling or refreshing a conversation is acceptable.
- Clarify whether a seller may reopen a sold listing and whether removed listings are recoverable. For the initial design, treat sold and removed as terminal states and retain records for conversation history.
- Search may be basic database text matching. Do not assume a traffic target or dedicated search service.

## Your Task

Design the smallest system that supports these workflows. Explain the data model and ownership rules, how active listings are found, how a conversation is associated with a listing, and how the system prevents one student from editing another student's listing or reading a conversation they do not participate in. Walk through creating a listing and contacting its seller.

## Interviewer Follow-Ups

- Two buyers open a listing just as the seller marks it sold. Which operations should still succeed?
- Students want to report suspicious listings. What minimal data and workflow would you add?
- The marketplace expands to several campuses. Which records and search rules need a campus identifier?

## Reference Solution

[View the reference solution](../solutions/system-design/06-student-marketplace.md)
