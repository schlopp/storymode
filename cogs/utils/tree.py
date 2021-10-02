import typing
from dataclasses import dataclass


__all__ = ["StoryNode", "StoryStart", "Story"]


@dataclass
class BaseStoryNode:
    """
    Base Story node
    """

    prompt: typing.Optional[str] = None
    result: typing.Optional[str] = None
    title: typing.Optional[str] = None
    situation: typing.Optional[str] = None
    options: typing.Optional[typing.List[StoryNode]] = []

    def __init__(
        self,
        *,
        prompt: typing.Optional[str] = None,
        result: typing.Optional[str] = None,
        title: typing.Optional[str] = None,
        situation: typing.Optional[str] = None,
        options: typing.Optional[typing.List[StoryNode]] = None,
    ):
        self.prompt = prompt
        self.result = result
        self.situation = situation
        self.options = options


@dataclass
class StoryNode(BaseStoryNode):
    """
    Story Node
    """

    prompt: str
    result: str
    options: typing.Optional[typing.List[StoryNode]] = []

    def __init__(
        self,
        prompt: str,
        result: str,
        options: typing.Optional[typing.List[StoryNode]] = [],
    ):
        super().__init__(prompt=prompt, result=result, options=options)


@dataclass
class StoryStart:
    """
    Story Start
    """

    title: str
    situation: str
    options: typing.List[StoryNode]

    def __init__(
        self,
        title: str,
        situation: str,
        options: typing.List[StoryNode],
    ):
        super().__init__(title=title, situation=situation, options=options)


@dataclass
class Story:
    """
    Story
    """

    start: StoryStart
    options: typing.List[StoryNode]

    def __init__(self, start: StoryStart, nodes: typing.List[StoryNode]):
        self.start = start
        self.nodes = nodes
        self.current = self.start

    @classmethod
    def from_json(cls, data: str):
        """
        Create a story from a json string
        """
        import json

        data = json.loads(data)
        start = StoryStart(
            title=data["title"],
            situation=data["situation"],
            options=data["options"],
        )
        options = []
        for option in data["options"]:
            options.append(
                StoryNode(
                    prompt=option["prompt"],
                    result=option["result"],
                    options=option["options"],
                )
            )
        return cls(start=start, options=options)
