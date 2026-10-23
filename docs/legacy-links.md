# Legacy workshop links

The workshop README published five assignment URLs under `/challenges/`. The
static site now uses `/problems/` and keeps those exact paths as client-side
redirect pages. Open one of these old links in a browser to reach its current
assignment page:

| Legacy path | Current assignment |
| --- | --- |
| `/challenges/r1-01-code-validator.html` | `/problems/round-1-01-code-validator.html` |
| `/challenges/r1-02-event-scheduler.html` | `/problems/round-1-02-event-scheduler.html` |
| `/challenges/r1-03-snack-inventory.html` | `/problems/round-1-03-snack-inventory.html` |
| `/challenges/r2-01-event-registration.html` | `/problems/round-2-01-event-registration.html` |
| `/challenges/r2-02-order-processing.html` | `/problems/round-2-02-order-processing.html` |

These redirects preserve the original repository's project-site prefix because
each file lives under `docs/challenges/`. They use an HTML refresh with a visible
link for browsers that do not follow it. GitHub Pages static files cannot send
an HTTP 301 response. Older challenge links not listed here have no published
path in the repository history.
