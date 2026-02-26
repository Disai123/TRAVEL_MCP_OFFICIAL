from typing import TypedDict, List, Optional, Dict, Any, Annotated
import operator

class TripState(TypedDict):
    messages: Annotated[List[Any], operator.add]
    source: str
    destination: str
    current_place: Optional[str]
    weather_info: Optional[str]
    itinerary: Optional[List[Dict]]
