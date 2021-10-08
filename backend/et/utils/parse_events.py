from loguru import logger

from et.common.models.reprs import EventWithChildren


def parse_events(events):
    remaining = list()
    root_events = list()

    # first find the root event(s)
    for event in events:
        if event.child_of is None:
            if len(root_events):
                logger.warning(f"multiple root-events for event id {event.event_id}")

            root_events.append(EventWithChildren(
                event=event,
                children=list()
            ))
        else:
            remaining.append(event)

    # then populate the tree of sub-spans
    build_sub_trees(root_events, remaining)

    return root_events


def build_sub_trees(parent_events, candidates):
    for parent in parent_events:
        remaining = list()

        for event in candidates:
            if event.child_of == parent.event.span_id:
                parent.children.append(EventWithChildren(
                    event=event,
                    children=list()
                ))
            else:
                remaining.append(event)

        parent.children = sorted(parent.children, key=lambda c: c.event.created_at)
        build_sub_trees(parent.children, remaining)
