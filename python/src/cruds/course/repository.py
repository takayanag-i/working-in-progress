from azure.cosmos import CosmosClient

from .interface import CourseRepository

from typing import List, Dict, Optional


class CourseRepositoryImpl(CourseRepository):
    def __init__(self, cosmos: CosmosClient):
        self.cosmos = cosmos

    def find_by_course_id(self) -> Optional[List[Dict]]:
        pass
