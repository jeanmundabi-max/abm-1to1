# Serval, seven target companies

**The advertiser:** [Serval](https://www.serval.com/) sells AI agents that close employee IT
requests end to end, inside Slack, instead of routing them to a person. Founded 2024, and by
its own published customer list it replaces ServiceNow and Jira Service Management.

**The run:** layer 2, a demonstration. The campaign Serval would run at the companies it wants
as customers, built as drafts and never activated.

## How the list was built

A company that has the problem Serval fixes is running a ticket queue today. A company on
ServiceNow or Jira Service Management publishes that fact without meaning to: the instance
answers on the open internet, at the company's own name.

**Four possible checks were tested. Two were thrown away**, because they also answered for a
company name that does not exist:

| Check | Real company | A made-up name | Kept |
|---|---|---|---|
| `<company>.service-now.com` resolves | an address | NXDOMAIN | **yes** |
| `<company>.atlassian.net/servicedesk` | 303 to the service desk login | 404 | **yes** |
| `<company>.atlassian.net` resolves | an address | **an address** | no |
| `it.` / `helpdesk.` / `servicedesk.` hostnames | an address | **an address** at 7 of the companies tested | no |

Twenty companies were built on the two that survived, across fifteen sectors. Seven went
forward after every figure was read again on the day.

## The seven

| Account | Why it is here | Reachable |
|---|---|---|
| [Wayfair](accounts/wayfair/) | ServiceNow and Jira Service Management, both live | 610 |
| [Chewy](accounts/chewy/) | Both, live. A workforce that turns over in both directions | 580 |
| [Carvana](accounts/carvana/) | Both, live. Removed the human from car buying, not from a folder request | 640 |
| [Docusign](accounts/docusign/) | Both, live. Filing says 7,044, LinkedIn says 8,900 | 1,200 |
| [Zoom](accounts/zoom/) | ServiceNow, confirmed twice via their own support host | 570 |
| [DoorDash](accounts/doordash/) | Jira only. The ServiceNow lookup came back empty and that is printed on the page | 1,100 |
| [Riot Games](accounts/riot-games/) | Both, live. Files nothing, so the page asserts no headcount | 380 |

**5,080 people in total.** That is the entire audience this campaign would ever speak to.

## The finding worth more than the list

Five companies that passed every other test were dropped for the same reason: between 1,500 and
3,000 US staff, and not one could field 300 reachable people in an IT function. LinkedIn will
not run an ad set below 300.

**On this channel, a one-to-one play for Serval starts at roughly 8,000 US employees.** Below
that the ads cannot be delivered at all, whatever the fit. That is a fact about the channel,
not about those companies.

## What else is here

- [The handover](handover.html) · 4,500 words. How the list was built, the controls, every
  decision and why it went that way, and what is not done. Written for the advertiser.
- [The run log](RUN-LOG.md) · what was rebuilt and why. Includes a layoff-tracker date rejected
  in favour of the primary source, four ad cards rebuilt for failing the standalone test, and
  **every card rebuilt a second time to strip figures that had been invented**.
