#!/usr/bin/env python3
# Copyright (C) 2022 tribe29 GmbH - License: GNU General Public License v2
# This file is part of Checkmk (https://checkmk.com). It is subject to the terms and
# conditions defined in the file COPYING, which is part of this source code package.

from collections.abc import Iterable, Iterator, Sequence

import feedparser  # type: ignore[import]
import requests
from feedparser.util import FeedParserDict  # type: ignore[import]
from pydantic import BaseModel

from cmk.utils.azure_constants import AZURE_REGIONS

from cmk.special_agents.utils.agent_common import SectionWriter, special_agent_main
from cmk.special_agents.utils.argument_parsing import Args, create_default_argument_parser


class AzureIssue(BaseModel, frozen=True):
    region: str
    title: str
    description: str


class AzureStatus(BaseModel, frozen=True):
    link: str
    regions: Sequence[str]
    issues: Sequence[AzureIssue]


def parse_arguments(argv: Sequence[str] | None) -> Args:
    parser = create_default_argument_parser(description=__doc__)
    parser.add_argument(
        "regions",
        type=str,
        nargs="*",
        metavar="REGION1 REGION2",
        help="Monitored Azure regions",
    )

    return parser.parse_args(argv)


def get_affected_regions(all_regions: Iterable[str], entry: FeedParserDict) -> set[str]:
    """Fetch regions affected by the issue

    Some regions are substrings of other regions e.g. (Central US of North Central US).
    This function makes sure that we don't return both regions when only the one with
    the longer name is present.
    all_regions list has to be sorted by length to produce a correct result.
    """
    affected_regions = set()
    title, summary = entry.title, entry.summary

    for region in all_regions:
        if region in title:
            affected_regions.add(region)
            title = title.replace(region, "")

        if region in summary:
            affected_regions.add(region)
            summary = summary.replace(region, "")

    return affected_regions


def get_azure_issues(
    entries: Iterable[FeedParserDict], selected_regions: list[str]
) -> Iterator[AzureIssue]:
    all_regions = sorted(list(AZURE_REGIONS.values()), key=len, reverse=True)

    for entry in entries:
        affected_regions = get_affected_regions(all_regions, entry)

        if not affected_regions:
            yield AzureIssue(region="Global", title=entry.title, description=entry.summary)

        for region in affected_regions:
            if region in selected_regions:
                yield AzureIssue(region=region, title=entry.title, description=entry.summary)


def write_section(args: Args) -> None:
    response = requests.get("https://status.azure.com/en-us/status/feed/")
    feed = feedparser.parse(response.text)

    selected_regions = [AZURE_REGIONS[r] for r in args.regions]
    selected_regions.append("Global")
    azure_issues = list(get_azure_issues(feed.entries, selected_regions))

    azure_status = AzureStatus(link=feed.feed.link, regions=selected_regions, issues=azure_issues)

    with SectionWriter("azure_status") as writer:
        writer.append_json(azure_status.dict())


def main() -> None:
    special_agent_main(parse_arguments, write_section)
