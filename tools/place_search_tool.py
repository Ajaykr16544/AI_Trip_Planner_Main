import os
from typing import Callable, List, Optional

from dotenv import load_dotenv
from langchain.tools import tool

from utils.place_info_search import GooglePlaceSearchTool, TavilyPlaceSearchTool


class PlaceSearchTool:
    def __init__(self):
        load_dotenv()
        self.google_api_key = os.environ.get("GPLACES_API_KEY", "").strip()
        self.tavily_api_key = os.environ.get("TAVILY_API_KEY", "").strip()
        self.google_places_search = (
            GooglePlaceSearchTool(self.google_api_key) if self.google_api_key else None
        )
        self.tavily_search = TavilyPlaceSearchTool()
        self.place_search_tool_list = self._setup_tools()

    def _search_with_fallback(
        self,
        place: str,
        google_search: Optional[Callable[[str], str]],
        tavily_search: Callable[[str], str],
        search_type: str,
    ) -> str:
        google_error: Optional[Exception] = None
        if google_search:
            try:
                result = google_search(place)
                if result:
                    return f"{search_type} in {place} as suggested by Google: {result}"
            except Exception as error:
                google_error = error

        if self.tavily_api_key:
            try:
                result = tavily_search(place)
                return f"{search_type} in {place}: {result}"
            except Exception as tavily_error:
                if google_error:
                    raise RuntimeError(
                        f"Google Places search failed ({google_error}); "
                        f"Tavily fallback also failed ({tavily_error})."
                    ) from tavily_error
                raise

        if google_error:
            return (
                f"Google Places search failed: {google_error}. "
                "Configure TAVILY_API_KEY to enable search fallback."
            )
        if google_search:
            return (
                f"Google Places returned no results for {place}. "
                "Configure TAVILY_API_KEY to enable search fallback."
            )
        return (
            f"Place search is unavailable for {place}. "
            "Configure GPLACES_API_KEY or TAVILY_API_KEY to enable it."
        )

    def _setup_tools(self) -> List:
        """Set up tools for searching places."""

        @tool
        def search_attractions(place: str) -> str:
            """Search attractions of a place."""
            google_search = (
                self.google_places_search.google_search_attractions
                if self.google_places_search
                else None
            )
            return self._search_with_fallback(
                place,
                google_search,
                self.tavily_search.tavily_search_attractions,
                "Attractions",
            )

        @tool
        def search_restaurants(place: str) -> str:
            """Search restaurants of a place."""
            google_search = (
                self.google_places_search.google_search_restaurants
                if self.google_places_search
                else None
            )
            return self._search_with_fallback(
                place,
                google_search,
                self.tavily_search.tavily_search_restaurants,
                "Restaurants",
            )

        @tool
        def search_activities(place: str) -> str:
            """Search activities of a place."""
            google_search = (
                self.google_places_search.google_search_activity
                if self.google_places_search
                else None
            )
            return self._search_with_fallback(
                place,
                google_search,
                self.tavily_search.tavily_search_activity,
                "Activities",
            )

        @tool
        def search_transportation(place: str) -> str:
            """Search transportation of a place."""
            google_search = (
                self.google_places_search.google_search_transportation
                if self.google_places_search
                else None
            )
            return self._search_with_fallback(
                place,
                google_search,
                self.tavily_search.tavily_search_transportation,
                "Transportation",
            )

        return [
            search_attractions,
            search_restaurants,
            search_activities,
            search_transportation,
        ]
