#!/usr/bin/env python

from pydantic import BaseModel

from crewai.flow import Flow, start

from crewai.utilities.events import (
    FlowStartedEvent,
    
)
from crewai.utilities.events.base_events import BaseEvent
from crewai.utilities.events.base_event_listener import BaseEventListener


class MyCustomEvent(BaseEvent):
    pass

class MyCustomListener(BaseEventListener):
    def __init__(self):
        super().__init__()

    def setup_listeners(self, crewai_event_bus):
        @crewai_event_bus.on(FlowStartedEvent)
        def _(source, event):
            print(f"Flow '{event.flow_name}' has started execution!")
            custom_event = MyCustomEvent(type="my_custom_event")
            crewai_event_bus.emit(source, custom_event)
        
        @crewai_event_bus.on(MyCustomEvent)
        def _(source, event):
            print(f"MyCustomEvent has been emitted!")


my_listener = MyCustomListener()

class EnterpriseFlowReproState(BaseModel):
    a_flow_method_result: str = ""


class EnterpriseFlowRepro(Flow[EnterpriseFlowReproState]):

    @start()
    def a_flow_method(self):
        print("RUNNING a_flow_method")
        self.state.a_flow_method_result = "DONE"


def kickoff():
    poem_flow = EnterpriseFlowRepro()
    poem_flow.kickoff()


def plot():
    poem_flow = EnterpriseFlowRepro()
    poem_flow.plot()


if __name__ == "__main__":
    kickoff()
